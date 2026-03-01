"""Material database: load, query, and filter automotive material grades."""

import json
from pathlib import Path
from typing import Optional

from weldfatigue.core.exceptions import MaterialNotFoundError
from weldfatigue.materials.models import AluminumGrade, Material, SteelGrade, WeldMaterial


class MaterialDatabase:
    """Loads and queries the material database from JSON files."""

    def __init__(self, data_dir: Optional[Path] = None):
        if data_dir is None:
            data_dir = Path(__file__).parent / "data"
        self.data_dir = data_dir
        self._materials: dict[str, Material] = {}
        self._weld_materials: dict[str, WeldMaterial] = {}
        self._load_all()

    def _load_all(self):
        self._load_steels()
        self._load_aluminums()
        self._load_weld_materials()

    def _load_steels(self):
        path = self.data_dir / "steel_grades.json"
        if not path.exists():
            return
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        for entry in data:
            grade = SteelGrade(**entry)
            self._materials[grade.name] = grade

    def _load_aluminums(self):
        path = self.data_dir / "aluminum_grades.json"
        if not path.exists():
            return
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        for entry in data:
            grade = AluminumGrade(**entry)
            self._materials[grade.name] = grade

    def _load_weld_materials(self):
        path = self.data_dir / "weld_materials.json"
        if not path.exists():
            return
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        for entry in data:
            wm = WeldMaterial(**entry)
            self._weld_materials[wm.base_material] = wm

    def get(self, name: str) -> Material:
        """Retrieve a material by grade name."""
        if name not in self._materials:
            raise MaterialNotFoundError(f"Material '{name}' not found in database.")
        return self._materials[name]

    def get_weld_properties(self, base_material: str) -> Optional[WeldMaterial]:
        """Get weld-specific properties for a base material."""
        return self._weld_materials.get(base_material)

    def list_grades(self, family: Optional[str] = None) -> list[str]:
        """List all available grade names, optionally filtered by family."""
        if family is None:
            return list(self._materials.keys())
        return [name for name, mat in self._materials.items() if mat.family == family]

    def search(
        self,
        min_yield: float = 0,
        max_yield: float = float("inf"),
        family: Optional[str] = None,
    ) -> list[Material]:
        """Filter materials by yield strength range and optionally by family."""
        results = []
        for mat in self._materials.values():
            if family and mat.family != family:
                continue
            if min_yield <= mat.yield_strength <= max_yield:
                results.append(mat)
        return results

    def get_strain_rate_params(self, name: str, model: str = "cowper_symonds") -> dict:
        """Get strain-rate model parameters for a specific grade."""
        mat = self.get(name)
        if model == "cowper_symonds":
            return {"D": mat.cs_D, "q": mat.cs_q}
        elif model == "johnson_cook":
            return {
                "A": mat.jc_A,
                "B": mat.jc_B,
                "n": mat.jc_n,
                "C": mat.jc_C,
                "m": mat.jc_m,
                "T_melt": mat.jc_T_melt,
                "T_ref": mat.jc_T_ref,
            }
        raise ValueError(f"Unknown model: {model}")

    def to_dataframe(self, family: Optional[str] = None):
        """Export material database to a pandas DataFrame."""
        import pandas as pd

        grades = self.list_grades(family)
        rows = []
        for name in grades:
            mat = self._materials[name]
            rows.append({
                "Name": mat.name,
                "Standard": mat.standard,
                "Family": mat.family,
                "Yield [MPa]": mat.yield_strength,
                "UTS [MPa]": mat.ultimate_strength,
                "E [MPa]": mat.youngs_modulus,
                "Density [kg/m3]": mat.density,
                "Elongation [%]": mat.elongation_at_break,
            })
        return pd.DataFrame(rows)
