"""A resolved stochastic cat-state switch, with its actual Wigner function.

The otherwise unobserved memory-loss channel is counted after displacement by a
local oscillator. This distinguishes the logical lobes in the full trajectory;
the compensating Hamiltonian preserves the original Lindblad generator exactly.
The buffer channel and its click record are unchanged. This visualization never
changes the submitted detector or supplies it with privileged state information.
"""
from dataclasses import replace
import json
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter


def localized_counting_model():
    """Same nominal device, different unraveling of the memory-loss channel.

    For real beta: L' = L + beta*I, H' = H + i*beta*(L^dagger-L)/2.
    Then -i[H',rho]+D[L']rho = -i[H,rho]+D[L]rho for every rho.
    """
    import dynamiqs as dq
    from catchtheflip import models, rates

    dq.set_precision('double')
    original = models.single_mode(models.SingleModeParams(nbar=2, N=24))
    index = original.channels.index('loss')
    loss = original.jump_ops[index]
    beta = 1.0
    operators = list(original.jump_ops)
    operators[index] = loss + beta * dq.eye(original.dim)
    channels = list(original.channels)
    channels[index] = 'loss + local oscillator'
    model = replace(original, jump_ops=operators, channels=tuple(channels),
                    H=original.H + 0.5j * beta * (loss.dag() - loss))
    error = float(np.max(np.abs(rates.liouvillian_matrix(model)
                               - rates.liouvillian_matrix(original))))
    if error > 1e-11:
        raise ValueError('The visualization must preserve the physical generator.')
    return model, error


