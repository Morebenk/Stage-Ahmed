"""Tests for post-weld treatment improvement factors."""

import pytest
from weldfatigue.fatigue.post_weld_treatment import PostWeldTreatmentFactors


class TestPostWeldTreatment:
    """Tests for PostWeldTreatmentFactors class."""

    # --- HFMI tests ---

    def test_hfmi_fat71_fy450(self):
        """HFMI: FAT 71, fy=450 MPa => 6 steps up => FAT 140."""
        upgraded = PostWeldTreatmentFactors.hfmi_upgraded_fat(71, 450.0)
        # 71(idx6) +6 steps = idx12 => 140
        assert upgraded == 140

    def test_hfmi_fat71_fy300(self):
        """HFMI: FAT 71, fy=300 MPa => 4 steps up => FAT 112."""
        upgraded = PostWeldTreatmentFactors.hfmi_upgraded_fat(71, 300.0)
        # 71(idx6) +4 steps = idx10 => 112
        assert upgraded == 112

    def test_hfmi_fat71_fy600(self):
        """HFMI: FAT 71, fy=600 MPa (high strength) => 8 steps up, capped at 160."""
        upgraded = PostWeldTreatmentFactors.hfmi_upgraded_fat(71, 600.0)
        assert upgraded == 160  # 8 steps from 71 exceeds sequence

    def test_hfmi_already_at_max(self):
        """HFMI on FAT 160 stays at 160 (cap)."""
        upgraded = PostWeldTreatmentFactors.hfmi_upgraded_fat(160, 500.0)
        assert upgraded == 160

    # --- TIG dressing tests ---

    def test_tig_dressing_fat71(self):
        """TIG dressing: FAT 71 => +2 steps => FAT 90."""
        assert PostWeldTreatmentFactors.tig_dressing_upgraded_fat(71) == 90

    def test_tig_dressing_fat80(self):
        """TIG dressing: FAT 80 => +2 steps => FAT 100."""
        assert PostWeldTreatmentFactors.tig_dressing_upgraded_fat(80) == 100

    # --- Burr grinding tests ---

    def test_burr_grinding_fat71(self):
        """Burr grinding: FAT 71 => +1 step => FAT 80."""
        assert PostWeldTreatmentFactors.burr_grinding_upgraded_fat(71) == 80

    def test_burr_grinding_fat56(self):
        """Burr grinding: FAT 56 => +1 step => FAT 63."""
        assert PostWeldTreatmentFactors.burr_grinding_upgraded_fat(56) == 63

    # --- Shot peening tests ---

    def test_shot_peening_fat71(self):
        """Shot peening: FAT 71 => +2 steps => FAT 90."""
        assert PostWeldTreatmentFactors.shot_peening_upgraded_fat(71) == 90

    # --- Hammer peening tests ---

    def test_hammer_peening_fat71_fy300(self):
        """Hammer peening: FAT 71, fy=300 => +2 steps => FAT 90."""
        assert PostWeldTreatmentFactors.hammer_peening_upgraded_fat(71, 300.0) == 90

    def test_hammer_peening_fat71_fy500(self):
        """Hammer peening: FAT 71, fy=500 => +3 steps => FAT 100."""
        assert PostWeldTreatmentFactors.hammer_peening_upgraded_fat(71, 500.0) == 100

    # --- apply_treatment dispatch ---

    def test_no_treatment(self):
        """No treatment returns original FAT class."""
        assert PostWeldTreatmentFactors.apply_treatment(71, "none") == 71

    def test_apply_treatment_hfmi(self):
        """apply_treatment dispatches to HFMI correctly."""
        result = PostWeldTreatmentFactors.apply_treatment(71, "hfmi", 450.0)
        assert result > 71

    def test_unknown_treatment_raises(self):
        """Unknown treatment raises ValueError."""
        with pytest.raises(ValueError):
            PostWeldTreatmentFactors.apply_treatment(71, "unknown_method")

    # --- Summary ---

    def test_improvement_summary_all_better(self):
        """All treatments should give FAT >= base FAT."""
        summary = PostWeldTreatmentFactors.improvement_summary(71, 400.0)
        for treatment, fat in summary.items():
            assert fat >= 71, f"{treatment} gave FAT {fat} < 71"

    def test_improvement_summary_ordering(self):
        """HFMI should give highest improvement."""
        summary = PostWeldTreatmentFactors.improvement_summary(71, 500.0)
        assert summary["hfmi"] >= summary["tig_dressing"]
        assert summary["tig_dressing"] >= summary["burr_grinding"]

    def test_fat_sequence_is_sorted(self):
        """FAT_SEQUENCE must be strictly increasing."""
        seq = PostWeldTreatmentFactors.FAT_SEQUENCE
        for i in range(len(seq) - 1):
            assert seq[i] < seq[i + 1]
