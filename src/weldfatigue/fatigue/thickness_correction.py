"""IIW thickness correction factors for welded joints."""

import math


class ThicknessCorrection:
    """
    IIW thickness correction per XIII-1823-07 Section 3.5.

    For plate thickness > 25mm, the FAT class must be reduced:
        f(t) = (t_ref / t_eff)^n

    For thin sheets (t < 5mm), special reference radius rules apply.
    """

    REFERENCE_THICKNESS = 25.0  # mm

    # IIW thickness correction exponents per joint/load combination
    EXPONENTS = {
        ("butt", "tension"): 0.2,
        ("butt", "bending"): 0.2,
        ("cruciform", "tension"): 0.3,
        ("cruciform", "bending"): 0.3,
        ("t_joint", "tension"): 0.2,
        ("t_joint", "bending"): 0.2,
        ("fillet", "tension"): 0.1,
        ("fillet", "bending"): 0.1,
        ("fillet", "shear"): 0.0,
        ("lap", "tension"): 0.1,
        ("lap", "shear"): 0.0,
        ("stiffener", "tension"): 0.2,
        ("stiffener", "bending"): 0.2,
    }

    @staticmethod
    def correction_factor(t_eff: float, weld_type: str, load_type: str) -> float:
        """
        Compute thickness correction factor f(t).

        f(t) = (t_ref / t_eff)^n for t_eff > t_ref
        f(t) = 1.0 for t_eff <= t_ref

        The correction reduces the effective FAT class for thick plates.
        """
        if t_eff <= 0:
            raise ValueError("Effective thickness must be positive")

        if t_eff <= ThicknessCorrection.REFERENCE_THICKNESS:
            return 1.0

        key = (weld_type, load_type)
        n = ThicknessCorrection.EXPONENTS.get(key, 0.2)  # Default 0.2

        return (ThicknessCorrection.REFERENCE_THICKNESS / t_eff) ** n

    @staticmethod
    def thin_sheet_reference_radius(t_eff: float) -> float:
        """
        Determine reference radius for notch stress method.

        - t >= 5mm: r_ref = 1.0 mm (standard)
        - t < 5mm:  r_ref = 0.05 mm (micro-support concept)
        """
        if t_eff < 5.0:
            return 0.05
        return 1.0

    @staticmethod
    def effective_thickness(t_nominal: float, attachment_length: float = 0.0) -> float:
        """
        Calculate effective thickness per IIW recommendations.

        For transverse attachments, the effective thickness considers
        the influence of the attachment length on stress distribution.

        t_eff = min(t_nominal, 0.5 * L_attachment) if L > 0
        """
        if t_nominal <= 0:
            raise ValueError("Nominal thickness must be positive")
        if attachment_length <= 0:
            return t_nominal
        return min(t_nominal, 0.5 * attachment_length)

    @staticmethod
    def corrected_fat_class(fat_class: int, t_eff: float, weld_type: str, load_type: str) -> float:
        """
        Return the corrected FAT class considering thickness effect.

        FAT_corrected = FAT * f(t)
        """
        f = ThicknessCorrection.correction_factor(t_eff, weld_type, load_type)
        return fat_class * f
