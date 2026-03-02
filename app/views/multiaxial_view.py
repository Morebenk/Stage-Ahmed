"""Multiaxial fatigue assessment view (Gough-Pollard / Findley / MWCM)."""

import streamlit as st
import numpy as np

from i18n import t
from weldfatigue.fatigue.multiaxial import MultiaxialFatigueAssessment


def render() -> None:
    """Render multiaxial assessment sidebar config and main content."""

    # ── Sidebar config ────────────────────────────────────────────────────
    st.sidebar.markdown("---")
    st.sidebar.subheader(t("multiaxial_params"))

    method_label = st.sidebar.selectbox(
        t("assessment_method"),
        ["Gough-Pollard", "Findley", "MWCM"],
        key="mx_method",
    )
    method_map = {
        "Gough-Pollard": "gough_pollard",
        "Findley": "findley",
        "MWCM": "mwcm",
    }
    method_key = method_map[method_label]

    fat_sigma = st.sidebar.number_input(
        "FAT (Normal Stress)", value=71,
        min_value=36, max_value=225, step=1, key="mx_fat_sigma",
    )
    fat_tau = st.sidebar.number_input(
        "FAT (Shear Stress)", value=int(fat_sigma * 0.58),
        min_value=20, max_value=160, step=1, key="mx_fat_tau",
    )
    num_cycles = st.sidebar.number_input(
        t("number_of_cycles"), value=2_000_000,
        min_value=1, step=1000, key="mx_cycles",
    )

    findley_k = 0.3
    if method_key == "findley":
        st.sidebar.markdown("---")
        findley_k = st.sidebar.number_input(
            "Findley k", value=0.3,
            min_value=0.05, max_value=1.0, step=0.05,
            help="Material constant, typically 0.2-0.4 for welded joints.",
            key="mx_findley_k",
        )

    # ── Main content ──────────────────────────────────────────────────────
    st.markdown(
        t("multiaxial_desc"),
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader(t("loading"))
        delta_sigma = st.number_input(
            t("normal_stress_range"), value=80.0,
            min_value=0.0, step=1.0, key="mx_delta_sigma",
            help=t("normal_stress_range_help"),
        )
        delta_tau = st.number_input(
            t("shear_stress_range"), value=40.0,
            min_value=0.0, step=1.0, key="mx_delta_tau",
            help=t("shear_stress_range_help"),
        )

    with col2:
        st.subheader(t("method_info"))
        if method_key == "gough_pollard":
            st.info(
                "**Gough-Pollard** interaction formula (IIW recommended).\n\n"
                "For proportional (in-phase) loading:\n\n"
                r"$(\Delta\sigma / \Delta\sigma_R)^2 + (\Delta\tau / \Delta\tau_R)^2 \leq 1$"
            )
        elif method_key == "findley":
            st.info(
                "**Findley** critical plane criterion.\n\n"
                r"Max damage parameter: $FP = \tau_a + k \cdot \sigma_{n,max}$"
            )
        elif method_key == "mwcm":
            st.info(
                "**Modified Wohler Curve Method** (Susmel & Lazzarin).\n\n"
                "Converts multiaxial loading to an equivalent uniaxial stress "
                "range using an energy-based approach."
            )

    # ── Run assessment ────────────────────────────────────────────────────
    if st.button(t("run_assessment"), type="primary", key="mx_run"):
        kwargs = {}
        if method_key == "findley":
            kwargs["sigma_max"] = delta_sigma / 2.0
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

    # ── Display results ───────────────────────────────────────────────────
    if "multiaxial_result" not in st.session_state:
        return

    result = st.session_state["multiaxial_result"]
    st.markdown("---")
    st.subheader(t("results"))

    _cls = "pass" if result["status"] == "PASS" else "fail"
    st.markdown(
        f'<div class="result-strip {_cls}">'
        f'<span>{result["status"]}</span>'
        f'<span>Method: {result["method"]}</span></div>',
        unsafe_allow_html=True,
    )

    rcol1, rcol2, rcol3 = st.columns(3)
    if result["method"] == "gough_pollard":
        rcol1.metric("Interaction Value", f'{result["interaction_value"]:.4f}')
        rcol2.metric("Normal Utilization", f'{result["normal_utilization"]:.2%}')
        rcol3.metric("Shear Utilization", f'{result["shear_utilization"]:.2%}')
    elif result["method"] == "findley":
        rcol1.metric("Findley Parameter", f'{result["findley_parameter"]:.2f} MPa')
        rcol2.metric("Critical Angle", f'{result["critical_angle_deg"]}\u00b0')
        rcol3.metric("Utilization", f'{result["utilization"]:.2%}')
    elif result["method"] == "mwcm":
        rcol1.metric("Equivalent Stress", f'{result["equivalent_stress_range"]:.1f} MPa')
        rcol2.metric("Biaxiality Ratio", f'{result["biaxiality_ratio"]:.3f}')
        rcol3.metric("Utilization", f'{result["utilization"]:.2%}')

    # ── Interaction diagram ───────────────────────────────────────────────
    st.subheader(t("interaction_diagram"))

    import plotly.graph_objects as go

    fig = go.Figure()
    theta = np.linspace(0, np.pi / 2, 100)

    if result["method"] == "gough_pollard":
        m_sn = 3.0
        delta_sigma_R = fat_sigma * (2e6 / max(num_cycles, 1)) ** (1.0 / m_sn)
        delta_tau_R = fat_tau * (2e6 / max(num_cycles, 1)) ** (1.0 / m_sn)

        fig.add_trace(go.Scatter(
            x=delta_sigma_R * np.cos(theta),
            y=delta_tau_R * np.sin(theta),
            mode="lines", name=t("interaction_envelope"),
            line={"color": "blue", "width": 2},
            fill="tozeroy", fillcolor="rgba(0, 128, 255, 0.08)",
        ))
        fig.add_trace(go.Scatter(
            x=[delta_sigma], y=[delta_tau],
            mode="markers+text", name=t("operating_point"),
            marker={"color": "red", "size": 12, "symbol": "x"},
            text=[f"({delta_sigma:.0f}, {delta_tau:.0f})"],
            textposition="top right",
        ))
        fig.update_layout(
            xaxis_title=t("normal_stress_range") + " [MPa]",
            yaxis_title=t("shear_stress_range") + " [MPa]",
        )
    else:
        util_val = result["utilization"]
        label = f"{method_label} Utilization"
        fig.add_trace(go.Bar(
            x=[label], y=[util_val],
            marker_color="green" if util_val <= 1.0 else "red",
            text=[f"{util_val:.2%}"], textposition="auto",
        ))
        fig.add_hline(y=1.0, line_dash="dash", line_color="black",
                      annotation_text="Limit = 1.0")
        fig.update_layout(yaxis_title="Utilization Ratio")

    fig.update_layout(
        title=f"Multiaxial Assessment - {method_label}",
        height=450,
    )
    st.plotly_chart(fig, use_container_width=True, key="mx_diagram")

    with st.expander(t("detailed_results"), expanded=False):
        import pandas as pd
        df = pd.DataFrame([
            {"Parameter": k, "Value": str(v)} for k, v in result.items()
        ])
        st.dataframe(df, hide_index=True)
