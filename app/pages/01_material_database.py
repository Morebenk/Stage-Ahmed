"""Material Database Browser - Streamlit page."""

import streamlit as st
import numpy as np
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from i18n import (
    t, format_family, rename_db_columns,
    FAMILY_KEYS,
)
from components.sidebar import render_sidebar

from weldfatigue.materials.database import MaterialDatabase
from weldfatigue.materials.strain_rate import cowper_symonds_yield
from weldfatigue.reporting.plots import ShockPlots

st.set_page_config(page_title="Material Database", layout="wide")

render_sidebar()

st.title(t("material_database"))

db = MaterialDatabase()

# Sidebar filters
st.sidebar.header(t("filters"))

family_options = [None] + FAMILY_KEYS
family = st.sidebar.selectbox(
    t("material_family"),
    family_options,
    format_func=lambda v: t("all") if v is None else format_family(v),
)
min_yield = st.sidebar.number_input(t("min_yield_strength"), value=0, min_value=0)
max_yield = st.sidebar.number_input(t("max_yield_strength"), value=2000, min_value=0)

# Filter and display
df = db.to_dataframe(family)
df = rename_db_columns(df)

# Apply yield filter (use translated column name)
yield_col = t("col_yield")
df = df[(df[yield_col] >= min_yield) & (df[yield_col] <= max_yield)]

st.subheader(t("available_grades"))
st.dataframe(df, hide_index=True)

# Material detail view
st.markdown("---")
st.subheader(t("material_detail_view"))

all_grades = db.list_grades(family)
if all_grades:
    selected = st.selectbox(t("select_grade_details"), all_grades)
    mat = db.get(selected)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**{t('mechanical_properties')}**")
        st.metric(t("yield_strength"), f"{mat.yield_strength} MPa")
        st.metric(t("ultimate_strength"), f"{mat.ultimate_strength} MPa")
        st.metric(t("youngs_modulus"), f"{mat.youngs_modulus} MPa")
        st.metric(t("elongation"), f"{mat.elongation_at_break}%")

    with col2:
        st.markdown(f"**{t('strain_rate_params_cs')}**")
        st.metric("D", f"{mat.cs_D}")
        st.metric("q", f"{mat.cs_q}")

        # Dynamic yield plot
        dyn_labels = {
            "title": t("plot_dynamic_yield_title", name=mat.name),
            "xaxis": t("plot_strain_rate_axis"),
            "yaxis": t("plot_yield_stress_axis"),
            "static_yield": t("plot_static_yield"),
        }
        fig = ShockPlots.dynamic_yield_vs_strain_rate_plotly(
            mat.name, mat.yield_strength, mat.cs_D, mat.cs_q,
            labels=dyn_labels,
        )
        st.plotly_chart(fig, key="dynamic_yield_plot")

    # HAZ properties
    weld_props = db.get_weld_properties(selected)
    if weld_props:
        st.markdown("---")
        st.subheader(t("weld_haz_properties"))
        wcol1, wcol2 = st.columns(2)
        with wcol1:
            st.metric(t("weld_process"), weld_props.weld_process)
            st.metric(t("haz_width"), f"{weld_props.haz_width} mm")
        with wcol2:
            st.metric(t("haz_yield_factor"), f"{weld_props.haz_yield_factor}")
            st.metric(t("haz_uts_factor"), f"{weld_props.haz_uts_factor}")
