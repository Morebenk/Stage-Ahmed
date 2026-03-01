"""Tests for Palmgren-Miner cumulative damage."""

import pytest

from weldfatigue.fatigue.sn_curve import SNCurve
from weldfatigue.fatigue.damage import PalmgrenMiner


class TestPalmgrenMiner:

    def test_single_block_below_limit(self):
        sn = SNCurve(71, "steel", variable_amplitude=True)
        miner = PalmgrenMiner(sn)
        result = miner.compute_damage([(100.0, 100_000)])
        assert result.status == "PASS"
        assert result.total_damage < 1.0

    def test_single_block_above_limit(self):
        sn = SNCurve(71, "steel", variable_amplitude=True)
        miner = PalmgrenMiner(sn)
        result = miner.compute_damage([(100.0, 10_000_000)])
        assert result.status == "FAIL"
        assert result.total_damage > 1.0

    def test_multiple_blocks(self):
        sn = SNCurve(71, "steel", variable_amplitude=True)
        miner = PalmgrenMiner(sn)
        spectrum = [(100.0, 500_000), (80.0, 1_000_000), (50.0, 5_000_000)]
        result = miner.compute_damage(spectrum)
        assert len(result.damage_per_block) == 3
        assert result.total_damage == pytest.approx(
            sum(result.damage_per_block), rel=1e-10
        )

    def test_below_cutoff_zero_damage(self):
        """Stress below cut-off should contribute zero damage."""
        sn = SNCurve(71, "steel", variable_amplitude=True)
        miner = PalmgrenMiner(sn)
        result = miner.compute_damage([(1.0, 1_000_000)])
        assert result.total_damage == 0.0

    def test_custom_damage_limit(self):
        """Safety-critical D_limit=0.5."""
        sn = SNCurve(71, "steel", variable_amplitude=True)
        miner = PalmgrenMiner(sn, damage_limit=0.5)
        result = miner.compute_damage([(100.0, 400_000)])
        # D should be moderate; check that 0.5 limit applies
        if result.total_damage >= 0.5:
            assert result.status == "FAIL"
        else:
            assert result.status == "PASS"

    def test_equivalent_stress_range(self):
        sn = SNCurve(71, "steel", variable_amplitude=True)
        miner = PalmgrenMiner(sn)
        spectrum = [(100.0, 500_000), (80.0, 1_000_000)]
        eq_range = miner.equivalent_stress_range(spectrum)
        assert 80.0 < eq_range < 100.0  # Weighted average

    def test_empty_spectrum(self):
        sn = SNCurve(71, "steel", variable_amplitude=True)
        miner = PalmgrenMiner(sn)
        result = miner.compute_damage([])
        assert result.total_damage == 0.0
        assert result.status == "PASS"
