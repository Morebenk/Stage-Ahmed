"""4R method for fatigue assessment (Nykänen & Björk 2016).

The 4R method accounts for four parameters:
    1. Stress Range (ΔS)
    2. Stress Ratio (R)
    3. Residual stress (σ_res)
    4. Material strength (Rm)

By correcting the applied notch stress range for local stress ratio
and residual stress effects, all data collapse onto a single
master S-N curve (FAT 200 for steel, r_ref = 1mm).

References:
    - Nykänen & Björk (2016), Int. J. Fatigue 93, 23–34
    - Björk et al. (2018), Welding in the World 62, 1285–1300
"""

import math

from weldfatigue.core.schemas import FourRResult
from weldfatigue.fatigue.sn_curve import SNCurve


class FourRMethod:
    """
    4R fatigue assessment method.

    Transforms applied stress conditions into an equivalent stress range
    on a universal master S-N curve by accounting for:
    - Local stress ratio (elastic-plastic via Neuber rule)
    - Residual stress superposition
    - Mean stress sensitivity (function of Rm)

    The master curve is FAT 200 (notch stress, r_ref = 1mm, R_local = 0).
    """

    MASTER_FAT_STEEL = 200
    MASTER_FAT_ALUMINUM = 71

    @staticmethod
    def neuber_correction(
        elastic_notch_stress: float,
        yield_strength: float,
        youngs_modulus: float = 210000.0,
    ) -> tuple[float, float]:
        """
        Neuber elastic-plastic correction at notch root.

        Neuber's rule: σ_local * ε_local = σ_elastic² / E

        For elastic-perfectly-plastic material:
            if σ_elastic <= Ry: σ_local = σ_elastic, ε_local = σ_elastic/E
            if σ_elastic > Ry:  σ_local = Ry, ε_local = σ_elastic²/(E*Ry)

        Args:
            elastic_notch_stress: Elastic notch stress [MPa]
            yield_strength: Material yield strength [MPa]
            youngs_modulus: Young's modulus [MPa]

        Returns:
            (sigma_local, epsilon_local) — local stress [MPa] and strain [-]
        """
        if abs(elastic_notch_stress) <= yield_strength:
            sigma_local = elastic_notch_stress
            epsilon_local = elastic_notch_stress / youngs_modulus
        else:
            sign = 1.0 if elastic_notch_stress >= 0 else -1.0
            sigma_local = sign * yield_strength
            epsilon_local = elastic_notch_stress ** 2 / (youngs_modulus * yield_strength)

        return sigma_local, epsilon_local

    @staticmethod
    def local_stress_ratio(
        sigma_max_notch: float,
        sigma_min_notch: float,
        residual_stress: float,
        yield_strength: float,
        youngs_modulus: float = 210000.0,
    ) -> float:
        """
        Compute local stress ratio R_local after elastic-plastic correction.

        Applies Neuber correction to both max and min notch stresses,
        then superposes residual stress:
            σ_max_local = σ_max_neuber + σ_res
            σ_min_local = σ_min_neuber + σ_res
            R_local = σ_min_local / σ_max_local

        Stress is clamped at yield to represent shakedown.
        """
        sigma_max_local, _ = FourRMethod.neuber_correction(
            sigma_max_notch, yield_strength, youngs_modulus
        )
        sigma_min_local, _ = FourRMethod.neuber_correction(
            sigma_min_notch, yield_strength, youngs_modulus
        )

        # Superpose residual stress
        sigma_max_total = sigma_max_local + residual_stress
        sigma_min_total = sigma_min_local + residual_stress

        # Clamp at yield (shakedown)
        sigma_max_total = min(sigma_max_total, yield_strength)
        sigma_min_total = min(sigma_min_total, yield_strength)

        if abs(sigma_max_total) < 1e-10:
            return 0.0

        return sigma_min_total / sigma_max_total

    @staticmethod
    def mean_stress_sensitivity(ultimate_strength: float) -> float:
        """
        Mean stress sensitivity parameter M.

        M = 0.00035 * Rm - 0.1

        Per Nykänen & Björk (2016) Table 2.
        Typical values:
            Rm=400 MPa => M=0.04
            Rm=600 MPa => M=0.11
            Rm=800 MPa => M=0.18
            Rm=1000 MPa => M=0.25

        Args:
            ultimate_strength: Material ultimate tensile strength Rm [MPa]

        Returns:
            Mean stress sensitivity M (clamped >= 0)
        """
        M = 0.00035 * ultimate_strength - 0.1
        return max(0.0, M)

    @staticmethod
    def equivalent_stress_range(
        stress_range: float,
        R_local: float,
        M: float,
    ) -> float:
        """
        Compute equivalent stress range for the master S-N curve.

        Δσ_eq = Δσ * (1 - M * R_local) / (1 + M)

        This transforms the actual stress range at local R-ratio
        to an equivalent range at R=0 on the master curve.

        For R_local > 1 (compression-dominated), the correction
        reduces the effective stress range (beneficial).
        For R_local < 0 (partially compressive), partial benefit.

        Args:
            stress_range: Applied notch stress range [MPa]
            R_local: Local stress ratio (after Neuber + residual)
            M: Mean stress sensitivity parameter

        Returns:
            Equivalent stress range [MPa]
        """
        denominator = 1.0 + M
        if denominator < 1e-10:
            return stress_range

        numerator = 1.0 - M * R_local
        factor = numerator / denominator

        # Factor must be positive and <= 1.0 (can't amplify beyond input)
        factor = max(0.0, min(factor, 1.0 + M))  # Allow slight increase for high R

        return stress_range * factor

    @staticmethod
    def evaluate(
        notch_stress_range: float,
        stress_ratio: float,
        residual_stress: float,
        ultimate_strength: float,
        yield_strength: float,
        num_cycles: int,
        youngs_modulus: float = 210000.0,
        material_type: str = "steel",
    ) -> FourRResult:
        """
        Full 4R method evaluation.

        Steps:
        1. Compute max/min notch stresses from range and R-ratio
        2. Neuber elastic-plastic correction
        3. Superpose residual stress → local R-ratio
        4. Compute mean stress sensitivity M from Rm
        5. Compute equivalent stress range
        6. Evaluate against master S-N curve (FAT 200)

        Args:
            notch_stress_range: Notch stress range [MPa]
            stress_ratio: Applied R-ratio
            residual_stress: Residual stress at weld [MPa]
            ultimate_strength: Material Rm [MPa]
            yield_strength: Material Rp0.2 [MPa]
            num_cycles: Number of applied cycles
            youngs_modulus: Young's modulus [MPa]
            material_type: steel or aluminum

        Returns:
            FourRResult with all assessment outputs
        """
        # Step 1: Compute max/min from range and R
        # ΔS = S_max - S_min, R = S_min / S_max
        # => S_max = ΔS / (1 - R),  S_min = R * ΔS / (1 - R)
        if abs(1.0 - stress_ratio) < 1e-10:
            # R ≈ 1 means zero range, treat as zero damage
            return FourRResult(
                local_stress_ratio=stress_ratio,
                equivalent_stress_range=0.0,
                allowable_cycles=float("inf"),
                applied_cycles=num_cycles,
                damage_ratio=0.0,
                status="PASS",
                master_curve_fat=FourRMethod.MASTER_FAT_STEEL,
            )

        sigma_max_notch = notch_stress_range / (1.0 - stress_ratio)
        sigma_min_notch = stress_ratio * sigma_max_notch

        # Step 2 & 3: Local stress ratio with Neuber + residual
        R_local = FourRMethod.local_stress_ratio(
            sigma_max_notch, sigma_min_notch,
            residual_stress, yield_strength, youngs_modulus,
        )

        # Step 4: Mean stress sensitivity
        M = FourRMethod.mean_stress_sensitivity(ultimate_strength)

        # Step 5: Equivalent stress range
        delta_sigma_eq = FourRMethod.equivalent_stress_range(
            notch_stress_range, R_local, M
        )

        # Step 6: Evaluate against master curve
        if material_type == "steel":
            master_fat = FourRMethod.MASTER_FAT_STEEL
        else:
            master_fat = FourRMethod.MASTER_FAT_ALUMINUM

        sn = SNCurve(master_fat, material_type, variable_amplitude=False)
        N_f = sn.cycles_to_failure(delta_sigma_eq)

        if N_f == float("inf"):
            damage_ratio = 0.0
        else:
            damage_ratio = num_cycles / N_f

        return FourRResult(
            local_stress_ratio=R_local,
            equivalent_stress_range=delta_sigma_eq,
            allowable_cycles=N_f,
            applied_cycles=num_cycles,
            damage_ratio=damage_ratio,
            status="PASS" if damage_ratio < 1.0 else "FAIL",
            master_curve_fat=master_fat,
        )
