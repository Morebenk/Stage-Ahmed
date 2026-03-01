"""Tests for energy absorption metrics."""

import pytest
import numpy as np

from weldfatigue.shock.energy import EnergyAbsorption


class TestTotalEnergy:

    def test_rectangular_pulse(self):
        """Constant force over distance -> E = F * d."""
        force = np.array([1000, 1000, 1000, 1000])
        disp = np.array([0, 10, 20, 30], dtype=float)
        energy = EnergyAbsorption.total_energy(force, disp)
        assert energy == pytest.approx(30000.0)

    def test_triangular_pulse(self):
        """Linear ramp: E = 0.5 * F_max * d_max."""
        force = np.array([0, 1000])
        disp = np.array([0, 20], dtype=float)
        energy = EnergyAbsorption.total_energy(force, disp)
        assert energy == pytest.approx(10000.0)

    def test_zero_force(self):
        force = np.zeros(10)
        disp = np.linspace(0, 100, 10)
        energy = EnergyAbsorption.total_energy(force, disp)
        assert energy == pytest.approx(0.0)


class TestSpecificEnergyAbsorption:

    def test_basic(self):
        sea = EnergyAbsorption.specific_energy_absorption(5000, 2.5)
        assert sea == pytest.approx(2000.0)

    def test_zero_mass_raises(self):
        with pytest.raises(ValueError, match="positive"):
            EnergyAbsorption.specific_energy_absorption(5000, 0)

    def test_negative_mass_raises(self):
        with pytest.raises(ValueError, match="positive"):
            EnergyAbsorption.specific_energy_absorption(5000, -1.0)


class TestCrushMetrics:

    @pytest.fixture
    def sample_data(self):
        force = np.array([0, 5000, 10000, 8000, 7000, 6000], dtype=float)
        disp = np.array([0, 5, 10, 15, 20, 25], dtype=float)
        return force, disp

    def test_peak_force(self, sample_data):
        force, disp = sample_data
        metrics = EnergyAbsorption.crush_metrics(force, disp)
        assert metrics.peak_force == pytest.approx(10000.0)

    def test_mean_force(self, sample_data):
        force, disp = sample_data
        metrics = EnergyAbsorption.crush_metrics(force, disp)
        assert metrics.mean_force > 0

    def test_cfe_range(self, sample_data):
        force, disp = sample_data
        metrics = EnergyAbsorption.crush_metrics(force, disp)
        assert 0 < metrics.crush_force_efficiency <= 1.0

    def test_total_energy_positive(self, sample_data):
        force, disp = sample_data
        metrics = EnergyAbsorption.crush_metrics(force, disp)
        assert metrics.total_energy > 0

    def test_sea_with_mass(self, sample_data):
        force, disp = sample_data
        metrics = EnergyAbsorption.crush_metrics(force, disp, mass=5.0)
        assert metrics.specific_energy_absorption is not None
        assert metrics.specific_energy_absorption > 0

    def test_sea_without_mass(self, sample_data):
        force, disp = sample_data
        metrics = EnergyAbsorption.crush_metrics(force, disp)
        assert metrics.specific_energy_absorption is None

    def test_cfe_formula(self):
        """CFE = mean_force / peak_force."""
        # Constant force -> CFE = 1.0
        force = np.array([500, 500, 500, 500], dtype=float)
        disp = np.array([0, 10, 20, 30], dtype=float)
        metrics = EnergyAbsorption.crush_metrics(force, disp)
        assert metrics.crush_force_efficiency == pytest.approx(1.0)
