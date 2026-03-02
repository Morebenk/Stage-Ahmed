"""Multiaxial fatigue assessment methods for welded joints."""

import math
import numpy as np


class MultiaxialFatigueAssessment:
    """
    Multiaxial fatigue assessment per IIW recommendations.

    Methods:
    - Gough-Pollard interaction formula (IIW recommended, proportional loading)
    - Findley critical plane criterion (non-proportional loading)
    - Modified Wohler Curve Method (MWCM, universal)

    References:
    - IIW XIII-2572-15 (Multiaxial fatigue recommendations)
    - Susmel & Lazzarin (MWCM)
    """

    @staticmethod
    def detect_proportionality(
        normal_history: np.ndarray,
        shear_history: np.ndarray,
        threshold: float = 0.1,
    ) -> bool:
        """
        Detect proportional vs non-proportional loading.

        Proportional loading: shear/normal ratio remains constant.
        Checks coefficient of variation of the instantaneous ratio.

        Args:
            normal_history: Time series of normal stress [MPa]
            shear_history: Time series of shear stress [MPa]
            threshold: CV threshold below which loading is proportional

        Returns:
            True if loading is proportional
        """
        # Avoid division by zero
        mask = np.abs(normal_history) > 1e-10
        if not np.any(mask):
            return True

        ratios = shear_history[mask] / normal_history[mask]
        if len(ratios) < 2:
            return True

        # Sign change in ratio implies non-proportional loading
        if np.any(ratios > 0) and np.any(ratios < 0):
            return False

        mean_ratio = np.mean(ratios)
        if abs(mean_ratio) < 1e-10:
            return True

        cv = np.std(ratios) / abs(mean_ratio)
        return cv < threshold

    @staticmethod
    def gough_pollard(
        delta_sigma: float,
        delta_tau: float,
        fat_sigma: int,
        fat_tau: int,
        num_cycles: int,
    ) -> dict:
        """
        IIW Gough-Pollard interaction formula.

        For proportional (in-phase) loading:
            (delta_sigma / delta_sigma_R)^2 + (delta_tau / delta_tau_R)^2 <= 1

        where delta_sigma_R and delta_tau_R are the allowable stress ranges
        from the respective S-N curves at the given number of cycles.

        Args:
            delta_sigma: Normal stress range [MPa]
            delta_tau: Shear stress range [MPa]
            fat_sigma: FAT class for normal stress
            fat_tau: FAT class for shear stress
            num_cycles: Number of applied cycles

        Returns:
            dict with interaction_value, utilizations, status
        """
        # Allowable stress ranges at N cycles (from S-N curve: N = (FAT/dS)^3 * 2e6)
        # => dS_allowable = FAT * (2e6 / N)^(1/3)
        m = 3.0
        if num_cycles <= 0:
            delta_sigma_R = float("inf")
            delta_tau_R = float("inf")
        else:
            delta_sigma_R = fat_sigma * (2e6 / num_cycles) ** (1.0 / m)
            delta_tau_R = fat_tau * (2e6 / num_cycles) ** (1.0 / m)

        # Utilization ratios
        sigma_util = (delta_sigma / delta_sigma_R) ** 2 if delta_sigma_R > 0 else 0
        tau_util = (delta_tau / delta_tau_R) ** 2 if delta_tau_R > 0 else 0

        interaction = sigma_util + tau_util

        return {
            "interaction_value": interaction,
            "normal_utilization": math.sqrt(sigma_util),
            "shear_utilization": math.sqrt(tau_util),
            "is_proportional": True,
            "method": "gough_pollard",
            "status": "PASS" if interaction <= 1.0 else "FAIL",
        }

    @staticmethod
    def findley_critical_plane(
        sigma_a: float,
        tau_a: float,
        sigma_max: float,
        k: float = 0.3,
        fatigue_limit: float = 100.0,
    ) -> dict:
        """
        Findley critical plane criterion.

        Searches for the plane with maximum damage parameter:
            FP = tau_a + k * sigma_n_max

        For simplified 2D assessment (normal + shear):
            The critical plane is found by rotating through all angles.

        Args:
            sigma_a: Normal stress amplitude [MPa]
            tau_a: Shear stress amplitude [MPa]
            sigma_max: Maximum normal stress [MPa]
            k: Findley material parameter (typically 0.2-0.4 for welds)
            fatigue_limit: Fatigue limit for the Findley parameter [MPa]

        Returns:
            dict with findley_parameter, critical_angle, status
        """
        max_fp = 0.0
        critical_angle = 0.0

        # Search through all plane orientations (0 to 180 degrees)
        for angle_deg in range(0, 181):
            theta = math.radians(angle_deg)

            # Stress transformation to plane at angle theta
            # tau on plane: tau_theta = -sigma_a * sin(2*theta) / 2 + tau_a * cos(2*theta)
            # sigma_n on plane: sigma_n = sigma_a * cos^2(theta) + ...
            tau_theta_a = abs(
                -sigma_a * math.sin(2.0 * theta) / 2.0
                + tau_a * math.cos(2.0 * theta)
            )
            sigma_n_max = (
                sigma_max * math.cos(theta) ** 2
            )

            fp = tau_theta_a + k * sigma_n_max

            if fp > max_fp:
                max_fp = fp
                critical_angle = angle_deg

        utilization = max_fp / fatigue_limit if fatigue_limit > 0 else 0

        return {
            "findley_parameter": max_fp,
            "critical_angle_deg": critical_angle,
            "utilization": utilization,
            "method": "findley",
            "status": "PASS" if utilization <= 1.0 else "FAIL",
        }

    @staticmethod
    def mwcm(
        delta_sigma: float,
        delta_tau: float,
        fat_class: int,
        material_type: str = "steel",
    ) -> dict:
        """
        Modified Wohler Curve Method (Susmel & Lazzarin).

        Modifies the S-N curve slope based on the degree of multiaxiality:
            rho = tau_a / sigma_a (biaxiality ratio)

        The effective slope varies from m=3 (uniaxial) to m=5 (pure shear).

        Equivalent uniaxial stress range:
            delta_sigma_eq = delta_sigma * sqrt(1 + (delta_tau/delta_sigma)^2)

        Args:
            delta_sigma: Normal stress range [MPa]
            delta_tau: Shear stress range [MPa]
            fat_class: FAT class for assessment
            material_type: steel or aluminum

        Returns:
            dict with equivalent_range, modified_slope, status
        """
        if delta_sigma <= 0:
            # Pure shear case
            delta_sigma_eq = delta_tau * math.sqrt(3)  # Von Mises
            rho = float("inf")
            m_eff = 5.0
        else:
            rho = delta_tau / delta_sigma

            # Equivalent stress range (energy-based)
            delta_sigma_eq = math.sqrt(delta_sigma ** 2 + 3.0 * delta_tau ** 2)

            # Modified slope: interpolate between m=3 (rho=0) and m=5 (rho=inf)
            m_eff = 3.0 + 2.0 * min(rho, 1.0)  # Cap at rho=1

        # Allowable range from FAT class at 2e6 cycles
        allowable = fat_class  # FAT class IS the allowable at 2e6

        utilization = delta_sigma_eq / allowable

        return {
            "equivalent_stress_range": delta_sigma_eq,
            "biaxiality_ratio": rho if rho != float("inf") else 999.0,
            "modified_slope": m_eff,
            "utilization": utilization,
            "method": "mwcm",
            "status": "PASS" if utilization <= 1.0 else "FAIL",
        }

    @staticmethod
    def evaluate(
        method: str,
        delta_sigma: float,
        delta_tau: float,
        fat_sigma: int,
        fat_tau: int = 0,
        num_cycles: int = 2_000_000,
        **kwargs,
    ) -> dict:
        """
        Dispatch to appropriate multiaxial method.

        Args:
            method: gough_pollard, findley, or mwcm
            delta_sigma: Normal stress range [MPa]
            delta_tau: Shear stress range [MPa]
            fat_sigma: FAT class for normal stress
            fat_tau: FAT class for shear stress (for Gough-Pollard)
            num_cycles: Number of cycles
        """
        if method == "gough_pollard":
            if fat_tau <= 0:
                fat_tau = int(fat_sigma * 0.58)  # ~FAT/sqrt(3) for shear
            return MultiaxialFatigueAssessment.gough_pollard(
                delta_sigma, delta_tau, fat_sigma, fat_tau, num_cycles
            )
        elif method == "findley":
            sigma_a = delta_sigma / 2.0
            tau_a = delta_tau / 2.0
            sigma_max = kwargs.get("sigma_max", sigma_a)
            k = kwargs.get("k", 0.3)
            fatigue_limit = kwargs.get("fatigue_limit", fat_sigma / 2.0)
            return MultiaxialFatigueAssessment.findley_critical_plane(
                sigma_a, tau_a, sigma_max, k, fatigue_limit
            )
        elif method == "mwcm":
            return MultiaxialFatigueAssessment.mwcm(
                delta_sigma, delta_tau, fat_sigma, kwargs.get("material_type", "steel")
            )
        else:
            raise ValueError(f"Unknown multiaxial method: {method}")
