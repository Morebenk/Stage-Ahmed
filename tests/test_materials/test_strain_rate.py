"""Tests for strain rate models."""

import pytest
import math

from weldfatigue.materials.strain_rate import (
    cowper_symonds_factor,
    cowper_symonds_yield,
    johnson_cook_flow_stress,
)


class TestCowperSymonds:

    def test_zero_strain_rate(self):
        factor = cowper_symonds_factor(0.0, D=40.4, q=5.0)
        assert factor == 1.0

    def test_negative_strain_rate(self):
        factor = cowper_symonds_factor(-1.0, D=40.4, q=5.0)
        assert factor == 1.0

    def test_positive_strain_rate(self):
        factor = cowper_symonds_factor(100.0, D=40.4, q=5.0)
        assert factor > 1.0

    def test_known_values_mild_steel(self):
        # Mild steel: D=40.4, q=5
        # At 1000/s: DIF = 1 + (1000/40.4)^(1/5) = 1 + (24.75)^0.2
        factor = cowper_symonds_factor(1000.0, D=40.4, q=5.0)
        expected = 1.0 + (1000.0 / 40.4) ** 0.2
        assert factor == pytest.approx(expected, rel=1e-6)

    def test_yield_computation(self):
        dynamic = cowper_symonds_yield(350.0, 100.0, D=100, q=4.73)
        assert dynamic > 350.0

    def test_yield_at_zero_rate(self):
        dynamic = cowper_symonds_yield(350.0, 0.0, D=100, q=4.73)
        assert dynamic == 350.0


class TestJohnsonCook:

    def test_quasi_static_at_ref_temp(self):
        """At quasi-static rate and reference temp, sigma ~ A."""
        sigma = johnson_cook_flow_stress(
            epsilon_p=0.0, strain_rate=1.0, temperature=293.0,
            A=330.0, B=780.0, n=0.48, C=0.012, m=0.8,
            T_ref=293.0, T_melt=1793.0,
        )
        assert sigma == pytest.approx(330.0, rel=1e-6)

    def test_strain_hardening(self):
        """Higher strain should give higher stress."""
        s1 = johnson_cook_flow_stress(
            0.01, 1.0, 293.0, A=330, B=780, n=0.48, C=0.012, m=0.8
        )
        s2 = johnson_cook_flow_stress(
            0.1, 1.0, 293.0, A=330, B=780, n=0.48, C=0.012, m=0.8
        )
        assert s2 > s1

    def test_rate_effect(self):
        """Higher strain rate should give higher stress."""
        s1 = johnson_cook_flow_stress(
            0.05, 1.0, 293.0, A=330, B=780, n=0.48, C=0.012, m=0.8
        )
        s2 = johnson_cook_flow_stress(
            0.05, 1000.0, 293.0, A=330, B=780, n=0.48, C=0.012, m=0.8
        )
        assert s2 > s1

    def test_thermal_softening(self):
        """Higher temperature should give lower stress."""
        s1 = johnson_cook_flow_stress(
            0.05, 1.0, 293.0, A=330, B=780, n=0.48, C=0.012, m=0.8,
            T_ref=293.0, T_melt=1793.0,
        )
        s2 = johnson_cook_flow_stress(
            0.05, 1.0, 800.0, A=330, B=780, n=0.48, C=0.012, m=0.8,
            T_ref=293.0, T_melt=1793.0,
        )
        assert s2 < s1
