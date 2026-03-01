"""Result display widgets for Streamlit."""

import streamlit as st
import pandas as pd
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from i18n import t


def render_fatigue_result(result: dict):
    """Display a fatigue result as a styled metric card."""
    col1, col2, col3, col4 = st.columns(4)

    status = result.get("status", "N/A")
    with col1:
        st.metric(t("status"), status)
    with col2:
        sf = result.get("safety_factor", 0)
        sf_str = f"{sf:.2f}" if sf != float("inf") else "INF"
        st.metric(t("safety_factor"), sf_str)
    with col3:
        st.metric(t("allowable_n"), f"{result.get('allowable_cycles', 0):.2e}")
    with col4:
        st.metric(t("damage_ratio"), f"{result.get('damage_ratio', 0):.4f}")


def render_results_dataframe(results: list[dict]):
    """Display multiple results as a DataFrame."""
    df = pd.DataFrame(results)
    st.dataframe(df)
