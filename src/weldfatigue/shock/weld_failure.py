"""Weld joint failure criteria for crash/shock loading."""

import math

from weldfatigue.core.schemas import WeldFailureResult


class WeldFailureCriteria:
    """
    Weld joint failure criteria for crash/shock loading.

    Implements:
        1. Force-based failure: compare weld forces against capacity
        2. Stress-based failure: compare equivalent stress against limit (EN 1993-1-8)
    """

    @staticmethod
    def force_based_check(
        normal_force: float,
        shear_force: float,
        weld_throat: float,
        weld_length: float,
        allowable_stress: float,
        safety_factor: float = 1.25,
    ) -> WeldFailureResult:
        """
        Check weld forces against capacity per force-based criterion.

        Args:
            normal_force: Force perpendicular to weld [N/mm]
            shear_force: Force parallel to weld [N/mm]
            weld_throat: Effective weld throat thickness [mm]
            weld_length: Effective weld length [mm]
            allowable_stress: Weld metal strength [MPa]
            safety_factor: Partial safety factor
        """
        weld_area = weld_throat * weld_length
        if weld_area <= 0:
            raise ValueError("Weld area must be positive.")

        # Combined stress in weld throat
        sigma_n = normal_force / weld_area
        tau = shear_force / weld_area
        equivalent = math.sqrt(sigma_n**2 + tau**2)

        allowable = allowable_stress / safety_factor
        utilization = equivalent / allowable if allowable > 0 else float("inf")

        return WeldFailureResult(
            equivalent_stress=equivalent,
            allowable_stress=allowable,
            utilization=utilization,
            status="PASS" if utilization < 1.0 else "FAIL",
            criterion="force_based",
        )

    @staticmethod
    def stress_based_check(
        sigma_perp: float,
        tau_perp: float,
        tau_parallel: float,
        fu: float,
        beta_w: float = 0.8,
        gamma_Mw: float = 1.25,
    ) -> WeldFailureResult:
        """
        Directional stress method per EN 1993-1-8.

        Criterion 1:
            sqrt(sigma_perp^2 + 3*(tau_perp^2 + tau_parallel^2)) <= fu/(beta_w*gamma_Mw)
        Criterion 2:
            sigma_perp <= 0.9 * fu / gamma_Mw
        """
        # Criterion 1: combined stress
        equiv = math.sqrt(
            sigma_perp**2 + 3.0 * (tau_perp**2 + tau_parallel**2)
        )
        allowable_1 = fu / (beta_w * gamma_Mw)

        # Criterion 2: normal stress
        allowable_2 = 0.9 * fu / gamma_Mw

        # Governing criterion
        util_1 = equiv / allowable_1 if allowable_1 > 0 else float("inf")
        util_2 = abs(sigma_perp) / allowable_2 if allowable_2 > 0 else float("inf")
        utilization = max(util_1, util_2)

        return WeldFailureResult(
            equivalent_stress=equiv,
            allowable_stress=allowable_1,
            utilization=utilization,
            status="PASS" if utilization < 1.0 else "FAIL",
            criterion="stress_based_EN1993",
        )
