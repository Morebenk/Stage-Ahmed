"""Pydantic data models for all inputs and outputs."""

from typing import Optional

from pydantic import BaseModel, Field


class StressTensorResult(BaseModel):
    """6-component stress tensor at a point."""

    node_id: int
    sigma_xx: float  # Normal stress [MPa]
    sigma_yy: float
    sigma_zz: float
    tau_xy: float  # Shear stress [MPa]
    tau_yz: float
    tau_xz: float


class FatigueInput(BaseModel):
    """Input parameters for a fatigue assessment."""

    fat_class: int = Field(..., description="IIW FAT class (e.g., 71, 80, 90)")
    stress_range: float = Field(..., gt=0, description="Applied stress range [MPa]")
    stress_ratio: float = Field(default=0.0, description="R-ratio = sigma_min/sigma_max")
    num_cycles: int = Field(..., gt=0, description="Number of applied cycles")
    material_type: str = Field(default="steel", pattern="^(steel|aluminum)$")
    method: str = Field(default="nominal", pattern="^(nominal|hotspot|notch)$")


class FatigueResult(BaseModel):
    """Output of a fatigue assessment."""

    method: str
    fat_class: int
    allowable_cycles: float
    applied_cycles: int
    damage_ratio: float
    utilization: float
    status: str  # "PASS" or "FAIL"
    safety_factor: float


class CumulativeDamageResult(BaseModel):
    """Output of Palmgren-Miner summation."""

    total_damage: float
    damage_per_block: list[float]
    critical_block_index: int
    status: str  # "PASS" if D < 1.0, else "FAIL"


class CrashInput(BaseModel):
    """Input for a crash/shock assessment."""

    model_config = {"protected_namespaces": ()}

    strain_rate: float = Field(..., ge=0, description="Strain rate [1/s]")
    static_yield: float = Field(..., gt=0, description="Static yield stress [MPa]")
    model_type: str = Field(default="cowper_symonds")


class CrashResult(BaseModel):
    """Output of a crash assessment."""

    dynamic_yield: float
    enhancement_factor: float
    energy_absorbed: Optional[float] = None
    weld_status: Optional[str] = None


class WeldFailureResult(BaseModel):
    """Output of a weld failure check."""

    equivalent_stress: float
    allowable_stress: float
    utilization: float
    status: str  # "PASS" or "FAIL"
    criterion: str  # "force_based" or "stress_based"


class EnergyMetrics(BaseModel):
    """Energy absorption metrics for crash assessment."""

    total_energy: float  # [J]
    specific_energy_absorption: Optional[float] = None  # [J/kg]
    mean_force: float  # [N]
    peak_force: float  # [N]
    crush_force_efficiency: float  # Pm/Pmax
