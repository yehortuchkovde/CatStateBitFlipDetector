"""Known-device simulations and a controlled check of the local-response theory.

No simulation here estimates or reconstructs the private test device or labels.
Photon counting and heterodyne are different unravelings; their examples are
independent. Never present a Tier-A click train as simultaneous with Tier-B I,Q.
"""
import json
import numpy as np
import matplotlib.pyplot as plt
from .detector import omega_gamma


def linear_response(figures, output):
    """Full Lindblad evolution versus PDF Eq. (34), with no fitted frequency.

    Subtract the evolution of an undisplaced reference state to remove its slow
    drift. This is a controlled small radial perturbation, not a logical flip.
    """
    import dynamiqs as dq
    from catchtheflip import models
    dq.set_precision('double')
    t=np.linspace(0,10,501); d=.05
    fig,axes=plt.subplots(2,2,figsize=(11,7))
    summaries=[]
    for ax,cat in zip(axes.flat,[2,2.5,3,3.5]):
        p=models.TwoModeParams(nbar=cat,kappa_b=4,Na=20,Nb=5)
        model=models.two_mode(p)
        perturbed=dq.tensor(dq.coherent(p.Na,p.alpha-d),dq.fock(p.Nb,0))
        initial=dq.stack([model.psi0,perturbed])
        result=dq.mesolve(model.H,model.jump_ops,initial,t,exp_ops=[model.b],
                           method=dq.method.Tsit5(max_steps=100000),
                           save_states=False,progress_meter=False)
        b=np.asarray(result.expects)[:,0,:]
        response=b[1]-b[0]
        omega,gamma=omega_gamma(cat)
        prediction=1j*(2*p.g2*p.alpha*d/omega)*np.exp(-gamma*t)*np.sin(omega*t)
        ax.plot(t,response.imag,label='Full Lindblad: Im(delta b)',lw=1.5)
        ax.plot(t,prediction.imag,'--',label='Linear theory; no fit',lw=1.3)
        ax.set(title=f'nbar={cat:g}; Omega={omega:.3f}, gamma={gamma:.2f}',
               xlabel='Time',ylabel='Buffer radial response')
        ax.legend(fontsize=8)
        summaries.append(dict(nbar=cat,Omega=float(omega),gamma=gamma,d=d,
                              displacement_fraction=d/p.alpha,
                              relative_RMS_error=float(np.linalg.norm(response-prediction)/np.linalg.norm(prediction)),
                              Na=p.Na,Nb=p.Nb))
    fig.suptitle('Known two-mode device: a small radial displacement excites the predicted ring-down')
    fig.tight_layout(); fig.savefig(figures/'linear_response.png',dpi=170); plt.close(fig)
    (output/'linear_response.json').write_text(json.dumps(summaries,indent=2)+'\n')


def counting_examples(figures, output, max_seeds=32):
    """Find one flip-labelled and one no-flip-labelled nominal trajectory.

    Every channel is counted in the simulation: rho is privileged state information,
    not a state inferred from a real buffer-only detector. Save the full joint
    rho(t), state vector, a(t), Z(t), ideal mean quadratures, and clicks.
    """
    import dynamiqs as dq
    from catchtheflip import models,simulate
    dq.set_precision('double')
    p=models.SingleModeParams(nbar=2,N=24)
    model=models.single_mode(p)
    found={}; summary=[]
    for seed in range(max_seeds):
        print(f'  Nominal counting seed {seed}',flush=True)
        tr=simulate.long_trajectory(model,T=200,seed=seed,n_save=401,
                                    dt=.001,nmaxclick=2000,save_states=True)
        final=float(tr['z'][-1])
        pneg=float(np.clip((1-final)/2,0,1))
        # A challenge label is a sampled terminal Z readout, not sign(<Z>) and
        # not an oracle timestamp. Jump trajectories often end in superpositions.
        label=int(np.random.default_rng([seed,2026]).random()<pneg)
        case='flip' if label else 'no_flip'
        if case in found: continue
        psi=tr['states']
        rho=psi[:,:,None]*psi[:,None,:].conj()
        L=np.asarray(model.L_buffer.to_jax())
        mean_L=np.einsum('ti,ij,tj->t',psi.conj(),L,psi)
        mean_I=np.sqrt(2)*mean_L.real
        mean_Q=-np.sqrt(2)*mean_L.imag  # dynamiqs iL convention; PDF uses opposite Q phase.
        projector=model.x_negative_projector if label else np.eye(model.dim)-model.x_negative_projector
        post=projector@psi[-1]
        post/=np.linalg.norm(post)
        np.savez_compressed(output/f'counting_{case}.npz',**tr,rho=rho,
                            ideal_I=mean_I,ideal_Q=mean_Q,seed=seed,
                            label=label,pneg=pneg,rho_post_readout=np.outer(post,post.conj()),
                            params=json.dumps(p.to_dict()))
        found[case]=(tr,mean_I,mean_Q)
        summary.append(dict(case=case,seed=seed,final_Z=final,label=label,pneg=pneg,
                            state_information='all-channel counting (privileged)',
                            N=p.N,dt=.001))
        if len(found)==2: break
    if len(found)!=2:
        raise RuntimeError(f'No labelled flip/no-flip pair within {max_seeds} seeds; increase --max-seeds.')
    fig,axes=plt.subplots(3,2,figsize=(12,7),sharex=True)
    for col,case in enumerate(['flip','no_flip']):
        tr,I,Q=found[case]
        axes[0,col].plot(tr['t'],tr['z'],label='Z(t)')
        axes[0,col].plot([200],[1-2*int(case=='flip')],'rx',ms=7,label='Sampled final readout')
        axes[0,col].set(title=f"Nominal counting: {case.replace('_',' ')}-labelled",
                        ylabel='Conditioned Z',ylim=(-1.1,1.1))
        axes[0,col].legend(fontsize=7)
        axes[1,col].plot(tr['t'],I,label='Ideal mean I')
        axes[1,col].plot(tr['t'],Q,label='Ideal mean Q')
        axes[1,col].set(ylabel='Ideal mean I,Q'); axes[1,col].legend(fontsize=7)
        for k,name in enumerate(model.channels):
            clicks=tr['clicktimes'][k]; clicks=clicks[np.isfinite(clicks)]
            axes[2,col].plot(clicks,np.full(len(clicks),k),'|',ms=5)
        axes[2,col].set(yticks=range(len(model.channels)),yticklabels=model.channels,xlabel='Time')
    fig.suptitle('Full states and channel-resolved clicks are simulation-only information')
    fig.tight_layout(); fig.savefig(figures/'counting_simulations.png',dpi=170); plt.close(fig)
    (output/'counting_examples.json').write_text(json.dumps(summary,indent=2)+'\n')


