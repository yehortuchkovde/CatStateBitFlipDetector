"""Event-resolved statistics of a KNOWN two-mode reference device.

The published datasets have final readout labels, not transition timestamps.
This separate simulation uses full, privileged conditioned <Z> to define events.
The saved I,Q are actual diffusive solver records, not noise added after a run.
This reference uses ideal buffer detection (eta=1), not the dataset's efficiency.
"""
import json
import time
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from .detector import omega_gamma

CONFIG = dict(n_trajectories=100, duration=800., integration_dt=.0005,
              saved_dt=.1, seed=907, nbar=2., kappa_b=4., Na=16, Nb=8)


def simulate_reference(output, force=False):
    """Pure-state diffusive unraveling of every environment channel.

    The loss-channel homodyne record distinguishes the lobes in this privileged
    state. Only the first two (buffer heterodyne) records are analyzed. Dropping
    the other detector records does not change their marginal distribution, but
    <Z> of the full state is NOT available to a buffer-only experimental observer.
    """
    cache = output / 'event_study_trajectories.npz'
    if cache.exists() and not force:
        with np.load(cache, allow_pickle=False) as archive:
            result = {key: archive[key] for key in archive.files}
        if json.loads(str(result['config'])) != CONFIG:
            raise ValueError('Event-study cache has different parameters; move it to regenerate.')
        return result
    import jax
    import dynamiqs as dq
    from catchtheflip import models
    dq.set_precision('double')
    p = models.TwoModeParams(nbar=CONFIG['nbar'], kappa_b=CONFIG['kappa_b'],
                            Na=CONFIG['Na'], Nb=CONFIG['Nb'])
    model = models.two_mode(p)
    L = model.L_buffer
    operators = [L/np.sqrt(2), 1j*L/np.sqrt(2), *model.jump_ops[1:]]
    Z = dq.asqarray(np.eye(model.dim)-2*model.x_negative_projector, dims=model.H.dims)
    top_memory = dq.tensor(dq.fock_dm(p.Na, p.Na-1), dq.eye(p.Nb))
    top_buffer = dq.tensor(dq.eye(p.Na), dq.fock_dm(p.Nb, p.Nb-1))
    times = tuple(np.arange(round(CONFIG['duration']/CONFIG['saved_dt'])+1)*CONFIG['saved_dt'])
    keys = jax.random.split(jax.random.PRNGKey(CONFIG['seed']), CONFIG['n_trajectories'])
    print(f"Simulating {CONFIG['n_trajectories']} known two-mode trajectories, T={CONFIG['duration']:g}, "
          f"dim={model.dim}, backend={jax.default_backend()}...", flush=True)
    started = time.monotonic()
    result = dq.dssesolve(model.H, operators, model.psi0, times, keys,
                          exp_ops=[Z, model.b, top_memory, top_buffer],
                          method=dq.method.Rouchon1(dt=CONFIG['integration_dt']), save_states=False)
    expects = np.asarray(result.expects)
    records = np.asarray(result.measurements)
    data = dict(config=json.dumps(CONFIG), params=json.dumps(p.to_dict()),
                t=np.asarray(times), z=expects[:, 0].real, b=expects[:, 1],
                top_memory=expects[:, 2].real, top_buffer=expects[:, 3].real,
                I=records[:, 0], Q=records[:, 1],
                elapsed_seconds=time.monotonic()-started, backend=jax.default_backend())
    np.savez_compressed(cache, **data)
    print('Reference simulation saved after', round(float(data['elapsed_seconds']), 1), 'seconds.', flush=True)
    return data


def z_transitions(z, dt, threshold=.8, hold_time=1., change_time=.5):
    """Confirm +/- logical plateaus, then timestamp a switch from Z alone.

    Opposite plateaus must each persist for 1 time unit beyond |Z|>=0.8. The
    event anchor is the midpoint of the largest directed drop over 0.5 units
    between them (rounded down to a saved sample). Zero-crossing times are also
    retained, so the choice can be audited; neither uses I,Q or Fourier power.
    """
    hold, step = round(hold_time/dt), round(change_time/dt)
    flags = np.zeros(len(z), dtype=np.int8)
    for sign in (1, -1):
        cumulative = np.r_[0, np.cumsum(sign*z >= threshold)]
        flags[hold-1:][cumulative[hold:]-cumulative[:-hold] == hold] = sign
    valid = np.flatnonzero(flags)
    changes = np.flatnonzero(np.diff(flags[valid]) != 0)+1
    events = []
    for position in changes:
        left, right = int(valid[position-1]), int(valid[position])
        sign = int(flags[left])
        indices = np.arange(left, right-step+1)
        if not len(indices):
            continue
        first = int(indices[np.argmax(sign*(z[indices]-z[indices+step]))])
        anchor = first + step//2
        segment = sign*z[left:right+1]
        crossings = np.flatnonzero((segment[:-1] >= 0) & (segment[1:] < 0))
        if not len(crossings):
            continue
        crossing = left+int(crossings[-1])
        fraction = float(z[crossing]/(z[crossing]-z[crossing+1]))
        events.append(dict(left=left, right=right, anchor=anchor, before=sign,
                           zero_crossing_time=(crossing+fraction)*dt))
    return events


