"""Shared test fixtures."""

import pytest
import numpy as np
from pathlib import Path

from weldfatigue.materials.database import MaterialDatabase
from weldfatigue.fatigue.sn_curve import SNCurve
from weldfatigue.fatigue.fat_classes import FATClassCatalog


@pytest.fixture
def material_db():
    return MaterialDatabase()


@pytest.fixture
def fat_catalog():
    return FATClassCatalog()


@pytest.fixture
def sn_curve_fat71_steel():
    return SNCurve(fat_class=71, material_type="steel")


@pytest.fixture
def sn_curve_fat80_steel():
    return SNCurve(fat_class=80, material_type="steel")


@pytest.fixture
def sample_stress_tensor():
    """Sample stress tensor data (10 nodes, 6 components)."""
    np.random.seed(42)
    return np.random.uniform(-200, 200, (10, 6))


@pytest.fixture
def fixtures_dir():
    return Path(__file__).parent / "fixtures"
