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


# --- New schemas for enhancement features ---


class SafetyFactorInput(BaseModel):
    """Partial safety factor configuration."""

    consequence_class: str = Field(
        default="normal", description="Consequence of failure: low, normal, high"
    )
    inspection_level: str = Field(
        default="periodic", description="Inspection access: none, periodic, continuous"
    )
    standard: str = Field(default="iiw", description="Design standard: iiw, eurocode3, dnv")
    survival_probability: float = Field(
        default=0.977, ge=0.5, le=0.9999, description="Target survival probability"
    )


class SafetyFactorResult(BaseModel):
    """Computed partial safety factors."""

    gamma_Mf: float
    gamma_Ff: float
    dff: float
    characteristic_factor: float
    combined_factor: float


class MultiaxialInput(BaseModel):
    """Input for multiaxial fatigue assessment."""

    normal_stress_range: float = Field(..., gt=0, description="Normal stress range [MPa]")
    shear_stress_range: float = Field(..., gt=0, description="Shear stress range [MPa]")
    phase_angle: float = Field(default=0.0, description="Phase angle [degrees]")
    fat_normal: int = Field(..., description="FAT class for normal stress")
    fat_shear: int = Field(..., description="FAT class for shear stress")
    num_cycles: int = Field(..., gt=0, description="Number of applied cycles")
    method: str = Field(default="gough_pollard")


class MultiaxialResult(BaseModel):
    """Output of multiaxial fatigue assessment."""

    interaction_value: float
    normal_utilization: float
    shear_utilization: float
    is_proportional: bool
    method: str
    status: str


class CrackGrowthInput(BaseModel):
    """Input for fracture mechanics crack growth analysis."""

    initial_crack_size: float = Field(..., gt=0, description="Initial crack depth a0 [mm]")
    critical_crack_size: float = Field(..., gt=0, description="Critical crack depth a_c [mm]")
    stress_range: float = Field(..., gt=0, description="Applied stress range [MPa]")
    plate_thickness: float = Field(..., gt=0, description="Plate thickness [mm]")
    weld_geometry: str = Field(default="t_butt")
    paris_C: float = Field(default=5.21e-13, description="Paris law coefficient [mm/cycle]")
    paris_m: float = Field(default=3.0, description="Paris law exponent")
    delta_K_th: float = Field(default=0.0, ge=0, description="Threshold SIF range [MPa*sqrt(mm)]")


class CrackGrowthResult(BaseModel):
    """Output of fracture mechanics analysis."""

    total_cycles: float
    crack_sizes: list[float]
    cycle_counts: list[float]
    delta_K_initial: float
    delta_K_final: float
    status: str


class PSDInput(BaseModel):
    """Power Spectral Density input for vibration fatigue."""

    frequencies: list[float] = Field(..., description="Frequency array [Hz]")
    psd_values: list[float] = Field(..., description="PSD values [(MPa)^2/Hz]")
    duration: float = Field(..., gt=0, description="Exposure duration [seconds]")


class VibrationFatigueResult(BaseModel):
    """Output of frequency-domain fatigue assessment."""

    spectral_moments: dict[str, float]
    expected_peak_rate: float
    irregularity_factor: float
    damage_dirlik: float
    damage_narrowband: float
    damage_wirsching: float
    equivalent_stress_range: float
    status: str


class FourRInput(BaseModel):
    """Input for 4R method (Nykanen & Bjork 2016)."""

    notch_stress_range: float = Field(..., gt=0, description="Notch stress range [MPa]")
    stress_ratio: float = Field(default=0.0, description="Applied R-ratio")
    residual_stress: float = Field(default=0.0, description="Residual stress [MPa]")
    ultimate_strength: float = Field(..., gt=0, description="Material Rm [MPa]")
    yield_strength: float = Field(..., gt=0, description="Material Rp0.2 [MPa]")
    youngs_modulus: float = Field(default=210000.0, gt=0, description="Young's modulus [MPa]")
    num_cycles: int = Field(..., gt=0, description="Number of applied cycles")


class FourRResult(BaseModel):
    """Output of 4R method."""

    local_stress_ratio: float
    equivalent_stress_range: float
    allowable_cycles: float
    applied_cycles: int
    damage_ratio: float
    status: str
    master_curve_fat: int
