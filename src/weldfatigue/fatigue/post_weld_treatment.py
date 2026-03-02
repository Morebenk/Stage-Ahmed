"""Post-weld treatment improvement factors for fatigue assessment."""


class PostWeldTreatmentFactors:
    """
    Fatigue strength improvement factors for post-weld treatments.

    Implements IIW 2024 HFMI guidelines and standard improvement
    factors for TIG dressing, burr grinding, and peening methods.

    References:
    - IIW-2259-15 (3rd ed. 2024), Chapter on HFMI
    - IIW XIII-2453-12 (HFMI recommendation)
    """

    # Standard FAT class sequence (IIW)
    FAT_SEQUENCE = [36, 40, 45, 50, 56, 63, 71, 80, 90, 100, 112, 125, 140, 160]

    # HFMI upgrade steps by yield strength range [MPa]
    # (min_fy, max_fy) -> number of FAT class steps upgrade
    HFMI_UPGRADES = {
        (235, 355): 4,
        (355, 550): 6,
        (550, 750): 8,
        (750, 1300): 8,  # Capped at 8 per IIW 2024
    }

    # Fixed upgrade steps for other treatments
    TIG_DRESSING_STEPS = 2
    BURR_GRINDING_STEPS = 1
    SHOT_PEENING_STEPS = 2

    # Hammer peening by yield strength range
    HAMMER_PEENING_UPGRADES = {
        (235, 355): 2,
        (355, 550): 3,
        (550, 1300): 3,
    }

    @staticmethod
    def _upgrade_fat(base_fat: int, steps: int) -> int:
        """
        Upgrade FAT class by the given number of steps.

        Moves up through FAT_SEQUENCE. Caps at FAT 160.
        """
        seq = PostWeldTreatmentFactors.FAT_SEQUENCE

        # Find position in sequence
        if base_fat in seq:
            idx = seq.index(base_fat)
        else:
            # Find closest lower FAT class
            idx = 0
            for i, f in enumerate(seq):
                if f <= base_fat:
                    idx = i

        new_idx = min(idx + steps, len(seq) - 1)
        return seq[new_idx]

    @staticmethod
    def _get_steps_for_yield(table: dict, yield_strength: float) -> int:
        """Look up upgrade steps from a yield-strength-keyed table."""
        for (fy_min, fy_max), steps in table.items():
            if fy_min <= yield_strength < fy_max:
                return steps
        # Below minimum range: use lowest entry
        if yield_strength < min(k[0] for k in table):
            return min(table.values())
        # Above maximum range: use highest entry
        return max(table.values())

    @staticmethod
    def hfmi_upgraded_fat(base_fat: int, yield_strength: float) -> int:
        """
        Compute HFMI-treated FAT class per IIW 2024 guidelines.

        Higher yield strength steels benefit more from HFMI treatment.

        Args:
            base_fat: As-welded FAT class
            yield_strength: Material yield strength [MPa]

        Returns:
            Upgraded FAT class (max FAT 160)
        """
        steps = PostWeldTreatmentFactors._get_steps_for_yield(
            PostWeldTreatmentFactors.HFMI_UPGRADES, yield_strength
        )
        return PostWeldTreatmentFactors._upgrade_fat(base_fat, steps)

    @staticmethod
    def tig_dressing_upgraded_fat(base_fat: int) -> int:
        """TIG dressing: +2 FAT class steps."""
        return PostWeldTreatmentFactors._upgrade_fat(
            base_fat, PostWeldTreatmentFactors.TIG_DRESSING_STEPS
        )

    @staticmethod
    def burr_grinding_upgraded_fat(base_fat: int) -> int:
        """Burr grinding: +1 FAT class step."""
        return PostWeldTreatmentFactors._upgrade_fat(
            base_fat, PostWeldTreatmentFactors.BURR_GRINDING_STEPS
        )

    @staticmethod
    def hammer_peening_upgraded_fat(base_fat: int, yield_strength: float) -> int:
        """Hammer peening: +2 to +3 FAT class steps depending on yield strength."""
        steps = PostWeldTreatmentFactors._get_steps_for_yield(
            PostWeldTreatmentFactors.HAMMER_PEENING_UPGRADES, yield_strength
        )
        return PostWeldTreatmentFactors._upgrade_fat(base_fat, steps)

    @staticmethod
    def shot_peening_upgraded_fat(base_fat: int) -> int:
        """Shot peening: +2 FAT class steps."""
        return PostWeldTreatmentFactors._upgrade_fat(
            base_fat, PostWeldTreatmentFactors.SHOT_PEENING_STEPS
        )

    @staticmethod
    def apply_treatment(
        base_fat: int, treatment: str, yield_strength: float = 355.0
    ) -> int:
        """
        Apply post-weld treatment and return upgraded FAT class.

        Args:
            base_fat: As-welded FAT class
            treatment: Treatment type (none, hfmi, tig_dressing,
                       burr_grinding, hammer_peening, shot_peening)
            yield_strength: Material yield strength [MPa]
        """
        if treatment == "none":
            return base_fat
        elif treatment == "hfmi":
            return PostWeldTreatmentFactors.hfmi_upgraded_fat(base_fat, yield_strength)
        elif treatment == "tig_dressing":
            return PostWeldTreatmentFactors.tig_dressing_upgraded_fat(base_fat)
        elif treatment == "burr_grinding":
            return PostWeldTreatmentFactors.burr_grinding_upgraded_fat(base_fat)
        elif treatment == "hammer_peening":
            return PostWeldTreatmentFactors.hammer_peening_upgraded_fat(
                base_fat, yield_strength
            )
        elif treatment == "shot_peening":
            return PostWeldTreatmentFactors.shot_peening_upgraded_fat(base_fat)
        else:
            raise ValueError(f"Unknown treatment: {treatment}")

    @staticmethod
    def improvement_summary(base_fat: int, yield_strength: float = 355.0) -> dict:
        """
        Compare all treatment options for a given base FAT class.

        Returns dict mapping treatment name to upgraded FAT class.
        """
        treatments = ["none", "burr_grinding", "tig_dressing", "shot_peening",
                       "hammer_peening", "hfmi"]
        return {
            t: PostWeldTreatmentFactors.apply_treatment(base_fat, t, yield_strength)
            for t in treatments
        }
