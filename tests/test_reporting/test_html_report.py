"""Tests for HTML report generation."""

import pytest
from pathlib import Path

from weldfatigue.reporting.html_report import HTMLReportGenerator


class TestHTMLReportGenerator:

    @pytest.fixture
    def generator(self):
        return HTMLReportGenerator()

    def test_create_generator(self, generator):
        assert generator.env is not None

    def test_generate_fatigue_report_string(self, generator):
        html = generator.generate_fatigue_report(
            project_name="Test Project",
            author="Test Author",
            date="2024-01-01",
            material_info={"name": "DP600", "yield_strength": 350},
            fatigue_results=[{
                "method": "nominal",
                "fat_class": 80,
                "applied_cycles": 2e6,
                "allowable_cycles": 5e6,
                "damage_ratio": 0.4,
                "safety_factor": 2.5,
                "status": "PASS",
            }],
        )
        assert "Test Project" in html
        assert "DP600" in html
        assert "PASS" in html

    def test_generate_fatigue_report_file(self, generator, tmp_path):
        output = tmp_path / "report.html"
        generator.generate_fatigue_report(
            project_name="File Test",
            author="Author",
            date="2024-01-01",
            material_info={"name": "S355J2"},
            fatigue_results=[],
            output_path=output,
        )
        assert output.exists()
        content = output.read_text(encoding="utf-8")
        assert "File Test" in content

    def test_generate_fatigue_report_with_miner(self, generator):
        html = generator.generate_fatigue_report(
            project_name="Miner Test",
            author="Author",
            date="2024-01-01",
            material_info={"name": "DP600"},
            fatigue_results=[],
            miner_result={
                "total_damage": 0.75,
                "status": "PASS",
                "damage_per_block": [0.3, 0.25, 0.2],
            },
        )
        assert "Miner" in html or "0.75" in html or "PASS" in html

    def test_generate_shock_report_string(self, generator):
        html = generator.generate_shock_report(
            project_name="Crash Test",
            author="Author",
            date="2024-01-01",
            material_info={"name": "DP780"},
            crash_result={
                "dynamic_yield": 650,
                "enhancement_factor": 1.3,
            },
        )
        assert "Crash Test" in html
        assert "DP780" in html

    def test_generate_shock_report_with_weld(self, generator):
        html = generator.generate_shock_report(
            project_name="Weld Test",
            author="Author",
            date="2024-01-01",
            material_info={"name": "S355J2"},
            crash_result={"dynamic_yield": 500, "enhancement_factor": 1.3},
            weld_result={
                "criterion": "stress_based_EN1993",
                "equivalent_stress": 300,
                "allowable_stress": 400,
                "utilization": 0.75,
                "status": "PASS",
            },
        )
        assert "Weld Test" in html

    def test_generate_shock_report_file(self, generator, tmp_path):
        output = tmp_path / "shock.html"
        generator.generate_shock_report(
            project_name="File Crash",
            author="Author",
            date="2024-01-01",
            material_info={"name": "DP600"},
            crash_result={"dynamic_yield": 550, "enhancement_factor": 1.2},
            output_path=output,
        )
        assert output.exists()
