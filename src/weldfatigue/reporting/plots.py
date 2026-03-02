"""Chart generators for fatigue and shock analysis - matplotlib and plotly."""

import numpy as np
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend
import matplotlib.pyplot as plt
import plotly.graph_objects as go

from weldfatigue.fatigue.sn_curve import SNCurve


class FatiguePlots:
    """Generate all fatigue-related plots."""

    @staticmethod
    def sn_curve_matplotlib(
        sn: SNCurve,
        highlight_point: tuple = None,
        title: str = None,
        labels: dict = None,
    ) -> plt.Figure:
        """Plot an S-N curve using matplotlib. Returns Figure.

        *labels* may contain keys: ``xaxis``, ``yaxis``, ``op_point``, ``knee``.
        """
        lb = labels or {}
        N_vals, stress_vals = sn.get_curve_points()

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.loglog(N_vals, stress_vals, "b-", linewidth=2, label=f"FAT {sn.fat_class}")

        if highlight_point:
            n_op, s_op = highlight_point
            ax.loglog(n_op, s_op, "ro", markersize=10,
                      label=lb.get("op_point", "Operating point"))

        ax.axvline(x=sn.N_knee, color="gray", linestyle="--", alpha=0.5,
                   label=lb.get("knee", "Knee point"))
        ax.axhline(y=sn.delta_sigma_knee, color="gray", linestyle=":", alpha=0.5)

        ax.set_xlabel(lb.get("xaxis", "Number of cycles N"), fontsize=12)
        ax.set_ylabel(lb.get("yaxis", "Stress range [MPa]"), fontsize=12)
        ax.set_title(
            title or f"S-N Curve - FAT {sn.fat_class} ({sn.material_type})",
            fontsize=14,
        )
        ax.legend(fontsize=10)
        ax.grid(True, which="both", alpha=0.3)
        ax.set_xlim(1e3, 1e9)
        fig.tight_layout()
        return fig

    @staticmethod
    def sn_curve_plotly(
        sn: SNCurve,
        highlight_point: tuple = None,
        title: str = None,
        labels: dict = None,
    ) -> go.Figure:
        """Plot an S-N curve using plotly for Streamlit.

        *labels* may contain keys: ``xaxis``, ``yaxis``, ``op_point``, ``knee``.
        """
        lb = labels or {}
        N_vals, stress_vals = sn.get_curve_points()

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=N_vals, y=stress_vals,
            mode="lines", name=f"FAT {sn.fat_class}",
            line={"color": "blue", "width": 2},
        ))

        if highlight_point:
            n_op, s_op = highlight_point
            fig.add_trace(go.Scatter(
                x=[n_op], y=[s_op],
                mode="markers",
                name=lb.get("op_point", "Operating point"),
                marker={"color": "red", "size": 12, "symbol": "circle"},
            ))

        fig.update_layout(
            title=title or f"S-N Curve - FAT {sn.fat_class} ({sn.material_type})",
            xaxis={"title": lb.get("xaxis", "Number of cycles N"), "type": "log"},
            yaxis={"title": lb.get("yaxis", "Stress range [MPa]"), "type": "log"},
            template="plotly_white",
        )
        return fig

    @staticmethod
    def haigh_diagram_plotly(
        Se: float,
        Su: float,
        Sy: float = None,
        operating_points: list[tuple] = None,
        labels: dict = None,
    ) -> go.Figure:
        """Plot a Goodman/Haigh diagram with operating points.

        *labels* may contain keys: ``title``, ``xaxis``, ``yaxis``, ``point_fmt``.
        """
        lb = labels or {}
        from weldfatigue.fatigue.mean_stress import MeanStressCorrection

        fig = go.Figure()

        mean_g, amp_g = MeanStressCorrection.haigh_diagram_points(Se, Su, "goodman")
        fig.add_trace(go.Scatter(
            x=mean_g, y=amp_g, mode="lines", name="Goodman",
            line={"color": "blue", "width": 2},
        ))

        mean_ge, amp_ge = MeanStressCorrection.haigh_diagram_points(Se, Su, "gerber")
        fig.add_trace(go.Scatter(
            x=mean_ge, y=amp_ge, mode="lines", name="Gerber",
            line={"color": "green", "width": 2, "dash": "dash"},
        ))

        if operating_points:
            point_fmt = lb.get("point_fmt", "Point {i}")
            for i, (sm, sa) in enumerate(operating_points):
                fig.add_trace(go.Scatter(
                    x=[sm], y=[sa], mode="markers",
                    name=point_fmt.format(i=i + 1),
                    marker={"size": 10, "symbol": "diamond"},
                ))

        fig.update_layout(
            title=lb.get("title", "Haigh Diagram (Mean Stress Correction)"),
            xaxis={"title": lb.get("xaxis", "Mean stress [MPa]")},
            yaxis={"title": lb.get("yaxis", "Stress amplitude [MPa]")},
            template="plotly_white",
        )
        return fig

    @staticmethod
    def haigh_diagram_matplotlib(
        Se: float,
        Su: float,
        Sy: float = None,
        operating_points: list[tuple] = None,
        labels: dict = None,
    ) -> plt.Figure:
        """Plot a Goodman/Haigh diagram using matplotlib for PDF reports.

        *labels* may contain keys: ``title``, ``xaxis``, ``yaxis``, ``point_fmt``.
        """
        lb = labels or {}
        from weldfatigue.fatigue.mean_stress import MeanStressCorrection

        fig, ax = plt.subplots(figsize=(10, 6))

        mean_g, amp_g = MeanStressCorrection.haigh_diagram_points(Se, Su, "goodman")
        ax.plot(mean_g, amp_g, "b-", linewidth=2, label="Goodman")

        mean_ge, amp_ge = MeanStressCorrection.haigh_diagram_points(Se, Su, "gerber")
        ax.plot(mean_ge, amp_ge, "g--", linewidth=2, label="Gerber")

        if operating_points:
            point_fmt = lb.get("point_fmt", "Point {i}")
            for i, (sm, sa) in enumerate(operating_points):
                ax.plot(sm, sa, "rd", markersize=10,
                        label=point_fmt.format(i=i + 1))

        ax.set_xlabel(lb.get("xaxis", "Mean stress [MPa]"), fontsize=12)
        ax.set_ylabel(lb.get("yaxis", "Stress amplitude [MPa]"), fontsize=12)
        ax.set_title(lb.get("title", "Haigh Diagram"), fontsize=14)
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)
        fig.tight_layout()
        return fig

    @staticmethod
    def damage_histogram_plotly(
        damage_per_block: list[float],
        stress_ranges: list[float],
        labels: dict = None,
    ) -> go.Figure:
        """Bar chart of damage contribution per load block.

        *labels* may contain keys: ``title``, ``xaxis``, ``yaxis``.
        """
        lb = labels or {}
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=[f"{sr:.0f} MPa" for sr in stress_ranges],
            y=damage_per_block,
            marker_color="steelblue",
        ))
        fig.update_layout(
            title=lb.get("title", "Damage Contribution per Load Block"),
            xaxis={"title": lb.get("xaxis", "Stress range")},
            yaxis={"title": lb.get("yaxis", "Damage ratio (ni/Ni)")},
            template="plotly_white",
        )
        return fig

    # ------------------------------------------------------------------
    # Crack growth (fracture mechanics)
    # ------------------------------------------------------------------

    @staticmethod
    def crack_growth_plotly(
        crack_sizes: list[float],
        cycle_counts: list[float],
        critical_crack: float = None,
        title: str = None,
        labels: dict = None,
    ) -> go.Figure:
        """Plot crack size *a* vs number of cycles *N* using plotly.

        *labels* may contain keys: ``xaxis``, ``yaxis``, ``trace``,
        ``critical``.
        """
        lb = labels or {}
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=cycle_counts, y=crack_sizes,
            mode="lines", name=lb.get("trace", "Crack size a(N)"),
            line={"color": "darkred", "width": 2},
        ))

        if critical_crack is not None:
            fig.add_hline(
                y=critical_crack, line_dash="dash", line_color="red",
                annotation_text=lb.get("critical",
                                       f"Critical a_c = {critical_crack:.2f} mm"),
            )

        fig.update_layout(
            title=title or "Crack Growth (a vs N)",
            xaxis={"title": lb.get("xaxis", "Number of cycles N")},
            yaxis={"title": lb.get("yaxis", "Crack size a [mm]")},
            template="plotly_white",
        )
        return fig

    @staticmethod
    def crack_growth_matplotlib(
        crack_sizes: list[float],
        cycle_counts: list[float],
        critical_crack: float = None,
        title: str = None,
        labels: dict = None,
    ) -> plt.Figure:
        """Plot crack size *a* vs number of cycles *N* using matplotlib.

        *labels* may contain keys: ``xaxis``, ``yaxis``, ``trace``,
        ``critical``.
        """
        lb = labels or {}
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(cycle_counts, crack_sizes, "r-", linewidth=2,
                label=lb.get("trace", "Crack size a(N)"))

        if critical_crack is not None:
            ax.axhline(y=critical_crack, color="red", linestyle="--", alpha=0.7,
                       label=lb.get("critical",
                                    f"Critical a_c = {critical_crack:.2f} mm"))

        ax.set_xlabel(lb.get("xaxis", "Number of cycles N"), fontsize=12)
        ax.set_ylabel(lb.get("yaxis", "Crack size a [mm]"), fontsize=12)
        ax.set_title(title or "Crack Growth (a vs N)", fontsize=14)
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)
        fig.tight_layout()
        return fig

    # ------------------------------------------------------------------
    # Multiaxial interaction (Gough-Pollard ellipse)
    # ------------------------------------------------------------------

    @staticmethod
    def multiaxial_interaction_plotly(
        normal_util: float,
        shear_util: float,
        title: str = None,
        labels: dict = None,
    ) -> go.Figure:
        """Gough-Pollard interaction ellipse diagram using plotly.

        Draws the unit circle (x^2 + y^2 = 1) and plots the operating
        point.  Annotates PASS or FAIL.

        *labels* may contain keys: ``xaxis``, ``yaxis``, ``boundary``,
        ``point``.
        """
        lb = labels or {}
        theta = np.linspace(0, 2 * np.pi, 200)
        x_circle = np.cos(theta)
        y_circle = np.sin(theta)

        fig = go.Figure()
        # Unit circle / ellipse boundary
        fig.add_trace(go.Scatter(
            x=x_circle, y=y_circle,
            mode="lines",
            name=lb.get("boundary", "Interaction limit"),
            line={"color": "blue", "width": 2},
        ))

        # Operating point
        interaction = normal_util ** 2 + shear_util ** 2
        status = "PASS" if interaction <= 1.0 else "FAIL"
        marker_color = "green" if interaction <= 1.0 else "red"

        fig.add_trace(go.Scatter(
            x=[normal_util], y=[shear_util],
            mode="markers+text",
            name=lb.get("point", f"Operating point ({status})"),
            marker={"color": marker_color, "size": 14, "symbol": "circle"},
            text=[status],
            textposition="top right",
            textfont={"size": 14, "color": marker_color},
        ))

        fig.update_layout(
            title=title or "Gough-Pollard Multiaxial Interaction",
            xaxis={"title": lb.get("xaxis",
                                    "Normal stress utilization "
                                    "(delta_sigma / delta_sigma_R)"),
                    "range": [-0.1, max(1.3, normal_util + 0.2)]},
            yaxis={"title": lb.get("yaxis",
                                    "Shear stress utilization "
                                    "(delta_tau / delta_tau_R)"),
                    "scaleanchor": "x", "scaleratio": 1,
                    "range": [-0.1, max(1.3, shear_util + 0.2)]},
            template="plotly_white",
        )
        return fig

    @staticmethod
    def multiaxial_interaction_matplotlib(
        normal_util: float,
        shear_util: float,
        title: str = None,
        labels: dict = None,
    ) -> plt.Figure:
        """Gough-Pollard interaction ellipse diagram using matplotlib.

        Draws the unit circle (x^2 + y^2 = 1) and plots the operating
        point.  Annotates PASS or FAIL.

        *labels* may contain keys: ``xaxis``, ``yaxis``, ``boundary``,
        ``point``.
        """
        lb = labels or {}
        theta = np.linspace(0, 2 * np.pi, 200)
        x_circle = np.cos(theta)
        y_circle = np.sin(theta)

        fig, ax = plt.subplots(figsize=(8, 8))
        ax.plot(x_circle, y_circle, "b-", linewidth=2,
                label=lb.get("boundary", "Interaction limit"))

        interaction = normal_util ** 2 + shear_util ** 2
        status = "PASS" if interaction <= 1.0 else "FAIL"
        marker_color = "green" if interaction <= 1.0 else "red"

        ax.plot(normal_util, shear_util, "o", color=marker_color,
                markersize=12,
                label=lb.get("point", f"Operating point ({status})"))
        ax.annotate(
            status,
            xy=(normal_util, shear_util),
            xytext=(normal_util + 0.08, shear_util + 0.08),
            fontsize=14, fontweight="bold", color=marker_color,
        )

        ax.set_xlabel(
            lb.get("xaxis",
                    "Normal stress utilization (delta_sigma / delta_sigma_R)"),
            fontsize=12,
        )
        ax.set_ylabel(
            lb.get("yaxis",
                    "Shear stress utilization (delta_tau / delta_tau_R)"),
            fontsize=12,
        )
        ax.set_title(
            title or "Gough-Pollard Multiaxial Interaction", fontsize=14,
        )
        ax.set_aspect("equal")
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)
        fig.tight_layout()
        return fig

    # ------------------------------------------------------------------
    # Treatment comparison bar chart
    # ------------------------------------------------------------------

    @staticmethod
    def treatment_comparison_plotly(
        treatment_results: dict,
        title: str = None,
        labels: dict = None,
    ) -> go.Figure:
        """Bar chart comparing FAT class upgrades for post-weld treatments.

        *treatment_results* maps treatment name to upgraded FAT class
        (e.g. output of ``PostWeldTreatmentFactors.improvement_summary()``).

        *labels* may contain keys: ``title``, ``xaxis``, ``yaxis``.
        """
        lb = labels or {}
        names = list(treatment_results.keys())
        values = list(treatment_results.values())

        colors = [
            "gray" if n == "none" else "steelblue" for n in names
        ]

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=names, y=values,
            marker_color=colors,
            text=[str(v) for v in values],
            textposition="outside",
        ))
        fig.update_layout(
            title=lb.get("title",
                         title or "Post-Weld Treatment FAT Class Comparison"),
            xaxis={"title": lb.get("xaxis", "Treatment")},
            yaxis={"title": lb.get("yaxis", "FAT class [MPa]")},
            template="plotly_white",
        )
        return fig

    @staticmethod
    def treatment_comparison_matplotlib(
        treatment_results: dict,
        title: str = None,
        labels: dict = None,
    ) -> plt.Figure:
        """Bar chart comparing FAT class upgrades for post-weld treatments.

        *treatment_results* maps treatment name to upgraded FAT class.

        *labels* may contain keys: ``title``, ``xaxis``, ``yaxis``.
        """
        lb = labels or {}
        names = list(treatment_results.keys())
        values = list(treatment_results.values())

        colors = [
            "gray" if n == "none" else "steelblue" for n in names
        ]

        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(names, values, color=colors)
        for bar, val in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                    str(val), ha="center", va="bottom", fontsize=10)

        ax.set_xlabel(lb.get("xaxis", "Treatment"), fontsize=12)
        ax.set_ylabel(lb.get("yaxis", "FAT class [MPa]"), fontsize=12)
        ax.set_title(
            lb.get("title",
                    title or "Post-Weld Treatment FAT Class Comparison"),
            fontsize=14,
        )
        ax.grid(True, axis="y", alpha=0.3)
        fig.tight_layout()
        return fig

    # ------------------------------------------------------------------
    # Safety factor waterfall chart (plotly only)
    # ------------------------------------------------------------------

    @staticmethod
    def safety_factor_waterfall_plotly(
        factors: dict,
        original_fat: int,
        title: str = None,
        labels: dict = None,
    ) -> go.Figure:
        """Waterfall chart showing how each safety factor reduces effective FAT.

        *factors* maps a factor name (e.g. ``"thickness"``, ``"treatment"``,
        ``"environment"``, ``"gamma_Mf"``) to its numeric value (>= 0).
        Each factor reduces the effective FAT by dividing (or multiplying).
        The waterfall starts at *original_fat* and each bar shows the
        reduction caused by that factor.

        *labels* may contain keys: ``title``, ``xaxis``, ``yaxis``.
        """
        lb = labels or {}
        categories = ["Original FAT"]
        values = [original_fat]
        running = float(original_fat)

        for name, factor_val in factors.items():
            if factor_val == 0:
                continue
            new_val = running / factor_val
            reduction = new_val - running
            categories.append(name)
            values.append(reduction)
            running = new_val

        categories.append("Effective FAT")
        values.append(running)

        # Build waterfall measure list
        measures = ["absolute"]
        measures.extend(["relative"] * len(factors))
        measures.append("total")

        fig = go.Figure(go.Waterfall(
            x=categories,
            y=values,
            measure=measures,
            textposition="outside",
            text=[f"{v:.1f}" for v in values],
            connector={"line": {"color": "gray", "width": 1}},
            increasing={"marker": {"color": "green"}},
            decreasing={"marker": {"color": "red"}},
            totals={"marker": {"color": "steelblue"}},
        ))

        fig.update_layout(
            title=lb.get("title",
                         title or "Safety Factor Waterfall on FAT Class"),
            xaxis={"title": lb.get("xaxis", "Factor")},
            yaxis={"title": lb.get("yaxis", "FAT class [MPa]")},
            template="plotly_white",
        )
        return fig

    # ------------------------------------------------------------------
    # Environmental S-N comparison
    # ------------------------------------------------------------------

    @staticmethod
    def environmental_sn_comparison_plotly(
        fat_class: int,
        material_type: str,
        environments: list[str],
        title: str = None,
        labels: dict = None,
    ) -> go.Figure:
        """Overlay S-N curves for different environments on the same plot.

        Uses ``EnvironmentalFactors.corrosion_factor()`` to obtain the
        corrected FAT class for each environment and then plots the
        corresponding ``SNCurve``.

        *labels* may contain keys: ``xaxis``, ``yaxis``.
        """
        lb = labels or {}
        from weldfatigue.fatigue.environmental import EnvironmentalFactors

        colors = [
            "blue", "orange", "red", "green", "purple",
            "brown", "magenta", "cyan",
        ]

        fig = go.Figure()
        for i, env in enumerate(environments):
            factor = EnvironmentalFactors.corrosion_factor(env, material_type)
            corrected_fat = int(round(fat_class * factor))
            sn = SNCurve(corrected_fat, material_type)
            N_vals, stress_vals = sn.get_curve_points()

            color = colors[i % len(colors)]
            fig.add_trace(go.Scatter(
                x=N_vals, y=stress_vals,
                mode="lines",
                name=f"{env} (FAT {corrected_fat})",
                line={"color": color, "width": 2},
            ))

        fig.update_layout(
            title=title or (f"S-N Curves - FAT {fat_class} "
                            f"({material_type}) by Environment"),
            xaxis={"title": lb.get("xaxis", "Number of cycles N"),
                    "type": "log"},
            yaxis={"title": lb.get("yaxis", "Stress range [MPa]"),
                    "type": "log"},
            template="plotly_white",
        )
        return fig

    @staticmethod
    def environmental_sn_comparison_matplotlib(
        fat_class: int,
        material_type: str,
        environments: list[str],
        title: str = None,
        labels: dict = None,
    ) -> plt.Figure:
        """Overlay S-N curves for different environments using matplotlib.

        Uses ``EnvironmentalFactors.corrosion_factor()`` to obtain the
        corrected FAT class for each environment and then plots the
        corresponding ``SNCurve``.

        *labels* may contain keys: ``xaxis``, ``yaxis``.
        """
        lb = labels or {}
        from weldfatigue.fatigue.environmental import EnvironmentalFactors

        colors = ["b", "orange", "r", "g", "purple", "brown", "m", "c"]

        fig, ax = plt.subplots(figsize=(10, 6))
        for i, env in enumerate(environments):
            factor = EnvironmentalFactors.corrosion_factor(env, material_type)
            corrected_fat = int(round(fat_class * factor))
            sn = SNCurve(corrected_fat, material_type)
            N_vals, stress_vals = sn.get_curve_points()

            color = colors[i % len(colors)]
            ax.loglog(N_vals, stress_vals, color=color, linewidth=2,
                      label=f"{env} (FAT {corrected_fat})")

        ax.set_xlabel(lb.get("xaxis", "Number of cycles N"), fontsize=12)
        ax.set_ylabel(lb.get("yaxis", "Stress range [MPa]"), fontsize=12)
        ax.set_title(
            title or (f"S-N Curves - FAT {fat_class} "
                      f"({material_type}) by Environment"),
            fontsize=14,
        )
        ax.set_xlim(1e3, 1e9)
        ax.legend(fontsize=10)
        ax.grid(True, which="both", alpha=0.3)
        fig.tight_layout()
        return fig

    # ------------------------------------------------------------------
    # PSD input (plotly only)
    # ------------------------------------------------------------------

    @staticmethod
    def psd_input_plotly(
        frequencies: list[float] | np.ndarray,
        psd_values: list[float] | np.ndarray,
        title: str = None,
        labels: dict = None,
    ) -> go.Figure:
        """Plot PSD vs frequency on a log-log scale using plotly.

        *labels* may contain keys: ``xaxis``, ``yaxis``, ``trace``.
        """
        lb = labels or {}
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=np.asarray(frequencies), y=np.asarray(psd_values),
            mode="lines",
            name=lb.get("trace", "Input PSD"),
            line={"color": "teal", "width": 2},
        ))

        fig.update_layout(
            title=title or "Power Spectral Density (PSD)",
            xaxis={"title": lb.get("xaxis", "Frequency [Hz]"),
                    "type": "log"},
            yaxis={"title": lb.get("yaxis", "PSD [MPa^2/Hz]"),
                    "type": "log"},
            template="plotly_white",
        )
        return fig

    # ------------------------------------------------------------------
    # Dirlik PDF (plotly only)
    # ------------------------------------------------------------------

    @staticmethod
    def dirlik_pdf_plotly(
        stress_ranges: list[float] | np.ndarray,
        pdf_values: list[float] | np.ndarray,
        title: str = None,
        labels: dict = None,
    ) -> go.Figure:
        """Plot Dirlik probability density function vs stress range.

        *labels* may contain keys: ``xaxis``, ``yaxis``, ``trace``.
        """
        lb = labels or {}
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=np.asarray(stress_ranges), y=np.asarray(pdf_values),
            mode="lines",
            name=lb.get("trace", "Dirlik PDF"),
            line={"color": "indigo", "width": 2},
            fill="tozeroy",
            fillcolor="rgba(75, 0, 130, 0.15)",
        ))

        fig.update_layout(
            title=title or "Dirlik Stress-Range PDF",
            xaxis={"title": lb.get("xaxis", "Stress range [MPa]")},
            yaxis={"title": lb.get("yaxis", "Probability density [1/MPa]")},
            template="plotly_white",
        )
        return fig


