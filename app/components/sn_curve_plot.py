"""Interactive S-N curve display for Streamlit."""

import streamlit as st

from weldfatigue.fatigue.sn_curve import SNCurve
from weldfatigue.reporting.plots import FatiguePlots


def render_sn_curve(
    fat_class: int,
    material_type: str = "steel",
    operating_point: tuple = None,
    variable_amplitude: bool = False,
    title: str = None,
    labels: dict = None,
    key: str = "sn_curve",
):
    """Render an interactive S-N curve in Streamlit."""
    sn = SNCurve(fat_class, material_type, variable_amplitude)
    fig = FatiguePlots.sn_curve_plotly(sn, operating_point, title=title, labels=labels)
    st.plotly_chart(fig, key=key)
