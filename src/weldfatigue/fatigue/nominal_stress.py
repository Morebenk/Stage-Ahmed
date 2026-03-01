"""IIW Nominal Stress Method for fatigue assessment."""

from weldfatigue.core.schemas import CumulativeDamageResult, FatigueResult
from weldfatigue.fatigue.damage import PalmgrenMiner
from weldfatigue.fatigue.mean_stress import MeanStressCorrection
from weldfatigue.fatigue.sn_curve import SNCurve


class NominalStressAssessment:
    """
    IIW Nominal Stress Method.

    The simplest IIW approach. The nominal stress is calculated using
    elementary structural mechanics (beam theory, etc.) excluding local
    stress concentrations from the weld itself. The FAT class encapsulates
    the effect of the weld detail.
    """

    def __init__(
        self,
        fat_class: int,
        material: str = "steel",
        variable_amplitude: bool = False,
    ):
        self.sn_curve = SNCurve(fat_class, material, variable_amplitude)
        self.fat_class = fat_class
        self.material = material

    def evaluate(
        self,
        stress_range: float,
        num_cycles: int,
        mean_stress_correction: str = "none",
        mean_stress: float = 0.0,
        ultimate_strength: float = None,
        yield_strength: float = None,
    ) -> FatigueResult:
        """Run nominal stress fatigue check for a single load block."""
        effective_stress_range = stress_range

        # Apply mean stress correction if needed
        if mean_stress_correction != "none" and mean_stress != 0:
            stress_amplitude = stress_range / 2.0
            if mean_stress_correction == "goodman" and ultimate_strength:
                corrected_amp = MeanStressCorrection.goodman(
                    stress_amplitude, mean_stress, ultimate_strength
                )
            elif mean_stress_correction == "gerber" and ultimate_strength:
                corrected_amp = MeanStressCorrection.gerber(
                    stress_amplitude, mean_stress, ultimate_strength
                )
            elif mean_stress_correction == "soderberg" and yield_strength:
                corrected_amp = MeanStressCorrection.soderberg(
                    stress_amplitude, mean_stress, yield_strength
                )
            else:
                corrected_amp = stress_amplitude

            effective_stress_range = corrected_amp * 2.0

        # Get allowable cycles
        N_f = self.sn_curve.cycles_to_failure(effective_stress_range)

        # Calculate damage and utilization
        if N_f == float("inf"):
            damage_ratio = 0.0
            utilization = 0.0
            safety_factor = float("inf")
        else:
            damage_ratio = num_cycles / N_f
            utilization = damage_ratio * 100.0
            safety_factor = N_f / num_cycles if num_cycles > 0 else float("inf")

        status = "PASS" if damage_ratio < 1.0 else "FAIL"

        return FatigueResult(
            method="nominal",
            fat_class=self.fat_class,
            allowable_cycles=N_f,
            applied_cycles=num_cycles,
            damage_ratio=damage_ratio,
            utilization=utilization,
            status=status,
            safety_factor=safety_factor,
        )

    def evaluate_spectrum(
        self,
        load_spectrum: list[tuple[float, int]],
        damage_limit: float = 1.0,
        mean_stress_correction: str = "none",
        mean_stress: float = 0.0,
        ultimate_strength: float = None,
    ) -> CumulativeDamageResult:
        """
        Evaluate variable-amplitude loading using Palmgren-Miner rule.
        load_spectrum: list of (stress_range, num_cycles) tuples.
        """
        # Apply mean stress correction to each block if needed
        corrected_spectrum = []
        for stress_range, n_cycles in load_spectrum:
            effective_range = stress_range
            if mean_stress_correction == "goodman" and ultimate_strength and mean_stress != 0:
                amp = stress_range / 2.0
                corrected_amp = MeanStressCorrection.goodman(
                    amp, mean_stress, ultimate_strength
                )
                effective_range = corrected_amp * 2.0
            corrected_spectrum.append((effective_range, n_cycles))

        va_curve = SNCurve(self.fat_class, self.material, variable_amplitude=True)
        miner = PalmgrenMiner(va_curve, damage_limit)
        return miner.compute_damage(corrected_spectrum)
