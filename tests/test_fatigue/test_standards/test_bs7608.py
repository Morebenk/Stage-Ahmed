"""Tests for BS 7608 S-N curves."""

import pytest
from weldfatigue.fatigue.standards.bs7608 import BS7608Curve


class TestBS7608Curve:

    def test_class_d_at_2e6(self):
        """Class D at 2e6 cycles = 53 MPa."""
        curve = BS7608Curve("D")
        assert curve.stress_range_at_cycles(2e6) == pytest.approx(53.0, rel=1e-3)

    def test_class_d_cycles_at_ref(self):
        """Class D at 53 MPa = 2e6 cycles."""
        curve = BS7608Curve("D")
        N = curve.cycles_to_failure(53.0)
        assert N == pytest.approx(2e6, rel=1e-3)

    def test_class_b_slope_4(self):
        """Class B has slope m=4."""
        curve = BS7608Curve("B")
        assert curve.m == pytest.approx(4.0)

    def test_class_f_slope_3(self):
        """Class F has slope m=3."""
        curve = BS7608Curve("F")
        assert curve.m == pytest.approx(3.0)

    def test_higher_class_higher_strength(self):
        """Class B > Class D > Class G at same cycles."""
        b = BS7608Curve("B").stress_range_at_cycles(2e6)
        d = BS7608Curve("D").stress_range_at_cycles(2e6)
        g = BS7608Curve("G").stress_range_at_cycles(2e6)
        assert b > d > g

    def test_constant_amplitude_cutoff(self):
        """Constant amplitude: infinite life beyond cut-off."""
        curve = BS7608Curve("D", variable_amplitude=False)
        assert curve.cycles_to_failure(10.0) == float("inf")

    def test_unknown_class_raises(self):
        with pytest.raises(ValueError):
            BS7608Curve("X")

    def test_zero_stress(self):
        curve = BS7608Curve("D")
        assert curve.cycles_to_failure(0.0) == float("inf")
