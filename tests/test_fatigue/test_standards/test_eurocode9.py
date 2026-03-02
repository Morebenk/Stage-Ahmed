"""Tests for Eurocode 9 EN 1999-1-3 aluminum S-N curves."""

import pytest
from weldfatigue.fatigue.standards.eurocode9 import Eurocode9Curve


class TestEurocode9Curve:

    def test_fat45_at_2e6(self):
        """FAT 45 at 2e6 cycles = 45 MPa."""
        curve = Eurocode9Curve(45)
        assert curve.stress_range_at_cycles(2e6) == pytest.approx(45.0, rel=1e-3)

    def test_knee_at_5e6(self):
        assert Eurocode9Curve.KNEE_CYCLES == 5e6

    def test_default_slope(self):
        curve = Eurocode9Curve(45)
        assert curve.m1 == pytest.approx(3.4)

    def test_high_detail_slope(self):
        """Some detail categories use m1=4.3."""
        curve = Eurocode9Curve(28)
        assert curve.m1 == pytest.approx(4.3)

    def test_constant_amplitude_infinite_below_knee(self):
        curve = Eurocode9Curve(45, variable_amplitude=False)
        N = curve.cycles_to_failure(10.0)
        assert N == float("inf")

    def test_zero_stress(self):
        curve = Eurocode9Curve(45)
        assert curve.cycles_to_failure(0.0) == float("inf")

    def test_higher_fat_higher_life(self):
        N_45 = Eurocode9Curve(45).cycles_to_failure(40.0)
        N_56 = Eurocode9Curve(56).cycles_to_failure(40.0)
        assert N_56 > N_45
