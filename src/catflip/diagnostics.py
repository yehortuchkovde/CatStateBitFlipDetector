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


def ensemble_spectra(val, figures, output):
    """All rows, separated by cat size and final label; no fitted frequencies.

    Full-segment spectra avoid selecting whichever short window looks most
    oscillatory. Baseline subtraction removes only DC. Q and non-flips are
    controls. This diagnostic must not be used to retune the submitted score.
    """
    T=val['meta']['T_seg']; dt=T/val['I'].shape[1]
    frequencies=2*np.pi*np.fft.rfftfreq(val['I'].shape[1],dt)
    fig,axes=plt.subplots(2,2,figsize=(11,7),sharex=True)
    summary=[]
    for ax,cat in zip(axes.flat,np.unique(val['nbar'])):
        omega,gamma=omega_gamma(cat)
        for label,style in [(0,'-'),(1,'--')]:
            rows=(val['nbar']==cat)&(val['labels']==label)
            for key,color in [('I','tab:blue'),('Q','tab:orange')]:
                x=val[key][rows].astype(float)
                x-=x.mean(axis=1,keepdims=True)
                powers=T*np.abs(np.fft.rfft(x,axis=1)/x.shape[1])**2
                average=powers.mean(axis=0)
                ax.plot(frequencies[1:],average[1:],color=color,ls=style,lw=1,
                        label=f'{key}, label {label} (n={rows.sum()})')
                k=int(np.argmin(abs(frequencies-omega)))
                # Explicit uncertainty of this fixed-bin ensemble average, not
                # a significance claim from the largest of many inspected bins.
                sem=powers[:,k].std(ddof=1)/np.sqrt(len(powers))
                summary.append(dict(nbar=float(cat),label=label,quadrature=key,
                                    Omega=float(omega),nearest_bin=float(frequencies[k]),
                                    mean_power=float(average[k]),standard_error=float(sem),
                                    trajectories=int(rows.sum())))
        ax.axvline(omega,color='tomato',ls=':',label='Predicted Omega (kb=4)')
        ax.axhline(1,color='gray',lw=.8,ls=':')
        ax.set(title=f'nbar={cat:g}',xlabel='Angular frequency',ylabel='Mean power / white-noise floor',
               xlim=(0,np.pi/dt))
        ax.legend(fontsize=6)
    fig.suptitle('Unselected validation spectra: compare data with the prediction, not just selected examples')
    fig.tight_layout(); fig.savefig(figures/'ensemble_spectra.png',dpi=170); plt.close(fig)
    (output/'ensemble_spectra.json').write_text(json.dumps(summary,indent=2)+'\n')


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