class ShockPlots:
    """Generate crash/shock-related plots."""

    @staticmethod
    def dynamic_yield_vs_strain_rate_plotly(
        material_name: str,
        static_yield: float,
        cs_D: float,
        cs_q: float,
        labels: dict = None,
    ) -> go.Figure:
        """Plot yield stress vs strain rate.

        *labels* may contain keys: ``title``, ``xaxis``, ``yaxis``,
        ``static_yield``.
        """
        lb = labels or {}
        from weldfatigue.materials.strain_rate import cowper_symonds_yield

        rates = np.logspace(-3, 4, 200)
        yields = [cowper_symonds_yield(static_yield, r, cs_D, cs_q) for r in rates]

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=rates, y=yields, mode="lines", name=material_name,
            line={"width": 2},
        ))
        fig.add_hline(
            y=static_yield, line_dash="dash", line_color="gray",
            annotation_text=lb.get("static_yield", "Static yield"),
        )

        fig.update_layout(
            title=lb.get("title",
                         f"Dynamic Yield vs Strain Rate - {material_name}"),
            xaxis={"title": lb.get("xaxis", "Strain rate [1/s]"), "type": "log"},
            yaxis={"title": lb.get("yaxis", "Yield stress [MPa]")},
            template="plotly_white",
        )
        return fig

    @staticmethod
    def force_displacement_plotly(
        force: np.ndarray,
        displacement: np.ndarray,
        metrics: dict = None,
        labels: dict = None,
    ) -> go.Figure:
        """Force-displacement curve with crush metrics.

        *labels* may contain keys: ``title``, ``xaxis``, ``yaxis``, ``trace``,
        ``mean_fmt``, ``peak_fmt``.
        """
        lb = labels or {}
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=displacement, y=force, mode="lines",
            name=lb.get("trace", "Force-Displacement"),
            line={"color": "red", "width": 2},
        ))

        if metrics:
            mean_f = metrics.get("mean_force", 0)
            peak_f = metrics.get("peak_force", 0)
            mean_fmt = lb.get("mean_fmt", "Mean: {v:.0f} N")
            peak_fmt = lb.get("peak_fmt", "Peak: {v:.0f} N")
            fig.add_hline(
                y=mean_f, line_dash="dash", line_color="blue",
                annotation_text=mean_fmt.format(v=mean_f),
            )
            fig.add_hline(
                y=peak_f, line_dash="dot", line_color="orange",
                annotation_text=peak_fmt.format(v=peak_f),
            )

        fig.update_layout(
            title=lb.get("title", "Force-Displacement Curve"),
            xaxis={"title": lb.get("xaxis", "Displacement [mm]")},
            yaxis={"title": lb.get("yaxis", "Force [N]")},
            template="plotly_white",
        )
        return fig
