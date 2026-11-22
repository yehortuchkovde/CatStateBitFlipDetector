"""Exploratory frequency checks, separate from the frozen four-bin detector.

End-of-segment labels are not flip timestamps. A DC-selected event is therefore
called a candidate excursion, never a measured logical-transition time.
"""
import json
import numpy as np
import matplotlib.pyplot as plt
from .detector import omega_gamma


def trajectory_examples(val, figures, output):
    dt = val['meta']['T_seg'] / val['I'].shape[1]
    # Same two illustrative rows used in the submitted presentation; no peak search.
    rows = [6406, 1523]
    fig, axes = plt.subplots(3, 2, figsize=(12, 8))
    examples = []
    for col, row in enumerate(rows):
        I, Q, cat = val['I'][row].astype(float), val['Q'][row].astype(float), val['nbar'][row]
        omega, gamma = omega_gamma(cat)
        # Anchor on the strongest downward DC excursion, not on a fitted frequency.
        means = np.lib.stride_tricks.sliding_window_view(I, 4).mean(axis=1)
        start = int(np.argmin(means)); center = (start+2)*dt
        left = int(np.clip(start+2-16, 0, len(I)-32))
        t = (np.arange(len(I))+.5)*dt
        axes[0,col].plot(t, I, lw=.6, label='Measured I')
        axes[0,col].plot(t, Q, lw=.6, alpha=.5, label='Measured Q')
        axes[0,col].axvspan(start*dt, (start+4)*dt, color='green', alpha=.16)
        axes[0,col].axvspan(left*dt, (left+32)*dt, color='orange', alpha=.12)
        axes[0,col].set(title=f"Validation row {row}: label={val['labels'][row]}, nbar={cat:g}",
                        ylabel='Record amplitude', xlabel='Time')
        axes[0,col].legend(fontsize=7)
        times = (np.arange(left,left+32)+.5)*dt
        axes[1,col].plot(times,I[left:left+32],'.-',label='I')
        axes[1,col].plot(times,Q[left:left+32],'.-',alpha=.6,label='Q')
        axes[1,col].axvline(center,color='green',ls=':',label='DC candidate time')
        axes[1,col].set(xlabel='Time',ylabel='Record amplitude',title='T=16 inspection window (32 bins)')
        axes[1,col].legend(fontsize=7)
        frequencies = 2*np.pi*np.fft.rfftfreq(32,dt)
        spectra = []
        for name, x in [('I',I),('Q',Q)]:
            segment=x[left:left+32]; segment=segment-segment.mean()
            power=16*np.abs(np.fft.rfft(segment)/32)**2
            axes[2,col].plot(frequencies[1:],power[1:],'.-',label=name)
            spectra.append(power)
        axes[2,col].axvline(omega,color='tomato',ls='--',label=f'Predicted Omega={omega:.2f}')
        axes[2,col].axhline(1,color='gray',ls=':',label='Unselected white-noise expectation')
        axes[2,col].set(xlabel='Angular frequency (rad / time unit)',ylabel='Noise-normalized power',
                        title='Actual DFT bins; no zero-padding or fitted frequency')
        axes[2,col].legend(fontsize=7)
        k=int(np.argmin(abs(frequencies-omega)))
        examples.append(dict(row=row,label=int(val['labels'][row]),nbar=float(cat),
                             candidate_time=center,Omega=float(omega),gamma=gamma,
                             nearest_DFT_frequency=float(frequencies[k]),
                             I_power_at_nearest_bin=float(spectra[0][k]),
                             Q_power_at_nearest_bin=float(spectra[1][k])))
    fig.suptitle('Candidate excursions, not known flip times; individual spectra are noisy',fontsize=12)
    fig.tight_layout(); fig.savefig(figures/'record_examples.png',dpi=170); plt.close(fig)
    (output/'trajectory_examples.json').write_text(json.dumps(examples,indent=2)+'\n')


