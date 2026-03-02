"""Eurocode 3 EN 1993-1-9 S-N curve implementation."""

import math
import numpy as np


class Eurocode3Curve:
    """
    EN 1993-1-9 S-N curve for fatigue design of steel structures.

    Key differences from IIW:
    - Knee point (constant amplitude fatigue limit) at 5e6 cycles
    - Cut-off at 1e8 cycles (not 1e9)
    - Same FAT class notation as IIW

    Reference: EN 1993-1-9:2005+A1:2009
    """

    M1 = 3.0
    M2 = 5.0
    KNEE_CYCLES = 5e6      # Constant amplitude fatigue limit
    CUTOFF_CYCLES = 1e8    # Cut-off for variable amplitude
    N_REF = 2e6            # Reference cycle count

    def __init__(self, fat_class: int, variable_amplitude: bool = False):
        self.fat_class = fat_class
        self.variable_amplitude = variable_amplitude

        # Stress at knee point
        self.delta_sigma_knee = fat_class * (self.N_REF / self.KNEE_CYCLES) ** (1.0 / self.M1)

        # Stress at cut-off
        self.delta_sigma_cutoff = self.delta_sigma_knee * (
            self.KNEE_CYCLES / self.CUTOFF_CYCLES
        ) ** (1.0 / self.M2)

    def cycles_to_failure(self, stress_range: float) -> float:
        """Compute allowable cycles for given stress range."""
        if stress_range <= 0:
            return float("inf")

        if stress_range >= self.delta_sigma_knee:
            # Region 1: slope m1 = 3
            N = ((self.fat_class / stress_range) ** self.M1) * self.N_REF
        elif self.variable_amplitude:
            # Region 2: slope m2 = 5
            if stress_range <= self.delta_sigma_cutoff:
                return float("inf")
            N = self.KNEE_CYCLES * (self.delta_sigma_knee / stress_range) ** self.M2
        else:
            # Constant amplitude: below knee = infinite life
            return float("inf")

        return N

    def stress_range_at_cycles(self, N: float) -> float:
        """Compute allowable stress range for target cycle count."""
        if N <= 0:
            return float("inf")
        if N <= self.KNEE_CYCLES:
            return self.fat_class * (self.N_REF / N) ** (1.0 / self.M1)
        if self.variable_amplitude and N <= self.CUTOFF_CYCLES:
            return self.delta_sigma_knee * (self.KNEE_CYCLES / N) ** (1.0 / self.M2)
        return 0.0

    def get_curve_points(
        self, N_min: float = 1e3, N_max: float = 1e9, n_points: int = 200
    ) -> tuple[np.ndarray, np.ndarray]:
        N_values = np.logspace(math.log10(N_min), math.log10(N_max), n_points)
        stress_values = np.array([self.stress_range_at_cycles(N) for N in N_values])
        return N_values, stress_values
