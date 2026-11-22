"""Original Step-3 score, with ROC/DET and post-selection diagnostics."""
import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import ndtri
from catchtheflip import scoring
from .detector import my_detector, training_split, calibrate


def metrics(scores, labels):
    decisions = np.zeros(len(scores), dtype=np.int8)
    decisions[np.argsort(scores, kind='stable')[round(0.7 * len(scores)):]] = 1
    c = scoring.confusion(decisions, labels)
    op = scoring.rho_at_yield(scores, labels)
    return dict(AUC=scoring.auc(scores, labels), suppression=op['suppression'],
                yield_fraction=op['yield'], recall=c['tpr'], FPR=c['fpr'],
                FNR=1-c['tpr'], precision=c['tp']/max(1, int(decisions.sum())),
                accuracy=(c['tp']+c['tn'])/len(labels),
                flips_caught=c['tp'], flips_total=int(np.sum(labels)))


def evaluate(train, val, figures, output):
    fit, heldout = training_split(train)
    calibration = calibrate(train, fit)
    (output/'calibration.json').write_text(json.dumps(calibration, indent=2)+'\n')
    modes = [('Final: DC + Omega + cat', 'DC+Omega', True),
             ('DC + cat', 'DC', True), ('Omega + cat', 'Omega', True),
             ('Cat size only', 'cat only', True)]
    all_metrics = {}
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.3))
    for name, mode, include_cat in modes:
        scores = my_detector(val['nbar'], val['I'], val['Q'], calibration, mode, include_cat)
        result = metrics(scores, val['labels'])
        all_metrics[name] = result
        fpr, tpr, _ = scoring.roc_curve(scores, val['labels'])
        axes[0].plot(fpr, tpr, label=f"{name} (AUC {result['AUC']:.3f})")
        axes[0].scatter(result['FPR'], result['recall'], s=24)
        # DET uses Gaussian-deviate axes; clip endpoints for display only.
        axes[1].plot(ndtri(np.clip(fpr, 1e-4, 1-1e-4)),
                     ndtri(np.clip(1-tpr, 1e-4, 1-1e-4)))
        axes[1].scatter(ndtri(result['FPR']), ndtri(result['FNR']), s=24)
        yields, rho = scoring.postselection_curve(scores, val['labels'])
        axes[2].plot(yields, 1-rho)
    axes[0].plot([0, 1], [0, 1], 'k:', lw=1)
    axes[0].set(xlabel='False-positive rate', ylabel='True-positive rate', title='Validation ROC')
    axes[0].legend(fontsize=7, loc='lower right')
    ticks = np.array([.01, .05, .1, .2, .4, .6, .8, .95])
    axes[1].set(xticks=ndtri(ticks), yticks=ndtri(ticks),
                xticklabels=[f'{100*x:g}' for x in ticks],
                yticklabels=[f'{100*x:g}' for x in ticks],
                xlim=ndtri([.01, .95]), ylim=ndtri([.01, .95]),
                xlabel='False positives (%)', ylabel='Missed flips (%)', title='Validation DET')
    axes[2].axvline(.7, color='k', ls=':', lw=1)
    axes[2].set(xlabel='Yield (fraction retained)', ylabel='Flip suppression', title='Post-selection')
    fig.suptitle('Frozen Step-3 detector; dots mark global 70% yield', fontsize=12)
    fig.tight_layout(); fig.savefig(figures/'roc_det.png', dpi=170); plt.close(fig)

    scores = my_detector(train['nbar'], train['I'], train['Q'], calibration)
    all_metrics['Final: training tuning'] = metrics(scores[fit], train['labels'][fit])
    all_metrics['Final: held-out training'] = metrics(scores[heldout], train['labels'][heldout])
    val_scores = my_detector(val['nbar'], val['I'], val['Q'], calibration)
    by_cat = {}
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    for cat in np.unique(val['nbar']):
        rows = val['nbar'] == cat
        result = metrics(val_scores[rows], val['labels'][rows])
        by_cat[str(float(cat))] = result
        fpr, tpr, _ = scoring.roc_curve(val_scores[rows], val['labels'][rows])
        axes[0].plot(fpr, tpr, label=f"nbar={cat:g}: {result['AUC']:.3f}")
        yields, rho = scoring.postselection_curve(val_scores[rows], val['labels'][rows])
        axes[1].plot(yields, 1-rho, label=f'nbar={cat:g}')
    axes[0].plot([0,1], [0,1], 'k:'); axes[0].legend(fontsize=8)
    axes[0].set(xlabel='False-positive rate', ylabel='True-positive rate', title='Validation ROC by cat size')
    axes[1].axvline(.7, color='k', ls=':'); axes[1].legend(fontsize=8)
    axes[1].set(xlabel='Yield within cat size', ylabel='Flip suppression', title='Per-cat cuts are diagnostic only')
    fig.tight_layout(); fig.savefig(figures/'per_cat.png', dpi=170); plt.close(fig)
    report = dict(overall=all_metrics, validation_by_cat=by_cat,
                  fit_rows=len(fit), heldout_rows=len(heldout),
                  reported_leaderboard=dict(suppression=.47, points=6.8, source='team screenshot'))
    (output/'metrics.json').write_text(json.dumps(report, indent=2)+'\n')
    print('\nValidation: suppression is relative reduction of the retained flip fraction, not recall.')
    print(f"{'Detector':32} {'AUC':>7} {'Suppression':>12} {'Flips caught':>13}")
    for name, _, _ in modes:
        r = all_metrics[name]
        print(f"{name:32} {r['AUC']:7.3f} {r['suppression']:11.1%} {r['recall']:12.1%}")
    return calibration, report


def export_submission(test, calibration, path):
    """Write locally; no leaderboard connection and no hidden-label inference."""
    scores = my_detector(test['nbar'], test['I'], test['Q'], calibration)
    decisions = np.zeros(len(scores), dtype=np.int8)
    decisions[np.argsort(scores, kind='stable')[round(.7*len(scores)):]] = 1
    if not np.isfinite(scores).all():
        raise ValueError('Submission scores must be finite.')
    np.savetxt(path, np.column_stack((np.arange(len(scores)), scores, decisions)),
               delimiter=',', header='segment_id,score,decision', comments='',
               fmt=('%d', '%.17g', '%d'))
