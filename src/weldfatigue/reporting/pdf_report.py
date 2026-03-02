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

    def add_modifiers_section(self, modifiers: dict):
        """Add modifier chain summary showing all applied correction factors.

        Parameters
        ----------
        modifiers : dict
            Dictionary with optional keys: ``"thickness"``,
            ``"post_weld_treatment"``, ``"environment"``,
            ``"safety_factors"``, ``"misalignment"``,
            ``"residual_stress"``, ``"pwht"``, ``"quality_level"``.
            Each value is a dict containing modifier details such as
            ``"factor"`` and ``"fat_class"``.
        """
        self.add_section_title("Modifier Chain")

        # Table header
        self.set_font("Helvetica", "B", 10)
        col_widths = [60, 50, 50]
        headers = ["Modifier", "Factor / Value", "Resulting FAT"]
        for w, h in zip(col_widths, headers):
            self.cell(w, 8, h, border=1, align="C")
        self.ln()

        # Table rows
        self.set_font("Helvetica", "", 9)
        display_names = {
            "thickness": "Thickness Correction",
            "post_weld_treatment": "Post-Weld Treatment",
            "environment": "Environment",
            "safety_factors": "Safety Factors",
            "misalignment": "Misalignment",
            "residual_stress": "Residual Stress",
            "pwht": "PWHT",
            "quality_level": "Quality Level",
        }
        for key, details in modifiers.items():
            name = display_names.get(key, str(key))
            factor = details.get("factor", details.get("value", ""))
            fat = details.get("fat_class", "")
            factor_str = f"{factor:.4f}" if isinstance(factor, float) else str(factor)
            self.cell(col_widths[0], 8, name, border=1)
            self.cell(col_widths[1], 8, factor_str, border=1, align="C")
            self.cell(col_widths[2], 8, str(fat), border=1, align="C")
            self.ln()

    def add_multiaxial_section(self, result: dict):
        """Add multiaxial fatigue assessment results.

        Parameters
        ----------
        result : dict
            Dictionary with keys: ``"interaction_value"``,
            ``"normal_utilization"``, ``"shear_utilization"``,
            ``"method"``, ``"status"``.
        """
        self.add_section_title("Multiaxial Assessment")

        self.set_font("Helvetica", "", 10)
        fields = [
            ("Method", "method"),
            ("Interaction Value", "interaction_value"),
            ("Normal Utilization", "normal_utilization"),
            ("Shear Utilization", "shear_utilization"),
        ]
        for label, key in fields:
            value = result.get(key, "")
            value_str = f"{value:.4f}" if isinstance(value, float) else str(value)
            self.cell(60, 7, label, border=0)
            self.cell(60, 7, value_str, border=0)
            self.ln()

        # Status with colour highlight
        status = result.get("status", "")
        self.cell(60, 7, "Status", border=0)
        if status.upper() == "PASS":
            self.set_text_color(0, 128, 0)
        else:
            self.set_text_color(200, 0, 0)
        self.set_font("Helvetica", "B", 10)
        self.cell(60, 7, str(status), border=0)
        self.set_text_color(0, 0, 0)
        self.set_font("Helvetica", "", 10)
        self.ln()

    def add_crack_growth_section(self, result: dict):
        """Add fracture mechanics / crack growth results.

        Parameters
        ----------
        result : dict
            Dictionary with keys: ``"total_cycles"``,
            ``"delta_K_initial"``, ``"delta_K_final"``, ``"status"``.
        """
        self.add_section_title("Crack Growth (Fracture Mechanics)")

        self.set_font("Helvetica", "", 10)
        fields = [
            ("Total Cycles", "total_cycles"),
            ("Initial Delta-K", "delta_K_initial"),
            ("Final Delta-K", "delta_K_final"),
        ]
        for label, key in fields:
            value = result.get(key, "")
            if isinstance(value, float):
                value_str = f"{value:.4f}"
            elif isinstance(value, int):
                value_str = f"{value:.2e}"
            else:
                value_str = str(value)
            self.cell(60, 7, label, border=0)
            self.cell(60, 7, value_str, border=0)
            self.ln()

        # Status with colour highlight
        status = result.get("status", "")
        self.cell(60, 7, "Status", border=0)
        if str(status).upper() == "PASS":
            self.set_text_color(0, 128, 0)
        else:
            self.set_text_color(200, 0, 0)
        self.set_font("Helvetica", "B", 10)
        self.cell(60, 7, str(status), border=0)
        self.set_text_color(0, 0, 0)
        self.set_font("Helvetica", "", 10)
        self.ln()

    def add_weld_quality_section(self, quality_info: dict):
        """Add ISO 5817 weld quality assessment section.

        Parameters
        ----------
        quality_info : dict
            Dictionary with keys: ``"km_axial"``, ``"km_angular"``,
            ``"km_combined"``, ``"fat_class"``, ``"quality_level"``.
        """
        self.add_section_title("Weld Quality Assessment (ISO 5817)")

        # Table header
        self.set_font("Helvetica", "B", 10)
        col_widths = [60, 60]
        headers = ["Parameter", "Value"]
        for w, h in zip(col_widths, headers):
            self.cell(w, 8, h, border=1, align="C")
        self.ln()

        # Table rows
        self.set_font("Helvetica", "", 9)
        rows = [
            ("Km Axial", "km_axial"),
            ("Km Angular", "km_angular"),
            ("Km Combined", "km_combined"),
            ("FAT Class", "fat_class"),
            ("Quality Level", "quality_level"),
        ]
        for label, key in rows:
            value = quality_info.get(key, "")
            value_str = f"{value:.4f}" if isinstance(value, float) else str(value)
            self.cell(col_widths[0], 8, label, border=1)
            self.cell(col_widths[1], 8, value_str, border=1, align="C")
            self.ln()

    def add_safety_factors_section(self, safety_info: dict):
        """Add safety factor breakdown section.

        Parameters
        ----------
        safety_info : dict
            Dictionary with keys: ``"gamma_Mf"``, ``"gamma_Ff"``,
            ``"dff"``, ``"characteristic_factor"``,
            ``"combined_factor"``.
        """
        self.add_section_title("Safety Factors")

        # Table header
        self.set_font("Helvetica", "B", 10)
        col_widths = [80, 50]
        headers = ["Factor", "Value"]
        for w, h in zip(col_widths, headers):
            self.cell(w, 8, h, border=1, align="C")
        self.ln()

        # Table rows
        self.set_font("Helvetica", "", 9)
        rows = [
            ("Partial Safety Factor (gamma_Mf)", "gamma_Mf"),
            ("Load Factor (gamma_Ff)", "gamma_Ff"),
            ("Design Fatigue Factor (DFF)", "dff"),
            ("Characteristic Factor", "characteristic_factor"),
            ("Combined Factor", "combined_factor"),
        ]
        for label, key in rows:
            value = safety_info.get(key, "")
            value_str = f"{value:.4f}" if isinstance(value, float) else str(value)
            self.cell(col_widths[0], 8, label, border=1)
            self.cell(col_widths[1], 8, value_str, border=1, align="C")
            self.ln()

    def add_environmental_section(self, env_info: dict):
        """Add environmental correction factors section.

        Parameters
        ----------
        env_info : dict
            Dictionary with keys: ``"factor"``, ``"fat_after"``,
            ``"removes_endurance_limit"``.
        """
        self.add_section_title("Environmental Factors")

        self.set_font("Helvetica", "", 10)

        factor = env_info.get("factor", "")
        factor_str = f"{factor:.4f}" if isinstance(factor, float) else str(factor)
        self.cell(60, 7, "Correction Factor", border=0)
        self.cell(60, 7, factor_str, border=0)
        self.ln()

        fat_after = env_info.get("fat_after", "")
        fat_str = f"{fat_after:.1f}" if isinstance(fat_after, float) else str(fat_after)
        self.cell(60, 7, "FAT After Correction", border=0)
        self.cell(60, 7, fat_str, border=0)
        self.ln()

        removes = env_info.get("removes_endurance_limit", "")
        removes_str = "Yes" if removes else "No"
        self.cell(60, 7, "Removes Endurance Limit", border=0)
        self.cell(60, 7, removes_str, border=0)
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
