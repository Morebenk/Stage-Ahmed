"""Extract hot-spot stresses from FEA results per IIW recommendations."""

import numpy as np
from scipy.interpolate import interp1d

from weldfatigue.fea.result_model import FEAResult
from weldfatigue.fea.stress_tensor import StressTensorOps


class HotSpotExtractor:
    """
    Extract hot-spot stresses from FEA results.

    Given FEA nodal stresses along a path perpendicular to the weld toe,
    perform surface stress extrapolation per IIW recommendations.
    """

    def __init__(self, fea_result: FEAResult, plate_thickness: float):
        self.fea = fea_result
        self.t = plate_thickness

    def extract_path_stresses(
        self,
        weld_toe_node: int,
        path_direction: np.ndarray,
        max_distance: float = None,
    ) -> tuple[np.ndarray, np.ndarray]:
        """
        Extract stresses along a path from the weld toe.

        Returns:
            (distances, stresses) arrays where stresses are von Mises.
        """
        if max_distance is None:
            max_distance = 2.0 * self.t

        # Find weld toe position
        toe_idx = np.nonzero(self.fea.node_ids == weld_toe_node)[0]
        if len(toe_idx) == 0:
            raise ValueError(f"Node {weld_toe_node} not found.")
        toe_pos = self.fea.node_coords[toe_idx[0]]

        # Normalize direction
        direction = path_direction / np.linalg.norm(path_direction)

        # Find nodes along path by projecting onto direction
        coords = self.fea.node_coords
        relative = coords - toe_pos
        projections = relative @ direction
        lateral_dist = np.linalg.norm(
            relative - np.outer(projections, direction), axis=1
        )

        # Select nodes close to the line and in the positive direction
        tolerance = self.t * 0.5
        mask = (projections > 0) & (projections <= max_distance) & (lateral_dist < tolerance)
        indices = np.nonzero(mask)[0]

        if len(indices) < 2:
            raise ValueError("Not enough nodes found along the specified path.")

        distances = projections[indices]
        sort_idx = np.argsort(distances)
        distances = distances[sort_idx]
        indices = indices[sort_idx]

        stress_tensor = self.fea.get_stress_tensor()
        vm_stresses = StressTensorOps.von_mises(stress_tensor[indices])

        return distances, vm_stresses

    def compute_hotspot_stress(
        self,
        weld_toe_node: int,
        path_direction: np.ndarray,
        hotspot_type: str = "a",
    ) -> float:
        """Compute the structural hot-spot stress by extrapolation."""
        distances, stresses = self.extract_path_stresses(
            weld_toe_node, path_direction
        )

        # Interpolate to get stresses at IIW reference points
        f = interp1d(distances, stresses, kind="linear", fill_value="extrapolate")

        if hotspot_type == "a":
            # Type a: reference points at 0.4t and 1.0t
            s_04t = float(f(0.4 * self.t))
            s_10t = float(f(1.0 * self.t))
            return 1.67 * s_04t - 0.67 * s_10t
        elif hotspot_type == "b":
            # Type b: reference points at 5mm, 15mm, 25mm
            s_5 = float(f(5.0))
            s_15 = float(f(15.0))
            s_25 = float(f(25.0))
            return 3.0 * s_5 - 3.0 * s_15 + s_25
        else:
            raise ValueError(f"Unknown hot-spot type: {hotspot_type}")
