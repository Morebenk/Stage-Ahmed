"""Strain-rate enhanced material properties for crash analysis."""

import numpy as np

from weldfatigue.materials.models import Material
from weldfatigue.materials.strain_rate import (
    cowper_symonds_factor,
    cowper_symonds_yield,
    johnson_cook_flow_stress,
)


class DynamicMaterialModel:
    """
    Compute strain-rate-enhanced material properties for crash analysis.

    Wraps Cowper-Symonds and Johnson-Cook models.
    """

    def __init__(self, material: Material):
        self.material = material

    def dynamic_yield(
        self, strain_rate: float, model: str = "cowper_symonds"
    ) -> float:
        """Compute dynamic yield stress at given strain rate."""
        mat = self.material
        if model == "cowper_symonds":
            return cowper_symonds_yield(
                mat.yield_strength, strain_rate, mat.cs_D, mat.cs_q
            )
        elif model == "johnson_cook":
            if mat.jc_A is None:
                raise ValueError(f"Johnson-Cook parameters not available for {mat.name}")
            return johnson_cook_flow_stress(
                epsilon_p=0.002,  # At yield (~0.2% offset)
                strain_rate=strain_rate,
                temperature=mat.jc_T_ref,
                A=mat.jc_A,
                B=mat.jc_B,
                n=mat.jc_n,
                C=mat.jc_C,
                m=mat.jc_m,
                T_melt=mat.jc_T_melt,
                T_ref=mat.jc_T_ref,
            )
        raise ValueError(f"Unknown model: {model}")

    def dynamic_increase_factor(
        self, strain_rate: float, model: str = "cowper_symonds"
    ) -> float:
        """DIF = sigma_dynamic / sigma_static."""
        dynamic = self.dynamic_yield(strain_rate, model)
        return dynamic / self.material.yield_strength

    def dynamic_flow_curve(
        self,
        strain_rate: float,
        strain_range: tuple[float, float] = (0.0, 0.5),
        n_points: int = 100,
        temperature: float = 293.0,
    ) -> tuple[np.ndarray, np.ndarray]:
        """Generate (plastic_strain, true_stress) curve at given strain rate."""
        mat = self.material
        if mat.jc_A is None:
            raise ValueError(f"Johnson-Cook parameters not available for {mat.name}")

        strains = np.linspace(strain_range[0], strain_range[1], n_points)
        # Avoid zero strain for power law
        strains_safe = np.maximum(strains, 1e-6)
        stresses = np.array([
            johnson_cook_flow_stress(
                epsilon_p=eps,
                strain_rate=strain_rate,
                temperature=temperature,
                A=mat.jc_A,
                B=mat.jc_B,
                n=mat.jc_n,
                C=mat.jc_C,
                m=mat.jc_m,
                T_melt=mat.jc_T_melt,
                T_ref=mat.jc_T_ref,
            )
            for eps in strains_safe
        ])
        return strains, stresses
