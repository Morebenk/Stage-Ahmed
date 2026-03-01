"""FEA Post-Processing - Streamlit page."""

import streamlit as st
import numpy as np
import pandas as pd
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from i18n import t, format_file_format, FILE_FORMAT_KEYS
from components.sidebar import render_sidebar

from weldfatigue.fea.generic_reader import GenericCSVReader
from weldfatigue.fea.stress_tensor import StressTensorOps

st.set_page_config(page_title="FEA Post-Processing", layout="wide")

render_sidebar()

st.title(t("fea_postprocessing"))

# Stress operation keys (internal) → i18n label keys
_STRESS_OPS = {
    "von_mises": "Von Mises",
    "principal": "principal_stresses",
    "max_shear": "max_shear",
    "hydrostatic": "hydrostatic",
}
_STRESS_OP_KEYS = list(_STRESS_OPS.keys())


def _stress_op_label(key):
    """Return translated label for a stress operation key."""
    if key == "von_mises":
        return "Von Mises"
    return t(_STRESS_OPS[key])


# Sidebar
st.sidebar.header(t("configuration"))
file_format = st.sidebar.selectbox(
    t("file_format"),
    FILE_FORMAT_KEYS,
    format_func=format_file_format,
)

stress_component = st.sidebar.multiselect(
    t("stress_operations"),
    _STRESS_OP_KEYS,
    default=["von_mises"],
    format_func=_stress_op_label,
)

plate_thickness = st.sidebar.number_input(t("plate_thickness"), value=10.0, min_value=0.1)

# Main area
uploaded = st.file_uploader(t("upload_fea_file"), type=["csv", "k", "key", "inp", "bdf"])

if uploaded is not None:
    if file_format == "CSV (generic)":
        df = pd.read_csv(uploaded)
        st.info(t("loaded_rows", n=len(df), m=len(df.columns)))
        st.dataframe(df.head(10))

        reader = GenericCSVReader()
        try:
            fea_result = reader.read_dataframe(df)
            st.success(t("parsed_nodes", n=fea_result.n_nodes))

            if "stress_tensor" in fea_result.nodal_fields:
                tensor = fea_result.get_stress_tensor()
                results_df = pd.DataFrame({
                    t("col_node_id"): fea_result.node_ids,
                })

                if "von_mises" in stress_component:
                    vm = StressTensorOps.von_mises(tensor)
                    results_df["Von Mises [MPa]"] = vm

                if "principal" in stress_component:
                    s1, s2, s3 = StressTensorOps.principal_stresses(tensor)
                    results_df["S1 [MPa]"] = s1
                    results_df["S2 [MPa]"] = s2
                    results_df["S3 [MPa]"] = s3

                if "max_shear" in stress_component:
                    ms = StressTensorOps.max_shear(tensor)
                    results_df[f"{t('max_shear')} [MPa]"] = ms

                if "hydrostatic" in stress_component:
                    hyd = StressTensorOps.hydrostatic(tensor)
                    results_df[f"{t('hydrostatic')} [MPa]"] = hyd

                st.subheader(t("computed_stress_results"))
                st.dataframe(
                    results_df.sort_values(results_df.columns[1], ascending=False).head(20),
                    hide_index=True,
                )

                # Histogram
                if "Von Mises [MPa]" in results_df.columns:
                    import plotly.express as px
                    fig = px.histogram(
                        results_df, x="Von Mises [MPa]", nbins=50,
                        title=t("vm_stress_distribution"),
                    )
                    st.plotly_chart(fig, key="vm_histogram")

                # Hot-spot extraction
                st.markdown("---")
                st.subheader(t("hotspot_extraction"))
                st.markdown(t("hotspot_explanation"))

                hcol1, hcol2 = st.columns(2)
                with hcol1:
                    toe_node = st.number_input(t("weld_toe_node"), value=int(fea_result.node_ids[0]), min_value=1)
                    dir_x = st.number_input(f"{t('path_direction')} X", value=1.0)
                    dir_y = st.number_input(f"{t('path_direction')} Y", value=0.0)
                    dir_z = st.number_input(f"{t('path_direction')} Z", value=0.0)

                with hcol2:
                    hs_type = st.selectbox(t("hotspot_type"), ["a", "b"])
                    if st.button(t("extract_hotspot")):
                        from weldfatigue.fea.hotspot_extractor import HotSpotExtractor
                        try:
                            extractor = HotSpotExtractor(fea_result, plate_thickness)
                            hs_stress = extractor.compute_hotspot_stress(
                                toe_node, np.array([dir_x, dir_y, dir_z]), hs_type
                            )
                            st.metric(t("hotspot_stress_label"), f"{hs_stress:.2f} MPa")
                            st.session_state["fea_hotspot_stress"] = hs_stress
                            st.session_state["fea_hotspot_type"] = hs_type
                            st.success(t("hotspot_saved_to_session"))
                            st.info(t("navigate_to_fatigue_hint"))
                        except (ValueError, KeyError) as e:
                            st.error(str(e))
            else:
                st.warning(t("no_stress_tensor"))

        except Exception as e:
            st.error(t("error_parsing", e=e))

    else:
        st.warning(t("parser_optional", fmt=file_format))

else:
    st.info(t("upload_to_start"))

    # Show expected CSV format
    st.markdown(f"### {t('expected_csv_format')}")
    sample_df = pd.DataFrame({
        "node_id": [1, 2, 3],
        "x": [0.0, 10.0, 20.0],
        "y": [0.0, 0.0, 0.0],
        "z": [0.0, 0.0, 0.0],
        "sigma_xx": [100.0, 150.0, 120.0],
        "sigma_yy": [50.0, 80.0, 60.0],
        "sigma_zz": [10.0, 20.0, 15.0],
        "tau_xy": [30.0, 40.0, 35.0],
        "tau_yz": [5.0, 10.0, 8.0],
        "tau_xz": [15.0, 25.0, 20.0],
    })
    st.dataframe(sample_df, hide_index=True)
