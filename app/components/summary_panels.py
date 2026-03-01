"""Rich engineering summary panel components.

Renders visually appealing HTML panels using custom CSS classes
defined in assets/style.css.  All panels are dark-mode compatible.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from i18n import t


# ---------------------------------------------------------------------------
# Severity classification
# ---------------------------------------------------------------------------

def classify_severity(value: float, thresholds: tuple) -> str:
    """Return 'safe', 'marginal', or 'critical'.

    *thresholds* = (marginal_boundary, critical_boundary).
    If ascending (e.g. damage ratio: 0.5, 1.0):
        value < marginal → safe,  marginal ≤ value < critical → marginal,  else critical
    If descending (e.g. safety factor: 2.0, 1.0):
        value > marginal → safe,  critical < value ≤ marginal → marginal,  else critical
    """
    lo, hi = thresholds
    if lo < hi:
        if value < lo:
            return "safe"
        return "marginal" if value < hi else "critical"
    else:
        if value > lo:
            return "safe"
        return "marginal" if value > hi else "critical"


# ---------------------------------------------------------------------------
# Primitive HTML builders
# ---------------------------------------------------------------------------

def _badge(severity: str) -> str:
    labels = {"safe": t("severity_safe"), "marginal": t("severity_marginal"),
              "critical": t("severity_critical")}
    return (f'<span class="eng-panel-badge badge-{severity}">'
            f'{labels.get(severity, severity)}</span>')


def _open(title: str, severity: str = "info") -> str:
    badge_html = _badge(severity) if severity != "info" else ""
    return (f'<div class="eng-panel severity-{severity}">'
            f'<div class="eng-panel-header">'
            f'<span class="eng-panel-title">{title}</span>'
            f'{badge_html}</div>')


def _close() -> str:
    return "</div>"


def _section(text: str) -> str:
    return f'<div class="eng-section-label">{text}</div>'


def _tile(label: str, value: str, unit: str = "",
          delta: str = "", delta_positive: bool = True) -> str:
    unit_h = f'<span class="metric-unit">{unit}</span>' if unit else ""
    delta_h = ""
    if delta:
        cls = "positive" if delta_positive else "negative"
        delta_h = f'<div class="metric-delta {cls}">{delta}</div>'
    return (f'<div class="eng-metric-tile">'
            f'<div class="metric-label">{label}</div>'
            f'<div class="metric-value">{value}{unit_h}</div>'
            f'{delta_h}</div>')


def _grid(tiles: list, cols: int = 3) -> str:
    return f'<div class="eng-metric-grid cols-{cols}">{"".join(tiles)}</div>'


def _progress(value: float, max_val: float = 1.0,
              label_left: str = "", label_right: str = "",
              large: bool = False) -> str:
    pct = min(max(value / max_val * 100, 0), 100) if max_val > 0 else 0
    ratio = value / max_val if max_val > 0 else 0
    fill = "fill-safe" if ratio < 0.6 else ("fill-warn" if ratio < 1.0 else "fill-danger")
    sz = " large" if large else ""
    lbl = ""
    if label_left or label_right:
        lbl = (f'<div class="eng-progress-label">'
               f'<span>{label_left}</span><span>{label_right}</span></div>')
    return (f'<div class="eng-progress-wrap">{lbl}'
            f'<div class="eng-progress-bar{sz}">'
            f'<div class="eng-progress-fill {fill}" style="width:{pct:.1f}%"></div>'
            f'</div></div>')


def _caption(text: str) -> str:
    return f'<div class="eng-caption">{text}</div>'


def _damage_row(label: str, pct: float, value_text: str, critical: bool = False) -> str:
    cls = " is-critical" if critical else ""
    return (f'<div class="eng-damage-row{cls}">'
            f'<span class="block-label">{label}</span>'
            f'<div class="block-bar">'
            f'<div class="block-bar-fill" style="width:{min(pct, 100):.1f}%"></div></div>'
            f'<span class="block-value">{value_text}</span></div>')


def _result_strip(status: str, right_text: str = "") -> str:
    cls = "pass" if status == "PASS" else "fail"
    return (f'<div class="result-strip {cls}">'
            f'<span>{status}</span><span>{right_text}</span></div>')


# ---------------------------------------------------------------------------
# High-level panel renderers
# ---------------------------------------------------------------------------

def render_fatigue_summary(
    stress_range, mean_stress, num_cycles,
    sigma_max, sigma_min, sigma_a, R, load_desc,
    allowable_stress, stress_margin,
    N_allow, D, sf,
    sn, variable_amplitude,
):
    """Complete fatigue single-block summary panel."""
    severity = classify_severity(D, (0.5, 1.0))

    # --- remaining life ---
    if N_allow != float("inf"):
        remaining = N_allow - num_cycles
        if remaining > 0:
            remaining_str = f"{int(remaining):,}"
            remaining_delta = ""
            remaining_pos = True
        else:
            remaining_str = f"−{int(abs(remaining)):,}"
            remaining_delta = t("severity_critical")
            remaining_pos = False
    else:
        remaining_str = "∞"
        remaining_delta = ""
        remaining_pos = True

    # --- allowable cycles display ---
    if N_allow != float("inf") and N_allow < 1e9:
        nf_str = f"{int(N_allow):,}"
    elif N_allow != float("inf"):
        nf_str = f"{N_allow:.2e}"
    else:
        nf_str = "∞"

    # --- repetitions ---
    if D >= 1.0:
        reps_str = f"< 1  (+{(D - 1.0) * 100:.1f}%)"
    elif D > 0:
        reps_str = f"{int(1.0 / D)}x"
    else:
        reps_str = "∞"

    # --- endurance ratio ---
    endo_ratio = stress_range / sn.delta_sigma_knee if sn.delta_sigma_knee > 0 else 0

    # --- operating region ---
    if stress_range >= sn.delta_sigma_knee:
        region = t("above_knee", m=sn.m1)
    elif variable_amplitude and stress_range > sn.delta_sigma_cutoff:
        region = t("below_knee_va", m=sn.m2)
    else:
        region = t("below_knee_ca")

    # --- safety factor display ---
    sf_str = f"{sf:.2f}" if sf != float("inf") else "∞"

    # --- stress margin delta ---
    margin_delta = ""
    margin_pos = True
    if stress_margin != float("inf"):
        if stress_margin >= 0:
            margin_delta = f"+{stress_margin:.1f} MPa reserve"
        else:
            margin_delta = f"{stress_margin:.1f} MPa deficit"
            margin_pos = False

    # --- allowable stress display ---
    allow_str = f"{allowable_stress:.1f}" if allowable_stress > 0 else "∞"

    # --- life consumed % ---
    life_pct = min(D * 100, 100)

    html = _open(t("engineering_summary"), severity)

    # STRESS STATE
    html += _section(t("section_stress_state"))
    html += _grid([
        _tile("σ_max", f"{sigma_max:.1f}", "MPa"),
        _tile("σ_min", f"{sigma_min:.1f}", "MPa"),
        _tile("σ_a", f"{sigma_a:.1f}", "MPa"),
        _tile("R", f"{R:.3f}"),
    ], 4)
    html += _caption(f"{t('loading_type_label')}: {load_desc}")

    # FATIGUE MARGINS
    html += _section(t("section_fatigue_margins"))
    html += _grid([
        _tile(t("max_allowable_stress", n=f"{num_cycles:.0e}"), allow_str, "MPa"),
        _tile(t("stress_margin"), f"{stress_margin:+.1f}" if stress_margin != float("inf") else "∞", "MPa",
              delta=margin_delta, delta_positive=margin_pos),
        _tile(t("endurance_ratio"), f"{endo_ratio:.2f}", "",
              delta=region, delta_positive=(endo_ratio < 1.0)),
    ], 3)

    # LIFE ASSESSMENT
    html += _section(t("section_life_assessment"))
    html += _progress(D, 1.0,
                      label_left=t("life_used_pct"),
                      label_right=f"{D * 100:.1f}%",
                      large=True)
    html += _grid([
        _tile(t("allowable_cycles"), nf_str, t("cycles_unit")),
        _tile(t("remaining_life"), remaining_str, t("cycles_unit"),
              delta=remaining_delta, delta_positive=remaining_pos),
        _tile(t("safety_factor"), sf_str, "",
              delta=f"{(sf - 1) * 100:+.0f}% margin" if sf != float("inf") and sf > 0 else "",
              delta_positive=(sf > 1.0)),
    ], 3)
    html += _grid([
        _tile(t("repetitions_to_failure"), reps_str),
    ], 3)
    html += _caption(t("knee_point_stress_val", v=sn.delta_sigma_knee, n=sn.N_knee))

    html += _close()
    return html


def render_miner_summary(
    D_total, D_per, spectrum, damage_limit, sn,
):
    """Complete Miner damage summary panel."""
    severity = classify_severity(D_total, (damage_limit * 0.5, damage_limit))

    remaining_budget = damage_limit - D_total
    if D_total > 0:
        reps = int(damage_limit / D_total)
        reps_str = f"{reps}x"
    else:
        reps_str = "∞"

    # equivalent stress range
    total_n = sum(nc for _, nc in spectrum)
    sum_ni_si_m = sum(nc * (sr ** sn.m1) for sr, nc in spectrum)
    if total_n > 0 and sum_ni_si_m > 0:
        delta_eq = (sum_ni_si_m / total_n) ** (1.0 / sn.m1)
        eq_str = f"{delta_eq:.1f}"
    else:
        eq_str = "—"

    html = _open(t("miner_summary"), severity)

    # DAMAGE BUDGET
    html += _section(t("section_damage_budget"))
    html += _progress(D_total, damage_limit,
                      label_left=f"{t('total_damage')}",
                      label_right=f"{D_total:.4f} / {damage_limit:.1f}",
                      large=True)
    html += _grid([
        _tile(t("remaining_damage_budget"), f"{remaining_budget:.4f}"),
        _tile(t("spectrum_repetitions"), reps_str),
        _tile(t("equivalent_stress_range"), eq_str, "MPa"),
    ], 3)

    # BLOCK ANALYSIS
    html += _section(t("section_block_analysis"))
    max_d = max(D_per) if D_per else 1
    crit_idx = D_per.index(max_d) if D_per else 0
    for i, (d_i, (sr_i, nc_i)) in enumerate(zip(D_per, spectrum)):
        pct = (d_i / D_total * 100) if D_total > 0 else 0
        val = f"Δσ={sr_i:.0f} MPa → D={d_i:.4f} ({pct:.0f}%)"
        html += _damage_row(
            f"Block {i + 1}", pct, val,
            critical=(i == crit_idx),
        )
    if D_total > 0:
        crit_pct = D_per[crit_idx] / D_total * 100
        html += _caption(t("most_damaging_block", i=crit_idx + 1, pct=crit_pct))

    html += _close()
    return html


def render_shock_dynamic_summary(
    static_yield, dynamic_yield, dif, strain_rate,
):
    """Dynamic yield summary panel."""
    severity = classify_severity(dif, (1.2, 1.5))
    increase = dynamic_yield - static_yield
    pct = (dif - 1.0) * 100

    # strain rate regime
    if strain_rate < 1:
        regime = t("regime_low")
    elif strain_rate < 100:
        regime = t("regime_medium")
    elif strain_rate < 1000:
        regime = t("regime_high")
    else:
        regime = t("regime_very_high")

    # DIF classification
    if dif < 1.05:
        dif_cls = t("dif_minimal")
    elif dif < 1.2:
        dif_cls = t("dif_low")
    elif dif < 1.5:
        dif_cls = t("dif_moderate")
    else:
        dif_cls = t("dif_high")

    # DIF bar (scale 1.0 to 2.0 → 0 to 1)
    dif_norm = min(max((dif - 1.0) / 1.0, 0), 1.0)

    html = _open(t("shock_summary"), severity)
    html += _section(t("section_stress_state"))
    html += _grid([
        _tile(t("static_yield"), f"{static_yield:.0f}", "MPa"),
        _tile(t("dynamic_yield"), f"{dynamic_yield:.1f}", "MPa",
              delta=f"+{increase:.1f} MPa (+{pct:.1f}%)", delta_positive=True),
        _tile("DIF", f"{dif:.3f}", "",
              delta=dif_cls, delta_positive=(dif < 1.5)),
        _tile(t("strain_rate_regime"), "", "",
              delta=regime, delta_positive=True),
    ], 4)
    html += _progress(dif_norm, 1.0,
                      label_left="DIF",
                      label_right=f"{dif:.3f}",
                      large=False)
    html += _close()
    return html


def render_weld_check_summary(
    equiv_stress, allowable, utilization, status,
    weld_throat=None, weld_length=None,
    normal_force=None, shear_force=None,
):
    """Weld failure check summary panel."""
    severity = classify_severity(utilization, (0.6, 1.0))
    rf = 1.0 / utilization if utilization > 0 else float("inf")
    margin = allowable - equiv_stress
    margin_pct = (1 - utilization) * 100

    # min throat for PASS (force-based only)
    min_throat_str = ""
    if weld_throat is not None and weld_length is not None and normal_force is not None:
        combined_force = (normal_force**2 + shear_force**2) ** 0.5 if shear_force else normal_force
        if allowable > 0 and weld_length > 0:
            min_a = combined_force / (allowable * weld_length)
            min_throat_str = f"{min_a:.2f}"

    html = _open(t("weld_summary"), severity)

    # WELD CAPACITY
    html += _section(t("section_weld_capacity"))
    html += _progress(utilization, 1.0,
                      label_left=t("utilization"),
                      label_right=f"{utilization:.3f} / 1.000",
                      large=True)
    tiles = [
        _tile(t("reserve_factor"),
              f"{rf:.2f}" if rf != float("inf") else "∞", "",
              delta=f"{(rf - 1) * 100:+.0f}% reserve" if rf != float("inf") and rf > 0 else "",
              delta_positive=(rf > 1.0)),
        _tile(t("stress_margin_weld"), f"{margin:+.1f}", "MPa",
              delta=f"{margin_pct:+.1f}%", delta_positive=(margin > 0)),
    ]
    if min_throat_str:
        tiles.append(_tile(t("min_weld_throat"), min_throat_str, "mm"))
    html += _grid(tiles, 3)

    html += _close()
    return html


def render_energy_summary(
    total_energy, sea, mean_force, peak_force, cfe,
    energy_per_mm, stroke, mass,
):
    """Energy absorption summary panel."""
    severity = classify_severity(cfe, (0.3, 0.6))
    # for CFE higher is better, so invert severity
    if cfe > 0.6:
        severity = "safe"
    elif cfe > 0.3:
        severity = "marginal"
    else:
        severity = "critical"

    # efficiency rating
    if cfe > 0.7:
        rating = t("efficiency_excellent")
    elif cfe > 0.5:
        rating = t("efficiency_good")
    elif cfe > 0.3:
        rating = t("efficiency_fair")
    else:
        rating = t("efficiency_poor")

    html = _open(t("energy_summary"), severity)

    # ENERGY METRICS
    html += _section(t("section_energy_metrics"))
    html += _grid([
        _tile(t("total_energy"), f"{total_energy:.0f}", "J"),
        _tile("SEA", f"{sea:.0f}", "J/kg"),
        _tile(t("peak_force"), f"{peak_force:.0f}", "N"),
    ], 3)

    # CRUSH PERFORMANCE
    html += _section(t("section_crush_performance"))
    html += _progress(cfe, 1.0,
                      label_left="CFE",
                      label_right=f"{cfe:.3f}",
                      large=True)
    html += _grid([
        _tile(t("mean_crush_force"), f"{mean_force:.0f}", "N"),
        _tile(t("energy_per_mm"), f"{energy_per_mm:.1f}", "J/mm"),
        _tile(t("stroke_length"), f"{stroke:.1f}", "mm"),
    ], 3)
    html += _grid([
        _tile(t("efficiency_rating"), "", "", delta=rating, delta_positive=(cfe > 0.5)),
    ], 3)

    html += _close()
    return html


def render_sn_info_panel(sn):
    """S-N curve parameter info panel."""
    html = _open(t("sn_curve_parameters"), "info")
    html += _grid([
        _tile(t("slope_m1"), f"{sn.m1:.1f}"),
        _tile(t("slope_m2"), f"{sn.m2:.1f}"),
        _tile(t("knee_point_stress"), f"{sn.delta_sigma_knee:.1f}", "MPa"),
        _tile(t("cutoff_stress_va"), f"{sn.delta_sigma_cutoff:.2f}", "MPa"),
    ], 4)
    html += _close()
    return html
