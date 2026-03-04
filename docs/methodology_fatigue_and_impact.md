# Complete Engineering Methodology for Fatigue Strength and Impact Resistance Verification of Welded Mechanical Structures

**Document Reference:** WF-METH-001 Rev.0
**Applicable Standards:** IIW XIII-2259-15 (2024), EN 1993-1-8/1-9, EN 1999-1-3, BS 7608:2014, BS 7910:2019, ISO 5817:2023, DNV-RP-C203, ASME KD-10
**Scope:** All welded steel and aluminum mechanical structures under fatigue and/or impact loading

---

## TABLE OF CONTENTS

- [PART I — GENERAL FRAMEWORK](#part-i--general-framework)
  - [1. Scope and Objectives](#1-scope-and-objectives)
  - [2. Normative References](#2-normative-references)
  - [3. Terminology and Definitions](#3-terminology-and-definitions)
  - [4. Global Verification Workflow](#4-global-verification-workflow)
- [PART II — FATIGUE STRENGTH VERIFICATION](#part-ii--fatigue-strength-verification)
  - [5. Phase 1: Data Collection and Classification](#5-phase-1-data-collection-and-classification)
  - [6. Phase 2: Assessment Method Selection](#6-phase-2-assessment-method-selection)
  - [7. Phase 3: S-N Curve and Standard Selection](#7-phase-3-s-n-curve-and-standard-selection)
  - [8. Phase 4: Modifier Chain — Correction Factors](#8-phase-4-modifier-chain--correction-factors)
  - [9. Phase 5: Damage Calculation and Acceptance Criteria](#9-phase-5-damage-calculation-and-acceptance-criteria)
  - [10. Special Cases in Fatigue](#10-special-cases-in-fatigue)
- [PART III — IMPACT RESISTANCE VERIFICATION](#part-iii--impact-resistance-verification)
  - [11. Phase 1: Dynamic Material Characterization](#11-phase-1-dynamic-material-characterization)
  - [12. Phase 2: Weld Joint Failure Assessment Under Impact](#12-phase-2-weld-joint-failure-assessment-under-impact)
  - [13. Phase 3: Energy Absorption Assessment](#13-phase-3-energy-absorption-assessment)
- [PART IV — FEA INTEGRATION](#part-iv--fea-integration)
  - [14. FEA Data Extraction for Fatigue](#14-fea-data-extraction-for-fatigue)
  - [15. FEA Data Extraction for Impact](#15-fea-data-extraction-for-impact)
- [PART V — COMBINED ASSESSMENT AND REPORTING](#part-v--combined-assessment-and-reporting)
  - [16. Combined Fatigue + Impact Scenarios](#16-combined-fatigue--impact-scenarios)
  - [17. Reporting Requirements](#17-reporting-requirements)
- [PART VI — DECISION TREES AND QUICK REFERENCE](#part-vi--decision-trees-and-quick-reference)
  - [18. Master Decision Tree — Which Method to Use](#18-master-decision-tree--which-method-to-use)
  - [19. Quick Reference Tables](#19-quick-reference-tables)
  - [20. Checklist for Complete Verification](#20-checklist-for-complete-verification)
- [ANNEXES](#annexes)
  - [Annex A: FAT Class Catalog](#annex-a-fat-class-catalog)
  - [Annex B: Material Database Summary](#annex-b-material-database-summary)
  - [Annex C: Formula Summary](#annex-c-formula-summary)
  - [Annex D: Worked Examples](#annex-d-worked-examples)

---

# PART I — GENERAL FRAMEWORK

## 1. Scope and Objectives

### 1.1 Purpose

This document establishes a **generic, systematic, and reproducible engineering methodology** for verifying:

1. **Fatigue strength** of welded joints and components under cyclic loading
2. **Impact resistance** of welded structures under dynamic/crash loading

The methodology is applicable to **any type of welded mechanical structure**, including but not limited to:

- Automotive body-in-white and chassis
- EV battery enclosures and structural frames
- Hydrogen tank frames and pressure vessels
- Structural reinforcements and crash absorbers
- Offshore and civil engineering structures
- Industrial equipment and pressure equipment

### 1.2 Applicability Conditions

This methodology applies when **ALL** of the following conditions are met:

| Condition | Range |
|-----------|-------|
| Material | Structural steel (yield 210–1500 MPa) or wrought aluminum alloys |
| Joining method | Arc welding (MIG/MAG, TIG), laser welding, friction stir welding, resistance spot welding |
| Temperature | -40 °C to +300 °C (steel), -40 °C to +150 °C (aluminum) |
| Loading | Cyclic (fatigue), dynamic impact (crash), or combined |
| Design life | Finite (10³ to 10⁹ cycles) or infinite (endurance limit) |
| Crack initiation site | Weld toe, weld root, or base material adjacent to weld |

### 1.3 Exclusions

This methodology does **NOT** cover:

- Cast or forged components (no weld)
- Creep-fatigue interaction (T > 300 °C for steel, T > 150 °C for aluminum)
- Bolt fatigue or adhesive bonding
- Fatigue of non-metallic materials
- Blast/explosion loading (strain rate > 10⁴ /s)

---

## 2. Normative References

| Standard | Title | Application in This Methodology |
|----------|-------|-------------------------------|
| IIW XIII-2259-15 (2024) | Recommendations for Fatigue Design of Welded Joints and Components, 3rd Edition | **Primary fatigue reference**: S-N curves, FAT classes, assessment methods |
| EN 1993-1-9 | Eurocode 3 — Fatigue of steel structures | Alternative S-N curves, partial safety factors |
| EN 1999-1-3 | Eurocode 9 — Fatigue of aluminum structures | Aluminum-specific S-N curves and FAT classes |
| EN 1993-1-8 | Eurocode 3 — Design of joints | Weld strength, static and impact failure criteria |
| BS 7608:2014 | Fatigue design of steel structures | Alternative detail classification (B–W1 classes) |
| BS 7910:2019 | Assessment of flaws in metallic structures | Fracture mechanics, geometry factors, Mk factors |
| ISO 5817:2023 | Weld quality — Fusion-welded joints | Quality levels B/C/D, imperfection limits |
| DNV-RP-C203 | Fatigue design of offshore structures | Design fatigue factors for marine/offshore |
| ASME KD-10 | Hydrogen vessel fatigue | Hydrogen embrittlement knockdown factors |
| ASTM E1049-85 | Rainflow cycle counting | Variable amplitude load decomposition |
| IIW-2259-15 HFMI (2024) | HFMI treatment for fatigue improvement | Post-weld treatment improvement factors |

---

## 3. Terminology and Definitions

| Term | Symbol | Definition |
|------|--------|------------|
| Stress range | Δσ | σ_max − σ_min [MPa] |
| Mean stress | σ_m | (σ_max + σ_min) / 2 [MPa] |
| Stress ratio | R | σ_min / σ_max |
| Stress amplitude | σ_a | Δσ / 2 [MPa] |
| FAT class | FAT | Characteristic fatigue strength at N = 2×10⁶ cycles [MPa] |
| S-N curve | — | Relationship between Δσ and N (Wöhler curve) |
| Knee point | N_knee | Transition point on bilinear S-N curve (10⁷ for IIW) |
| Cumulative damage | D | Palmgren-Miner damage sum (failure at D ≥ 1.0) |
| Dynamic Increase Factor | DIF | σ_dynamic / σ_static |
| Strain rate | ε̇ | Rate of strain change [1/s] |
| Weld throat | a | Effective throat thickness of fillet weld [mm] |
| Hot-spot stress | σ_hs | Structural stress extrapolated to weld toe [MPa] |
| Notch stress | σ_notch | Maximum stress at weld toe with reference radius [MPa] |
| Specific Energy Absorption | SEA | Energy absorbed per unit mass [J/kg] |
| Crush Force Efficiency | CFE | P_mean / P_max (ratio of mean to peak crush force) |

---

## 4. Global Verification Workflow

The complete verification of a welded structure follows this master workflow:

```
START
  │
  ├──► STEP 1: Identify loading type
  │      ├── Cyclic loading only?  ──────────► GO TO PART II (Fatigue)
  │      ├── Impact/crash only?    ──────────► GO TO PART III (Impact)
  │      └── Combined?            ──────────► GO TO PART V (Combined)
  │
  ├──► STEP 2: Collect input data (Section 5)
  │      ├── Material properties
  │      ├── Joint geometry and weld type
  │      ├── Loading spectrum or impact conditions
  │      └── Environmental conditions
  │
  ├──► STEP 3: Select assessment method (Section 6)
  │      └── Use Decision Tree (Section 18)
  │
  ├──► STEP 4: Apply method-specific procedure
  │      └── Follow relevant section in Part II or Part III
  │
  ├──► STEP 5: Apply correction factors (Section 8)
  │
  ├──► STEP 6: Check acceptance criteria (Section 9)
  │
  └──► STEP 7: Document and report (Section 17)
```

**Principle: Every verification must produce a binary result — PASS or FAIL — with a quantified safety margin.**

---

# PART II — FATIGUE STRENGTH VERIFICATION

## 5. Phase 1: Data Collection and Classification

Before any calculation, the engineer must systematically collect and classify all input data. Missing or incorrectly classified data is the primary source of errors in fatigue assessment.

### 5.1 Material Data

**Required parameters:**

| Parameter | Symbol | Units | Source |
|-----------|--------|-------|--------|
| Material family | — | — | Drawing / specification |
| Grade designation | — | — | EN 10025, EN 10338, EN 10268, etc. |
| Yield strength | R_y (or R_p0.2) | MPa | Material certificate or standard minimum |
| Ultimate tensile strength | R_m (or S_u) | MPa | Material certificate or standard minimum |
| Young's modulus | E | MPa | 210 000 (steel), 70 000 (aluminum) |

**Decision rule for material family:**
- If the base material is carbon steel, alloy steel, or stainless steel → **Material = STEEL**
- If the base material is a wrought aluminum alloy (2xxx, 5xxx, 6xxx, 7xxx series) → **Material = ALUMINUM**
- Other materials → outside this methodology's scope

### 5.2 Joint Geometry and Weld Classification

Classify the joint according to the following decision table:

| Observation | Classification → WeldType |
|-------------|--------------------------|
| Two plates joined end-to-end, full penetration | **BUTT** |
| Triangular weld connecting overlapping or perpendicular members | **FILLET** |
| Two plates joined at right angles with full penetration butt welds on both sides | **CRUCIFORM** |
| Two overlapping plates with fillet welds | **LAP** |
| Plate welded perpendicular to another plate (one-sided or double-sided fillet) | **T_JOINT** |
| Longitudinal or transverse attachment (stiffener) | **STIFFENER** |
| Resistance spot weld (no filler metal, no visible bead) | **SPOT** |
| Laser butt weld (narrow bead, deep penetration) | **LASER_BUTT** |
| Laser fillet weld | **LASER_FILLET** |
| Friction stir weld (solid-state, no filler, characteristic flash) | **FSW_BUTT** |

**Additional geometric parameters to record:**

| Parameter | Symbol | When Required |
|-----------|--------|---------------|
| Plate thickness | t | Always |
| Weld throat | a | Fillet, cruciform, lap, T-joint |
| Penetration depth | p | Partial penetration welds |
| Attachment length | L | Stiffeners, longitudinal attachments |
| Weld length | L_w | Weld failure checks |
| Axial misalignment | e_axial | If misalignment observed or suspected |
| Angular misalignment | e_angular | If misalignment observed or suspected |

### 5.3 Loading Classification

**Step 1 — Determine the nature of loading:**

| Question | If YES → | If NO → |
|----------|----------|---------|
| Is the load repeated cyclically? | Fatigue loading | Continue |
| Is the load a single sudden event (crash, drop, explosion)? | Impact loading | Continue |
| Is the load random vibration (described by PSD)? | Vibration fatigue | Continue |
| Does the load have multiple directions simultaneously? | Multiaxial loading | Uniaxial loading |

**Step 2 — For fatigue loading, classify the amplitude:**

| Condition | Classification | Assessment Approach |
|-----------|---------------|---------------------|
| Δσ is constant throughout service life | **Constant Amplitude (CA)** | Direct S-N lookup |
| Δσ varies in blocks or randomly | **Variable Amplitude (VA)** | Palmgren-Miner cumulative damage |
| Load described by PSD in frequency domain | **Random / Vibration** | Dirlik or narrowband method |

**Step 3 — For fatigue loading, classify the directionality:**

| Condition | Classification | Assessment Approach |
|-----------|---------------|---------------------|
| Only one stress component (σ or τ) acts on the weld | **Uniaxial** | Standard S-N curve |
| Both normal (σ) and shear (τ) stress act simultaneously | **Multiaxial** | Gough-Pollard / Findley / MWCM |
| Stress components are in-phase (constant ratio σ/τ) | **Proportional** | Gough-Pollard (simpler) |
| Stress components are out-of-phase (varying ratio σ/τ) | **Non-proportional** | Findley / MWCM (required) |

**Step 4 — Determine load type on the weld:**

| Dominant stress at weld | Classification → LoadType |
|------------------------|--------------------------|
| Axial tension/compression perpendicular to or along the weld | **TENSION** |
| Bending-induced stress (linear gradient through thickness) | **BENDING** |
| In-plane shear along the weld throat | **SHEAR** |
| Combination of the above | **COMBINED** |

### 5.4 Environmental Conditions

Record the service environment:

| Parameter | Options | Effect |
|-----------|---------|--------|
| Atmosphere | Air, seawater (free corrosion), seawater (cathodic protection), industrial | Corrosion reduction factor |
| Temperature | Operating temperature [°C] | Temperature reduction factor |
| Hydrogen | Hydrogen pressure [bar] (if applicable) | Hydrogen embrittlement factor |
| Cryogenic | Temperature < -40 °C? | Ductile-to-brittle transition risk |

### 5.5 Weld Quality Data

Record observed or specified quality:

| Parameter | Options | Source |
|-----------|---------|--------|
| Quality level specification | B (best), C (intermediate), D (minimum) | Drawing or specification per ISO 5817 |
| Observed imperfections | Undercut, porosity, lack of fusion, misalignment, incomplete penetration, excess weld metal | Inspection report (visual, NDT) |
| Post-weld treatment | None, HFMI, TIG dressing, burr grinding, hammer peening, shot peening | Manufacturing specification |
| Post-weld heat treatment (PWHT) | Yes/No, temperature, hold time | Manufacturing specification |
| Weld process | MIG/MAG, TIG, laser, FSW, resistance spot, laser hybrid | Manufacturing specification |

### 5.6 Consequence and Safety Requirements

| Parameter | Options |
|-----------|---------|
| Consequence class | Low, Normal, High |
| Inspection level | None, periodic, continuous |
| Design standard | IIW, Eurocode 3, Eurocode 9, BS 7608, DNV |
| Required survival probability | 97.7% (standard), 99%, 99.9% |

---

## 6. Phase 2: Assessment Method Selection

This is the most critical decision in the fatigue verification. The wrong method leads to incorrect results. Use the following **decision logic**, proceeding from top to bottom:

### 6.1 Primary Method Selection Decision Tree

```
START: Do you have FEA results?
  │
  ├── YES, with fine mesh at weld toe (element ≤ r_ref/4)
  │     └──► Can you model the weld with reference radius r_ref = 1 mm?
  │           ├── YES ──► EFFECTIVE NOTCH STRESS METHOD (Section 6.4)
  │           └── NO  ──► Continue to hot-spot question
  │
  ├── YES, with coarse/medium mesh (element ≈ t)
  │     └──► Can you extract surface stresses at prescribed distances from weld toe?
  │           ├── YES ──► HOT-SPOT STRESS METHOD (Section 6.3)
  │           └── NO  ──► NOMINAL STRESS METHOD with FEA stresses (Section 6.2)
  │
  └── NO (hand calculation or simple FEA)
        └──► Can you calculate the nominal stress at the weld cross-section?
              ├── YES ──► Does the weld detail match an IIW catalog entry?
              │     ├── YES ──► NOMINAL STRESS METHOD (Section 6.2)
              │     └── NO  ──► HOT-SPOT or NOTCH method required (need FEA)
              └── NO  ──► Complex geometry — FEA required, then re-enter tree
```

**Additional decision checks (applied after primary selection):**

```
Is the loading MULTIAXIAL (combined σ and τ)?
  ├── YES ──► Use MULTIAXIAL assessment IN ADDITION to primary method (Section 10.1)
  └── NO  ──► Continue with primary method

Is there a known or assumed CRACK already present?
  ├── YES ──► Use FRACTURE MECHANICS (Section 10.3) instead of or in addition to S-N approach
  └── NO  ──► Continue with S-N approach

Is the weld a partial penetration fillet weld and root failure is possible?
  ├── YES ──► Check ROOT FATIGUE (Section 10.2) in addition to toe fatigue
  └── NO  ──► Continue with toe fatigue only

Is the loading random vibration (PSD input)?
  ├── YES ──► Use VIBRATION FATIGUE method (Section 10.4)
  └── NO  ──► Continue with time-domain approach

Do you have high-strength steel (R_y > 355 MPa) with known residual stresses?
  ├── YES ──► Consider 4R METHOD (Section 10.5) for more accurate mean stress treatment
  └── NO  ──► Standard mean stress correction is sufficient
```

### 6.2 Nominal Stress Method

**When to use:**
- The weld detail can be clearly identified in the IIW (or BS 7608) FAT class catalog
- Nominal stresses can be calculated by beam theory or simple FEA (away from discontinuities)
- The structural geometry matches a cataloged detail without significant modification
- Preliminary design or verification when FEA is not yet available

**When NOT to use:**
- Complex geometry that does not match any cataloged detail
- Stress gradients are too steep to define a meaningful "nominal" stress
- Multiple stress raisers interact near the weld

**Procedure:**

```
1. Calculate nominal stress range:
      Δσ_nom = σ_max - σ_min [MPa]
      (from section forces: Δσ = ΔF/A + ΔM·y/I for combined axial + bending)

2. Select FAT class from IIW catalog:
      → Based on WeldType + LoadType + material
      → See Annex A for complete catalog

3. Apply modifier chain (Section 8) to obtain effective FAT_design

4. Calculate allowable cycles:
      N_allow = (FAT_design / Δσ_nom)^m × 2×10⁶

5. Check acceptance:
      N_allow ≥ N_required → PASS
      OR: Δσ_nom ≤ FAT_design × (2×10⁶ / N_required)^(1/m) → PASS
```

### 6.3 Hot-Spot Stress Method

**When to use:**
- FEA is available with appropriate mesh at the weld toe region
- The stress gradient near the weld is significant and cannot be captured by nominal stress
- The weld detail is a standard type but the geometry has proportions not covered exactly by the nominal stress catalog
- Type a (plate surface) or Type b (plate edge) extrapolation can be applied

**When NOT to use:**
- Root failure is the critical mode (hot-spot method only addresses toe failures)
- The weld is at a free edge without a plate surface for extrapolation
- Coarse mesh does not allow stress extraction at the prescribed distances

**Procedure:**

```
1. Extract surface stresses from FEA at prescribed distances from weld toe:

   TYPE A (plate surface, perpendicular to weld):
     Linear:    σ_hs = 1.67 × σ(0.4t) - 0.67 × σ(1.0t)
     Quadratic: σ_hs = 2.52 × σ(0.4t) - 2.24 × σ(0.9t) + 0.72 × σ(1.4t)

   TYPE B (along plate edge, along weld toe):
     σ_hs = 3 × σ(5mm) - 3 × σ(15mm) + σ(25mm)

2. Select hot-spot FAT class:
     Non-load-carrying fillet: FAT 100
     Load-carrying fillet:     FAT 90

3. Apply modifier chain (Section 8) to obtain FAT_design

4. Calculate allowable cycles from S-N curve:
     N_allow = (FAT_design / Δσ_hs)^m × 2×10⁶

5. Check: N_allow ≥ N_required → PASS
```

**Which extrapolation to choose:**

| Situation | Use |
|-----------|-----|
| Weld on plate surface, mesh size ≈ t | Type A, Linear (2-point) |
| Weld on plate surface, fine mesh (≤ 0.4t) | Type A, Quadratic (3-point) |
| Weld at plate edge or along free edge | Type B (fixed distances) |

### 6.4 Effective Notch Stress Method

**When to use:**
- Fine FE mesh is available (element size ≈ r_ref/4 = 0.25 mm)
- The weld geometry is complex and cannot be classified by the nominal stress catalog
- Assessment of both weld toe and weld root failure is needed
- High accuracy is required for critical components
- Thick plates (t ≥ 5 mm) for standard r_ref, or thin sheets with micro-support r_ref

**When NOT to use:**
- Thin sheets (t < 5 mm) unless the micro-support r_ref = 0.05 mm is used
- When a coarse FE mesh is the only option
- For preliminary design (unnecessarily complex)

**Procedure:**

```
1. Model the weld with reference radius:
     Standard (t ≥ 5 mm): r_ref = 1.0 mm at toe and/or root
     Thin sheet (t < 5 mm): r_ref = 0.05 mm

2. Run FEA and extract maximum principal stress at the notch:
     Δσ_notch = σ_max,notch - σ_min,notch

3. Use universal FAT class:
     Steel:    FAT 225
     Aluminum: FAT 71

4. Apply modifier chain (Section 8) to obtain FAT_design
     NOTE: Thickness correction is NOT applied (geometry is explicitly modeled)
     NOTE: Weld quality km is NOT applied (geometry is explicit)

5. Calculate allowable cycles:
     N_allow = (FAT_design / Δσ_notch)^m × 2×10⁶

6. Check: N_allow ≥ N_required → PASS
```

### 6.5 Method Comparison and Selection Summary

| Criterion | Nominal Stress | Hot-Spot Stress | Effective Notch Stress |
|-----------|---------------|-----------------|----------------------|
| Complexity | Low | Medium | High |
| FEA required? | No (optional) | Yes | Yes (fine mesh) |
| Mesh requirement | N/A | Element ≈ t | Element ≈ r_ref/4 |
| Weld detail catalog required? | Yes | Partially | No |
| Captures local geometry? | No | Partially | Yes |
| Root failure? | No | No | Yes |
| Typical application | Preliminary design, standard details | FEA-based verification | Critical components, complex geometry |
| Conservatism | Variable (depends on catalog match) | Moderate | Least conservative (most accurate) |

---

## 7. Phase 3: S-N Curve and Standard Selection

### 7.1 Standard Selection Decision

```
What is the governing design code for your project?

  ├── European steel structures (buildings, bridges, cranes)
  │     └──► EN 1993-1-9 (Eurocode 3)
  │
  ├── European aluminum structures
  │     └──► EN 1999-1-3 (Eurocode 9)
  │
  ├── UK practice for steel structures
  │     └──► BS 7608:2014
  │
  ├── Offshore / marine structures
  │     └──► DNV-RP-C203
  │
  ├── International / automotive / general mechanical engineering
  │     └──► IIW XIII-2259-15 (2024)  ← RECOMMENDED DEFAULT
  │
  └── No specific code requirement
        └──► IIW XIII-2259-15 (2024)  ← RECOMMENDED DEFAULT
```

### 7.2 S-N Curve Parameters by Standard

#### IIW (Default — Recommended)

| Parameter | Steel | Aluminum |
|-----------|-------|----------|
| Reference cycles (N_ref) | 2 × 10⁶ | 2 × 10⁶ |
| Slope m₁ (below knee) | 3.0 | 3.376 |
| Slope m₂ (above knee, VA only) | 5.0 | 5.376 |
| Knee point (N_knee) | 10⁷ | 10⁷ |
| Cut-off (N_cut) | 10⁹ | 10⁹ |
| Constant amplitude: below knee stress | Infinite life | Infinite life |
| Variable amplitude: below knee stress | Continues with m₂ | Continues with m₂ |

**S-N equation:**
```
Region 1 (N ≤ N_knee):
    N = (FAT / Δσ)^m₁ × N_ref

Region 2 (N_knee < N ≤ N_cut, variable amplitude only):
    N = (Δσ_knee / Δσ)^m₂ × N_knee
    where Δσ_knee = FAT × (N_ref / N_knee)^(1/m₁)
```

#### Eurocode 3 (EN 1993-1-9)

| Parameter | Value |
|-----------|-------|
| Slope m₁ | 3.0 |
| Slope m₂ | 5.0 |
| Knee point | 5 × 10⁶ (earlier than IIW) |
| Cut-off | 10⁸ (lower than IIW) |

#### BS 7608:2014

| Detail Class | Slope m | Reference Stress S_ref [MPa] |
|-------------|---------|------------------------------|
| B | 4.0 | 100 |
| C | 3.5 | 78 |
| D | 3.0 | 53 |
| E | 3.0 | 47 |
| F | 3.0 | 40 |
| F2 | 3.0 | 35 |
| G | 3.0 | 29 |
| W1 | 3.0 | 25 |

Cut-off: 10⁸ cycles

#### Eurocode 9 (EN 1999-1-3 — Aluminum)

| Parameter | Value |
|-----------|-------|
| Slope m₁ | 3.4 (most details) or 4.3 (FAT 32, 28, 25) |
| Slope m₂ | 5.4 |
| Knee point | 5 × 10⁶ |
| Cut-off | 10⁸ |

### 7.3 Decision Rule: Which S-N Curve for Your Case

```
IF material = aluminum
    IF standard = eurocode9 → Use Eurocode 9 curve (m₁=3.4, knee at 5e6)
    ELSE → Use IIW aluminum curve (m₁=3.376, knee at 1e7)

IF material = steel
    IF standard = eurocode3 → Use Eurocode 3 curve (m₁=3, knee at 5e6, cut-off 1e8)
    IF standard = bs7608 → Use BS 7608 curve (variable m per class)
    IF standard = dnv → Use IIW curve + DNV DFF on life
    ELSE → Use IIW steel curve (m₁=3, knee at 1e7, cut-off 1e9)

IF loading = constant_amplitude
    → S-N curve terminates at knee point (infinite life below)
    → Exception: corrosive environment removes endurance limit

IF loading = variable_amplitude
    → S-N curve extends past knee with slope m₂
    → Cut-off applies (no damage below cut-off stress)
```

---

## 8. Phase 4: Modifier Chain — Correction Factors

The "raw" FAT class must be adjusted by a chain of correction factors before use. **All applicable factors are multiplied together** to obtain the effective design FAT class:

```
FAT_design = FAT_base × f_thickness × f_environment × f_treatment × f_process × f_quality / (γ_Mf × γ_Ff) × f_survival
```

**Apply the modifiers in the following order. Each modifier is applied ONLY when the corresponding condition is met:**

### 8.1 Thickness Correction

**When to apply:** Plate thickness t > 25 mm (reference thickness t_ref = 25 mm)

**When NOT to apply:**
- Effective notch stress method (geometry explicitly modeled)
- Shear loading on fillet welds (exponent = 0)
- t ≤ 25 mm (factor = 1.0)

**Formula:**
```
f_thickness = (t_ref / t_eff)^n    for t_eff > t_ref
f_thickness = 1.0                   for t_eff ≤ t_ref

t_ref = 25 mm
```

**Exponent n by weld type and load:**

| Weld Type | Tension/Bending | Shear |
|-----------|----------------|-------|
| Butt | 0.2 | 0.1 |
| Cruciform | 0.3 | — |
| T-joint | 0.2 | — |
| Fillet | 0.1 | 0.0 |
| Lap | 0.1 | 0.0 |
| Stiffener | 0.2 | — |

### 8.2 Environmental Correction

**When to apply:** Service environment is NOT dry air at ambient temperature

**Corrosion factor (f_corrosion):**

| Environment | Steel | Aluminum |
|-------------|-------|----------|
| Air (dry or mild) | 1.0 | 1.0 |
| Seawater, free corrosion | 0.7 | 0.6 |
| Seawater, cathodic protection | 0.85 | 0.8 |
| Industrial atmosphere | 0.9 | 0.85 |
| Hydrogen gas | 0.5 | 0.9 |

**Temperature factor (f_temperature):**

| Material | Condition | Factor |
|----------|-----------|--------|
| Steel | T ≤ 100 °C | 1.0 |
| Steel | 100 < T ≤ 300 °C | 1.0 − 0.0015 × (T − 100) |
| Steel | T > 300 °C | **Outside scope** (creep regime) |
| Aluminum | T ≤ 50 °C | 1.0 |
| Aluminum | 50 < T ≤ 150 °C | 1.0 − 0.003 × (T − 50) |
| Aluminum | T > 150 °C | **Outside scope** |

**Hydrogen embrittlement factor (f_hydrogen):**
```
f_H2 = 1 / (1 + 0.002 × p)    [steel only, p in bar]
f_H2 = 1.0                      [aluminum, unaffected]
```

**Cryogenic factor (f_cryo):**
```
T < -40 °C (carbon/low-alloy steel): f_cryo = 0.8
T < -40 °C (austenitic SS or aluminum): f_cryo = 1.0
T ≥ -40 °C: f_cryo = 1.0
```

**Combined environmental factor:**
```
f_environment = f_corrosion × f_temperature × f_H2 × f_cryo
```

**Special rule:** In seawater environments (free or CP), the endurance limit is **removed** — the S-N curve continues with slope m₁ indefinitely (no knee point).

### 8.3 Post-Weld Treatment Improvement

**When to apply:** Post-weld treatment has been applied and verified

**Treatment upgrade in FAT steps (IIW standard FAT sequence: 36, 40, 45, 50, 56, 63, 71, 80, 90, 100, 112, 125, 140, 160):**

| Treatment | Upgrade Steps | Conditions / Notes |
|-----------|--------------|-------------------|
| None | 0 | Baseline (as-welded) |
| Burr grinding | +1 | Surface smoothing at weld toe |
| TIG dressing | +2 | Re-melting of weld toe for smoother profile |
| Shot peening | +2 | Compressive residual stress introduced |
| Hammer peening | +2 to +3 | Yield-dependent improvement |
| **HFMI** | **+4 to +8** | **IIW 2024 yield-dependent:** see table below |

**HFMI improvement table (IIW-2259-15, 2024):**

| Yield Strength R_y [MPa] | Upgrade Steps |
|--------------------------|---------------|
| 235 – 355 | +4 |
| 355 – 550 | +6 |
| 550 – 750 | +8 |
| 750 – 1300 | +8 (capped) |

**Example:** FAT 71 with HFMI on R_y = 500 MPa steel:
- Upgrade +6 steps: 71 → 80 → 90 → 100 → 112 → 125 → 140
- Result: FAT 140

**Important restrictions:**
- Post-weld treatment improvement is valid ONLY for weld toe failure
- Root failure is NOT improved by surface treatments
- Treatment quality must be verified by inspection

### 8.4 Weld Process Factor

**When to apply:** The weld process differs from MIG/MAG (reference process)

| Process | Factor (on FAT) |
|---------|-----------------|
| MIG/MAG | 1.00 (reference) |
| TIG | 1.10 (better toe geometry) |
| Laser | 1.10 – 1.20 (narrow HAZ) |
| FSW | 1.30 (solid-state, no defects) |
| Laser hybrid | 1.15 |

### 8.5 Weld Quality and Misalignment

**Quality level FAT adjustment (ISO 5817):**

Instead of applying a factor, select the base FAT class according to the achieved quality level:

| Quality Level | Butt | Fillet | Cruciform | T-Joint | Lap |
|---------------|------|--------|-----------|---------|-----|
| B (highest) | FAT 112 | FAT 90 | FAT 80 | FAT 80 | FAT 71 |
| C (intermediate) | FAT 90 | FAT 71 | FAT 63 | FAT 63 | FAT 56 |
| D (minimum) | FAT 71 | FAT 56 | FAT 50 | FAT 50 | FAT 45 |

**Misalignment stress magnification factor (k_m):**

If axial or angular misalignment is present, the applied stress is increased:

```
Axial:   k_m,axial = 1 + e/t
Angular: k_m,angular = 1 + c × (e/t)
    where c = 1.5 (fixed ends) or 3.0 (pinned ends)

Combined: k_m = k_m,axial × k_m,angular

Effective stress: σ_eff = σ_nom × k_m
```

**When to apply:** The nominal stress method is used AND misalignment has been measured or assumed from tolerances. For the notch stress method, misalignment should be modeled explicitly in FEA.

### 8.6 Mean Stress Correction

**When to apply:** The loading has a non-zero mean stress AND the joint is stress-relieved (PWHT)

**Decision rule for method selection:**

```
IF joint is as-welded (no PWHT):
    → No mean stress correction needed (IIW assumption: residual stresses
      already at yield, so R-ratio effect is negligible)
    → f(R) = 1.0

IF joint is stress-relieved (PWHT):
    → Apply IIW enhancement factor f(R):
        R < -1:        f(R) = 1.6
        -1 ≤ R ≤ 0.5:  f(R) = -0.4R + 1.2
        R > 0.5:       f(R) = 1.0

    OR apply one of the classical methods:
        Goodman:   Δσ_eq = Δσ / (1 - σ_m/S_u)     [most common]
        Gerber:    Δσ_eq = Δσ / (1 - (σ_m/S_u)²)   [less conservative]
        Soderberg: Δσ_eq = Δσ / (1 - σ_m/R_y)       [most conservative]
```

**Selection guidance:**
- **IIW f(R):** Recommended for welded joints; use when R-ratio is known
- **Goodman:** General-purpose; conservative for most cases
- **Gerber:** Use when Goodman is over-conservative and test data supports it
- **Soderberg:** Use for safety-critical components requiring maximum conservatism

### 8.7 Residual Stress Consideration

**As-welded condition (default):**
```
σ_res = R_y (yield strength)    [IIW conservative assumption]
→ No mean stress correction benefit (worst-case R-ratio already assumed)
```

**After PWHT:**
```
Remaining residual stress fraction:
    f_relief = exp(-k × (T - 200) × √t_hold)

where:
    k = 0.004 (empirical constant)
    T = PWHT temperature [°C] (must be > 200 °C for any relief)
    t_hold = hold time [hours]

σ_res,final = σ_res,initial × f_relief

Typical relief:
    550 °C, 1 hour → ~70% relief
    600 °C, 1 hour → ~80% relief
    620 °C, 2 hours → ~90% relief
```

**Under cyclic loading (relaxation):**
```
After first cycle: σ_res = max(0, R_y - σ_max)    [if plasticity occurs]
Continued cycling: σ_res(N) = σ_res(1) × (1 - 0.1 × log₁₀(N))
```

### 8.8 Safety Factors

**Partial safety factor on resistance (γ_Mf):**

*IIW Standard:*

| Consequence \ Inspection | Periodic | Continuous | None |
|-------------------------|----------|------------|------|
| Low | 1.00 | 1.00 | 1.00 |
| Normal | 1.15 | 1.00 | 1.25 |
| High | 1.30 | 1.15 | 1.40 |

*Eurocode 3:*

| Consequence | γ_Mf |
|-------------|-------|
| Low | 1.00 |
| Normal | 1.15 |
| High | 1.35 |

**DNV Design Fatigue Factor (DFF):**

| Consequence \ Inspection | Periodic | None |
|-------------------------|----------|------|
| Low | 1.0 | 2.0 |
| Normal | 2.0 | 3.0 |
| High | 3.0 | 10.0 |

Applied as: N_design = N_calculated / DFF (reduces allowable life)

**Load partial factor (γ_Ff):** 1.0 for all standards (loads assumed already factored)

**Survival probability adjustment:**
```
IIW curves are characteristic at 97.7% survival (mean − 2σ)
Standard deviation in log₁₀(N) = 0.2 for welded joints

For different probability:
    f_survival = 10^(-Δz × 0.2 / m)
    where Δz = z(target) - 2.0

Common:
    97.7% → f_survival = 1.000 (reference)
    99.0% → f_survival ≈ 0.957
    99.9% → f_survival ≈ 0.869
```

**Combined effect on FAT class:**
```
FAT_design = FAT_base × f_survival / (γ_Mf × γ_Ff)
```

### 8.9 Complete Modifier Chain — Summary Table

Apply the following factors **in order**. If a factor does not apply (condition not met), set it to 1.0:

| # | Factor | Symbol | Applied To | Condition to Apply |
|---|--------|--------|-----------|-------------------|
| 1 | Thickness correction | f_thick | FAT class | t > 25 mm AND not notch method |
| 2 | Environmental correction | f_env | FAT class | Environment ≠ air at 20°C |
| 3 | Post-weld treatment | f_pwt | FAT class (step upgrade) | Treatment applied |
| 4 | Weld process | f_proc | FAT class | Process ≠ MIG/MAG |
| 5 | Misalignment | k_m | Applied stress | Misalignment present |
| 6 | Mean stress correction | f(R) or equivalent | Applied stress | Stress-relieved joint, R ≠ 0 |
| 7 | Partial safety factor (resistance) | 1/γ_Mf | FAT class | Always (γ_Mf ≥ 1.0) |
| 8 | Load partial factor | 1/γ_Ff | Stress range | Always (typically 1.0) |
| 9 | Survival probability | f_surv | FAT class | Target ≠ 97.7% |

```
Effective stress:  Δσ_eff = Δσ_nom × k_m × γ_Ff / f(R)
Effective FAT:     FAT_eff = FAT_base × f_thick × f_env × f_pwt × f_proc × f_surv / γ_Mf
```

---

## 9. Phase 5: Damage Calculation and Acceptance Criteria

### 9.1 Constant Amplitude Loading

**Procedure:**

```
1. Compute effective stress range: Δσ_eff (after corrections)
2. Compute effective FAT class: FAT_eff (after all modifiers)
3. Calculate allowable cycles:

   N_allow = (FAT_eff / Δσ_eff)^m × 2×10⁶

4. Check infinite life:
   IF Δσ_eff < Δσ_knee AND loading is constant amplitude AND environment does not remove endurance limit:
       → N_allow = ∞ → PASS (infinite life)

   where Δσ_knee = FAT_eff × (2×10⁶ / N_knee)^(1/m₁)

5. Check finite life:
   IF N_allow ≥ N_required → PASS
   IF N_allow < N_required → FAIL

6. Calculate safety factor:
   SF = (N_allow / N_required)^(1/m)
       → SF > 1.0 → PASS
       → SF ≤ 1.0 → FAIL
```

### 9.2 Variable Amplitude Loading

**Procedure (Palmgren-Miner cumulative damage):**

```
1. Decompose load history into stress range blocks:
   - From measured spectrum: use RAINFLOW COUNTING (ASTM E1049-85)
   - From design spectrum: use pre-defined load blocks {(Δσ_i, n_i)}

2. For each block i:
   a. Calculate effective stress: Δσ_i,eff (apply misalignment, mean stress)
   b. Calculate allowable cycles from S-N curve:
      - If Δσ_i,eff ≥ Δσ_knee:  N_i = (FAT_eff / Δσ_i,eff)^m₁ × N_ref
      - If Δσ_knee > Δσ_i,eff ≥ Δσ_cut: N_i = (Δσ_knee / Δσ_i,eff)^m₂ × N_knee
      - If Δσ_i,eff < Δσ_cut:   N_i = ∞ (no damage contribution)
   c. Calculate partial damage: D_i = n_i / N_i

3. Sum cumulative damage:
   D_total = Σ D_i

4. Check acceptance:
   D_total < D_limit → PASS
   D_total ≥ D_limit → FAIL

   where D_limit:
     Standard structures:        D_limit = 1.0
     Safety-critical structures: D_limit = 0.5

5. Calculate equivalent constant amplitude stress range:
   Δσ_eq = [Σ(n_i × Δσ_i,eff^m) / Σn_i]^(1/m)
   (useful for comparison and reporting)
```

### 9.3 Acceptance Criteria Summary

| Criterion | PASS Condition | Notes |
|-----------|---------------|-------|
| Constant amplitude, finite life | N_allow ≥ N_required | OR SF ≥ 1.0 |
| Constant amplitude, infinite life | Δσ_eff < Δσ_knee | Only if endurance limit exists |
| Variable amplitude | D_total < D_limit | D_limit = 1.0 (normal) or 0.5 (critical) |
| Multiaxial (Gough-Pollard) | (Δσ/Δσ_R)² + (Δτ/Δτ_R)² < 1 | Interaction criterion |
| Multiaxial (Findley) | FP / FP_limit < 1 | Critical plane criterion |
| Fracture mechanics | a_final < a_critical at N_required | Crack must not reach critical size |
| Root fatigue | N_allow,root ≥ N_required | Separate check for root failure |

---

## 10. Special Cases in Fatigue

### 10.1 Multiaxial Fatigue

**When required:** Combined normal stress (σ) and shear stress (τ) act on the weld simultaneously.

**Step 1 — Determine proportionality:**

```
IF time histories of σ(t) and τ(t) are available:
    Compute ratio: ρ(t) = τ(t) / σ(t)
    IF coefficient of variation of ρ(t) < 0.1 → PROPORTIONAL
    ELSE → NON-PROPORTIONAL

IF only peak values are known:
    IF σ and τ reach their maxima simultaneously → assume PROPORTIONAL
    IF they are out of phase → NON-PROPORTIONAL
```

**Step 2 — Select multiaxial criterion:**

| Loading Type | Recommended Criterion |
|-------------|----------------------|
| Proportional | **Gough-Pollard** (IIW recommended) |
| Non-proportional, moderate | **Modified Wöhler Curve Method (MWCM)** |
| Non-proportional, critical components | **Findley critical plane** |

**Step 3 — Apply the selected criterion:**

**Gough-Pollard (Proportional):**
```
Check: (Δσ / Δσ_R)² + (Δτ / Δτ_R)² ≤ 1.0

where:
    Δσ_R = FAT_σ × (N_ref / N)^(1/m)    [allowable normal stress range]
    Δτ_R = FAT_τ × (N_ref / N)^(1/m)    [allowable shear stress range]

IF FAT_τ is not specified: FAT_τ = FAT_σ / √3

Utilization = √((Δσ/Δσ_R)² + (Δτ/Δτ_R)²)
PASS if utilization < 1.0
```

**Findley Critical Plane (Non-Proportional):**
```
For each plane angle θ from 0° to 180°:
    τ_a(θ) = shear stress amplitude on plane
    σ_n,max(θ) = maximum normal stress on plane

    FP(θ) = τ_a(θ) + k × σ_n,max(θ)

Find θ_critical where FP is maximum.

Material parameter k = 0.2 to 0.4 for welded joints (typically 0.3)

Utilization = FP(θ_critical) / FP_allowable
PASS if utilization < 1.0
```

**MWCM (Non-Proportional):**
```
Equivalent stress range:
    Δσ_eq = √(Δσ² + 3 × Δτ²)    [von Mises energy criterion]

Biaxiality ratio: ρ = Δτ / Δσ (or τ_a / σ_a)

Modified S-N slope: m_eff = 3.0 + 2.0 × min(ρ, 1.0)

Evaluate against S-N curve with slope m_eff
```

### 10.2 Root Fatigue (Partial Penetration Welds)

**When to check:** The weld is a partial penetration fillet weld and cracking from the root is geometrically possible.

**Identification rule:**
```
IF weld type = FILLET or T_JOINT or LAP or CRUCIFORM
    AND penetration < plate thickness (partial penetration)
    → Root fatigue check is REQUIRED in addition to toe check
```

**Procedure:**

```
1. Calculate root stress concentration factor:
   SCF_root = 1 + 2 × √((t - p) / (2 × a))
   where:
       t = plate thickness [mm]
       p = penetration depth [mm]
       a = weld throat [mm]

   For bending: SCF_bending = SCF_tension × 0.85

2. Calculate root notch stress:
   σ_root = σ_nominal × SCF_root × min(t / a_eff, 3.0)
   where a_eff = a + p

3. Use root FAT class:
   Steel:    FAT 200
   Aluminum: FAT 71

4. Calculate N_allow for root:
   N_allow,root = (FAT_root / Δσ_root)^m × N_ref

5. Compare with toe result:
   Critical location = min(N_allow,toe, N_allow,root)
   Report which location governs
```

**Important:** Post-weld surface treatments (HFMI, grinding, etc.) do NOT improve root fatigue life.

### 10.3 Fracture Mechanics (LEFM)

**When to use:**
- A crack or flaw is known to exist (from inspection or assumed)
- Fitness-for-service assessment of a component with detected flaws
- Remaining life estimation after crack detection
- Design life verification when S-N approach is insufficient

**Procedure:**

```
1. Define initial crack parameters:
   a₀ = initial crack depth [mm]
       → If known from inspection: use measured value
       → If assumed (design): a₀ = 0.1 to 0.5 mm (typical for welded joints)
   a_c = critical crack depth [mm]
       → From fracture toughness: a_c = (K_Ic / (Y × σ_max))² / π
       → Or from structural requirement (e.g., through-thickness = plate thickness t)

2. Select Paris law parameters:

   | Environment | Material | C [mm/cycle] | m |
   |-------------|----------|-------------|---|
   | Air | Steel | 5.21 × 10⁻¹³ | 3.0 |
   | Seawater (free) | Steel | 1.30 × 10⁻¹² | 3.0 |
   | Seawater (CP) | Steel | (use air values) | 3.0 |
   | Air | Aluminum | 1.59 × 10⁻¹¹ | 3.06 |

3. Select geometry and weld magnification factors:

   Geometry factor Y(a/t):
       Edge crack:    Y = polynomial fit (BS 7910)
       Through crack: Y = 1.0
       Surface crack: Y = 1.12 / √Q (semi-elliptical)

   Weld magnification Mk(a/t):
       T-butt:     Mk = 0.51 × (a/t)^(-0.31)
       Cruciform:  Mk = 0.50 × (a/t)^(-0.29)
       Lap:        Mk = 0.45 × (a/t)^(-0.25)
       Fillet:     Mk = 0.48 × (a/t)^(-0.30)

4. Stress intensity factor range:
   ΔK = Y × Mk × Δσ × √(π × a)

5. Integrate crack growth:
   da/dN = C × (ΔK - ΔK_th)^m    [threshold included]

   ΔK_th (threshold):
       Steel: 63 MPa√mm (~2 MPa√m)
       Aluminum: 30 MPa√mm (~1 MPa√m)

   Numerical integration: Euler forward from a₀ to a_c
   → Count total cycles N_total

6. Acceptance:
   N_total ≥ N_required → PASS (crack does not reach critical size during design life)
   N_total < N_required → FAIL
```

### 10.4 Vibration Fatigue (Frequency Domain)

**When to use:** Loading is random vibration described by a Power Spectral Density (PSD) rather than a time history.

**Procedure:**

```
1. Obtain PSD: G(f) [MPa²/Hz] as function of frequency f [Hz]
   (from measured data, test specification, or FEA)

2. Compute spectral moments:
   m_n = ∫ f^n × G(f) df    for n = 0, 1, 2, 4

3. Compute bandwidth parameters:
   Irregularity factor: γ = m₂ / √(m₀ × m₄)
   Expected peak rate:  E_P = √(m₄ / m₂) [peaks/second]
   Expected zero rate:  E_0 = √(m₂ / m₀) [zero-crossings/second]

4. Select method based on bandwidth:

   IF γ > 0.99:
       → NARROW-BAND approximation (conservative, simple)
       D = E_0 × T × (2√(2m₀))^m × Γ(1 + m/2) / C_sn
       where C_sn = FAT^m × N_ref

   IF γ < 0.99:
       → DIRLIK'S METHOD (most accurate for wide-band Gaussian)
       Compute Dirlik PDF p(S) and integrate:
       D = E_P × T × ∫ S^m × p(S) dS / C_sn

   ALTERNATIVELY:
       → WIRSCHING-LIGHT CORRECTION (correction to narrow-band)
       ε = √(1 - γ²)    [bandwidth parameter]
       λ = a(m) + (1 - a(m)) × (1 - ε)^b(m)
       a(m) = 0.926 - 0.033m
       b(m) = 1.587m - 2.323
       D_corrected = λ × D_narrowband

5. Duration: T = total exposure time [seconds]

6. Acceptance:
   D < D_limit → PASS
```

**Method selection guidance:**

| Bandwidth (γ) | Recommended Method | Notes |
|---------------|-------------------|-------|
| γ > 0.99 | Narrow-band | Simple, conservative |
| 0.7 < γ < 0.99 | Wirsching-Light | Good correction for moderate bandwidth |
| γ < 0.7 | Dirlik | Required for wide-band processes |

### 10.5 4R Method (Advanced Mean Stress Correction)

**When to use:**
- High-strength steel (R_y > 355 MPa) where standard mean stress corrections may be inaccurate
- Known residual stress state (measured or PWHT data available)
- Maximum accuracy needed for critical components

**Procedure:**

```
1. Determine local stresses (Neuber correction):
   IF σ_elastic ≤ R_y:
       σ_local = σ_elastic
   IF σ_elastic > R_y:
       σ_local = R_y (capped at yield)
       ε_local = σ_elastic² / (E × R_y)

2. Include residual stress:
   σ_max,local = σ_max,neuber + σ_res (capped at R_y)
   σ_min,local = σ_min,neuber + σ_res

3. Local stress ratio:
   R_local = σ_min,local / σ_max,local

4. Mean stress sensitivity:
   M = 0.00035 × R_m - 0.1    (clamped ≥ 0)

5. Equivalent stress range:
   Δσ_eq = Δσ × (1 - M × R_local) / (1 + M)

6. Evaluate against master curve:
   Steel: FAT 200 (r_ref = 1mm, R_local = 0)
   Aluminum: FAT 71
```

---

# PART III — IMPACT RESISTANCE VERIFICATION

## 11. Phase 1: Dynamic Material Characterization

### 11.1 When Is Impact Assessment Required?

```
IF any of the following:
    - Component is in a crash load path
    - Design specification includes impact/crash load case
    - Strain rate in service exceeds 1 /s
    - Dynamic loading duration < 100 ms
→ Impact assessment is REQUIRED
```

### 11.2 Strain Rate Model Selection

**Decision rule:**

```
IF only strain-rate effects are needed (no thermal or strain hardening):
    → Use COWPER-SYMONDS model (simpler, sufficient for most crash cases)

IF thermal effects are significant (adiabatic heating, high-speed impact):
    → Use JOHNSON-COOK model (captures strain rate + temperature + strain hardening)

IF the material is common structural steel:
    → Cowper-Symonds is the default choice

IF high-fidelity simulation is needed (ballistic, forming):
    → Johnson-Cook with temperature coupling
```

### 11.3 Cowper-Symonds Model

**Formula:**
```
DIF = 1 + (ε̇ / D)^(1/q)
σ_dynamic = σ_static × DIF

where:
    ε̇ = strain rate [1/s]
    D, q = material constants
```

**Material parameters:**

| Grade | D [1/s] | q | Typical Application |
|-------|---------|---|---------------------|
| DC04 | 40.4 | 5.0 | Deep-drawing, body panels |
| DP600 | 100.0 | 4.73 | Structural reinforcements |
| DP780 | 200.0 | 4.5 | B-pillars, side impact |
| DP980 | 300.0 | 4.0 | Safety cage components |
| HSLA340 | 80.0 | 4.8 | Chassis, subframes |
| HSLA420 | 120.0 | 4.5 | Cross members |
| 22MnB5 | 802.0 | 3.585 | Hot-stamped components |
| S355J2 | 40.4 | 5.0 | Structural steel (civil/general) |
| 316L | 100.0 | 10.0 | Stainless (high rate-sensitivity) |
| 6061-T6 | 6500.0 | 4.0 | Aluminum structures |
| 6082-T6 | 6500.0 | 4.0 | Aluminum extrusions |
| 5083-H111 | 6500.0 | 4.0 | Marine aluminum |
| 5754-O | 6500.0 | 4.0 | Automotive aluminum |
| 7075-T6 | 6500.0 | 4.0 | Aerospace aluminum |

**Typical strain rates by application:**

| Scenario | Strain Rate [1/s] | Notes |
|----------|--------------------|-------|
| Quasi-static testing | 10⁻⁴ to 10⁻² | Standard tensile test |
| Seismic loading | 10⁻² to 1 | Earthquake response |
| Automotive crash | 1 to 500 | Front/side/rear impact |
| High-speed crash | 500 to 1000 | High-speed collision |
| Blast/explosion | 1000 to 10⁴ | Outside scope |

### 11.4 Johnson-Cook Model

**Formula:**
```
σ = (A + B × εₚⁿ) × (1 + C × ln(ε̇ / ε̇₀)) × (1 - T*ᵐ)

where:
    T* = (T - T_ref) / (T_melt - T_ref)    [homologous temperature]
    εₚ = plastic strain
    ε̇₀ = reference strain rate (typically 1.0 /s)
    T_ref = reference temperature (typically 293 K)
```

**Three-term decomposition:**

| Term | Formula | Physical Meaning |
|------|---------|-----------------|
| Strain hardening | (A + B × εₚⁿ) | Stress increases with plastic deformation |
| Strain rate | (1 + C × ln(ε̇/ε̇₀)) | Stress increases with loading speed |
| Thermal softening | (1 − T*ᵐ) | Stress decreases with temperature rise |

**When to use each term:**
- Static analysis at room temperature: Only Term 1 (pure σ-ε curve)
- Crash at room temperature: Terms 1 + 2 (rate-dependent yield)
- High-speed impact with adiabatic heating: All three terms
- Hot forming (press hardening): Terms 1 + 3 (no rate effect needed)

**For crash assessment at room temperature:**
```
Dynamic yield at 0.2% offset:
    σ_y,dyn = (A + B × 0.002ⁿ) × (1 + C × ln(ε̇ / ε̇₀))
```

### 11.5 Acceptance Criteria for Dynamic Material

```
Calculate:
    DIF = σ_dynamic / σ_static
    σ_dynamic = σ_static × DIF

Check:
    IF DIF is unreasonably high (> 3 for steel, > 2 for aluminum):
        → Verify strain rate assumption; may indicate error in load estimation

Design use:
    → Use σ_dynamic as the material yield in all subsequent impact checks
    → σ_dynamic replaces σ_static in weld failure formulas and energy calculations
```

---

## 12. Phase 2: Weld Joint Failure Assessment Under Impact

### 12.1 When Is Weld Failure Assessment Required?

```
IF the structure contains welds in the crash load path
    AND the weld is subjected to significant forces during impact
→ Weld failure check is REQUIRED

The check ensures welds do not fracture or tear during the crash event.
```

### 12.2 Method Selection

```
IF force resultants on the weld are known (from FEA or hand calculation):
    → Use FORCE-BASED check (simpler, Section 12.3)

IF stress components in the weld throat plane are known (from detailed FEA):
    → Use STRESS-BASED check (EN 1993-1-8, Section 12.4)

IF both are available:
    → Use STRESS-BASED (more rigorous) and verify with FORCE-BASED
```

### 12.3 Force-Based Weld Failure Check

**Procedure:**

```
1. Determine weld forces:
   F_n = normal force on weld [N] (perpendicular to weld axis)
   F_s = shear force on weld [N] (parallel to weld axis)

2. Calculate weld area:
   A_w = a × L_w [mm²]
   where a = throat thickness, L_w = effective weld length

3. Calculate stresses:
   σ_n = F_n / A_w [MPa]
   τ = F_s / A_w [MPa]

4. Calculate equivalent stress (von Mises):
   σ_eq = √(σ_n² + τ²) [MPa]

5. Calculate allowable stress:
   σ_allow = f_u / γ_Mw [MPa]
   where:
       f_u = ultimate tensile strength of weld metal [MPa]
       γ_Mw = partial safety factor (default 1.25)

6. Calculate utilization:
   U = σ_eq / σ_allow

7. PASS if U < 1.0, FAIL if U ≥ 1.0
```

### 12.4 Stress-Based Weld Failure Check (EN 1993-1-8)

**Procedure:**

```
1. Determine stress components in the weld throat plane:
   σ_⊥ = normal stress perpendicular to weld throat [MPa]
   τ_⊥ = shear stress perpendicular to weld throat (in throat plane) [MPa]
   τ_∥ = shear stress parallel to weld axis [MPa]

2. Check Criterion 1 (Combined stress):
   σ_eq = √(σ_⊥² + 3 × (τ_⊥² + τ_∥²)) [MPa]
   σ_allow,1 = f_u / (β_w × γ_Mw)
   U_1 = σ_eq / σ_allow,1

3. Check Criterion 2 (Normal stress limit):
   σ_allow,2 = 0.9 × f_u / γ_Mw
   U_2 = |σ_⊥| / σ_allow,2

4. Governing utilization:
   U = max(U_1, U_2)

5. PASS if U < 1.0, FAIL if U ≥ 1.0
```

**Parameter values:**

| Parameter | Value | Notes |
|-----------|-------|-------|
| β_w | 0.8 | Normal structural steels (S235–S460) |
| β_w | 0.85 | Austenitic stainless steels |
| β_w | 1.0 | Conservative (if steel grade unknown) |
| γ_Mw | 1.25 | Standard safety factor |
| γ_Mw | 1.0 | For crash/accidental design situations (Eurocode allows) |

**For crash (accidental) design situations:**
- Eurocode allows γ_Mw = 1.0 (partial factor removed for accidental actions)
- However, company or project-specific requirements may still require γ_Mw > 1.0

### 12.5 Dynamic vs. Static Weld Strength

```
IF weld failure check uses dynamic material properties:
    → Use f_u,dynamic = f_u × DIF_ultimate
    → Where DIF_ultimate is the dynamic increase factor for ultimate strength
    → CAUTION: DIF for ultimate strength is lower than DIF for yield
    → Conservative approach: use static f_u (do NOT increase for strain rate)
```

**Recommendation:** Use **static** f_u for weld failure checks unless dynamic testing data is available for the specific weld metal. This is conservative because:
1. Weld metal may not benefit from strain rate hardening as much as base metal
2. Weld defects can reduce dynamic ductility
3. Strain rate in the weld may differ from the global strain rate

---

## 13. Phase 3: Energy Absorption Assessment

### 13.1 When Is Energy Absorption Assessment Required?

```
IF the component is designed to absorb crash energy (crush zone, crash box, crumple zone)
    OR design specification includes minimum energy absorption
    OR force-displacement performance is specified
→ Energy absorption assessment is REQUIRED
```

### 13.2 Metrics and Formulas

| Metric | Symbol | Formula | Units | Target |
|--------|--------|---------|-------|--------|
| Total energy | E | ∫ F(δ) dδ | J | ≥ specification |
| Specific energy absorption | SEA | E / m | J/kg | Higher = better |
| Mean force | P_m | E / Δδ_total | N | ≥ specification |
| Peak force | P_max | max(F) | N | ≤ specification |
| Crush force efficiency | CFE | P_m / P_max | — | 0.6–0.8 typical, higher = better |

### 13.3 Procedure

```
1. Obtain force-displacement data:
   - From FEA crash simulation
   - From physical crash test
   - From design specification (synthetic curve)

2. Calculate all metrics:
   E = ∫ F(δ) dδ  (trapezoidal integration)
   P_m = E / δ_max
   P_max = max(F)
   CFE = P_m / P_max
   SEA = E / m_component  (if mass is known)

3. Check against requirements:

   | Requirement Type | Criterion | PASS if |
   |-----------------|-----------|---------|
   | Minimum energy | E ≥ E_required | Total energy meets spec |
   | Maximum peak force | P_max ≤ P_max,allowed | Occupant/payload protection |
   | Minimum SEA | SEA ≥ SEA_target | Weight-efficient design |
   | Minimum CFE | CFE ≥ CFE_target | Stable progressive crush |
```

### 13.4 Interpretation Guidelines

| CFE Range | Interpretation | Typical Structure |
|-----------|---------------|-------------------|
| < 0.4 | Unstable collapse, sharp force peaks | Monocoque without triggers |
| 0.4 – 0.6 | Moderate stability | Simple crush tubes |
| 0.6 – 0.8 | Good progressive crush | Well-designed crash boxes |
| > 0.8 | Excellent absorption efficiency | Foam-filled or multi-cell tubes |

---

# PART IV — FEA INTEGRATION

## 14. FEA Data Extraction for Fatigue

### 14.1 FEA Requirements by Assessment Method

| Method | Element Type | Element Size | Output Required | Stress Location |
|--------|-------------|-------------|-----------------|-----------------|
| Nominal stress | Shell or solid | Coarse (≥ 2t) | Section forces or far-field stress | Away from weld |
| Hot-spot stress | Shell or solid | ≈ t × t | Surface stress at 0.4t, 1.0t (Type A) or 5/15/25 mm (Type B) | Surface, perpendicular to weld toe |
| Notch stress | Solid only | ≈ r_ref/4 (≈0.25 mm) | Max principal stress at notch | At weld toe/root modeled with r_ref |
| Fracture mechanics | Solid only | Fine at crack tip | K or J-integral | Crack tip region |

### 14.2 Stress Tensor Processing

When FEA provides full stress tensor (σ_xx, σ_yy, σ_zz, τ_xy, τ_yz, τ_xz), extract the relevant stress measure:

```
Von Mises equivalent stress:
    σ_VM = √(0.5 × ((σ_xx-σ_yy)² + (σ_yy-σ_zz)² + (σ_zz-σ_xx)² + 6×(τ_xy²+τ_yz²+τ_xz²)))

Maximum principal stress:
    Eigenvalues of the stress tensor → σ₁ ≥ σ₂ ≥ σ₃
    Use σ₁ for fatigue if crack opens perpendicular to σ₁

Weld-local coordinate stress:
    Transform stress tensor to weld local axes:
    → σ_⊥ (perpendicular to weld), τ_⊥ (in-plane shear), τ_∥ (along weld)
    → Required for EN 1993-1-8 weld failure check
```

**Which stress measure to use:**

| Assessment Method | Stress Measure |
|------------------|---------------|
| Nominal stress method | Nominal stress (from section forces, not FEA stress at elements near weld) |
| Hot-spot method | Maximum principal stress on the surface, perpendicular to weld |
| Notch stress method | Maximum principal stress at the notch |
| Multiaxial fatigue | Both σ and τ components separately |
| Weld failure (EN 1993-1-8) | σ_⊥, τ_⊥, τ_∥ in weld throat coordinates |

### 14.3 Hot-Spot Extraction from FEA

```
1. Identify weld toe location in FE model
2. Define stress path perpendicular to weld toe (Type A) or along weld toe (Type B)
3. Extract surface stress at prescribed distances:
   Type A: 0.4t, 1.0t (linear) or 0.4t, 0.9t, 1.4t (quadratic)
   Type B: 5 mm, 15 mm, 25 mm
4. Apply extrapolation formula (Section 6.3)
5. Result: hot-spot stress range Δσ_hs
```

### 14.4 Supported FEA Solvers

| Solver | Reader | File Format | Notes |
|--------|--------|-------------|-------|
| Abaqus | AbaqusResultsReader | .odb, .dat | Standard Abaqus output |
| LS-DYNA | LSDynaResultsReader | ASCII d3plot, binout | Crash simulation |
| Nastran | NastranResultsReader | .f06, .pch | Linear/nonlinear |
| Generic CSV | GenericCSVReader | .csv | Any solver export |

---

## 15. FEA Data Extraction for Impact

### 15.1 Required FEA Outputs for Impact Assessment

| Output | Use | Extraction Location |
|--------|-----|---------------------|
| Plastic strain rate ε̇ | Dynamic yield calculation | Element at weld or critical section |
| Forces on weld | Weld failure check | Section forces at weld interface |
| Force-displacement curve | Energy absorption | Global or section response |
| Stress tensor at weld | Stress-based weld check | Elements in weld throat |
| Contact force | Peak force check | Interface between impactor and structure |

### 15.2 Strain Rate from FEA

```
IF FEA provides strain rate directly (LS-DYNA, Abaqus Explicit):
    → Use maximum strain rate at the location of interest

IF FEA provides strain-time history:
    → ε̇ = Δε / Δt at the time step of interest
    → Use peak strain rate for dynamic yield calculation

IF FEA does not provide strain rate:
    → Estimate from impact velocity and structure geometry:
    → ε̇ ≈ v_impact / L_structure [1/s]
    → This is approximate; FEA is preferred
```

---

# PART V — COMBINED ASSESSMENT AND REPORTING

## 16. Combined Fatigue + Impact Scenarios

### 16.1 When Does Combined Assessment Apply?

```
IF the component is subjected to BOTH:
    - Cyclic fatigue loading during service (e.g., road vibration, pressure cycles)
    - One or more impact events (e.g., crash, drop)
→ Combined assessment is REQUIRED

Typical examples:
    - EV battery enclosure: fatigue from road vibration + crash in collision
    - Hydrogen tank frame: pressure cycling + accidental impact
    - Chassis components: fatigue from road loads + crash integrity
```

### 16.2 Combined Assessment Procedure

```
STEP 1: Perform fatigue assessment (Part II)
    → Result: N_allow or D_total and PASS/FAIL

STEP 2: Perform impact assessment (Part III)
    → Result: Weld utilization, energy absorption, and PASS/FAIL

STEP 3: Check interaction:
    a. IF fatigue occurs BEFORE potential impact:
       → Fatigue damage may have propagated cracks that reduce impact resistance
       → Conservative approach: reduce f_u by (1 - D_total) for weld failure check
       → OR: use fracture mechanics to estimate crack size at time of impact

    b. IF impact occurs BEFORE fatigue service:
       → Impact may introduce residual stresses, geometric distortion, or micro-cracks
       → Conservative approach: assume initial crack a₀ = 1 mm for fracture mechanics
       → Or use reduced FAT class (one step down)

    c. IF both occur simultaneously or alternately:
       → Treat as most severe combination
       → Apply both checks independently with worst-case assumptions

STEP 4: Overall verdict:
    PASS only if BOTH fatigue AND impact checks pass individually
    AND interaction effects are accounted for
```

---

## 17. Reporting Requirements

### 17.1 Minimum Report Contents

Every fatigue and/or impact verification report must contain:

| Section | Contents |
|---------|----------|
| **1. Project Identification** | Project name, component ID, author, date, revision |
| **2. Scope** | What is being verified, loading cases, acceptance criteria |
| **3. Material Data** | Grade, yield, UTS, modulus, source (certificate / standard) |
| **4. Joint Description** | Weld type, geometry (t, a, p), process, quality level |
| **5. Loading Description** | Load type, stress ranges, R-ratio or spectrum, number of cycles |
| **6. Environmental Conditions** | Temperature, atmosphere, hydrogen (if applicable) |
| **7. Method Selection Justification** | Why this method was chosen (reference Section 6 decision tree) |
| **8. Standard and S-N Curve** | Which standard, which S-N curve parameters |
| **9. Modifier Chain** | Each factor applied, its value, and justification |
| **10. Calculation Results** | N_allow, D_total, safety factor, utilization |
| **11. PASS/FAIL Verdict** | Clear binary result with quantified margin |
| **12. Assumptions and Limitations** | Any simplifications, conservatisms, or limitations |
| **13. References** | Standards, specifications, reports referenced |

### 17.2 Report Formats

Two formats are supported:

- **PDF Report** (formal deliverable): Generated via `FatigueReport` class. Includes cover page, formatted tables, embedded plots (S-N curves, Haigh diagrams, crack growth).
- **HTML Report** (interactive review): Generated via `HTMLReportGenerator`. Includes interactive plots, filterable tables.

---

# PART VI — DECISION TREES AND QUICK REFERENCE

## 18. Master Decision Tree — Which Method to Use

### 18.1 Complete Method Selection Flowchart

```
╔══════════════════════════════════════════════════════════════════════╗
║                  WELDED STRUCTURE VERIFICATION                       ║
║                  START HERE                                           ║
╚══════════════════════════════════════════════════════════════════════╝
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
  ┌──────────┐         ┌──────────┐         ┌──────────────┐
  │ FATIGUE  │         │  IMPACT  │         │  COMBINED    │
  │ loading  │         │  loading │         │  fatigue +   │
  │ (cyclic) │         │ (crash)  │         │  impact      │
  └────┬─────┘         └────┬─────┘         └──────┬───────┘
       │                    │                      │
       ▼                    ▼                      ▼
  ┌──────────────┐   ┌──────────────┐    Do BOTH branches
  │ Uniaxial or  │   │ Dynamic      │    independently, then
  │ multiaxial?  │   │ material     │    check interaction
  └──┬───────┬───┘   │ (Sec. 11)   │    (Section 16)
     │       │        └──────┬──────┘
     ▼       ▼               │
  ┌─────┐ ┌───────┐    ┌────┴────────┐
  │ UNI │ │ MULTI │    │ Weld failure│
  │     │ │ AXIAL │    │ (Sec. 12)   │
  └──┬──┘ └───┬───┘    └──────┬──────┘
     │        │               │
     ▼        ▼          ┌────┴──────┐
  ┌────────┐ See 10.1    │ Energy    │
  │ FEA    │             │ absorption│
  │ avail? │             │ (Sec. 13) │
  └─┬────┬─┘             └───────────┘
    │    │
    ▼    ▼
  YES    NO
    │    │
    ▼    ▼
  ┌────┐ ┌────────────┐
  │Fine│ │ Can calc   │
  │mesh│ │ nominal σ? │
  │?   │ └──┬─────┬───┘
  └┬─┬─┘   ▼     ▼
   │ │    YES    NO
   │ │     │     │
   ▼ ▼     ▼     ▼
  ┌──┐ ┌──┐ ┌───────┐ ┌──────────┐
  │r=│ │t │ │NOMINAL│ │ FEA      │
  │1 │ │×t│ │STRESS │ │ required │
  │mm│ │  │ │       │ │ → re-    │
  └┬─┘ └┬─┘ └───────┘ │ enter   │
   │    │              └──────────┘
   ▼    ▼
 NOTCH  HOTSPOT
 STRESS STRESS
```

### 18.2 Loading-Based Decision Matrix

| Loading | Amplitude | Directionality | Method |
|---------|-----------|---------------|--------|
| Cyclic | Constant | Uniaxial | Nominal / Hot-spot / Notch + direct S-N lookup |
| Cyclic | Variable | Uniaxial | Same method + Palmgren-Miner damage |
| Cyclic | Constant | Multiaxial, proportional | Primary method + Gough-Pollard |
| Cyclic | Constant | Multiaxial, non-proportional | Primary method + Findley / MWCM |
| Cyclic | Variable | Multiaxial | Primary method + Miner + Multiaxial criterion |
| Random vibration | PSD input | Uniaxial | Vibration fatigue (Dirlik / narrowband) |
| Random vibration | PSD input | Multiaxial | Advanced (outside standard scope) |
| Impact | Single event | — | Cowper-Symonds/J-C + weld failure + energy |
| Mixed | Fatigue + impact | — | Both assessments + interaction |

### 18.3 Weld Configuration Decision Matrix

| Weld Type | Primary Failure Mode | Recommended Method | Root Check Needed? |
|-----------|---------------------|-------------------|-------------------|
| Butt, full penetration | Toe crack | Nominal (if cataloged) or hot-spot | No |
| Butt, partial penetration | Toe or root | Notch or nominal + root check | YES |
| Fillet, non-load-carrying | Toe crack | Nominal or hot-spot (FAT 80) | No |
| Fillet, load-carrying | Toe or root | Nominal + root check | YES |
| Cruciform, full penetration | Toe crack | Nominal or hot-spot | No |
| Cruciform, partial | Toe or root | Nominal + root check | YES |
| Lap joint | Toe or root | Nominal (FAT 45–71) + root check | YES |
| T-joint | Toe crack | Nominal or hot-spot | Depends on penetration |
| Stiffener | Toe crack | Nominal (FAT depends on length) | No |
| Spot weld | Nugget edge | Special methods (outside standard scope) | N/A |
| Laser butt | Toe or root | Notch stress (narrow bead) | Possible |
| FSW butt | Retreating side | Nominal + process factor | No |

---

## 19. Quick Reference Tables

### 19.1 FAT Class Quick Lookup (Steel, IIW)

| Weld Detail | Tension FAT | Bending FAT |
|-------------|------------|-------------|
| Base material, rolled surface | 160 | 160 |
| Base material, flame-cut edges | 140 | 140 |
| Transverse butt, ground flush, NDT | 125 | 125 |
| Transverse butt, ground flush | 112 | 112 |
| Transverse butt, as-welded (both sides) | 100 | 100 |
| Transverse butt, one-side, full pen. | 90 | 90 |
| Transverse butt, on backing bar | 71 | 71 |
| Non-load-carrying fillet, transverse | 80 | 80 |
| Load-carrying fillet, longitudinal | 71 | 71 |
| Cruciform, full penetration K-butt | 90 | 90 |
| Cruciform, load-carrying fillet | 71 | 71 |
| Cruciform, partial penetration | 63 | 63 |
| Lap joint, fillet welds | 45–63 | 45–63 |

### 19.2 Environmental Factors Quick Reference

| Condition | Steel Factor | Aluminum Factor |
|-----------|-------------|-----------------|
| Air, 20°C | 1.0 | 1.0 |
| Seawater (free) | 0.7 | 0.6 |
| Seawater (CP) | 0.85 | 0.8 |
| Industrial | 0.9 | 0.85 |
| Hydrogen (50 bar) | 0.91 | 1.0 |
| Hydrogen (200 bar) | 0.71 | 1.0 |
| Hydrogen (350 bar) | 0.59 | 1.0 |
| 150°C (steel) | 0.925 | N/A |
| 200°C (steel) | 0.85 | N/A |
| 300°C (steel) | 0.70 | N/A |
| 100°C (aluminum) | N/A | 0.85 |
| -50°C (carbon steel) | 0.8 | 1.0 |

### 19.3 Safety Factor Quick Reference

| Standard | Consequence | Inspection | γ_Mf |
|----------|------------|------------|------|
| IIW | Normal | Periodic | 1.15 |
| IIW | High | None | 1.40 |
| EC3 | Normal | — | 1.15 |
| EC3 | High | — | 1.35 |
| DNV | Normal | Periodic | DFF = 2.0 |
| DNV | High | None | DFF = 10.0 |

---

## 20. Checklist for Complete Verification

Use this checklist to ensure no step is missed:

### 20.1 Fatigue Verification Checklist

- [ ] **Material data** collected (grade, R_y, R_m, E, material family)
- [ ] **Weld classification** completed (WeldType, geometry: t, a, p, L)
- [ ] **Loading classified** (CA/VA, uniaxial/multiaxial, load type)
- [ ] **Stress calculated** (nominal, hot-spot, or notch)
- [ ] **Assessment method selected** and justified (Section 6 decision tree)
- [ ] **FAT class selected** (from catalog or quality-level table)
- [ ] **S-N curve and standard selected** (Section 7)
- [ ] **Thickness correction** applied (if t > 25 mm)
- [ ] **Environmental correction** applied (if non-air environment)
- [ ] **Post-weld treatment** accounted for (if applied)
- [ ] **Weld process factor** applied (if non-MIG/MAG)
- [ ] **Misalignment** accounted for (if present)
- [ ] **Mean stress correction** applied (if PWHT and R ≠ 0)
- [ ] **Safety factors** applied (γ_Mf, γ_Ff, survival probability)
- [ ] **Damage calculated** (N_allow for CA, D_total for VA)
- [ ] **Root fatigue checked** (if partial penetration)
- [ ] **Multiaxial checked** (if combined σ + τ)
- [ ] **PASS/FAIL determined** with quantified safety margin
- [ ] **Report generated** with all required sections

### 20.2 Impact Verification Checklist

- [ ] **Material data** collected (including Cowper-Symonds or J-C parameters)
- [ ] **Strain rate estimated** (from FEA or impact velocity)
- [ ] **Strain rate model selected** (Cowper-Symonds or Johnson-Cook)
- [ ] **Dynamic yield calculated** (DIF × σ_static)
- [ ] **Weld forces/stresses** determined (from FEA)
- [ ] **Weld failure check** performed (force-based and/or stress-based)
- [ ] **Energy absorption** calculated (if applicable: E, SEA, P_m, P_max, CFE)
- [ ] **All criteria met** (utilization < 1, energy ≥ spec, P_max ≤ spec)
- [ ] **PASS/FAIL determined** for each criterion
- [ ] **Report generated** with all required sections

### 20.3 Combined Assessment Checklist

- [ ] Fatigue assessment completed → PASS/FAIL
- [ ] Impact assessment completed → PASS/FAIL
- [ ] Interaction effects considered (Section 16.2)
- [ ] Overall verdict: PASS only if both pass AND interaction is acceptable

---

# ANNEXES

## Annex A: FAT Class Catalog

The complete FAT class catalog is maintained in the tool's data files:
- Steel: `src/weldfatigue/fatigue/data/fat_catalog_steel.json`
- Aluminum: `src/weldfatigue/fatigue/data/fat_catalog_aluminum.json`

Consult IIW XIII-2259-15 (2024) Tables 4.1–4.8 for the full catalog with illustrations.

## Annex B: Material Database Summary

### Steel Grades

| Grade | Standard | R_y [MPa] | R_m [MPa] | E [GPa] | CS D [1/s] | CS q |
|-------|----------|-----------|-----------|---------|----------|------|
| DC04 | EN 10130 | 210 | 310 | 210 | 40.4 | 5.0 |
| DP600 | EN 10338 | 350 | 600 | 210 | 100.0 | 4.73 |
| DP780 | EN 10338 | 480 | 780 | 210 | 200.0 | 4.5 |
| DP980 | EN 10338 | 600 | 980 | 210 | 300.0 | 4.0 |
| HSLA340 | EN 10268 | 340 | 410 | 210 | 80.0 | 4.8 |
| HSLA420 | EN 10268 | 420 | 480 | 210 | 120.0 | 4.5 |
| 22MnB5 | EN 10083 | 1000 | 1500 | 210 | 802.0 | 3.585 |
| S355J2 | EN 10025 | 355 | 510 | 210 | 40.4 | 5.0 |
| 316L | EN 10088 | 220 | 520 | 200 | 100.0 | 10.0 |

### Aluminum Grades

| Grade | Standard | R_y [MPa] | R_m [MPa] | E [GPa] | CS D [1/s] | CS q |
|-------|----------|-----------|-----------|---------|----------|------|
| 6061-T6 | EN 573 | 276 | 310 | 70 | 6500 | 4.0 |
| 6082-T6 | EN 573 | 260 | 310 | 70 | 6500 | 4.0 |
| 5083-H111 | EN 573 | 165 | 275 | 70 | 6500 | 4.0 |
| 5754-O | EN 573 | 100 | 190 | 70 | 6500 | 4.0 |
| 7075-T6 | EN 573 | 503 | 572 | 72 | 6500 | 4.0 |

## Annex C: Formula Summary

### C.1 Core S-N Relationship
```
N = (FAT / Δσ)^m × N_ref

Δσ = FAT × (N_ref / N)^(1/m)

N_ref = 2 × 10⁶ (IIW)
```

### C.2 Palmgren-Miner Damage
```
D = Σ(n_i / N_i)

Failure: D ≥ D_limit (1.0 standard, 0.5 safety-critical)
```

### C.3 Equivalent Stress Range
```
Δσ_eq = [Σ(n_i × Δσ_i^m) / Σn_i]^(1/m)
```

### C.4 Hot-Spot Extrapolation
```
Type A linear:    σ_hs = 1.67 × σ(0.4t) - 0.67 × σ(1.0t)
Type A quadratic: σ_hs = 2.52 × σ(0.4t) - 2.24 × σ(0.9t) + 0.72 × σ(1.4t)
Type B:           σ_hs = 3 × σ(5mm) - 3 × σ(15mm) + σ(25mm)
```

### C.5 Thickness Correction
```
f(t) = (25 / t)^n    for t > 25 mm
```

### C.6 Cowper-Symonds Dynamic Yield
```
σ_dyn = σ_static × [1 + (ε̇ / D)^(1/q)]
```

### C.7 Johnson-Cook Flow Stress
```
σ = (A + B × εₚⁿ) × (1 + C × ln(ε̇/ε̇₀)) × (1 - T*ᵐ)
```

### C.8 Weld Failure (EN 1993-1-8)
```
Criterion 1: √(σ_⊥² + 3(τ_⊥² + τ_∥²)) ≤ f_u / (β_w × γ_Mw)
Criterion 2: |σ_⊥| ≤ 0.9 × f_u / γ_Mw
```

### C.9 Paris Law Crack Growth
```
da/dN = C × (ΔK)^m
ΔK = Y × Mk × Δσ × √(π × a)
```

### C.10 Gough-Pollard Interaction
```
(Δσ / Δσ_R)² + (Δτ / Δτ_R)² ≤ 1
```

### C.11 Dirlik Spectral Moments
```
m_n = ∫ f^n × G(f) df    (n = 0, 1, 2, 4)
γ = m₂ / √(m₀ × m₄)     [irregularity factor]
```

### C.12 Energy Absorption Metrics
```
E = ∫ F dδ
SEA = E / m
P_m = E / δ_max
CFE = P_m / P_max
```

## Annex D: Worked Examples

### D.1 Example: Constant Amplitude Fatigue of a Butt Weld

**Given:**
- Material: S355J2 steel (R_y = 355 MPa, R_m = 510 MPa)
- Weld type: Transverse butt weld, as-welded both sides
- Loading: Constant amplitude tension, Δσ = 80 MPa, R = 0.1
- Design life: N = 2 × 10⁶ cycles
- Environment: Air, 20 °C
- Quality level: C
- Plate thickness: 12 mm
- No post-weld treatment
- Consequence: Normal, periodic inspection

**Solution:**

```
Step 1: FAT class selection
    Quality level C, butt weld → FAT 90 (from Table, Section 8.5)

Step 2: Modifier chain
    Thickness: t = 12 mm < 25 mm → f_thick = 1.0
    Environment: Air, 20°C → f_env = 1.0
    Treatment: None → f_pwt = 1.0 (no upgrade)
    Process: MIG/MAG → f_proc = 1.0
    Mean stress: As-welded → f(R) = 1.0 (no correction per IIW)
    Misalignment: None specified → k_m = 1.0
    Safety factor: Normal consequence, periodic → γ_Mf = 1.15
    Load factor: γ_Ff = 1.0
    Survival: 97.7% → f_surv = 1.0

    FAT_design = 90 × 1.0 × 1.0 × 1.0 × 1.0 × 1.0 / 1.15 = 78.3 MPa

Step 3: Calculate allowable cycles
    N_allow = (78.3 / 80)^3 × 2×10⁶ = 1.87 × 10⁶ cycles

Step 4: Check
    N_allow = 1.87 × 10⁶ < N_required = 2 × 10⁶

    → FAIL (marginal)

Step 5: Safety factor
    SF = (1.87 × 10⁶ / 2 × 10⁶)^(1/3) = 0.977
    SF < 1.0 → Confirms FAIL

Recommendation:
    → Upgrade quality to level B (FAT 112) or apply HFMI treatment
    → With quality B: FAT_design = 112/1.15 = 97.4 MPa
      N_allow = (97.4/80)^3 × 2×10⁶ = 3.60 × 10⁶ → PASS (SF = 1.22)
```

### D.2 Example: Impact Assessment of a Crash Box Weld

**Given:**
- Material: DP600 (R_y = 350 MPa, R_m = 600 MPa)
- Cowper-Symonds: D = 100 /s, q = 4.73
- Strain rate at weld: 200 /s
- Weld: Fillet weld, a = 4 mm, L = 80 mm
- Normal force on weld: 40 000 N
- Shear force on weld: 25 000 N
- Allowable stress (weld metal): 480 MPa

**Solution:**

```
Step 1: Dynamic yield
    DIF = 1 + (200 / 100)^(1/4.73) = 1 + 2^0.211 = 1 + 1.159 = 2.159
    σ_y,dyn = 350 × 2.159 = 755.7 MPa

Step 2: Weld failure check (force-based)
    A_w = 4 × 80 = 320 mm²
    σ_n = 40000 / 320 = 125.0 MPa
    τ = 25000 / 320 = 78.1 MPa
    σ_eq = √(125² + 78.1²) = 147.4 MPa
    σ_allow = 480 / 1.25 = 384 MPa    (static, conservative)
    U = 147.4 / 384 = 0.384

    → PASS (utilization = 38.4%, significant margin)
```

---

## Document History

| Revision | Date | Description |
|----------|------|-------------|
| Rev.0 | 2026-03-02 | Initial release — complete methodology |

---

*This methodology document is based on the WeldFatigue toolset (v0.1.0) and aligns with all implemented assessment methods, correction factors, and standards. Each step in this methodology corresponds to a function or class in the codebase, ensuring full traceability between the documented procedure and its computational implementation.*
