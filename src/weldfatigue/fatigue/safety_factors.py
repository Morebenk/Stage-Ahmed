"""Partial safety factors for fatigue design per IIW, Eurocode 3, and DNV."""

import math


class PartialSafetyFactors:
    """
    Partial safety factors for fatigue assessment.

    IIW, Eurocode 3, and DNV each define partial factors for
    fatigue resistance (gamma_Mf) and fatigue loading (gamma_Ff).
    """

    # IIW gamma_Mf table (consequence_class, inspection_level) -> factor
    IIW_GAMMA_MF = {
        ("low", "periodic"): 1.00,
        ("low", "continuous"): 1.00,
        ("low", "none"): 1.00,
        ("normal", "periodic"): 1.15,
        ("normal", "continuous"): 1.00,
        ("normal", "none"): 1.25,
        ("high", "periodic"): 1.30,
        ("high", "continuous"): 1.15,
        ("high", "none"): 1.40,
    }

    # Eurocode 3 EN 1993-1-9 gamma_Mf values
    EC3_GAMMA_MF = {
        "low": 1.00,
        "normal": 1.15,
        "high": 1.35,
    }

    # DNV-RP-C203 Design Fatigue Factors
    DNV_DFF = {
        ("low", "periodic"): 1.0,
        ("low", "none"): 2.0,
        ("normal", "periodic"): 2.0,
        ("normal", "none"): 3.0,
        ("high", "periodic"): 3.0,
        ("high", "none"): 10.0,
    }

    # IIW gamma_Ff (load partial factor) per standard
    GAMMA_FF = {
        "iiw": 1.00,
        "eurocode3": 1.00,
        "dnv": 1.00,
    }

    @staticmethod
    def gamma_Mf(consequence: str, inspection: str, standard: str = "iiw") -> float:
        """
        Get material/resistance partial safety factor.

        Args:
            consequence: Consequence class (low, normal, high)
            inspection: Inspection level (none, periodic, continuous)
            standard: Design standard (iiw, eurocode3, dnv)
        """
        if standard == "iiw":
            return PartialSafetyFactors.IIW_GAMMA_MF.get(
                (consequence, inspection), 1.15
            )
        elif standard == "eurocode3":
            return PartialSafetyFactors.EC3_GAMMA_MF.get(consequence, 1.15)
        elif standard == "dnv":
            # DNV uses DFF instead of gamma_Mf
            return 1.0
        return 1.15

    @staticmethod
    def gamma_Ff(standard: str = "iiw") -> float:
        """Get load partial safety factor."""
        return PartialSafetyFactors.GAMMA_FF.get(standard, 1.0)

    @staticmethod
    def design_fatigue_factor(consequence: str, inspection: str = "periodic") -> float:
        """
        DNV Design Fatigue Factor (DFF).

        Applied directly to fatigue life: N_design = N_calculated / DFF.
        """
        return PartialSafetyFactors.DNV_DFF.get(
            (consequence, inspection), 2.0
        )

    @staticmethod
    def survival_probability_factor(probability: float = 0.977) -> float:
        """
        Shift from mean S-N curve to characteristic at given survival probability.

        IIW S-N curves are already at 97.7% survival (mean - 2*std_dev).
        For other probabilities, adjust using Gaussian z-factor.

        Standard deviation in log10(N) for welded joints: ~0.2 (IIW typical).
        """
        if probability <= 0.5:
            return 1.0  # Mean curve

        # z-values for common probabilities (one-sided)
        z_table = {
            0.500: 0.000,
            0.750: 0.674,
            0.900: 1.282,
            0.950: 1.645,
            0.975: 1.960,
            0.977: 2.000,  # IIW characteristic
            0.990: 2.326,
            0.999: 3.090,
        }

        # Find closest z-value or interpolate
        std_dev_log = 0.2  # Standard deviation in log10(N) for welded joints

        # Use inverse normal approximation for arbitrary probability
        # Abramowitz & Stegun approximation
        p = 1.0 - probability
        if p <= 0:
            return 0.5  # Very conservative
        t = math.sqrt(-2.0 * math.log(p))
        c0, c1, c2 = 2.515517, 0.802853, 0.010328
        d1, d2, d3 = 1.432788, 0.189269, 0.001308
        z = t - (c0 + c1 * t + c2 * t * t) / (1.0 + d1 * t + d2 * t * t + d3 * t * t * t)

        # IIW reference is at z=2.0 (97.7%).
        # Adjustment factor on stress: 10^(delta_z * std_dev_log / m)
        # where m is the S-N slope (typically 3)
        z_ref = 2.0
        delta_z = z - z_ref
        m = 3.0

        # Factor on FAT class (stress-based)
        factor = 10.0 ** (-delta_z * std_dev_log / m)
        return factor

    @staticmethod
    def apply_to_fat_class(
        fat_class: int,
        consequence: str = "normal",
        inspection: str = "periodic",
        standard: str = "iiw",
        survival_probability: float = 0.977,
    ) -> float:
        """
        Return reduced FAT class after applying all safety factors.

        FAT_design = FAT / (gamma_Mf * gamma_Ff) * sp_factor
        """
        g_mf = PartialSafetyFactors.gamma_Mf(consequence, inspection, standard)
        g_ff = PartialSafetyFactors.gamma_Ff(standard)
        sp = PartialSafetyFactors.survival_probability_factor(survival_probability)

        return fat_class * sp / (g_mf * g_ff)

    @staticmethod
    def compute_all(
        consequence: str = "normal",
        inspection: str = "periodic",
        standard: str = "iiw",
        survival_probability: float = 0.977,
    ) -> dict:
        """Compute all safety factors and return as dict."""
        g_mf = PartialSafetyFactors.gamma_Mf(consequence, inspection, standard)
        g_ff = PartialSafetyFactors.gamma_Ff(standard)
        dff = PartialSafetyFactors.design_fatigue_factor(consequence, inspection)
        sp = PartialSafetyFactors.survival_probability_factor(survival_probability)

        return {
            "gamma_Mf": g_mf,
            "gamma_Ff": g_ff,
            "dff": dff,
            "characteristic_factor": sp,
            "combined_factor": g_mf * g_ff / sp,
        }
