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
