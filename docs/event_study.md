# State-timed simulated transition spectra

The challenge provides end-of-segment readouts, not flip timestamps. This separate
experiment asks whether measured Fourier power changes during *state-defined*
transitions of a known device; it does not infer the hidden device or tune S.

## Model and measurement

`src/catflip/event_study.py` uses the unchanged Alice & Bob `two_mode` builder:
`nbar=2`, `kappa2=1`, `kappa_b=4`, `g2=1`, `kappa1=kappa_phi=0.02`, `nth=0.1`,
`K=0`, memory/buffer Fock dimensions 16/8. These are reference constants, not fits.
The theory predicts Omega=2.6495 and gamma=1.01 (see the original theory PDF).

100 histories start in |+alpha,0> and run to T=800 using `dssesolve`, Rouchon1
step 0.0005, complex128 arithmetic, saved spacing 0.1, PRNG seed 907. Buffer
operators L_b/sqrt(2) and i L_b/sqrt(2) produce genuine heterodyne records at
**eta=1**. The other environment channels are homodyne-unravelled too, allowing
a localized **privileged** conditional state and its Z expectation. This leaves
the unconditional Lindblad generator unchanged, but its full-state Z is not a
buffer-only experimental observer's reconstructed state; event statistics depend
on the chosen unraveling. The buffer records are the solver's noisy measurement
outputs, not conditional means with independently fabricated noise added.
This is not a reproduction of the supplied dataset's detection efficiency.

The CPU reference run took 1106.5 seconds. Maximum highest-Fock-level populations
were 6.38e-5 (memory) and 2.62e-4 (buffer). These are truncation diagnostics,
not a cutoff/time-step convergence study or a precision flip-rate estimate.
The full raw trajectory cache is ignored by git; compact measured windows are bundled.

## Event and control selection

Confirm positive or negative logical plateaus only after |Z|>=0.8 persists for
one time unit. Opposite confirmed plateaus define a transition. Its anchor is
the midpoint (rounded down to a saved sample) of the largest *directed* Z change
over 0.5 time units between the plateaus. The last directed zero-crossing time
is also recorded for auditing. This rule depends only on Z, not on spectral power.
Rapid unconfirmed recrossings are excluded; a quantum trajectory does not have
an unraveling-independent classical flip timestamp.

There were 155 confirmed transitions; 140 passed the fixed boundary and isolation
requirements for 16-unit context windows. Cycle through history IDs before using
a second event from a history, stopping at 100 event/control pairs. Each random
control is from the same trajectory and starting logical side, with confirmed
same-side endpoints and no confirmed transition intersecting its context.
Controls cannot overlap each other. I/Q amplitude never selects events or controls.
The 100 pairs come from 74 independent histories, not 100 independent histories.
Control RNG seed: 2028.

## Spectra and uncertainty

Rebin actual I/Q records from 0.1 to 0.5 units; take fixed 3-, 4- or 16-bin windows
centered at each anchor. For odd length, use the earlier half-bin alignment.
Subtract each window mean, then evaluate |sum(x_r exp(-i omega r dt))/L|^2.
Divide by the unselected white-noise expectation
`(1-|mean(exp(-i omega r dt))|^2)/(L*dt)` to account for local demeaning.
State-based selection can change the conditional noise distribution; power above
one is not itself a significance test. The comparison is against matched controls.

Average power across windows, with 2000 paired cluster bootstrap draws (seed
2029): resample *whole histories*, retaining all their pairs and event/control
pairing. Bands are pointwise percentile 95% intervals, exploratory and without
multiple-comparison correction. The continuous frequency grid displays exact
finite-window projections, not additional independent DFT bins. Dotted vertical
Omega markers denote frequency; a horizontal Omega marker on a power axis would
be dimensionally incorrect.

Short-window I power at Omega is higher during transitions, but the difference
is broad. The 16-bin I difference at Omega is inconclusive, so these results do
not demonstrate a sharply localized spectral peak, a hidden-device Omega, or
a reliable incremental contribution of F to detection. Q is shown without
suppressing unfavorable comparisons. The submitted detector is unchanged.

## Reproduce

```
uv run python main.py --event-study
uv run --extra cuda python main.py --resimulate-events
```

The first command replots `outputs/simulated_event_windows.npz`, reading provenance
from `outputs/simulated_event_study.json`; no simulation is required. The second
regenerates all 100 histories and selection, saving an ignored full cache at
`outputs/event_study_trajectories.npz`. CPU simulation is supported, but the saved
reference run was already close to the challenge's 20-minute compute guideline.

Compact NPZ keys: trajectory IDs, starting signs, event/control sample centers,
all selected event metadata (JSON including zero-crossing times), candidate/eligible
counts, I/Q context windows (100x160), and direction-normalized Z (100x161).
Window centers index the original 0.1-unit saved grid. Only Z is sign-aligned;
I/Q spectra use the measured records unchanged. All fitted detector statistics
and the dataset evaluation pipeline remain separate.
