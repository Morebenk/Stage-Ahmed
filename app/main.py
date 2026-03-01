"""WeldFatigue Streamlit Application - Entry point."""

import streamlit as st
from i18n import t
from components.sidebar import render_sidebar

st.set_page_config(
    page_title="WeldFatigue - OPmobility C-Power",
    page_icon="\u2699\ufe0f",
    layout="wide",
    initial_sidebar_state="expanded",
)


_MODULES = [
    ("pages/01_material_database.py", "mat_icon", "mod_material_db_title", "mod_material_db"),
    ("pages/02_fatigue_analysis.py", "fat_icon", "mod_fatigue_title", "mod_fatigue"),
    ("pages/03_shock_analysis.py", "shock_icon", "mod_shock_title", "mod_shock"),
    ("pages/04_fea_postprocessing.py", "fea_icon", "mod_fea_title", "mod_fea"),
    ("pages/05_report_generation.py", "report_icon", "mod_report_title", "mod_report"),
]

_ICONS = {
    "mat_icon": "\U0001f9f1",      # brick
    "fat_icon": "\U0001f4c9",      # chart decreasing
    "shock_icon": "\U0001f4a5",    # collision
    "fea_icon": "\U0001f9ee",      # abacus
    "report_icon": "\U0001f4cb",   # clipboard
}


def main():
    render_sidebar()

    # ── Hero banner ───────────────────────────────────────────────────────
    st.markdown(
        f'<div class="hero-banner">'
        f"<h1>WeldFatigue</h1>"
        f'<p class="tagline">{t("main_subtitle")}</p>'
        f'<span class="badge">OPmobility C-Power</span>'
        f"</div>",
        unsafe_allow_html=True,
    )
    st.markdown(t("main_description"))

    # ── Module cards (3 columns) ──────────────────────────────────────────
    st.markdown(f"#### {t('available_modules')}")
    rows = [_MODULES[i : i + 3] for i in range(0, len(_MODULES), 3)]
    for row in rows:
        cols = st.columns(3)
        for idx, (page, icon_key, title_key, desc_key) in enumerate(row):
            with cols[idx]:
                with st.container(border=True):
                    st.markdown(f"### {_ICONS[icon_key]}  {t(title_key)}")
                    st.caption(t(desc_key))
                    st.page_link(page, label=t("open_module"), icon="\u27a1\ufe0f")

    # ── Session status (with summary values when available) ──────────────
    st.markdown("---")
    st.markdown(f"#### {t('session_status')}")
    s1, s2, s3 = st.columns(3)

    def _status_chip(key):
        """Build a status chip with summary info if results exist."""
        if key not in st.session_state:
            return f'<span class="status-chip status-pending">{t("pending")}</span>'

        data = st.session_state[key]
        detail = ""
        if key == "fatigue_result" and isinstance(data, dict):
            sbr = data.get("single_block_result", {})
            s = sbr.get("status", "")
            sf = sbr.get("safety_factor", 0)
            sf_txt = f"SF={sf:.1f}" if sf != float("inf") else "SF=∞"
            detail = f" — {s} {sf_txt}"
        elif key == "shock_result" and isinstance(data, dict):
            dif_v = data.get("dif", 0)
            detail = f" — DIF={dif_v:.2f}"
        elif key == "fea_hotspot_stress":
            detail = f" — {data:.1f} MPa"

        return (f'<span class="status-chip status-ready">'
                f'{t("ready")}{detail}</span>')

    with s1:
        st.markdown(
            f"**{t('mod_fatigue_title')}** &nbsp; {_status_chip('fatigue_result')}",
            unsafe_allow_html=True,
        )
    with s2:
        st.markdown(
            f"**{t('mod_shock_title')}** &nbsp; {_status_chip('shock_result')}",
            unsafe_allow_html=True,
        )
    with s3:
        st.markdown(
            f"**{t('mod_fea_title')}** &nbsp; {_status_chip('fea_hotspot_stress')}",
            unsafe_allow_html=True,
        )

    # ── Standards & applications (collapsible) ────────────────────────────
    with st.expander(t("applicable_standards")):
        st.markdown(
            "- **IIW Recommendations XIII-1823-07** (Fatigue Design of Welded Joints)\n"
            "- **EN 1993-1-8** (Eurocode 3 - Weld Design)\n"
            "- **ASTM E1049-85** (Rainflow Cycle Counting)"
        )

    with st.expander(t("target_applications")):
        st.markdown(
            f"- {t('ev_battery')}\n"
            f"- {t('h2_tank')}\n"
            f"- {t('structural_reinforcements')}\n"
            f"- {t('welded_chassis')}"
        )


if __name__ == "__main__":
    main()
