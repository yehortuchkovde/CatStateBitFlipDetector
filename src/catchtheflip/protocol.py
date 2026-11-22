"""The protocol of the challenge datasets, in one place (CHALLENGE.md, device sheet).

A *segment* is one memory experiment: the cat is prepared in |+alpha>, idles for `T_SEG`
while the buffer output is monitored, and is read out in the Z basis. The datasets hold
segments of the same device at the cat sizes `CAT_SIZES`, mixed in one file, and the
leaderboard keeps the fraction `YIELD` of the segments of the test file.

Two datasets: the heterodyne records (dataset "tier B") are the ones of the challenge and of
the leaderboard; the click records (dataset "tier A") are the data of tutorial 5 and a tool
for the physics questions, with nothing to submit.
"""

T_SEG = 200.0  # duration of a segment, in units of 1/kappa_2
CAT_SIZES = (2.0, 2.5, 3.0, 3.5)  # cat sizes nbar = alpha^2 of the datasets
YIELD = 0.7  # the leaderboard discards the 30 % most suspicious segments

SCORE_ERROR = 0.015  # statistical uncertainty of the leaderboard score 1 - rho_70 (finite test split)
POINTS_ZERO = 0.30  # leaderboard score worth no points: what "discard the smallest cats" gets without any record
POINTS_FULL = 0.55  # leaderboard score worth full points (CHALLENGE.md, step 3)

ETA_A = 0.8  # click records (tier A): efficiency of the photon counter
DARK_RATE = 0.02  # click records (tier A): dark counts per unit time
ETA_B = 1.0  # heterodyne records (tier B): efficiency of the detection (an ideal detector)
N_BINS = 400  # heterodyne records (tier B): bins per segment (bin duration T_SEG / N_BINS = 0.5)


def fock_cutoff(nbar: float) -> int:
    """Fock cutoff of the memory used for the datasets at cat size `nbar`."""
    return 24 if nbar <= 2.5 else 28
