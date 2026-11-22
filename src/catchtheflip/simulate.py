"""Stochastic simulations of monitored cat-qubit segments.

A *segment* is a memory experiment of duration `T_seg`: the memory is prepared in |alpha>,
the buffer output is monitored (photon counting or heterodyne) and at the end the memory is
read out in the Z basis (x quadrature thresholded at 0). The label of a segment is the
readout outcome: 1 if "-alpha" was read (a bit flip), 0 otherwise.

All functions return plain numpy arrays. The random keys are derived from `seed`, so a
given (model, seed, n_segments) is reproducible.
"""

from __future__ import annotations

import numpy as np

import jax
import jax.numpy as jnp
import dynamiqs as dq

from .models import Model
from .protocol import ETA_B, N_BINS, T_SEG

dq.set_precision("double")


def _keys(seed: int, n: int):
    return jax.random.split(jax.random.PRNGKey(seed), n)


def _final_states(final_state) -> np.ndarray:
    """Normalised final state vectors, shape (n, dim).

    With `save_states=False`, the event method of dynamiqs 0.3.7 returns the unnormalised
    no-click state as `final_state` (its squared norm is about 0.4 on average for the nominal
    device), so normalise for every method.
    """
    psi = np.asarray(final_state.to_jax())[..., :, 0]
    return psi / np.linalg.norm(psi, axis=-1, keepdims=True)


def _pneg(model: Model, psi: np.ndarray) -> np.ndarray:
    P = model.x_negative_projector
    return np.einsum("ki,ij,kj->k", psi.conj(), P, psi).real.clip(0.0, 1.0)


def _dither(clicktimes: np.ndarray, step: float, T_seg: float, seed: int, forward: bool) -> np.ndarray:
    """Spread click times uniformly over the integration step in which they occurred.

    Both jump integrators of dynamiqs 0.3.7 resolve a click to one integration step only:
    `EulerJump` stamps it with the start of the step, `Event` with the end of a step of
    length `dtmax`. Left as they are, click times sit on a time grid, which nothing physical
    shares: dark counts added afterwards, for example, would be recognisable at a glance.
    """
    rng = np.random.default_rng([seed, 0xD17E])  # its own stream: the trajectories do not depend on it
    shift = rng.random(clicktimes.shape) * step
    out = clicktimes + shift if forward else clicktimes - shift
    return np.sort(np.clip(out, 0.0, np.nextafter(T_seg, 0.0)), axis=-1)  # NaN padding stays last


def counting_segments(
    model: Model,
    n_segments: int,
    T_seg: float = T_SEG,
    seed: int = 0,
    dt: float = 2e-3,
    method: str = "euler",
    dtmax: float = 0.01,
    nmaxclick: int = 256,
    chunk: int = 500,
    return_states: bool = False,
    dither: bool = True,
) -> dict:
    """Photon-counting records of the buffer channel for `n_segments` independent segments.

    Args:
        model: a `Model` (single or two mode).
        n_segments: number of independent segments, each starting in |alpha>.
        T_seg: duration of a segment (units of 1/kappa_2; the default is the one of the
            challenge datasets, 200). The cost grows with the simulated time: a laptop
            simulates about one segment of 200 per second.
        seed: PRNG seed.
        dt: fixed time step of the `EulerJump` method (`method="euler"`). With the default the
            flip probability of a segment of 200 comes out about 1 % too large at nbar = 2 and
            6 % at nbar = 3.5; the published datasets use 1e-3.
        method: `"euler"` (fixed step; use `dt` <= 2e-3 for the single-mode model and
            <= 1e-3 for the two-mode model, whose Hamiltonian terms make larger steps
            unstable) or `"event"` (adaptive no-click integration with event detection, no
            time-step bias). Validate any method against `master_equation_pneg` before
            trusting it.
        dtmax: maximum step of the no-click integration for `method="event"` (sets the
            precision of click times). The default 0.01 overestimates the flip probability of
            the nominal device by about 2 %; use 0.002 for precision work.
        nmaxclick: maximum number of clicks per channel kept by the solver.
        chunk: number of segments simulated per solver call (memory control).
        return_states: also return the final conditional states.
        dither: spread every click time uniformly over the integration step in which the
            click occurred (`dt`, or `dtmax` for the event method). The integrators resolve a
            click to one step only; without dithering all click times are multiples of the
            step. The published datasets are dithered.

    Returns:
        dict with
        - `clicktimes`: array (n_segments, nmaxclick) of buffer click times, sorted and
          NaN-padded;
        - `pneg`: array (n_segments,) probability that the end-of-segment Z readout gives
          "-alpha" (the conditional state's weight on x < 0). Privileged information: the
          state is conditioned on the jumps of *every* channel, so `pneg` describes an
          observer who also counts the photons of the unmonitored channels (see
          docs/THEORY.md, section 4);
        - `nclicks`: array (n_segments, n_channels) number of jumps per channel (all
          channels, including the unmonitored ones: privileged information);
        - `channels`: tuple of channel names;
        - `T_seg`: the segment duration;
        - `states` (optional): final conditional states, shape (n_segments, dim).
    """
    if method == "euler":
        tsave = tuple(np.linspace(0.0, T_seg, 3))
        meth = dq.method.EulerJump(dt=dt)
    elif method == "event":
        tsave = np.linspace(0.0, T_seg, 3)
        meth = dq.method.Event(dtmax=dtmax)
    else:
        raise ValueError("method must be 'euler' or 'event'")
    keys = _keys(seed, n_segments)
    clicks, pneg, nclicks, states = [], [], [], []
    for start in range(0, n_segments, chunk):
        k = keys[start : start + chunk]
        res = dq.jssesolve(
            model.H, model.jump_ops, model.psi0, tsave, k, method=meth, save_states=False, nmaxclick=nmaxclick
        )
        clicks.append(np.asarray(res.clicktimes)[:, model.buffer_index, :])
        nclicks.append(np.asarray(res.nclicks))
        psi = _final_states(res.final_state)
        pneg.append(_pneg(model, psi))
        if return_states:
            states.append(psi)
    clicktimes = np.concatenate(clicks)
    if dither:
        euler = method == "euler"
        clicktimes = _dither(clicktimes, dt if euler else dtmax, T_seg, seed, forward=euler)
    out = {
        "clicktimes": clicktimes,
        "pneg": np.concatenate(pneg),
        "nclicks": np.concatenate(nclicks),
        "channels": model.channels,
        "T_seg": T_seg,
    }
    if return_states:
        out["states"] = np.concatenate(states)
    return out


