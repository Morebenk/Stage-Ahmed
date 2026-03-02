"""Tests for fracture mechanics (LEFM) assessment."""

import math
import pytest
from weldfatigue.fatigue.fracture_mechanics import FractureMechanicsAssessment


class TestFractureMechanics:
    """Tests for FractureMechanicsAssessment class."""

    # --- Stress intensity factor ---

    def test_sif_basic(self):
        """K = Y * Mk * sigma * sqrt(pi*a) with Y=1, Mk=1."""
        K = FractureMechanicsAssessment.stress_intensity_factor(100.0, 1.0)
        expected = 100.0 * math.sqrt(math.pi * 1.0)
        assert K == pytest.approx(expected, rel=1e-6)

    def test_sif_zero_crack(self):
        """Zero crack size => K = 0."""
        K = FractureMechanicsAssessment.stress_intensity_factor(100.0, 0.0)
        assert K == pytest.approx(0.0)

    def test_sif_with_factors(self):
        """K with Y=1.12 and Mk=1.5."""
        K = FractureMechanicsAssessment.stress_intensity_factor(100.0, 2.0, 1.12, 1.5)
        expected = 1.12 * 1.5 * 100.0 * math.sqrt(math.pi * 2.0)
        assert K == pytest.approx(expected, rel=1e-6)

    # --- Geometry factor ---

    def test_Y_edge_small_crack(self):
        """Edge crack with small a/t: Y ≈ 1.12."""
        Y = FractureMechanicsAssessment.geometry_factor_Y(0.5, 50.0, "edge")
        assert Y == pytest.approx(1.12, abs=0.05)

    def test_Y_through_crack(self):
        """Through crack: Y = 1.0."""
        Y = FractureMechanicsAssessment.geometry_factor_Y(5.0, 10.0, "through")
        assert Y == pytest.approx(1.0)

    def test_Y_increases_with_a_over_t(self):
        """Y generally increases with a/t for edge crack."""
        Y_small = FractureMechanicsAssessment.geometry_factor_Y(1.0, 50.0, "edge")
        Y_large = FractureMechanicsAssessment.geometry_factor_Y(20.0, 50.0, "edge")
        assert Y_large > Y_small

    # --- Mk factor ---

    def test_Mk_small_crack(self):
        """Small crack: Mk should be significant (> 1)."""
        Mk = FractureMechanicsAssessment.Mk_factor(0.5, 20.0, "t_butt")
        assert Mk >= 1.0

    def test_Mk_deep_crack(self):
        """Deep crack: Mk approaches 1.0."""
        Mk = FractureMechanicsAssessment.Mk_factor(15.0, 20.0, "t_butt")
        assert Mk >= 1.0

    # --- Paris law ---

    def test_paris_rate_basic(self):
        """da/dN = C * dK^m."""
        rate = FractureMechanicsAssessment.paris_law_rate(100.0, 5.21e-13, 3.0)
        expected = 5.21e-13 * 100.0 ** 3.0
        assert rate == pytest.approx(expected, rel=1e-6)

    def test_paris_rate_below_threshold(self):
        """Below threshold: da/dN = 0."""
        rate = FractureMechanicsAssessment.paris_law_rate(50.0, 5.21e-13, 3.0, 60.0)
        assert rate == pytest.approx(0.0)

    def test_paris_rate_higher_dK_faster(self):
        """Higher delta_K => higher growth rate."""
        r1 = FractureMechanicsAssessment.paris_law_rate(100.0, 5.21e-13, 3.0)
        r2 = FractureMechanicsAssessment.paris_law_rate(200.0, 5.21e-13, 3.0)
        assert r2 > r1

    # --- Crack growth integration ---

    def test_integration_produces_cycles(self):
        """Integration should produce positive cycle count."""
        fm = FractureMechanicsAssessment()
        result = fm.integrate_crack_growth(
            initial_crack=0.5, critical_crack=10.0,
            stress_range=100.0, plate_thickness=20.0,
        )
        assert result["total_cycles"] > 0
        assert len(result["crack_sizes"]) > 1

    def test_integration_crack_grows(self):
        """Crack sizes should be monotonically increasing."""
        fm = FractureMechanicsAssessment()
        result = fm.integrate_crack_growth(
            initial_crack=0.5, critical_crack=10.0,
            stress_range=80.0, plate_thickness=20.0,
        )
        cracks = result["crack_sizes"]
        for i in range(len(cracks) - 1):
            assert cracks[i + 1] >= cracks[i]

    def test_higher_stress_fewer_cycles(self):
        """Higher stress range => fewer cycles to failure."""
        fm = FractureMechanicsAssessment()
        r1 = fm.integrate_crack_growth(0.5, 10.0, 80.0, 20.0)
        r2 = fm.integrate_crack_growth(0.5, 10.0, 160.0, 20.0)
        assert r2["total_cycles"] < r1["total_cycles"]

    # --- Two-phase model ---

    def test_two_phase_total(self):
        """N_total = N_init + N_prop."""
        fm = FractureMechanicsAssessment()
        result = fm.two_phase_model(
            initiation_cycles=100000,
            initial_crack=0.5, critical_crack=10.0,
            stress_range=100.0, plate_thickness=20.0,
        )
        assert result["total_cycles"] == pytest.approx(
            result["initiation_cycles"] + result["propagation_cycles"]
        )

    # --- Paris parameters ---

    def test_paris_params_steel_air(self):
        """Default steel/air parameters should exist."""
        params = FractureMechanicsAssessment.get_paris_parameters("steel", "air")
        assert "C" in params
        assert "m" in params
        assert params["m"] == pytest.approx(3.0)

    def test_paris_params_aluminum(self):
        """Aluminum parameters should have higher C."""
        p_steel = FractureMechanicsAssessment.get_paris_parameters("steel", "air")
        p_al = FractureMechanicsAssessment.get_paris_parameters("aluminum", "air")
        assert p_al["C"] > p_steel["C"]
