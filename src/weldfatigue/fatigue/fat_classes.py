"""IIW FAT class catalog for structural weld details."""

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from weldfatigue.core.exceptions import InvalidFATClassError


@dataclass
class FATDetail:
    """A single IIW FAT class detail entry."""

    fat_class: int
    detail_number: int
    description: str
    weld_type: str
    load_type: str
    material: str
    conditions: str = ""
    reference: str = "IIW XIII-1823-07"


class FATClassCatalog:
    """
    IIW FAT class catalog -- the complete table of classified structural
    details for fatigue assessment.

    Data sourced from IIW Recommendations XIII-1823-07/XV-1254-07.
    """

    def __init__(self, data_dir: Optional[Path] = None):
        if data_dir is None:
            data_dir = Path(__file__).parent / "data"
        self.data_dir = data_dir
        self._details: dict[str, list[FATDetail]] = {"steel": [], "aluminum": []}
        self._load_catalogs()

    def _load_catalogs(self):
        for material in ["steel", "aluminum"]:
            path = self.data_dir / f"fat_catalog_{material}.json"
            if not path.exists():
                continue
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            for entry in data:
                self._details[material].append(FATDetail(**entry))

    def lookup(
        self, weld_type: str, load_type: str, material: str = "steel"
    ) -> list[FATDetail]:
        """Find matching FAT details by weld type and loading."""
        return [
            d
            for d in self._details.get(material, [])
            if d.weld_type == weld_type and d.load_type == load_type
        ]

    def get_fat_class(self, detail_number: int, material: str = "steel") -> int:
        """Get the FAT class for a specific detail number."""
        for d in self._details.get(material, []):
            if d.detail_number == detail_number:
                return d.fat_class
        raise InvalidFATClassError(
            f"Detail number {detail_number} not found for {material}."
        )

    def list_all(self, material: str = "steel") -> list[FATDetail]:
        """Return all FAT details for a material family."""
        return self._details.get(material, [])

    def recommend(
        self, weld_type: str, load_type: str, material: str = "steel"
    ) -> Optional[FATDetail]:
        """Return the most conservative (lowest) matching FAT class."""
        matches = self.lookup(weld_type, load_type, material)
        if not matches:
            return None
        return min(matches, key=lambda d: d.fat_class)
