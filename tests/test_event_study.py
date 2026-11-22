"""State-based event timing and paired, trajectory-level uncertainty."""
import unittest
import numpy as np
from catflip.event_study import z_transitions,select_event_windows,_paired_cluster_means,_spectral_power


class EventStudyTests(unittest.TestCase):
    def test_opposite_plateaus_define_one_switch_in_either_direction(self):
        z=np.r_[np.ones(300),np.linspace(1,-1,41),-np.ones(300)]
        for sign in (1,-1):
            events=z_transitions(sign*z,.1)
            self.assertEqual(len(events),1)
            self.assertEqual(events[0]['before'],sign)
            self.assertAlmostEqual(events[0]['zero_crossing_time'],32.,places=10)
            self.assertTrue(events[0]['left'] <= events[0]['anchor'] <= events[0]['right'])

    def test_unconfirmed_short_recrossing_is_not_a_metastable_event(self):
        z=np.ones(400);z[150:155]=-.99
        self.assertEqual(z_transitions(z,.1),[])

    def test_event_selection_never_looks_at_fourier_or_record_amplitude(self):
        z=np.r_[np.ones(300),np.linspace(1,-1,41),-np.ones(300)]
        rng=np.random.default_rng(6)
        data=dict(z=np.stack([z,z]),I=rng.normal(size=(2,len(z)-1)),Q=rng.normal(size=(2,len(z)-1)))
        first=select_event_windows(data,target=2)
        data['I']*=100; data['Q']+=30
        second=select_event_windows(data,target=2)
        for key in ('trajectory','event_center','control_center','before'):
            np.testing.assert_array_equal(first[key],second[key])
        self.assertEqual(len(first['trajectory']),2)

    def test_bootstrap_preserves_pairing_and_clusters(self):
        ids=np.array([0,0,0,1,2])
        control=np.array([[1.],[1.],[1.],[5.],[8.]])
        event=control+2
        _,_,difference=_paired_cluster_means(event,control,ids,np.random.default_rng(4),repetitions=100)
        np.testing.assert_allclose(difference,2,atol=1e-12)

    def test_unselected_white_noise_normalization(self):
        rng=np.random.default_rng(92);dt=.5
        windows=rng.normal(0,1/np.sqrt(dt),size=(8000,16))
        powers=_spectral_power(windows,dt,np.array([1.,2.65,5.]))
        np.testing.assert_allclose(powers.mean(0),1,atol=.05)
