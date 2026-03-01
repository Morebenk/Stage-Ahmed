"""Tests for the Nominal Stress Method."""

import pytest

from weldfatigue.fatigue.nominal_stress import NominalStressAssessment


class TestNominalStress:

    def test_pass_case(self):
        """Low stress range should pass."""
        assessor = NominalStressAssessment(fat_class=71, material="steel")
        result = assessor.evaluate(stress_range=50.0, num_cycles=1_000_000)
        assert result.status == "PASS"
        assert result.damage_ratio < 1.0

    def test_fail_case(self):
        """High stress range with many cycles should fail."""
        assessor = NominalStressAssessment(fat_class=71, material="steel")
        result = assessor.evaluate(stress_range=100.0, num_cycles=5_000_000)
        assert result.status == "FAIL"
        assert result.damage_ratio > 1.0

    def test_fat80_at_80mpa_2e6(self):
        """FAT 80, 80 MPa, 2e6 cycles: damage ratio should be ~1.0."""
        assessor = NominalStressAssessment(fat_class=80, material="steel")
        result = assessor.evaluate(stress_range=80.0, num_cycles=2_000_000)
        assert result.damage_ratio == pytest.approx(1.0, rel=1e-4)

    def test_goodman_correction_increases_damage(self):
        """Positive mean stress with Goodman should increase effective stress."""
        assessor = NominalStressAssessment(fat_class=71, material="steel")
        r_no_corr = assessor.evaluate(60.0, 2_000_000)
        r_goodman = assessor.evaluate(
            60.0, 2_000_000,
            mean_stress_correction="goodman",
            mean_stress=100.0,
            ultimate_strength=600.0,
        )
        assert r_goodman.damage_ratio >= r_no_corr.damage_ratio

    def test_spectrum_evaluation(self):
        """Variable amplitude with Miner rule."""
        assessor = NominalStressAssessment(
            fat_class=71, material="steel", variable_amplitude=True
        )
        spectrum = [(100.0, 500_000), (80.0, 1_000_000), (50.0, 5_000_000)]
        result = assessor.evaluate_spectrum(spectrum)
        assert result.total_damage > 0
        assert len(result.damage_per_block) == 3

    def test_method_name(self):
        assessor = NominalStressAssessment(fat_class=71)
        result = assessor.evaluate(50.0, 1_000_000)
        assert result.method == "nominal"

    def test_safety_factor(self):
        assessor = NominalStressAssessment(fat_class=80)
        result = assessor.evaluate(stress_range=50.0, num_cycles=1_000_000)
        assert result.safety_factor > 1.0
