"""IIW weld root fatigue assessment."""

import math
from weldfatigue.core.schemas import FatigueResult
from weldfatigue.fatigue.sn_curve import SNCurve


class RootFatigueAssessment:
    """
    IIW weld root fatigue assessment for partial penetration welds.

    Root failure is a critical failure mode for fillet welds where
    the crack initiates from the unfused root face.

    References:
    - IIW root fatigue guideline (Fricke, 2013)
    - IIW XIII-1823-07 Section 4.1.5
    """

    ROOT_REFERENCE_RADIUS = 0.05  # mm, micro-support concept
    ROOT_FAT_STEEL = 200  # For r_ref = 0.05mm in steel
    ROOT_FAT_ALUMINUM = 71  # For r_ref = 0.05mm in aluminum

    @staticmethod
    def root_stress_concentration(
        weld_throat: float,
        penetration_depth: float,
        plate_thickness: float,
        load_type: str = "tension",
    ) -> float:
        """
        Stress concentration factor at weld root.

        Depends on the ratio of penetration depth to plate thickness
        and the weld throat dimension.

        For partial penetration:
            SCF = 1 + 2 * sqrt((t - p) / (2 * a))

        where t = plate thickness, p = penetration depth, a = throat.
        """
        if plate_thickness <= 0 or weld_throat <= 0:
            raise ValueError("Thickness and throat must be positive")

        gap = plate_thickness - penetration_depth
        if gap <= 0:
            return 1.0  # Full penetration, minimal root concentration

        scf = 1.0 + 2.0 * math.sqrt(gap / (2.0 * weld_throat))

        if load_type == "bending":
            scf *= 0.85  # Bending has lower root stress than tension

        return scf

    @staticmethod
    def root_notch_stress(
        nominal_stress: float,
        weld_throat: float,
        plate_thickness: float,
        penetration_depth: float,
        load_type: str = "tension",
    ) -> float:
        """
        Effective notch stress at weld root.

        Uses r_ref = 0.05mm (micro-support concept for root assessment).

        sigma_root = sigma_nominal * SCF * (t / a_eff)

        where a_eff is the effective throat considering penetration.
        """
        scf = RootFatigueAssessment.root_stress_concentration(
            weld_throat, penetration_depth, plate_thickness, load_type
        )

        # Effective throat includes penetration
        a_eff = weld_throat + penetration_depth
        if a_eff <= 0:
            a_eff = weld_throat

        # Stress at root = nominal * SCF * geometry ratio
        stress_ratio = plate_thickness / a_eff if a_eff > 0 else 1.0
        root_stress = nominal_stress * scf * min(stress_ratio, 3.0)

        return root_stress

    def __init__(
        self,
        material: str = "steel",
        variable_amplitude: bool = False,
    ):
        self.material = material
        if material == "steel":
            self.fat_class = self.ROOT_FAT_STEEL
        else:
            self.fat_class = self.ROOT_FAT_ALUMINUM

        self.sn_curve = SNCurve(self.fat_class, material, variable_amplitude)

    def evaluate(
        self,
        root_stress_range: float,
        num_cycles: int,
    ) -> FatigueResult:
        """
        Evaluate root fatigue life.

        Uses the root-specific FAT class and S-N curve.
        """
        N_f = self.sn_curve.cycles_to_failure(root_stress_range)

        if N_f == float("inf"):
            damage_ratio = 0.0
            safety_factor = float("inf")
        else:
            damage_ratio = num_cycles / N_f
            safety_factor = N_f / num_cycles if num_cycles > 0 else float("inf")

        return FatigueResult(
            method="root",
            fat_class=self.fat_class,
            allowable_cycles=N_f,
            applied_cycles=num_cycles,
            damage_ratio=damage_ratio,
            utilization=damage_ratio * 100.0,
            status="PASS" if damage_ratio < 1.0 else "FAIL",
            safety_factor=safety_factor,
        )

    @staticmethod
    def toe_vs_root_comparison(
        toe_result: FatigueResult,
        root_result: FatigueResult,
    ) -> dict:
        """
        Compare toe and root failure modes.

        Returns dict identifying the critical (governing) failure location.
        """
        toe_life = toe_result.allowable_cycles
        root_life = root_result.allowable_cycles

        if toe_life <= root_life:
            critical = "toe"
            governing_result = toe_result
        else:
            critical = "root"
            governing_result = root_result

        return {
            "critical_location": critical,
            "toe_life": toe_life,
            "root_life": root_life,
            "life_ratio": toe_life / root_life if root_life > 0 and root_life != float("inf") else float("inf"),
            "governing_result": governing_result.model_dump(),
        }
