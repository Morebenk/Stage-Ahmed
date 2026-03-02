"""Multiaxial Fatigue Assessment - Streamlit page."""

import streamlit as st
import numpy as np
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from i18n import t
from components.sidebar import render_sidebar

try:
    from weldfatigue.fatigue.multiaxial import MultiaxialFatigueAssessment
except ImportError:
    MultiaxialFatigueAssessment = None

st.set_page_config(page_title="Multiaxial Assessment", layout="wide")
render_sidebar()

st.title("Multiaxial Fatigue Assessment")
st.markdown(
    "Assess fatigue under combined normal and shear loading using "
    "IIW multiaxial methods (Gough-Pollard, Findley, MWCM)."
)

if MultiaxialFatigueAssessment is None:
    st.error(
        "Could not import `MultiaxialFatigueAssessment`. "
        "Please verify that the `weldfatigue` package is installed."
    )
    st.stop()

# ── Sidebar inputs ────────────────────────────────────────────────────────
st.sidebar.header("Multiaxial Parameters")

method_label = st.sidebar.selectbox(
    "Assessment Method",
    ["Gough-Pollard", "Findley", "MWCM"],
)
method_map = {
    "Gough-Pollard": "gough_pollard",
    "Findley": "findley",
    "MWCM": "mwcm",
}
method_key = method_map[method_label]

fat_sigma = st.sidebar.number_input(
    "FAT Class (Normal Stress)", value=71, min_value=36, max_value=225, step=1,
)
fat_tau = st.sidebar.number_input(
    "FAT Class (Shear Stress)", value=int(fat_sigma * 0.58),
    min_value=20, max_value=160, step=1,
)
num_cycles = st.sidebar.number_input(
    "Number of Cycles", value=2_000_000, min_value=1, step=1000,
)

# Findley-specific parameters
if method_key == "findley":
    st.sidebar.markdown("---")
    st.sidebar.subheader("Findley Parameters")
    findley_k = st.sidebar.number_input(
        "Findley k (material constant)", value=0.3,
        min_value=0.05, max_value=1.0, step=0.05,
        help="Typically 0.2-0.4 for welded joints.",
    )

# ── Main area inputs ──────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("Loading")
    delta_sigma = st.number_input(
        "Normal Stress Range (MPa)", value=80.0, min_value=0.0, step=1.0,
        help="Peak-to-peak normal (axial/bending) stress range.",
    )
    delta_tau = st.number_input(
        "Shear Stress Range (MPa)", value=40.0, min_value=0.0, step=1.0,
        help="Peak-to-peak shear stress range.",
    )

with col2:
    st.subheader("Method Information")
    if method_key == "gough_pollard":
        st.info(
            "**Gough-Pollard** interaction formula (IIW recommended).\n\n"
            "For proportional (in-phase) loading:\n\n"
            r"$(\Delta\sigma / \Delta\sigma_R)^2 + (\Delta\tau / \Delta\tau_R)^2 \leq 1$"
        )
    elif method_key == "findley":
        st.info(
            "**Findley** critical plane criterion.\n\n"
            r"Searches all plane orientations for max damage parameter: $FP = \tau_a + k \cdot \sigma_{n,max}$"
        )
    elif method_key == "mwcm":
        st.info(
            "**Modified Wohler Curve Method** (Susmel & Lazzarin).\n\n"
            "Converts multiaxial loading to an equivalent uniaxial stress range "
            "using an energy-based approach."
        )

# ── Run assessment ────────────────────────────────────────────────────────
if st.button("Run Assessment", type="primary"):
    kwargs = {}
    if method_key == "findley":
        sigma_a = delta_sigma / 2.0
        kwargs["sigma_max"] = sigma_a  # Conservative: amplitude as max
        kwargs["k"] = findley_k
        kwargs["fatigue_limit"] = fat_sigma / 2.0

    result = MultiaxialFatigueAssessment.evaluate(
        method=method_key,
        delta_sigma=delta_sigma,
        delta_tau=delta_tau,
        fat_sigma=fat_sigma,
        fat_tau=fat_tau,
        num_cycles=num_cycles,
        **kwargs,
    )
    st.session_state["multiaxial_result"] = result

