"""Measurement records: detector imperfections, binning, datasets on disk and on Aqora."""

from __future__ import annotations

import json
import os
import re

import numpy as np

# The challenge data on Aqora: one dataset per tier, one row per segment, a column `split`.
AQORA_DATASETS = {"A": "Alice_Bob/catch-the-flip-tier-a", "B": "Alice_Bob/catch-the-flip-tier-b"}
AQORA_VERSION = "v1.0.0"
_SPLIT_FILE = re.compile(r"tier([AB])_(train|val|test)\.npz")


def pad_clicks(click_lists, nmax: int | None = None) -> np.ndarray:
    """Stack a list of 1-d click-time arrays into a NaN-padded (n, nmax) array."""
    nmax = nmax or max((len(c) for c in click_lists), default=1)
    nmax = max(nmax, 1)
    out = np.full((len(click_lists), nmax), np.nan)
    for i, c in enumerate(click_lists):
        c = np.asarray(c)[:nmax]
        out[i, : len(c)] = np.sort(c)
    return out


def unpad_clicks(clicktimes: np.ndarray) -> list:
    """Inverse of `pad_clicks`: list of sorted 1-d arrays without the NaNs."""
    return [np.sort(row[~np.isnan(row)]) for row in clicktimes]


def apply_counting_imperfections(
    clicktimes: np.ndarray, T_seg: float, eta: float = 1.0, dark_rate: float = 0.0, rng=None, nmax: int | None = None
) -> np.ndarray:
    """Finite detection efficiency and dark counts for photon-counting records.

    A detector of efficiency `eta` registers each emitted photon independently with
    probability eta (random thinning), and adds dark counts as a Poisson process of rate
    `dark_rate` (per unit time), uniform over [0, T_seg).
    """
    rng = np.random.default_rng(rng)
    out = []
    for c in unpad_clicks(clicktimes):
        c = c[rng.random(len(c)) < eta]
        n_dark = rng.poisson(dark_rate * T_seg)
        c = np.concatenate([c, rng.random(n_dark) * T_seg])
        out.append(np.sort(c))
    return pad_clicks(out, nmax or clicktimes.shape[1])


def bin_clicks(clicktimes: np.ndarray, T_seg: float, n_bins: int) -> np.ndarray:
    """Histogram the click times of each segment into `n_bins` equal bins: array (n, n_bins)."""
    edges = np.linspace(0.0, T_seg, n_bins + 1)
    out = np.zeros((clicktimes.shape[0], n_bins), dtype=np.int32)
    for i, c in enumerate(unpad_clicks(clicktimes)):
        out[i] = np.histogram(c, bins=edges)[0]
    return out


def add_gaussian_noise(records: np.ndarray, sigma: float, rng=None) -> np.ndarray:
    """Add classical white noise (amplifier noise) of standard deviation `sigma` per bin."""
    rng = np.random.default_rng(rng)
    return records + sigma * rng.standard_normal(records.shape)


def sample_labels(pneg: np.ndarray, rng=None) -> np.ndarray:
    """Sample the end-of-segment Z readout: label 1 ("-alpha", a flip) with probability pneg."""
    rng = np.random.default_rng(rng)
    return (rng.random(len(pneg)) < pneg).astype(np.int8)


def save_dataset(path, meta: dict | None = None, **arrays) -> None:
    """Save arrays plus a JSON `meta` dict into an .npz file."""
    np.savez_compressed(path, meta=json.dumps(meta or {}), **arrays)


def load_dataset(path) -> dict:
    """Load an .npz dataset written by `save_dataset`; `meta` is returned as a dict.

    The six files of the challenge, `tierA_train.npz` to `tierB_test.npz`, are also stored
    on Aqora as two datasets. If `path` is one of these names and the file does not exist
    (the Aqora workspace has no data files), the split is read from Aqora with `load_aqora`
    and comes back in the same layout.
    """
    if isinstance(path, (str, os.PathLike)) and not os.path.exists(path):
        split_file = _SPLIT_FILE.fullmatch(os.path.basename(path))
        if split_file:
            return load_aqora(split_file[1], split_file[2])
    with np.load(path, allow_pickle=False) as f:
        d = {k: f[k] for k in f.files}
    d["meta"] = json.loads(str(d["meta"]))
    return d


def load_aqora(tier: str, split: str, version: str = AQORA_VERSION) -> dict:
    """Load one split ("train", "val" or "test") of a tier ("A" or "B") from its Aqora dataset.

    The datasets are https://aqora.io/datasets/Alice_Bob/catch-the-flip-tier-a and
    https://aqora.io/datasets/Alice_Bob/catch-the-flip-tier-b: Parquet tables with one row
    per segment. The result has the layout of the .npz files: `nbar`, `labels` (not for the
    test split), `clicktimes` padded with NaN (tier A) or `I` and `Q` (tier B), and `meta`.
    Row i is the segment of `segment_id` i.

    Inside an Aqora workspace the kernel is already signed in. Elsewhere, install the reader
    with `pip install "aqora[pyarrow]"` and run `aqora login` once.
    """
    try:
        import pyarrow.compute as pc
        from aqora.pyarrow import dataset
    except ImportError as error:
        raise ImportError('reading the Aqora datasets needs the package "aqora[pyarrow]"') from error

    table = dataset(AQORA_DATASETS[tier], version).to_table(filter=pc.field("split") == split)
    if len(table) == 0:
        raise ValueError(f"no split {split!r} in {AQORA_DATASETS[tier]} {version}")
    segment_id = table["segment_id"].to_numpy()
    if not np.array_equal(segment_id, np.arange(len(table))):
        table = table.take(np.argsort(segment_id))
    d = {"nbar": table["nbar"].to_numpy()}
    if table["label"].null_count == 0:
        d["labels"] = table["label"].to_numpy()
    if tier == "A":
        column = table["clicktimes"].combine_chunks()
        counts = column.value_lengths().to_numpy()
        clicktimes = np.full((len(column), counts.max() + 1), np.nan)
        clicktimes[np.arange(clicktimes.shape[1])[None, :] < counts[:, None]] = column.flatten().to_numpy()
        d["clicktimes"] = clicktimes
    else:
        for key in ("I", "Q"):
            column = table[key].combine_chunks()
            d[key] = column.flatten().to_numpy().reshape(len(column), -1).astype(np.float16)
    d["meta"] = {**json.loads(table.schema.metadata[b"catchtheflip"]), "n": len(table)}
    return d
