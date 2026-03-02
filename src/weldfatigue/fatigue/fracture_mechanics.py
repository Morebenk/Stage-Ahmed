"""Linear Elastic Fracture Mechanics (LEFM) fatigue crack growth assessment."""

import math
import numpy as np


class FractureMechanicsAssessment:
    """
    LEFM-based fatigue crack growth assessment (4th IIW method).

    Implements Paris law crack propagation: da/dN = C * (delta_K)^m

    References:
    - IIW XIII-1823-07 Section 6 (Fracture Mechanics)
    - BS 7910:2019 (Guide to methods for assessing flaws)
    """

    # Default Paris law parameters (units: mm, MPa, cycles)
    # da/dN in mm/cycle, delta_K in MPa*sqrt(mm)
    PARIS_DEFAULTS = {
        ("steel", "air"): {"C": 5.21e-13, "m": 3.0},
        ("steel", "seawater"): {"C": 1.30e-12, "m": 3.0},
        ("aluminum", "air"): {"C": 1.59e-11, "m": 3.06},
    }

    # Threshold stress intensity factor range [MPa*sqrt(mm)]
    DELTA_K_TH = {
        "steel": 63.0,     # ~2.0 MPa*sqrt(m) converted to MPa*sqrt(mm)
        "aluminum": 30.0,  # ~1.0 MPa*sqrt(m)
    }

    @staticmethod
    def stress_intensity_factor(
        stress: float,
        crack_size: float,
        Y: float = 1.0,
        Mk: float = 1.0,
    ) -> float:
        """
        Compute stress intensity factor K.

        K = Y * Mk * sigma * sqrt(pi * a)

        Args:
            stress: Applied stress [MPa]
            crack_size: Crack depth a [mm]
            Y: Geometry correction factor
            Mk: Weld magnification factor

        Returns:
            Stress intensity factor K [MPa*sqrt(mm)]
        """
        if crack_size <= 0:
            return 0.0
        return Y * Mk * stress * math.sqrt(math.pi * crack_size)

    @staticmethod
    def geometry_factor_Y(a: float, t: float, geometry: str = "edge") -> float:
        """
        Geometry correction factor Y(a/t).

        Simplified polynomial fit for common geometries:
        - Edge crack in plate: Y = 1.12 - 0.23*(a/t) + 10.55*(a/t)^2 - ...
        - Through crack: Y = 1.0 (no correction)
        - Semi-elliptical surface crack: Y = 1.12 / sqrt(Q)

        Uses BS 7910 Annex M simplified factors.
        """
        if t <= 0:
            return 1.0

        ratio = a / t
        ratio = min(ratio, 0.9)  # Limit validity range

        if geometry == "edge":
            # Newman-Raju edge crack approximation
            Y = 1.12 - 0.231 * ratio + 10.55 * ratio ** 2 - 21.71 * ratio ** 3 + 30.38 * ratio ** 4
            return Y
        elif geometry == "through":
            return 1.0
        elif geometry == "surface":
            # Semi-elliptical surface crack (aspect ratio c/a = 2)
            Q = 1.0 + 1.464 * (ratio) ** 1.65  # Flaw shape parameter
            return 1.12 / math.sqrt(Q)
        else:
            return 1.12  # Conservative default

    @staticmethod
    def Mk_factor(a: float, t: float, weld_geometry: str = "t_butt") -> float:
        """
        Weld toe magnification factor Mk.

        Accounts for the stress concentration effect of the weld geometry
        on the crack-tip stress field.

        Simplified fit from BS 7910 / IIW:
            Mk = C1 * (a/t)^C2

        where C1, C2 depend on weld geometry.
        """
        if t <= 0 or a <= 0:
            return 1.0

        ratio = a / t

        # Coefficients from BS 7910 Table M.1 (simplified)
        mk_params = {
            "t_butt": {"C1": 0.51, "C2": -0.31},
            "cruciform": {"C1": 0.50, "C2": -0.29},
            "lap": {"C1": 0.45, "C2": -0.25},
            "fillet": {"C1": 0.48, "C2": -0.30},
        }

        params = mk_params.get(weld_geometry, {"C1": 0.50, "C2": -0.30})
        Mk = params["C1"] * ratio ** params["C2"]

        return max(1.0, Mk)  # Mk >= 1.0

    @staticmethod
    def paris_law_rate(
        delta_K: float,
        C: float = 5.21e-13,
        m: float = 3.0,
        delta_K_th: float = 0.0,
    ) -> float:
        """
        Paris law crack growth rate.

        da/dN = C * (delta_K - delta_K_th)^m

        Returns:
            Crack growth rate da/dN [mm/cycle]
        """
        effective_dK = delta_K - delta_K_th
        if effective_dK <= 0:
            return 0.0
        return C * effective_dK ** m

    def integrate_crack_growth(
        self,
        initial_crack: float,
        critical_crack: float,
        stress_range: float,
        plate_thickness: float,
        weld_geometry: str = "t_butt",
        C: float = 5.21e-13,
        m: float = 3.0,
        delta_K_th: float = 0.0,
        num_steps: int = 500,
    ) -> dict:
        """
        Numerical integration of crack growth from a0 to a_c.

        Uses Euler forward integration with adaptive stepping.

        Returns:
            dict with total_cycles, crack_sizes, cycle_counts, etc.
        """
        a = initial_crack
        N_total = 0.0
        crack_sizes = [a]
        cycle_counts = [0.0]

        da_step = (critical_crack - initial_crack) / num_steps

        for _ in range(num_steps):
            if a >= critical_crack:
                break

            # Compute SIF at current crack size
            Y = self.geometry_factor_Y(a, plate_thickness)
            Mk = self.Mk_factor(a, plate_thickness, weld_geometry)
            delta_K = self.stress_intensity_factor(stress_range, a, Y, Mk)

            # Growth rate
            dadN = self.paris_law_rate(delta_K, C, m, delta_K_th)

            if dadN <= 0:
                # Below threshold: no growth
                break

            # Cycles for this increment
            dN = da_step / dadN
            N_total += dN
            a += da_step

            crack_sizes.append(a)
            cycle_counts.append(N_total)

        # Initial and final delta_K
        Y0 = self.geometry_factor_Y(initial_crack, plate_thickness)
        Mk0 = self.Mk_factor(initial_crack, plate_thickness, weld_geometry)
        dK_initial = self.stress_intensity_factor(stress_range, initial_crack, Y0, Mk0)

        Yf = self.geometry_factor_Y(a, plate_thickness)
        Mkf = self.Mk_factor(a, plate_thickness, weld_geometry)
        dK_final = self.stress_intensity_factor(stress_range, a, Yf, Mkf)

        return {
            "total_cycles": N_total,
            "crack_sizes": crack_sizes,
            "cycle_counts": cycle_counts,
            "delta_K_initial": dK_initial,
            "delta_K_final": dK_final,
            "status": "COMPLETE" if a >= critical_crack else "ARRESTED",
        }

    def two_phase_model(
        self,
        initiation_cycles: float,
        initial_crack: float,
        critical_crack: float,
        stress_range: float,
        plate_thickness: float,
        **kwargs,
    ) -> dict:
        """
        Combined initiation + propagation life model.

        N_total = N_initiation + N_propagation
        """
        prop_result = self.integrate_crack_growth(
            initial_crack, critical_crack, stress_range,
            plate_thickness, **kwargs,
        )

        return {
            "initiation_cycles": initiation_cycles,
            "propagation_cycles": prop_result["total_cycles"],
            "total_cycles": initiation_cycles + prop_result["total_cycles"],
            "crack_growth": prop_result,
        }

    @staticmethod
    def get_paris_parameters(
        material_type: str = "steel",
        environment: str = "air",
    ) -> dict:
        """Get default Paris law parameters for material/environment."""
        return FractureMechanicsAssessment.PARIS_DEFAULTS.get(
            (material_type, environment),
            {"C": 5.21e-13, "m": 3.0},
        )
