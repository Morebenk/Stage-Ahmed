"""FEA result data model - solver-agnostic container."""

from dataclasses import dataclass, field

import numpy as np


@dataclass
class FEAResult:
    """
    Solver-agnostic container for FEA results.

    Stores nodal coordinates, element connectivity, and field data
    (stresses, strains, displacements, forces).
    """

    node_ids: np.ndarray  # (N_nodes,)
    node_coords: np.ndarray  # (N_nodes, 3)
    element_ids: np.ndarray = field(default_factory=lambda: np.array([]))
    element_connectivity: list = field(default_factory=list)
    element_types: list = field(default_factory=list)

    # Field data -- dict keyed by field name
    nodal_fields: dict[str, np.ndarray] = field(default_factory=dict)
    # e.g., {"stress_tensor": (N_nodes, 6), "displacement": (N_nodes, 3)}

    elemental_fields: dict[str, np.ndarray] = field(default_factory=dict)

    # Metadata
    source_solver: str = "generic"
    time_steps: list[float] = field(default_factory=list)
    units: dict[str, str] = field(
        default_factory=lambda: {"length": "mm", "stress": "MPa", "force": "N"}
    )

    @property
    def n_nodes(self) -> int:
        return len(self.node_ids)

    @property
    def n_elements(self) -> int:
        return len(self.element_ids)

    def get_stress_tensor(self) -> np.ndarray:
        """Get the stress tensor field (N_nodes, 6)."""
        if "stress_tensor" not in self.nodal_fields:
            raise KeyError("No stress tensor data available.")
        return self.nodal_fields["stress_tensor"]

    def get_displacement(self) -> np.ndarray:
        """Get displacement field (N_nodes, 3)."""
        if "displacement" not in self.nodal_fields:
            raise KeyError("No displacement data available.")
        return self.nodal_fields["displacement"]
