"""Tests for weld root fatigue assessment."""

import pytest
from weldfatigue.core.schemas import FatigueResult
from weldfatigue.fatigue.root_fatigue import RootFatigueAssessment


class TestRootFatigueAssessment:
    """Tests for RootFatigueAssessment class."""

    # --- Root stress concentration ---

    def test_full_penetration_scf_one(self):
        """Full penetration: SCF ≈ 1.0 (no root notch)."""
        scf = RootFatigueAssessment.root_stress_concentration(
            weld_throat=5.0, penetration_depth=10.0, plate_thickness=10.0
        )
        assert scf == pytest.approx(1.0)

    def test_partial_penetration_higher_scf(self):
        """Partial penetration increases SCF."""
        scf = RootFatigueAssessment.root_stress_concentration(
            weld_throat=5.0, penetration_depth=5.0, plate_thickness=10.0
        )
        assert scf > 1.0

    def test_deeper_penetration_lower_scf(self):
        """More penetration => lower SCF."""
        scf_low = RootFatigueAssessment.root_stress_concentration(
            5.0, 3.0, 10.0
        )
        scf_high = RootFatigueAssessment.root_stress_concentration(
            5.0, 7.0, 10.0
        )
        assert scf_high < scf_low

    def test_bending_lower_scf(self):
        """Bending gives lower root SCF than tension."""
        scf_tension = RootFatigueAssessment.root_stress_concentration(
            5.0, 5.0, 10.0, "tension"
        )
        scf_bending = RootFatigueAssessment.root_stress_concentration(
            5.0, 5.0, 10.0, "bending"
        )
        assert scf_bending < scf_tension

    def test_invalid_thickness_raises(self):
        with pytest.raises(ValueError):
            RootFatigueAssessment.root_stress_concentration(5.0, 5.0, 0.0)

    # --- Root notch stress ---

    def test_root_notch_stress_positive(self):
        """Root notch stress should be positive for positive nominal."""
        stress = RootFatigueAssessment.root_notch_stress(
            100.0, 5.0, 10.0, 5.0
        )
        assert stress > 0

    def test_root_notch_stress_increases_with_nominal(self):
        """Higher nominal stress => higher root stress."""
        s1 = RootFatigueAssessment.root_notch_stress(50.0, 5.0, 10.0, 5.0)
        s2 = RootFatigueAssessment.root_notch_stress(100.0, 5.0, 10.0, 5.0)
        assert s2 > s1

    # --- Root fatigue evaluation ---

    def test_evaluate_pass(self):
        """Low stress should pass."""
        assessor = RootFatigueAssessment(material="steel")
        result = assessor.evaluate(50.0, 1_000_000)
        assert result.status == "PASS"

    def test_evaluate_fail(self):
        """High stress should fail."""
        assessor = RootFatigueAssessment(material="steel")
        result = assessor.evaluate(300.0, 10_000_000)
        assert result.status == "FAIL"

    def test_evaluate_returns_fatigue_result(self):
        """Should return FatigueResult schema."""
        assessor = RootFatigueAssessment(material="steel")
        result = assessor.evaluate(100.0, 1_000_000)
        assert isinstance(result, FatigueResult)
        assert result.method == "root"

    def test_steel_fat_class(self):
        """Steel root FAT class = 200."""
        assessor = RootFatigueAssessment(material="steel")
        assert assessor.fat_class == 200

    def test_aluminum_fat_class(self):
        """Aluminum root FAT class = 71."""
        assessor = RootFatigueAssessment(material="aluminum")
        assert assessor.fat_class == 71

    # --- Toe vs root comparison ---

    def test_toe_vs_root_identifies_critical(self):
        """Should identify the weaker location as critical."""
        toe = FatigueResult(
            method="notch", fat_class=225, allowable_cycles=1e6,
            applied_cycles=1000, damage_ratio=0.001, utilization=0.1,
            status="PASS", safety_factor=1000,
        )
        root = FatigueResult(
            method="root", fat_class=200, allowable_cycles=5e5,
            applied_cycles=1000, damage_ratio=0.002, utilization=0.2,
            status="PASS", safety_factor=500,
        )
        comparison = RootFatigueAssessment.toe_vs_root_comparison(toe, root)
        assert comparison["critical_location"] == "root"

    def test_toe_vs_root_equal(self):
        """When toe life <= root life, toe is critical."""
        toe = FatigueResult(
            method="notch", fat_class=225, allowable_cycles=1e6,
            applied_cycles=1000, damage_ratio=0.001, utilization=0.1,
            status="PASS", safety_factor=1000,
        )
        root = FatigueResult(
            method="root", fat_class=200, allowable_cycles=2e6,
            applied_cycles=1000, damage_ratio=0.0005, utilization=0.05,
            status="PASS", safety_factor=2000,
        )
        comparison = RootFatigueAssessment.toe_vs_root_comparison(toe, root)
        assert comparison["critical_location"] == "toe"