def heterodyne_segments(
    model: Model,
    n_segments: int,
    T_seg: float = T_SEG,
    n_bins: int = N_BINS,
    eta: float = ETA_B,
    seed: int = 0,
    dt: float = 5e-4,
    method: str = "rouchon",
    chunk: int = 500,
    return_states: bool = False,
) -> dict:
    """Heterodyne records of the buffer channel with detection efficiency `eta`.

    `method` is `"rouchon"` (the default: the first-order scheme of Rouchon and Ralph, which
    keeps the state physical) or `"euler"` (Euler-Maruyama), both with the fixed step `dt`.
    Do not use Euler-Maruyama for the segments of the challenge: the measured operator a^2 is
    large on the Fock states of a big cat, rare large noise increments then scramble the
    state, and over 200 time units the flip probability comes out two to four times too
    large at nbar = 3.5, whatever the step. The published datasets use `"rouchon"`.

    The scheme is of first order in the step. With the default dt = 5e-4 the flip probability
    agrees with the master equation, but the mean of I of single-mode records comes out 0.01
    (nbar = 2) to 0.03 (nbar = 3.5) too low, and the variance of a bin slightly too low; both
    errors are proportional to dt, and Q is not affected. The published training records
    therefore use dt = 5e-4 / 32, the validation and test records (two-mode model, where the
    shift is about -0.004) dt = 5e-4. Use a smaller step when the baseline of I matters, and
    validate against `master_equation_pneg`.

    Heterodyne detection of the output field of channel L with efficiency eta is modelled by
    three channels: sqrt(eta/2) L measured in its X quadrature, i sqrt(eta/2) L measured in
    its X quadrature (which is the P quadrature of L), and sqrt(1 - eta) L whose record is
    discarded. All other channels of the model are unmonitored (their records are
    discarded). The recorded signals are the time averages over each bin of
        dY_I = sqrt(2 eta) Re<L> dt + dW_I,   dY_Q = -sqrt(2 eta) Im<L> dt + dW_Q,
    with the dynamiqs convention `I_k = <L_k + L_k^dagger> + dW_k/dt` for each measured channel,
    so that white noise of variance 1/(bin duration) sits on top of the signal.

    The diffusive solver unravels *every* channel diffusively, including the unmonitored ones
    whose records are discarded. The records and the labels sampled from `pneg` do not depend
    on that choice, but `pneg` itself does: here it describes an observer who also measures
    the output of the memory's loss channel with a homodyne detector, which `counting_segments`
    does not (docs/THEORY.md, section 4).

    Returns:
        dict with `I`, `Q` arrays of shape (n_segments, n_bins), `t_bins` (bin edges),
        `pneg`, `eta`, `T_seg`, and optionally `states`.
    """
    L = model.L_buffer
    others = [op for i, op in enumerate(model.jump_ops) if i != model.buffer_index]
    lost = [np.sqrt(1 - eta) * L] if eta < 1 else []  # the part of the buffer output that the detector misses
    jump_ops = [np.sqrt(eta / 2) * L, 1j * np.sqrt(eta / 2) * L, *lost, *others]
    tsave = tuple(np.linspace(0.0, T_seg, n_bins + 1))
    if method not in ("rouchon", "euler"):
        raise ValueError("method must be 'rouchon' or 'euler'")
    meth = dq.method.EulerMaruyama(dt=dt) if method == "euler" else dq.method.Rouchon1(dt=dt)
    keys = _keys(seed, n_segments)
    I, Q, pneg, states = [], [], [], []
    for start in range(0, n_segments, chunk):
        k = keys[start : start + chunk]
        res = dq.dssesolve(model.H, jump_ops, model.psi0, tsave, k, method=meth, save_states=False)
        m = np.asarray(res.measurements)
        I.append(m[:, 0, :])
        Q.append(m[:, 1, :])
        psi = _final_states(res.final_state)
        pneg.append(_pneg(model, psi))
        if return_states:
            states.append(psi)
    out = {
        "I": np.concatenate(I),
        "Q": np.concatenate(Q),
        "t_bins": np.asarray(tsave),
        "pneg": np.concatenate(pneg),
        "eta": eta,
        "T_seg": T_seg,
    }
    if return_states:
        out["states"] = np.concatenate(states)
    return out


