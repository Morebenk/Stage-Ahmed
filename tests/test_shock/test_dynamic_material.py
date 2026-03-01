"""Tests for dynamic material model."""

import pytest
import numpy as np

from weldfatigue.materials.database import MaterialDatabase
from weldfatigue.shock.dynamic_material import DynamicMaterialModel


class TestDynamicMaterialModel:

    @pytest.fixture
    def dp600_model(self, material_db):
        mat = material_db.get("DP600")
        return DynamicMaterialModel(mat)

    def test_dynamic_yield_cs(self, dp600_model):
        dy = dp600_model.dynamic_yield(100.0, "cowper_symonds")
        assert dy > 350.0  # Must be above static yield

    def test_dynamic_yield_zero_rate(self, dp600_model):
        dy = dp600_model.dynamic_yield(0.0, "cowper_symonds")
        assert dy == 350.0

    def test_dif_at_100(self, dp600_model):
        dif = dp600_model.dynamic_increase_factor(100.0, "cowper_symonds")
        assert dif > 1.0

    def test_dif_at_zero(self, dp600_model):
        dif = dp600_model.dynamic_increase_factor(0.0, "cowper_symonds")
        assert dif == 1.0

    def test_dynamic_yield_jc(self, dp600_model):
        dy = dp600_model.dynamic_yield(100.0, "johnson_cook")
        assert dy > 350.0

    def test_flow_curve_shape(self, dp600_model):
        strains, stresses = dp600_model.dynamic_flow_curve(100.0)
        assert len(strains) == 100
        assert len(stresses) == 100
        # Stress should increase with strain (hardening)
        assert stresses[-1] > stresses[0]

    def test_higher_rate_higher_stress(self, dp600_model):
        _, s1 = dp600_model.dynamic_flow_curve(1.0)
        _, s2 = dp600_model.dynamic_flow_curve(1000.0)
        assert np.mean(s2) > np.mean(s1)


class TestWeldFailure:

    def test_force_based_pass(self):
        from weldfatigue.shock.weld_failure import WeldFailureCriteria
        result = WeldFailureCriteria.force_based_check(
            normal_force=100, shear_force=50,
            weld_throat=5, weld_length=100,
            allowable_stress=500, safety_factor=1.25,
        )
        assert result.status == "PASS"

    def test_stress_based_pass(self):
        from weldfatigue.shock.weld_failure import WeldFailureCriteria
        result = WeldFailureCriteria.stress_based_check(
            sigma_perp=100, tau_perp=50, tau_parallel=30,
            fu=600, beta_w=0.8, gamma_Mw=1.25,
        )
        assert result.status == "PASS"
        assert result.utilization < 1.0

    def test_stress_based_fail(self):
        from weldfatigue.shock.weld_failure import WeldFailureCriteria
        result = WeldFailureCriteria.stress_based_check(
            sigma_perp=400, tau_perp=200, tau_parallel=150,
            fu=500, beta_w=0.8, gamma_Mw=1.25,
        )
        assert result.status == "FAIL"


class TestEnergyAbsorption:

    def test_total_energy(self):
        from weldfatigue.shock.energy import EnergyAbsorption
        force = np.array([0, 1000, 2000, 1500, 1000])
        disp = np.array([0, 10, 20, 30, 40])
        energy = EnergyAbsorption.total_energy(force, disp)
        assert energy > 0

    def test_crush_metrics(self):
        from weldfatigue.shock.energy import EnergyAbsorption
        force = np.array([0, 5000, 4000, 4500, 3000])
        disp = np.array([0, 10, 20, 30, 40])
        metrics = EnergyAbsorption.crush_metrics(force, disp, mass=2.0)
        assert metrics.peak_force == 5000
        assert 0 < metrics.crush_force_efficiency <= 1.0
        assert metrics.specific_energy_absorption > 0
