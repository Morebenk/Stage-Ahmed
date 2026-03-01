"""Tests for the IIW FAT class catalog."""

import pytest

from weldfatigue.fatigue.fat_classes import FATClassCatalog
from weldfatigue.core.exceptions import InvalidFATClassError


class TestFATClassCatalog:

    @pytest.fixture
    def catalog(self):
        return FATClassCatalog()

    def test_load_steel_details(self, catalog):
        details = catalog.list_all("steel")
        assert len(details) > 0

    def test_load_aluminum_details(self, catalog):
        details = catalog.list_all("aluminum")
        assert len(details) > 0

    def test_lookup_butt_tension_steel(self, catalog):
        matches = catalog.lookup("butt", "tension", "steel")
        assert len(matches) > 0
        fat_classes = [d.fat_class for d in matches]
        assert 80 in fat_classes

    def test_lookup_fillet_tension_steel(self, catalog):
        matches = catalog.lookup("fillet", "tension", "steel")
        assert len(matches) > 0

    def test_lookup_returns_correct_material(self, catalog):
        matches = catalog.lookup("butt", "tension", "aluminum")
        for d in matches:
            assert d.material == "aluminum"

    def test_get_fat_class_by_detail_number(self, catalog):
        fat = catalog.get_fat_class(125, "steel")
        assert fat == 80  # Detail 125 = FAT 80 for steel butt weld

    def test_get_fat_class_nonexistent(self, catalog):
        with pytest.raises(InvalidFATClassError):
            catalog.get_fat_class(99999, "steel")

    def test_recommend_most_conservative(self, catalog):
        rec = catalog.recommend("butt", "tension", "steel")
        assert rec is not None
        all_matches = catalog.lookup("butt", "tension", "steel")
        min_fat = min(d.fat_class for d in all_matches)
        assert rec.fat_class == min_fat

    def test_recommend_fillet_steel(self, catalog):
        rec = catalog.recommend("fillet", "tension", "steel")
        assert rec is not None
        assert rec.weld_type == "fillet"

    def test_recommend_no_match(self, catalog):
        rec = catalog.recommend("nonexistent_weld", "tension", "steel")
        assert rec is None

    def test_detail_has_description(self, catalog):
        details = catalog.list_all("steel")
        for d in details:
            assert len(d.description) > 0

    def test_t_joint_available(self, catalog):
        matches = catalog.lookup("t_joint", "tension", "steel")
        assert len(matches) > 0

    def test_shear_loading(self, catalog):
        matches = catalog.lookup("butt", "shear", "steel")
        assert len(matches) > 0
