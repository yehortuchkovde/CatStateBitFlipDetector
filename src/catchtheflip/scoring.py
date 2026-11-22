"""Scoring of flip detectors.

Two figures of merit are used in the challenge.

**Post-selection (the leaderboard).** The detector gives every segment a score (higher =
more suspicious) and the segments with the highest scores are *discarded*. Keeping a
fraction Y of the segments (the yield), the flip probability among the kept segments is
p_kept, and the figure of merit is

    rho(Y) = p_kept / p_flip                                         (lower is better)

rho = 1 means the record carries no information, rho -> 0 means every flip was discarded.
The leaderboard uses the yield Y = 0.7 (`rho_at_yield`, `leaderboard_score`): the scorer
discards the 30 % most suspicious segments of the submission and reports the flip
suppression

    1 - rho(0.7)                                                     (higher is better)

0 means no information, 1 that every flip was discarded; it is negative if the scores point
the wrong way. The datasets mix segments of several cat sizes, and the 30 % are taken from
the whole file: scores must be comparable across cat sizes (`by_cat_size` shows where a
detector spends its budget). The leaderboard shows only this number, with two decimals; the
operating point of the decisions, the AUC and S (`evaluate`) are for the labelled validation
set. The test split is finite, so the score carries a statistical uncertainty of about
`SCORE_ERROR`, and the judges read it in points, not in ranks (`leaderboard_points`).

**Pauli-frame correction (the capstone).** If instead a flagged segment is *corrected* by a
logical X, a detector of efficiency TPR and false-alarm probability FPR leaves, per segment,

    p_eff = p_flip (1 - TPR) + (1 - p_flip) FPR

residual flips, against p_flip without heralding:

    S = p_eff / p_flip = (1 - TPR) + (1 - p_flip) FPR / p_flip        (lower is better)

S = 1 means correction brings nothing, S > 1 that it hurts. Step 4 of the challenge asks
how small S can be made, and how that compares with rho (docs/THEORY.md, section 7).
"""

from __future__ import annotations

import csv

import numpy as np

from .protocol import POINTS_FULL, POINTS_ZERO, YIELD


def confusion(decisions, labels) -> dict:
    d = np.asarray(decisions).astype(bool)
    y = np.asarray(labels).astype(bool)
    tp = int(np.sum(d & y))
    fn = int(np.sum(~d & y))
    fp = int(np.sum(d & ~y))
    tn = int(np.sum(~d & ~y))
    tpr = tp / max(tp + fn, 1)
    fpr = fp / max(fp + tn, 1)
    return {"tp": tp, "fn": fn, "fp": fp, "tn": tn, "tpr": tpr, "fpr": fpr}


def score(decisions, labels, p_flip: float | None = None) -> dict:
    """Correction score S of binary decisions against labels (see module docstring; this is
    not the leaderboard score, which is `rho_at_yield(...)["suppression"]`).

    `p_flip` defaults to the empirical flip fraction of `labels`.
    """
    c = confusion(decisions, labels)
    y = np.asarray(labels).astype(bool)
    p = float(y.mean()) if p_flip is None else float(p_flip)
    S = (1.0 - c["tpr"]) + (1.0 - p) * c["fpr"] / p
    c.update({"p_flip": p, "S": float(S)})
    return c


def roc_curve(scores, labels):
    """ROC curve (fpr, tpr, thresholds) for continuous scores, higher = more likely a flip."""
    s = np.asarray(scores, dtype=float)
    y = np.asarray(labels).astype(bool)
    order = np.argsort(-s, kind="stable")
    s, y = s[order], y[order]
    tp = np.cumsum(y)
    fp = np.cumsum(~y)
    last = np.r_[s[1:] != s[:-1], True]  # last index of each distinct score
    tpr = np.r_[0.0, tp[last] / max(y.sum(), 1)]
    fpr = np.r_[0.0, fp[last] / max((~y).sum(), 1)]
    thr = np.r_[np.inf, s[last]]
    return fpr, tpr, thr


def auc(scores, labels) -> float:
    """Area under the ROC curve (probability that a flip scores higher than a non-flip)."""
    fpr, tpr, _ = roc_curve(scores, labels)
    return float(np.trapezoid(tpr, fpr))


def best_threshold(scores, labels, p_flip: float | None = None) -> dict:
    """Threshold on `scores` that minimises the correction score S."""
    y = np.asarray(labels).astype(bool)
    p = float(y.mean()) if p_flip is None else float(p_flip)
    fpr, tpr, thr = roc_curve(scores, y)
    S = (1.0 - tpr) + (1.0 - p) * fpr / p
    k = int(np.argmin(S))
    return {"threshold": float(thr[k]), "S": float(S[k]), "tpr": float(tpr[k]), "fpr": float(fpr[k])}


