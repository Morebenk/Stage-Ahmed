"""Tests for environmental and corrosion factors."""

import pytest
from weldfatigue.fatigue.environmental import EnvironmentalFactors


class TestEnvironmentalFactors:
    """Tests for EnvironmentalFactors class."""

    # --- Corrosion factor tests ---

    def test_air_gives_factor_one(self):
        assert EnvironmentalFactors.corrosion_factor("air", "steel") == pytest.approx(1.0)

    def test_seawater_free_steel(self):
        assert EnvironmentalFactors.corrosion_factor("seawater_free", "steel") == pytest.approx(0.7)

    def test_seawater_cp_steel(self):
        assert EnvironmentalFactors.corrosion_factor("seawater_cp", "steel") == pytest.approx(0.85)

    def test_hydrogen_steel(self):
        assert EnvironmentalFactors.corrosion_factor("hydrogen", "steel") == pytest.approx(0.5)

    def test_industrial_aluminum(self):
        assert EnvironmentalFactors.corrosion_factor("industrial", "aluminum") == pytest.approx(0.85)

    def test_unknown_environment_gives_one(self):
        assert EnvironmentalFactors.corrosion_factor("unknown", "steel") == pytest.approx(1.0)

    # --- Endurance limit removal ---

    def test_air_keeps_endurance_limit(self):
        assert not EnvironmentalFactors.removes_endurance_limit("air")

    def test_seawater_removes_endurance_limit(self):
        assert EnvironmentalFactors.removes_endurance_limit("seawater_free")

    def test_seawater_cp_removes_endurance_limit(self):
        assert EnvironmentalFactors.removes_endurance_limit("seawater_cp")

    # --- Temperature factor tests ---

    def test_steel_room_temperature(self):
        assert EnvironmentalFactors.temperature_factor(20.0, "steel") == pytest.approx(1.0)

    def test_steel_100c_boundary(self):
        assert EnvironmentalFactors.temperature_factor(100.0, "steel") == pytest.approx(1.0)

    def test_steel_200c(self):
        expected = 1.0 - 1.5e-3 * 100.0  # = 0.85
        assert EnvironmentalFactors.temperature_factor(200.0, "steel") == pytest.approx(expected)

    def test_steel_300c(self):
        expected = 1.0 - 1.5e-3 * 200.0  # = 0.70
        assert EnvironmentalFactors.temperature_factor(300.0, "steel") == pytest.approx(expected)

    def test_aluminum_50c_boundary(self):
        assert EnvironmentalFactors.temperature_factor(50.0, "aluminum") == pytest.approx(1.0)

    def test_aluminum_100c(self):
        expected = 1.0 - 3.0e-3 * 50.0  # = 0.85
        assert EnvironmentalFactors.temperature_factor(100.0, "aluminum") == pytest.approx(expected)

    # --- Hydrogen knockdown tests ---

    def test_h2_zero_pressure(self):
        assert EnvironmentalFactors.hydrogen_knockdown(0.0, "steel") == pytest.approx(1.0)

    def test_h2_700_bar(self):
        """700 bar H2 tank: significant knockdown."""
        f = EnvironmentalFactors.hydrogen_knockdown(700.0, "steel")
        expected = 1.0 / (1.0 + 0.002 * 700.0)  # ~0.417
        assert f == pytest.approx(expected, rel=1e-3)
        assert f < 0.5

    def test_h2_aluminum_unaffected(self):
        assert EnvironmentalFactors.hydrogen_knockdown(700.0, "aluminum") == pytest.approx(1.0)

    # --- Cryogenic tests ---

    def test_cryo_normal_temperature(self):
        assert EnvironmentalFactors.cryogenic_factor(20.0, "steel") == pytest.approx(1.0)

    def test_cryo_very_cold_steel(self):
        assert EnvironmentalFactors.cryogenic_factor(-60.0, "steel") == pytest.approx(0.8)

    def test_cryo_aluminum_unaffected(self):
        assert EnvironmentalFactors.cryogenic_factor(-196.0, "aluminum") == pytest.approx(1.0)

    # --- Combined factor tests ---

    def test_combined_air_room_temp(self):
        f = EnvironmentalFactors.combined_environmental_factor("air", 20.0, 0.0, "steel")
        assert f == pytest.approx(1.0)

    def test_combined_seawater_elevated(self):
        f = EnvironmentalFactors.combined_environmental_factor(
            "seawater_free", 200.0, 0.0, "steel"
        )
        assert f < 0.7  # Worse than corrosion alone

    def test_corrected_fat_class_air(self):
        corrected = EnvironmentalFactors.corrected_fat_class(80, "air")
        assert corrected == pytest.approx(80.0)

    def test_corrected_fat_class_hydrogen(self):
        corrected = EnvironmentalFactors.corrected_fat_class(80, "hydrogen", 20.0, 350.0, "steel")
        assert corrected < 80.0
