"""Tests for the material database."""

import pytest

from weldfatigue.materials.database import MaterialDatabase
from weldfatigue.core.exceptions import MaterialNotFoundError


class TestMaterialDatabase:

    def test_load_steels(self, material_db):
        grades = material_db.list_grades("steel")
        assert len(grades) >= 9
        assert "DP600" in grades
        assert "S355J2" in grades

    def test_load_aluminums(self, material_db):
        grades = material_db.list_grades("aluminum")
        assert len(grades) >= 5
        assert "6061-T6" in grades

    def test_get_dp600(self, material_db):
        mat = material_db.get("DP600")
        assert mat.name == "DP600"
        assert mat.yield_strength == 350
        assert mat.ultimate_strength == 600
        assert mat.family == "steel"

    def test_get_6061_t6(self, material_db):
        mat = material_db.get("6061-T6")
        assert mat.yield_strength == 276
        assert mat.family == "aluminum"

    def test_get_nonexistent_raises(self, material_db):
        with pytest.raises(MaterialNotFoundError):
            material_db.get("FAKE_MATERIAL")

    def test_search_by_yield(self, material_db):
        results = material_db.search(min_yield=400, max_yield=700)
        names = [m.name for m in results]
        assert "DP780" in names
        assert "DP600" not in names  # yield=350

    def test_search_by_family(self, material_db):
        results = material_db.search(family="aluminum")
        for mat in results:
            assert mat.family == "aluminum"

    def test_strain_rate_params_cs(self, material_db):
        params = material_db.get_strain_rate_params("DP600", "cowper_symonds")
        assert "D" in params
        assert "q" in params
        assert params["D"] == 100
        assert params["q"] == 4.73

    def test_strain_rate_params_jc(self, material_db):
        params = material_db.get_strain_rate_params("DP600", "johnson_cook")
        assert params["A"] == 330

    def test_to_dataframe(self, material_db):
        df = material_db.to_dataframe("steel")
        assert len(df) >= 9
        assert "Name" in df.columns
        assert "Yield [MPa]" in df.columns

    def test_weld_properties(self, material_db):
        wp = material_db.get_weld_properties("DP600")
        assert wp is not None
        assert wp.haz_yield_factor < 1.0
