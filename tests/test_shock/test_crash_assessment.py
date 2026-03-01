"""Tests for the crash assessment orchestrator."""

import pytest
import numpy as np

from weldfatigue.shock.crash_assessment import CrashAssessment


class TestCrashAssessment:

    @pytest.fixture
    def assessor(self):
        return CrashAssessment()

    def test_evaluate_dynamic_material(self, assessor):
        result = assessor.evaluate_dynamic_material("DP600", strain_rate=100.0)
        assert result.dynamic_yield > 350  # Must exceed static yield
        assert result.enhancement_factor > 1.0

    def test_evaluate_dynamic_material_zero_rate(self, assessor):
        result = assessor.evaluate_dynamic_material("DP600", strain_rate=0.0)
        # At zero strain rate, dynamic yield ~ static yield
        assert result.enhancement_factor == pytest.approx(1.0, abs=0.01)

    def test_check_weld_failure_force_based(self, assessor):
        result = assessor.check_weld_failure(
            criterion="force_based",
            normal_force=500,
            shear_force=300,
            weld_throat=5.0,
            weld_length=100.0,
            allowable_stress=400.0,
        )
        assert result.status in ("PASS", "FAIL")
        assert result.criterion == "force_based"

    def test_check_weld_failure_stress_based(self, assessor):
        result = assessor.check_weld_failure(
            criterion="stress_based",
            sigma_perp=50,
            tau_perp=30,
            tau_parallel=20,
            fu=500,
        )
        assert result.status in ("PASS", "FAIL")
        assert result.criterion == "stress_based_EN1993"

    def test_check_weld_failure_unknown_raises(self, assessor):
        with pytest.raises(ValueError, match="Unknown criterion"):
            assessor.check_weld_failure(criterion="unknown")

    def test_evaluate_energy(self, assessor):
        force = np.array([0, 5000, 10000, 8000], dtype=float)
        disp = np.array([0, 5, 10, 15], dtype=float)
        metrics = assessor.evaluate_energy(force, disp, mass=3.0)
        assert metrics.total_energy > 0
        assert metrics.specific_energy_absorption is not None

    def test_run_full_assessment(self, assessor):
        result = assessor.run_full_assessment(
            material_name="DP600",
            strain_rate=500.0,
        )
        assert "dynamic_material" in result
        assert result["dynamic_material"]["dynamic_yield"] > 0

    def test_run_full_with_weld_check(self, assessor):
        result = assessor.run_full_assessment(
            material_name="S355J2",
            strain_rate=100.0,
            weld_check={
                "criterion": "stress_based",
                "sigma_perp": 100,
                "tau_perp": 50,
                "tau_parallel": 30,
                "fu": 490,
            },
        )
        assert "weld_failure" in result
        assert result["weld_failure"]["status"] in ("PASS", "FAIL")

    def test_run_full_with_energy(self, assessor):
        result = assessor.run_full_assessment(
            material_name="DP600",
            strain_rate=200.0,
            force_displacement={
                "force": np.array([0, 5000, 10000, 8000], dtype=float),
                "displacement": np.array([0, 5, 10, 15], dtype=float),
                "mass": 2.0,
            },
        )
        assert "energy" in result
        assert result["energy"]["total_energy"] > 0

    def test_aluminum_material(self, assessor):
        result = assessor.evaluate_dynamic_material("6061-T6", strain_rate=50.0)
        assert result.dynamic_yield > 0