# ── Display results ───────────────────────────────────────────────────────
if "multiaxial_result" in st.session_state:
    result = st.session_state["multiaxial_result"]
    st.markdown("---")
    st.subheader("Results")

    # Status strip
    _cls = "pass" if result["status"] == "PASS" else "fail"
    st.markdown(
        f'<div class="result-strip {_cls}">'
        f'<span>{result["status"]}</span>'
        f'<span>Method: {result["method"]}</span></div>',
        unsafe_allow_html=True,
    )

    # Metrics row
    rcol1, rcol2, rcol3 = st.columns(3)

    if result["method"] == "gough_pollard":
        rcol1.metric("Interaction Value", f'{result["interaction_value"]:.4f}')
        rcol2.metric("Normal Utilization", f'{result["normal_utilization"]:.2%}')
        rcol3.metric("Shear Utilization", f'{result["shear_utilization"]:.2%}')
    elif result["method"] == "findley":
        rcol1.metric("Findley Parameter", f'{result["findley_parameter"]:.2f} MPa')
        rcol2.metric("Critical Angle", f'{result["critical_angle_deg"]}deg')
        rcol3.metric("Utilization", f'{result["utilization"]:.2%}')
    elif result["method"] == "mwcm":
        rcol1.metric("Equivalent Stress Range", f'{result["equivalent_stress_range"]:.1f} MPa')
        rcol2.metric("Biaxiality Ratio", f'{result["biaxiality_ratio"]:.3f}')
        rcol3.metric("Utilization", f'{result["utilization"]:.2%}')

    # ── Interaction diagram ───────────────────────────────────────────────
    st.subheader("Interaction Diagram")

    try:
        import plotly.graph_objects as go

        fig = go.Figure()

        # Interaction envelope (unit circle for Gough-Pollard, unit line for others)
        theta = np.linspace(0, np.pi / 2, 100)

        if result["method"] == "gough_pollard":
            # Allowable stress ranges at N cycles
            m_sn = 3.0
            if num_cycles > 0:
                delta_sigma_R = fat_sigma * (2e6 / num_cycles) ** (1.0 / m_sn)
                delta_tau_R = fat_tau * (2e6 / num_cycles) ** (1.0 / m_sn)
            else:
                delta_sigma_R = fat_sigma
                delta_tau_R = fat_tau

            # Ellipse envelope: (x/dSR)^2 + (y/dTR)^2 = 1
            env_sigma = delta_sigma_R * np.cos(theta)
            env_tau = delta_tau_R * np.sin(theta)

            fig.add_trace(go.Scatter(
                x=env_sigma, y=env_tau,
                mode="lines", name="Interaction Envelope",
                line=dict(color="blue", width=2),
                fill="tozeroy", fillcolor="rgba(0, 128, 255, 0.08)",
            ))
            fig.add_trace(go.Scatter(
                x=[delta_sigma], y=[delta_tau],
                mode="markers+text", name="Operating Point",
                marker=dict(color="red", size=12, symbol="x"),
                text=[f"({delta_sigma:.0f}, {delta_tau:.0f})"],
                textposition="top right",
            ))
            fig.update_layout(
                xaxis_title="Normal Stress Range (MPa)",
                yaxis_title="Shear Stress Range (MPa)",
            )
        else:
            # Generic utilization bar chart for Findley / MWCM
            if result["method"] == "findley":
                util_val = result["utilization"]
                label = "Findley Utilization"
            else:
                util_val = result["utilization"]
                label = "MWCM Utilization"

            fig.add_trace(go.Bar(
                x=[label],
                y=[util_val],
                marker_color="green" if util_val <= 1.0 else "red",
                text=[f"{util_val:.2%}"],
                textposition="auto",
            ))
            fig.add_hline(
                y=1.0, line_dash="dash", line_color="black",
                annotation_text="Limit = 1.0",
            )
            fig.update_layout(
                yaxis_title="Utilization Ratio",
            )

        fig.update_layout(
            title=f"Multiaxial Assessment - {method_label}",
            height=450,
        )
        st.plotly_chart(fig, use_container_width=True, key="multiaxial_diagram")

    except ImportError:
        st.warning("Install `plotly` to display interaction diagrams.")

    # ── Detailed results table ────────────────────────────────────────────
    with st.expander("Detailed Results", expanded=False):
        import pandas as pd
        df = pd.DataFrame([
            {"Parameter": k, "Value": str(v)}
            for k, v in result.items()
        ])
        st.dataframe(df, hide_index=True)
