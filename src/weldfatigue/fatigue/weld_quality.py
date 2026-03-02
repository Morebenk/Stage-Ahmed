"""ISO 5817 weld quality assessment and misalignment stress magnification."""

import json
import math
from pathlib import Path


class WeldQualityAssessment:
    """
    ISO 5817:2023 weld quality assessment.

    Evaluates weld imperfections against quality levels (B, C, D)
    and computes misalignment stress magnification factors (km).

    References:
    - ISO 5817:2023 (Quality levels for imperfections)
    - IIW XIII-1823-07 Annex D (Misalignment)
    """

    # ISO 5817 Annex B: Quality level to FAT class mapping
    QUALITY_FAT_MAPPING = {
        "B": {"butt": 112, "fillet": 90, "cruciform": 80, "t_joint": 80, "lap": 71},
        "C": {"butt": 90, "fillet": 71, "cruciform": 63, "t_joint": 63, "lap": 56},
        "D": {"butt": 71, "fillet": 56, "cruciform": 50, "t_joint": 50, "lap": 45},
    }

    # ISO 5817 imperfection limits {quality_level: {type: {param: value}}}
    IMPERFECTION_LIMITS = {
        "B": {
            "undercut": {"max_depth_fraction": 0.05, "max_depth_mm": 0.5},
            "porosity": {"max_area_fraction": 0.01},
            "misalignment_axial": {"max_fraction": 0.10},
            "incomplete_penetration": {"max_depth_mm": 0.0},  # Not permitted
            "excess_weld_metal": {"max_height_fraction": 0.10},
        },
        "C": {
            "undercut": {"max_depth_fraction": 0.10, "max_depth_mm": 1.0},
            "porosity": {"max_area_fraction": 0.02},
            "misalignment_axial": {"max_fraction": 0.15},
            "incomplete_penetration": {"max_depth_mm": 0.0},  # Not permitted
            "excess_weld_metal": {"max_height_fraction": 0.15},
        },
        "D": {
            "undercut": {"max_depth_fraction": 0.20, "max_depth_mm": 2.0},
            "porosity": {"max_area_fraction": 0.05},
            "misalignment_axial": {"max_fraction": 0.25},
            "incomplete_penetration": {"max_depth_mm": 1.5},
            "excess_weld_metal": {"max_height_fraction": 0.25},
        },
    }

    @staticmethod
    def axial_misalignment_km(eccentricity: float, thickness: float) -> float:
        """
        Stress magnification factor for axial misalignment.

        km = 1 + (e / t)

        where e = axial offset, t = plate thickness.
        """
        if thickness <= 0:
            raise ValueError("Thickness must be positive")
        if eccentricity < 0:
            raise ValueError("Eccentricity must be non-negative")
        return 1.0 + eccentricity / thickness

    @staticmethod
    def angular_misalignment_km(
        eccentricity: float,
        thickness: float,
        length: float,
        restraint: str = "fixed",
    ) -> float:
        """
        Stress magnification factor for angular misalignment.

        km = 1 + 3 * (e/t) * tanh(lambda*L/2) / (lambda*L/2)

        where lambda = sqrt(sigma_m * t / (D * E_mod)) is a buckling parameter.
        For simplified assessment without axial load:
            km = 1 + 3 * (e/t) for pinned ends
            km = 1 + 1.5 * (e/t) for fixed ends
        """
        if thickness <= 0:
            raise ValueError("Thickness must be positive")
        if eccentricity < 0:
            raise ValueError("Eccentricity must be non-negative")

        if eccentricity == 0:
            return 1.0

        ratio = eccentricity / thickness

        if restraint == "fixed":
            return 1.0 + 1.5 * ratio
        else:  # pinned
            return 1.0 + 3.0 * ratio

    @staticmethod
    def combined_km(km_axial: float, km_angular: float) -> float:
        """
        Combined misalignment factor.

        km = km_axial * km_angular

        Conservative multiplication of individual factors.
        """
        return km_axial * km_angular

    @staticmethod
    def quality_level_fat(quality_level: str, weld_type: str) -> int:
        """
        Get FAT class corresponding to ISO 5817 quality level.

        Based on ISO 5817:2023 Annex B mapping.
        """
        level_map = WeldQualityAssessment.QUALITY_FAT_MAPPING.get(quality_level)
        if level_map is None:
            raise ValueError(f"Unknown quality level: {quality_level}. Use B, C, or D.")

        fat = level_map.get(weld_type)
        if fat is None:
            # Default to most conservative for unknown weld type
            fat = min(level_map.values())
        return fat

    @staticmethod
    def check_imperfection(
        imperfection_type: str,
        measured_value: float,
        quality_level: str,
        thickness: float,
    ) -> dict:
        """
        Check if an imperfection is within ISO 5817 limits.

        Returns:
            dict with keys: acceptable, limit, measured, margin
        """
        limits = WeldQualityAssessment.IMPERFECTION_LIMITS.get(quality_level)
        if limits is None:
            raise ValueError(f"Unknown quality level: {quality_level}")

        imp_limits = limits.get(imperfection_type)
        if imp_limits is None:
            return {"acceptable": True, "limit": None, "measured": measured_value, "margin": None}

        # Determine the applicable limit
        if "max_depth_fraction" in imp_limits:
            limit = min(
                imp_limits["max_depth_fraction"] * thickness,
                imp_limits.get("max_depth_mm", float("inf")),
            )
        elif "max_depth_mm" in imp_limits:
            limit = imp_limits["max_depth_mm"]
        elif "max_fraction" in imp_limits:
            limit = imp_limits["max_fraction"] * thickness
        elif "max_area_fraction" in imp_limits:
            limit = imp_limits["max_area_fraction"] * thickness * thickness
        elif "max_height_fraction" in imp_limits:
            limit = imp_limits["max_height_fraction"] * thickness
        else:
            return {"acceptable": True, "limit": None, "measured": measured_value, "margin": None}

        acceptable = measured_value <= limit
        margin = (limit - measured_value) / limit if limit > 0 else 0.0

        return {
            "acceptable": acceptable,
            "limit": limit,
            "measured": measured_value,
            "margin": margin,
        }

    @staticmethod
    def assess_quality(
        weld_type: str,
        quality_level: str,
        axial_misalignment: float = 0.0,
        angular_misalignment: float = 0.0,
        thickness: float = 10.0,
        length: float = 100.0,
        restraint: str = "fixed",
    ) -> dict:
        """
        Complete quality assessment: km factors and FAT class.

        Returns:
            dict with km_axial, km_angular, km_combined, fat_class
        """
        km_ax = WeldQualityAssessment.axial_misalignment_km(axial_misalignment, thickness)
        km_ang = WeldQualityAssessment.angular_misalignment_km(
            angular_misalignment, thickness, length, restraint
        )
        km = WeldQualityAssessment.combined_km(km_ax, km_ang)
        fat = WeldQualityAssessment.quality_level_fat(quality_level, weld_type)

        return {
            "km_axial": km_ax,
            "km_angular": km_ang,
            "km_combined": km,
            "fat_class": fat,
            "quality_level": quality_level,
        }
