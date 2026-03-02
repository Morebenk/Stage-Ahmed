"""ISO 5817 Weld Quality Assessment - Streamlit page."""

import streamlit as st
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from i18n import t
from components.sidebar import render_sidebar

try:
    from weldfatigue.fatigue.weld_quality import WeldQualityAssessment
except ImportError:
    WeldQualityAssessment = None

st.set_page_config(page_title="Weld Quality", layout="wide")
render_sidebar()

st.title("ISO 5817 Weld Quality Assessment")
st.markdown(
    "Evaluate weld imperfections against ISO 5817:2023 quality levels (B, C, D), "
    "compute misalignment stress magnification factors (km), and determine "
    "the quality-adjusted FAT class."
)

if WeldQualityAssessment is None:
    st.error(
        "Could not import `WeldQualityAssessment`. "
        "Please verify that the `weldfatigue` package is installed."
    )
    st.stop()

wqa = WeldQualityAssessment

# ── Sidebar inputs ────────────────────────────────────────────────────────
st.sidebar.header("Quality Assessment Parameters")

quality_level = st.sidebar.selectbox(
    "ISO 5817 Quality Level",
    ["B", "C", "D"],
    index=0,
    help="B = stringent (highest quality), D = moderate (lowest quality).",
)

weld_type = st.sidebar.selectbox(
    "Weld Type",
    ["butt", "fillet", "cruciform", "t_joint", "lap"],
    index=0,
    format_func=lambda x: x.replace("_", " ").title(),
)

restraint = st.sidebar.selectbox(
    "End Restraint", ["fixed", "pinned"], index=0,
    help="Boundary conditions for angular misalignment calculation.",
)

# ── Main area inputs ──────────────────────────────────────────────────────
st.subheader("Geometry & Misalignment")

col1, col2 = st.columns(2)

with col1:
    thickness = st.number_input(
        "Plate Thickness t (mm)", value=10.0, min_value=1.0, step=0.5,
    )
    length = st.number_input(
        "Joint Length L (mm)", value=100.0, min_value=1.0, step=10.0,
        help="Span length for angular misalignment calculation.",
    )

with col2:
    axial_misalignment = st.number_input(
        "Axial Misalignment e_axial (mm)", value=0.5, min_value=0.0, step=0.1,
        help="Offset between plate centrelines.",
    )
    angular_misalignment = st.number_input(
        "Angular Misalignment e_angular (mm)", value=0.3, min_value=0.0, step=0.1,
        help="Angular distortion expressed as eccentricity over the joint length.",
    )

# ── Imperfection checks ──────────────────────────────────────────────────
st.markdown("---")
st.subheader("Imperfection Checks (ISO 5817)")
st.markdown(
    "Enter measured imperfection values. They will be compared against "
    f"the limits for quality level **{quality_level}**."
)

imp_col1, imp_col2 = st.columns(2)

with imp_col1:
    undercut_depth = st.number_input(
        "Undercut Depth (mm)", value=0.0, min_value=0.0, step=0.1,
    )
    porosity_area = st.number_input(
        "Porosity Area (mm^2)", value=0.0, min_value=0.0, step=0.1,
        help="Total projected area of porosity.",
    )
    excess_weld_metal = st.number_input(
        "Excess Weld Metal Height (mm)", value=0.0, min_value=0.0, step=0.1,
    )

with imp_col2:
    incomplete_pen = st.number_input(
        "Incomplete Penetration Depth (mm)", value=0.0, min_value=0.0, step=0.1,
    )
    axial_mis_imp = st.number_input(
        "Axial Misalignment (imperfection check, mm)", value=axial_misalignment,
        min_value=0.0, step=0.1,
        help="Measured axial misalignment for ISO 5817 imperfection check.",
    )

# ── Run assessment ────────────────────────────────────────────────────────
if st.button("Run Quality Assessment", type="primary"):
    # Core km + FAT assessment
    qa_result = wqa.assess_quality(
        weld_type=weld_type,
        quality_level=quality_level,
        axial_misalignment=axial_misalignment,
        angular_misalignment=angular_misalignment,
        thickness=thickness,
        length=length,
        restraint=restraint,
    )

    # Imperfection checks
    imperfection_checks = {}
    imperfections = {
        "undercut": undercut_depth,
        "porosity": porosity_area,
        "excess_weld_metal": excess_weld_metal,
        "incomplete_penetration": incomplete_pen,
        "misalignment_axial": axial_mis_imp,
    }
    for imp_type, measured in imperfections.items():
        imperfection_checks[imp_type] = wqa.check_imperfection(
            imp_type, measured, quality_level, thickness,
        )

    st.session_state["wq_result"] = qa_result
    st.session_state["wq_imperfections"] = imperfection_checks

