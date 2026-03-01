"""Tests for weld failure criteria."""

import pytest
import math

from weldfatigue.shock.weld_failure import WeldFailureCriteria


class TestForceBasedCheck:

    def test_pass_low_forces(self):
        result = WeldFailureCriteria.force_based_check(
            normal_force=500,
            shear_force=300,
            weld_throat=5.0,
            weld_length=100.0,
            allowable_stress=400.0,
        )
        assert result.status == "PASS"
        assert result.utilization < 1.0
        assert result.criterion == "force_based"

    def test_fail_high_forces(self):
        result = WeldFailureCriteria.force_based_check(
            normal_force=200000,
            shear_force=150000,
            weld_throat=5.0,
            weld_length=100.0,
            allowable_stress=400.0,
        )
        assert result.status == "FAIL"
        assert result.utilization > 1.0

    def test_equivalent_stress_formula(self):
        result = WeldFailureCriteria.force_based_check(
            normal_force=1000,
            shear_force=0,
            weld_throat=10.0,
            weld_length=100.0,
            allowable_stress=500.0,
        )
        assert result.equivalent_stress == pytest.approx(1.0)

    def test_combined_stress(self):
        result = WeldFailureCriteria.force_based_check(
            normal_force=3000,
            shear_force=4000,
            weld_throat=10.0,
            weld_length=100.0,
            allowable_stress=500.0,
        )
        assert result.equivalent_stress == pytest.approx(5.0)

    def test_zero_weld_area_raises(self):
        with pytest.raises(ValueError, match="positive"):
            WeldFailureCriteria.force_based_check(
                normal_force=100, shear_force=50,
                weld_throat=0, weld_length=100,
                allowable_stress=400,
            )

    def test_custom_safety_factor(self):
        r1 = WeldFailureCriteria.force_based_check(
            normal_force=500, shear_force=300,
            weld_throat=5.0, weld_length=100.0,
            allowable_stress=400.0, safety_factor=1.0,
        )
        r2 = WeldFailureCriteria.force_based_check(
            normal_force=500, shear_force=300,
            weld_throat=5.0, weld_length=100.0,
            allowable_stress=400.0, safety_factor=2.0,
        )
        # Higher safety factor -> higher utilization
        assert r2.utilization > r1.utilization


class TestStressBasedCheck:

    def test_pass_low_stress(self):
        result = WeldFailureCriteria.stress_based_check(
            sigma_perp=50,
            tau_perp=30,
            tau_parallel=20,
            fu=500,
        )
        assert result.status == "PASS"
        assert result.utilization < 1.0

    def test_fail_high_stress(self):
        result = WeldFailureCriteria.stress_based_check(
            sigma_perp=400,
            tau_perp=200,
            tau_parallel=150,
            fu=500,
        )
        assert result.status == "FAIL"
        assert result.utilization > 1.0

    def test_en1993_formula(self):
        """Verify sqrt(sigma_perp^2 + 3*(tau_perp^2 + tau_par^2))."""
        result = WeldFailureCriteria.stress_based_check(
            sigma_perp=100,
            tau_perp=0,
            tau_parallel=0,
            fu=500,
        )
        assert result.equivalent_stress == pytest.approx(100.0)

    def test_en1993_combined(self):
        result = WeldFailureCriteria.stress_based_check(
            sigma_perp=0,
            tau_perp=100,
            tau_parallel=0,
            fu=500,
        )
        expected = math.sqrt(3 * 100**2)  # = 173.2
        assert result.equivalent_stress == pytest.approx(expected, rel=1e-3)

    def test_criterion_label(self):
        result = WeldFailureCriteria.stress_based_check(
            sigma_perp=50, tau_perp=30, tau_parallel=20, fu=500,
        )
        assert result.criterion == "stress_based_EN1993"

    def test_custom_beta_w(self):
        r1 = WeldFailureCriteria.stress_based_check(
            sigma_perp=100, tau_perp=50, tau_parallel=30,
            fu=500, beta_w=0.8,
        )
        r2 = WeldFailureCriteria.stress_based_check(
            sigma_perp=100, tau_perp=50, tau_parallel=30,
            fu=500, beta_w=1.0,
        )
        # beta_w=1.0 gives lower allowable -> higher utilization
        assert r2.utilization > r1.utilization
