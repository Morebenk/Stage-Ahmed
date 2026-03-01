"""Shock/Crash Analysis - Streamlit page."""

import streamlit as st
import numpy as np
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from i18n import t, format_family, FAMILY_KEYS
from components.sidebar import render_sidebar
from components.summary_panels import (
    render_shock_dynamic_summary, render_weld_check_summary,
    render_energy_summary,
)

from weldfatigue.materials.database import MaterialDatabase
from weldfatigue.shock.dynamic_material import DynamicMaterialModel
from weldfatigue.shock.weld_failure import WeldFailureCriteria
from weldfatigue.shock.energy import EnergyAbsorption
from weldfatigue.reporting.plots import ShockPlots

st.set_page_config(page_title="Shock Analysis", layout="wide")

render_sidebar()

st.title(t("crash_shock_assessment"))

db = MaterialDatabase()

# Sidebar
st.sidebar.header(t("configuration"))
family = st.sidebar.selectbox(
    t("material_family"), FAMILY_KEYS, format_func=format_family,
)
grades = db.list_grades(family)
material_name = st.sidebar.selectbox(t("material_grade"), grades)
material = db.get(material_name)

model_type = st.sidebar.radio(t("strain_rate_model"), ["Cowper-Symonds", "Johnson-Cook"])
model_key = "cowper_symonds" if model_type == "Cowper-Symonds" else "johnson_cook"

# ── Translated plot label helpers ─────────────────────────────────────────
def _dyn_yield_labels(name):
    return {
        "title": t("plot_dynamic_yield_title", name=name),
        "xaxis": t("plot_strain_rate_axis"),
        "yaxis": t("plot_yield_stress_axis"),
        "static_yield": t("plot_static_yield"),
    }

def _fd_labels():
    return {
        "title": t("plot_fd_title"),
        "xaxis": t("plot_displacement_axis"),
        "yaxis": t("plot_force_axis"),
        "trace": t("plot_fd_trace"),
        "mean_fmt": t("plot_mean_annotation"),
        "peak_fmt": t("plot_peak_annotation"),
    }

# Tabs
tab1, tab2, tab3 = st.tabs([
    t("dynamic_material_properties"), t("weld_failure_check"), t("energy_absorption"),
])

# ══════════════════════════════════════════════════════════════════════════
# TAB 1 — Dynamic Material Properties
# ══════════════════════════════════════════════════════════════════════════
with tab1:
    st.subheader(t("dynamic_material_properties"))
    col1, col2 = st.columns(2)

    _dyn_computed = False
    with col1:
        strain_rate = st.number_input(t("strain_rate"), value=100.0, min_value=0.0, step=10.0)
        temperature = st.number_input(t("temperature"), value=293.0, min_value=0.0, step=1.0)

        dyn_model = DynamicMaterialModel(material)
        try:
            dyn_yield = dyn_model.dynamic_yield(strain_rate, model_key)
            dif = dyn_model.dynamic_increase_factor(strain_rate, model_key)

            # ── Result strip ──
            st.markdown(
                f'<div class="result-strip pass">'
                f'<span>DIF = {dif:.3f}</span>'
                f'<span>{dyn_yield:.1f} MPa</span></div>',
                unsafe_allow_html=True,
            )
            st.metric(t("static_yield"), f"{material.yield_strength} MPa")
            st.metric(t("dynamic_yield"), f"{dyn_yield:.1f} MPa")

            st.session_state["shock_result"] = {
                "dynamic_yield": dyn_yield,
                "dif": dif,
                "material_name": material_name,
                "strain_rate": strain_rate,
                "model": model_key,
            }
            _dyn_computed = True

        except ValueError as e:
            st.error(str(e))

    with col2:
        fig = ShockPlots.dynamic_yield_vs_strain_rate_plotly(
            material.name, material.yield_strength, material.cs_D, material.cs_q,
            labels=_dyn_yield_labels(material.name),
        )
        st.plotly_chart(fig, key="shock_dynamic_yield")

    # ── Rich summary panel (full width, BELOW both columns) ──────────────
    if _dyn_computed:
        html = render_shock_dynamic_summary(
            static_yield=material.yield_strength,
            dynamic_yield=dyn_yield,
            dif=dif,
            strain_rate=strain_rate,
        )
        st.markdown(html, unsafe_allow_html=True)

    # Flow curves at multiple strain rates
    if material.jc_A is not None:
        st.markdown("---")
        st.subheader(t("flow_curves_jc"))
        rates = [0.001, 1, 10, 100, 1000]
        import plotly.graph_objects as go_
        fig_flow = go_.Figure()
        for rate in rates:
            try:
                strains, stresses = dyn_model.dynamic_flow_curve(
                    rate, temperature=temperature
                )
                fig_flow.add_trace(go_.Scatter(
                    x=strains, y=stresses, mode="lines",
                    name=f"{rate} /s",
                ))
            except ValueError:
                pass
        fig_flow.update_layout(
            title=t("true_stress_vs_plastic_strain"),
            xaxis={"title": t("plastic_strain")},
            yaxis={"title": t("true_stress")},
            template="plotly_white",
        )
        st.plotly_chart(fig_flow, key="jc_flow_curves")

