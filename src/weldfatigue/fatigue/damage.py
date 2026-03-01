"""Palmgren-Miner linear cumulative damage rule."""

from weldfatigue.core.schemas import CumulativeDamageResult
from weldfatigue.fatigue.sn_curve import SNCurve


class PalmgrenMiner:
    """
    Palmgren-Miner linear cumulative damage rule.

    D = sum(n_i / N_i) for each load block i

    Failure criterion: D >= D_limit
    (IIW recommends D_limit = 0.5 for safety-critical, 1.0 for normal)
    """

    def __init__(self, sn_curve: SNCurve, damage_limit: float = 1.0):
        self.sn_curve = sn_curve
        self.damage_limit = damage_limit

    def compute_damage(
        self, load_spectrum: list[tuple[float, int]]
    ) -> CumulativeDamageResult:
        """
        Compute cumulative damage for a variable-amplitude load spectrum.

        Args:
            load_spectrum: List of (stress_range [MPa], num_cycles) tuples.
        """
        damage_per_block = []
        for stress_range, n_cycles in load_spectrum:
            N_f = self.sn_curve.cycles_to_failure(stress_range)
            if N_f == float("inf"):
                damage_per_block.append(0.0)
            else:
                damage_per_block.append(n_cycles / N_f)

        total_damage = sum(damage_per_block)
        critical_idx = (
            damage_per_block.index(max(damage_per_block)) if damage_per_block else 0
        )

        return CumulativeDamageResult(
            total_damage=total_damage,
            damage_per_block=damage_per_block,
            critical_block_index=critical_idx,
            status="PASS" if total_damage < self.damage_limit else "FAIL",
        )

    def equivalent_stress_range(self, load_spectrum: list[tuple[float, int]]) -> float:
        """
        Compute the equivalent constant-amplitude stress range.
        delta_sigma_eq = [sum(n_i * delta_sigma_i^m) / sum(n_i)]^(1/m)
        """
        m = self.sn_curve.m1
        numerator = sum(n * (ds**m) for ds, n in load_spectrum)
        denominator = sum(n for _, n in load_spectrum)
        if denominator == 0:
            return 0.0
        return (numerator / denominator) ** (1.0 / m)
