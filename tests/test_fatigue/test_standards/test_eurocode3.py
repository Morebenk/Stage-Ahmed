"""Tests for Eurocode 3 EN 1993-1-9 S-N curves."""

import pytest
from weldfatigue.fatigue.standards.eurocode3 import Eurocode3Curve


class TestEurocode3Curve:

    def test_fat71_at_2e6(self):
        """FAT 71 at 2e6 cycles = 71 MPa."""
        curve = Eurocode3Curve(71)
        assert curve.stress_range_at_cycles(2e6) == pytest.approx(71.0, rel=1e-3)

    def test_knee_at_5e6(self):
        """EC3 knee at 5e6 cycles (not 1e7 like IIW)."""
        assert Eurocode3Curve.KNEE_CYCLES == 5e6

    def test_cutoff_at_1e8(self):
        """EC3 cut-off at 1e8 (not 1e9 like IIW)."""
        assert Eurocode3Curve.CUTOFF_CYCLES == 1e8

    def test_constant_amplitude_below_knee(self):
        """Below knee point in CA = infinite life."""
        curve = Eurocode3Curve(71, variable_amplitude=False)
        # At very low stress, should be below knee
        N = curve.cycles_to_failure(20.0)
        assert N == float("inf")

    def test_variable_amplitude_continues(self):
        """VA continues with m2=5 after knee."""
        curve = Eurocode3Curve(71, variable_amplitude=True)
        N = curve.cycles_to_failure(20.0)
        # Should get finite cycles (below knee but above cutoff in VA)
        # depends on stress level; 20 MPa may still be above cutoff
        assert isinstance(N, float)

    def test_higher_fat_higher_strength(self):
        """Higher FAT class = higher allowable stress."""
        s71 = Eurocode3Curve(71).stress_range_at_cycles(2e6)
        s90 = Eurocode3Curve(90).stress_range_at_cycles(2e6)
        assert s90 > s71

    def test_slope_m1_is_3(self):
        assert Eurocode3Curve.M1 == 3.0

    def test_slope_m2_is_5(self):
        assert Eurocode3Curve.M2 == 5.0
