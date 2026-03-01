"""Report Generation - Streamlit page."""

import streamlit as st
from pathlib import Path
from datetime import date
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from i18n import t
from components.sidebar import render_sidebar
from components.result_table import render_fatigue_result

from weldfatigue.reporting.pdf_report import FatigueReport
from weldfatigue.reporting.html_report import HTMLReportGenerator
from weldfatigue.reporting.plots import FatiguePlots
from weldfatigue.fatigue.sn_curve import SNCurve

st.set_page_config(page_title="Report Generation", layout="wide")

render_sidebar()

st.title(t("report_generation"))

# ── Section keys (internal) mapped to translated labels ───────────────────
_SECTION_IDS = ["cover", "material", "fatigue", "sn", "haigh", "crash", "energy"]
_SECTION_LABELS = {
    "cover": "cover_page", "material": "material_data", "fatigue": "fatigue_results",
    "sn": "sn_curves", "haigh": "haigh_diagram", "crash": "crash_results",
    "energy": "energy_metrics",
}

# Report configuration
st.sidebar.header(t("report_settings"))

selected_sections = st.sidebar.multiselect(
    t("include_sections"),
    _SECTION_IDS,
    default=["cover", "material", "fatigue", "sn"],
    format_func=lambda sid: t(_SECTION_LABELS[sid]),
)

report_format = st.sidebar.radio(t("output_format"), ["PDF", "HTML"])

# Main form
st.subheader(t("project_information"))
col1, col2 = st.columns(2)
with col1:
    project_name = st.text_input(t("project_name"), value=t("default_project_name"))
    author = st.text_input(t("author"), value="")
with col2:
    report_date = st.date_input(t("date"), value=date.today())
    component = st.text_input(t("component"), value="")

st.markdown("---")
st.subheader(t("results_data"))
st.markdown(t("results_auto_include"))

# Show available results
has_fatigue = "fatigue_result" in st.session_state
has_shock = "shock_result" in st.session_state
has_fea = "fea_hotspot_stress" in st.session_state

if has_fatigue:
    st.markdown(f"- :green[{t('fatigue_results_available')}]")
    render_fatigue_result(st.session_state["fatigue_result"]["single_block_result"])
else:
    st.markdown(f"- {t('fatigue_results_not_computed')}")

if has_shock:
    st.markdown(f"- :green[{t('crash_results_available')}]")
else:
    st.markdown(f"- {t('crash_results_not_computed')}")

if has_fea:
    st.markdown(f"- :green[{t('fea_results_available')}]")
else:
    st.markdown(f"- {t('fea_results_not_computed')}")

st.markdown("---")

if st.button(t("generate_report"), type="primary"):
    if report_format == "PDF":
        report = FatigueReport(project_name, author, str(report_date))

        if "cover" in selected_sections:
            report.add_cover_page(
                t("weld_assessment"),
                f"{t('component')} : {component}" if component else "",
            )

        if "material" in selected_sections and has_fatigue:
            r = st.session_state["fatigue_result"]
            report.add_material_section(r.get("material", {}))

        if "fatigue" in selected_sections and has_fatigue:
            r = st.session_state["fatigue_result"]
            report.add_fatigue_summary([r["single_block_result"]])

        if "sn" in selected_sections and has_fatigue:
            r = st.session_state["fatigue_result"]
            sn = SNCurve(r["fat_class"], r["material"]["family"])
            fig_sn = FatiguePlots.sn_curve_matplotlib(sn)
            report.add_plot_image(fig_sn, t("sn_curves"))

        if "haigh" in selected_sections and has_fatigue:
            r = st.session_state["fatigue_result"]
            mat = r.get("material", {})
            fig_h = FatiguePlots.haigh_diagram_matplotlib(
                mat.get("ultimate_strength", 400) * 0.5,
                mat.get("ultimate_strength", 400),
                mat.get("yield_strength", 250),
            )
            report.add_plot_image(fig_h, t("haigh_diagram"))

        output_path = Path("report_output.pdf")
        report.generate(output_path)

        with open(output_path, "rb") as f:
            st.download_button(
                t("download_pdf"),
                data=f,
                file_name=f"{project_name.replace(' ', '_')}_report.pdf",
                mime="application/pdf",
            )
        output_path.unlink(missing_ok=True)
        st.success(t("pdf_generated"))

    elif report_format == "HTML":
        generator = HTMLReportGenerator()

        # Fatigue HTML report
        if any(s in selected_sections for s in ["fatigue", "material", "sn"]):
            material_info = {}
            fatigue_results = []
            miner_result = None
            if has_fatigue:
                r = st.session_state["fatigue_result"]
                material_info = r.get("material", {})
                fatigue_results = [r["single_block_result"]]
                miner_result = r.get("miner_result")

            html = generator.generate_fatigue_report(
                project_name=project_name,
                author=author,
                date=str(report_date),
                material_info=material_info,
                fatigue_results=fatigue_results,
                miner_result=miner_result,
            )

            st.download_button(
                t("download_html"),
                data=html,
                file_name=f"{project_name.replace(' ', '_')}_fatigue_report.html",
                mime="text/html",
            )

            with st.expander(t("preview_report")):
                st.components.v1.html(html, height=600, scrolling=True)

        # Shock HTML report
        if any(s in selected_sections for s in ["crash", "energy"]) and has_shock:
            sr = st.session_state["shock_result"]
            shock_html = generator.generate_shock_report(
                project_name=project_name,
                author=author,
                date=str(report_date),
                material_info={
                    "name": sr.get("material_name", ""),
                    "strain_rate": sr.get("strain_rate"),
                },
                crash_result={
                    "dynamic_yield": sr["dynamic_yield"],
                    "enhancement_factor": sr["dif"],
                },
                weld_result=st.session_state.get("shock_weld_result"),
                energy_result=st.session_state.get("shock_energy_result"),
            )

            st.download_button(
                t("download_shock_html"),
                data=shock_html,
                file_name=f"{project_name.replace(' ', '_')}_shock_report.html",
                mime="text/html",
                key="dl_shock_html",
            )

        st.success(t("html_generated"))
