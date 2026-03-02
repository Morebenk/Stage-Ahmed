"""Fatigue Analysis - Streamlit page.

Unified hub for all fatigue assessment modes:
  - Standard (IIW): nominal / hot-spot / notch stress
  - Multiaxial: Gough-Pollard / Findley / MWCM
  - Fracture Mechanics: LEFM crack growth (Paris law)
  - Vibration Fatigue: PSD-based frequency-domain analysis

Weld Quality (ISO 5817) is available as a tab within Standard mode.
"""

import streamlit as st
import numpy as np
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from i18n import (
    t, format_family, format_weld_type,
    format_load_type, format_msc,
    FAMILY_KEYS, WELD_TYPE_KEYS, LOAD_TYPE_KEYS, MSC_KEYS,
)
from components.sidebar import render_sidebar
from components.summary_panels import (
    render_fatigue_summary, render_miner_summary, render_sn_info_panel,
)

from weldfatigue.materials.database import MaterialDatabase
from weldfatigue.fatigue.sn_curve import SNCurve
from weldfatigue.fatigue.fat_classes import FATClassCatalog
from weldfatigue.fatigue.assessment import FatigueAssessment
from weldfatigue.reporting.plots import FatiguePlots

st.set_page_config(page_title="Fatigue Analysis", layout="wide")

render_sidebar()

st.title(t("fatigue_assessment"))

db = MaterialDatabase()
catalog = FATClassCatalog()

# ══════════════════════════════════════════════════════════════════════════
# MODE SELECTOR — horizontal radio at the top of main content
# ══════════════════════════════════════════════════════════════════════════
MODE_KEYS = ["standard", "multiaxial", "fracture", "vibration"]
MODE_LABELS = {
    "standard": t("mode_standard"),
    "multiaxial": t("mode_multiaxial"),
    "fracture": t("mode_fracture"),
    "vibration": t("mode_vibration"),
}

selected_mode = st.radio(
    t("analysis_mode"),
    MODE_KEYS,
    format_func=lambda k: MODE_LABELS[k],
    horizontal=True,
    key="fatigue_mode",
)

# ══════════════════════════════════════════════════════════════════════════
# SHARED SIDEBAR — Material selection (always visible)
# ══════════════════════════════════════════════════════════════════════════
st.sidebar.header(t("configuration"))

family = st.sidebar.selectbox(
    t("material_family"), FAMILY_KEYS, format_func=format_family,
)
grades = db.list_grades(family)
material_name = st.sidebar.selectbox(t("material_grade"), grades)
material = db.get(material_name)


