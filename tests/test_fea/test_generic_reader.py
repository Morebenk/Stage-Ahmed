"""Tests for the generic CSV/numpy/DataFrame FEA reader."""

import pytest
import numpy as np
import pandas as pd
from pathlib import Path

from weldfatigue.fea.generic_reader import GenericCSVReader


class TestGenericCSVReader:

    @pytest.fixture
    def reader(self):
        return GenericCSVReader()

    @pytest.fixture
    def sample_df(self):
        return pd.DataFrame({
            "node_id": [1, 2, 3],
            "x": [0.0, 1.0, 2.0],
            "y": [0.0, 0.0, 0.0],
            "z": [0.0, 0.0, 0.0],
            "sigma_xx": [100.0, 200.0, 150.0],
            "sigma_yy": [50.0, 80.0, 60.0],
            "sigma_zz": [30.0, 40.0, 35.0],
            "tau_xy": [10.0, 20.0, 15.0],
            "tau_yz": [5.0, 8.0, 6.0],
            "tau_xz": [2.0, 3.0, 1.0],
        })

    def test_read_dataframe(self, reader, sample_df):
        result = reader.read_dataframe(sample_df)
        assert result.n_nodes == 3
        assert result.source_solver == "csv"

    def test_stress_tensor_from_df(self, reader, sample_df):
        result = reader.read_dataframe(sample_df)
        tensor = result.get_stress_tensor()
        assert tensor.shape == (3, 6)
        assert tensor[0, 0] == 100.0  # sigma_xx of node 1

    def test_node_coords_from_df(self, reader, sample_df):
        result = reader.read_dataframe(sample_df)
        assert result.node_coords[1, 0] == 1.0  # x of node 2

    def test_read_numpy(self, reader):
        coords = np.array([[0, 0, 0], [1, 0, 0]], dtype=float)
        stress = np.array([[100, 50, 30, 10, 5, 2], [200, 80, 40, 20, 8, 3]], dtype=float)
        result = reader.read_numpy(coords, stress)
        assert result.n_nodes == 2
        assert result.source_solver == "numpy"

    def test_read_numpy_auto_ids(self, reader):
        coords = np.array([[0, 0, 0], [1, 0, 0]], dtype=float)
        stress = np.array([[100, 50, 30, 10, 5, 2], [200, 80, 40, 20, 8, 3]], dtype=float)
        result = reader.read_numpy(coords, stress)
        np.testing.assert_array_equal(result.node_ids, [1, 2])

    def test_read_numpy_custom_ids(self, reader):
        coords = np.array([[0, 0, 0], [1, 0, 0]], dtype=float)
        stress = np.array([[100, 50, 30, 10, 5, 2], [200, 80, 40, 20, 8, 3]], dtype=float)
        ids = np.array([10, 20])
        result = reader.read_numpy(coords, stress, node_ids=ids)
        np.testing.assert_array_equal(result.node_ids, [10, 20])

    def test_df_with_displacement(self, reader, sample_df):
        sample_df["ux"] = [0.1, 0.2, 0.3]
        sample_df["uy"] = [0.0, 0.1, 0.0]
        sample_df["uz"] = [0.0, 0.0, 0.0]
        result = reader.read_dataframe(sample_df)
        disp = result.get_displacement()
        assert disp.shape == (3, 3)
        assert disp[0, 0] == pytest.approx(0.1)

    def test_df_missing_stress_columns(self, reader):
        df = pd.DataFrame({
            "node_id": [1],
            "x": [0.0], "y": [0.0], "z": [0.0],
            "sigma_xx": [100.0],
            # Missing other stress columns
        })
        result = reader.read_dataframe(df)
        assert "stress_tensor" not in result.nodal_fields

    def test_custom_column_mapping(self):
        mapping = {
            "node_id": "NID",
            "x": "X", "y": "Y", "z": "Z",
            "sigma_xx": "SXX", "sigma_yy": "SYY", "sigma_zz": "SZZ",
            "tau_xy": "SXY", "tau_yz": "SYZ", "tau_xz": "SXZ",
        }
        reader = GenericCSVReader(column_mapping=mapping)
        df = pd.DataFrame({
            "NID": [1], "X": [0.0], "Y": [0.0], "Z": [0.0],
            "SXX": [100.0], "SYY": [50.0], "SZZ": [30.0],
            "SXY": [10.0], "SYZ": [5.0], "SXZ": [2.0],
        })
        result = reader.read_dataframe(df)
        assert result.n_nodes == 1

    def test_read_csv_file(self, reader, tmp_path):
        csv_path = tmp_path / "test.csv"
        csv_path.write_text(
            "node_id,x,y,z,sigma_xx,sigma_yy,sigma_zz,tau_xy,tau_yz,tau_xz\n"
            "1,0,0,0,100,50,30,10,5,2\n"
            "2,1,0,0,200,80,40,20,8,3\n"
        )
        result = reader.read_stress_csv(csv_path)
        assert result.n_nodes == 2
