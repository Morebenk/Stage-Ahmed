"""IIW Effective Notch Stress Method."""

from weldfatigue.core.schemas import FatigueResult
from weldfatigue.fatigue.sn_curve import SNCurve


class EffectiveNotchStressAssessment:
    """
    IIW Effective Notch Stress Method.

    All welds modeled with a fictitious reference radius of:
        - r_ref = 1.0 mm for steel and aluminum (plate thickness >= 5mm)
        - r_ref = 0.05 mm for thin sheets (plate thickness < 5mm)

    Universal FAT class:
        - FAT 225 for steel (all weld details)
        - FAT 71 for aluminum (all weld details)

    The method requires an FEA model with the notch radius explicitly
    modeled at the weld toe/root.
    """

    STANDARD_RADIUS = 1.0  # mm, for t >= 5mm
    THIN_SHEET_RADIUS = 0.05  # mm, for t < 5mm

    FAT_STEEL = 225
    FAT_ALUMINUM = 71

    def __init__(
        self,
        material: str = "steel",
        plate_thickness: float = 10.0,
        variable_amplitude: bool = False,
    ):
        self.material = material
        self.plate_thickness = plate_thickness

        if plate_thickness < 5.0:
            self.reference_radius = self.THIN_SHEET_RADIUS
        else:
            self.reference_radius = self.STANDARD_RADIUS

        if material == "steel":
            self.fat_class = self.FAT_STEEL
        else:
            self.fat_class = self.FAT_ALUMINUM

        self.sn_curve = SNCurve(self.fat_class, material, variable_amplitude)

    def evaluate(
        self, notch_stress_range: float, num_cycles: int
    ) -> FatigueResult:
        """Evaluate fatigue using effective notch stress."""
        N_f = self.sn_curve.cycles_to_failure(notch_stress_range)

        if N_f == float("inf"):
            damage_ratio = 0.0
            safety_factor = float("inf")
        else:
            damage_ratio = num_cycles / N_f
            safety_factor = N_f / num_cycles if num_cycles > 0 else float("inf")

        return FatigueResult(
            method="notch",
            fat_class=self.fat_class,
            allowable_cycles=N_f,
            applied_cycles=num_cycles,
            damage_ratio=damage_ratio,
            utilization=damage_ratio * 100.0,
            status="PASS" if damage_ratio < 1.0 else "FAIL",
            safety_factor=safety_factor,
        )
