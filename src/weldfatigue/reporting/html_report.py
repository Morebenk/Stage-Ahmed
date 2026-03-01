"""HTML report generation using Jinja2."""

from pathlib import Path
from typing import Optional

from jinja2 import Environment, FileSystemLoader


class HTMLReportGenerator:
    """Generate HTML fatigue/crash assessment reports."""

    def __init__(self, template_dir: Optional[Path] = None):
        if template_dir is None:
            template_dir = Path(__file__).parent / "templates"
        self.env = Environment(loader=FileSystemLoader(str(template_dir)))

    def generate_fatigue_report(
        self,
        project_name: str,
        author: str,
        date: str,
        material_info: dict,
        fatigue_results: list[dict],
        miner_result: dict = None,
        output_path: Path = None,
    ) -> str:
        """Generate a fatigue assessment HTML report."""
        template = self.env.get_template("fatigue_report.html")
        html = template.render(
            project_name=project_name,
            author=author,
            date=date,
            material=material_info,
            results=fatigue_results,
            miner=miner_result,
        )
        if output_path:
            output_path.write_text(html, encoding="utf-8")
        return html

    def generate_shock_report(
        self,
        project_name: str,
        author: str,
        date: str,
        material_info: dict,
        crash_result: dict,
        weld_result: dict = None,
        energy_result: dict = None,
        output_path: Path = None,
    ) -> str:
        """Generate a crash/shock assessment HTML report."""
        template = self.env.get_template("shock_report.html")
        html = template.render(
            project_name=project_name,
            author=author,
            date=date,
            material=material_info,
            crash=crash_result,
            weld=weld_result,
            energy=energy_result,
        )
        if output_path:
            output_path.write_text(html, encoding="utf-8")
        return html
