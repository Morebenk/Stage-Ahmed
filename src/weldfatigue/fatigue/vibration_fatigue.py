"""Frequency-domain vibration fatigue assessment."""

import math
import numpy as np
from weldfatigue.fatigue.sn_curve import SNCurve


class VibrationFatigueAssessment:
    """
    Frequency-domain fatigue analysis from PSD input.

    Methods:
    - Dirlik's method (most accurate for wide-band)
    - Narrow-band approximation (conservative)
    - Wirsching-Light correction

    References:
    - Dirlik (1985) PhD Thesis
    - Wirsching & Light (1980)
    """

    @staticmethod
    def spectral_moments(
        frequencies: np.ndarray,
        psd: np.ndarray,
    ) -> dict:
        """
        Compute spectral moments m_n = integral(f^n * G(f) df).

        Returns dict with keys: m0, m1, m2, m4.
        """
        df = np.diff(frequencies)
        f_mid = (frequencies[:-1] + frequencies[1:]) / 2.0
        psd_mid = (psd[:-1] + psd[1:]) / 2.0

        m0 = float(np.sum(psd_mid * df))
        m1 = float(np.sum(f_mid * psd_mid * df))
        m2 = float(np.sum(f_mid ** 2 * psd_mid * df))
        m4 = float(np.sum(f_mid ** 4 * psd_mid * df))

        return {"m0": m0, "m1": m1, "m2": m2, "m4": m4}

    @staticmethod
    def bandwidth_parameters(moments: dict) -> dict:
        """
        Compute bandwidth parameters from spectral moments.

        gamma (irregularity factor) = m2 / sqrt(m0 * m4)
        E[P] (expected peak rate) = sqrt(m4 / m2)
        E[0] (expected zero-crossing rate) = sqrt(m2 / m0)
        """
        m0 = moments["m0"]
        m1 = moments["m1"]
        m2 = moments["m2"]
        m4 = moments["m4"]

        if m0 <= 0 or m2 <= 0 or m4 <= 0:
            return {
                "gamma": 0.0,
                "expected_peak_rate": 0.0,
                "expected_zero_rate": 0.0,
                "xm": 0.0,
            }

        gamma = m2 / math.sqrt(m0 * m4)
        E_P = math.sqrt(m4 / m2)  # Expected peaks per second
        E_0 = math.sqrt(m2 / m0)  # Expected zero-crossings per second
        xm = m1 / m0 * math.sqrt(m0 / m4)

        return {
            "gamma": gamma,
            "expected_peak_rate": E_P,
            "expected_zero_rate": E_0,
            "xm": xm,
        }

    @staticmethod
    def dirlik_pdf(S: float, moments: dict) -> float:
        """
        Dirlik's probability density function for stress range.

        p(S) = (D1/Q * exp(-Z/Q) + D2*Z/R^2 * exp(-Z^2/(2*R^2))
                + D3*Z * exp(-Z^2/2)) / (2*sqrt(m0))

        where Z = S / (2*sqrt(m0))
        """
        m0 = moments["m0"]
        m1 = moments["m1"]
        m2 = moments["m2"]
        m4 = moments["m4"]

        if m0 <= 0 or S <= 0:
            return 0.0

        sqrt_m0 = math.sqrt(m0)
        Z = S / (2.0 * sqrt_m0)

        gamma = m2 / math.sqrt(m0 * m4)
        xm = m1 / m0 * math.sqrt(m0 / m4)

        D1 = 2.0 * (xm - gamma ** 2) / (1.0 + gamma ** 2)
        R = (gamma - xm - D1 ** 2) / (1.0 - gamma - D1 + D1 ** 2)
        if R <= 0:
            R = 0.01  # Prevent division by zero
        D2 = (1.0 - gamma - D1 + D1 ** 2) / (1.0 - R)
        D3 = 1.0 - D1 - D2
        Q = 1.25 * (gamma - D3 - D2 * R) / D1
        if Q <= 0:
            Q = 0.01

        term1 = D1 / Q * math.exp(-Z / Q)
        term2 = D2 * Z / R ** 2 * math.exp(-Z ** 2 / (2.0 * R ** 2))
        term3 = D3 * Z * math.exp(-Z ** 2 / 2.0)

        pdf = (term1 + term2 + term3) / (2.0 * sqrt_m0)
        return max(0.0, pdf)

    @staticmethod
    def dirlik_damage(
        frequencies: np.ndarray,
        psd: np.ndarray,
        duration: float,
        fat_class: int,
        material_type: str = "steel",
        m: float = 3.0,
        n_stress_bins: int = 100,
    ) -> float:
        """
        Compute Palmgren-Miner damage using Dirlik's method.

        D = E[P] * T * integral(S^m * p(S) dS) / C

        where C = FAT^m * 2e6 (from S-N curve).
        """
        moments = VibrationFatigueAssessment.spectral_moments(frequencies, psd)
        params = VibrationFatigueAssessment.bandwidth_parameters(moments)

        if moments["m0"] <= 0:
            return 0.0

        E_P = params["expected_peak_rate"]
        sqrt_m0 = math.sqrt(moments["m0"])

        # S-N curve constant: N = (FAT / S)^m * 2e6  =>  C_sn = FAT^m * 2e6
        C_sn = fat_class ** m * 2e6

        # Numerical integration of S^m * p(S) dS
        S_max = 6.0 * 2.0 * sqrt_m0  # 6 sigma range
        dS = S_max / n_stress_bins

        integral = 0.0
        for i in range(1, n_stress_bins + 1):
            S = i * dS
            p_S = VibrationFatigueAssessment.dirlik_pdf(S, moments)
            integral += S ** m * p_S * dS

        D = E_P * duration * integral / C_sn
        return D

    @staticmethod
    def narrowband_damage(
        frequencies: np.ndarray,
        psd: np.ndarray,
        duration: float,
        fat_class: int,
        material_type: str = "steel",
        m: float = 3.0,
    ) -> float:
        """
        Narrow-band approximation (conservative for wide-band signals).

        D = E[0] * T * (2*sqrt(2*m0))^m * Gamma(1+m/2) / C_sn
        """
        moments = VibrationFatigueAssessment.spectral_moments(frequencies, psd)

        if moments["m0"] <= 0:
            return 0.0

        E_0 = math.sqrt(moments["m2"] / moments["m0"])
        C_sn = fat_class ** m * 2e6

        # Gamma function
        gamma_val = math.gamma(1.0 + m / 2.0)

        D = E_0 * duration * (2.0 * math.sqrt(2.0 * moments["m0"])) ** m * gamma_val / C_sn
        return D

    @staticmethod
    def wirsching_light_correction(gamma: float, m: float) -> float:
        """
        Wirsching-Light correction factor for wide-band signals.

        lambda = a(m) + [1 - a(m)] * (1 - epsilon)^b(m)

        where epsilon = sqrt(1 - gamma^2) is the bandwidth parameter.
        """
        a = 0.926 - 0.033 * m
        b = 1.587 * m - 2.323

        epsilon = math.sqrt(max(0.0, 1.0 - gamma ** 2))

        correction = a + (1.0 - a) * (1.0 - epsilon) ** b
        return max(0.01, correction)

    @staticmethod
    def evaluate(
        frequencies: np.ndarray,
        psd: np.ndarray,
        duration: float,
        fat_class: int,
        material_type: str = "steel",
    ) -> dict:
        """
        Complete vibration fatigue assessment.

        Returns dict with all damage estimates and spectral parameters.
        """
        m = 3.0  # IIW S-N slope

        moments = VibrationFatigueAssessment.spectral_moments(
            np.asarray(frequencies), np.asarray(psd)
        )
        params = VibrationFatigueAssessment.bandwidth_parameters(moments)

        D_dirlik = VibrationFatigueAssessment.dirlik_damage(
            np.asarray(frequencies), np.asarray(psd),
            duration, fat_class, material_type, m,
        )
        D_nb = VibrationFatigueAssessment.narrowband_damage(
            np.asarray(frequencies), np.asarray(psd),
            duration, fat_class, material_type, m,
        )

        # Wirsching-Light corrected narrow-band
        wl_factor = VibrationFatigueAssessment.wirsching_light_correction(
            params["gamma"], m
        )
        D_wl = D_nb * wl_factor

        # Equivalent stress range (from Dirlik damage)
        if D_dirlik > 0 and duration > 0:
            E_P = params["expected_peak_rate"]
            N_eq = E_P * duration
            C_sn = fat_class ** m * 2e6
            if N_eq > 0:
                eq_stress = (D_dirlik * C_sn / N_eq) ** (1.0 / m)
            else:
                eq_stress = 0.0
        else:
            eq_stress = 0.0

        status = "PASS" if D_dirlik < 1.0 else "FAIL"

        return {
            "spectral_moments": moments,
            "expected_peak_rate": params["expected_peak_rate"],
            "irregularity_factor": params["gamma"],
            "damage_dirlik": D_dirlik,
            "damage_narrowband": D_nb,
            "damage_wirsching": D_wl,
            "equivalent_stress_range": eq_stress,
            "status": status,
        }
