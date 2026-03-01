"""IIW Structural Hot-Spot Stress Method."""

import numpy as np

from weldfatigue.core.schemas import FatigueResult
from weldfatigue.fatigue.sn_curve import SNCurve


class HotSpotStressAssessment:
    """
    IIW Structural Hot-Spot Stress Method.

    Determines the structural stress at the weld toe by surface stress
    extrapolation, eliminating the singular stress peak at the notch.

    Type a hot spot: extrapolation perpendicular to weld toe
        - Linear: sigma_hs = 1.67 * sigma(0.4t) - 0.67 * sigma(1.0t)
        - Quadratic: sigma_hs = 2.52*sigma(0.4t) - 2.24*sigma(0.9t) + 0.72*sigma(1.4t)

    Type b hot spot: extrapolation along weld toe
        - sigma_hs = 3*sigma(5mm) - 3*sigma(15mm) + sigma(25mm)

    Applicable FAT classes (steel):
        - FAT 100 for load-carrying fillet welds
        - FAT 90 for non-load-carrying fillet welds
    """

    def __init__(
        self,
        hotspot_type: str = "a",
        fat_class: int = 100,
        material: str = "steel",
        variable_amplitude: bool = False,
    ):
        self.hotspot_type = hotspot_type
        self.fat_class = fat_class
        self.material = material
        self.sn_curve = SNCurve(fat_class, material, variable_amplitude)

    @staticmethod
    def extrapolate_type_a(stress_04t: float, stress_10t: float) -> float:
        """Linear surface stress extrapolation for Type a."""
        return 1.67 * stress_04t - 0.67 * stress_10t

    @staticmethod
    def extrapolate_type_a_fine(
        stress_04t: float, stress_09t: float, stress_14t: float
    ) -> float:
        """Quadratic surface stress extrapolation for Type a with fine mesh."""
        return 2.52 * stress_04t - 2.24 * stress_09t + 0.72 * stress_14t

    @staticmethod
    def extrapolate_type_b(
        stress_5mm: float, stress_15mm: float, stress_25mm: float
    ) -> float:
        """Quadratic extrapolation for Type b hot spot."""
        return 3.0 * stress_5mm - 3.0 * stress_15mm + stress_25mm

    def extrapolate_from_fea(
        self,
        nodal_stresses: np.ndarray,
        distances: np.ndarray,
        plate_thickness: float,
    ) -> float:
        """General extrapolation from FEA nodal results using polyfit."""
        if self.hotspot_type == "a":
            # Fit linear/quadratic through reference points
            if len(nodal_stresses) >= 3:
                coeffs = np.polyfit(distances, nodal_stresses, 2)
                poly = np.poly1d(coeffs)
            else:
                coeffs = np.polyfit(distances, nodal_stresses, 1)
                poly = np.poly1d(coeffs)
            return float(poly(0))  # Extrapolate to weld toe (distance=0)
        else:
            coeffs = np.polyfit(distances, nodal_stresses, 2)
            poly = np.poly1d(coeffs)
            return float(poly(0))

    def evaluate(
        self, hotspot_stress_range: float, num_cycles: int
    ) -> FatigueResult:
        """Evaluate fatigue using hot-spot stress."""
        N_f = self.sn_curve.cycles_to_failure(hotspot_stress_range)

        if N_f == float("inf"):
            damage_ratio = 0.0
            safety_factor = float("inf")
        else:
            damage_ratio = num_cycles / N_f
            safety_factor = N_f / num_cycles if num_cycles > 0 else float("inf")

        return FatigueResult(
            method="hotspot",
            fat_class=self.fat_class,
            allowable_cycles=N_f,
            applied_cycles=num_cycles,
            damage_ratio=damage_ratio,
            utilization=damage_ratio * 100.0,
            status="PASS" if damage_ratio < 1.0 else "FAIL",
            safety_factor=safety_factor,
        )
