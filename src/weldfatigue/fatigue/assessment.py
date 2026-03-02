"""Top-level fatigue assessment orchestrator."""

from dataclasses import dataclass, field
from typing import Optional

from weldfatigue.fatigue.damage import PalmgrenMiner
from weldfatigue.fatigue.environmental import EnvironmentalFactors
from weldfatigue.fatigue.fat_classes import FATClassCatalog
from weldfatigue.fatigue.four_r_method import FourRMethod
from weldfatigue.fatigue.fracture_mechanics import FractureMechanicsAssessment
from weldfatigue.fatigue.hotspot_stress import HotSpotStressAssessment
from weldfatigue.fatigue.multiaxial import MultiaxialFatigueAssessment
from weldfatigue.fatigue.nominal_stress import NominalStressAssessment
from weldfatigue.fatigue.notch_stress import EffectiveNotchStressAssessment
from weldfatigue.fatigue.post_weld_treatment import PostWeldTreatmentFactors
from weldfatigue.fatigue.residual_stress import ResidualStressModel
from weldfatigue.fatigue.root_fatigue import RootFatigueAssessment
from weldfatigue.fatigue.safety_factors import PartialSafetyFactors
from weldfatigue.fatigue.sn_curve import SNCurve
from weldfatigue.fatigue.thickness_correction import ThicknessCorrection
from weldfatigue.fatigue.weld_quality import WeldQualityAssessment
from weldfatigue.materials.database import MaterialDatabase


@dataclass
class AssessmentConfig:
    """Configuration parameters for a fatigue assessment run."""

    # Core parameters
    method: str = "nominal"
    material_name: str = "S355"
    weld_type: str = "butt"
    load_type: str = "tension"
    stress_range: float = 100.0
    num_cycles: int = 2_000_000
    fat_class: Optional[int] = None
    mean_stress: float = 0.0
    mean_stress_correction: str = "none"
    damage_limit: float = 1.0
    plate_thickness: float = 10.0
    variable_amplitude: bool = False
    load_spectrum: Optional[list] = None
    # Modifier chain
    post_weld_treatment: str = "none"
    environment: str = "air"
    temperature_celsius: float = 20.0
    hydrogen_pressure_bar: float = 0.0
    consequence_class: str = "normal"
    inspection_level: str = "periodic"
    standard: str = "iiw"
    survival_probability: float = 0.977
    quality_level: Optional[str] = None
    axial_misalignment: float = 0.0
    angular_misalignment: float = 0.0
    residual_stress: Optional[float] = None
    pwht_temperature: float = 0.0
    pwht_hold_time: float = 0.0
    # Multiaxial
    shear_stress_range: float = 0.0
    fat_shear: Optional[int] = None
    multiaxial_method: str = "gough_pollard"
    # Root fatigue
    weld_throat: float = 0.0
    penetration_depth: float = 0.0
    # Fracture mechanics
    initial_crack_size: float = 0.0
    critical_crack_size: float = 0.0
    weld_geometry: str = "t_butt"
    # 4R method
    notch_stress_range: Optional[float] = None
    stress_ratio: float = 0.0


