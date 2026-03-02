"""Tests for ISO 5817 weld quality assessment."""

import pytest
from weldfatigue.fatigue.weld_quality import WeldQualityAssessment


class TestWeldQualityAssessment:
    """Tests for WeldQualityAssessment class."""

    # --- Axial misalignment ---

    def test_axial_km_zero_eccentricity(self):
        """No misalignment => km = 1.0."""
        km = WeldQualityAssessment.axial_misalignment_km(0.0, 10.0)
        assert km == pytest.approx(1.0)

    def test_axial_km_basic(self):
        """km = 1 + e/t = 1 + 1/10 = 1.1."""
        km = WeldQualityAssessment.axial_misalignment_km(1.0, 10.0)
        assert km == pytest.approx(1.1)

    def test_axial_km_large_eccentricity(self):
        """Large eccentricity gives significant km."""
        km = WeldQualityAssessment.axial_misalignment_km(5.0, 10.0)
        assert km == pytest.approx(1.5)

    def test_axial_km_negative_thickness_raises(self):
        with pytest.raises(ValueError):
            WeldQualityAssessment.axial_misalignment_km(1.0, -5.0)

    # --- Angular misalignment ---

    def test_angular_km_zero(self):
        """No angular misalignment => km = 1.0."""
        km = WeldQualityAssessment.angular_misalignment_km(0.0, 10.0, 100.0)
        assert km == pytest.approx(1.0)

    def test_angular_km_fixed(self):
        """Fixed ends: km = 1 + 1.5*(e/t)."""
        km = WeldQualityAssessment.angular_misalignment_km(1.0, 10.0, 100.0, "fixed")
        assert km == pytest.approx(1.15)

    def test_angular_km_pinned(self):
        """Pinned ends: km = 1 + 3*(e/t)."""
        km = WeldQualityAssessment.angular_misalignment_km(1.0, 10.0, 100.0, "pinned")
        assert km == pytest.approx(1.3)

    # --- Combined km ---

    def test_combined_km(self):
        """Combined = product of individual factors."""
        km = WeldQualityAssessment.combined_km(1.1, 1.15)
        assert km == pytest.approx(1.265)

    # --- Quality level FAT mapping ---

    def test_quality_b_butt(self):
        """Quality B butt weld => FAT 112."""
        assert WeldQualityAssessment.quality_level_fat("B", "butt") == 112

    def test_quality_c_fillet(self):
        """Quality C fillet weld => FAT 71."""
        assert WeldQualityAssessment.quality_level_fat("C", "fillet") == 71

    def test_quality_d_cruciform(self):
        """Quality D cruciform => FAT 50."""
        assert WeldQualityAssessment.quality_level_fat("D", "cruciform") == 50

    def test_quality_ordering(self):
        """B > C > D for same weld type."""
        b = WeldQualityAssessment.quality_level_fat("B", "butt")
        c = WeldQualityAssessment.quality_level_fat("C", "butt")
        d = WeldQualityAssessment.quality_level_fat("D", "butt")
        assert b > c > d

    def test_unknown_quality_raises(self):
        with pytest.raises(ValueError):
            WeldQualityAssessment.quality_level_fat("X", "butt")

    # --- Imperfection checks ---

    def test_undercut_within_limit_b(self):
        """Small undercut within quality B limits."""
        result = WeldQualityAssessment.check_imperfection("undercut", 0.3, "B", 10.0)
        assert result["acceptable"]

    def test_undercut_exceeds_limit_b(self):
        """Undercut exceeding quality B limits."""
        result = WeldQualityAssessment.check_imperfection("undercut", 1.0, "B", 10.0)
        assert not result["acceptable"]

    def test_incomplete_penetration_not_allowed_b(self):
        """Incomplete penetration not permitted in quality B."""
        result = WeldQualityAssessment.check_imperfection(
            "incomplete_penetration", 0.1, "B", 10.0
        )
        assert not result["acceptable"]

    def test_incomplete_penetration_allowed_d(self):
        """Small incomplete penetration allowed in quality D."""
        result = WeldQualityAssessment.check_imperfection(
            "incomplete_penetration", 1.0, "D", 10.0
        )
        assert result["acceptable"]

    # --- Full assessment ---

    def test_assess_quality_no_misalignment(self):
        """Assessment with no misalignment."""
        result = WeldQualityAssessment.assess_quality("butt", "B")
        assert result["km_combined"] == pytest.approx(1.0)
        assert result["fat_class"] == 112

    def test_assess_quality_with_misalignment(self):
        """Assessment with both axial and angular misalignment."""
        result = WeldQualityAssessment.assess_quality(
            "butt", "C", axial_misalignment=1.0, angular_misalignment=0.5,
            thickness=10.0, length=100.0
        )
        assert result["km_combined"] > 1.0
        assert result["fat_class"] == 90