def click_examples(clicks, figures):
    """Tier A is a different set of experiments, not aligned to Tier B rows."""
    fig,axes=plt.subplots(2,1,figsize=(10,3),sharex=True)
    for ax,label in zip(axes,[1,0]):
        row=int(np.flatnonzero((clicks['labels']==label)&(clicks['nbar']==2))[0])
        events=clicks['clicktimes'][row]
        events=events[np.isfinite(events)]
        ax.eventplot(events,colors='tab:purple')
        ax.set(yticks=[],ylabel=f'Label {label}',title=f'Tier A validation row {row}, nbar=2, {len(events)} clicks')
    axes[-1].set(xlim=(0,clicks['meta']['T_seg']),xlabel='Time')
    fig.suptitle('Photon-counting examples: separate experiments from the heterodyne records')
    fig.tight_layout(); fig.savefig(figures/'click_examples.png',dpi=170); plt.close(fig)


def candidate_excursion_power(I, nbar, dt, inspection_bins=32, frequency_factor=1.0):
    """Power at a prescribed frequency, anchored only by the four-bin DC dip.

    Inspection lengths 3, 4 and 32 are fixed comparisons, not optimized per cat.
    Odd lengths choose the earlier of two equally centered windows. Edges shift
    inward; no record is discarded. Each inspection mean is subtracted first.
    frequency_factor is only for declared diagnostic controls, never a search
    or a change to the submitted detector's raw-I four-bin Fourier maximum.
    """
    values = np.asarray(I, dtype=np.float64)
    nbar = np.asarray(nbar)
    length = inspection_bins
    if not isinstance(length, (int, np.integer)) or length < 2:
        raise ValueError('Inspection length must be an integer >=2.')
    if values.ndim != 2 or nbar.shape != (len(values),) or values.shape[1] < max(4, length):
        raise ValueError('Expected compatible records, cat sizes and window lengths.')
    if dt <= 0 or frequency_factor <= 0 or not np.isfinite(values).all():
        raise ValueError('Use finite records and positive dt/frequency factor.')
    means = np.lib.stride_tricks.sliding_window_view(values, 4, axis=1).mean(axis=-1)
    dc_start = np.argmin(means, axis=1)
    centered_start = np.floor(dc_start + 2 - length / 2).astype(int)
    inspection_start = np.clip(centered_start, 0, values.shape[1] - length)
    windows = values[np.arange(len(values))[:, None], inspection_start[:, None] + np.arange(length)]
    windows -= windows.mean(axis=1, keepdims=True)
    power = np.empty(len(values))
    for cat in np.unique(nbar):
        omega, _ = omega_gamma(cat)
        omega *= frequency_factor
        if omega >= np.pi / dt:
            raise ValueError('Prescribed frequency exceeds Nyquist.')
        phase = np.exp(-1j * omega * np.arange(length) * dt)
        # Correct the UNSELECTED white-noise expectation for local demeaning.
        # Selecting the deepest DC dip can change this noise distribution;
        # short_window_comparison repeats the selection on pure Gaussian noise.
        white_variance = (1 - abs(phase.mean())**2) / (length * dt)
        rows = nbar == cat
        amplitude = windows[rows] @ phase / length
        power[rows] = np.abs(amplitude)**2 / white_variance
    return power, dc_start, inspection_start


def _bootstrap_medians(values, rng, repetitions=2000):
    """Resample independent trajectories, not correlated overlapping windows."""
    medians = []
    for start in range(0, repetitions, 100):
        size = min(100, repetitions - start)
        samples = rng.integers(0, len(values), size=(size, len(values)))
        medians.extend(np.median(values[samples], axis=1))
    return np.asarray(medians)


