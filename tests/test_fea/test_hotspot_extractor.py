"""Tests for the hot-spot stress extractor from FEA results."""

import pytest
import numpy as np

from weldfatigue.fea.result_model import FEAResult
from weldfatigue.fea.hotspot_extractor import HotSpotExtractor


class TestHotSpotExtractor:

    @pytest.fixture
    def fea_with_path(self):
        """Create an FEA result with nodes along x-axis from weld toe."""
        t = 10.0  # plate thickness
        n_nodes = 20
        # Nodes from x=0 (weld toe) to x=30mm along the surface
        x_positions = np.linspace(0, 30, n_nodes)
        node_ids = np.arange(1, n_nodes + 1)
        node_coords = np.zeros((n_nodes, 3))
        node_coords[:, 0] = x_positions

        # Stress decreasing away from weld toe (typical hot-spot pattern)
        # sigma_xx dominant, others small
        sigma_xx = 200.0 * np.exp(-0.05 * x_positions)  # decaying
        stress_tensor = np.zeros((n_nodes, 6))
        stress_tensor[:, 0] = sigma_xx  # sigma_xx
        stress_tensor[:, 1] = 0.3 * sigma_xx  # sigma_yy
        stress_tensor[:, 2] = 0.0  # sigma_zz
        stress_tensor[:, 3] = 0.1 * sigma_xx  # tau_xy

        result = FEAResult(
            node_ids=node_ids,
            node_coords=node_coords,
            nodal_fields={"stress_tensor": stress_tensor},
        )
        return result, t

    def test_extract_path_stresses(self, fea_with_path):
        result, t = fea_with_path
        extractor = HotSpotExtractor(result, plate_thickness=t)
        distances, stresses = extractor.extract_path_stresses(
            weld_toe_node=1,
            path_direction=np.array([1.0, 0.0, 0.0]),
        )
        assert len(distances) > 0
        assert len(stresses) == len(distances)
        # Stresses should be positive (von Mises)
        assert all(s >= 0 for s in stresses)

    def test_extract_path_distances_sorted(self, fea_with_path):
        result, t = fea_with_path
        extractor = HotSpotExtractor(result, plate_thickness=t)
        distances, _ = extractor.extract_path_stresses(
            weld_toe_node=1,
            path_direction=np.array([1.0, 0.0, 0.0]),
        )
        # Distances should be sorted ascending
        for i in range(len(distances) - 1):
            assert distances[i] <= distances[i + 1]

    def test_compute_hotspot_type_a(self, fea_with_path):
        result, t = fea_with_path
        extractor = HotSpotExtractor(result, plate_thickness=t)
        hs_stress = extractor.compute_hotspot_stress(
            weld_toe_node=1,
            path_direction=np.array([1.0, 0.0, 0.0]),
            hotspot_type="a",
        )
        # Hot-spot stress should be positive
        assert hs_stress > 0

    def test_compute_hotspot_type_b(self, fea_with_path):
        result, t = fea_with_path
        extractor = HotSpotExtractor(result, plate_thickness=t)
        hs_stress = extractor.compute_hotspot_stress(
            weld_toe_node=1,
            path_direction=np.array([1.0, 0.0, 0.0]),
            hotspot_type="b",
        )
        assert hs_stress > 0

    def test_unknown_hotspot_type_raises(self, fea_with_path):
        result, t = fea_with_path
        extractor = HotSpotExtractor(result, plate_thickness=t)
        with pytest.raises(ValueError, match="Unknown hot-spot type"):
            extractor.compute_hotspot_stress(
                weld_toe_node=1,
                path_direction=np.array([1.0, 0.0, 0.0]),
                hotspot_type="c",
            )

    def test_nonexistent_node_raises(self, fea_with_path):
        result, t = fea_with_path
        extractor = HotSpotExtractor(result, plate_thickness=t)
        with pytest.raises(ValueError, match="not found"):
            extractor.extract_path_stresses(
                weld_toe_node=9999,
                path_direction=np.array([1.0, 0.0, 0.0]),
            )

    def test_hotspot_type_a_formula(self):
        """Verify Type a extrapolation: 1.67*s(0.4t) - 0.67*s(1.0t)."""
        t = 10.0
        # Create nodes at exactly 0.4t=4mm and 1.0t=10mm (and more)
        positions = np.array([0, 2, 4, 6, 8, 10, 12, 15, 18, 20], dtype=float)
        n = len(positions)
        node_ids = np.arange(1, n + 1)
        coords = np.zeros((n, 3))
        coords[:, 0] = positions

        # Uniform uniaxial stress for simplicity -> von Mises = sigma_xx
        sigma_vals = np.array([200, 180, 160, 140, 130, 120, 110, 100, 95, 90], dtype=float)
        stress = np.zeros((n, 6))
        stress[:, 0] = sigma_vals

        result = FEAResult(
            node_ids=node_ids,
            node_coords=coords,
            nodal_fields={"stress_tensor": stress},
        )
        extractor = HotSpotExtractor(result, plate_thickness=t)
        hs = extractor.compute_hotspot_stress(
            weld_toe_node=1,
            path_direction=np.array([1.0, 0.0, 0.0]),
            hotspot_type="a",
        )
        # s(0.4t=4mm)=160, s(1.0t=10mm)=120
        expected = 1.67 * 160 - 0.67 * 120
        assert hs == pytest.approx(expected, rel=0.05)
