"""Rainflow cycle counting per ASTM E1049-85."""

import numpy as np


def _find_reversals(signal: np.ndarray) -> np.ndarray:
    """Extract peaks and valleys from a signal."""
    if len(signal) < 3:
        return signal.copy()

    reversals = [signal[0]]
    for i in range(1, len(signal) - 1):
        if (signal[i] - signal[i - 1]) * (signal[i + 1] - signal[i]) < 0:
            reversals.append(signal[i])
    reversals.append(signal[-1])
    return np.array(reversals)


def rainflow_count(signal: np.ndarray) -> list[tuple[float, float, float]]:
    """
    Rainflow cycle counting per ASTM E1049-85.

    Args:
        signal: 1D array of stress or strain values over time.

    Returns:
        List of (stress_range, mean_stress, count) tuples.
        Half-cycles have count=0.5, full cycles have count=1.0.
    """
    reversals = _find_reversals(signal)
    cycles = []
    stack = []

    for point in reversals:
        stack.append(point)
        while len(stack) >= 4:
            S0 = abs(stack[-2] - stack[-1])  # current range
            S1 = abs(stack[-3] - stack[-2])  # previous range

            if S0 < S1:
                break

            # Extract a full cycle
            mean = (stack[-3] + stack[-2]) / 2.0
            cycles.append((S1, mean, 1.0))
            # Remove the two middle points
            stack.pop(-2)
            stack.pop(-2)

    # Remaining stack forms half-cycles
    for i in range(len(stack) - 1):
        rng = abs(stack[i + 1] - stack[i])
        mean = (stack[i + 1] + stack[i]) / 2.0
        cycles.append((rng, mean, 0.5))

    return cycles


def signal_to_spectrum(
    signal: np.ndarray, n_bins: int = 64
) -> list[tuple[float, int]]:
    """
    Convert a time signal to a load spectrum via rainflow counting and binning.

    Returns:
        List of (stress_range, num_cycles) sorted by descending range.
    """
    cycles = rainflow_count(signal)
    if not cycles:
        return []

    ranges = [c[0] for c in cycles]
    counts = [c[2] for c in cycles]

    max_range = max(ranges)
    if max_range == 0:
        return []

    bin_width = max_range / n_bins
    spectrum = {}

    for rng, count in zip(ranges, counts):
        bin_idx = min(int(rng / bin_width), n_bins - 1)
        bin_center = (bin_idx + 0.5) * bin_width
        if bin_center not in spectrum:
            spectrum[bin_center] = 0.0
        spectrum[bin_center] += count

    result = [(rng, int(round(cnt))) for rng, cnt in spectrum.items() if cnt > 0]
    result.sort(key=lambda x: x[0], reverse=True)
    return result
