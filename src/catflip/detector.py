"""Step 3, extracted from the submitted solution without changing its score.

Theory: docs/AlmostLinearResponseTheoryModel.pdf, equations (32), (48), (49).
The PDF's last paragraph describes an earlier demeaned Fourier variant; the final
submitted implementation below intentionally uses the raw I window for F.
"""
import numpy as np

PHYSICS = dict(kappa_b=4.0, kappa2=1.0, kappa1=0.02, kappa_phi=0.02)


def omega_gamma(nbar, **physics):
    """K=0 local relaxation, not the logical bit-flip rate Gamma_Z.

    kappa_b=4 is the Tutorial 4 reference, not a fitted hidden-device constant.
    """
    kb, k2, k1, kp = (physics.get(k, v) for k, v in PHYSICS.items())
    omega2 = k2 * kb * np.asarray(nbar) - (kb - k1 - kp) ** 2 / 16
    if np.any(omega2 <= 0):
        raise ValueError("Overdamped response: no real oscillation frequency.")
    return np.sqrt(omega2), (kb + k1 + kp) / 4


def sliding_fourier_witness(I, Q, nbar, dt, baseline_by_cat, window_time=2.0):
    """One signed DC maximum D and Fourier-power maximum F per segment.

    All overlapping windows advance one bin. With L bins and T=L*dt:
      D = max_m sqrt(T) * (baseline - mean(I[m:m+L]))
      F = max_m T * |mean(I[m:m+L] * exp(-i*Omega*r*dt))|**2
    D and F may attain their maxima in different windows. Q is checked for the
    expected shape but is not used by the submitted score. No frequency search.
    """
    I, Q, nbar = np.asarray(I), np.asarray(Q), np.asarray(nbar)
    if I.ndim != 2 or Q.shape != I.shape or nbar.shape != (len(I),):
        raise ValueError("I,Q must be (segments,bins); nbar must be (segments,).")
    if dt <= 0 or not np.isfinite(I).all() or not np.isfinite(Q).all():
        raise ValueError("Use finite records and positive dt.")
    length = round(window_time / dt)
    if not 2 <= length <= I.shape[1]:
        raise ValueError("Window must contain 2..n_bins samples.")
    T = length * dt
    D, F = np.empty(len(I)), np.empty(len(I))
    for cat in np.unique(nbar):
        omega, _ = omega_gamma(cat)
        if omega >= np.pi / dt:
            raise ValueError("Predicted Omega exceeds Nyquist.")
        phase = np.exp(-1j * np.arange(length)[:, None] * dt * omega)
        indices = np.flatnonzero(nbar == cat)
        baseline = baseline_by_cat[str(float(cat))]
        for start in range(0, len(indices), 512):
            rows = indices[start:start + 512]
            windows = np.lib.stride_tricks.sliding_window_view(
                I[rows].astype(np.float64), length, axis=1)
            D[rows] = np.sqrt(T) * (baseline - windows.mean(axis=-1)).max(axis=1)
            power = T * np.abs(windows @ phase / length) ** 2
            F[rows] = power.max(axis=-1).max(axis=1)
    return D, F


def training_split(train):
    """Original seed-2026 70/30 split, stratified by (cat size, readout label)."""
    rng = np.random.default_rng(2026)
    fit, heldout = [], []
    for cat in np.unique(train['nbar']):
        for label in (0, 1):
            rows = np.flatnonzero((train['nbar'] == cat) & (train['labels'] == label))
            rows = rng.permutation(rows)
            cut = round(0.7 * len(rows))
            fit.extend(rows[:cut]); heldout.extend(rows[cut:])
    return np.sort(fit), np.sort(heldout)


def calibrate(train, fit):
    """Estimate 22 training-only statistics; no physical constants or weights fit.

    Four I baselines + four cats * (D,F centers and scales) + two cat-score stats.
    Labels determine stratification, not the baselines, centers or scales.
    """
    cats = np.unique(train['nbar'])
    baseline = {}
    for cat in cats:
        rows = fit[train['nbar'][fit] == cat]
        baseline[str(float(cat))] = float(np.median(
            train['I'][rows].mean(axis=1, dtype=np.float64)))
    dt = train['meta']['T_seg'] / train['I'].shape[1]
    D, F = sliding_fourier_witness(train['I'], train['Q'], train['nbar'], dt, baseline)
    scales = {}
    for cat in cats:
        rows = fit[train['nbar'][fit] == cat]
        scales[str(float(cat))] = {}
        for name, values in [('D', D), ('F', F)]:
            x = values[rows]
            scale = max(float(np.subtract(*np.percentile(x, [75, 25])) / 1.349), 1e-12)
            scales[str(float(cat))][name] = [float(np.median(x)), scale]
    cat_values = -train['nbar'][fit]
    return dict(baseline=baseline, scales=scales,
                cat=[float(cat_values.mean()), float(cat_values.std())],
                dt=float(dt), window_time=2.0, physics=PHYSICS)


def my_detector(nbar, I, Q, calibration, mode='DC+Omega', include_cat=True):
    """Final S=(z_D+z_F)/2+z_C at T=2: higher means more suspicious.

    Retained among the evaluated F-containing candidates for its training
    suppression at 70% yield. The fixed 1/2,1/2,1 weights were not optimized.
    DC+cat tied training suppression and had higher AUC; F's added value is small.
    No clipping, fitted frequency, per-cat flip prior, or nbar division is used.
    Other modes below are ablations, never selected on validation labels.
    """
    nbar = np.asarray(nbar)
    D, F = sliding_fourier_witness(I, Q, nbar, calibration['dt'],
                                 calibration['baseline'], calibration['window_time'])
    zD, zF = np.empty(len(nbar)), np.empty(len(nbar))
    for cat in np.unique(nbar):
        rows = nbar == cat
        for name, values, output in [('D', D, zD), ('F', F, zF)]:
            center, scale = calibration['scales'][str(float(cat))][name]
            output[rows] = (values[rows] - center) / scale
    center, scale = calibration['cat']
    zC = (-nbar - center) / scale
    if mode == 'cat only':
        return zC
    score = {'DC': zD, 'Omega': zF, 'DC+Omega': (zD + zF) / 2}[mode]
    return score + zC if include_cat else score