# ══════════════════════════════════════════════════════════════════════════
# STANDARD (IIW) MODE
# ══════════════════════════════════════════════════════════════════════════
if selected_mode == "standard":
    # ── Standard sidebar config ───────────────────────────────────────────
    st.sidebar.markdown("---")
    method = st.sidebar.radio(
        t("assessment_method"),
        [t("nominal_stress"), t("hotspot_stress"), t("notch_stress")],
    )
    method_map = {
        t("nominal_stress"): "nominal",
        t("hotspot_stress"): "hotspot",
        t("notch_stress"): "notch",
    }
    method_key = method_map[method]

    weld_type = st.sidebar.selectbox(
        t("weld_type"), WELD_TYPE_KEYS, format_func=format_weld_type,
    )
    load_type = st.sidebar.selectbox(
        t("load_type"), LOAD_TYPE_KEYS, format_func=format_load_type,
    )

    recommended = catalog.recommend(weld_type, load_type, family)
    default_fat = recommended.fat_class if recommended else 71
    fat_class = st.sidebar.number_input(
        t("fat_class"), value=default_fat, min_value=36, max_value=225,
    )
    if recommended:
        st.sidebar.caption(
            f"{t('recommended')} : FAT {recommended.fat_class} - "
            f"{recommended.description}"
        )

    mean_correction = st.sidebar.selectbox(
        t("mean_stress_correction"), MSC_KEYS, format_func=format_msc,
    )
    variable_amplitude = st.sidebar.checkbox(t("variable_amplitude_loading"))

    st.sidebar.markdown("---")
    damage_limit = st.sidebar.select_slider(
        t("damage_limit"),
        options=[0.5, 0.6, 0.7, 0.8, 1.0],
        value=1.0,
    )
    st.sidebar.caption(t("damage_limit_help"))

    if method_key in ("hotspot", "notch") and mean_correction != "none":
        st.sidebar.warning(t("msc_not_applicable_for_method"))

    with st.sidebar.expander(t("method_explanation")):
        _help_keys = {
            "nominal": "help_nominal",
            "hotspot": "help_hotspot",
            "notch": "help_notch",
        }
        st.markdown(t(_help_keys[method_key]))

    with st.sidebar.expander(t("fat_class_guide")):
        st.markdown(t("fat_class_explanation"))

    # ── Plot label helpers ────────────────────────────────────────────────
    def _sn_labels():
        return {
            "xaxis": t("plot_cycles_axis"),
            "yaxis": t("plot_stress_range_axis"),
            "op_point": t("plot_operating_point"),
            "knee": t("plot_knee_point"),
        }

    def _damage_labels():
        return {
            "title": t("plot_damage_title"),
            "xaxis": t("plot_stress_range_label"),
            "yaxis": t("plot_damage_ratio_axis"),
        }

    def _haigh_labels():
        return {
            "title": t("plot_haigh_title"),
            "xaxis": t("plot_mean_stress_axis"),
            "yaxis": t("plot_stress_amplitude_axis"),
            "point_fmt": t("plot_point"),
        }

    # ── FEA import banner ─────────────────────────────────────────────────
    _prefill_stress = 100.0
    if "fea_hotspot_stress" in st.session_state:
        hs = st.session_state["fea_hotspot_stress"]
        hs_type = st.session_state.get("fea_hotspot_type", "a")
        with st.container(border=True):
            bcol1, bcol2 = st.columns([3, 1])
            with bcol1:
                st.markdown(f"**{t('fea_result_available')}**")
                st.markdown(
                    t("fea_hotspot_detected", stress=f"{hs:.1f}", hs_type=hs_type)
                )
            with bcol2:
                if st.button(t("import_from_fea"), type="primary"):
                    _prefill_stress = hs

    # ── Tabs ──────────────────────────────────────────────────────────────
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        t("single_load_block"),
        t("variable_amplitude_miner"),
        t("weld_quality_tab"),
        t("sn_curve_explorer"),
        t("fat_class_catalog"),
        t("haigh_diagram"),
    ])

    # ── TAB 1: Single Load Block Assessment ───────────────────────────────
    with tab1:
        st.subheader(t("single_block_assessment"))
        col1, col2 = st.columns(2)

        with col1:
            stress_range = st.number_input(
                t("stress_range"), value=_prefill_stress,
                min_value=0.1, step=1.0,
                help=t("help_stress_range"),
            )
            num_cycles = st.number_input(
                t("number_of_cycles"), value=2_000_000,
                min_value=1, step=1000,
                help=t("help_num_cycles"),
            )
            mean_stress = st.number_input(
                t("mean_stress"), value=0.0, step=1.0,
                help=t("help_mean_stress"),
            )

            if st.button(t("run_assessment"), type="primary"):
                assessor = FatigueAssessment(db, catalog)
                result = assessor.run_simple(
                    method=method_key,
                    material_name=material_name,
                    weld_type=weld_type,
                    load_type=load_type,
                    stress_range=stress_range,
                    num_cycles=num_cycles,
                    fat_class=fat_class,
                    mean_stress=mean_stress,
                    mean_stress_correction=mean_correction,
                    variable_amplitude=variable_amplitude,
                    damage_limit=damage_limit,
                )
                st.session_state["fatigue_result"] = result
                st.session_state["fatigue_last_mean_stress"] = mean_stress

        with col2:
            if "fatigue_result" in st.session_state:
                r = st.session_state["fatigue_result"]["single_block_result"]
                _strip_cls = "pass" if r["status"] == "PASS" else "fail"
                sf = r["safety_factor"]
                _sf_disp = f"SF = {sf:.2f}" if sf != float("inf") else "SF = \u221e"
                st.markdown(
                    f'<div class="result-strip {_strip_cls}">'
                    f'<span>{r["status"]}</span><span>{_sf_disp}</span></div>',
                    unsafe_allow_html=True,
                )
                _nf = r["allowable_cycles"]
                if _nf == float("inf"):
                    _nf_str = "\u221e"
                elif _nf < 1e9:
                    _nf_str = f"{int(_nf):,}"
                else:
                    _nf_str = f"{_nf:.2e}"
                st.metric(t("allowable_cycles"), _nf_str)
                st.metric(t("damage_ratio"), f"{r['damage_ratio']:.4f}")

        # S-N curve plot
        sn = SNCurve(fat_class, family, variable_amplitude)
        op_point = None
        if "fatigue_result" in st.session_state:
            r = st.session_state["fatigue_result"]["single_block_result"]
            if r["allowable_cycles"] != float("inf"):
                op_point = (num_cycles, stress_range)
        fig = FatiguePlots.sn_curve_plotly(
            sn, op_point,
            title=t("plot_sn_title", fat=sn.fat_class,
                     mat=format_family(sn.material_type)),
            labels=_sn_labels(),
        )
        st.plotly_chart(fig, key="sn_tab1")

        # Rich engineering summary
        if "fatigue_result" in st.session_state:
            r = st.session_state["fatigue_result"]["single_block_result"]
            D = r["damage_ratio"]
            sf = r["safety_factor"]
            N_allow = r["allowable_cycles"]
            allowable_stress = sn.stress_range_at_cycles(num_cycles)
            stress_margin = (
                (allowable_stress - stress_range) if allowable_stress > 0
                else float("inf")
            )

            sigma_max = mean_stress + stress_range / 2.0
            sigma_min = mean_stress - stress_range / 2.0
            sigma_a = stress_range / 2.0
            R_ratio = sigma_min / sigma_max if sigma_max != 0 else 0.0

            if abs(R_ratio + 1) < 0.01:
                load_desc = t("fully_reversed")
            elif abs(R_ratio) < 0.01:
                load_desc = t("pulsating_tension")
            elif 0 < R_ratio < 1:
                load_desc = t("tension_tension")
            elif R_ratio > 1 or R_ratio < -1:
                load_desc = t("compression_dominated")
            else:
                load_desc = t("general_loading", r=R_ratio)

            html = render_fatigue_summary(
                stress_range=stress_range, mean_stress=mean_stress,
                num_cycles=num_cycles,
                sigma_max=sigma_max, sigma_min=sigma_min,
                sigma_a=sigma_a, R=R_ratio, load_desc=load_desc,
                allowable_stress=allowable_stress,
                stress_margin=stress_margin,
                N_allow=N_allow, D=D, sf=sf,
                sn=sn, variable_amplitude=variable_amplitude,
            )
            st.markdown(html, unsafe_allow_html=True)

            # What-If Calculator
            with st.expander(
                f"\U0001f52c {t('what_if_calculator')}", expanded=False,
            ):
                wi_stress = st.slider(
                    t("what_if_stress_label"),
                    min_value=1.0,
                    max_value=float(max(500.0, stress_range * 3)),
                    value=float(stress_range),
                    step=1.0,
                    key="what_if_slider",
                )
                wi_N = sn.cycles_to_failure(wi_stress)
                wi_D = (
                    num_cycles / wi_N
                    if wi_N != float("inf") and wi_N > 0 else 0.0
                )
                wi_sf = 1.0 / wi_D if wi_D > 0 else float("inf")
                wi_status = "PASS" if wi_D <= damage_limit else "FAIL"
                _wi_cls = "pass" if wi_status == "PASS" else "fail"
                _wi_sf = (
                    f"SF = {wi_sf:.2f}" if wi_sf != float("inf")
                    else "SF = \u221e"
                )
                if wi_N == float("inf"):
                    _wi_nf = "\u221e"
                elif wi_N < 1e9:
                    _wi_nf = f"{int(wi_N):,}"
                else:
                    _wi_nf = f"{wi_N:.2e}"
                st.markdown(
                    f'<div class="result-strip {_wi_cls}">'
                    f'<span>\u0394\u03c3 = {wi_stress:.0f} MPa \u2192 '
                    f'{wi_status}</span>'
                    f'<span>D = {wi_D:.4f}  |  {_wi_sf}  |  '
                    f'N = {_wi_nf}</span></div>',
                    unsafe_allow_html=True,
                )

    # ── TAB 2: Variable Amplitude (Miner) ─────────────────────────────────
    with tab2:
        st.subheader(t("miner_assessment"))

        with st.expander(t("rainflow_from_signal"), expanded=False):
            st.markdown(t("rainflow_explanation"))
            sig_file = st.file_uploader(
                t("upload_time_signal"), type=["csv", "txt"],
                key="rf_upload",
            )
            if sig_file:
                import pandas as pd
                from weldfatigue.utils.rainflow import signal_to_spectrum
                sig_df = pd.read_csv(sig_file, header=None)
                sig_col = sig_df.columns[0]
                if len(sig_df.columns) > 1:
                    sig_col = st.selectbox(
                        t("signal_column"), sig_df.columns,
                    )
                signal = sig_df[sig_col].values
                n_bins = st.slider(
                    t("rainflow_bins"), 8, 128, 64, key="rf_bins",
                )
                rf_spectrum = signal_to_spectrum(signal, n_bins)
                rf_df = pd.DataFrame(
                    rf_spectrum,
                    columns=[t("stress_range"), t("number_of_cycles")],
                )
                st.dataframe(rf_df, hide_index=True)
                import plotly.express as px
                fig_rf = px.bar(
                    rf_df, x=t("stress_range"),
                    y=t("number_of_cycles"),
                    title=t("rainflow_spectrum"),
                )
                st.plotly_chart(fig_rf, key="rf_hist")
                if st.button(t("use_for_miner"), key="rf_apply"):
                    st.session_state["rainflow_spectrum"] = rf_spectrum
                    st.success(t("spectrum_loaded"))

        st.markdown("---")
        st.markdown(t("enter_load_spectrum"))

        rf_loaded = st.session_state.get("rainflow_spectrum")
        if rf_loaded:
            n_blocks = len(rf_loaded)
            st.info(f"Rainflow: {n_blocks} blocks loaded")
        else:
            n_blocks = st.number_input(
                t("number_load_blocks"), value=3,
                min_value=1, max_value=20,
            )

        spectrum = []
        for i in range(n_blocks):
            c1, c2 = st.columns(2)
            default_sr = (
                rf_loaded[i][0] if rf_loaded and i < len(rf_loaded)
                else 100.0 * (n_blocks - i) / n_blocks
            )
            default_nc = (
                int(rf_loaded[i][1]) if rf_loaded and i < len(rf_loaded)
                else 100000 * (i + 1)
            )
            with c1:
                sr = st.number_input(
                    t("block_stress_range", i=i + 1),
                    value=float(default_sr), key=f"sr_{i}",
                )
            with c2:
                nc = st.number_input(
                    t("block_cycles", i=i + 1),
                    value=default_nc, min_value=1, key=f"nc_{i}",
                )
            spectrum.append((sr, nc))

        if st.button(t("run_miner_assessment"), type="primary"):
            assessor = FatigueAssessment(db, catalog)
            result = assessor.run_simple(
                method=method_key,
                material_name=material_name,
                weld_type=weld_type,
                load_type=load_type,
                stress_range=spectrum[0][0],
                num_cycles=spectrum[0][1],
                fat_class=fat_class,
                variable_amplitude=True,
                load_spectrum=spectrum,
                damage_limit=damage_limit,
            )
            if "miner_result" in result:
                mr = result["miner_result"]

                _m_cls = "pass" if mr["status"] == "PASS" else "fail"
                st.markdown(
                    f'<div class="result-strip {_m_cls}">'
                    f'<span>{mr["status"]}</span>'
                    f'<span>D = {mr["total_damage"]:.4f} / '
                    f'{damage_limit}</span></div>',
                    unsafe_allow_html=True,
                )

                fig = FatiguePlots.damage_histogram_plotly(
                    mr["damage_per_block"],
                    [s[0] for s in spectrum],
                    labels=_damage_labels(),
                )
                st.plotly_chart(fig, key="miner_damage")

                sn = SNCurve(fat_class, family, variable_amplitude)
                html = render_miner_summary(
                    D_total=mr["total_damage"],
                    D_per=mr["damage_per_block"],
                    spectrum=spectrum,
                    damage_limit=damage_limit,
                    sn=sn,
                )
                st.markdown(html, unsafe_allow_html=True)

    # ── TAB 3: Weld Quality (ISO 5817) ────────────────────────────────────
    with tab3:
        st.subheader(t("weld_quality_tab"))
        from views.weld_quality_view import render as render_weld_quality
        render_weld_quality()

    # ── TAB 4: S-N Curve Explorer ─────────────────────────────────────────
    with tab4:
        st.subheader(t("sn_curve_explorer"))
        exp_fat = st.selectbox(
            t("fat_class"),
            [36, 40, 45, 50, 56, 63, 71, 80, 90, 100, 112, 125, 140, 160, 225],
            index=6,
        )
        exp_mat = st.selectbox(
            t("material"), FAMILY_KEYS, format_func=format_family,
            key="exp_mat",
        )
        exp_va = st.checkbox(
            t("variable_amplitude_loading"), key="exp_va",
        )

        sn_exp = SNCurve(exp_fat, exp_mat, exp_va)
        fig_exp = FatiguePlots.sn_curve_plotly(
            sn_exp,
            title=t("plot_sn_title", fat=sn_exp.fat_class,
                     mat=format_family(sn_exp.material_type)),
            labels=_sn_labels(),
        )
        st.plotly_chart(fig_exp, key="sn_explorer")
        st.markdown(render_sn_info_panel(sn_exp), unsafe_allow_html=True)

    # ── TAB 5: FAT Class Catalog ──────────────────────────────────────────
    with tab5:
        st.subheader(t("iiw_fat_class_catalog"))
        cat_mat = st.selectbox(
            t("material"), FAMILY_KEYS, format_func=format_family,
            key="cat_mat",
        )
        details = catalog.list_all(cat_mat)
        if details:
            import pandas as pd
            cat_df = pd.DataFrame([{
                "FAT": d.fat_class,
                t("col_detail_num"): d.detail_number,
                t("weld_type"): d.weld_type,
                t("load_type"): d.load_type,
                t("col_description"): d.description,
            } for d in details])
            st.dataframe(cat_df, hide_index=True)
        else:
            st.info(t("no_details_found"))

    # ── TAB 6: Haigh Diagram ──────────────────────────────────────────────
    with tab6:
        st.subheader(t("haigh_diagram"))

        Se = material.ultimate_strength * 0.5
        Su = material.ultimate_strength
        Sy = material.yield_strength

        op_points = []
        if "fatigue_result" in st.session_state:
            ms = st.session_state.get("fatigue_last_mean_stress", 0.0)
            sa = stress_range / 2.0
            op_points = [(ms, sa)]

        fig_haigh = FatiguePlots.haigh_diagram_plotly(
            Se, Su, Sy, op_points, labels=_haigh_labels(),
        )
        st.plotly_chart(fig_haigh, key="haigh_tab6")
        st.caption(t("haigh_explanation"))


# ══════════════════════════════════════════════════════════════════════════
# MULTIAXIAL MODE
# ══════════════════════════════════════════════════════════════════════════
elif selected_mode == "multiaxial":
    from views.multiaxial_view import render as render_multiaxial
    render_multiaxial()


# ══════════════════════════════════════════════════════════════════════════
# FRACTURE MECHANICS MODE
# ══════════════════════════════════════════════════════════════════════════
elif selected_mode == "fracture":
    from views.fracture_view import render as render_fracture
    render_fracture(material_type=family)


# ══════════════════════════════════════════════════════════════════════════
# VIBRATION FATIGUE MODE
# ══════════════════════════════════════════════════════════════════════════
elif selected_mode == "vibration":
    from views.vibration_view import render as render_vibration
    render_vibration(material_type=family)
