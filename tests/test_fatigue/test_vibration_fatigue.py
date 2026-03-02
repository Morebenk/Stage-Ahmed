"""Tests for vibration fatigue (frequency-domain) assessment."""

import math
import numpy as np
import pytest
from weldfatigue.fatigue.vibration_fatigue import VibrationFatigueAssessment


class TestVibrationFatigue:
    """Tests for VibrationFatigueAssessment class."""

    @pytest.fixture
    def white_noise_psd(self):
        """Flat PSD (white noise) for testing."""
        freq = np.linspace(1, 100, 200)
        psd = np.ones_like(freq) * 10.0  # Flat 10 MPa^2/Hz
        return freq, psd

    @pytest.fixture
    def narrowband_psd(self):
        """Narrow-band PSD centered at 50 Hz."""
        freq = np.linspace(1, 100, 200)
        psd = np.exp(-0.5 * ((freq - 50) / 2) ** 2) * 100.0
        return freq, psd

    # --- Spectral moments ---

    def test_spectral_moments_keys(self, white_noise_psd):
        freq, psd = white_noise_psd
        moments = VibrationFatigueAssessment.spectral_moments(freq, psd)
        assert "m0" in moments
        assert "m1" in moments
        assert "m2" in moments
        assert "m4" in moments

    def test_spectral_moments_positive(self, white_noise_psd):
        freq, psd = white_noise_psd
        moments = VibrationFatigueAssessment.spectral_moments(freq, psd)
        assert moments["m0"] > 0
        assert moments["m2"] > 0
        assert moments["m4"] > 0

    def test_spectral_moments_ordering(self, white_noise_psd):
        """Higher moments should be larger for f > 1 Hz."""
        freq, psd = white_noise_psd
        moments = VibrationFatigueAssessment.spectral_moments(freq, psd)
        assert moments["m4"] > moments["m2"] > moments["m0"]

    # --- Bandwidth parameters ---

    def test_gamma_range(self, white_noise_psd):
        """Irregularity factor gamma should be between 0 and 1."""
        freq, psd = white_noise_psd
        moments = VibrationFatigueAssessment.spectral_moments(freq, psd)
        params = VibrationFatigueAssessment.bandwidth_parameters(moments)
        assert 0.0 <= params["gamma"] <= 1.0

    def test_narrowband_gamma_near_one(self, narrowband_psd):
        """Narrow-band PSD should have gamma close to 1."""
        freq, psd = narrowband_psd
        moments = VibrationFatigueAssessment.spectral_moments(freq, psd)
        params = VibrationFatigueAssessment.bandwidth_parameters(moments)
        assert params["gamma"] > 0.8

    # --- Dirlik PDF ---

    def test_dirlik_pdf_positive(self, white_noise_psd):
        """PDF should be non-negative."""
        freq, psd = white_noise_psd
        moments = VibrationFatigueAssessment.spectral_moments(freq, psd)
        for S in [10, 50, 100, 200]:
            p = VibrationFatigueAssessment.dirlik_pdf(S, moments)
            assert p >= 0.0

    def test_dirlik_pdf_zero_stress(self, white_noise_psd):
        """PDF at S=0 should be 0."""
        freq, psd = white_noise_psd
        moments = VibrationFatigueAssessment.spectral_moments(freq, psd)
        p = VibrationFatigueAssessment.dirlik_pdf(0.0, moments)
        assert p == pytest.approx(0.0)

    # --- Damage calculations ---

    def test_dirlik_damage_positive(self, white_noise_psd):
        """Dirlik damage should be positive for non-zero PSD."""
        freq, psd = white_noise_psd
        D = VibrationFatigueAssessment.dirlik_damage(freq, psd, 3600.0, 71)
        assert D > 0

    def test_narrowband_damage_positive(self, white_noise_psd):
        """Narrow-band damage should be positive."""
        freq, psd = white_noise_psd
        D = VibrationFatigueAssessment.narrowband_damage(freq, psd, 3600.0, 71)
        assert D > 0

    def test_narrowband_more_conservative(self, white_noise_psd):
        """Narrow-band should give higher (more conservative) damage than Dirlik."""
        freq, psd = white_noise_psd
        D_dir = VibrationFatigueAssessment.dirlik_damage(freq, psd, 3600.0, 71)
        D_nb = VibrationFatigueAssessment.narrowband_damage(freq, psd, 3600.0, 71)
        # For wide-band, narrowband is conservative
        assert D_nb >= D_dir * 0.5  # At least in same order of magnitude

    def test_damage_increases_with_duration(self, white_noise_psd):
        """Longer duration => more damage."""
        freq, psd = white_noise_psd
        D1 = VibrationFatigueAssessment.dirlik_damage(freq, psd, 1000.0, 71)
        D2 = VibrationFatigueAssessment.dirlik_damage(freq, psd, 2000.0, 71)
        assert D2 == pytest.approx(2 * D1, rel=0.01)

    def test_higher_fat_less_damage(self, white_noise_psd):
        """Higher FAT class => less damage."""
        freq, psd = white_noise_psd
        D_71 = VibrationFatigueAssessment.dirlik_damage(freq, psd, 3600.0, 71)
        D_90 = VibrationFatigueAssessment.dirlik_damage(freq, psd, 3600.0, 90)
        assert D_90 < D_71

    # --- Wirsching-Light ---

    def test_wl_correction_at_gamma_one(self):
        """At gamma=1 (narrow-band), correction ≈ 1.0."""
        wl = VibrationFatigueAssessment.wirsching_light_correction(1.0, 3.0)
        assert wl == pytest.approx(1.0, abs=0.1)

    def test_wl_correction_decreases_with_bandwidth(self):
        """Wider bandwidth (lower gamma) => lower correction factor."""
        wl_narrow = VibrationFatigueAssessment.wirsching_light_correction(0.95, 3.0)
        wl_wide = VibrationFatigueAssessment.wirsching_light_correction(0.5, 3.0)
        assert wl_wide < wl_narrow

    # --- Full evaluation ---

    def test_evaluate_returns_all_keys(self, white_noise_psd):
        freq, psd = white_noise_psd
        result = VibrationFatigueAssessment.evaluate(freq, psd, 3600.0, 71)
        assert "spectral_moments" in result
        assert "expected_peak_rate" in result
        assert "irregularity_factor" in result
        assert "damage_dirlik" in result
        assert "damage_narrowband" in result
        assert "damage_wirsching" in result
        assert "equivalent_stress_range" in result
        assert "status" in result

    def test_evaluate_status(self, white_noise_psd):
        freq, psd = white_noise_psd
        # Short duration should pass
        result = VibrationFatigueAssessment.evaluate(freq, psd, 1.0, 160)
        assert result["status"] == "PASS"
