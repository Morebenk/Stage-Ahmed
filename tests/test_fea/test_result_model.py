"""Tests for the FEA result data model."""

import pytest
import numpy as np

from weldfatigue.fea.result_model import FEAResult


class TestFEAResult:

    @pytest.fixture
    def simple_result(self):
        node_ids = np.array([1, 2, 3])
        node_coords = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0]], dtype=float)
        stress = np.array([
            [100, 50, 30, 10, 5, 2],
            [200, 80, 40, 20, 8, 3],
            [150, 60, 35, 15, 6, 1],
        ], dtype=float)
        return FEAResult(
            node_ids=node_ids,
            node_coords=node_coords,
            nodal_fields={"stress_tensor": stress},
            source_solver="test",
        )

    def test_n_nodes(self, simple_result):
        assert simple_result.n_nodes == 3

    def test_n_elements_empty(self, simple_result):
        assert simple_result.n_elements == 0

    def test_get_stress_tensor(self, simple_result):
        tensor = simple_result.get_stress_tensor()
        assert tensor.shape == (3, 6)

    def test_get_stress_tensor_missing(self):
        result = FEAResult(
            node_ids=np.array([1]),
            node_coords=np.array([[0, 0, 0]]),
        )
        with pytest.raises(KeyError):
            result.get_stress_tensor()

    def test_get_displacement_missing(self, simple_result):
        with pytest.raises(KeyError):
            simple_result.get_displacement()

    def test_get_displacement(self):
        result = FEAResult(
            node_ids=np.array([1, 2]),
            node_coords=np.array([[0, 0, 0], [1, 0, 0]], dtype=float),
            nodal_fields={"displacement": np.array([[0.1, 0.2, 0.0], [0.3, 0.1, 0.0]])},
        )
        disp = result.get_displacement()
        assert disp.shape == (2, 3)

    def test_default_units(self, simple_result):
        assert simple_result.units["stress"] == "MPa"
        assert simple_result.units["length"] == "mm"

    def test_source_solver(self, simple_result):
        assert simple_result.source_solver == "test"

    def test_with_elements(self):
        result = FEAResult(
            node_ids=np.array([1, 2, 3]),
            node_coords=np.zeros((3, 3)),
            element_ids=np.array([1, 2]),
            element_connectivity=[[1, 2, 3], [2, 3, 1]],
            element_types=["TRIA3", "TRIA3"],
        )
        assert result.n_elements == 2
