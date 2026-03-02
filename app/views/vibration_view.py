"""Vibration fatigue (frequency-domain PSD) view."""

import streamlit as st
import numpy as np

from i18n import t
from weldfatigue.fatigue.vibration_fatigue import VibrationFatigueAssessment


def render(material_type: str) -> None:
    """Render vibration fatigue sidebar config and main content."""

    # ── Sidebar config ────────────────────────────────────────────────────
    st.sidebar.markdown("---")
    st.sidebar.subheader(t("vibration_params"))

    fat_class = st.sidebar.number_input(
        t("fat_class"), value=71,
        min_value=36, max_value=225, step=1, key="vf_fat",
    )
    duration = st.sidebar.number_input(
        t("duration_seconds"), value=3600.0,
        min_value=0.1, step=100.0, key="vf_duration",
        help=t("duration_help"),
    )
    st.sidebar.markdown("---")
    damage_limit = st.sidebar.select_slider(
        t("damage_limit"),
        options=[0.5, 0.6, 0.7, 0.8, 1.0],
        value=1.0, key="vf_dlim",
    )

    # ── PSD input ─────────────────────────────────────────────────────────
    st.markdown(t("vibration_desc"))

    input_mode = st.radio(
        t("psd_input_mode"),
        [t("psd_example"), t("psd_manual"), t("psd_csv")],
        horizontal=True, key="vf_input_mode",
    )

    frequencies = None
    psd_values = None

    if input_mode == t("psd_example"):
        st.info(t("psd_example_info"))
        frequencies = np.linspace(5, 500, 200)
        psd_values = np.ones_like(frequencies) * 1.0

    elif input_mode == t("psd_manual"):
        st.markdown(t("psd_manual_info"))
        default_text = "5, 0.1\n20, 1.0\n50, 2.5\n100, 2.5\n200, 1.0\n500, 0.1"
        csv_text = st.text_area(
            t("psd_manual_label"), value=default_text, height=200,
            key="vf_manual_text",
        )
        if csv_text.strip():
            try:
                lines = [
                    line.strip()
                    for line in csv_text.strip().split("\n")
                    if line.strip()
                ]
                data = []
                for line in lines:
                    parts = line.split(",")
                    if len(parts) >= 2:
                        data.append((
                            float(parts[0].strip()),
                            float(parts[1].strip()),
                        ))
                if len(data) >= 2:
                    data.sort(key=lambda x: x[0])
                    frequencies = np.array([d[0] for d in data])
                    psd_values = np.array([d[1] for d in data])
                else:
                    st.warning(t("psd_need_points"))
            except ValueError:
                st.error(t("psd_parse_error"))

    elif input_mode == t("psd_csv"):
        uploaded = st.file_uploader(
            t("psd_csv_upload"), type=["csv", "txt"], key="vf_csv_upload",
        )
        if uploaded is not None:
            try:
                import pandas as pd
                df_upload = pd.read_csv(uploaded)
                if len(df_upload.columns) >= 2:
                    frequencies = df_upload.iloc[:, 0].values.astype(float)
                    psd_values = df_upload.iloc[:, 1].values.astype(float)
                    st.success(f"{len(frequencies)} data points loaded.")
                else:
                    st.error(t("psd_csv_error"))
            except Exception as e:
                st.error(f"Error reading CSV: {e}")

    # ── PSD plot ──────────────────────────────────────────────────────────
    if frequencies is not None and psd_values is not None:
        import plotly.graph_objects as go

        fig_psd = go.Figure()
        fig_psd.add_trace(go.Scatter(
            x=frequencies, y=psd_values,
            mode="lines", name="PSD",
            line={"color": "steelblue", "width": 2},
            fill="tozeroy", fillcolor="rgba(70, 130, 180, 0.15)",
        ))
        fig_psd.update_layout(
            title=t("psd_input_title"),
            xaxis_title=t("psd_freq_axis"),
            yaxis_title=t("psd_value_axis"),
            height=350,
        )
        st.plotly_chart(fig_psd, use_container_width=True, key="vf_psd_plot")

        # ── Run assessment ────────────────────────────────────────────────
        if st.button(t("run_assessment"), type="primary", key="vf_run"):
            result = VibrationFatigueAssessment.evaluate(
                frequencies=frequencies,
                psd=psd_values,
                duration=duration,
                fat_class=fat_class,
                material_type=material_type,
            )
            st.session_state["vib_fatigue_result"] = result

    # ── Display results ───────────────────────────────────────────────────
    if "vib_fatigue_result" not in st.session_state:
        if frequencies is None:
            st.info(t("psd_provide_input"))
        return

    result = st.session_state["vib_fatigue_result"]
    st.markdown("---")
    st.subheader(t("results"))

    D_dirlik = result["damage_dirlik"]
    _cls = "pass" if D_dirlik <= damage_limit else "fail"
    _status = "PASS" if D_dirlik <= damage_limit else "FAIL"

    st.markdown(
        f'<div class="result-strip {_cls}">'
        f"<span>{_status}</span>"
        f'<span>Dirlik D = {D_dirlik:.4f} / {damage_limit}</span></div>',
        unsafe_allow_html=True,
    )

    mcol1, mcol2, mcol3 = st.columns(3)
    mcol1.metric("Dirlik", f"{D_dirlik:.4e}")
    mcol2.metric("Narrow-Band", f'{result["damage_narrowband"]:.4e}')
    mcol3.metric("Wirsching-Light", f'{result["damage_wirsching"]:.4e}')

    mcol4, mcol5, mcol6 = st.columns(3)
    mcol4.metric(t("equivalent_stress"), f'{result["equivalent_stress_range"]:.1f} MPa')
    mcol5.metric(t("peak_rate"), f'{result["expected_peak_rate"]:.1f} Hz')
    mcol6.metric(t("irregularity_factor"), f'{result["irregularity_factor"]:.3f}')

    with st.expander(t("spectral_moments"), expanded=False):
        import pandas as pd
        m = result["spectral_moments"]
        params_data = [
            {"Parameter": "m\u2080 (variance)", "Value": f'{m["m0"]:.4e}'},
            {"Parameter": "m\u2081", "Value": f'{m["m1"]:.4e}'},
            {"Parameter": "m\u2082", "Value": f'{m["m2"]:.4e}'},
            {"Parameter": "m\u2084", "Value": f'{m["m4"]:.4e}'},
            {"Parameter": "\u03b3 (irregularity)", "Value": f'{result["irregularity_factor"]:.4f}'},
            {"Parameter": "E[P] (Hz)", "Value": f'{result["expected_peak_rate"]:.2f}'},
        ]
        st.dataframe(pd.DataFrame(params_data), hide_index=True)

    # ── Damage comparison bar chart ───────────────────────────────────────
    st.subheader(t("damage_comparison"))
    import plotly.graph_objects as go

    methods = ["Dirlik", "Narrow-Band", "Wirsching-Light"]
    damages = [
        result["damage_dirlik"],
        result["damage_narrowband"],
        result["damage_wirsching"],
    ]
    colors = ["green" if d <= damage_limit else "red" for d in damages]

    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        x=methods, y=damages,
        marker_color=colors,
        text=[f"{d:.4e}" for d in damages],
        textposition="auto",
    ))
    fig_bar.add_hline(
        y=damage_limit, line_dash="dash", line_color="black",
        annotation_text=f"D_lim = {damage_limit}",
    )
    fig_bar.update_layout(
        title=t("damage_by_method"),
        yaxis_title="Cumulative Damage D",
        height=400,
    )
    st.plotly_chart(fig_bar, use_container_width=True, key="vf_damage_bar")
