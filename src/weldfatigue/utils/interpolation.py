"""Log-log interpolation utilities for S-N curves."""

import math

import numpy as np


def log_log_interpolate(
    x: float, x1: float, y1: float, x2: float, y2: float
) -> float:
    """Linear interpolation in log-log space."""
    if x <= 0 or x1 <= 0 or x2 <= 0 or y1 <= 0 or y2 <= 0:
        raise ValueError("All values must be positive for log-log interpolation.")
    log_x = math.log10(x)
    log_x1 = math.log10(x1)
    log_x2 = math.log10(x2)
    log_y1 = math.log10(y1)
    log_y2 = math.log10(y2)

    log_y = log_y1 + (log_y2 - log_y1) * (log_x - log_x1) / (log_x2 - log_x1)
    return 10**log_y


def log_log_slope(x1: float, y1: float, x2: float, y2: float) -> float:
    """Compute slope in log-log space."""
    return (math.log10(y2) - math.log10(y1)) / (math.log10(x2) - math.log10(x1))