def heterodyne_examples(figures, output, max_seeds=32):
    """Buffer-only stochastic master equation of the nominal single-mode device.

    rho(t) is conditioned on measured I,Q, with other channels unobserved. End
    labels are sampled with the Born rule, just as in the challenge; labels do
    not expose an exact flip time. This is independent of counting_examples().
    """
    import dynamiqs as dq
    import jax
    from catchtheflip import models
    dq.set_precision('double')
    p=models.SingleModeParams(nbar=2,N=24); model=models.single_mode(p)
    L=model.L_buffer
    ops=[L/np.sqrt(2),1j*L/np.sqrt(2),*model.jump_ops[1:]]
    etas=[1.,1.,*([0.]*(len(ops)-2))]
    Z=dq.asqarray(np.eye(model.dim)-2*model.x_negative_projector)
    times=tuple(np.linspace(0,200,401))
    found={}; metadata=[]
    for start in range(0,max_seeds,4):
        seeds=list(range(start,min(start+4,max_seeds)))
        print(f'  Nominal heterodyne seeds {1000+seeds[0]}..{1000+seeds[-1]}',flush=True)
        keys=np.stack([jax.random.PRNGKey(1000+s) for s in seeds])
        result=dq.dsmesolve(model.H,ops,etas,model.psi0,times,keys,
                             exp_ops=[Z,model.a,model.a.dag()@model.a],
                             method=dq.method.Rouchon1(dt=.0005),save_states=True)
        rhos=np.asarray(result.states.to_jax())
        measurements=np.asarray(result.measurements)
        ex=np.asarray(result.expects)
        for k,seed in enumerate(seeds):
            pneg=float(np.clip((1-ex[k,0,-1].real)/2,0,1))
            label=int(np.random.default_rng([1000+seed,2026]).random()<pneg)
            case='flip' if label else 'no_flip'
            if case in found: continue
            projector=model.x_negative_projector if label else np.eye(model.dim)-model.x_negative_projector
            post=projector@rhos[k,-1]@projector
            post/=np.trace(post).real
            data=dict(t=np.asarray(times),I=measurements[k,0],Q=measurements[k,1],
                      rho=rhos[k],z=ex[k,0].real,a=ex[k,1],n=ex[k,2].real,
                      rho_post_readout=post,pneg=pneg,label=label,seed=1000+seed,
                      params=json.dumps(p.to_dict()))
            np.savez_compressed(output/f'heterodyne_{case}.npz',**data)
            found[case]=data
            metadata.append(dict(case=case,seed=1000+seed,pneg=pneg,label=label,
                                 dt=.0005,N=p.N,information='buffer-only conditioned SME'))
        if len(found)==2: break
    if len(found)!=2:
        raise RuntimeError('No sampled flip/no-flip pair found; increase --max-seeds.')
    fig,axes=plt.subplots(3,2,figsize=(12,7),sharex=True)
    for col,case in enumerate(['flip','no_flip']):
        data=found[case]; t=data['t']; centers=(t[1:]+t[:-1])/2
        axes[0,col].plot(t,data['z'])
        axes[0,col].plot([200],[1-2*data['label']],'rx',ms=7,label='Sampled final readout')
        axes[0,col].legend(fontsize=7)
        axes[0,col].set(ylabel='Conditioned Z',ylim=(-1.1,1.1),
            title=f"Nominal heterodyne: {case.replace('_',' ')}-labelled\nseed={data['seed']}, P(-alpha)={data['pneg']:.2f}")
        axes[1,col].plot(centers,data['I'],lw=.6); axes[1,col].set(ylabel='Measured I')
        axes[2,col].plot(centers,data['Q'],lw=.6); axes[2,col].set(ylabel='Measured Q',xlabel='Time')
    fig.suptitle('Actual noisy heterodyne records; no simultaneous photon-counting record')
    fig.tight_layout(); fig.savefig(figures/'heterodyne_simulations.png',dpi=170); plt.close(fig)
    (output/'heterodyne_examples.json').write_text(json.dumps(metadata,indent=2)+'\n')
