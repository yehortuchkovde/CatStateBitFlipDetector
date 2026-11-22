"""Physical consistency of the illustrative Wigner trajectory."""
from pathlib import Path
import unittest
import numpy as np
from catflip.wigner_demo import localized_counting_model

ROOT = Path(__file__).resolve().parents[1]


class WignerDemoTests(unittest.TestCase):
    def test_environment_measurement_preserves_generator(self):
        from catchtheflip import models
        model, error = localized_counting_model()
        original = models.single_mode(models.SingleModeParams(nbar=2, N=24))
        self.assertLess(error, 1e-11)
        np.testing.assert_array_equal(model.L_buffer.to_jax(), original.L_buffer.to_jax())

    def test_saved_example_is_a_resolved_switch(self):
        path = ROOT / 'outputs/wigner_trajectory.npz'
        if not path.exists():
            self.skipTest('Run main.py --wigner-only to create the state trajectory.')
        with np.load(path, allow_pickle=False) as data:
            self.assertEqual(int(data['seed']), 7)
            self.assertGreater(float(data['z'][0]), .8)
            self.assertLess(float(np.max(data['z'][-100:])), -.8)
            psi = data['states']
            np.testing.assert_allclose(np.sum(np.abs(psi)**2, axis=1), 1, atol=1e-10)
            clicks = data['clicktimes'][0]
            clicks = clicks[np.isfinite(clicks)]
            self.assertTrue(np.all((clicks >= 0) & (clicks <= data['t'][-1])))