def select_event_windows(data, target=100):
    """Pair state-defined event windows with non-transition windows in the same run.

    A round-robin over trajectory IDs uses each eventful history before taking
    a second event from one history. Events cannot overlap. Control endpoints
    must be on the same confirmed logical side, with no confirmed transition in
    their context; non-flip disturbances are not excluded by I/Q amplitude.
    """
    dt = CONFIG['saved_dt']
    context = round(16/dt)
    half = context//2
    rng = np.random.default_rng(2028)
    per_trajectory, all_events = [], []
    for trajectory, z in enumerate(data['z']):
        events = z_transitions(z, dt)
        all_events.append(events)
        eligible = []
        for event in events:
            center = event['anchor']
            if center < half or center+half >= len(z):
                continue
            if any(other is not event and abs(other['anchor']-center) < context for other in events):
                continue
            eligible.append(dict(event, trajectory=trajectory))
        per_trajectory.append(eligible)
    ordered = []
    for ordinal in range(max(map(len, per_trajectory), default=0)):
        ordered.extend(events[ordinal] for events in per_trajectory if ordinal < len(events))
    selected, used_controls = [], {j: [] for j in range(len(data['z']))}
    for event in ordered:
        trajectory = event['trajectory']; z = data['z'][trajectory]
        centers = np.arange(half, len(z)-half)
        sign = event['before']
        hold = round(1/dt)
        cumulative = np.r_[0, np.cumsum(sign*z >= .8)]
        confirmed = np.zeros(len(z), dtype=bool)
        confirmed[hold-1:] = cumulative[hold:]-cumulative[:-hold] == hold
        good = confirmed[centers-half] & confirmed[centers+half]
        for other in all_events[trajectory]:
            good &= ((centers+half < other['left']) | (centers-half > other['right']))
        for previous in used_controls[trajectory]:
            good &= abs(centers-previous) >= context
        candidates = centers[good]
        if not len(candidates):
            continue
        control = int(rng.choice(candidates))
        used_controls[trajectory].append(control)
        selected.append(dict(event, control=control))
        if len(selected) == target:
            break
    if not selected:
        raise ValueError('No eligible event/control pairs; no figure can be claimed.')
    result = dict(trajectory=np.array([x['trajectory'] for x in selected]),
                  before=np.array([x['before'] for x in selected]),
                  event_center=np.array([x['anchor'] for x in selected]),
                  control_center=np.array([x['control'] for x in selected]),
                  candidate_count=sum(map(len, all_events)),
                  eligible_count=len(ordered), metadata=json.dumps(selected))
    for name in ('I', 'Q'):
        for group, key in [('event', 'anchor'), ('control', 'control')]:
            result[f'{name}_{group}'] = np.stack([
                data[name][x['trajectory'], x[key]-half:x[key]+half] for x in selected])
    for group, key in [('event', 'anchor'), ('control', 'control')]:
        result[f'z_{group}'] = np.stack([
            data['z'][x['trajectory'], x[key]-half:x[key]+half+1]*x['before'] for x in selected])
    return result


def _paired_cluster_means(event, control, trajectory, rng, repetitions=2000):
    """Resample full trajectories, retaining their event/control pairs together."""
    ids = np.unique(trajectory)
    if len(ids) < 2:
        raise ValueError('At least two independent histories are needed for uncertainty.')
    counts = np.array([np.sum(trajectory == index) for index in ids])
    event_sum = np.stack([event[trajectory == index].sum(axis=0) for index in ids])
    control_sum = np.stack([control[trajectory == index].sum(axis=0) for index in ids])
    weights = rng.multinomial(len(ids), np.full(len(ids), 1/len(ids)), size=repetitions)
    denominator = (weights @ counts)[:, None]
    e = weights @ event_sum / denominator
    c = weights @ control_sum / denominator
    return (np.percentile(e, [2.5, 97.5], axis=0),
            np.percentile(c, [2.5, 97.5], axis=0),
            np.percentile(e-c, [2.5, 97.5], axis=0))


