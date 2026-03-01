"""Tests for rainflow cycle counting."""

import pytest
import numpy as np

from weldfatigue.utils.rainflow import rainflow_count, signal_to_spectrum


class TestRainflowCount:

    def test_simple_cycle(self):
        """A simple up-down-up signal should produce one full cycle."""
        signal = np.array([0, 100, -100, 0])
        cycles = rainflow_count(signal)
        assert len(cycles) > 0
        # Total count should be positive
        total = sum(c[2] for c in cycles)
        assert total > 0

    def test_constant_signal_no_cycles(self):
        """Constant signal has no reversals -> minimal cycles."""
        signal = np.array([50, 50, 50, 50])
        cycles = rainflow_count(signal)
        ranges = [c[0] for c in cycles]
        assert all(r == 0 for r in ranges)

    def test_symmetric_sinusoidal(self):
        """Sinusoidal signal with known amplitude."""
        t = np.linspace(0, 2 * np.pi * 5, 1000)
        signal = 100 * np.sin(t)
        cycles = rainflow_count(signal)
        assert len(cycles) > 0
        # Largest range should be close to 200 (peak-to-peak)
        max_range = max(c[0] for c in cycles)
        assert max_range == pytest.approx(200.0, rel=0.05)

    def test_output_format(self):
        """Each cycle should be (range, mean, count)."""
        signal = np.array([0, 100, 0, 80, 0])
        cycles = rainflow_count(signal)
        for rng, mean, count in cycles:
            assert isinstance(rng, (int, float, np.integer, np.floating))
            assert isinstance(mean, (int, float, np.integer, np.floating))
            assert float(count) in (0.5, 1.0)

    def test_monotonic_signal(self):
        """Monotonic increasing signal has no internal reversals."""
        signal = np.array([0, 10, 20, 30, 40])
        cycles = rainflow_count(signal)
        # Should have only half-cycles from the start/end
        for _, _, count in cycles:
            assert count == 0.5

    def test_two_peaks(self):
        signal = np.array([0, 100, 0, 50, 0])
        cycles = rainflow_count(signal)
        ranges = sorted([c[0] for c in cycles], reverse=True)
        assert ranges[0] == pytest.approx(100.0, rel=1e-6)


class TestSignalToSpectrum:

    def test_basic_conversion(self):
        t = np.linspace(0, 2 * np.pi * 3, 500)
        signal = 80 * np.sin(t) + 20 * np.sin(3 * t)
        spectrum = signal_to_spectrum(signal, n_bins=32)
        assert len(spectrum) > 0
        # Sorted by descending range
        for i in range(len(spectrum) - 1):
            assert spectrum[i][0] >= spectrum[i + 1][0]

    def test_output_format(self):
        signal = np.array([0, 100, -50, 80, -30, 60])
        spectrum = signal_to_spectrum(signal, n_bins=8)
        for stress_range, num_cycles in spectrum:
            assert stress_range > 0
            assert num_cycles >= 0

    def test_empty_signal(self):
        signal = np.array([50, 50, 50])
        spectrum = signal_to_spectrum(signal, n_bins=8)
        # Constant signal -> no meaningful cycles
        assert len(spectrum) == 0 or all(s[0] == 0 for s in spectrum)
