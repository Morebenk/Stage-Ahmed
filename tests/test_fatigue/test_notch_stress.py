"""Tests for the Effective Notch Stress Method."""

import pytest

from weldfatigue.fatigue.notch_stress import EffectiveNotchStressAssessment


class TestEffectiveNotchStress:

    def test_steel_fat_class(self):
        """Steel uses FAT 225."""
        assessor = EffectiveNotchStressAssessment(material="steel")
        assert assessor.fat_class == 225

    def test_aluminum_fat_class(self):
        """Aluminum uses FAT 71."""
        assessor = EffectiveNotchStressAssessment(material="aluminum")
        assert assessor.fat_class == 71

    def test_standard_radius(self):
        """For t >= 5mm, reference radius = 1.0 mm."""
        assessor = EffectiveNotchStressAssessment(plate_thickness=10.0)
        assert assessor.reference_radius == 1.0

    def test_thin_sheet_radius(self):
        """For t < 5mm, reference radius = 0.05 mm."""
        assessor = EffectiveNotchStressAssessment(plate_thickness=3.0)
        assert assessor.reference_radius == 0.05

    def test_evaluate_pass(self):
        assessor = EffectiveNotchStressAssessment(material="steel")
        result = assessor.evaluate(notch_stress_range=200.0, num_cycles=1_000_000)
        assert result.status == "PASS"
        assert result.method == "notch"

    def test_evaluate_fail(self):
        assessor = EffectiveNotchStressAssessment(material="steel")
        result = assessor.evaluate(notch_stress_range=300.0, num_cycles=5_000_000)
        assert result.status == "FAIL"

    def test_fat225_at_2e6(self):
        """FAT 225 at 225 MPa, 2e6 cycles: damage ratio = 1.0."""
        assessor = EffectiveNotchStressAssessment(material="steel")
        result = assessor.evaluate(225.0, 2_000_000)
        assert result.damage_ratio == pytest.approx(1.0, rel=1e-4)

    def test_safety_factor_high_stress(self):
        assessor = EffectiveNotchStressAssessment(material="steel")
        result = assessor.evaluate(250.0, 2_000_000)
        assert result.safety_factor < 1.0  # Overstressed

    def test_safety_factor_low_stress(self):
        assessor = EffectiveNotchStressAssessment(material="steel")
        result = assessor.evaluate(100.0, 500_000)
        assert result.safety_factor > 1.0

    def test_aluminum_evaluation(self):
        assessor = EffectiveNotchStressAssessment(material="aluminum", plate_thickness=8.0)
        result = assessor.evaluate(50.0, 1_000_000)
        assert result.status == "PASS"
        assert result.fat_class == 71
