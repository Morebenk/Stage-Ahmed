"""Top-level fatigue assessment orchestrator."""

from typing import Optional

from weldfatigue.core.schemas import CumulativeDamageResult, FatigueResult
from weldfatigue.fatigue.damage import PalmgrenMiner
from weldfatigue.fatigue.fat_classes import FATClassCatalog
from weldfatigue.fatigue.hotspot_stress import HotSpotStressAssessment
from weldfatigue.fatigue.mean_stress import MeanStressCorrection
from weldfatigue.fatigue.nominal_stress import NominalStressAssessment
from weldfatigue.fatigue.notch_stress import EffectiveNotchStressAssessment
from weldfatigue.fatigue.sn_curve import SNCurve
from weldfatigue.materials.database import MaterialDatabase


class FatigueAssessment:
    """
    Top-level orchestrator for IIW fatigue assessment.

    Coordinates material lookup, FAT class selection, method dispatch,
    mean stress correction, cumulative damage, and result packaging.
    """

    def __init__(
        self,
        material_db: Optional[MaterialDatabase] = None,
        fat_catalog: Optional[FATClassCatalog] = None,
    ):
        self.material_db = material_db or MaterialDatabase()
        self.fat_catalog = fat_catalog or FATClassCatalog()

    def run(
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
        load_spectrum: Optional[list[tuple[float, int]]] = None,
    ) -> dict:
        """
        Run a complete fatigue assessment.

        Returns a dict with all intermediate and final results.
        """
        # 1. Material lookup
        material = self.material_db.get(material_name)

        # 2. FAT class selection
        if fat_class is None:
            recommended = self.fat_catalog.recommend(
                weld_type, load_type, material.family
            )
            if recommended:
                fat_class = recommended.fat_class
            else:
                raise ValueError(
                    f"No FAT class found for {weld_type}/{load_type}/{material.family}. "
                    "Please specify fat_class explicitly."
                )

        # 3. Method dispatch
        if method == "nominal":
            assessor = NominalStressAssessment(
                fat_class, material.family, variable_amplitude
            )
            result = assessor.evaluate(
                stress_range,
                num_cycles,
                mean_stress_correction=mean_stress_correction,
                mean_stress=mean_stress,
                ultimate_strength=material.ultimate_strength,
                yield_strength=material.yield_strength,
            )
        elif method == "hotspot":
            assessor = HotSpotStressAssessment(
                fat_class=fat_class,
                material=material.family,
                variable_amplitude=variable_amplitude,
            )
            result = assessor.evaluate(stress_range, num_cycles)
        elif method == "notch":
            assessor = EffectiveNotchStressAssessment(
                material=material.family,
                plate_thickness=plate_thickness,
                variable_amplitude=variable_amplitude,
            )
            result = assessor.evaluate(stress_range, num_cycles)
            # Notch method uses its own FAT class (225 steel / 71 aluminum)
            fat_class = assessor.fat_class
        else:
            raise ValueError(f"Unknown method: {method}")

        # 4. Variable amplitude (Miner) if spectrum provided
        miner_result = None
        if load_spectrum:
            va_curve = SNCurve(fat_class, material.family, variable_amplitude=True)
            miner = PalmgrenMiner(va_curve, damage_limit)
            miner_result = miner.compute_damage(load_spectrum)

        # 5. Package results
        output = {
            "material": {
                "name": material.name,
                "family": material.family,
                "yield_strength": material.yield_strength,
                "ultimate_strength": material.ultimate_strength,
            },
            "fat_class": fat_class,
            "method": method,
            "single_block_result": result.model_dump(),
        }
        if miner_result:
            output["miner_result"] = miner_result.model_dump()

        return output
