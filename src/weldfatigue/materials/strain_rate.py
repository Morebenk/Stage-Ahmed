"""Strain-rate dependent material models: Cowper-Symonds and Johnson-Cook."""

import math


def cowper_symonds_factor(strain_rate: float, D: float, q: float) -> float:
    """
    Compute the dynamic increase factor (DIF) using Cowper-Symonds model.

    sigma_d = sigma_s * [1 + (eps_dot / D)^(1/q)]

    Returns the multiplicative factor [1 + (eps_dot / D)^(1/q)].
    """
    if strain_rate <= 0:
        return 1.0
    return 1.0 + (strain_rate / D) ** (1.0 / q)


def cowper_symonds_yield(
    static_yield: float, strain_rate: float, D: float, q: float
) -> float:
    """Compute dynamic yield stress using Cowper-Symonds."""
    return static_yield * cowper_symonds_factor(strain_rate, D, q)


def johnson_cook_flow_stress(
    epsilon_p: float,
    strain_rate: float,
    temperature: float,
    A: float,
    B: float,
    n: float,
    C: float,
    m: float,
    eps_dot_0: float = 1.0,
    T_ref: float = 293.0,
    T_melt: float = 1793.0,
) -> float:
    """
    Johnson-Cook constitutive model:
    sigma = (A + B * eps_p^n) * (1 + C * ln(eps_dot/eps_dot_0)) * (1 - T*^m)
    where T* = (T - T_ref) / (T_melt - T_ref)
    """
    # Strain hardening term
    hardening = A + B * (epsilon_p**n) if epsilon_p > 0 else A

    # Strain rate term
    rate_ratio = strain_rate / eps_dot_0 if eps_dot_0 > 0 else 1.0
    rate_term = 1.0 + C * math.log(max(rate_ratio, 1.0))

    # Thermal softening term
    if T_melt > T_ref:
        T_star = (temperature - T_ref) / (T_melt - T_ref)
        T_star = max(0.0, min(1.0, T_star))
        thermal_term = 1.0 - (T_star**m)
    else:
        thermal_term = 1.0

    return hardening * rate_term * thermal_term