def make_wigner_demo(figures, output):
    """Reproduce the seed-7 example and render a PNG plus a synchronized GIF.

    This seed was selected for an actual sustained lobe switch, not a frequency
    peak. It illustrates a transition, not its population frequency or score.
    Every frame is computed from the saved state, not a translated Gaussian.
    """
    import dynamiqs as dq
    from catchtheflip import simulate

    figures, output = Path(figures), Path(output)
    figures.mkdir(parents=True, exist_ok=True)
    output.mkdir(parents=True, exist_ok=True)
    model, generator_error = localized_counting_model()
    cache = output / 'wigner_trajectory.npz'
    if cache.exists():
        with np.load(cache, allow_pickle=False) as archive:
            data = {key: archive[key] for key in archive.files}
        if int(data['seed']) != 7 or float(data['beta']) != 1.0:
            raise ValueError('Unexpected Wigner-demo cache; remove it to regenerate.')
    else:
        data = simulate.long_trajectory(model, T=200, seed=7, n_save=2001,
                                        dt=.001, nmaxclick=3000, save_states=True)
        data.update(seed=7, beta=1.0)
        np.savez_compressed(cache, **data)

    t, z, states = data['t'], data['z'], data['states']
    if z[0] < .8 or np.max(z[-100:]) > -.8:
        raise ValueError('Expected a resolved switch from +alpha to -alpha.')
    switch = int(np.flatnonzero((z[:-1] >= 0) & (z[1:] < 0))[0]) + 1
    left = max(0, switch - 130)
    right = min(len(t) - 1, switch + 130)
    frames = np.arange(left, right + 1, 2)
    alpha = model.params.alpha
    xmean = data['a'].real / alpha
    L = np.asarray(model.L_buffer.to_jax())
    rate = np.sum(np.abs(states @ L.T) ** 2, axis=1)
    clicks = data['clicktimes'][model.buffer_index]
    clicks = clicks[np.isfinite(clicks)]

    # Whole trajectory: the shaded region is exactly the interval animated below.
    fig, axes = plt.subplots(3, 1, figsize=(10, 5.6), sharex=True,
                             gridspec_kw={'height_ratios': [2, 1.3, 1.3]})
    axes[0].plot(t, xmean, color='tab:blue', lw=1.3)
    for value in (-1, 1):
        axes[0].axhline(value, color='gray', ls=':', lw=.8)
    extent = max(1.2, 1.08 * np.max(np.abs(xmean)))
    axes[0].set(ylabel=r'$\langle x\rangle/\alpha$', ylim=(-extent, extent))
    axes[1].plot(t, z, color='tab:purple', lw=1.1)
    axes[1].set(ylabel=r'$\langle Z\rangle$', ylim=(-1.2, 1.2))
    axes[2].plot(t, rate, color='tab:orange', lw=.9, label='Conditional emission rate')
    tick_height = -.07 * max(rate.max(), .1)
    axes[2].plot(clicks, np.full_like(clicks, tick_height), '|',
                 color='firebrick', ms=9, label='Sampled buffer clicks')
    axes[2].set(ylabel='Buffer photons / time', xlabel=r'Time ($1/\kappa_2$)', xlim=(0, 200))
    axes[2].legend(fontsize=8, loc='upper right')
    for ax in axes:
        ax.axvspan(t[left], t[right], color='gray', alpha=.13)
    fig.suptitle('One resolved stochastic switch: same state trajectory and buffer click record\n'
                 'Nominal device, nbar=2, seed=7; shaded interval is animated', fontsize=11)
    fig.tight_layout()
    fig.savefig(figures / 'stochastic_trajectory.png', dpi=160)
    plt.close(fig)

    # hbar=1/2: coherent states are centered at (Re(alpha), Im(alpha)).
    # dq.wigner returns W[x_index,p_index], so imshow needs its transpose.
    x, p, wigner = dq.wigner(dq.asqarray(states[frames, :, None]),
                              xmax=3.5, ymax=3.5, npixels=101, hbar=.5)
    x, p, wigner = np.asarray(x), np.asarray(p), np.asarray(wigner)
    fig = plt.figure(figsize=(9, 4.6), layout='constrained')
    grid = fig.add_gridspec(2, 2, width_ratios=[1, 1.1], height_ratios=[2, 1])
    phase = fig.add_subplot(grid[:, 0])
    trajectory = fig.add_subplot(grid[0, 1])
    counts = fig.add_subplot(grid[1, 1], sharex=trajectory)
    image = phase.imshow(wigner[0].T, origin='lower', extent=[x[0], x[-1], p[0], p[-1]],
                          cmap='RdBu_r', vmin=-2/np.pi, vmax=2/np.pi, interpolation='bilinear')
    phase.plot([-alpha, alpha], [0, 0], 'o', mfc='none', mec='black', ms=12, mew=.8)
    phase.text(alpha, -.55, r'$+\alpha$', ha='center')
    phase.text(-alpha, -.55, r'$-\alpha$', ha='center')
    phase.set(xlabel=r'$x=\mathrm{Re}(a)$', ylabel=r'$p=\mathrm{Im}(a)$',
              title=r'Actual $W(x,p)$ of the simulated state')
    fig.colorbar(image, ax=phase, shrink=.7, label=r'$W(x,p)$')
    trajectory.plot(t[left:right+1], xmean[left:right+1], color='tab:blue', lw=1.3)
    trajectory.axhline(1, color='gray', ls=':', lw=.8)
    trajectory.axhline(-1, color='gray', ls=':', lw=.8)
    zoom_extent = max(1.2, 1.08 * np.max(np.abs(xmean[left:right+1])))
    trajectory.set(ylabel=r'$\langle x\rangle/\alpha$', ylim=(-zoom_extent, zoom_extent),
                   title='Same stochastic trajectory')
    counts.plot(t[left:right+1], rate[left:right+1], color='tab:orange', lw=1)
    selected_clicks = clicks[(clicks >= t[left]) & (clicks <= t[right])]
    tick_height = -.1 * max(rate[left:right+1].max(), .1)
    counts.plot(selected_clicks, np.full_like(selected_clicks, tick_height), '|',
                 color='firebrick', ms=11, label='Buffer clicks')
    counts.legend(fontsize=8, loc='upper right')
    counts.set(xlabel=r'Time ($1/\kappa_2$)', ylabel='Buffer rate', xlim=(t[left], t[right]))
    cursors = [ax.axvline(t[frames[0]], color='black', lw=1) for ax in (trajectory, counts)]
    dot, = trajectory.plot([t[frames[0]]], [xmean[frames[0]]], 'ko', ms=4)
    title = fig.suptitle('', fontsize=11)

    def update(index):
        frame = frames[index]
        image.set_data(wigner[index].T)
        for cursor in cursors:
            cursor.set_xdata([t[frame], t[frame]])
        dot.set_data([t[frame]], [xmean[frame]])
        title.set_text(f'Stochastic cat-state switch | t={t[frame]:.1f} | seed=7')
        return image, dot, title, *cursors

    animation = FuncAnimation(fig, update, frames=len(frames), interval=1000/12, blit=False)
    animation.save(figures / 'wigner_transition.gif', writer=PillowWriter(fps=12), dpi=95)
    plt.close(fig)

    summary = dict(seed=7, params=model.params.to_dict(), integration_dt=.001,
                   saved_dt=float(t[1]-t[0]), time_of_first_Z_crossing=float(t[switch]),
                   animation_interval=[float(t[left]), float(t[right])],
                   initial_Z=float(z[0]), final_Z=float(z[-1]),
                   initial_x_over_alpha=float(xmean[0]), final_x_over_alpha=float(xmean[-1]),
                   buffer_clicks=clicks.tolist(), local_oscillator_beta=1.0,
                   generator_max_absolute_difference=generator_error,
                   frames=len(frames), fps=12,
                   selection='Fixed illustrative seed with a sustained lobe switch; not a statistical sample.',
                   state_information='Full state conditioned on all simulated environment channels.')
    (output / 'wigner_demo.json').write_text(json.dumps(summary, indent=2) + '\n')
    print('Saved stochastic_trajectory.png and wigner_transition.gif from the same simulated run.', flush=True)