# ══════════════════════════════════════════════════════════════════════════
# TAB 2 — Weld Failure Check
# ══════════════════════════════════════════════════════════════════════════
with tab2:
    st.subheader(t("weld_failure_check"))
    criterion = st.radio(t("criterion"), [t("force_based"), t("stress_based_en1993")])

    if criterion == t("force_based"):
        col1, col2 = st.columns(2)
        with col1:
            normal_force = st.number_input(t("normal_force"), value=500.0)
            shear_force = st.number_input(t("shear_force"), value=300.0)
            weld_throat = st.number_input(t("weld_throat"), value=5.0, min_value=0.1)
        with col2:
            weld_length = st.number_input(t("weld_length"), value=100.0, min_value=0.1)
            allowable_stress = st.number_input(t("allowable_stress"), value=float(material.ultimate_strength))
            safety_factor = st.number_input(t("safety_factor"), value=1.25, min_value=1.0)

        if st.button(t("check_weld"), type="primary"):
            result = WeldFailureCriteria.force_based_check(
                normal_force, shear_force, weld_throat,
                weld_length, allowable_stress, safety_factor,
            )

            # ── Result strip ──
            _w_cls = "pass" if result.status == "PASS" else "fail"
            st.markdown(
                f'<div class="result-strip {_w_cls}">'
                f'<span>{result.status}</span>'
                f'<span>U = {result.utilization:.3f}</span></div>',
                unsafe_allow_html=True,
            )

            st.session_state["shock_weld_result"] = {
                "equivalent_stress": result.equivalent_stress,
                "allowable_stress": result.allowable_stress,
                "utilization": result.utilization,
                "status": result.status,
                "criterion": "force_based",
            }

            # ── Rich panel ──
            html = render_weld_check_summary(
                equiv_stress=result.equivalent_stress,
                allowable=result.allowable_stress,
                utilization=result.utilization,
                status=result.status,
                weld_throat=weld_throat,
                weld_length=weld_length,
                normal_force=normal_force,
                shear_force=shear_force,
            )
            st.markdown(html, unsafe_allow_html=True)

    else:
        col1, col2 = st.columns(2)
        with col1:
            sigma_perp = st.number_input(t("sigma_perp"), value=150.0)
            tau_perp = st.number_input(t("tau_perp"), value=80.0)
            tau_parallel = st.number_input(t("tau_parallel"), value=60.0)
        with col2:
            fu = st.number_input(t("fu_uts"), value=float(material.ultimate_strength))
            beta_w = st.number_input("Beta_w", value=0.8, min_value=0.1)
            gamma_Mw = st.number_input("Gamma_Mw", value=1.25, min_value=1.0)

        if st.button(t("check_weld_stress"), type="primary"):
            result = WeldFailureCriteria.stress_based_check(
                sigma_perp, tau_perp, tau_parallel, fu, beta_w, gamma_Mw
            )

            # ── Result strip ──
            _w_cls = "pass" if result.status == "PASS" else "fail"
            st.markdown(
                f'<div class="result-strip {_w_cls}">'
                f'<span>{result.status}</span>'
                f'<span>U = {result.utilization:.3f}</span></div>',
                unsafe_allow_html=True,
            )

            st.session_state["shock_weld_result"] = {
                "equivalent_stress": result.equivalent_stress,
                "allowable_stress": result.allowable_stress,
                "utilization": result.utilization,
                "status": result.status,
                "criterion": "stress_based_EN1993",
            }

            # ── Rich panel ──
            html = render_weld_check_summary(
                equiv_stress=result.equivalent_stress,
                allowable=result.allowable_stress,
                utilization=result.utilization,
                status=result.status,
            )
            st.markdown(html, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════
# TAB 3 — Energy Absorption
# ══════════════════════════════════════════════════════════════════════════
with tab3:
    st.subheader(t("energy_absorption_analysis"))
    st.markdown(t("upload_or_enter_fd_data"))

    input_method = st.radio(t("input_method"), [t("manual_sample"), t("upload_csv")])

    if input_method == t("manual_sample"):
        # Generate sample crush curve
        disp = np.linspace(0, 100, 200)
        force = 50000 * (1 + 0.3 * np.sin(disp / 5)) * np.exp(-disp / 200)
        force[0:5] = np.linspace(0, force[5], 5)

        mass = st.number_input(t("component_mass"), value=2.5, min_value=0.01)

        metrics = EnergyAbsorption.crush_metrics(force, disp, mass)

        # ── Key metrics ──
        col1, col2 = st.columns(2)
        with col1:
            st.metric(t("total_energy"), f"{metrics.total_energy:.0f} J")
            st.metric("SEA", f"{metrics.specific_energy_absorption:.0f} J/kg")
        with col2:
            st.metric(t("peak_force"), f"{metrics.peak_force:.0f} N")
            st.metric("CFE", f"{metrics.crush_force_efficiency:.3f}")

        st.session_state["shock_energy_result"] = metrics.model_dump()

        # ── Plot FIRST, then summary below ──
        fig = ShockPlots.force_displacement_plotly(
            force, disp, metrics.model_dump(),
            labels=_fd_labels(),
        )
        st.plotly_chart(fig, key="force_disp_plot")

        # ── Rich energy panel ──
        total_stroke = disp[-1] - disp[0]
        energy_per_mm = metrics.total_energy / total_stroke if total_stroke > 0 else 0
        html = render_energy_summary(
            total_energy=metrics.total_energy,
            sea=metrics.specific_energy_absorption,
            mean_force=metrics.mean_force,
            peak_force=metrics.peak_force,
            cfe=metrics.crush_force_efficiency,
            energy_per_mm=energy_per_mm,
            stroke=total_stroke,
            mass=mass,
        )
        st.markdown(html, unsafe_allow_html=True)

    else:
        uploaded = st.file_uploader(t("upload_fd_csv"), type=["csv"])
        if uploaded:
            import pandas as pd
            df = pd.read_csv(uploaded)
            st.dataframe(df.head())
            if "force" in df.columns and "displacement" in df.columns:
                force = df["force"].values
                disp = df["displacement"].values
                mass = st.number_input(t("component_mass"), value=1.0, min_value=0.01)
                metrics = EnergyAbsorption.crush_metrics(force, disp, mass)

                # ── Key metrics ──
                st.metric(t("total_energy"), f"{metrics.total_energy:.0f} J")
                st.metric("SEA", f"{metrics.specific_energy_absorption:.0f} J/kg")
                st.metric(t("peak_force"), f"{metrics.peak_force:.0f} N")
                st.metric("CFE", f"{metrics.crush_force_efficiency:.3f}")
                st.session_state["shock_energy_result"] = metrics.model_dump()

                # ── Plot FIRST ──
                fig = ShockPlots.force_displacement_plotly(
                    force, disp, metrics.model_dump(),
                    labels=_fd_labels(),
                )
                st.plotly_chart(fig, key="force_disp_csv")

                # ── Rich energy panel ──
                total_stroke = disp[-1] - disp[0]
                energy_per_mm = metrics.total_energy / total_stroke if total_stroke > 0 else 0
                html = render_energy_summary(
                    total_energy=metrics.total_energy,
                    sea=metrics.specific_energy_absorption,
                    mean_force=metrics.mean_force,
                    peak_force=metrics.peak_force,
                    cfe=metrics.crush_force_efficiency,
                    energy_per_mm=energy_per_mm,
                    stroke=total_stroke,
                    mass=mass,
                )
                st.markdown(html, unsafe_allow_html=True)