def _spectral_power(windows, dt, frequencies):
    windows = np.asarray(windows, dtype=float)
    centered = windows-windows.mean(axis=1, keepdims=True)
    phase = np.exp(-1j*np.arange(windows.shape[1])[:, None]*dt*frequencies)
    variance = (1-abs(phase.mean(axis=0))**2)/(windows.shape[1]*dt)
    return abs(centered @ phase/windows.shape[1])**2/variance


def plot_event_study(data, windows, figures, output):
    """Actual simulated event records versus matched non-transition records."""
    n = len(windows['trajectory'])
    clusters = len(np.unique(windows['trajectory']))
    omega, gamma = omega_gamma(CONFIG['nbar'])
    rng = np.random.default_rng(2029)
    dt = CONFIG['saved_dt']
    context_bins = windows['I_event'].shape[1]
    tstate = (np.arange(context_bins+1)-context_bins/2)*dt
    trecord = (np.arange(context_bins)+.5-context_bins/2)*dt
    fig, axes = plt.subplots(2, 1, figsize=(10, 5.5), sharex=True)
    for ax, key, time_axis, ylabel in [
            (axes[0], 'z', tstate, 'Direction-normalized logical Z'),
            (axes[1], 'I', trecord, 'Mean measured I')]:
        event, control = windows[f'{key}_event'], windows[f'{key}_control']
        eb, cb, _ = _paired_cluster_means(event, control, windows['trajectory'], rng)
        for mean, band, color, label in [(event.mean(0), eb, 'tab:orange', 'Confirmed transitions'),
                                         (control.mean(0), cb, 'tab:blue', 'Matched no-transition windows')]:
            ax.plot(time_axis, mean, color=color, label=label)
            ax.fill_between(time_axis, *band, color=color, alpha=.17, lw=0)
        ax.axvline(0, color='black', ls=':', lw=1)
        ax.set(ylabel=ylabel)
        ax.legend(fontsize=8)
    axes[-1].set(xlabel='Time from state-defined event anchor', xlim=(-8, 8))
    fig.suptitle(f'Known two-mode simulation: {n} transition / {n} control windows\n'
                 f'{CONFIG["n_trajectories"]} simulated histories; {clusters} contributing histories; no end-label timing', fontsize=11)
    fig.tight_layout()
    fig.savefig(figures/'simulated_event_alignment.png', dpi=160)
    plt.close(fig)

    # Rebin genuine dY/dt solver records to the challenge's 0.5-unit bin duration.
    # Context starts at an event-defined sample; no candidate is chosen by I,Q.
    coarse_dt = .5
    factor = round(coarse_dt/dt)
    coarse = {key: windows[key].reshape(n, -1, factor).mean(axis=-1)
              for key in ('I_event', 'I_control', 'Q_event', 'Q_control')}
    lengths = (4, 5, 6, 7, 8, 16)
    fig, axes = plt.subplots(2, len(lengths), figsize=(13, 6.4), sharex=True)
    spectra = []
    for col, length in enumerate(lengths):
        dft = 2*np.pi*np.fft.rfftfreq(length, coarse_dt)[1:]
        freq = np.unique(np.r_[np.linspace(.04, np.pi/coarse_dt, 128), omega, dft])
        left = int(np.floor(coarse['I_event'].shape[1]/2-length/2))
        entries = []
        for row, quadrature in enumerate(('I', 'Q')):
            event = _spectral_power(coarse[f'{quadrature}_event'][:, left:left+length], coarse_dt, freq)
            control = _spectral_power(coarse[f'{quadrature}_control'][:, left:left+length], coarse_dt, freq)
            eb, cb, difference = _paired_cluster_means(event, control, windows['trajectory'], rng)
            ax = axes[row, col]
            for mean, band, color, label in [(event.mean(0), eb, 'tab:orange', f'Transition (n={n})'),
                                             (control.mean(0), cb, 'tab:blue', f'No transition (n={n})')]:
                ax.plot(freq, mean, color=color, lw=1.6, label=label)
                ax.fill_between(freq, *band, color=color, alpha=.17, lw=0)
                indices = np.searchsorted(freq, dft)
                ax.scatter(dft, mean[indices], color=color, s=12)
            ax.axvline(omega, color='black', ls=':', lw=1.2, label=rf'Predicted $\Omega={omega:.2f}$')
            ax.set(title=f'{quadrature}: {length} bins, T={length*coarse_dt:g}', xlim=(0, np.pi/coarse_dt))
            ax.legend(fontsize=7)
            ax.grid(alpha=.15)
            k = int(np.searchsorted(freq, omega))
            entries.append(dict(quadrature=quadrature, event_mean=event.mean(0).tolist(),
                                control_mean=control.mean(0).tolist(), event_CI95=eb.tolist(),
                                control_CI95=cb.tolist(), paired_difference_CI95=difference.tolist(),
                                ratio_at_Omega=float(event[:, k].mean()/control[:, k].mean())))
        spectra.append(dict(bins=length, bin_duration=coarse_dt, frequencies=freq.tolist(),
                            actual_DFT_frequencies=dft.tolist(), quadratures=entries))
    fig.suptitle(f'Event-centered simulated spectra | known K=0 device, nbar=2, kappa_b=4\n'
                 f'{n} transition and {n} matched controls; bands resample {clusters} whole trajectories', fontsize=11)
    fig.supxlabel('Angular frequency (kappa2 units)', y=.105, fontsize=10)
    fig.supylabel('Mean power / unselected white-noise expectation', fontsize=10)
    fig.text(.5, .035, 'Dots: actual DFT bins. Smooth short-window curves do not add resolution. CIs are pointwise, exploratory.',
              ha='center', fontsize=9)
    fig.tight_layout(rect=(.025, .12, 1, .95))
    fig.savefig(figures/'simulated_event_spectra.png', dpi=160)
    plt.close(fig)
    summary = dict(config=CONFIG, selection_version=1, buffer_efficiency=1., precision='complex128', physical_params=json.loads(str(data['params'])),
                   actual_pairs=n, contributing_trajectories=clusters,
                   candidate_transitions=int(windows['candidate_count']), eligible_transitions=int(windows['eligible_count']),
                   Omega=float(omega), gamma=float(gamma),
                   event_rule='Opposite |Z|>=0.8 plateaus held for 1 unit; largest directed 0.5-unit Z drop sets anchor',
                   window_selection='Round-robin trajectory order; controls from same trajectory and starting side; no I/Q selection',
                   state_information='Privileged full-environment diffusive state; not buffer-only reconstructed Z',
                   measured_records='Genuine buffer heterodyne solver outputs; not noise added to conditional means',
                   uncertainty='2000 paired bootstrap resamples of whole contributing trajectories, seed 2029; pointwise CIs',
                   bootstrap_seed=2029, max_top_memory=float(data['top_memory'].max()),
                   max_top_buffer=float(data['top_buffer'].max()),
                   elapsed_seconds=float(data['elapsed_seconds']), backend=str(data['backend']),
                   spectra=spectra)
    (output/'simulated_event_study.json').write_text(json.dumps(summary, indent=2)+'\n')
    np.savez_compressed(output/'simulated_event_windows.npz', **windows)
    print(f'Event study: {n} transition/control pairs from {clusters} contributing trajectories.', flush=True)
    return summary


def run_event_study(figures, output, resimulate=False):
    figures, output = Path(figures), Path(output)
    figures.mkdir(parents=True, exist_ok=True); output.mkdir(parents=True, exist_ok=True)
    window_cache, report_cache = output/'simulated_event_windows.npz', output/'simulated_event_study.json'
    if not resimulate and window_cache.exists() and report_cache.exists():
        report = json.loads(report_cache.read_text())
        if report['config'] != CONFIG or report.get('selection_version') != 1:
            raise ValueError('The bundled event study has a different protocol; rerun with --resimulate-events.')
        with np.load(window_cache, allow_pickle=False) as archive:
            windows = {key: archive[key] for key in archive.files}
        # Plot the bundled measured windows without needing the large raw cache.
        data = dict(params=json.dumps(report['physical_params']),
                    top_memory=np.array(report['max_top_memory']),
                    top_buffer=np.array(report['max_top_buffer']),
                    elapsed_seconds=report['elapsed_seconds'], backend=report['backend'])
    else:
        data = simulate_reference(output, force=resimulate)
        windows = select_event_windows(data)
    return plot_event_study(data, windows, figures, output)
