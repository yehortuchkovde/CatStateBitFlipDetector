# Measurement records

These are **simulated quantum measurement records**, not laboratory measurements.
Both complete challenge datasets are included locally under their original MIT
license; see [LICENSE](LICENSE), [manifest.json](manifest.json), and the official
[Tier B](https://aqora.io/datasets/Alice_Bob/catch-the-flip-tier-b) and
[Tier A](https://aqora.io/datasets/Alice_Bob/catch-the-flip-tier-a) pages.

| File | Observable | Device | Rows | Labels |
|---|---|---|---:|---|
| `tierB_train.npz` | Heterodyne I,Q | Nominal single-mode | 15,000 | Yes |
| `tierB_val.npz` | Heterodyne I,Q | Hidden two-mode + Kerr | 7,500 | Yes |
| `tierB_test.npz` | Heterodyne I,Q | Hidden two-mode + Kerr | 22,500 | No |
| `tierA_train.npz` | Photon click times | Nominal single-mode | 30,000 | Yes |
| `tierA_val.npz` | Photon click times | Hidden two-mode + Kerr | 15,000 | Yes |
| `tierA_test.npz` | Photon click times | Hidden two-mode + Kerr | 30,000 | No |

Every segment starts in `|+alpha>` and ends with a Z readout at `T_seg=200`, in
units of `1/kappa2`. **Label 1 means the final readout was `-alpha`**; it is not
an annotation of a burst time, and a trajectory can undergo multiple excursions.
The four cat sizes `nbar=alpha**2` are 2, 2.5, 3, and 3.5, mixed in the proportions
1:2:4:8 and shuffled. The known noise parameters are `kappa1=kappa_phi=0.02`,
`nth=0.1`, and `kappa2=1`.

Each archive contains `nbar` (float64), `labels` (int8, only train/val), and
`meta` (a JSON string). Load with `numpy.load(path, allow_pickle=False)`, or use
`catflip.data.load` to decode metadata. Tier B additionally contains `I,Q`, each
float16 with shape `(rows,400)`: bin-averaged records at `dt=0.5`, efficiency
`eta=1`, and bin noise standard deviation `1/sqrt(dt)=sqrt(2)`.
Tier A contains sorted `clicktimes`, padded with NaNs; efficiency and dark counts
are already applied and recorded in `meta`.

Tier A and Tier B are **separate experiments**, not aligned modalities of the
same segment; row numbers must not be paired. Tier A illustrates photon bursts
and is never used by the scored heterodyne detector.

Training uses a nominal single-mode model. The hidden validation/test device has
a finite-bandwidth buffer and a small Kerr nonlinearity; its noise rates and cat
sizes remain nominal. The hidden buffer parameters and test seeds are private.
The heterodyne simulator's finite integration step shifts validation/test mean I
by about -0.004; this baseline offset should not be interpreted as device physics.

The files are supplied, so normal runs require no Aqora account or network.
`uv sync --extra download` followed by `uv run python scripts/fetch_data.py`
can restore the six published splits; this downloads records and never regenerates
private test data. The script checks array-content hashes against the manifest.