class FatigueAssessment:
    """
    Top-level orchestrator for IIW fatigue assessment.

    Coordinates material lookup, FAT class selection, method dispatch,
    modifier chain (thickness, treatment, safety, environment, quality),
    mean stress correction, residual stress, cumulative damage, and
    result packaging.
    """

    def __init__(
        self,
        material_db: Optional[MaterialDatabase] = None,
        fat_catalog: Optional[FATClassCatalog] = None,
    ):
        self.material_db = material_db or MaterialDatabase()
        self.fat_catalog = fat_catalog or FATClassCatalog()

    def run(self, config: AssessmentConfig) -> dict:
        """
        Run a complete fatigue assessment from a config object.

        Supports methods: nominal, hotspot, notch, multiaxial, root,
        fracture_mechanics, four_r.

        Returns a dict with all intermediate and final results.
        """
        material = self.material_db.get(config.material_name)

        # Dispatch independent methods first
        if config.method == "four_r":
            return self._run_four_r(config, material)
        if config.method == "fracture_mechanics":
            return self._run_fracture_mechanics(config, material)
        if config.method == "multiaxial":
            return self._run_multiaxial(config, material)

        # Resolve FAT class
        fat_class = self._resolve_fat_class(config, material)
        original_fat = fat_class

        # Apply modifier chain
        fat_class, effective_stress, effective_mean, modifiers, va = (
            self._apply_modifiers(config, fat_class, material)
        )

        # Root method has its own dispatch path
        if config.method == "root":
            return self._run_root(
                config, material, effective_stress, fat_class,
                original_fat, modifiers, va,
            )

        # Standard method dispatch (nominal / hotspot / notch)
        result, fat_class = self._dispatch_standard(
            config, fat_class, material, effective_stress,
            effective_mean, va,
        )

        # Variable amplitude (Miner) if spectrum provided
        miner_result = None
        if config.load_spectrum:
            va_curve = SNCurve(fat_class, material.family, variable_amplitude=True)
            miner = PalmgrenMiner(va_curve, config.damage_limit)
            miner_result = miner.compute_damage(config.load_spectrum)

        # Package results
        output = {
            "material": {
                "name": material.name,
                "family": material.family,
                "yield_strength": material.yield_strength,
                "ultimate_strength": material.ultimate_strength,
            },
            "fat_class_original": original_fat,
            "fat_class_effective": fat_class,
            "method": config.method,
            "single_block_result": result.model_dump(),
        }
        if modifiers:
            output["modifiers_applied"] = modifiers
        if miner_result:
            output["miner_result"] = miner_result.model_dump()

        return output

    def run_simple(
        self,
        method: str,
        material_name: str,
        weld_type: str,
        load_type: str,
        stress_range: float,
        num_cycles: int,
        fat_class: Optional[int] = None,
        mean_stress: float = 0.0,
        mean_stress_correction: str = "none",
        damage_limit: float = 1.0,
        plate_thickness: float = 10.0,
        variable_amplitude: bool = False,
        load_spectrum: Optional[list] = None,
    ) -> dict:
        """
        Backwards-compatible simple assessment (no enhancement modifiers).

        For enhanced assessments, use ``run(AssessmentConfig(...))``.
        """
        config = AssessmentConfig(
            method=method,
            material_name=material_name,
            weld_type=weld_type,
            load_type=load_type,
            stress_range=stress_range,
            num_cycles=num_cycles,
            fat_class=fat_class,
            mean_stress=mean_stress,
            mean_stress_correction=mean_stress_correction,
            damage_limit=damage_limit,
            plate_thickness=plate_thickness,
            variable_amplitude=variable_amplitude,
            load_spectrum=load_spectrum,
        )
        return self.run(config)

    # --- Private helpers ---

    def _resolve_fat_class(self, config: AssessmentConfig, material) -> int:
        """Resolve FAT class from config or catalog."""
        if config.fat_class is not None:
            return config.fat_class

        recommended = self.fat_catalog.recommend(
            config.weld_type, config.load_type, material.family
        )
        if recommended:
            return recommended.fat_class

        raise ValueError(
            f"No FAT class found for "
            f"{config.weld_type}/{config.load_type}/{material.family}. "
            "Please specify fat_class explicitly."
        )

    def _apply_modifiers(
        self, config: AssessmentConfig, fat_class: int, material,
    ) -> tuple[int, float, float, dict, bool]:
        """
        Apply the modifier chain to FAT class and stress.

        Returns (fat_class, effective_stress, effective_mean,
                 modifiers_dict, variable_amplitude).
        """
        modifiers: dict = {}
        va = config.variable_amplitude

        # Thickness correction
        fat_class = self._apply_thickness(
            fat_class, config, modifiers,
        )

        # Post-weld treatment
        fat_class = self._apply_treatment(
            fat_class, config, material, modifiers,
        )

        # Environmental reduction
        fat_class, va = self._apply_environment(
            fat_class, config, material, modifiers, va,
        )

        # Partial safety factors
        fat_class = self._apply_safety(fat_class, config, modifiers)

        # Misalignment stress magnification
        effective_stress = self._apply_misalignment(
            config, modifiers,
        )

        # Residual stress
        effective_stress, effective_mean = self._apply_residual(
            config, material, effective_stress, modifiers,
        )

        # Quality level FAT mapping
        fat_class = self._apply_quality_level(
            fat_class, config, modifiers,
        )

        return fat_class, effective_stress, effective_mean, modifiers, va

    @staticmethod
    def _apply_thickness(
        fat_class: int, config: AssessmentConfig, modifiers: dict,
    ) -> int:
        factor = ThicknessCorrection.correction_factor(
            config.plate_thickness, config.weld_type, config.load_type,
        )
        fat_class = int(round(fat_class * factor))
        if factor < 1.0:
            modifiers["thickness"] = {"factor": factor, "fat_after": fat_class}
        return fat_class

    @staticmethod
    def _apply_treatment(
        fat_class: int, config: AssessmentConfig, material, modifiers: dict,
    ) -> int:
        if config.post_weld_treatment == "none":
            return fat_class
        fat_class = PostWeldTreatmentFactors.apply_treatment(
            fat_class, config.post_weld_treatment, material.yield_strength,
        )
        modifiers["post_weld_treatment"] = {
            "treatment": config.post_weld_treatment,
            "fat_after": fat_class,
        }
        return fat_class

    @staticmethod
    def _apply_environment(
        fat_class: int, config: AssessmentConfig, material,
        modifiers: dict, va: bool,
    ) -> tuple[int, bool]:
        env_factor = EnvironmentalFactors.combined_environmental_factor(
            config.environment, config.temperature_celsius,
            config.hydrogen_pressure_bar, material.family,
        )
        if env_factor < 1.0:
            fat_class = int(round(fat_class * env_factor))
            modifiers["environment"] = {
                "factor": env_factor,
                "fat_after": fat_class,
                "removes_endurance_limit": EnvironmentalFactors.removes_endurance_limit(
                    config.environment,
                ),
            }
        if config.environment in ("seawater_free", "seawater_cp"):
            va = True
        return fat_class, va

    @staticmethod
    def _apply_safety(
        fat_class: int, config: AssessmentConfig, modifiers: dict,
    ) -> int:
        gamma = PartialSafetyFactors.gamma_Mf(
            config.consequence_class, config.inspection_level, config.standard,
        )
        sp = PartialSafetyFactors.survival_probability_factor(
            config.survival_probability,
        )
        if gamma > 1.0 or sp < 1.0:
            fat_class = int(round(fat_class * sp / gamma))
            modifiers["safety_factors"] = {
                "gamma_Mf": gamma,
                "sp_factor": sp,
                "fat_after": fat_class,
            }
        return fat_class

    @staticmethod
    def _apply_misalignment(
        config: AssessmentConfig, modifiers: dict,
    ) -> float:
        if config.axial_misalignment <= 0 and config.angular_misalignment <= 0:
            return config.stress_range

        km_ax = WeldQualityAssessment.axial_misalignment_km(
            config.axial_misalignment, config.plate_thickness,
        )
        km_ang = WeldQualityAssessment.angular_misalignment_km(
            config.angular_misalignment, config.plate_thickness, 100.0,
        )
        km_combined = WeldQualityAssessment.combined_km(km_ax, km_ang)
        effective_stress = config.stress_range * km_combined
        modifiers["misalignment"] = {
            "km_axial": km_ax,
            "km_angular": km_ang,
            "km_combined": km_combined,
            "effective_stress": effective_stress,
        }
        return effective_stress

    @staticmethod
    def _apply_residual(
        config: AssessmentConfig, material,
        effective_stress: float, modifiers: dict,
    ) -> tuple[float, float]:
        if config.residual_stress is None:
            return effective_stress, config.mean_stress

        actual_residual = config.residual_stress
        if config.pwht_temperature > 200 and config.pwht_hold_time > 0:
            relief = ResidualStressModel.pwht_relief_factor(
                config.pwht_temperature, config.pwht_hold_time,
            )
            actual_residual *= relief
            modifiers["pwht"] = {
                "relief_factor": relief,
                "residual_after": actual_residual,
            }

        actual_residual = ResidualStressModel.relaxation_under_cycling(
            actual_residual, effective_stress,
            material.yield_strength, config.num_cycles,
        )

        effective_stress, effective_mean = (
            ResidualStressModel.superpose_on_applied(
                effective_stress, config.mean_stress, actual_residual,
            )
        )
        modifiers["residual_stress"] = {
            "residual_applied": actual_residual,
            "effective_mean": effective_mean,
        }
        return effective_stress, effective_mean

    @staticmethod
    def _apply_quality_level(
        fat_class: int, config: AssessmentConfig, modifiers: dict,
    ) -> int:
        if config.quality_level is None:
            return fat_class

        quality_fat = WeldQualityAssessment.quality_level_fat(
            config.quality_level, config.weld_type,
        )
        fat_class = min(fat_class, quality_fat)
        modifiers["quality_level"] = {
            "level": config.quality_level,
            "quality_fat": quality_fat,
            "fat_after": fat_class,
        }
        return fat_class

    @staticmethod
    def _dispatch_standard(
        config: AssessmentConfig, fat_class: int, material,
        effective_stress: float, effective_mean: float, va: bool,
    ) -> tuple:
        """Dispatch to nominal / hotspot / notch assessor."""
        if config.method == "nominal":
            assessor = NominalStressAssessment(
                fat_class, material.family, va,
            )
            result = assessor.evaluate(
                effective_stress, config.num_cycles,
                mean_stress_correction=config.mean_stress_correction,
                mean_stress=effective_mean,
                ultimate_strength=material.ultimate_strength,
                yield_strength=material.yield_strength,
            )
        elif config.method == "hotspot":
            assessor = HotSpotStressAssessment(
                fat_class=fat_class, material=material.family,
                variable_amplitude=va,
            )
            result = assessor.evaluate(effective_stress, config.num_cycles)
        elif config.method == "notch":
            assessor = EffectiveNotchStressAssessment(
                material=material.family,
                plate_thickness=config.plate_thickness,
                variable_amplitude=va,
            )
            result = assessor.evaluate(effective_stress, config.num_cycles)
            fat_class = assessor.fat_class
        else:
            raise ValueError(f"Unknown method: {config.method}")
        return result, fat_class

    # --- Specialized method dispatchers ---

    def _run_multiaxial(self, config: AssessmentConfig, material) -> dict:
        result = MultiaxialFatigueAssessment.evaluate(
            method=config.multiaxial_method,
            delta_sigma=config.stress_range,
            delta_tau=config.shear_stress_range,
            fat_sigma=config.fat_class or 80,
            fat_tau=config.fat_shear or 0,
            num_cycles=config.num_cycles,
            material_type=material.family,
        )
        return {
            "material": {"name": material.name, "family": material.family},
            "method": "multiaxial",
            "multiaxial_method": config.multiaxial_method,
            "result": result,
        }

    def _run_root(
        self, config: AssessmentConfig, material,
        effective_stress: float, fat_class: int, original_fat: int,
        modifiers: dict, va: bool,
    ) -> dict:
        if config.weld_throat > 0 and config.plate_thickness > 0:
            root_stress = RootFatigueAssessment.root_notch_stress(
                effective_stress, config.weld_throat, config.plate_thickness,
                config.penetration_depth, config.load_type,
            )
        else:
            root_stress = effective_stress

        assessor = RootFatigueAssessment(material=material.family, variable_amplitude=va)
        result = assessor.evaluate(root_stress, config.num_cycles)

        output = {
            "material": {"name": material.name, "family": material.family},
            "method": "root",
            "fat_class_original": original_fat,
            "fat_class_effective": fat_class,
            "root_fat_class": assessor.fat_class,
            "root_stress_range": root_stress,
            "result": result.model_dump(),
        }
        if modifiers:
            output["modifiers_applied"] = modifiers
        return output

    def _run_fracture_mechanics(self, config: AssessmentConfig, material) -> dict:
        fm = FractureMechanicsAssessment()
        paris = FractureMechanicsAssessment.get_paris_parameters(
            material.family, config.environment,
        )
        threshold_sif = FractureMechanicsAssessment.DELTA_K_TH.get(
            material.family, 63.0,
        )
        result = fm.integrate_crack_growth(
            initial_crack=config.initial_crack_size,
            critical_crack=config.critical_crack_size,
            stress_range=config.stress_range,
            plate_thickness=config.plate_thickness,
            weld_geometry=config.weld_geometry,
            C=paris["C"], m=paris["m"],
            delta_K_th=threshold_sif,
        )
        return {
            "material": {"name": material.name, "family": material.family},
            "method": "fracture_mechanics",
            "paris_parameters": paris,
            "delta_K_threshold": threshold_sif,
            "result": result,
        }

    def _run_four_r(self, config: AssessmentConfig, material) -> dict:
        result = FourRMethod.evaluate(
            notch_stress_range=config.notch_stress_range or config.stress_range,
            stress_ratio=config.stress_ratio,
            residual_stress=config.residual_stress or 0.0,
            ultimate_strength=material.ultimate_strength,
            yield_strength=material.yield_strength,
            num_cycles=config.num_cycles,
            material_type=material.family,
        )
        return {
            "material": {
                "name": material.name,
                "family": material.family,
                "yield_strength": material.yield_strength,
                "ultimate_strength": material.ultimate_strength,
            },
            "method": "four_r",
            "result": result.model_dump(),
        }
