"""Tests for mean stress correction methods."""

import pytest

from weldfatigue.fatigue.mean_stress import MeanStressCorrection


class TestGoodman:

    def test_zero_mean_no_change(self):
        result = MeanStressCorrection.goodman(100.0, 0.0, 600.0)
        assert result == 100.0

    def test_positive_mean_increases(self):
        result = MeanStressCorrection.goodman(100.0, 200.0, 600.0)
        assert result > 100.0

    def test_at_uts_returns_inf(self):
        result = MeanStressCorrection.goodman(100.0, 600.0, 600.0)
        assert result == float("inf")

    def test_known_value(self):
        # Sa_eq = 100 / (1 - 200/600) = 100 / 0.6667 = 150
        result = MeanStressCorrection.goodman(100.0, 200.0, 600.0)
        assert result == pytest.approx(150.0, rel=1e-3)


class TestGerber:

    def test_zero_mean_no_change(self):
        result = MeanStressCorrection.gerber(100.0, 0.0, 600.0)
        assert result == pytest.approx(100.0, rel=1e-6)

    def test_positive_mean_increases(self):
        result = MeanStressCorrection.gerber(100.0, 200.0, 600.0)
        assert result > 100.0

    def test_gerber_less_than_goodman(self):
        """Gerber is less conservative than Goodman."""
        g = MeanStressCorrection.goodman(100.0, 200.0, 600.0)
        ge = MeanStressCorrection.gerber(100.0, 200.0, 600.0)
        assert ge < g


class TestSoderberg:

    def test_zero_mean(self):
        result = MeanStressCorrection.soderberg(100.0, 0.0, 350.0)
        assert result == 100.0

    def test_more_conservative_than_goodman(self):
        """Soderberg uses yield, so more conservative."""
        s = MeanStressCorrection.soderberg(100.0, 200.0, 350.0)
        g = MeanStressCorrection.goodman(100.0, 200.0, 600.0)
        assert s > g  # Higher equivalent amplitude = more conservative


class TestIIWEnhancementFactor:

    def test_as_welded_always_one(self):
        """As-welded joints: f(R) = 1.0 for all R."""
        for R in [-2, -1, 0, 0.5, 1]:
            assert MeanStressCorrection.iiw_enhancement_factor(R, stress_relieved=False) == 1.0

    def test_stress_relieved_R_minus2(self):
        f = MeanStressCorrection.iiw_enhancement_factor(-2.0, stress_relieved=True)
        assert f == 1.6

    def test_stress_relieved_R_zero(self):
        f = MeanStressCorrection.iiw_enhancement_factor(0.0, stress_relieved=True)
        assert f == pytest.approx(1.2, rel=1e-6)

    def test_stress_relieved_R_05(self):
        f = MeanStressCorrection.iiw_enhancement_factor(0.5, stress_relieved=True)
        assert f == pytest.approx(1.0, rel=1e-6)

    def test_stress_relieved_R_1(self):
        f = MeanStressCorrection.iiw_enhancement_factor(1.0, stress_relieved=True)
        assert f == 1.0


class TestStressRatio:

    def test_r_zero(self):
        R = MeanStressCorrection.stress_ratio_from_range_and_mean(200.0, 100.0)
        # sigma_max=200, sigma_min=0, R=0
        assert R == pytest.approx(0.0, abs=1e-6)

    def test_r_minus_one(self):
        R = MeanStressCorrection.stress_ratio_from_range_and_mean(200.0, 0.0)
        # sigma_max=100, sigma_min=-100, R=-1
        assert R == pytest.approx(-1.0, abs=1e-6)
