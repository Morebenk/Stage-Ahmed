"""Parser for Nastran .bdf files."""

from pathlib import Path

import numpy as np

from weldfatigue.core.exceptions import FEAParsingError
from weldfatigue.fea.result_model import FEAResult


class NastranReader:
    """
    Parser for Nastran bulk data (.bdf) files.

    Parses GRID, CQUAD4, CTRIA3, CHEXA, CTETRA cards.
    For .op2 binary reading, use pyNastran.
    """

    def read_bdf(self, filepath: Path) -> FEAResult:
        """Parse a Nastran .bdf file for mesh data."""
        filepath = Path(filepath)
        if not filepath.exists():
            raise FEAParsingError(f"File not found: {filepath}")

        text = filepath.read_text(encoding="utf-8", errors="replace")

        nodes = self._parse_grids(text)
        elements, elem_types = self._parse_elements(text)

        if len(nodes) == 0:
            raise FEAParsingError("No GRID data found in .bdf file.")

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
            source_solver="nastran",
        )

    def _parse_grids(self, text: str) -> list[tuple]:
        """Parse GRID cards (free-field and fixed-field formats)."""
        nodes = []
        for line in text.split("\n"):
            stripped = line.strip()
            if stripped.upper().startswith("GRID"):
                if "," in stripped:
                    # Free-field format
                    parts = [p.strip() for p in stripped.split(",")]
                    if len(parts) >= 5:
                        try:
                            nid = int(parts[1])
                            x = float(parts[3]) if parts[3] else 0.0
                            y = float(parts[4]) if parts[4] else 0.0
                            z = float(parts[5]) if len(parts) > 5 and parts[5] else 0.0
                            nodes.append((nid, x, y, z))
                        except (ValueError, IndexError):
                            continue
                else:
                    # Fixed-field format (8 chars per field)
                    try:
                        nid = int(stripped[8:16].strip())
                        # Skip CP field (16:24)
                        x = float(stripped[24:32].strip()) if stripped[24:32].strip() else 0.0
                        y = float(stripped[32:40].strip()) if stripped[32:40].strip() else 0.0
                        z = float(stripped[40:48].strip()) if stripped[40:48].strip() else 0.0
                        nodes.append((nid, x, y, z))
                    except (ValueError, IndexError):
                        continue
        return nodes

    def _parse_elements(self, text: str) -> tuple[list, list]:
        """Parse element cards (CQUAD4, CTRIA3, CHEXA, CTETRA)."""
        elements = []
        elem_types = []
        elem_keywords = ["CQUAD4", "CTRIA3", "CHEXA", "CTETRA"]

        for line in text.split("\n"):
            stripped = line.strip().upper()
            for kw in elem_keywords:
                if stripped.startswith(kw):
                    if "," in stripped:
                        parts = [p.strip() for p in stripped.split(",")]
                    else:
                        # Fixed field: parse in 8-char blocks
                        parts = [stripped[i:i+8].strip() for i in range(0, len(stripped), 8)]
                    try:
                        eid = int(parts[1])
                        # Skip PID (parts[2])
                        conn = [int(p) for p in parts[3:] if p]
                        elements.append([eid] + conn)
                        elem_types.append(kw)
                    except (ValueError, IndexError):
                        continue
                    break

        return elements, elem_types

    def read_op2(self, filepath: Path):
        """Read .op2 binary results via pyNastran."""
        try:
            from pyNastran.op2.op2 import OP2
        except ImportError:
            raise ImportError(
                "pyNastran is required for .op2 reading. "
                "Install with: pip install weldfatigue[solvers]"
            )

        op2 = OP2()
        op2.read_op2(str(filepath))
        return op2
