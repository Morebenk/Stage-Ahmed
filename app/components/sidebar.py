"""Shared sidebar component for the Streamlit app."""

import streamlit as st
from pathlib import Path
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from i18n import t, language_selector


def _load_css():
    """Inject custom CSS into the page."""
    css_path = Path(__file__).parent.parent / "assets" / "style.css"
    if css_path.exists():
        st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)


def render_sidebar():
    """Render the common sidebar elements: branding + language + CSS."""
    _load_css()
    st.sidebar.markdown(
        '<div class="sidebar-brand">'
        "<h2>WeldFatigue</h2>"
        "<p>OPmobility C-Power</p>"
        "</div>",
        unsafe_allow_html=True,
    )
    language_selector()
    st.sidebar.markdown("---")
