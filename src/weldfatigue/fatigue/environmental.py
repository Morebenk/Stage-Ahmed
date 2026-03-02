"""Environmental and corrosion reduction factors for fatigue assessment."""

import math


class EnvironmentalFactors:
    """
    Environmental factors affecting fatigue life of welded joints.

    Covers:
    - Corrosion fatigue (seawater, industrial atmosphere)
    - Temperature effects on S-N curves
    - Hydrogen embrittlement knockdown for H2 tank applications

    References:
    - IIW XIII-1823-07 Section 3.7
    - BS 7608:2014 Section 16
    - ASME Article KD-10
    """

    # Corrosion reduction factors on FAT class
    CORROSION_FACTORS = {
        ("air", "steel"): 1.0,
        ("air", "aluminum"): 1.0,
        ("seawater_free", "steel"): 0.7,  # Free corrosion
        ("seawater_free", "aluminum"): 0.6,
        ("seawater_cp", "steel"): 0.85,  # With cathodic protection
        ("seawater_cp", "aluminum"): 0.8,
        ("industrial", "steel"): 0.9,
        ("industrial", "aluminum"): 0.85,
        ("hydrogen", "steel"): 0.5,  # Hydrogen embrittlement
        ("hydrogen", "aluminum"): 0.9,  # Aluminum less susceptible
    }

    # Whether endurance limit is removed in this environment
    REMOVES_ENDURANCE_LIMIT = {
        "air": False,
        "seawater_free": True,  # No endurance limit in corrosion
        "seawater_cp": True,
        "industrial": False,
        "hydrogen": False,
    }

    @staticmethod
    def corrosion_factor(environment: str, material_type: str = "steel") -> float:
        """
        Get FAT class reduction factor for corrosive environment.

        FAT_env = FAT * corrosion_factor
        """
        return EnvironmentalFactors.CORROSION_FACTORS.get(
            (environment, material_type), 1.0
        )

    @staticmethod
    def removes_endurance_limit(environment: str) -> bool:
        """
        Whether environment removes the endurance limit (constant amplitude).

        In corrosive environments (seawater), there is no fatigue limit:
        the S-N curve continues with slope m1 throughout.
        """
        return EnvironmentalFactors.REMOVES_ENDURANCE_LIMIT.get(environment, False)

    @staticmethod
    def temperature_factor(temperature_celsius: float, material_type: str = "steel") -> float:
        """
        IIW temperature correction factor on FAT class.

        Steel:
            f(T) = 1.0                          for T <= 100°C
            f(T) = 1.0 - 1.5e-3 * (T - 100)    for 100 < T <= 300°C
            Not valid above 300°C (creep regime)

        Aluminum:
            f(T) = 1.0                          for T <= 50°C
            f(T) = 1.0 - 3.0e-3 * (T - 50)     for 50 < T <= 150°C
            Not valid above 150°C
        """
        if material_type == "steel":
            if temperature_celsius <= 100.0:
                return 1.0
            elif temperature_celsius <= 300.0:
                return 1.0 - 1.5e-3 * (temperature_celsius - 100.0)
            else:
                return max(0.3, 1.0 - 1.5e-3 * (temperature_celsius - 100.0))
        elif material_type == "aluminum":
            if temperature_celsius <= 50.0:
                return 1.0
            elif temperature_celsius <= 150.0:
                return 1.0 - 3.0e-3 * (temperature_celsius - 50.0)
            else:
                return max(0.3, 1.0 - 3.0e-3 * (temperature_celsius - 50.0))
        return 1.0

    @staticmethod
    def hydrogen_knockdown(
        hydrogen_pressure_bar: float, material_type: str = "steel"
    ) -> float:
        """
        Hydrogen embrittlement reduction factor on fatigue strength.

        Based on ASME Article KD-10 and NASA-STD-6016 data.
        Applicable primarily to steel in gaseous hydrogen.

        Factor decreases with increasing hydrogen pressure:
            f(p) = 1.0 / (1 + 0.002 * p)  for steel

        Aluminum is largely unaffected by hydrogen embrittlement.
        """
        if material_type != "steel":
            return 1.0  # Aluminum largely unaffected

        if hydrogen_pressure_bar <= 0:
            return 1.0

        # Empirical knockdown based on ASME KD-10 guidance
        return 1.0 / (1.0 + 0.002 * hydrogen_pressure_bar)

    @staticmethod
    def cryogenic_factor(temperature_celsius: float, material_type: str = "steel") -> float:
        """
        Cryogenic temperature factor.

        At very low temperatures, steels may become brittle (ductile-to-brittle
        transition), while austenitic stainless steels and aluminum maintain ductility.
        """
        if material_type == "aluminum":
            # Aluminum alloys generally maintain fatigue properties at low temperatures
            return 1.0

        # For structural steels: concern below ductile-to-brittle transition
        if temperature_celsius < -40.0:
            return 0.8  # Conservative reduction for carbon steels
        return 1.0

    @staticmethod
    def combined_environmental_factor(
        environment: str = "air",
        temperature_celsius: float = 20.0,
        hydrogen_pressure_bar: float = 0.0,
        material_type: str = "steel",
    ) -> float:
        """
        Combined environmental reduction factor.

        Multiplies corrosion, temperature, hydrogen, and cryogenic factors.
        """
        f_corr = EnvironmentalFactors.corrosion_factor(environment, material_type)
        f_temp = EnvironmentalFactors.temperature_factor(temperature_celsius, material_type)
        f_h2 = EnvironmentalFactors.hydrogen_knockdown(hydrogen_pressure_bar, material_type)
        f_cryo = EnvironmentalFactors.cryogenic_factor(temperature_celsius, material_type)

        return f_corr * f_temp * f_h2 * f_cryo

    @staticmethod
    def corrected_fat_class(
        fat_class: int,
        environment: str = "air",
        temperature_celsius: float = 20.0,
        hydrogen_pressure_bar: float = 0.0,
        material_type: str = "steel",
    ) -> float:
        """Return FAT class adjusted for environmental effects."""
        f = EnvironmentalFactors.combined_environmental_factor(
            environment, temperature_celsius, hydrogen_pressure_bar, material_type
        )
        return fat_class * f
