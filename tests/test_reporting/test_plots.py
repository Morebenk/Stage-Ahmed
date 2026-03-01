"""Tests for chart generators."""

import pytest
import numpy as np

from weldfatigue.fatigue.sn_curve import SNCurve
from weldfatigue.reporting.plots import FatiguePlots, ShockPlots


class TestFatiguePlots:

    @pytest.fixture
    def sn80(self):
        return SNCurve(fat_class=80, material_type="steel")

    def test_sn_curve_matplotlib_returns_figure(self, sn80):
        fig = FatiguePlots.sn_curve_matplotlib(sn80)
        import matplotlib.pyplot as plt
        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_sn_curve_matplotlib_with_highlight(self, sn80):
        import matplotlib.pyplot as plt
        fig = FatiguePlots.sn_curve_matplotlib(sn80, highlight_point=(1e6, 100))
        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_sn_curve_plotly_returns_figure(self, sn80):
        import plotly.graph_objects as go
        fig = FatiguePlots.sn_curve_plotly(sn80)
        assert isinstance(fig, go.Figure)

    def test_sn_curve_plotly_with_highlight(self, sn80):
        import plotly.graph_objects as go
        fig = FatiguePlots.sn_curve_plotly(sn80, highlight_point=(2e6, 80))
        assert isinstance(fig, go.Figure)
        # Should have 2 traces (curve + point)
        assert len(fig.data) == 2

    def test_haigh_diagram_plotly(self):
        import plotly.graph_objects as go
        fig = FatiguePlots.haigh_diagram_plotly(Se=100, Su=500, Sy=350)
        assert isinstance(fig, go.Figure)
        # At least Goodman + Gerber traces
        assert len(fig.data) >= 2

    def test_haigh_diagram_with_operating_points(self):
        import plotly.graph_objects as go
        points = [(50, 80), (100, 60)]
        fig = FatiguePlots.haigh_diagram_plotly(Se=100, Su=500, operating_points=points)
        # Goodman + Gerber + 2 operating points
        assert len(fig.data) == 4

    def test_damage_histogram(self):
        import plotly.graph_objects as go
        damage = [0.3, 0.2, 0.05]
        ranges = [100, 80, 50]
        fig = FatiguePlots.damage_histogram_plotly(damage, ranges)
        assert isinstance(fig, go.Figure)


class TestShockPlots:

    def test_dynamic_yield_vs_strain_rate(self):
        import plotly.graph_objects as go
        fig = ShockPlots.dynamic_yield_vs_strain_rate_plotly(
            material_name="DP600",
            static_yield=350,
            cs_D=40.4,
            cs_q=5.0,
        )
        assert isinstance(fig, go.Figure)

    def test_force_displacement(self):
        import plotly.graph_objects as go
        force = np.array([0, 5000, 10000, 8000, 7000])
        disp = np.array([0, 5, 10, 15, 20], dtype=float)
        fig = ShockPlots.force_displacement_plotly(force, disp)
        assert isinstance(fig, go.Figure)

    def test_force_displacement_with_metrics(self):
        import plotly.graph_objects as go
        force = np.array([0, 5000, 10000, 8000, 7000])
        disp = np.array([0, 5, 10, 15, 20], dtype=float)
        metrics = {"mean_force": 6000, "peak_force": 10000}
        fig = ShockPlots.force_displacement_plotly(force, disp, metrics=metrics)
        assert isinstance(fig, go.Figure)
