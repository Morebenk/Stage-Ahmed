"""PDF report generation using fpdf2."""

import io
from pathlib import Path
from typing import Optional

from fpdf import FPDF

from weldfatigue.core.schemas import CumulativeDamageResult, FatigueResult


class FatigueReport(FPDF):
    """
    Generate a professional PDF fatigue assessment report.

    Structure:
        1. Cover page
        2. Summary table (PASS/FAIL per weld detail)
        3. Material properties
        4. Detailed results
        5. Conclusions
    """

    def __init__(self, project_name: str, author: str, date: str = None):
        super().__init__()
        self.project_name = project_name
        self.author = author
        self.date = date or ""
        self.set_auto_page_break(auto=True, margin=15)

    def header(self):
        self.set_font("Helvetica", "B", 10)
        self.cell(0, 8, f"WeldFatigue Report - {self.project_name}", align="L")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    def add_cover_page(self, title: str, subtitle: str = ""):
        self.add_page()
        self.set_font("Helvetica", "B", 28)
        self.ln(60)
        self.cell(0, 20, title, align="C")
        self.ln(15)
        self.set_font("Helvetica", "", 16)
        self.cell(0, 10, subtitle, align="C")
        self.ln(30)
        self.set_font("Helvetica", "", 12)
        self.cell(0, 8, f"Author: {self.author}", align="C")
        self.ln(8)
        self.cell(0, 8, f"Date: {self.date}", align="C")
        self.ln(8)
        self.cell(0, 8, f"Project: {self.project_name}", align="C")

    def add_section_title(self, title: str):
        self.set_font("Helvetica", "B", 14)
        self.ln(5)
        self.cell(0, 10, title)
        self.ln(8)

    def add_fatigue_summary(self, results: list[dict]):
        """Add a summary table of fatigue results."""
        self.add_page()
        self.add_section_title("Fatigue Assessment Summary")

        self.set_font("Helvetica", "B", 10)
        col_widths = [30, 30, 35, 35, 25, 30]
        headers = ["Method", "FAT Class", "Applied N", "Allowable N", "Status", "Safety Factor"]
        for w, h in zip(col_widths, headers):
            self.cell(w, 8, h, border=1, align="C")
        self.ln()

        self.set_font("Helvetica", "", 9)
        for r in results:
            self.cell(col_widths[0], 8, str(r.get("method", "")), border=1, align="C")
            self.cell(col_widths[1], 8, str(r.get("fat_class", "")), border=1, align="C")
            self.cell(col_widths[2], 8, f"{r.get('applied_cycles', 0):.2e}", border=1, align="C")
            self.cell(col_widths[3], 8, f"{r.get('allowable_cycles', 0):.2e}", border=1, align="C")
            status = r.get("status", "")
            self.cell(col_widths[4], 8, status, border=1, align="C")
            sf = r.get("safety_factor", 0)
            sf_str = f"{sf:.2f}" if sf != float("inf") else "INF"
            self.cell(col_widths[5], 8, sf_str, border=1, align="C")
            self.ln()

    def add_material_section(self, material_info: dict):
        """Add material properties section."""
        self.add_section_title("Material Properties")
        self.set_font("Helvetica", "", 10)
        for key, value in material_info.items():
            self.cell(60, 7, str(key), border=0)
            self.cell(60, 7, str(value), border=0)
            self.ln()

    def add_plot_image(self, fig, title: str = ""):
        """Add a matplotlib figure as an image."""
        if title:
            self.add_section_title(title)

        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")
        buf.seek(0)

        # Save to temp file for fpdf
        tmp_path = Path("_temp_plot.png")
        tmp_path.write_bytes(buf.getvalue())
        self.image(str(tmp_path), x=10, w=190)
        tmp_path.unlink(missing_ok=True)
        self.ln(5)

    def generate(self, output_path: Path):
        """Finalize and save the PDF."""
        self.alias_nb_pages()
        self.output(str(output_path))
