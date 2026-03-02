"""Eurocode 9 EN 1999-1-3 S-N curve for aluminum structures."""

import math
import numpy as np


class Eurocode9Curve:
    """
    EN 1999-1-3 S-N curve for fatigue design of aluminum structures.

    Key differences from IIW aluminum curves:
    - Slope m1 varies by detail category (3.4 to 4.3)
    - Knee point at 5e6 cycles
    - Cut-off at 1e8 cycles

    Reference: EN 1999-1-3:2007+A1:2011
    """

    M2 = 5.4             # Second slope (after knee)
    KNEE_CYCLES = 5e6
    CUTOFF_CYCLES = 1e8
    N_REF = 2e6

    # FAT classes with detail-specific m1 slopes
    DETAIL_SLOPES = {
        71: 3.4,
        63: 3.4,
        56: 3.4,
        50: 3.4,
        45: 3.4,
        40: 3.4,
        36: 3.4,
        32: 4.3,  # Some details have different slopes
        28: 4.3,
        25: 4.3,
    }

    def __init__(self, fat_class: int, variable_amplitude: bool = False):
        self.fat_class = fat_class
        self.variable_amplitude = variable_amplitude
        self.m1 = self.DETAIL_SLOPES.get(fat_class, 3.4)

        self.delta_sigma_knee = fat_class * (self.N_REF / self.KNEE_CYCLES) ** (1.0 / self.m1)
        self.delta_sigma_cutoff = self.delta_sigma_knee * (
            self.KNEE_CYCLES / self.CUTOFF_CYCLES
        ) ** (1.0 / self.M2)

    def cycles_to_failure(self, stress_range: float) -> float:
        if stress_range <= 0:
            return float("inf")

        if stress_range >= self.delta_sigma_knee:
            N = ((self.fat_class / stress_range) ** self.m1) * self.N_REF
        elif self.variable_amplitude:
            if stress_range <= self.delta_sigma_cutoff:
                return float("inf")
            N = self.KNEE_CYCLES * (self.delta_sigma_knee / stress_range) ** self.M2
        else:
            return float("inf")

        return N

    def stress_range_at_cycles(self, N: float) -> float:
        if N <= 0:
            return float("inf")
        if N <= self.KNEE_CYCLES:
            return self.fat_class * (self.N_REF / N) ** (1.0 / self.m1)
        if self.variable_amplitude and N <= self.CUTOFF_CYCLES:
            return self.delta_sigma_knee * (self.KNEE_CYCLES / N) ** (1.0 / self.M2)
        return 0.0

    def get_curve_points(
        self, N_min: float = 1e3, N_max: float = 1e9, n_points: int = 200
    ) -> tuple[np.ndarray, np.ndarray]:
        N_values = np.logspace(math.log10(N_min), math.log10(N_max), n_points)
        stress_values = np.array([self.stress_range_at_cycles(N) for N in N_values])
        return N_values, stress_values
