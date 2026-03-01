"""Tests for log-log interpolation utilities."""

import pytest
import math

from weldfatigue.utils.interpolation import log_log_interpolate, log_log_slope


class TestLogLogInterpolate:

    def test_midpoint(self):
        """Interpolate at the geometric midpoint."""
        x_mid = math.sqrt(100 * 10000)  # = 1000
        result = log_log_interpolate(x_mid, 100, 500, 10000, 50)
        # In log-log space, midpoint should give geometric mean of y values
        expected = math.sqrt(500 * 50)  # = 158.11
        assert result == pytest.approx(expected, rel=1e-3)

    def test_at_endpoints(self):
        """Interpolation at x1 should give y1."""
        result = log_log_interpolate(100.0, 100.0, 200.0, 1000.0, 20.0)
        assert result == pytest.approx(200.0, rel=1e-6)

    def test_at_x2(self):
        """Interpolation at x2 should give y2."""
        result = log_log_interpolate(1000.0, 100.0, 200.0, 1000.0, 20.0)
        assert result == pytest.approx(20.0, rel=1e-6)

    def test_negative_raises(self):
        with pytest.raises(ValueError):
            log_log_interpolate(-1, 10, 100, 1000, 10)

    def test_zero_raises(self):
        with pytest.raises(ValueError):
            log_log_interpolate(0, 10, 100, 1000, 10)


class TestLogLogSlope:

    def test_known_slope(self):
        """S-N curve slope m=3: if N increases by 10x, stress decreases by 10^(1/3)."""
        # Points on N = (FAT/ds)^3 * 2e6 with FAT=80
        N1 = 2e6
        ds1 = 80.0
        N2 = 2e6 * (80 / 40) ** 3  # = 16e6
        ds2 = 40.0
        slope = log_log_slope(N1, ds1, N2, ds2)
        # Slope in log-log should be -1/3 (stress decreases as cycles increase)
        assert slope == pytest.approx(-1.0 / 3.0, rel=1e-3)
