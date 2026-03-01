"""Stress tensor operations for fatigue and crash post-processing."""

import numpy as np


class StressTensorOps:
    """
    Stress tensor operations.

    Works on arrays of shape (N, 6) where columns are:
        [sigma_xx, sigma_yy, sigma_zz, tau_xy, tau_yz, tau_xz]
    """

    @staticmethod
    def von_mises(tensor: np.ndarray) -> np.ndarray:
        """Compute von Mises equivalent stress for all nodes."""
        sxx, syy, szz = tensor[:, 0], tensor[:, 1], tensor[:, 2]
        txy, tyz, txz = tensor[:, 3], tensor[:, 4], tensor[:, 5]

        return np.sqrt(
            0.5
            * (
                (sxx - syy) ** 2
                + (syy - szz) ** 2
                + (szz - sxx) ** 2
                + 6.0 * (txy**2 + tyz**2 + txz**2)
            )
        )

    @staticmethod
    def principal_stresses(
        tensor: np.ndarray,
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Compute principal stresses (sigma_1 >= sigma_2 >= sigma_3)."""
        n = tensor.shape[0]
        s1 = np.zeros(n)
        s2 = np.zeros(n)
        s3 = np.zeros(n)

        for i in range(n):
            mat = np.array([
                [tensor[i, 0], tensor[i, 3], tensor[i, 5]],
                [tensor[i, 3], tensor[i, 1], tensor[i, 4]],
                [tensor[i, 5], tensor[i, 4], tensor[i, 2]],
            ])
            eigenvalues = np.linalg.eigvalsh(mat)
            # Sort descending
            eigenvalues = np.sort(eigenvalues)[::-1]
            s1[i], s2[i], s3[i] = eigenvalues

        return s1, s2, s3

    @staticmethod
    def max_shear(tensor: np.ndarray) -> np.ndarray:
        """Maximum shear stress = (sigma_1 - sigma_3) / 2."""
        s1, _, s3 = StressTensorOps.principal_stresses(tensor)
        return (s1 - s3) / 2.0

    @staticmethod
    def hydrostatic(tensor: np.ndarray) -> np.ndarray:
        """Hydrostatic stress = (sigma_xx + sigma_yy + sigma_zz) / 3."""
        return (tensor[:, 0] + tensor[:, 1] + tensor[:, 2]) / 3.0

    @staticmethod
    def stress_range(
        tensor_max: np.ndarray, tensor_min: np.ndarray
    ) -> np.ndarray:
        """Compute stress range tensor and its von Mises equivalent."""
        delta = tensor_max - tensor_min
        return StressTensorOps.von_mises(delta)

    @staticmethod
    def transform_to_weld_local(
        tensor: np.ndarray,
        weld_direction: np.ndarray,
        normal: np.ndarray,
    ) -> np.ndarray:
        """
        Transform stress tensor to weld local coordinate system.

        Args:
            tensor: (N, 6) stress tensor in global coordinates
            weld_direction: Unit vector along the weld line
            normal: Unit vector normal to the plate surface

        Returns:
            (N, 6) stress tensor in weld-local coordinates
            [sigma_perp, sigma_parallel, sigma_normal, tau_perp, tau_normal_parallel, tau_perp_normal]
        """
        # Build rotation matrix
        e1 = weld_direction / np.linalg.norm(weld_direction)
        e3 = normal / np.linalg.norm(normal)
        e2 = np.cross(e3, e1)
        e2 = e2 / np.linalg.norm(e2)

        R = np.array([e2, e1, e3])  # perpendicular, parallel, normal

        n = tensor.shape[0]
        result = np.zeros_like(tensor)

        for i in range(n):
            mat = np.array([
                [tensor[i, 0], tensor[i, 3], tensor[i, 5]],
                [tensor[i, 3], tensor[i, 1], tensor[i, 4]],
                [tensor[i, 5], tensor[i, 4], tensor[i, 2]],
            ])
            rotated = R @ mat @ R.T
            result[i, 0] = rotated[0, 0]  # sigma_perp
            result[i, 1] = rotated[1, 1]  # sigma_parallel
            result[i, 2] = rotated[2, 2]  # sigma_normal
            result[i, 3] = rotated[0, 1]  # tau_perp_parallel
            result[i, 4] = rotated[1, 2]  # tau_parallel_normal
            result[i, 5] = rotated[0, 2]  # tau_perp_normal

        return result
