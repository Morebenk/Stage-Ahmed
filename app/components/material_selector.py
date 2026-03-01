"""Material grade selection widget for Streamlit."""

import streamlit as st
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from i18n import t, format_family, FAMILY_KEYS

from weldfatigue.materials.database import MaterialDatabase


def material_selector(
    db: MaterialDatabase, key: str = "material"
) -> str:
    """Render a material grade selector in the sidebar."""
    family = st.sidebar.selectbox(
        t("material_family"),
        FAMILY_KEYS,
        format_func=format_family,
        key=f"{key}_family",
    )
    grades = db.list_grades(family)
    selected = st.sidebar.selectbox(
        t("material_grade"),
        grades,
        key=f"{key}_grade",
    )
    return selected
