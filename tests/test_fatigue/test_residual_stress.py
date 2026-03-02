"""Tests for residual stress modeling."""

import math
import pytest
from weldfatigue.fatigue.residual_stress import ResidualStressModel


class TestResidualStressModel:
    """Tests for ResidualStressModel class."""

    # --- As-welded peak ---

    def test_as_welded_peak_equals_yield(self):
        """Conservative assumption: sigma_res = yield strength."""
        assert ResidualStressModel.as_welded_peak(355.0) == pytest.approx(355.0)

    def test_as_welded_peak_high_strength(self):
        assert ResidualStressModel.as_welded_peak(960.0) == pytest.approx(960.0)

    # --- PWHT relief ---

    def test_pwht_no_treatment(self):
        """No PWHT (low temp) => factor = 1.0."""
        f = ResidualStressModel.pwht_relief_factor(100.0, 1.0)
        assert f == pytest.approx(1.0)

    def test_pwht_600c_1h(self):
        """600°C for 1h => significant relief (factor < 0.3)."""
        f = ResidualStressModel.pwht_relief_factor(600.0, 1.0)
        assert f < 0.3

    def test_pwht_higher_temp_more_relief(self):
        """Higher temperature gives more relief."""
        f550 = ResidualStressModel.pwht_relief_factor(550.0, 1.0)
        f650 = ResidualStressModel.pwht_relief_factor(650.0, 1.0)
        assert f650 < f550

    def test_pwht_longer_hold_more_relief(self):
        """Longer hold time gives more relief."""
        f1 = ResidualStressModel.pwht_relief_factor(600.0, 1.0)
        f4 = ResidualStressModel.pwht_relief_factor(600.0, 4.0)
        assert f4 < f1

    def test_pwht_minimum_residual(self):
        """PWHT factor should not go below 0.05."""
        f = ResidualStressModel.pwht_relief_factor(800.0, 10.0)
        assert f >= 0.05

    # --- Residual after PWHT ---

    def test_residual_after_pwht_no_treatment(self):
        """Without PWHT, residual = yield."""
        r = ResidualStressModel.residual_after_pwht(355.0)
        assert r == pytest.approx(355.0)

    def test_residual_after_pwht_with_treatment(self):
        """With PWHT, residual is reduced."""
        r = ResidualStressModel.residual_after_pwht(355.0, 600.0, 1.0)
        assert r < 355.0

    # --- Relaxation under cycling ---

    def test_relaxation_no_plasticity(self):
        """If sigma_res + sigma_max < yield, no first-cycle relaxation."""
        r = ResidualStressModel.relaxation_under_cycling(100.0, 100.0, 355.0, 1)
        assert r == pytest.approx(100.0)

    def test_relaxation_with_plasticity(self):
        """If sigma_res + sigma_max > yield, shakedown occurs."""
        r = ResidualStressModel.relaxation_under_cycling(
            355.0, 200.0, 355.0, 1
        )
        expected = 355.0 - 100.0  # yield - sigma_max
        assert r == pytest.approx(expected)

    def test_relaxation_cyclic_reduction(self):
        """Multiple cycles further reduce residual stress."""
        r1 = ResidualStressModel.relaxation_under_cycling(100.0, 50.0, 355.0, 1)
        r1000 = ResidualStressModel.relaxation_under_cycling(100.0, 50.0, 355.0, 1000)
        assert r1000 < r1

    def test_relaxation_never_negative(self):
        """Residual stress should never go negative."""
        r = ResidualStressModel.relaxation_under_cycling(50.0, 400.0, 355.0, 1)
        assert r >= 0.0

    # --- Effective R-ratio ---

    def test_effective_r_no_residual(self):
        """Without residual stress, R_eff = standard R."""
        R_eff = ResidualStressModel.effective_stress_ratio(100.0, 0.0, 0.0)
        # sigma_max = 50, sigma_min = -50, R = -1
        assert R_eff == pytest.approx(-1.0)

    def test_effective_r_with_residual(self):
        """With residual stress, R_eff shifts towards positive."""
        R_no = ResidualStressModel.effective_stress_ratio(100.0, 0.0, 0.0)
        R_with = ResidualStressModel.effective_stress_ratio(100.0, 0.0, 200.0)
        assert R_with > R_no  # Residual shifts R upward

    # --- Superposition ---

    def test_superpose_range_unchanged(self):
        """Stress range is unchanged by residual stress superposition."""
        sr, sm = ResidualStressModel.superpose_on_applied(100.0, 50.0, 200.0)
        assert sr == pytest.approx(100.0)  # Range unchanged
        assert sm == pytest.approx(250.0)  # Mean shifted

    # --- Through-thickness distribution ---

    def test_distribution_self_equilibrating(self):
        """Through-thickness residual stress should approximately integrate to zero."""
        depths, stresses = ResidualStressModel.through_thickness_distribution(
            355.0, 20.0, 100
        )
        # Trapezoidal integration
        integral = 0.0
        for i in range(len(depths) - 1):
            dz = depths[i + 1] - depths[i]
            avg_stress = (stresses[i] + stresses[i + 1]) / 2.0
            integral += avg_stress * dz
        # Should be close to zero for self-equilibrating
        assert abs(integral) < 10.0  # Allow small numerical error

    def test_distribution_surface_tension(self):
        """Surface should have tensile residual stress."""
        depths, stresses = ResidualStressModel.through_thickness_distribution(
            355.0, 20.0, 20
        )
        assert stresses[0] > 0  # Surface is in tension