def rho_at_yield(scores, labels, yield_frac: float = YIELD) -> dict:
    """Residual flip fraction when the (1 - yield_frac) highest scores are discarded.

    Segments with equal scores are ranked by their position: among them, the last ones are
    discarded first. A score with few distinct values therefore leaves the cut to chance.
    """
    s = np.asarray(scores, dtype=float)
    y = np.asarray(labels).astype(bool)
    n_keep = int(round(yield_frac * len(s)))
    order = np.argsort(s, kind="stable")  # ascending: the most suspicious come last
    keep = np.zeros(len(s), dtype=bool)
    keep[order[:n_keep]] = True
    p = float(y.mean())
    p_kept = float(y[keep].mean()) if n_keep else float("nan")
    rho = p_kept / p if p > 0 else float("nan")
    return {"yield": float(keep.mean()), "p_flip": p, "p_kept": p_kept, "rho": rho, "suppression": 1.0 - rho,
            "flips_discarded": int(y[~keep].sum()), "flips_total": int(y.sum())}


def by_cat_size(scores, labels, nbar, yield_frac: float = YIELD) -> dict:
    """Where the post-selection of the whole file spends its budget: for every cat size, the
    number of segments, the fraction of them that is discarded, and the flips discarded and
    in total. The cut is the one of `rho_at_yield` on all segments together."""
    s = np.asarray(scores, dtype=float)
    y = np.asarray(labels).astype(bool)
    nbar = np.asarray(nbar)
    n_keep = int(round(yield_frac * len(s)))
    discard = np.ones(len(s), dtype=bool)
    discard[np.argsort(s, kind="stable")[:n_keep]] = False
    out = {}
    for v in np.unique(nbar):
        m = nbar == v
        out[float(v)] = {"segments": int(m.sum()), "discarded": float(discard[m].mean()),
                         "flips_discarded": int(y[m & discard].sum()), "flips_total": int(y[m].sum())}
    return out


def postselection(decisions, labels) -> dict:
    """Post-selection at the operating point of binary decisions (1 = discard)."""
    d = np.asarray(decisions).astype(bool)
    y = np.asarray(labels).astype(bool)
    keep = ~d
    p = float(y.mean())
    p_kept = float(y[keep].mean()) if keep.any() else float("nan")
    return {"yield": float(keep.mean()), "p_flip": p, "p_kept": p_kept, "rho": p_kept / p if p > 0 else float("nan")}


def postselection_curve(scores, labels, yields=None):
    """rho as a function of the yield Y (trade-off curve of a detector)."""
    yields = np.linspace(0.5, 1.0, 51) if yields is None else np.asarray(yields)
    return yields, np.array([rho_at_yield(scores, labels, float(Y))["rho"] for Y in yields])


def write_submission(path, scores, decisions) -> None:
    """Write a submission CSV with columns segment_id, score, decision."""
    scores = np.asarray(scores, dtype=float)
    decisions = np.asarray(decisions).astype(int)
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["segment_id", "score", "decision"])
        for i, (s, d) in enumerate(zip(scores, decisions)):
            w.writerow([i, f"{s:.6g}", int(d)])


def read_submission(path) -> dict:
    ids, scores, decisions = [], [], []
    with open(path, newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            ids.append(int(row["segment_id"]))
            scores.append(float(row["score"]))
            decisions.append(int(row["decision"]))
    ids = np.asarray(ids)
    order = np.argsort(ids)
    return {"segment_id": ids[order], "score": np.asarray(scores)[order], "decision": np.asarray(decisions)[order]}


def evaluate(scores, decisions, labels, p_flip: float | None = None, yield_frac: float = YIELD) -> dict:
    """Every number of a detector: the leaderboard post-selection at the reference yield
    (from the scores; its "suppression" is the leaderboard score), the post-selection at the
    decisions, the AUC, and the correction score S."""
    return {
        "leaderboard": rho_at_yield(scores, labels, yield_frac),
        "operating_point": postselection(decisions, labels),
        "auc": auc(scores, labels),
        "correction": score(decisions, labels, p_flip),
    }


def _read_checked(submission_path, labels):
    sub = read_submission(submission_path)
    if len(sub["decision"]) != len(labels) or np.any(sub["segment_id"] != np.arange(len(labels))):
        raise ValueError("submission must contain exactly one row per segment, segment_id = 0..n-1")
    return sub


def score_submission(submission_path, labels, p_flip: float | None = None, yield_frac: float = YIELD) -> dict:
    """`evaluate` a submission CSV against labels."""
    labels = np.asarray(labels)
    sub = _read_checked(submission_path, labels)
    return evaluate(sub["score"], sub["decision"], labels, p_flip, yield_frac)


def leaderboard_score(submission_path, labels, yield_frac: float = YIELD) -> float:
    """The leaderboard score of a submission CSV: the flip suppression 1 - rho_70 (higher is better)."""
    labels = np.asarray(labels)
    return rho_at_yield(_read_checked(submission_path, labels)["score"], labels, yield_frac)["suppression"]


def leaderboard_points(suppression: float, scale: float = 10.0) -> float:
    """Points of the leaderboard criterion for a score 1 - rho_70 (CHALLENGE.md, step 3).

    No points up to `POINTS_ZERO`, the score of a detector that discards the smallest cats
    without looking at any record; `scale` points from `POINTS_FULL`; linear in between. The
    judges grade the points, not the rank: differences below the statistical uncertainty of
    the score (`protocol.SCORE_ERROR`) move them by a few percent of the scale.
    """
    return scale * float(np.clip((suppression - POINTS_ZERO) / (POINTS_FULL - POINTS_ZERO), 0.0, 1.0))
