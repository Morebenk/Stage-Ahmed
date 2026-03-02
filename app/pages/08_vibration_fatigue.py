"""Vibration Fatigue (Frequency Domain) - Streamlit page."""

import streamlit as st
import numpy as np
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from i18n import t
from components.sidebar import render_sidebar

try:
    from weldfatigue.fatigue.vibration_fatigue import VibrationFatigueAssessment
except ImportError:
    VibrationFatigueAssessment = None

st.set_page_config(page_title="Vibration Fatigue", layout="wide")
render_sidebar()

st.title("Vibration Fatigue Assessment")
st.markdown(
    "Frequency-domain fatigue analysis from Power Spectral Density (PSD) input. "
    "Computes Palmgren-Miner damage using Dirlik, narrow-band, and Wirsching-Light methods."
)

if VibrationFatigueAssessment is None:
    st.error(
        "Could not import `VibrationFatigueAssessment`. "
        "Please verify that the `weldfatigue` package is installed."
    )
    st.stop()

# ── Sidebar inputs ────────────────────────────────────────────────────────
st.sidebar.header("Vibration Fatigue Parameters")

fat_class = st.sidebar.number_input(
    "FAT Class", value=71, min_value=36, max_value=225, step=1,
)
material_type = st.sidebar.selectbox(
    "Material Type", ["steel", "aluminum"], index=0,
)
duration = st.sidebar.number_input(
    "Duration (seconds)", value=3600.0, min_value=0.1, step=100.0,
    help="Total exposure duration in seconds.",
)

st.sidebar.markdown("---")
st.sidebar.subheader("Damage Limit")
damage_limit = st.sidebar.select_slider(
    "Allowable Damage D_lim",
    options=[0.5, 0.6, 0.7, 0.8, 1.0],
    value=1.0,
)

# ── PSD input ─────────────────────────────────────────────────────────────
st.subheader("PSD Input")

input_mode = st.radio(
    "Input Mode",
    ["Example PSD (flat broadband)", "Manual Entry", "CSV Upload"],
    horizontal=True,
)

frequencies = None
psd_values = None

if input_mode == "Example PSD (flat broadband)":
    st.info(
        "Using a flat PSD of 1.0 MPa^2/Hz between 5 Hz and 500 Hz "
        "as a demonstration input."
    )
    frequencies = np.linspace(5, 500, 200)
    psd_values = np.ones_like(frequencies) * 1.0

elif input_mode == "Manual Entry":
    st.markdown(
        "Enter frequency and PSD values as comma-separated lines. "
        "Each line: `frequency, PSD_value`"
    )
    default_text = (
        "5, 0.1\n"
        "20, 1.0\n"
        "50, 2.5\n"
        "100, 2.5\n"
        "200, 1.0\n"
        "500, 0.1"
    )
    csv_text = st.text_area("Frequency, PSD (one pair per line)", value=default_text, height=200)
    if csv_text.strip():
        try:
            lines = [line.strip() for line in csv_text.strip().split("\n") if line.strip()]
            data = []
            for line in lines:
                parts = line.split(",")
                if len(parts) >= 2:
                    data.append((float(parts[0].strip()), float(parts[1].strip())))
            if len(data) >= 2:
                data.sort(key=lambda x: x[0])
                frequencies = np.array([d[0] for d in data])
                psd_values = np.array([d[1] for d in data])
            else:
                st.warning("Need at least 2 data points.")
        except ValueError:
            st.error("Could not parse input. Use the format: `frequency, PSD_value`")

elif input_mode == "CSV Upload":
    uploaded = st.file_uploader(
        "Upload CSV (columns: frequency, PSD)", type=["csv", "txt"],
    )
    if uploaded is not None:
        try:
            import pandas as pd
            df_upload = pd.read_csv(uploaded)
            if len(df_upload.columns) >= 2:
                frequencies = df_upload.iloc[:, 0].values.astype(float)
                psd_values = df_upload.iloc[:, 1].values.astype(float)
                st.success(f"Loaded {len(frequencies)} data points.")
            else:
                st.error("CSV must have at least 2 columns (frequency, PSD).")
        except Exception as e:
            st.error(f"Error reading CSV: {e}")

