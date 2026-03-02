"""Fracture mechanics (LEFM crack growth) view."""

import streamlit as st
import numpy as np

from i18n import t
from weldfatigue.fatigue.fracture_mechanics import FractureMechanicsAssessment


def render(material_type: str) -> None:
    """Render fracture mechanics sidebar config and main content."""

    fm = FractureMechanicsAssessment()

    # ── Sidebar config ────────────────────────────────────────────────────
    st.sidebar.markdown("---")
    st.sidebar.subheader(t("crack_growth_params"))

    environment = st.sidebar.selectbox(
        t("environment"), ["air", "seawater"], index=0, key="fm_env",
    )

    defaults = FractureMechanicsAssessment.get_paris_parameters(
        material_type, environment,
    )

    st.sidebar.markdown("---")
    st.sidebar.caption("**Paris Law:** da/dN = C (\u0394K)\u1d50")
    C_param = st.sidebar.number_input(
        "C (Paris constant)", value=defaults["C"],
        min_value=1e-20, max_value=1e-5, step=1e-14,
        format="%.2e", key="fm_C",
        help="Paris law coefficient. Units: mm/cycle per (MPa \u221amm)^m.",
    )
    m_param = st.sidebar.number_input(
        "m (Paris exponent)", value=defaults["m"],
        min_value=1.0, max_value=10.0, step=0.1, key="fm_m",
    )

    default_dKth = FractureMechanicsAssessment.DELTA_K_TH.get(material_type, 63.0)
    delta_K_th = st.sidebar.number_input(
        "\u0394K threshold (MPa \u221amm)", value=default_dKth,
        min_value=0.0, step=1.0, key="fm_dKth",
        help="Below this value no crack growth occurs.",
    )

    weld_geometry = st.sidebar.selectbox(
        t("weld_geometry"), ["t_butt", "cruciform", "lap", "fillet"],
        index=0, key="fm_geom",
        format_func=lambda x: x.replace("_", " ").title(),
    )

    # ── Main content ──────────────────────────────────────────────────────
    st.markdown(t("fracture_desc"))

    col1, col2 = st.columns(2)

    with col1:
        st.subheader(t("geometry_loading"))
        initial_crack = st.number_input(
            "a\u2080 (mm)", value=0.5,
            min_value=0.01, step=0.1, key="fm_a0",
            help=t("initial_crack_help"),
        )
        critical_crack = st.number_input(
            "a\u1d9c (mm)", value=5.0,
            min_value=0.1, step=0.5, key="fm_ac",
            help=t("critical_crack_help"),
        )
        plate_thickness = st.number_input(
            t("plate_thickness") + " (mm)", value=10.0,
            min_value=1.0, step=1.0, key="fm_thick",
        )
        stress_range = st.number_input(
            t("stress_range") + " (MPa)", value=100.0,
            min_value=0.1, step=1.0, key="fm_stress",
        )

    with col2:
        st.subheader(t("initial_conditions"))
        Y0 = fm.geometry_factor_Y(initial_crack, plate_thickness)
        Mk0 = fm.Mk_factor(initial_crack, plate_thickness, weld_geometry)
        dK0 = fm.stress_intensity_factor(stress_range, initial_crack, Y0, Mk0)

        st.metric("Y(a\u2080/t)", f"{Y0:.3f}")
        st.metric("Mk(a\u2080)", f"{Mk0:.3f}")
        st.metric("\u0394K\u2080 (MPa \u221amm)", f"{dK0:.1f}")

        if dK0 < delta_K_th:
            st.warning(t("below_threshold_warning"))

    # ── Run analysis ──────────────────────────────────────────────────────
    if st.button(t("run_assessment"), type="primary", key="fm_run"):
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
                C=C_param, m=m_param, delta_K_th=delta_K_th,
            )
            st.session_state["fm_result"] = result

    # ── Display results ───────────────────────────────────────────────────
    if "fm_result" not in st.session_state:
        return

    result = st.session_state["fm_result"]
    st.markdown("---")
    st.subheader(t("results"))

    status_text = result["status"]
    if status_text == "COMPLETE":
        _cls = "fail"
        status_display = t("crack_grows_critical")
    else:
        _cls = "pass"
        status_display = t("crack_arrested")

    st.markdown(
        f'<div class="result-strip {_cls}">'
        f"<span>{status_display}</span>"
        f'<span>N = {result["total_cycles"]:,.0f} cycles</span></div>',
        unsafe_allow_html=True,
    )

    mcol1, mcol2, mcol3, mcol4 = st.columns(4)
    mcol1.metric(t("propagation_life"), f'{result["total_cycles"]:,.0f}')
    mcol2.metric("\u0394K initial", f'{result["delta_K_initial"]:.1f}')
    mcol3.metric("\u0394K final", f'{result["delta_K_final"]:.1f}')
    mcol4.metric("Status", status_text)

    # ── Crack growth curve ────────────────────────────────────────────────
    st.subheader(t("crack_growth_curve"))
    import plotly.graph_objects as go

    a_arr = np.array(result["crack_sizes"])
    N_arr = np.array(result["cycle_counts"])

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=N_arr, y=a_arr,
        mode="lines", name="a(N)",
        line={"color": "crimson", "width": 2},
    ))
    fig.add_hline(y=critical_crack, line_dash="dash", line_color="black",
                  annotation_text=f"a\u1d9c = {critical_crack} mm")
    fig.add_hline(y=initial_crack, line_dash="dot", line_color="grey",
                  annotation_text=f"a\u2080 = {initial_crack} mm")
    fig.update_layout(
        title=t("crack_growth_curve"),
        xaxis_title=t("plot_cycles_axis"),
        yaxis_title="a (mm)",
        height=450,
    )
    st.plotly_chart(fig, use_container_width=True, key="fm_curve")

    with st.expander(t("detailed_results"), expanded=False):
        import pandas as pd
        step = max(1, len(result["crack_sizes"]) // 50)
        df = pd.DataFrame({
            "Cycle Count": [f"{n:,.0f}" for n in result["cycle_counts"][::step]],
            "Crack Size (mm)": [f"{a:.3f}" for a in result["crack_sizes"][::step]],
        })
        st.dataframe(df, hide_index=True)
