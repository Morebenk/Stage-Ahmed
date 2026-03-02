"""Residual stress modeling for welded joints."""

import math


class ResidualStressModel:
    """
    Simplified analytical residual stress estimation for welded joints.

    Provides residual stress estimation, relaxation modeling,
    and integration with mean stress correction.

    References:
    - IIW XIII-1823-07 (Residual stress assumptions)
    - Maddox (1991) Fatigue Strength of Welded Structures
    """

    @staticmethod
    def as_welded_peak(yield_strength: float) -> float:
        """
        Peak residual stress at weld toe in as-welded condition.

        Conservative IIW assumption: sigma_res = yield strength.
        """
        return yield_strength

    @staticmethod
    def pwht_relief_factor(
        temperature_celsius: float, hold_time_hours: float
    ) -> float:
        """
        Post-Weld Heat Treatment stress relief factor.

        Returns factor (0 to 1) representing remaining fraction of
        original residual stress after PWHT.

        Typical:
            550°C, 1h => ~70% relief (factor = 0.30)
            600°C, 1h => ~80% relief (factor = 0.20)
            620°C, 2h => ~90% relief (factor = 0.10)

        Simplified model: factor = max(0.05, exp(-k * T * sqrt(t)))
        """
        if temperature_celsius <= 200 or hold_time_hours <= 0:
            return 1.0  # No effective relief

        # Larson-Miller type parameter, simplified
        k = 0.004  # Empirical constant
        temp_eff = temperature_celsius - 200.0  # Effective temperature above threshold
        t_eff = math.sqrt(hold_time_hours)

        factor = math.exp(-k * temp_eff * t_eff)
        return max(0.05, min(1.0, factor))

    @staticmethod
    def residual_after_pwht(
        yield_strength: float,
        temperature_celsius: float = 0.0,
        hold_time_hours: float = 0.0,
    ) -> float:
        """
        Residual stress after optional PWHT.

        Returns:
            Remaining residual stress [MPa]
        """
        sigma_res = ResidualStressModel.as_welded_peak(yield_strength)
        if temperature_celsius > 200 and hold_time_hours > 0:
            factor = ResidualStressModel.pwht_relief_factor(
                temperature_celsius, hold_time_hours
            )
            sigma_res *= factor
        return sigma_res

    @staticmethod
    def relaxation_under_cycling(
        sigma_res_initial: float,
        stress_range: float,
        yield_strength: float,
        num_cycles: int = 1,
    ) -> float:
        """
        Residual stress relaxation due to cyclic loading.

        First-cycle plasticity: if (sigma_res + sigma_max) > yield,
        the residual stress reduces to (yield - sigma_max).

        Further relaxation occurs logarithmically with cycles:
            sigma_res(N) = sigma_res(1) * (1 - 0.1 * log10(N))

        Args:
            sigma_res_initial: Initial residual stress [MPa]
            stress_range: Applied stress range [MPa]
            yield_strength: Material yield strength [MPa]
            num_cycles: Number of loading cycles

        Returns:
            Relaxed residual stress [MPa]
        """
        sigma_max = stress_range / 2.0  # Assuming R=0

        # First-cycle plasticity (shakedown)
        if sigma_res_initial + sigma_max > yield_strength:
            sigma_res = yield_strength - sigma_max
        else:
            sigma_res = sigma_res_initial

        sigma_res = max(0.0, sigma_res)

        # Logarithmic relaxation with cycling
        if num_cycles > 1 and sigma_res > 0:
            relaxation = 1.0 - 0.1 * math.log10(num_cycles)
            sigma_res *= max(0.1, relaxation)

        return max(0.0, sigma_res)

    @staticmethod
    def effective_stress_ratio(
        stress_range: float,
        mean_stress: float,
        residual_stress: float,
    ) -> float:
        """
        Effective R-ratio including residual stress.

        R_eff = (sigma_min + sigma_res) / (sigma_max + sigma_res)
        """
        sigma_max = mean_stress + stress_range / 2.0
        sigma_min = mean_stress - stress_range / 2.0

        denominator = sigma_max + residual_stress
        if abs(denominator) < 1e-10:
            return 0.0

        return (sigma_min + residual_stress) / denominator

    @staticmethod
    def effective_mean_stress(
        mean_stress: float, residual_stress: float
    ) -> float:
        """
        Effective mean stress with residual stress superposition.

        sigma_m_eff = sigma_m + sigma_res
        """
        return mean_stress + residual_stress

    @staticmethod
    def superpose_on_applied(
        stress_range: float,
        mean_stress: float,
        residual_stress: float,
    ) -> tuple[float, float]:
        """
        Return (effective_range, effective_mean) with residual stress.

        The stress range itself is unchanged by residual stress
        (it shifts both min and max equally). The mean stress shifts.
        """
        effective_mean = mean_stress + residual_stress
        return stress_range, effective_mean

    @staticmethod
    def through_thickness_distribution(
        yield_strength: float,
        thickness: float,
        n_points: int = 20,
    ) -> tuple[list[float], list[float]]:
        """
        Simplified through-thickness residual stress distribution.

        Self-equilibrating profile: tension at surfaces, compression
        in the middle. Integral must equal zero.

        Returns:
            (depth_array, stress_array) both as lists
        """
        depths = []
        stresses = []

        for i in range(n_points):
            z = i * thickness / (n_points - 1)
            # Normalized position: -1 at surface, +1 at mid-thickness, -1 at far surface
            x = 2.0 * z / thickness - 1.0
            # Cosine distribution (self-equilibrating)
            # Tension at surfaces (weld location), compression at mid-thickness
            sigma = -yield_strength * math.cos(math.pi * x)
            depths.append(z)
            stresses.append(sigma)

        return depths, stresses
