"""Tests for the 4R fatigue assessment method."""

import math
import pytest

from weldfatigue.fatigue.four_r_method import FourRMethod


class TestNeuberCorrection:
    """Tests for Neuber elastic-plastic correction."""

    def test_elastic_regime(self):
        """Stress below yield: no correction needed."""
        sigma, eps = FourRMethod.neuber_correction(200.0, 355.0, 210000.0)
        assert sigma == pytest.approx(200.0)
        assert eps == pytest.approx(200.0 / 210000.0)

    def test_at_yield(self):
        """Stress exactly at yield."""
        sigma, eps = FourRMethod.neuber_correction(355.0, 355.0, 210000.0)
        assert sigma == pytest.approx(355.0)
        assert eps == pytest.approx(355.0 / 210000.0)

    def test_plastic_regime(self):
        """Stress above yield: Neuber correction applies."""
        sigma, eps = FourRMethod.neuber_correction(500.0, 355.0, 210000.0)
        assert sigma == pytest.approx(355.0)  # Clamped at yield
        assert eps == pytest.approx(500.0 ** 2 / (210000.0 * 355.0))
        assert eps > 355.0 / 210000.0  # Strain exceeds elastic limit

    def test_compressive_elastic(self):
        """Compressive stress below yield."""
        sigma, eps = FourRMethod.neuber_correction(-200.0, 355.0, 210000.0)
        assert sigma == pytest.approx(-200.0)

    def test_compressive_plastic(self):
        """Compressive stress above yield magnitude."""
        sigma, eps = FourRMethod.neuber_correction(-500.0, 355.0, 210000.0)
        assert sigma == pytest.approx(-355.0)  # Clamped at -yield


class TestLocalStressRatio:
    """Tests for local stress ratio computation."""

    def test_fully_elastic_r0(self):
        """R=0 loading, no residual: R_local = 0."""
        R = FourRMethod.local_stress_ratio(200.0, 0.0, 0.0, 355.0)
        assert R == pytest.approx(0.0, abs=1e-6)

    def test_with_tensile_residual(self):
        """Tensile residual stress shifts R_local upward."""
        R_no_res = FourRMethod.local_stress_ratio(200.0, 0.0, 0.0, 355.0)
        R_with_res = FourRMethod.local_stress_ratio(200.0, 0.0, 100.0, 355.0)
        assert R_with_res > R_no_res

    def test_high_residual_clamp_at_yield(self):
        """Residual stress causing total > yield should be clamped."""
        R = FourRMethod.local_stress_ratio(300.0, 0.0, 300.0, 355.0)
        # Both max and min are clamped, so R should reflect clamped values
        assert R <= 1.0

    def test_zero_max_stress(self):
        """Zero max stress returns R=0."""
        R = FourRMethod.local_stress_ratio(0.0, 0.0, 0.0, 355.0)
        assert R == pytest.approx(0.0)


class TestMeanStressSensitivity:
    """Tests for mean stress sensitivity parameter M."""

    def test_low_strength_steel(self):
        """Rm=400 MPa: M = 0.00035*400 - 0.1 = 0.04."""
        M = FourRMethod.mean_stress_sensitivity(400.0)
        assert M == pytest.approx(0.04)

    def test_medium_strength_steel(self):
        """Rm=600 MPa: M = 0.00035*600 - 0.1 = 0.11."""
        M = FourRMethod.mean_stress_sensitivity(600.0)
        assert M == pytest.approx(0.11)

    def test_high_strength_steel(self):
        """Rm=1000 MPa: M = 0.00035*1000 - 0.1 = 0.25."""
        M = FourRMethod.mean_stress_sensitivity(1000.0)
        assert M == pytest.approx(0.25)

    def test_very_low_strength_clamped(self):
        """Below Rm≈286 MPa, M is clamped at 0."""
        M = FourRMethod.mean_stress_sensitivity(200.0)
        assert M == pytest.approx(0.0)

    def test_always_non_negative(self):
        """M should never be negative."""
        for rm in [100, 200, 250, 285, 286]:
            assert FourRMethod.mean_stress_sensitivity(float(rm)) >= 0.0


