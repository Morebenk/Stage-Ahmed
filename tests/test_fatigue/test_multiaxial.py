"""Tests for multiaxial fatigue assessment."""

import math
import numpy as np
import pytest
from weldfatigue.fatigue.multiaxial import MultiaxialFatigueAssessment


class TestMultiaxialFatigue:
    """Tests for MultiaxialFatigueAssessment class."""

    # --- Proportionality detection ---

    def test_proportional_constant_ratio(self):
        """Constant ratio => proportional."""
        normal = np.array([10, 20, 30, 40, 50], dtype=float)
        shear = np.array([5, 10, 15, 20, 25], dtype=float)
        assert MultiaxialFatigueAssessment.detect_proportionality(normal, shear)

    def test_non_proportional_varying_ratio(self):
        """Varying ratio with phase shift => non-proportional."""
        t = np.linspace(0.1, np.pi - 0.1, 100)  # Avoid zero-crossings
        normal = 100 * np.sin(t)
        shear = 50 * np.cos(t)  # 90-degree phase shift, different shape
        assert not MultiaxialFatigueAssessment.detect_proportionality(normal, shear, 0.1)

    # --- Gough-Pollard tests ---

    def test_gp_pure_normal(self):
        """Pure normal stress: interaction = (dS/dS_R)^2."""
        result = MultiaxialFatigueAssessment.gough_pollard(
            delta_sigma=71.0, delta_tau=0.0, fat_sigma=71, fat_tau=36, num_cycles=2_000_000
        )
        assert result["interaction_value"] == pytest.approx(1.0, rel=1e-3)
        assert result["shear_utilization"] == pytest.approx(0.0)

    def test_gp_pure_shear(self):
        """Pure shear: interaction = (dT/dT_R)^2."""
        result = MultiaxialFatigueAssessment.gough_pollard(
            delta_sigma=0.0, delta_tau=36.0, fat_sigma=71, fat_tau=36, num_cycles=2_000_000
        )
        assert result["interaction_value"] == pytest.approx(1.0, rel=1e-3)
        assert result["normal_utilization"] == pytest.approx(0.0)

    def test_gp_combined_pass(self):
        """Combined low stress: should pass."""
        result = MultiaxialFatigueAssessment.gough_pollard(
            delta_sigma=30.0, delta_tau=15.0, fat_sigma=71, fat_tau=36, num_cycles=2_000_000
        )
        assert result["status"] == "PASS"
        assert result["interaction_value"] < 1.0

    def test_gp_combined_fail(self):
        """Combined high stress: should fail."""
        result = MultiaxialFatigueAssessment.gough_pollard(
            delta_sigma=71.0, delta_tau=36.0, fat_sigma=71, fat_tau=36, num_cycles=2_000_000
        )
        assert result["status"] == "FAIL"
        assert result["interaction_value"] > 1.0

    def test_gp_at_reference_life(self):
        """At 2e6 cycles, allowable = FAT class value."""
        result = MultiaxialFatigueAssessment.gough_pollard(
            delta_sigma=50.0, delta_tau=25.0, fat_sigma=71, fat_tau=36, num_cycles=2_000_000
        )
        # (50/71)^2 + (25/36)^2
        expected = (50 / 71) ** 2 + (25 / 36) ** 2
        assert result["interaction_value"] == pytest.approx(expected, rel=1e-3)

    # --- Findley critical plane tests ---

    def test_findley_uniaxial(self):
        """Uniaxial case: Findley reduces to standard fatigue."""
        result = MultiaxialFatigueAssessment.findley_critical_plane(
            sigma_a=50.0, tau_a=0.0, sigma_max=50.0, k=0.3, fatigue_limit=100.0
        )
        assert result["status"] == "PASS"
        assert result["findley_parameter"] > 0

    def test_findley_high_stress_fails(self):
        """High combined stress should fail."""
        result = MultiaxialFatigueAssessment.findley_critical_plane(
            sigma_a=80.0, tau_a=60.0, sigma_max=80.0, k=0.3, fatigue_limit=50.0
        )
        assert result["status"] == "FAIL"

    def test_findley_critical_angle_range(self):
        """Critical angle should be between 0 and 180 degrees."""
        result = MultiaxialFatigueAssessment.findley_critical_plane(
            sigma_a=50.0, tau_a=30.0, sigma_max=50.0
        )
        assert 0 <= result["critical_angle_deg"] <= 180

    # --- MWCM tests ---

    def test_mwcm_uniaxial(self):
        """Pure normal: equivalent = normal stress range."""
        result = MultiaxialFatigueAssessment.mwcm(
            delta_sigma=71.0, delta_tau=0.0, fat_class=71
        )
        assert result["equivalent_stress_range"] == pytest.approx(71.0)
        assert result["utilization"] == pytest.approx(1.0)

    def test_mwcm_combined(self):
        """Combined loading: Von Mises equivalent."""
        result = MultiaxialFatigueAssessment.mwcm(
            delta_sigma=50.0, delta_tau=30.0, fat_class=71
        )
        expected_eq = math.sqrt(50 ** 2 + 3 * 30 ** 2)
        assert result["equivalent_stress_range"] == pytest.approx(expected_eq, rel=1e-3)

    def test_mwcm_slope_increases_with_multiaxiality(self):
        """Higher biaxiality ratio => higher effective slope."""
        r1 = MultiaxialFatigueAssessment.mwcm(100.0, 10.0, 71)
        r2 = MultiaxialFatigueAssessment.mwcm(100.0, 80.0, 71)
        assert r2["modified_slope"] > r1["modified_slope"]

    def test_mwcm_pure_shear(self):
        """Pure shear uses Von Mises equivalent."""
        result = MultiaxialFatigueAssessment.mwcm(0.0, 50.0, 71)
        expected = 50.0 * math.sqrt(3)
        assert result["equivalent_stress_range"] == pytest.approx(expected, rel=1e-3)

    # --- Dispatch tests ---

    def test_evaluate_gp(self):
        result = MultiaxialFatigueAssessment.evaluate(
            "gough_pollard", 50.0, 25.0, 71, 36, 2_000_000
        )
        assert result["method"] == "gough_pollard"

    def test_evaluate_findley(self):
        result = MultiaxialFatigueAssessment.evaluate(
            "findley", 100.0, 50.0, 71
        )
        assert result["method"] == "findley"

    def test_evaluate_mwcm(self):
        result = MultiaxialFatigueAssessment.evaluate(
            "mwcm", 50.0, 30.0, 71
        )
        assert result["method"] == "mwcm"

    def test_evaluate_unknown_raises(self):
        with pytest.raises(ValueError):
            MultiaxialFatigueAssessment.evaluate("unknown", 50.0, 25.0, 71)
