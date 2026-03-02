"""Tests for partial safety factors."""

import pytest
from weldfatigue.fatigue.safety_factors import PartialSafetyFactors


class TestPartialSafetyFactors:
    """Tests for PartialSafetyFactors class."""

    # --- IIW gamma_Mf tests ---

    def test_iiw_low_periodic(self):
        """IIW: low consequence, periodic inspection => 1.0."""
        assert PartialSafetyFactors.gamma_Mf("low", "periodic", "iiw") == pytest.approx(1.0)

    def test_iiw_normal_periodic(self):
        """IIW: normal consequence, periodic inspection => 1.15."""
        assert PartialSafetyFactors.gamma_Mf("normal", "periodic", "iiw") == pytest.approx(1.15)

    def test_iiw_high_periodic(self):
        """IIW: high consequence, periodic inspection => 1.30."""
        assert PartialSafetyFactors.gamma_Mf("high", "periodic", "iiw") == pytest.approx(1.30)

    def test_iiw_high_none(self):
        """IIW: high consequence, no inspection => 1.40."""
        assert PartialSafetyFactors.gamma_Mf("high", "none", "iiw") == pytest.approx(1.40)

    def test_iiw_normal_continuous(self):
        """IIW: normal consequence, continuous inspection => 1.0."""
        assert PartialSafetyFactors.gamma_Mf("normal", "continuous", "iiw") == pytest.approx(1.0)

    # --- Eurocode 3 tests ---

    def test_ec3_normal(self):
        """Eurocode 3: normal consequence => 1.15."""
        assert PartialSafetyFactors.gamma_Mf("normal", "periodic", "eurocode3") == pytest.approx(1.15)

    def test_ec3_high(self):
        """Eurocode 3: high consequence => 1.35."""
        assert PartialSafetyFactors.gamma_Mf("high", "periodic", "eurocode3") == pytest.approx(1.35)

    # --- DNV DFF tests ---

    def test_dnv_low_periodic(self):
        """DNV: low consequence, periodic => DFF 1.0."""
        assert PartialSafetyFactors.design_fatigue_factor("low", "periodic") == pytest.approx(1.0)

    def test_dnv_high_none(self):
        """DNV: high consequence, no inspection => DFF 10.0."""
        assert PartialSafetyFactors.design_fatigue_factor("high", "none") == pytest.approx(10.0)

    def test_dnv_normal_periodic(self):
        """DNV: normal, periodic => DFF 2.0."""
        assert PartialSafetyFactors.design_fatigue_factor("normal", "periodic") == pytest.approx(2.0)

    # --- Survival probability tests ---

    def test_sp_factor_at_977(self):
        """At 97.7% (IIW characteristic), factor should be ~1.0."""
        sp = PartialSafetyFactors.survival_probability_factor(0.977)
        assert sp == pytest.approx(1.0, abs=0.05)

    def test_sp_factor_at_50_percent(self):
        """At 50% (mean curve), factor = 1.0."""
        sp = PartialSafetyFactors.survival_probability_factor(0.5)
        assert sp == pytest.approx(1.0)

    def test_higher_probability_gives_lower_factor(self):
        """Higher survival probability => lower FAT class factor."""
        sp_977 = PartialSafetyFactors.survival_probability_factor(0.977)
        sp_999 = PartialSafetyFactors.survival_probability_factor(0.999)
        assert sp_999 < sp_977

    # --- Combined application tests ---

    def test_apply_fat_class_low_consequence(self):
        """Low consequence => FAT class barely reduced."""
        reduced = PartialSafetyFactors.apply_to_fat_class(
            80, "low", "periodic", "iiw", 0.977
        )
        assert reduced == pytest.approx(80.0, abs=5.0)

    def test_apply_fat_class_high_consequence(self):
        """High consequence => FAT class significantly reduced."""
        reduced = PartialSafetyFactors.apply_to_fat_class(
            80, "high", "none", "iiw", 0.977
        )
        assert reduced < 80.0
        assert reduced < 80.0 / 1.30  # At least gamma_Mf reduction

    def test_compute_all_returns_all_keys(self):
        """compute_all returns dict with all expected keys."""
        result = PartialSafetyFactors.compute_all("normal", "periodic", "iiw")
        assert "gamma_Mf" in result
        assert "gamma_Ff" in result
        assert "dff" in result
        assert "characteristic_factor" in result
        assert "combined_factor" in result

    def test_gamma_ff_is_one(self):
        """Load partial factor is 1.0 for all current standards."""
        assert PartialSafetyFactors.gamma_Ff("iiw") == pytest.approx(1.0)
        assert PartialSafetyFactors.gamma_Ff("eurocode3") == pytest.approx(1.0)
