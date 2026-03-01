"""Mean stress correction methods for fatigue assessment."""

import numpy as np


class MeanStressCorrection:
    """
    Mean stress correction methods.

    Under non-zero mean stress, the allowable stress range changes.
    IIW recommends corrections for R-ratios other than R=0.5.
    """

    @staticmethod
    def goodman(stress_amplitude: float, mean_stress: float, ultimate_strength: float) -> float:
        """
        Goodman correction (linear).
        Sa_eq = Sa / (1 - Sm/Su)
        """
        if mean_stress >= ultimate_strength:
            return float("inf")
        if mean_stress <= 0:
            return stress_amplitude
        return stress_amplitude / (1.0 - mean_stress / ultimate_strength)

    @staticmethod
    def gerber(stress_amplitude: float, mean_stress: float, ultimate_strength: float) -> float:
        """
        Gerber correction (parabolic).
        Sa_eq = Sa / (1 - (Sm/Su)^2)
        """
        if abs(mean_stress) >= ultimate_strength:
            return float("inf")
        ratio = (mean_stress / ultimate_strength) ** 2
        return stress_amplitude / (1.0 - ratio)

    @staticmethod
    def soderberg(stress_amplitude: float, mean_stress: float, yield_strength: float) -> float:
        """
        Soderberg correction (conservative, uses yield).
        Sa_eq = Sa / (1 - Sm/Sy)
        """
        if mean_stress >= yield_strength:
            return float("inf")
        if mean_stress <= 0:
            return stress_amplitude
        return stress_amplitude / (1.0 - mean_stress / yield_strength)

    @staticmethod
    def iiw_enhancement_factor(R: float, stress_relieved: bool = False) -> float:
        """
        IIW mean stress enhancement factor f(R).

        For as-welded joints with high residual stress:
            f(R) = 1.0 for all R (no benefit)

        For stress-relieved joints:
            f(R) = 1.6              for R < -1
            f(R) = -0.4*R + 1.2    for -1 <= R <= 0.5
            f(R) = 1.0             for R > 0.5
        """
        if not stress_relieved:
            return 1.0

        if R < -1:
            return 1.6
        elif R <= 0.5:
            return -0.4 * R + 1.2
        else:
            return 1.0

    @staticmethod
    def stress_ratio_from_range_and_mean(stress_range: float, mean_stress: float) -> float:
        """Compute R-ratio from stress range and mean stress."""
        sigma_max = mean_stress + stress_range / 2
        sigma_min = mean_stress - stress_range / 2
        if sigma_max == 0:
            return float("-inf")
        return sigma_min / sigma_max

    @staticmethod
    def haigh_diagram_points(
        Se: float,
        Su: float,
        method: str = "goodman",
        n_points: int = 50,
    ) -> tuple[np.ndarray, np.ndarray]:
        """Generate (mean_stress, amplitude) points for plotting a Haigh diagram."""
        mean_values = np.linspace(0, Su * 0.95, n_points)
        amp_values = np.zeros(n_points)

        for i, sm in enumerate(mean_values):
            if method == "goodman":
                amp_values[i] = Se * (1.0 - sm / Su)
            elif method == "gerber":
                amp_values[i] = Se * (1.0 - (sm / Su) ** 2)
            elif method == "soderberg":
                # Use Su as proxy for Sy (would need actual Sy)
                amp_values[i] = Se * (1.0 - sm / (Su * 0.7))
                amp_values[i] = max(0, amp_values[i])

        return mean_values, amp_values