def excursion_power_distributions(val, figures, output, inspection_bins=32):
    """All labelled validation rows: local-power distributions and median CIs.

    Time window and frequency are fixed before reading labels. Labels are used
    only for grouping. No records are selected by their Fourier response.
    """
    dt = val['meta']['T_seg'] / val['I'].shape[1]
    duration = inspection_bins * dt
    suffix = '' if inspection_bins == 32 else f'_{inspection_bins}bins'
    power, dc_start, inspection_start = candidate_excursion_power(val['I'], val['nbar'], dt, inspection_bins)
    rng = np.random.default_rng(2026)
    cats = np.unique(val['nbar'])
    if len(cats) != 4:
        raise ValueError('This challenge figure expects the four published cat sizes.')
    fig, axes = plt.subplots(2, 2, figsize=(9, 7), sharey=True)
    summary = []
    log_power = np.log10(np.maximum(power, 1e-8))  # display floor only; no rows removed
    lower, upper = np.floor(log_power.min()), np.ceil(log_power.max())
    ticks = np.arange(lower, upper + 1)
    for ax, cat in zip(axes.flat, cats):
        omega, _ = omega_gamma(cat)
        draws, groups = [], []
        for label, color in [(0, 'tab:blue'), (1, 'tab:orange')]:
            rows = (val['nbar'] == cat) & (val['labels'] == label)
            values = power[rows]
            boot = _bootstrap_medians(values, rng)
            median = float(np.median(values))
            low, high = np.percentile(boot, [2.5, 97.5])
            violin = ax.violinplot([log_power[rows]], positions=[label], widths=.65,
                                   showmeans=False, showmedians=False, showextrema=False)
            for body in violin['bodies']:
                body.set_facecolor(color); body.set_edgecolor(color); body.set_alpha(.4)
            # Densities are in log power; error bars are bootstrap CIs of medians,
            # not the spread of individual trajectory powers.
            y = np.log10(max(median, 1e-8))
            errors = [[y - np.log10(max(low, 1e-8))], [np.log10(max(high, 1e-8)) - y]]
            ax.errorbar([label], [y], yerr=errors, fmt='o', color='black', ms=5,
                         capsize=6, elinewidth=2, zorder=4)
            draws.append(boot)
            groups.append(dict(label=label, records=int(rows.sum()), median=median,
                               median_CI95=[float(low), float(high)], mean=float(values.mean())))
        ratio = np.median(power[(val['nbar'] == cat) & (val['labels'] == 1)]) / np.median(
            power[(val['nbar'] == cat) & (val['labels'] == 0)])
        ratio_ci = np.percentile(draws[1] / draws[0], [2.5, 97.5])
        summary.append(dict(nbar=float(cat), Omega=float(omega), groups=groups,
                            median_flip_to_no_flip_ratio=float(ratio),
                            ratio_CI95=ratio_ci.tolist()))
        ax.set(title=rf'$\bar n={cat:g}$ | predicted $\Omega={omega:.2f}$', xlim=(-.6, 1.6),
               xticks=[0, 1], xticklabels=[f"No-flip readout\nn={groups[0]['records']:,}",
                                         f"Flip readout\nn={groups[1]['records']:,}"],
               yticks=ticks, yticklabels=[rf'$10^{{{int(tick)}}}$' for tick in ticks])
        ax.grid(axis='y', alpha=.2)
    fig.suptitle(f'Local I power near predicted Omega: all {len(power):,} validation records\n'
                 f'Four-bin DC selection; fixed {inspection_bins}-bin (T={duration:g}) spectral window', fontsize=12)
    fig.supylabel('Fourier power / unselected white-noise expectation (log scale)', fontsize=10)
    fig.text(.5, .015, 'Violin: full distribution   |   Black dot: median   |   Bar: 95% bootstrap CI of median',
              ha='center', fontsize=9)
    fig.tight_layout(rect=(.025, .045, 1, .93))
    fig.savefig(figures / f'excursion_power_distributions{suffix}.png', dpi=170)
    plt.close(fig)
    report = dict(split='validation', records=len(power), dc_bins=4, dc_time=4*dt,
                  inspection_bins=inspection_bins, inspection_time=duration, dt=dt,
                  frequency='Exact predicted Omega; no frequency search',
                  baseline='Inspection-window mean subtracted',
                  noise_normalization='Unselected white-noise expectation; selection bias is not removed',
                  bootstrap_repetitions=2000, bootstrap_seed=2026,
                  uncertainty='Pointwise percentile 95% CIs; no multiple-comparison adjustment',
                  edge_shifted_records=int(np.sum(inspection_start != np.floor(dc_start + 2 - inspection_bins/2).astype(int))),
                  records_at_display_floor=int(np.sum(power < 1e-8)), by_cat=summary)
    (output / f'excursion_power_distributions{suffix}.json').write_text(json.dumps(report, indent=2) + '\n')
    np.savez_compressed(output / f'excursion_powers{suffix}.npz', segment_id=np.arange(len(power)),
                        power=power, nbar=val['nbar'], labels=val['labels'],
                        dc_start=dc_start, inspection_start=inspection_start)
    print(f'All-record excursion-power comparison ({inspection_bins} bins):', flush=True)
    for entry in summary:
        lo, hi = entry['ratio_CI95']
        print(f"  nbar={entry['nbar']:g}: flip/no-flip median ratio "
              f"{entry['median_flip_to_no_flip_ratio']:.2f}, 95% CI [{lo:.2f}, {hi:.2f}]")
    return report