class TestEquivalentStressRange:
    """Tests for equivalent stress range computation."""

    def test_r_zero_no_change(self):
        """At R=0 and M>0: Δσ_eq = Δσ * 1/(1+M)."""
        M = 0.1
        ds_eq = FourRMethod.equivalent_stress_range(100.0, 0.0, M)
        assert ds_eq == pytest.approx(100.0 / 1.1, rel=1e-4)

    def test_r_minus_one(self):
        """At R=-1: Δσ_eq = Δσ * (1+M)/(1+M) = Δσ."""
        M = 0.1
        ds_eq = FourRMethod.equivalent_stress_range(100.0, -1.0, M)
        assert ds_eq == pytest.approx(100.0, rel=1e-4)

    def test_m_zero_no_correction(self):
        """With M=0, no mean stress correction."""
        ds_eq = FourRMethod.equivalent_stress_range(100.0, 0.5, 0.0)
        assert ds_eq == pytest.approx(100.0)

    def test_high_r_reduces_range(self):
        """High R (tensile mean stress) reduces equivalent range."""
        M = 0.15
        ds_eq = FourRMethod.equivalent_stress_range(100.0, 0.5, M)
        assert ds_eq < 100.0


class TestEvaluate:
    """Tests for full 4R evaluation."""

    def test_basic_evaluation(self):
        """Standard evaluation returns valid FourRResult."""
        result = FourRMethod.evaluate(
            notch_stress_range=150.0,
            stress_ratio=0.0,
            residual_stress=0.0,
            ultimate_strength=500.0,
            yield_strength=355.0,
            num_cycles=1_000_000,
        )
        assert result.master_curve_fat == 200
        assert result.applied_cycles == 1_000_000
        assert result.equivalent_stress_range > 0
        assert result.allowable_cycles > 0

    def test_with_residual_stress(self):
        """Residual stress increases R_local and reduces equivalent range."""
        result_no_res = FourRMethod.evaluate(
            notch_stress_range=150.0,
            stress_ratio=0.0,
            residual_stress=0.0,
            ultimate_strength=500.0,
            yield_strength=355.0,
            num_cycles=1_000_000,
        )
        result_with_res = FourRMethod.evaluate(
            notch_stress_range=150.0,
            stress_ratio=0.0,
            residual_stress=200.0,
            ultimate_strength=500.0,
            yield_strength=355.0,
            num_cycles=1_000_000,
        )
        assert result_with_res.local_stress_ratio > result_no_res.local_stress_ratio

    def test_low_stress_passes(self):
        """Low stress range should pass."""
        result = FourRMethod.evaluate(
            notch_stress_range=50.0,
            stress_ratio=0.0,
            residual_stress=0.0,
            ultimate_strength=500.0,
            yield_strength=355.0,
            num_cycles=100_000,
        )
        assert result.status == "PASS"
        assert result.damage_ratio < 1.0

    def test_high_stress_fails(self):
        """Very high stress range should fail."""
        result = FourRMethod.evaluate(
            notch_stress_range=400.0,
            stress_ratio=0.0,
            residual_stress=300.0,
            ultimate_strength=500.0,
            yield_strength=355.0,
            num_cycles=10_000_000,
        )
        assert result.status == "FAIL"
        assert result.damage_ratio > 1.0

    def test_r_ratio_one_zero_range(self):
        """R=1 means zero effective range, should pass."""
        result = FourRMethod.evaluate(
            notch_stress_range=150.0,
            stress_ratio=1.0,
            residual_stress=0.0,
            ultimate_strength=500.0,
            yield_strength=355.0,
            num_cycles=1_000_000,
        )
        assert result.status == "PASS"
        assert result.damage_ratio == 0.0

    def test_aluminum_master_curve(self):
        """Aluminum should use FAT 71 master curve."""
        result = FourRMethod.evaluate(
            notch_stress_range=100.0,
            stress_ratio=0.0,
            residual_stress=0.0,
            ultimate_strength=300.0,
            yield_strength=200.0,
            num_cycles=500_000,
            material_type="aluminum",
        )
        assert result.master_curve_fat == 71

    def test_higher_rm_increases_sensitivity(self):
        """Higher Rm gives higher M, changing equivalent range."""
        result_low_rm = FourRMethod.evaluate(
            notch_stress_range=150.0,
            stress_ratio=0.3,
            residual_stress=100.0,
            ultimate_strength=400.0,
            yield_strength=300.0,
            num_cycles=500_000,
        )
        result_high_rm = FourRMethod.evaluate(
            notch_stress_range=150.0,
            stress_ratio=0.3,
            residual_stress=100.0,
            ultimate_strength=800.0,
            yield_strength=600.0,
            num_cycles=500_000,
        )
        # Different Rm => different M => different equivalent range
        assert result_low_rm.equivalent_stress_range != result_high_rm.equivalent_stress_range
