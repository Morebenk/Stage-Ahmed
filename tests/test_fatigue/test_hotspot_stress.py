"""Tests for the Hot-Spot Stress Method."""

import pytest
import numpy as np

from weldfatigue.fatigue.hotspot_stress import HotSpotStressAssessment


class TestHotSpotExtrapolation:

    def test_type_a_linear(self):
        """Type a linear: sigma_hs = 1.67*s(0.4t) - 0.67*s(1.0t)."""
        hs = HotSpotStressAssessment.extrapolate_type_a(150.0, 120.0)
        expected = 1.67 * 150.0 - 0.67 * 120.0
        assert hs == pytest.approx(expected, rel=1e-6)

    def test_type_a_linear_uniform_stress(self):
        """If stress is uniform along path, hot-spot = that stress."""
        hs = HotSpotStressAssessment.extrapolate_type_a(100.0, 100.0)
        assert hs == pytest.approx(100.0, rel=1e-6)

    def test_type_a_fine_quadratic(self):
        """Type a quadratic: 2.52*s(0.4t) - 2.24*s(0.9t) + 0.72*s(1.4t)."""
        hs = HotSpotStressAssessment.extrapolate_type_a_fine(160.0, 140.0, 125.0)
        expected = 2.52 * 160.0 - 2.24 * 140.0 + 0.72 * 125.0
        assert hs == pytest.approx(expected, rel=1e-6)

    def test_type_b(self):
        """Type b: sigma_hs = 3*s(5mm) - 3*s(15mm) + s(25mm)."""
        hs = HotSpotStressAssessment.extrapolate_type_b(200.0, 160.0, 130.0)
        expected = 3.0 * 200.0 - 3.0 * 160.0 + 130.0
        assert hs == pytest.approx(expected, rel=1e-6)

    def test_type_a_extrapolation_increases_stress(self):
        """Hot-spot stress should be higher than reference point stresses if stress decreases away from toe."""
        hs = HotSpotStressAssessment.extrapolate_type_a(150.0, 100.0)
        assert hs > 150.0  # Extrapolation to toe should be higher


class TestHotSpotAssessment:

    def test_evaluate_pass(self):
        assessor = HotSpotStressAssessment(fat_class=100, material="steel")
        result = assessor.evaluate(hotspot_stress_range=80.0, num_cycles=1_000_000)
        assert result.status == "PASS"
        assert result.method == "hotspot"

    def test_evaluate_fail(self):
        assessor = HotSpotStressAssessment(fat_class=100, material="steel")
        result = assessor.evaluate(hotspot_stress_range=150.0, num_cycles=5_000_000)
        assert result.status == "FAIL"

    def test_fat100_at_2e6(self):
        """FAT 100 at 100 MPa, 2e6 cycles: damage ratio = 1.0."""
        assessor = HotSpotStressAssessment(fat_class=100, material="steel")
        result = assessor.evaluate(100.0, 2_000_000)
        assert result.damage_ratio == pytest.approx(1.0, rel=1e-4)

    def test_safety_factor(self):
        assessor = HotSpotStressAssessment(fat_class=100, material="steel")
        result = assessor.evaluate(70.0, 1_000_000)
        assert result.safety_factor > 1.0

    def test_aluminum_fat_class(self):
        assessor = HotSpotStressAssessment(fat_class=45, material="aluminum")
        result = assessor.evaluate(30.0, 1_000_000)
        assert result.status == "PASS"

    def test_extrapolate_from_fea(self):
        assessor = HotSpotStressAssessment(hotspot_type="a")
        distances = np.array([4.0, 8.0, 12.0, 16.0])
        stresses = np.array([180.0, 150.0, 130.0, 115.0])
        hs = assessor.extrapolate_from_fea(stresses, distances, plate_thickness=10.0)
        assert hs > 0
        assert hs > stresses[0]  # Extrapolated to toe should be higher
