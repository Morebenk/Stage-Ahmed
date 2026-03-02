"""BS 7608:2014 S-N curve implementation."""

import math
import numpy as np


class BS7608Curve:
    """
    BS 7608:2014 S-N curve for fatigue design of steel products.

    Detail classes: B, C, D, E, F, F2, G, W1
    Each has specific S-N slope and reference stress at 2e6 cycles.

    Reference: BS 7608:2014+A1:2015
    """

    DETAIL_CLASSES = {
        "B":  {"m": 4.0, "S_ref": 100.0, "N_ref": 2e6, "cutoff": 1e8},
        "C":  {"m": 3.5, "S_ref": 78.0,  "N_ref": 2e6, "cutoff": 1e8},
        "D":  {"m": 3.0, "S_ref": 53.0,  "N_ref": 2e6, "cutoff": 1e8},
        "E":  {"m": 3.0, "S_ref": 47.0,  "N_ref": 2e6, "cutoff": 1e8},
        "F":  {"m": 3.0, "S_ref": 40.0,  "N_ref": 2e6, "cutoff": 1e8},
        "F2": {"m": 3.0, "S_ref": 35.0,  "N_ref": 2e6, "cutoff": 1e8},
        "G":  {"m": 3.0, "S_ref": 29.0,  "N_ref": 2e6, "cutoff": 1e8},
        "W1": {"m": 3.0, "S_ref": 25.0,  "N_ref": 2e6, "cutoff": 1e8},
    }

    def __init__(self, detail_class: str, variable_amplitude: bool = False):
        if detail_class not in self.DETAIL_CLASSES:
            raise ValueError(
                f"Unknown BS 7608 class: {detail_class}. "
                f"Valid: {list(self.DETAIL_CLASSES.keys())}"
            )
        params = self.DETAIL_CLASSES[detail_class]
        self.detail_class = detail_class
        self.m = params["m"]
        self.S_ref = params["S_ref"]
        self.N_ref = params["N_ref"]
        self.cutoff = params["cutoff"]
        self.variable_amplitude = variable_amplitude

    def cycles_to_failure(self, stress_range: float) -> float:
        """Compute allowable cycles N for given stress range."""
        if stress_range <= 0:
            return float("inf")

        N = ((self.S_ref / stress_range) ** self.m) * self.N_ref

        if not self.variable_amplitude and N > self.cutoff:
            return float("inf")

        return N

    def stress_range_at_cycles(self, N: float) -> float:
        """Compute allowable stress range for target cycle count."""
        if N <= 0:
            return float("inf")
        if not self.variable_amplitude and N > self.cutoff:
            return 0.0
        return self.S_ref * (self.N_ref / N) ** (1.0 / self.m)

    def get_curve_points(
        self, N_min: float = 1e3, N_max: float = 1e9, n_points: int = 200
    ) -> tuple[np.ndarray, np.ndarray]:
        """Generate (N, stress_range) arrays for plotting."""
        N_values = np.logspace(math.log10(N_min), math.log10(N_max), n_points)
        stress_values = np.array([self.stress_range_at_cycles(N) for N in N_values])
        return N_values, stress_values
