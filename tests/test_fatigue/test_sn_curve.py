"""Tests for IIW S-N curve implementation."""

import pytest
import math

from weldfatigue.fatigue.sn_curve import SNCurve


class TestSNCurve:
    """IIW S-N curve validation against known values."""

    def test_fat71_at_2e6_cycles(self):
        """FAT 71: stress range at 2e6 cycles must equal 71 MPa."""
        sn = SNCurve(fat_class=71, material_type="steel")
        assert sn.stress_range_at_cycles(2e6) == pytest.approx(71.0, rel=1e-6)

    def test_fat71_cycles_at_fat_stress(self):
        """FAT 71 at 71 MPa must give exactly 2e6 cycles."""
        sn = SNCurve(fat_class=71, material_type="steel")
        assert sn.cycles_to_failure(71.0) == pytest.approx(2e6, rel=1e-6)

    def test_fat80_at_2e6(self):
        """FAT 80 at 2e6 cycles must give 80 MPa."""
        sn = SNCurve(fat_class=80, material_type="steel")
        assert sn.stress_range_at_cycles(2e6) == pytest.approx(80.0, rel=1e-6)

    def test_knee_point_stress(self):
        """Verify knee point stress range for FAT 71 steel."""
        sn = SNCurve(fat_class=71, material_type="steel")
        expected = 71.0 * (2e6 / 1e7) ** (1.0 / 3.0)
        assert sn.delta_sigma_knee == pytest.approx(expected, rel=1e-4)

    def test_below_knee_constant_amplitude(self):
        """Below knee point, constant amplitude = infinite life."""
        sn = SNCurve(fat_class=71, material_type="steel", variable_amplitude=False)
        assert sn.cycles_to_failure(30.0) == float("inf")

    def test_below_knee_variable_amplitude(self):
        """Below knee point with variable amplitude uses m2=5 slope."""
        sn = SNCurve(fat_class=71, material_type="steel", variable_amplitude=True)
        N = sn.cycles_to_failure(35.0)
        assert N > 1e7
        assert N < float("inf")

    def test_below_cutoff_variable_amplitude(self):
        """Below cut-off stress, variable amplitude = infinite life."""
        sn = SNCurve(fat_class=71, material_type="steel", variable_amplitude=True)
        N = sn.cycles_to_failure(1.0)  # Very low stress
        assert N == float("inf")

    @pytest.mark.benchmark
    def test_iiw_example_butt_weld_fat80(self):
        """IIW Example: butt weld FAT 80, stress range 100 MPa."""
        sn = SNCurve(fat_class=80, material_type="steel")
        N = sn.cycles_to_failure(100.0)
        expected = (80 / 100) ** 3 * 2e6  # = 1,024,000
        assert N == pytest.approx(expected, rel=1e-4)

    def test_higher_stress_fewer_cycles(self):
        """Higher stress range must give fewer cycles."""
        sn = SNCurve(fat_class=71, material_type="steel")
        N_100 = sn.cycles_to_failure(100.0)
        N_200 = sn.cycles_to_failure(200.0)
        assert N_200 < N_100

    def test_zero_stress_infinite_life(self):
        sn = SNCurve(fat_class=71, material_type="steel")
        assert sn.cycles_to_failure(0.0) == float("inf")

    def test_get_curve_points(self):
        sn = SNCurve(fat_class=71, material_type="steel")
        N_vals, stress_vals = sn.get_curve_points()
        assert len(N_vals) == 200
        assert len(stress_vals) == 200
        assert N_vals[0] < N_vals[-1]

    def test_aluminum_parameters(self):
        sn = SNCurve(fat_class=45, material_type="aluminum")
        assert sn.m1 == pytest.approx(3.376, rel=1e-3)
        assert sn.stress_range_at_cycles(2e6) == pytest.approx(45.0, rel=1e-6)
