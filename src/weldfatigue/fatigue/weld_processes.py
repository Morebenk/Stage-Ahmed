"""Weld process-specific fatigue assessment methods."""

import math


class WeldProcessFatigue:
    """
    Process-specific fatigue modifications for different weld types.

    Covers laser welds, resistance spot welds, and friction stir welds.
    """

    # Laser weld FAT classes (typically 1-2 classes above arc welds)
    LASER_FAT_CLASSES = {
        ("butt", "steel"): 100,
        ("butt", "aluminum"): 50,
        ("fillet", "steel"): 90,
        ("fillet", "aluminum"): 45,
        ("lap", "steel"): 80,
        ("lap", "aluminum"): 40,
    }

    # FSW FAT classes (superior to arc welds)
    FSW_FAT_CLASSES = {
        ("butt", "steel"): 112,
        ("butt", "aluminum"): 56,
        ("lap", "steel"): 90,
        ("lap", "aluminum"): 45,
    }

    # Spot weld F-N curve parameters: N = C * F_range^(-m)
    # F in N, N in cycles
    SPOT_WELD_FN_PARAMS = {
        "steel": {"C": 4.876e17, "m": 3.64},
        "aluminum": {"C": 2.134e15, "m": 3.20},
    }

    # Process modification factors on base FAT class (arc weld FAT)
    PROCESS_FACTORS = {
        "mig_mag": 1.0,   # Reference (no modification)
        "tig": 1.1,       # +10% due to better toe geometry
        "laser": 1.2,     # +20% due to narrow HAZ
        "friction_stir": 1.3,  # +30% due to solid-state, no melting
        "laser_hybrid": 1.15,
        "resistance_spot": 1.0,  # Uses force-based approach instead
    }

    @staticmethod
    def laser_weld_fat_class(joint_type: str, material: str) -> int:
        """
        Get FAT class for laser welded joints.

        Laser welds typically achieve 1-2 FAT class steps above
        conventional arc welds due to:
        - Narrow, symmetrical weld profile
        - Smaller HAZ
        - Lower residual stresses
        """
        return WeldProcessFatigue.LASER_FAT_CLASSES.get(
            (joint_type, material), 80
        )

    @staticmethod
    def fsw_fat_class(joint_type: str, material: str) -> int:
        """
        Get FAT class for friction stir welded joints.

        FSW produces superior fatigue properties due to:
        - Solid-state process (no melting defects)
        - Fine, equiaxed grain structure
        - Lower residual stresses
        """
        return WeldProcessFatigue.FSW_FAT_CLASSES.get(
            (joint_type, material), 90
        )

    @staticmethod
    def spot_weld_fatigue_life(
        force_range: float,
        sheet_thickness: float,
        nugget_diameter: float,
        material: str = "steel",
    ) -> float:
        """
        Force-based fatigue life for resistance spot welds.

        Uses F-N curve approach: N = C * F_range^(-m)

        Force is normalized by sheet thickness and nugget diameter:
            F_norm = F_range / (t * d)

        Args:
            force_range: Applied force range [N]
            sheet_thickness: Sheet thickness [mm]
            nugget_diameter: Weld nugget diameter [mm]
            material: steel or aluminum

        Returns:
            Number of cycles to failure
        """
        if force_range <= 0:
            return float("inf")

        params = WeldProcessFatigue.SPOT_WELD_FN_PARAMS.get(material)
        if params is None:
            raise ValueError(f"No spot weld data for material: {material}")

        # Normalize force by geometry
        f_norm = force_range / (sheet_thickness * nugget_diameter)

        N = params["C"] * f_norm ** (-params["m"])
        return N

    @staticmethod
    def spot_weld_structural_stress(
        force: float,
        moment: float,
        sheet_thickness: float,
        nugget_diameter: float,
    ) -> float:
        """
        Structural stress at spot weld edge per Rupp/Storzel/Grubisic method.

        sigma_struct = F / (pi * d * t) + 6 * M / (pi * d * t^2)

        Args:
            force: Applied force [N]
            moment: Applied moment [N*mm]
            sheet_thickness: Sheet thickness [mm]
            nugget_diameter: Weld nugget diameter [mm]

        Returns:
            Structural stress [MPa]
        """
        d = nugget_diameter
        t = sheet_thickness

        sigma_f = force / (math.pi * d * t)
        sigma_m = 6.0 * moment / (math.pi * d * t ** 2)

        return abs(sigma_f) + abs(sigma_m)

    @staticmethod
    def process_modification_factor(process: str) -> float:
        """
        Get FAT class modification factor for weld process.

        Factor is multiplied with the base (arc weld) FAT class.
        """
        return WeldProcessFatigue.PROCESS_FACTORS.get(process, 1.0)

    @staticmethod
    def corrected_fat_for_process(base_fat: int, process: str) -> float:
        """
        Return FAT class adjusted for weld process.

        FAT_process = FAT_arc * process_factor
        """
        factor = WeldProcessFatigue.process_modification_factor(process)
        return base_fat * factor

    @staticmethod
    def minimum_nugget_diameter(sheet_thickness: float) -> float:
        """
        Minimum spot weld nugget diameter per AWS D8.9M.

        d_min = 4 * sqrt(t)  for t in mm
        """
        if sheet_thickness <= 0:
            raise ValueError("Sheet thickness must be positive")
        return 4.0 * math.sqrt(sheet_thickness)
