"""Enumerations for the weldfatigue package."""

from enum import Enum


class WeldType(str, Enum):
    BUTT = "butt"
    FILLET = "fillet"
    CRUCIFORM = "cruciform"
    LAP = "lap"
    T_JOINT = "t_joint"
    STIFFENER = "stiffener"


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


class StrainRateModel(str, Enum):
    COWPER_SYMONDS = "cowper_symonds"
    JOHNSON_COOK = "johnson_cook"


class MeanStressCorrectionType(str, Enum):
    NONE = "none"
    GOODMAN = "goodman"
    GERBER = "gerber"
    SODERBERG = "soderberg"
