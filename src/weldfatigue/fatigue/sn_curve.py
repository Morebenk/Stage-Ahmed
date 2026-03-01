"""IIW S-N (Woehler) curve implementation."""

import math
import numpy as np


class SNConfiguration:
    """IIW S-N curve parameters."""

    # Standard IIW slopes for steel welded joints
    STEEL_M1 = 3.0
    STEEL_M2 = 5.0
    STEEL_KNEE_CYCLES = 1e7
    STEEL_CUTOFF_CYCLES = 1e9

    # IIW slopes for aluminum welded joints
    ALUMINUM_M1 = 3.376
    ALUMINUM_M2 = 5.376
    ALUMINUM_KNEE_CYCLES = 1e7
    ALUMINUM_CUTOFF_CYCLES = 1e9


class SNCurve:
    """
    IIW S-N (Woehler) curve.

    The S-N curve is defined as:
        N = (FAT / delta_sigma)^m * 2e6

    For steel:
        - m = 3 for N <= 1e7
        - m = 5 for 1e7 < N <= 1e9 (variable amplitude)
        - Infinite life beyond cut-off

    For constant amplitude, the curve is horizontal (endurance limit)
    after the knee point at 1e7 cycles.
    """

    def __init__(
        self,
        fat_class: int,
        material_type: str = "steel",
        variable_amplitude: bool = False,
    ):
        self.fat_class = fat_class
        self.material_type = material_type
        self.variable_amplitude = variable_amplitude
        self._setup_parameters()

    def _setup_parameters(self):
        if self.material_type == "steel":
            self.m1 = SNConfiguration.STEEL_M1
            self.m2 = SNConfiguration.STEEL_M2
            self.N_knee = SNConfiguration.STEEL_KNEE_CYCLES
            self.N_cutoff = SNConfiguration.STEEL_CUTOFF_CYCLES
        elif self.material_type == "aluminum":
            self.m1 = SNConfiguration.ALUMINUM_M1
            self.m2 = SNConfiguration.ALUMINUM_M2
            self.N_knee = SNConfiguration.ALUMINUM_KNEE_CYCLES
            self.N_cutoff = SNConfiguration.ALUMINUM_CUTOFF_CYCLES
        else:
            raise ValueError(f"Unknown material type: {self.material_type}")

        # Stress range at knee point
        # N_knee = (FAT / delta_sigma_knee)^m1 * 2e6
        # => delta_sigma_knee = FAT * (2e6 / N_knee)^(1/m1)
        self.delta_sigma_knee = self.fat_class * (2e6 / self.N_knee) ** (1.0 / self.m1)

        # Cut-off stress (only relevant for variable amplitude)
        self.delta_sigma_cutoff = self.delta_sigma_knee * (
            self.N_knee / self.N_cutoff
        ) ** (1.0 / self.m2)

    def cycles_to_failure(self, stress_range: float) -> float:
        """
        Compute allowable cycles N for a given stress range.
        Returns float('inf') if below endurance limit.
        """
        if stress_range <= 0:
            return float("inf")

        if stress_range >= self.delta_sigma_knee:
            # Region 1: slope m1
            N = ((self.fat_class / stress_range) ** self.m1) * 2e6
        elif self.variable_amplitude:
            # Region 2: slope m2 (only for variable amplitude)
            if stress_range <= self.delta_sigma_cutoff:
                return float("inf")
            N = self.N_knee * (self.delta_sigma_knee / stress_range) ** self.m2
        else:
            # Constant amplitude: below knee point = infinite life
            return float("inf")

        return N

    def stress_range_at_cycles(self, N: float) -> float:
        """Compute the allowable stress range for a target number of cycles."""
        if N <= 0:
            return float("inf")
        if N <= 2e6:
            return self.fat_class * (2e6 / N) ** (1.0 / self.m1)
        if N <= self.N_knee:
            return self.fat_class * (2e6 / N) ** (1.0 / self.m1)
        if self.variable_amplitude and N <= self.N_cutoff:
            return self.delta_sigma_knee * (self.N_knee / N) ** (1.0 / self.m2)
        return 0.0

    def get_curve_points(
        self, N_min: float = 1e3, N_max: float = 1e9, n_points: int = 200
    ) -> tuple[np.ndarray, np.ndarray]:
        """Generate (N, stress_range) arrays for plotting."""
        N_values = np.logspace(math.log10(N_min), math.log10(N_max), n_points)
        stress_values = np.array([self.stress_range_at_cycles(N) for N in N_values])
        return N_values, stress_values
