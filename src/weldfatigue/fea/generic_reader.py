"""Solver-agnostic readers for FEA results from CSV, numpy, and DataFrames."""

from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd

from weldfatigue.fea.result_model import FEAResult


class GenericCSVReader:
    """
    Solver-agnostic reader for FEA results stored in CSV or numpy format.

    Expected CSV format (minimum):
        node_id, x, y, z, sigma_xx, sigma_yy, sigma_zz, tau_xy, tau_yz, tau_xz
    """

    DEFAULT_MAPPING = {
        "node_id": "node_id",
        "x": "x",
        "y": "y",
        "z": "z",
        "sigma_xx": "sigma_xx",
        "sigma_yy": "sigma_yy",
        "sigma_zz": "sigma_zz",
        "tau_xy": "tau_xy",
        "tau_yz": "tau_yz",
        "tau_xz": "tau_xz",
    }

    def __init__(self, column_mapping: Optional[dict] = None):
        self.column_mapping = column_mapping or self.DEFAULT_MAPPING

    def read_stress_csv(self, filepath: Path) -> FEAResult:
        """Read nodal stress results from a CSV file."""
        df = pd.read_csv(filepath)
        return self._parse_dataframe(df)

    def read_numpy(
        self,
        node_coords: np.ndarray,
        stress_tensor: np.ndarray,
        node_ids: Optional[np.ndarray] = None,
    ) -> FEAResult:
        """Create FEAResult directly from numpy arrays."""
        n_nodes = node_coords.shape[0]
        if node_ids is None:
            node_ids = np.arange(1, n_nodes + 1)

        return FEAResult(
            node_ids=node_ids,
            node_coords=node_coords,
            nodal_fields={"stress_tensor": stress_tensor},
            source_solver="numpy",
        )

    def read_dataframe(self, df: pd.DataFrame) -> FEAResult:
        """Create FEAResult from a pandas DataFrame."""
        return self._parse_dataframe(df)

    def _parse_dataframe(self, df: pd.DataFrame) -> FEAResult:
        """Parse a DataFrame into an FEAResult."""
        m = self.column_mapping

        node_ids = df[m["node_id"]].values.astype(int)
        node_coords = df[[m["x"], m["y"], m["z"]]].values

        stress_cols = [
            m["sigma_xx"], m["sigma_yy"], m["sigma_zz"],
            m["tau_xy"], m["tau_yz"], m["tau_xz"],
        ]

        # Check which stress columns exist
        available = [c for c in stress_cols if c in df.columns]
        if len(available) == 6:
            stress_tensor = df[stress_cols].values
            nodal_fields = {"stress_tensor": stress_tensor}
        else:
            nodal_fields = {}

        # Check for displacement columns
        disp_cols = ["ux", "uy", "uz"]
        if all(c in df.columns for c in disp_cols):
            nodal_fields["displacement"] = df[disp_cols].values

        return FEAResult(
            node_ids=node_ids,
            node_coords=node_coords,
            nodal_fields=nodal_fields,
            source_solver="csv",
        )
