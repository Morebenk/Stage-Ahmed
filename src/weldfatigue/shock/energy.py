"""Energy absorption metrics for crash/impact assessment."""

import numpy as np

from weldfatigue.core.schemas import EnergyMetrics


class EnergyAbsorption:
    """
    Energy absorption metrics for crash/impact assessment.

    Metrics:
        - Total absorbed energy (integral of force-displacement)
        - Specific energy absorption (SEA) [J/kg]
        - Crush force efficiency (CFE) = Pm/Pmax
        - Mean crush force (Pm)
        - Peak force (Pmax)
    """

    @staticmethod
    def total_energy(force: np.ndarray, displacement: np.ndarray) -> float:
        """Integrate force-displacement curve using trapezoidal rule."""
        return float(np.trapezoid(force, displacement))

    @staticmethod
    def specific_energy_absorption(total_energy_j: float, mass_kg: float) -> float:
        """SEA = E / m [J/kg]."""
        if mass_kg <= 0:
            raise ValueError("Mass must be positive.")
        return total_energy_j / mass_kg

    @staticmethod
    def crush_metrics(
        force: np.ndarray,
        displacement: np.ndarray,
        mass: float = None,
    ) -> EnergyMetrics:
        """
        Compute all crush metrics from force-displacement curve.

        Args:
            force: Force array [N]
            displacement: Displacement array [mm]
            mass: Component mass [kg] (optional, for SEA calculation)
        """
        total_e = float(np.trapezoid(force, displacement))
        peak_force = float(np.max(force))
        total_stroke = displacement[-1] - displacement[0]
        mean_force = total_e / total_stroke if total_stroke > 0 else 0.0
        cfe = mean_force / peak_force if peak_force > 0 else 0.0

        sea = None
        if mass is not None and mass > 0:
            sea = total_e / mass

        return EnergyMetrics(
            total_energy=total_e,
            specific_energy_absorption=sea,
            mean_force=mean_force,
            peak_force=peak_force,
            crush_force_efficiency=cfe,
        )
