"""Fracture Mechanics (LEFM Crack Growth) - Streamlit page."""

import streamlit as st
import numpy as np
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from i18n import t
from components.sidebar import render_sidebar

try:
    from weldfatigue.fatigue.fracture_mechanics import FractureMechanicsAssessment
except ImportError:
    FractureMechanicsAssessment = None

st.set_page_config(page_title="Fracture Mechanics", layout="wide")
render_sidebar()

st.title("LEFM Crack Growth Assessment")
st.markdown(
    "Paris law fatigue crack propagation analysis (IIW 4th method). "
    "Integrates crack growth from initial flaw size to critical size."
)

if FractureMechanicsAssessment is None:
    st.error(
        "Could not import `FractureMechanicsAssessment`. "
        "Please verify that the `weldfatigue` package is installed."
    )
    st.stop()

fm = FractureMechanicsAssessment()

# ── Sidebar inputs ────────────────────────────────────────────────────────
st.sidebar.header("Crack Growth Parameters")

material_type = st.sidebar.selectbox(
    "Material Type", ["steel", "aluminum"], index=0,
)
environment = st.sidebar.selectbox(
    "Environment", ["air", "seawater"], index=0,
)

# Load default Paris law parameters
defaults = FractureMechanicsAssessment.get_paris_parameters(material_type, environment)

st.sidebar.markdown("---")
st.sidebar.subheader("Paris Law: da/dN = C (dK)^m")
C_param = st.sidebar.number_input(
    "C (Paris constant)", value=defaults["C"],
    min_value=1e-20, max_value=1e-5, step=1e-14,
    format="%.2e",
    help="Paris law coefficient. Units: mm/cycle per (MPa sqrt(mm))^m.",
)
m_param = st.sidebar.number_input(
    "m (Paris exponent)", value=defaults["m"],
    min_value=1.0, max_value=10.0, step=0.1,
)

default_dKth = FractureMechanicsAssessment.DELTA_K_TH.get(material_type, 63.0)
delta_K_th = st.sidebar.number_input(
    "Threshold dK (MPa sqrt(mm))", value=default_dKth,
    min_value=0.0, step=1.0,
    help="Below this value no crack growth occurs.",
)

weld_geometry = st.sidebar.selectbox(
    "Weld Geometry", ["t_butt", "cruciform", "lap", "fillet"], index=0,
    format_func=lambda x: x.replace("_", " ").title(),
)

# ── Main area inputs ──────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("Geometry & Loading")
    initial_crack = st.number_input(
        "Initial Crack Size a0 (mm)", value=0.5, min_value=0.01, step=0.1,
        help="Initial flaw depth detected or assumed.",
    )
    critical_crack = st.number_input(
        "Critical Crack Size ac (mm)", value=5.0, min_value=0.1, step=0.5,
        help="Crack size at which failure / instability occurs.",
    )
    plate_thickness = st.number_input(
        "Plate Thickness (mm)", value=10.0, min_value=1.0, step=1.0,
    )
    stress_range = st.number_input(
        "Stress Range (MPa)", value=100.0, min_value=0.1, step=1.0,
        help="Applied stress range at the crack location.",
    )

with col2:
    st.subheader("Initial Conditions")
    # Show the initial geometry factor and Mk factor
    Y0 = fm.geometry_factor_Y(initial_crack, plate_thickness)
    Mk0 = fm.Mk_factor(initial_crack, plate_thickness, weld_geometry)
    dK0 = fm.stress_intensity_factor(stress_range, initial_crack, Y0, Mk0)

    st.metric("Geometry Factor Y(a0/t)", f"{Y0:.3f}")
    st.metric("Weld Magnification Mk(a0)", f"{Mk0:.3f}")
    st.metric("Initial dK (MPa sqrt(mm))", f"{dK0:.1f}")

    if dK0 < delta_K_th:
        st.warning("Initial dK is below the threshold -- no crack growth expected.")

# ── Run crack growth integration ──────────────────────────────────────────
if st.button("Run Crack Growth Analysis", type="primary"):
    if initial_crack >= critical_crack:
        st.error("Initial crack size must be smaller than critical crack size.")
    elif initial_crack >= plate_thickness:
        st.error("Initial crack size must be smaller than plate thickness.")
    else:
        result = fm.integrate_crack_growth(
            initial_crack=initial_crack,
            critical_crack=critical_crack,
            stress_range=stress_range,
            plate_thickness=plate_thickness,
            weld_geometry=weld_geometry,
            C=C_param,
            m=m_param,
            delta_K_th=delta_K_th,
        )
        st.session_state["fm_result"] = result

# ── Display results ───────────────────────────────────────────────────────
if "fm_result" in st.session_state:
    result = st.session_state["fm_result"]
    st.markdown("---")
    st.subheader("Results")

    # Status strip
    status_text = result["status"]
    if status_text == "COMPLETE":
        _cls = "fail"
        status_display = "CRACK GROWS TO CRITICAL SIZE"
    else:
        _cls = "pass"
        status_display = "CRACK ARRESTED (below threshold)"

    st.markdown(
        f'<div class="result-strip {_cls}">'
        f"<span>{status_display}</span>"
        f'<span>N = {result["total_cycles"]:,.0f} cycles</span></div>',
        unsafe_allow_html=True,
    )

    # Metrics
    mcol1, mcol2, mcol3, mcol4 = st.columns(4)
    mcol1.metric("Propagation Life", f'{result["total_cycles"]:,.0f} cycles')
    mcol2.metric("Initial dK", f'{result["delta_K_initial"]:.1f} MPa sqrt(mm)')
    mcol3.metric("Final dK", f'{result["delta_K_final"]:.1f} MPa sqrt(mm)')
    mcol4.metric("Status", status_text)

    # ── Crack growth curve (a vs N) ──────────────────────────────────────
    st.subheader("Crack Growth Curve")
    try:
        import plotly.graph_objects as go

        a_arr = np.array(result["crack_sizes"])
        N_arr = np.array(result["cycle_counts"])

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=N_arr, y=a_arr,
            mode="lines", name="Crack size a(N)",
            line=dict(color="crimson", width=2),
        ))
        # Mark initial and critical
        fig.add_hline(
            y=critical_crack, line_dash="dash", line_color="black",
            annotation_text=f"Critical ac = {critical_crack} mm",
        )
        fig.add_hline(
            y=initial_crack, line_dash="dot", line_color="grey",
            annotation_text=f"Initial a0 = {initial_crack} mm",
        )
        fig.update_layout(
            title="Crack Size vs. Number of Cycles",
            xaxis_title="Number of Cycles N",
            yaxis_title="Crack Size a (mm)",
            height=450,
        )
        st.plotly_chart(fig, use_container_width=True, key="crack_growth_curve")

    except ImportError:
        st.warning("Install `plotly` to display crack growth curves.")

    # ── Detailed data table ───────────────────────────────────────────────
    with st.expander("Crack Growth Data Table", expanded=False):
        import pandas as pd
        step = max(1, len(result["crack_sizes"]) // 50)  # Limit to ~50 rows
        df = pd.DataFrame({
            "Cycle Count": [f"{n:,.0f}" for n in result["cycle_counts"][::step]],
            "Crack Size (mm)": [f"{a:.3f}" for a in result["crack_sizes"][::step]],
        })
        st.dataframe(df, hide_index=True)
