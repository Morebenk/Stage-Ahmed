"""Top-level crash/shock assessment orchestrator."""

from typing import Optional

import numpy as np

from weldfatigue.core.schemas import CrashResult, EnergyMetrics, WeldFailureResult
from weldfatigue.materials.database import MaterialDatabase
from weldfatigue.shock.dynamic_material import DynamicMaterialModel
from weldfatigue.shock.energy import EnergyAbsorption
from weldfatigue.shock.weld_failure import WeldFailureCriteria


class CrashAssessment:
    """
    Top-level orchestrator for crash/shock assessment.

    Coordinates dynamic material properties, weld failure checks,
    and energy absorption analysis.
    """

    def __init__(self, material_db: Optional[MaterialDatabase] = None):
        self.material_db = material_db or MaterialDatabase()

    def evaluate_dynamic_material(
        self,
        material_name: str,
        strain_rate: float,
        model: str = "cowper_symonds",
    ) -> CrashResult:
        """Compute dynamic material properties at given strain rate."""
        material = self.material_db.get(material_name)
        dyn_model = DynamicMaterialModel(material)

        dynamic_yield = dyn_model.dynamic_yield(strain_rate, model)
        dif = dyn_model.dynamic_increase_factor(strain_rate, model)

        return CrashResult(
            dynamic_yield=dynamic_yield,
            enhancement_factor=dif,
        )

    def check_weld_failure(
        self,
        criterion: str,
        **kwargs,
    ) -> WeldFailureResult:
        """Run a weld failure check."""
        if criterion == "force_based":
            return WeldFailureCriteria.force_based_check(**kwargs)
        elif criterion == "stress_based":
            return WeldFailureCriteria.stress_based_check(**kwargs)
        raise ValueError(f"Unknown criterion: {criterion}")

    def evaluate_energy(
        self,
        force: np.ndarray,
        displacement: np.ndarray,
        mass: Optional[float] = None,
    ) -> EnergyMetrics:
        """Compute energy absorption metrics."""
        return EnergyAbsorption.crush_metrics(force, displacement, mass)

    def run_full_assessment(
        self,
        material_name: str,
        strain_rate: float,
        strain_rate_model: str = "cowper_symonds",
        weld_check: Optional[dict] = None,
        force_displacement: Optional[dict] = None,
    ) -> dict:
        """
        Run a complete crash assessment.

        Returns dict with dynamic material, weld check, and energy results.
        """
        # Dynamic material
        crash_result = self.evaluate_dynamic_material(
            material_name, strain_rate, strain_rate_model
        )

        output = {
            "dynamic_material": crash_result.model_dump(),
        }

        # Weld failure check
        if weld_check:
            criterion = weld_check.pop("criterion", "stress_based")
            weld_result = self.check_weld_failure(criterion, **weld_check)
            output["weld_failure"] = weld_result.model_dump()

        # Energy absorption
        if force_displacement:
            energy_result = self.evaluate_energy(
                force_displacement["force"],
                force_displacement["displacement"],
                force_displacement.get("mass"),
            )
            output["energy"] = energy_result.model_dump()

        return output
