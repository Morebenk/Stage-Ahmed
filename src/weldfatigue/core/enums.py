"""Enumerations for the weldfatigue package."""

from enum import Enum


class WeldType(str, Enum):
    BUTT = "butt"
    FILLET = "fillet"
    CRUCIFORM = "cruciform"
    LAP = "lap"
    T_JOINT = "t_joint"
    STIFFENER = "stiffener"
    SPOT = "spot"
    LASER_BUTT = "laser_butt"
    LASER_FILLET = "laser_fillet"
    FSW_BUTT = "fsw_butt"


class LoadType(str, Enum):
    TENSION = "tension"
    BENDING = "bending"
    SHEAR = "shear"
    COMBINED = "combined"


class MaterialFamily(str, Enum):
    STEEL = "steel"
    ALUMINUM = "aluminum"


class AssessmentMethod(str, Enum):
    NOMINAL = "nominal"
    HOTSPOT = "hotspot"
    NOTCH = "notch"
    MULTIAXIAL = "multiaxial"
    FRACTURE_MECHANICS = "fracture_mechanics"
    ROOT = "root"
    FOUR_R = "four_r"


class StrainRateModel(str, Enum):
    COWPER_SYMONDS = "cowper_symonds"
    JOHNSON_COOK = "johnson_cook"


class MeanStressCorrectionType(str, Enum):
    NONE = "none"
    GOODMAN = "goodman"
    GERBER = "gerber"
    SODERBERG = "soderberg"


class PostWeldTreatment(str, Enum):
    NONE = "none"
    HFMI = "hfmi"
    TIG_DRESSING = "tig_dressing"
    BURR_GRINDING = "burr_grinding"
    HAMMER_PEENING = "hammer_peening"
    SHOT_PEENING = "shot_peening"


class Environment(str, Enum):
    AIR = "air"
    SEAWATER_FREE_CORROSION = "seawater_free"
    SEAWATER_CATHODIC_PROTECTION = "seawater_cp"
    INDUSTRIAL_ATMOSPHERE = "industrial"
    HYDROGEN = "hydrogen"


class ConsequenceClass(str, Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"


class FatigueStandard(str, Enum):
    IIW = "iiw"
    EUROCODE3 = "eurocode3"
    EUROCODE9 = "eurocode9"
    BS7608 = "bs7608"
    DNV = "dnv"


class QualityLevel(str, Enum):
    B = "B"
    C = "C"
    D = "D"


class ImperfectionType(str, Enum):
    UNDERCUT = "undercut"
    POROSITY = "porosity"
    LACK_OF_FUSION = "lack_of_fusion"
    MISALIGNMENT_AXIAL = "misalignment_axial"
    MISALIGNMENT_ANGULAR = "misalignment_angular"
    INCOMPLETE_PENETRATION = "incomplete_penetration"
    EXCESS_WELD_METAL = "excess_weld_metal"


class WeldProcess(str, Enum):
    MIG_MAG = "mig_mag"
    TIG = "tig"
    LASER = "laser"
    RESISTANCE_SPOT = "resistance_spot"
    FRICTION_STIR = "friction_stir"
    LASER_HYBRID = "laser_hybrid"


class MultiaxialMethod(str, Enum):
    GOUGH_POLLARD = "gough_pollard"
    FINDLEY = "findley"
    MWCM = "mwcm"


class LoadingProportionality(str, Enum):
    PROPORTIONAL = "proportional"
    NON_PROPORTIONAL = "non_proportional"
    AUTO_DETECT = "auto_detect"
