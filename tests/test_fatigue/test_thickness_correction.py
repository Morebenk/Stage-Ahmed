"""Tests for IIW thickness correction factors."""

import pytest
from weldfatigue.fatigue.thickness_correction import ThicknessCorrection


class TestThicknessCorrection:
    """Tests for ThicknessCorrection class."""

    def test_reference_thickness_gives_factor_one(self):
        """At reference thickness (25mm), correction factor = 1.0."""
        f = ThicknessCorrection.correction_factor(25.0, "butt", "tension")
        assert f == pytest.approx(1.0)

    def test_below_reference_gives_factor_one(self):
        """Below reference thickness, correction factor = 1.0 (no benefit)."""
        f = ThicknessCorrection.correction_factor(10.0, "butt", "tension")
        assert f == pytest.approx(1.0)

    def test_thick_butt_tension_reduces_fat(self):
        """Butt weld in tension at 50mm: f = (25/50)^0.2."""
        f = ThicknessCorrection.correction_factor(50.0, "butt", "tension")
        expected = (25.0 / 50.0) ** 0.2
        assert f == pytest.approx(expected, rel=1e-6)

    def test_cruciform_has_higher_exponent(self):
        """Cruciform joints use n=0.3 (more severe correction)."""
        f_cruciform = ThicknessCorrection.correction_factor(50.0, "cruciform", "tension")
        f_butt = ThicknessCorrection.correction_factor(50.0, "butt", "tension")
        assert f_cruciform < f_butt  # More reduction for cruciform

    def test_fillet_shear_no_correction(self):
        """Fillet welds in shear have n=0 (no thickness correction)."""
        f = ThicknessCorrection.correction_factor(100.0, "fillet", "shear")
        assert f == pytest.approx(1.0)

    def test_iiw_example_butt_50mm_fat80(self):
        """IIW benchmark: butt weld, t=50mm, FAT 80."""
        corrected = ThicknessCorrection.corrected_fat_class(80, 50.0, "butt", "tension")
        expected = 80 * (25.0 / 50.0) ** 0.2
        assert corrected == pytest.approx(expected, rel=1e-6)
        assert corrected < 80  # Must be reduced

    def test_corrected_fat_at_reference_unchanged(self):
        """FAT class at reference thickness should be unchanged."""
        corrected = ThicknessCorrection.corrected_fat_class(71, 25.0, "fillet", "tension")
        assert corrected == pytest.approx(71.0)

    def test_thin_sheet_reference_radius_below_5mm(self):
        """Thin sheets (t < 5mm) use r_ref = 0.05mm."""
        r = ThicknessCorrection.thin_sheet_reference_radius(3.0)
        assert r == pytest.approx(0.05)

    def test_standard_reference_radius_above_5mm(self):
        """Standard plates (t >= 5mm) use r_ref = 1.0mm."""
        r = ThicknessCorrection.thin_sheet_reference_radius(10.0)
        assert r == pytest.approx(1.0)

    def test_effective_thickness_no_attachment(self):
        """Without attachment, effective thickness = nominal."""
        t = ThicknessCorrection.effective_thickness(30.0)
        assert t == pytest.approx(30.0)

    def test_effective_thickness_with_attachment(self):
        """With attachment, t_eff = min(t, 0.5*L)."""
        t = ThicknessCorrection.effective_thickness(30.0, attachment_length=40.0)
        assert t == pytest.approx(20.0)  # min(30, 0.5*40=20)

    def test_effective_thickness_short_attachment(self):
        """Short attachment doesn't reduce thickness below nominal."""
        t = ThicknessCorrection.effective_thickness(10.0, attachment_length=100.0)
        assert t == pytest.approx(10.0)

    def test_negative_thickness_raises(self):
        """Negative thickness must raise ValueError."""
        with pytest.raises(ValueError):
            ThicknessCorrection.correction_factor(-5.0, "butt", "tension")

    def test_unknown_weld_type_uses_default_exponent(self):
        """Unknown weld/load combo falls back to n=0.2."""
        f = ThicknessCorrection.correction_factor(50.0, "unknown", "unknown")
        expected = (25.0 / 50.0) ** 0.2
        assert f == pytest.approx(expected, rel=1e-6)

    def test_very_thick_plate(self):
        """Very thick plate (200mm) should have significant correction."""
        f = ThicknessCorrection.correction_factor(200.0, "cruciform", "tension")
        expected = (25.0 / 200.0) ** 0.3
        assert f == pytest.approx(expected, rel=1e-6)
        assert f < 0.7  # Significant reduction
