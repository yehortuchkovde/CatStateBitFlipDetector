# Wigner trajectory: measurement choice and reproducibility

`main.py --wigner-only` produces `figures/stochastic_trajectory.png` and
`figures/wigner_transition.gif` from the **same** saved trajectory in
`outputs/wigner_trajectory.npz`. The animation is a 26-time-unit zoom around the
first zero crossing of the simulated logical-Z expectation; it has a moving
cursor on the state trace and buffer-emission plot, with actual buffer-click
times from that simulation. Orange is a conditional emission rate, not another
measured heterodyne channel. It is not an animation of a validation record.

The model is the known nominal single-mode device, `nbar=2`, `N=24`, with the
original challenge rates and `dt=0.001`. Seed **7** was selected because it shows
a resolved switch that stays in the negative lobe. This is an illustration of a
transition, not a representative draw for estimating its frequency, and it is
never used to calibrate the detector. All parameters and the selection rationale
are recorded in `outputs/wigner_demo.json`.

## Why the environmental measurement matters

A quantum trajectory is a state conditioned on a particular measurement of the
environment. Direct photon counting of every original channel can leave a
logical superposition rather than a localized state moving between the lobes.
For this visualization, the otherwise unobserved memory-loss output is counted
after interference with a real local oscillator of amplitude `beta=1`:

$$
L_1'=L_1+\beta\mathbb I,\qquad
H'=H+\frac{i\beta}{2}(L_1^\dagger-L_1).
$$

This measurement distinguishes the two lobes in the full conditioned state.
It changes the unraveling, **not the unconditional physical device**, because

$$
-i[H',\rho]+\mathcal D[L_1']\rho
=-i[H,\rho]+\mathcal D[L_1]\rho.
$$

The code verifies equality of the complete Liouvillian matrices to numerical
precision; the maximum entrywise difference is about `7e-15`. The buffer jump
operator is untouched, so the corresponding buffer click process is still that
of the original nominal model. The state shown is privileged full-environment
information, not a reconstruction obtainable from buffer clicks alone. This
does not modify the detector or its interpretation of the supplied datasets.
For background on measurement-dependent quantum trajectories, see
[Verstraelen and Wouters, Appendix A](https://doi.org/10.3390/app8091427).

## What is rendered

Every frame is computed with `dynamiqs.wigner` from the actual saved state
$\rho(t)=|\psi(t)\rangle\langle\psi(t)|$, with
$x=(a+a^\dagger)/2$, $p=(a-a^\dagger)/(2i)$ and $[x,p]=i/2$.
Coherent-state centers are therefore at $(\pm\alpha,0)$. The color scale stays
fixed throughout; blue values are negative Wigner interference, not negative
probabilities. The state can split into two lobes and develop fringes during the
transition: the animation does not prescribe a rigid Gaussian blob moving
along an invented path. `dq.wigner` arrays are transposed for plotting so that
the x and p axes have the correct orientation.

The complete trace lasts 200 time units, with states saved every 0.1 units.
The GIF displays every second saved state in the zoom, at 12 frames per second.
The saved trajectory is reused when present; delete `outputs/wigner_trajectory.npz`
to rerun the seed-7 stochastic simulation.
