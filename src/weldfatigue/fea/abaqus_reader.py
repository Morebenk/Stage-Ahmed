"""Parser for Abaqus .inp files."""

from pathlib import Path

import numpy as np

from weldfatigue.core.exceptions import FEAParsingError
from weldfatigue.fea.result_model import FEAResult


class AbaqusReader:
    """
    Parser for Abaqus input (.inp) files.

    Parses *Node and *Element sections.
    Note: .odb binary reading requires the Abaqus Python API (proprietary).
    """

    def read_inp(self, filepath: Path) -> FEAResult:
        """Parse an Abaqus .inp file for mesh data."""
        filepath = Path(filepath)
        if not filepath.exists():
            raise FEAParsingError(f"File not found: {filepath}")

        text = filepath.read_text(encoding="utf-8", errors="replace")

        nodes = self._parse_nodes(text)
        elements, elem_types = self._parse_elements(text)

        if len(nodes) == 0:
            raise FEAParsingError("No *Node data found in .inp file.")

        node_ids = np.array([n[0] for n in nodes], dtype=int)
        node_coords = np.array([[n[1], n[2], n[3]] for n in nodes])

        element_ids = np.array([e[0] for e in elements], dtype=int) if elements else np.array([])
        connectivity = [np.array(e[1:], dtype=int) for e in elements]

        return FEAResult(
            node_ids=node_ids,
            node_coords=node_coords,
            element_ids=element_ids,
            element_connectivity=connectivity,
            element_types=elem_types,
            source_solver="abaqus",
        )

    def _parse_nodes(self, text: str) -> list[tuple]:
        """Parse *Node section."""
        nodes = []
        in_node = False

        for line in text.split("\n"):
            stripped = line.strip()
            if stripped.upper().startswith("*NODE"):
                in_node = True
                continue
            if in_node:
                if stripped.startswith("*"):
                    in_node = False
                    continue
                if not stripped or stripped.startswith("**"):
                    continue
                parts = [p.strip() for p in stripped.split(",")]
                if len(parts) >= 4:
                    try:
                        nid = int(parts[0])
                        x, y, z = float(parts[1]), float(parts[2]), float(parts[3])
                        nodes.append((nid, x, y, z))
                    except (ValueError, IndexError):
                        continue
        return nodes

    def _parse_elements(self, text: str) -> tuple[list, list]:
        """Parse *Element sections."""
        elements = []
        elem_types = []
        in_element = False
        current_type = ""

        for line in text.split("\n"):
            stripped = line.strip()
            if stripped.upper().startswith("*ELEMENT"):
                in_element = True
                # Extract type from header
                upper = stripped.upper()
                if "TYPE=" in upper:
                    type_str = upper.split("TYPE=")[1].split(",")[0].strip()
                    current_type = type_str
                else:
                    current_type = "UNKNOWN"
                continue
            if in_element:
                if stripped.startswith("*"):
                    in_element = False
                    continue
                if not stripped or stripped.startswith("**"):
                    continue
                parts = [int(p.strip()) for p in stripped.split(",") if p.strip()]
                if len(parts) >= 2:
                    elements.append(parts)
                    elem_types.append(current_type)

        return elements, elem_types
