"""Unit conversion helpers."""

import math


def mpa_to_ksi(mpa: float) -> float:
    return mpa * 0.145038


def ksi_to_mpa(ksi: float) -> float:
    return ksi / 0.145038


def mm_to_inch(mm: float) -> float:
    return mm * 0.0393701


def inch_to_mm(inch: float) -> float:
    return inch / 0.0393701


def n_to_lbf(n: float) -> float:
    return n * 0.224809


def lbf_to_n(lbf: float) -> float:
    return lbf / 0.224809


def strain_rate_to_log(rate: float) -> float:
    """Convert strain rate to log10 for plotting."""
    return math.log10(rate) if rate > 0 else float("-inf")