# ── Plot PSD input ────────────────────────────────────────────────────────
if frequencies is not None and psd_values is not None:
    st.subheader("PSD Input Plot")
    try:
        import plotly.graph_objects as go

        fig_psd = go.Figure()
        fig_psd.add_trace(go.Scatter(
            x=frequencies, y=psd_values,
            mode="lines", name="PSD",
            line=dict(color="steelblue", width=2),
            fill="tozeroy", fillcolor="rgba(70, 130, 180, 0.15)",
        ))
        fig_psd.update_layout(
            title="Input Power Spectral Density",
            xaxis_title="Frequency (Hz)",
            yaxis_title="PSD (MPa^2 / Hz)",
            height=350,
        )
        st.plotly_chart(fig_psd, use_container_width=True, key="psd_input_plot")

    except ImportError:
        st.warning("Install `plotly` to display the PSD plot.")

    # ── Run assessment ────────────────────────────────────────────────────
    if st.button("Run Vibration Fatigue Assessment", type="primary"):
        result = VibrationFatigueAssessment.evaluate(
            frequencies=frequencies,
            psd=psd_values,
            duration=duration,
            fat_class=fat_class,
            material_type=material_type,
        )
        st.session_state["vib_fatigue_result"] = result

# ── Display results ───────────────────────────────────────────────────────
if "vib_fatigue_result" in st.session_state:
    result = st.session_state["vib_fatigue_result"]
    st.markdown("---")
    st.subheader("Results")

    # Status strip
    D_dirlik = result["damage_dirlik"]
    _cls = "pass" if D_dirlik <= damage_limit else "fail"
    _status = "PASS" if D_dirlik <= damage_limit else "FAIL"

    st.markdown(
        f'<div class="result-strip {_cls}">'
        f"<span>{_status}</span>"
        f'<span>Dirlik Damage D = {D_dirlik:.4f} / {damage_limit}</span></div>',
        unsafe_allow_html=True,
    )

    # Metrics row
    mcol1, mcol2, mcol3 = st.columns(3)
    mcol1.metric("Dirlik Damage", f"{D_dirlik:.4e}")
    mcol2.metric("Narrow-Band Damage", f'{result["damage_narrowband"]:.4e}')
    mcol3.metric("Wirsching-Light Damage", f'{result["damage_wirsching"]:.4e}')

    mcol4, mcol5, mcol6 = st.columns(3)
    mcol4.metric("Equivalent Stress Range", f'{result["equivalent_stress_range"]:.1f} MPa')
    mcol5.metric("Expected Peak Rate", f'{result["expected_peak_rate"]:.1f} Hz')
    mcol6.metric("Irregularity Factor", f'{result["irregularity_factor"]:.3f}')

    # ── Spectral moments table ────────────────────────────────────────────
    with st.expander("Spectral Moments & Bandwidth Parameters", expanded=False):
        import pandas as pd
        m = result["spectral_moments"]
        params_data = [
            {"Parameter": "m0 (variance)", "Value": f'{m["m0"]:.4e}'},
            {"Parameter": "m1", "Value": f'{m["m1"]:.4e}'},
            {"Parameter": "m2", "Value": f'{m["m2"]:.4e}'},
            {"Parameter": "m4", "Value": f'{m["m4"]:.4e}'},
            {"Parameter": "Irregularity Factor (gamma)", "Value": f'{result["irregularity_factor"]:.4f}'},
            {"Parameter": "Expected Peak Rate E[P] (Hz)", "Value": f'{result["expected_peak_rate"]:.2f}'},
        ]
        st.dataframe(pd.DataFrame(params_data), hide_index=True)

    # ── Damage comparison bar chart ───────────────────────────────────────
    st.subheader("Damage Comparison")
    try:
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
            annotation_text=f"Damage Limit = {damage_limit}",
        )
        fig_bar.update_layout(
            title="Damage Estimates by Method",
            yaxis_title="Cumulative Damage D",
            height=400,
        )
        st.plotly_chart(fig_bar, use_container_width=True, key="vib_damage_bar")

    except ImportError:
        st.warning("Install `plotly` to display the damage comparison chart.")
else:
    if frequencies is None:
        st.info("Provide PSD input data above, then run the assessment.")