# ── Display results ───────────────────────────────────────────────────────
if "wq_result" in st.session_state:
    qa_result = st.session_state["wq_result"]
    imperfection_checks = st.session_state.get("wq_imperfections", {})

    st.markdown("---")
    st.subheader("Results")

    # ── km factors ────────────────────────────────────────────────────────
    st.markdown("#### Misalignment Stress Magnification Factors")

    kcol1, kcol2, kcol3 = st.columns(3)
    kcol1.metric("km (Axial)", f'{qa_result["km_axial"]:.3f}')
    kcol2.metric("km (Angular)", f'{qa_result["km_angular"]:.3f}')
    kcol3.metric("km (Combined)", f'{qa_result["km_combined"]:.3f}')

    # ── FAT class ─────────────────────────────────────────────────────────
    base_fat = qa_result["fat_class"]
    adjusted_fat = base_fat / qa_result["km_combined"]

    fcol1, fcol2 = st.columns(2)
    fcol1.metric(
        f"Base FAT Class (Level {quality_level})",
        f"FAT {base_fat}",
    )
    fcol2.metric(
        "Effective FAT Class (km-adjusted)",
        f"FAT {adjusted_fat:.0f}",
        delta=f"{adjusted_fat - base_fat:.0f}" if adjusted_fat != base_fat else None,
        delta_color="inverse",
    )

    if qa_result["km_combined"] > 1.0:
        st.warning(
            f"Misalignment reduces the effective FAT class from "
            f"**{base_fat}** to **{adjusted_fat:.0f}** "
            f"(km = {qa_result['km_combined']:.3f})."
        )

    # ── Imperfection check results ────────────────────────────────────────
    if imperfection_checks:
        st.markdown("---")
        st.subheader("Imperfection Check Results")

        all_pass = True
        import pandas as pd

        rows = []
        for imp_type, check in imperfection_checks.items():
            label = imp_type.replace("_", " ").title()
            status = "PASS" if check["acceptable"] else "FAIL"
            if not check["acceptable"]:
                all_pass = False

            limit_str = f'{check["limit"]:.2f}' if check["limit"] is not None else "N/A"
            margin_str = f'{check["margin"]:.1%}' if check["margin"] is not None else "N/A"

            rows.append({
                "Imperfection": label,
                "Measured": f'{check["measured"]:.2f}',
                "Limit": limit_str,
                "Margin": margin_str,
                "Status": status,
            })

        df_imp = pd.DataFrame(rows)
        st.dataframe(df_imp, hide_index=True)

        # Overall strip
        _cls = "pass" if all_pass else "fail"
        _overall = "ALL CHECKS PASS" if all_pass else "SOME CHECKS FAIL"
        st.markdown(
            f'<div class="result-strip {_cls}">'
            f"<span>{_overall}</span>"
            f'<span>Quality Level {quality_level}</span></div>',
            unsafe_allow_html=True,
        )

    # ── Quality level comparison chart ────────────────────────────────────
    st.subheader("Quality Level Comparison")
    try:
        import plotly.graph_objects as go

        levels = ["B", "C", "D"]
        fat_values = [
            wqa.quality_level_fat(lvl, weld_type) for lvl in levels
        ]
        colors = [
            "green" if lvl == quality_level else "lightgray"
            for lvl in levels
        ]

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=levels,
            y=fat_values,
            marker_color=colors,
            text=[f"FAT {v}" for v in fat_values],
            textposition="auto",
        ))
        # Mark the adjusted FAT
        fig.add_hline(
            y=adjusted_fat, line_dash="dash", line_color="red",
            annotation_text=f"Effective FAT {adjusted_fat:.0f} (km-adjusted)",
        )
        fig.update_layout(
            title=f"FAT Class by Quality Level ({weld_type.replace('_', ' ').title()} Weld)",
            xaxis_title="ISO 5817 Quality Level",
            yaxis_title="FAT Class",
            height=400,
        )
        st.plotly_chart(fig, use_container_width=True, key="quality_comparison")

    except ImportError:
        st.warning("Install `plotly` to display the quality comparison chart.")

    # ── Summary table ─────────────────────────────────────────────────────
    with st.expander("Full Assessment Summary", expanded=False):
        import pandas as pd
        summary_data = [
            {"Parameter": "Quality Level", "Value": quality_level},
            {"Parameter": "Weld Type", "Value": weld_type.replace("_", " ").title()},
            {"Parameter": "Plate Thickness (mm)", "Value": f"{thickness:.1f}"},
            {"Parameter": "Axial Misalignment (mm)", "Value": f"{axial_misalignment:.2f}"},
            {"Parameter": "Angular Misalignment (mm)", "Value": f"{angular_misalignment:.2f}"},
            {"Parameter": "km (Axial)", "Value": f'{qa_result["km_axial"]:.3f}'},
            {"Parameter": "km (Angular)", "Value": f'{qa_result["km_angular"]:.3f}'},
            {"Parameter": "km (Combined)", "Value": f'{qa_result["km_combined"]:.3f}'},
            {"Parameter": "Base FAT Class", "Value": str(base_fat)},
            {"Parameter": "Effective FAT Class", "Value": f"{adjusted_fat:.0f}"},
        ]
        st.dataframe(pd.DataFrame(summary_data), hide_index=True)
