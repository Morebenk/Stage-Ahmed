"""Parser for LS-DYNA keyword (.k / .key) files."""

import re
from pathlib import Path

import numpy as np

from weldfatigue.core.exceptions import FEAParsingError
from weldfatigue.fea.result_model import FEAResult


class LSDynaReader:
    """
    Parser for LS-DYNA keyword files and result files.

    Parses *NODE, *ELEMENT_SHELL, *ELEMENT_SOLID cards.
    Optional d3plot reading requires lasso-python.
    """

    def read_keyword(self, filepath: Path) -> FEAResult:
        """Parse an LS-DYNA keyword file for mesh data."""
        filepath = Path(filepath)
        if not filepath.exists():
            raise FEAParsingError(f"File not found: {filepath}")

        text = filepath.read_text(encoding="utf-8", errors="replace")

        nodes = self._parse_nodes(text)
        elements, elem_types = self._parse_elements(text)

        if len(nodes) == 0:
            raise FEAParsingError("No *NODE data found in keyword file.")

        node_ids = np.array([n[0] for n in nodes], dtype=int)
        node_coords = np.array([[n[1], n[2], n[3]] for n in nodes])

        element_ids = np.array([e[0] for e in elements], dtype=int) if elements else np.array([])
        connectivity = [np.array(e[2:], dtype=int) for e in elements]

        return FEAResult(
            node_ids=node_ids,
            node_coords=node_coords,
            element_ids=element_ids,
            element_connectivity=connectivity,
            element_types=elem_types,
            source_solver="ls-dyna",
        )

    def _parse_nodes(self, text: str) -> list[tuple]:
        """Parse *NODE card."""
        nodes = []
        in_node_block = False

        for line in text.split("\n"):
            stripped = line.strip()
            if stripped.upper().startswith("*NODE"):
                in_node_block = True
                continue
            if in_node_block:
                if stripped.startswith("*") or stripped.startswith("$"):
                    if stripped.startswith("$"):
                        continue
                    in_node_block = False
                    continue
                if not stripped:
                    continue
                parts = stripped.split()
                if len(parts) >= 4:
                    try:
                        nid = int(parts[0])
                        x, y, z = float(parts[1]), float(parts[2]), float(parts[3])
                        nodes.append((nid, x, y, z))
                    except (ValueError, IndexError):
                        continue
        return nodes

    def _parse_elements(self, text: str) -> tuple[list, list]:
        """Parse *ELEMENT_SHELL and *ELEMENT_SOLID cards."""
        elements = []
        elem_types = []
        in_block = False
        current_type = ""

        for line in text.split("\n"):
            stripped = line.strip()
            if stripped.upper().startswith("*ELEMENT_SHELL"):
                in_block = True
                current_type = "SHELL4"
                continue
            elif stripped.upper().startswith("*ELEMENT_SOLID"):
                in_block = True
                current_type = "SOLID8"
                continue
            elif stripped.startswith("*") and not stripped.startswith("$"):
                in_block = False
                continue

            if in_block:
                if stripped.startswith("$") or not stripped:
                    continue
                parts = stripped.split()
                if len(parts) >= 6:
                    try:
                        eid = int(parts[0])
                        pid = int(parts[1])
                        conn = [int(p) for p in parts[2:]]
                        elements.append([eid, pid] + conn)
                        elem_types.append(current_type)
                    except (ValueError, IndexError):
                        continue
        return elements, elem_types

    def read_d3plot(self, filepath: Path, states: list[int] = None) -> FEAResult:
        """Read d3plot binary (requires lasso-python)."""
        try:
            from lasso.dyna import D3plot, ArrayType
        except ImportError:
            raise ImportError(
                "lasso-python is required for d3plot reading. "
                "Install with: pip install weldfatigue[solvers]"
            )

        d3 = D3plot(str(filepath))

        node_ids = d3.arrays[ArrayType.node_ids]
        node_coords = d3.arrays[ArrayType.node_coordinates]

        result = FEAResult(
            node_ids=node_ids,
            node_coords=node_coords,
            source_solver="ls-dyna-d3plot",
        )

        # Try to get stress data
        if ArrayType.element_shell_stress in d3.arrays:
            shell_stress = d3.arrays[ArrayType.element_shell_stress]
            result.elemental_fields["shell_stress"] = shell_stress

        return result