def short_window_comparison(val, figures, output, reference_report=None):
    """Report both proposed short windows and the original 32-bin comparison.

    Same rows, DC anchor, demeaning and frequency rule for every length. No
    candidate detector is fitted or selected here. Off-frequency checks are
    reported as controls, not used to choose a better frequency.
    """
    reports = [excursion_power_distributions(val, figures, output, inspection_bins=L)
               for L in (3, 4)]
    if reference_report is None:
        reference_report = excursion_power_distributions(val, figures, output)
    reports.append(reference_report)
    dt = val['meta']['T_seg'] / val['I'].shape[1]
    cats = np.unique(val['nbar'])
    noise = np.random.default_rng(2027).normal(0, 1/np.sqrt(dt), size=val['I'].shape)
    controls = []
    for length in (3, 4, 32):
        white, _, _ = candidate_excursion_power(noise, val['nbar'], dt, length)
        for cat in cats:
            groups = [white[(val['nbar'] == cat) & (val['labels'] == label)] for label in (0, 1)]
            controls.append(dict(inspection_bins=length, nbar=float(cat),
                                 selected_gaussian_noise_median=float(np.median(white[val['nbar'] == cat])),
                                 gaussian_label_group_median_ratio=float(np.median(groups[1])/np.median(groups[0]))))
    off_frequency = []
    for length in (3, 4):
        for factor in (.5, 1.5):
            power, _, _ = candidate_excursion_power(val['I'], val['nbar'], dt, length, factor)
            for cat in cats:
                medians = [np.median(power[(val['nbar'] == cat) & (val['labels'] == label)])
                           for label in (0, 1)]
                off_frequency.append(dict(inspection_bins=length, nbar=float(cat),
                                          frequency_factor=factor,
                                          median_flip_to_no_flip_ratio=float(medians[1]/medians[0])))

    result = dict(records=len(val['nbar']), dc_bins=4, inspection_bins=[3, 4, 32],
                  reports=reports, gaussian_control_seed=2027,
                  noise_control='Independent white noise of known bin variance 1/dt; identical DC-selection pipeline',
                  selected_gaussian_controls=controls,
                  off_frequency_controls=off_frequency,
                  interpretation='Short-record power differences do not identify a unique oscillation frequency; exploratory and unadjusted')
    (output / 'short_window_comparison.json').write_text(json.dumps(result, indent=2) + '\n')
    return result
