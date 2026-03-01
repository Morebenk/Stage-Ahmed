"""Tests for stress tensor operations."""

import pytest
import numpy as np

from weldfatigue.fea.stress_tensor import StressTensorOps


class TestVonMises:

    def test_uniaxial(self):
        """Uniaxial tension: von Mises = |sigma_xx|."""
        tensor = np.array([[100, 0, 0, 0, 0, 0]], dtype=float)
        vm = StressTensorOps.von_mises(tensor)
        assert vm[0] == pytest.approx(100.0, rel=1e-6)

    def test_pure_shear(self):
        """Pure shear: von Mises = sqrt(3) * tau."""
        tau = 100.0
        tensor = np.array([[0, 0, 0, tau, 0, 0]], dtype=float)
        vm = StressTensorOps.von_mises(tensor)
        assert vm[0] == pytest.approx(np.sqrt(3) * tau, rel=1e-6)

    def test_hydrostatic(self):
        """Hydrostatic stress: von Mises = 0."""
        tensor = np.array([[100, 100, 100, 0, 0, 0]], dtype=float)
        vm = StressTensorOps.von_mises(tensor)
        assert vm[0] == pytest.approx(0.0, abs=1e-10)

    def test_batch(self, sample_stress_tensor):
        vm = StressTensorOps.von_mises(sample_stress_tensor)
        assert len(vm) == 10
        assert all(v >= 0 for v in vm)


class TestPrincipalStresses:

    def test_uniaxial(self):
        tensor = np.array([[100, 0, 0, 0, 0, 0]], dtype=float)
        s1, s2, s3 = StressTensorOps.principal_stresses(tensor)
        assert s1[0] == pytest.approx(100.0, rel=1e-6)
        assert s2[0] == pytest.approx(0.0, abs=1e-10)
        assert s3[0] == pytest.approx(0.0, abs=1e-10)

    def test_ordering(self, sample_stress_tensor):
        s1, s2, s3 = StressTensorOps.principal_stresses(sample_stress_tensor)
        for i in range(len(s1)):
            assert s1[i] >= s2[i] >= s3[i]


class TestMaxShear:

    def test_uniaxial(self):
        tensor = np.array([[200, 0, 0, 0, 0, 0]], dtype=float)
        ms = StressTensorOps.max_shear(tensor)
        assert ms[0] == pytest.approx(100.0, rel=1e-6)


class TestHydrostatic:

    def test_uniform(self):
        tensor = np.array([[100, 200, 300, 0, 0, 0]], dtype=float)
        h = StressTensorOps.hydrostatic(tensor)
        assert h[0] == pytest.approx(200.0, rel=1e-6)


class TestGenericReader:

    def test_read_csv(self, tmp_path):
        import pandas as pd
        from weldfatigue.fea.generic_reader import GenericCSVReader

        df = pd.DataFrame({
            "node_id": [1, 2, 3],
            "x": [0, 10, 20],
            "y": [0, 0, 0],
            "z": [0, 0, 0],
            "sigma_xx": [100, 150, 120],
            "sigma_yy": [50, 80, 60],
            "sigma_zz": [10, 20, 15],
            "tau_xy": [30, 40, 35],
            "tau_yz": [5, 10, 8],
            "tau_xz": [15, 25, 20],
        })
        csv_path = tmp_path / "test.csv"
        df.to_csv(csv_path, index=False)

        reader = GenericCSVReader()
        result = reader.read_stress_csv(csv_path)
        assert result.n_nodes == 3
        assert "stress_tensor" in result.nodal_fields

    def test_read_numpy(self):
        from weldfatigue.fea.generic_reader import GenericCSVReader

        coords = np.array([[0, 0, 0], [10, 0, 0]], dtype=float)
        stress = np.array([[100, 50, 10, 30, 5, 15], [150, 80, 20, 40, 10, 25]], dtype=float)

        reader = GenericCSVReader()
        result = reader.read_numpy(coords, stress)
        assert result.n_nodes == 2
