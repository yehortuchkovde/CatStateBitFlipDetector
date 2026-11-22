"""Alignment and baseline-invariance checks for the all-record diagnostic."""
import unittest
import numpy as np
from catflip.diagnostics import candidate_excursion_power


class ExcursionPowerTests(unittest.TestCase):
    def setUp(self):
        self.I = np.random.default_rng(15).normal(size=(3, 80))
        self.starts = np.array([0, 36, 76])
        for row, start in enumerate(self.starts):
            self.I[row, start:start+4] -= 100
        self.cats = np.array([2., 2.5, 3.])

    def test_edge_windows_shift_without_padding_or_dropping_records(self):
        before = self.I.copy()
        self.I.setflags(write=False)
        for length, expected in [(3, [0, 36, 76]), (4, [0, 36, 76]), (32, [0, 22, 48])]:
            with self.subTest(bins=length):
                power, dc_start, inspection_start = candidate_excursion_power(self.I, self.cats, .5, length)
                np.testing.assert_array_equal(dc_start, self.starts)
                np.testing.assert_array_equal(inspection_start, expected)
                np.testing.assert_array_equal(self.I, before)
                self.assertEqual(len(power), 3)
                self.assertTrue(np.all(np.isfinite(power) & (power >= 0)))

    def test_constant_record_offsets_do_not_change_the_diagnostic(self):
        for length in (3, 4, 32):
            with self.subTest(bins=length):
                first = candidate_excursion_power(self.I, self.cats, .5, length)
                shifted = candidate_excursion_power(self.I + np.array([5, -6, 12])[:, None], self.cats, .5, length)
                for a, b in zip(first, shifted):
                    np.testing.assert_allclose(a, b, rtol=1e-12, atol=1e-12)

    def test_control_frequencies_do_not_reselect_events(self):
        for length in (3, 4):
            _, starts, windows = candidate_excursion_power(self.I, self.cats, .5, length)
            for factor in (.5, 1.5):
                _, other_starts, other_windows = candidate_excursion_power(self.I, self.cats, .5, length, factor)
                np.testing.assert_array_equal(starts, other_starts)
                np.testing.assert_array_equal(windows, other_windows)
