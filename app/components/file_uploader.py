"""FEA file upload handler for Streamlit."""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from i18n import t, format_file_format, FILE_FORMAT_KEYS

from weldfatigue.fea.generic_reader import GenericCSVReader
from weldfatigue.fea.result_model import FEAResult


def fea_file_uploader(key: str = "fea_upload") -> FEAResult | None:
    """Render a file uploader for FEA results."""
    file_format = st.sidebar.selectbox(
        t("file_format"),
        FILE_FORMAT_KEYS,
        format_func=format_file_format,
        key=f"{key}_format",
    )

    uploaded = st.file_uploader(
        t("upload_fea_results"),
        type=["csv", "k", "key", "inp", "bdf"],
        key=key,
    )

    if uploaded is None:
        return None

    if file_format == "CSV (generic)":
        df = pd.read_csv(uploaded)
        st.info(t("loaded_csv_rows", n=len(df)))
        reader = GenericCSVReader()
        return reader.read_dataframe(df)

    st.warning(t("parser_optional_ext", fmt=format_file_format(file_format)))
    return None
