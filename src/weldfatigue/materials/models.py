"""Material data models for automotive steels and aluminum alloys."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Material:
    """Base material model."""

    name: str = ""
    standard: str = ""
    family: str = ""  # "steel" or "aluminum"
    density: float = 0.0  # [kg/m3]
    youngs_modulus: float = 0.0  # E [MPa]
    poissons_ratio: float = 0.0
    yield_strength: float = 0.0  # Rp0.2 [MPa]
    ultimate_strength: float = 0.0  # Rm [MPa]
    elongation_at_break: float = 0.0  # A80 [%]
    thermal_expansion: Optional[float] = None  # [1/K]


@dataclass
class SteelGrade(Material):
    """Steel with automotive-specific properties and strain-rate parameters."""

    family: str = "steel"
    carbon_equivalent: Optional[float] = None
    # Cowper-Symonds parameters
    cs_D: float = 40.4  # [1/s] typical for mild steel
    cs_q: float = 5.0
    # Johnson-Cook parameters
    jc_A: Optional[float] = None  # [MPa]
    jc_B: Optional[float] = None  # [MPa]
    jc_n: Optional[float] = None
    jc_C: Optional[float] = None
    jc_m: Optional[float] = None
    jc_T_melt: Optional[float] = None  # [K]
    jc_T_ref: float = 293.0  # [K]


@dataclass
class AluminumGrade(Material):
    """Aluminum alloy with strain-rate parameters."""

    family: str = "aluminum"
    temper: str = ""
    # Cowper-Symonds parameters
    cs_D: float = 6500.0  # [1/s] typical for aluminum
    cs_q: float = 4.0
    # Johnson-Cook parameters
    jc_A: Optional[float] = None
    jc_B: Optional[float] = None
    jc_n: Optional[float] = None
    jc_C: Optional[float] = None
    jc_m: Optional[float] = None
    jc_T_melt: Optional[float] = None
    jc_T_ref: float = 293.0


@dataclass
class WeldMaterial:
    """Weld-specific material properties including HAZ."""

    base_material: str = ""
    weld_process: str = ""  # "MIG", "TIG", "laser", "resistance_spot"
    haz_yield_factor: float = 0.85  # Fraction of base metal yield in HAZ
    haz_uts_factor: float = 0.90
    haz_width: float = 3.0  # [mm] typical HAZ width
    filler_yield: Optional[float] = None  # [MPa]
    filler_uts: Optional[float] = None
