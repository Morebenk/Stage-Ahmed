"""ISO 5817 weld quality assessment view (rendered as a tab)."""

import streamlit as st

from i18n import t
from weldfatigue.fatigue.weld_quality import WeldQualityAssessment


def render() -> None:
    """Render weld quality assessment content inside a tab."""

    wqa = WeldQualityAssessment

    st.markdown(t("weld_quality_desc"))

    # ── Configuration (inline, not sidebar - this is a tab) ───────────────
    cfg1, cfg2, cfg3 = st.columns(3)
    with cfg1:
        quality_level = st.selectbox(
            t("quality_level"), ["B", "C", "D"], index=0, key="wq_ql",
            help=t("quality_level_help"),
        )
    with cfg2:
        weld_type = st.selectbox(
            t("weld_type_wq"),
            ["butt", "fillet", "cruciform", "t_joint", "lap"],
            index=0, key="wq_wtype",
            format_func=lambda x: x.replace("_", " ").title(),
        )
    with cfg3:
        restraint = st.selectbox(
            t("end_restraint"), ["fixed", "pinned"], index=0, key="wq_restr",
            format_func=lambda x: x.title(),
        )

    # ── Geometry & misalignment ───────────────────────────────────────────
    st.markdown("---")
    st.subheader(t("geometry_misalignment"))

    col1, col2 = st.columns(2)
    with col1:
        thickness = st.number_input(
            t("plate_thickness") + " (mm)", value=10.0,
            min_value=1.0, step=0.5, key="wq_thick",
        )
        length = st.number_input(
            t("joint_length") + " (mm)", value=100.0,
            min_value=1.0, step=10.0, key="wq_len",
        )
    with col2:
        axial_mis = st.number_input(
            t("axial_misalignment") + " (mm)", value=0.5,
            min_value=0.0, step=0.1, key="wq_eax",
        )
        angular_mis = st.number_input(
            t("angular_misalignment") + " (mm)", value=0.3,
            min_value=0.0, step=0.1, key="wq_eang",
        )

    # ── Imperfection checks ───────────────────────────────────────────────
    st.markdown("---")
    st.subheader(t("imperfection_checks"))
    st.markdown(t("imperfection_intro").format(ql=quality_level))

    imp1, imp2 = st.columns(2)
    with imp1:
        undercut = st.number_input(
            t("undercut_depth") + " (mm)", value=0.0,
            min_value=0.0, step=0.1, key="wq_undercut",
        )
        porosity = st.number_input(
            t("porosity_area") + " (mm\u00b2)", value=0.0,
            min_value=0.0, step=0.1, key="wq_porosity",
        )
        excess_wm = st.number_input(
            t("excess_weld_metal") + " (mm)", value=0.0,
            min_value=0.0, step=0.1, key="wq_excess",
        )
    with imp2:
        incomplete_pen = st.number_input(
            t("incomplete_penetration") + " (mm)", value=0.0,
            min_value=0.0, step=0.1, key="wq_pen",
        )
        axial_mis_imp = st.number_input(
            t("axial_mis_check") + " (mm)", value=axial_mis,
            min_value=0.0, step=0.1, key="wq_mis_check",
        )

    # ── Run assessment ────────────────────────────────────────────────────
    if st.button(t("run_assessment"), type="primary", key="wq_run"):
        qa_result = wqa.assess_quality(
            weld_type=weld_type,
            quality_level=quality_level,
            axial_misalignment=axial_mis,
            angular_misalignment=angular_mis,
            thickness=thickness,
            length=length,
            restraint=restraint,
        )

        imperfection_checks = {}
        imperfections = {
            "undercut": undercut,
            "porosity": porosity,
            "excess_weld_metal": excess_wm,
            "incomplete_penetration": incomplete_pen,
            "misalignment_axial": axial_mis_imp,
        }
        for imp_type, measured in imperfections.items():
            imperfection_checks[imp_type] = wqa.check_imperfection(
                imp_type, measured, quality_level, thickness,
            )

        st.session_state["wq_result"] = qa_result
        st.session_state["wq_imperfections"] = imperfection_checks

    # ── Display results ───────────────────────────────────────────────────
    if "wq_result" not in st.session_state:
        return

    qa_result = st.session_state["wq_result"]
    imp_checks = st.session_state.get("wq_imperfections", {})

    st.markdown("---")
    st.subheader(t("results"))

    # km factors
    st.markdown(f"#### {t('km_factors')}")
    kcol1, kcol2, kcol3 = st.columns(3)
    kcol1.metric("km (Axial)", f'{qa_result["km_axial"]:.3f}')
    kcol2.metric("km (Angular)", f'{qa_result["km_angular"]:.3f}')
    kcol3.metric("km (Combined)", f'{qa_result["km_combined"]:.3f}')

    # FAT class
    base_fat = qa_result["fat_class"]
    adjusted_fat = base_fat / qa_result["km_combined"]

    fcol1, fcol2 = st.columns(2)
    fcol1.metric(
        f"Base FAT (Level {quality_level})", f"FAT {base_fat}",
    )
    fcol2.metric(
        t("effective_fat_km"), f"FAT {adjusted_fat:.0f}",
        delta=f"{adjusted_fat - base_fat:.0f}" if adjusted_fat != base_fat else None,
        delta_color="inverse",
    )

    if qa_result["km_combined"] > 1.0:
        st.warning(
            f"Misalignment reduces FAT from **{base_fat}** to "
            f"**{adjusted_fat:.0f}** (km = {qa_result['km_combined']:.3f})."
        )

    # Imperfection results
    if imp_checks:
        st.markdown("---")
        st.markdown(f"#### {t('imperfection_results')}")

        import pandas as pd

        all_pass = True
        rows = []
        for imp_type, check in imp_checks.items():
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
        st.dataframe(pd.DataFrame(rows), hide_index=True)

        _cls = "pass" if all_pass else "fail"
        _overall = t("all_checks_pass") if all_pass else t("some_checks_fail")
        st.markdown(
            f'<div class="result-strip {_cls}">'
            f"<span>{_overall}</span>"
            f'<span>Quality Level {quality_level}</span></div>',
            unsafe_allow_html=True,
        )

    # Quality level comparison chart
    st.markdown(f"#### {t('quality_comparison')}")
    import plotly.graph_objects as go

    levels = ["B", "C", "D"]
    fat_values = [wqa.quality_level_fat(lvl, weld_type) for lvl in levels]
    colors = [
        "green" if lvl == quality_level else "lightgray" for lvl in levels
    ]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=levels, y=fat_values,
        marker_color=colors,
        text=[f"FAT {v}" for v in fat_values],
        textposition="auto",
    ))
    fig.add_hline(
        y=adjusted_fat, line_dash="dash", line_color="red",
        annotation_text=f"Effective FAT {adjusted_fat:.0f} (km-adjusted)",
    )
    fig.update_layout(
        title=t("fat_by_quality_level"),
        xaxis_title="ISO 5817 Quality Level",
        yaxis_title="FAT Class",
        height=400,
    )
    st.plotly_chart(fig, use_container_width=True, key="wq_chart")
