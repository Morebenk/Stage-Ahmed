"""Tests for PDF report generation."""

import pytest
from pathlib import Path

from weldfatigue.reporting.pdf_report import FatigueReport


class TestFatigueReport:

    @pytest.fixture
    def report(self):
        return FatigueReport(
            project_name="Test Project",
            author="Test Author",
            date="2024-01-01",
        )

    def test_create_report(self, report):
        assert report.project_name == "Test Project"
        assert report.author == "Test Author"

    def test_add_cover_page(self, report):
        report.add_cover_page("Test Title", "Test Subtitle")
        assert report.page_no() == 1

    def test_add_fatigue_summary(self, report):
        results = [
            {
                "method": "nominal",
                "fat_class": 80,
                "applied_cycles": 2e6,
                "allowable_cycles": 5e6,
                "status": "PASS",
                "safety_factor": 2.5,
            },
            {
                "method": "hotspot",
                "fat_class": 100,
                "applied_cycles": 1e6,
                "allowable_cycles": 8e5,
                "status": "FAIL",
                "safety_factor": 0.8,
            },
        ]
        report.add_fatigue_summary(results)
        assert report.page_no() >= 1

    def test_add_material_section(self, report):
        report.add_cover_page("Title")
        report.add_material_section({
            "Name": "DP600",
            "Yield Strength": "350 MPa",
            "Ultimate Strength": "600 MPa",
        })
        assert report.page_no() >= 1

    def test_generate_pdf(self, report, tmp_path):
        report.add_cover_page("Test Report", "Fatigue Assessment")
        report.add_fatigue_summary([{
            "method": "nominal",
            "fat_class": 80,
            "applied_cycles": 2e6,
            "allowable_cycles": 5e6,
            "status": "PASS",
            "safety_factor": 2.5,
        }])

        output = tmp_path / "test_report.pdf"
        report.generate(output)
        assert output.exists()
        assert output.stat().st_size > 0

    def test_add_plot_image(self, report, tmp_path):
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots()
        ax.plot([1, 2, 3], [1, 4, 9])

        report.add_cover_page("Test")
        report.add_plot_image(fig, title="Test Plot")

        output = tmp_path / "test_with_plot.pdf"
        report.generate(output)
        assert output.exists()
        plt.close(fig)

    def test_inf_safety_factor(self, report, tmp_path):
        report.add_fatigue_summary([{
            "method": "nominal",
            "fat_class": 80,
            "applied_cycles": 2e6,
            "allowable_cycles": 5e6,
            "status": "PASS",
            "safety_factor": float("inf"),
        }])
        output = tmp_path / "test_inf.pdf"
        report.generate(output)
        assert output.exists()
