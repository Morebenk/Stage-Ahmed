"""Tests for the FatigueAssessment orchestrator."""

import pytest

from weldfatigue.fatigue.assessment import FatigueAssessment
from weldfatigue.materials.database import MaterialDatabase
from weldfatigue.fatigue.fat_classes import FATClassCatalog


class TestFatigueAssessment:

    @pytest.fixture
    def assessor(self):
        return FatigueAssessment()

    def test_nominal_method(self, assessor):
        result = assessor.run(
            method="nominal",
            material_name="DP600",
            weld_type="fillet",
            load_type="tension",
            stress_range=80.0,
            num_cycles=2_000_000,
        )
        assert "single_block_result" in result
        assert result["single_block_result"]["method"] == "nominal"
        assert result["material"]["name"] == "DP600"

    def test_hotspot_method(self, assessor):
        result = assessor.run(
            method="hotspot",
            material_name="S355J2",
            weld_type="fillet",
            load_type="tension",
            stress_range=90.0,
            num_cycles=1_000_000,
            fat_class=100,
        )
        assert result["single_block_result"]["method"] == "hotspot"

    def test_notch_method(self, assessor):
        result = assessor.run(
            method="notch",
            material_name="DP600",
            weld_type="fillet",
            load_type="tension",
            stress_range=200.0,
            num_cycles=1_000_000,
        )
        assert result["single_block_result"]["method"] == "notch"
        assert result["fat_class"] == 225  # Steel notch FAT class

    def test_with_explicit_fat_class(self, assessor):
        result = assessor.run(
            method="nominal",
            material_name="DP600",
            weld_type="butt",
            load_type="tension",
            stress_range=80.0,
            num_cycles=1_000_000,
            fat_class=90,
        )
        assert result["fat_class"] == 90

    def test_with_load_spectrum(self, assessor):
        spectrum = [(100.0, 500_000), (80.0, 1_000_000), (50.0, 3_000_000)]
        result = assessor.run(
            method="nominal",
            material_name="DP600",
            weld_type="fillet",
            load_type="tension",
            stress_range=100.0,
            num_cycles=500_000,
            load_spectrum=spectrum,
            variable_amplitude=True,
        )
        assert "miner_result" in result
        assert len(result["miner_result"]["damage_per_block"]) == 3

    def test_material_properties_in_output(self, assessor):
        result = assessor.run(
            method="nominal",
            material_name="DP780",
            weld_type="butt",
            load_type="tension",
            stress_range=100.0,
            num_cycles=1_000_000,
            fat_class=80,
        )
        assert result["material"]["yield_strength"] == 480
        assert result["material"]["ultimate_strength"] == 780

    def test_aluminum_material(self, assessor):
        result = assessor.run(
            method="nominal",
            material_name="6061-T6",
            weld_type="butt",
            load_type="tension",
            stress_range=40.0,
            num_cycles=1_000_000,
        )
        assert result["material"]["family"] == "aluminum"

    def test_unknown_method_raises(self, assessor):
        with pytest.raises(ValueError, match="Unknown method"):
            assessor.run(
                method="invalid",
                material_name="DP600",
                weld_type="butt",
                load_type="tension",
                stress_range=100.0,
                num_cycles=1_000_000,
                fat_class=80,
            )
