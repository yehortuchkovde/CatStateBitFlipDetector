"""Regression checks against the submitted detector and public split boundaries."""
import json
from pathlib import Path
import unittest
import numpy as np
from catflip.data import load,content_hash
from catflip.detector import training_split,calibrate,my_detector
from catflip.evaluation import metrics

ROOT=Path(__file__).resolve().parents[1]


class ReproductionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.train=load(ROOT/'data','B','train')
        cls.val=load(ROOT/'data','B','val')
        cls.fit,cls.heldout=training_split(cls.train)
        cls.calibration=calibrate(cls.train,cls.fit)
        cls.scores=my_detector(cls.val['nbar'],cls.val['I'],cls.val['Q'],cls.calibration)

    def test_submission_regression(self):
        r=metrics(self.scores,self.val['labels'])
        self.assertAlmostEqual(r['AUC'],.7533418863245274,places=12)
        self.assertAlmostEqual(r['suppression'],.5124329595319356,places=12)
        self.assertEqual(r['flips_caught'],386)
        self.assertEqual((len(self.fit),len(self.heldout)),(10500,4500))
        self.assertEqual(len(np.intersect1d(self.fit,self.heldout)),0)

    def test_scores_do_not_depend_on_other_records_in_batch(self):
        rows=np.array([0,1,6406,1523,7499])
        independent=my_detector(self.val['nbar'][rows],self.val['I'][rows],
                                self.val['Q'][rows],self.calibration)
        np.testing.assert_allclose(independent,self.scores[rows],rtol=1e-13,atol=1e-13)

    def test_all_public_files_and_hidden_labels(self):
        manifest=json.loads((ROOT/'data/manifest.json').read_text())
        for name,entry in manifest['files'].items():
            tier,split=name[4],name[6:-4]
            d=load(ROOT/'data',tier,split)
            self.assertEqual(content_hash(d),entry['content_sha256'],name)
            self.assertEqual(len(d['nbar']),entry['segments'])
            self.assertEqual('labels' in d,split!='test')

    def test_simulated_density_matrices_when_available(self):
        paths=[ROOT/'outputs'/f'{method}_{case}.npz'
               for method in ('counting','heterodyne') for case in ('flip','no_flip')]
        if not all(p.exists() for p in paths):
            self.skipTest('Run the full demo to create simulated density matrices.')
        for path in paths:
            with np.load(path,allow_pickle=False) as f:
                rho=f['rho']
                np.testing.assert_allclose(np.trace(rho,axis1=-2,axis2=-1),1,atol=1e-10)
                np.testing.assert_allclose(rho,rho.conj().swapaxes(-1,-2),atol=1e-10)
                self.assertGreater(np.linalg.eigvalsh(rho[-1]).min(),-1e-10)
                self.assertAlmostEqual(float(np.trace(f['rho_post_readout']).real),1,places=10)


if __name__=='__main__': unittest.main()
