"""Session state key constants for cross-page data flow."""

# Written by page 02 — Standard mode (Fatigue Analysis)
FATIGUE_RESULT = "fatigue_result"
FATIGUE_LAST_MEAN_STRESS = "fatigue_last_mean_stress"

# Written by page 02 — Multiaxial mode
MULTIAXIAL_RESULT = "multiaxial_result"

# Written by page 02 — Fracture Mechanics mode
FM_RESULT = "fm_result"

# Written by page 02 — Vibration Fatigue mode
VIB_FATIGUE_RESULT = "vib_fatigue_result"

# Written by page 02 — Weld Quality tab
WQ_RESULT = "wq_result"
WQ_IMPERFECTIONS = "wq_imperfections"

# Written by page 03 (Shock Analysis)
SHOCK_RESULT = "shock_result"
SHOCK_WELD_RESULT = "shock_weld_result"
SHOCK_ENERGY_RESULT = "shock_energy_result"

# Written by page 04 (FEA Post-Processing)
FEA_HOTSPOT_STRESS = "fea_hotspot_stress"
FEA_HOTSPOT_TYPE = "fea_hotspot_type"
FEA_MATERIAL_NAME = "fea_material_name"

# Rainflow spectrum (written by page 02 rainflow expander)
RAINFLOW_SPECTRUM = "rainflow_spectrum"
