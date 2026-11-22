"""Run the theory checks, record diagnostics, and frozen Step-3 evaluation.

    uv run python main.py                    # full demonstration
    uv run python main.py --skip-simulations # dataset analysis only
"""
import argparse
from pathlib import Path
import os


def main():
    root=Path(__file__).resolve().parent
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--skip-simulations',action='store_true',help='Only analyze the supplied records.')
    parser.add_argument('--export-test',action='store_true',help='Write outputs/tierB.csv locally; never upload.')
    parser.add_argument('--max-seeds',type=int,default=32,help='Bound the illustrative simulation search.')
    args=parser.parse_args()
    os.environ.setdefault('MPLBACKEND','Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'axes.spines.top':False,'axes.spines.right':False,
                         'font.size':10,'savefig.facecolor':'white'})
    from catflip.data import load
    from catflip.evaluation import evaluate,export_submission
    from catflip.diagnostics import trajectory_examples,ensemble_spectra,click_examples
    figures=root/'figures'; output=root/'outputs'
    figures.mkdir(exist_ok=True); output.mkdir(exist_ok=True)
    train,val=(load(root/'data','B',split) for split in ('train','val'))
    if not args.skip_simulations:
        import jax
        print('JAX backend:',jax.default_backend(),'| devices:',jax.devices(),flush=True)
        from catflip.simulation import linear_response,counting_examples,heterodyne_examples
        print('Simulating counting examples with flip/no-flip terminal readouts...',flush=True)
        counting_examples(figures,output,args.max_seeds)
        print('Simulating buffer-conditioned heterodyne records and density matrices...',flush=True)
        heterodyne_examples(figures,output,args.max_seeds)
        print('Checking the predicted small-displacement response (known two-mode model)...',flush=True)
        linear_response(figures,output)
    trajectory_examples(val,figures,output)
    ensemble_spectra(val,figures,output)
    click_examples(load(root/'data','A','val'),figures)
    calibration,_=evaluate(train,val,figures,output)
    if args.export_test:
        export_submission(load(root/'data','B','test'),calibration,output/'tierB.csv')
        print('Wrote local submission; no upload performed.')
    print(f'\nFigures: {figures}\nNumerical results and simulated states: {output}')


if __name__=='__main__':
    main()