def long_trajectory(
    model: Model,
    T: float,
    seed: int = 0,
    n_save: int | None = None,
    dt: float = 2e-3,
    method: str = "euler",
    dtmax: float = 0.01,
    nmaxclick: int = 20000,
    save_states: bool = False,
) -> dict:
    """One long jump trajectory with expectation values, to *watch* flips and bursts.

    Returns dict with `t`, `z` (<Z_L> = 1 - 2 P(x < 0), the expectation of the Z readout),
    `a` (<a>), `n` (<a^dagger a>), `nb` (<b^dagger b>, two-mode only), `clicktimes` (per
    channel, NaN-padded), `nclicks`, `channels` and optionally `states` (normalised).

    The `EulerJump` method of dynamiqs 0.3.7 keeps the norm of the state only to first order
    in `dt` between clicks (squared norms of 1.27 occur in long trajectories), and it saves
    the expectation values of that state. They are divided by the squared norm here.
    """
    n_save = n_save or int(T / 0.25) + 1
    P = dq.asqarray(jnp.asarray(model.x_negative_projector), dims=model.H.dims)
    identity = dq.asqarray(jnp.eye(model.dim), dims=model.H.dims)
    exp_ops = [P, model.a, model.a.dag() @ model.a, identity]
    if model.b is not None:
        exp_ops.append(model.b.dag() @ model.b)
    if method == "euler":
        tsave = tuple(np.linspace(0.0, T, n_save))
        meth = dq.method.EulerJump(dt=dt)
    else:
        tsave = np.linspace(0.0, T, n_save)
        meth = dq.method.Event(dtmax=dtmax)
    keys = _keys(seed, 1)
    res = dq.jssesolve(
        model.H, model.jump_ops, model.psi0, tsave, keys, exp_ops=exp_ops, method=meth,
        save_states=save_states, nmaxclick=nmaxclick,
    )
    ex = np.asarray(res.expects)[0]
    norm2 = ex[3].real  # 1 for the event method, which saves normalised states
    out = {
        "t": np.asarray(tsave),
        "z": 1.0 - 2.0 * ex[0].real / norm2,
        "a": ex[1] / norm2,
        "n": ex[2].real / norm2,
        "clicktimes": np.asarray(res.clicktimes)[0],
        "nclicks": np.asarray(res.nclicks)[0],
        "channels": model.channels,
    }
    if model.b is not None:
        out["nb"] = ex[4].real / norm2
    if save_states:
        out["states"] = np.asarray(res.states.to_jax())[0, :, :, 0] / np.sqrt(norm2)[:, None]
    return out


def master_equation_pneg(model: Model, T: float = T_SEG, n_save: int = 2, max_steps: int = 20_000_000) -> np.ndarray:
    """P("-alpha" readout)(t) from the Lindblad master equation (unconditional).

    Use it to validate an ensemble of stochastic segments: the mean of `pneg` over segments
    must agree with this value at t = T_seg. Returns the probability at `n_save` times from 0
    to T. The two-mode model needs several 10^5 solver steps for a segment of 200 (a minute
    or two on a laptop), more than the default limit of dynamiqs, hence `max_steps`.
    """
    tsave = np.linspace(0.0, T, n_save)
    rho0 = model.psi0 @ model.psi0.dag()
    P = dq.asqarray(jnp.asarray(model.x_negative_projector), dims=model.H.dims)
    res = dq.mesolve(
        model.H, model.jump_ops, rho0, tsave, exp_ops=[P], method=dq.method.Tsit5(max_steps=max_steps),
        save_states=False, progress_meter=False,
    )
    return np.asarray(res.expects)[0].real
