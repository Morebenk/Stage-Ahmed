"""Tests for weld process-specific fatigue assessment."""

import math
import pytest
from weldfatigue.fatigue.weld_processes import WeldProcessFatigue


class TestWeldProcessFatigue:
    """Tests for WeldProcessFatigue class."""

    # --- Laser weld FAT classes ---

    def test_laser_butt_steel(self):
        assert WeldProcessFatigue.laser_weld_fat_class("butt", "steel") == 100

    def test_laser_butt_aluminum(self):
        assert WeldProcessFatigue.laser_weld_fat_class("butt", "aluminum") == 50

    def test_laser_fillet_steel(self):
        assert WeldProcessFatigue.laser_weld_fat_class("fillet", "steel") == 90

    def test_laser_unknown_defaults(self):
        fat = WeldProcessFatigue.laser_weld_fat_class("unknown", "steel")
        assert fat == 80  # Default

    # --- FSW FAT classes ---

    def test_fsw_butt_steel(self):
        assert WeldProcessFatigue.fsw_fat_class("butt", "steel") == 112

    def test_fsw_butt_aluminum(self):
        assert WeldProcessFatigue.fsw_fat_class("butt", "aluminum") == 56

    # --- Spot weld fatigue life ---

    def test_spot_weld_zero_force(self):
        N = WeldProcessFatigue.spot_weld_fatigue_life(0, 1.5, 6.0, "steel")
        assert N == float("inf")

    def test_spot_weld_life_decreases_with_force(self):
        N_low = WeldProcessFatigue.spot_weld_fatigue_life(1000, 1.5, 6.0, "steel")
        N_high = WeldProcessFatigue.spot_weld_fatigue_life(2000, 1.5, 6.0, "steel")
        assert N_high < N_low

    def test_spot_weld_unknown_material_raises(self):
        with pytest.raises(ValueError):
            WeldProcessFatigue.spot_weld_fatigue_life(1000, 1.5, 6.0, "titanium")

    def test_spot_weld_positive_life(self):
        N = WeldProcessFatigue.spot_weld_fatigue_life(1500, 1.2, 5.0, "steel")
        assert N > 0

    # --- Spot weld structural stress ---

    def test_structural_stress_force_only(self):
        sigma = WeldProcessFatigue.spot_weld_structural_stress(1000, 0, 1.5, 6.0)
        expected = 1000 / (math.pi * 6.0 * 1.5)
        assert sigma == pytest.approx(expected, rel=1e-6)

    def test_structural_stress_force_and_moment(self):
        sigma = WeldProcessFatigue.spot_weld_structural_stress(1000, 500, 1.5, 6.0)
        sigma_f = 1000 / (math.pi * 6.0 * 1.5)
        sigma_m = 6.0 * 500 / (math.pi * 6.0 * 1.5 ** 2)
        assert sigma == pytest.approx(sigma_f + sigma_m, rel=1e-6)

    # --- Process modification factors ---

    def test_mig_mag_factor_one(self):
        assert WeldProcessFatigue.process_modification_factor("mig_mag") == pytest.approx(1.0)

    def test_laser_factor_higher(self):
        assert WeldProcessFatigue.process_modification_factor("laser") > 1.0

    def test_fsw_factor_highest(self):
        f_fsw = WeldProcessFatigue.process_modification_factor("friction_stir")
        f_laser = WeldProcessFatigue.process_modification_factor("laser")
        assert f_fsw > f_laser

    def test_corrected_fat_laser(self):
        corrected = WeldProcessFatigue.corrected_fat_for_process(71, "laser")
        assert corrected == pytest.approx(71 * 1.2)

    # --- Minimum nugget diameter ---

    def test_min_nugget_diameter(self):
        d = WeldProcessFatigue.minimum_nugget_diameter(1.5)
        assert d == pytest.approx(4.0 * math.sqrt(1.5), rel=1e-6)

    def test_min_nugget_negative_thickness_raises(self):
        with pytest.raises(ValueError):
            WeldProcessFatigue.minimum_nugget_diameter(-1.0)
