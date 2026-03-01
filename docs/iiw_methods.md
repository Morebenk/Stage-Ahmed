# IIW Fatigue Assessment Methods

This document describes the three IIW (International Institute of Welding) fatigue assessment methods implemented in WeldFatigue, following the IIW recommendations for fatigue design of welded joints and components (Hobbacher, 2016).

---

## 1. S-N Curve Fundamentals

All IIW methods are based on the S-N (Wöhler) curve, relating stress range Δσ to the number of cycles to failure N.

### Basic Equation

```
N = (FAT / Δσ)^m × 2×10⁶
```

Where:
- **FAT** = characteristic fatigue strength at N = 2×10⁶ cycles [MPa]
- **Δσ** = applied stress range [MPa]
- **m** = slope exponent
- **N** = number of cycles to failure

### Bilinear S-N Curve (Steel)

| Region | Cycles | Slope m |
|--------|--------|---------|
| Below knee point | N < 10⁷ | m = 3 |
| Above knee (variable amplitude) | N ≥ 10⁷ | m = 5 |
| Constant amplitude fatigue limit | N = 5×10⁶ | Cutoff (infinite life) |
| Cut-off limit (variable amplitude) | N = 10⁸ | Absolute cutoff |

### Aluminum Parameters

| Region | Slope m |
|--------|---------|
| Below knee | m = 3.5 |
| Above knee | m = 5.5 |
| Knee point | N = 5×10⁶ |

### Knee Point Stress

The stress at the knee point is:

```
Δσ_knee = FAT × (2×10⁶ / N_knee)^(1/m₁)
```

---

## 2. Nominal Stress Method

**Simplest and most widely used method.**

### Principle
Compare the nominal stress range (calculated from section forces, away from stress concentrations) against the appropriate FAT class for the weld detail.

### Procedure

1. Calculate nominal stress range Δσ_nom from applied loading
2. Select the appropriate FAT class from the IIW catalog (based on weld type, load direction, and material)
3. Determine allowable cycles N from the S-N curve
4. Check: N_allowable ≥ N_applied → PASS

### FAT Class Selection

The FAT class depends on:
- **Weld type:** butt, fillet, T-joint, cruciform, etc.
- **Loading:** tension, bending, shear
- **Material:** steel or aluminum
- **Quality level and geometry**

Common steel FAT classes:
| Detail | FAT |
|--------|-----|
| Ground butt weld | 112 |
| Butt weld, good quality | 80-90 |
| Fillet weld, toe failure | 63-71 |
| Cruciform joint | 36-56 |

### Mean Stress Correction

For non-zero mean stress, the equivalent stress amplitude is corrected:

**Goodman:**
```
Sa_eq = Sa / (1 - Sm/Su)
```

**Gerber:**
```
Sa_eq = Sa / (1 - (Sm/Su)²)
```

**IIW Enhancement Factor f(R):**
- As-welded: f(R) = 1.0 (no correction needed due to residual stresses)
- Stress-relieved:
  - R < -1: f(R) = 1.6
  - -1 ≤ R ≤ 0.5: f(R) = -0.4R + 1.2
  - R > 0.5: f(R) = 1.0

---

## 3. Structural Hot-Spot Stress Method

**Uses surface stress extrapolation to account for geometric stress concentration.**

### Principle
The structural (hot-spot) stress is determined by extrapolating surface stresses to the weld toe, excluding the local notch effect but including the structural stress concentration.

### Type a — Linear Extrapolation (Plate Surface)

Reference points at 0.4t and 1.0t from the weld toe (t = plate thickness):

```
σ_hs = 1.67 × σ(0.4t) - 0.67 × σ(1.0t)
```

Fine mesh quadratic extrapolation (reference points at 0.4t, 0.9t, 1.4t):

```
σ_hs = 2.52 × σ(0.4t) - 2.24 × σ(0.9t) + 0.72 × σ(1.4t)
```

### Type b — 3-Point Extrapolation (Along Plate Edge)

Reference points at fixed distances (5mm, 15mm, 25mm):

```
σ_hs = 3 × σ(5mm) - 3 × σ(15mm) + σ(25mm)
```

### FAT Classes for Hot-Spot Method

Typical hot-spot FAT classes for steel:
- Butt weld: FAT 100
- Fillet weld (toe crack): FAT 90-100
- Load-carrying fillet: FAT 90

### FEA Requirements

- Mesh size: ≤ t × t (element size roughly equal to plate thickness)
- Stress must be read at surface nodes
- Path perpendicular to weld toe

---

## 4. Effective Notch Stress Method

**Most general method — applicable to all weld geometries.**

### Principle
Model the weld toe and root with a reference radius (r_ref) and compute the elastic notch stress. Use a single, universal FAT class.

### Reference Radius

| Condition | r_ref |
|-----------|-------|
| Standard plates (t ≥ 5mm) | 1.0 mm |
| Thin sheets (t < 5mm) | 0.05 mm |

### FAT Classes

| Material | FAT Class |
|----------|-----------|
| Steel | **225** |
| Aluminum | **71** |

### Procedure

1. Create FE model with reference radius at weld toe/root
2. Extract maximum principal or von Mises stress at the notch
3. This is the effective notch stress Δσ_notch
4. Check against FAT 225 (steel) or FAT 71 (aluminum) S-N curve

### Advantages
- No need to classify weld details
- Captures local geometry effects
- Works for complex joint configurations

### Limitations
- Requires fine FE mesh at notch (element size ≈ r_ref/4)
- Not applicable to root failures in load-carrying fillet welds without modeling the gap

---

## 5. Cumulative Damage (Palmgren-Miner Rule)

For variable amplitude loading, damage from each load block accumulates linearly:

```
D = Σ (ni / Ni)
```

Where:
- ni = number of applied cycles at stress range Δσi
- Ni = allowable cycles at Δσi from the S-N curve
- Failure criterion: D ≥ 1.0

### Variable Amplitude S-N Curve

For variable amplitude loading, the S-N curve extends beyond the knee point with a reduced slope (m₂ = 5 for steel, m₂ = 5.5 for aluminum), allowing low-amplitude cycles to contribute to damage.

### Equivalent Stress Range

The equivalent constant amplitude stress range that produces the same damage:

```
Δσ_eq = [Σ(ni × Δσi^m) / Σ(ni)]^(1/m)
```

---

## 6. References

1. Hobbacher, A.F. (2016). *Recommendations for Fatigue Design of Welded Joints and Components.* IIW document IIW-2259-15 ex XIII-2460-13/XV-1440-13. Springer.
2. Eurocode 3: EN 1993-1-9 — Fatigue design of steel structures
3. Eurocode 9: EN 1999-1-3 — Fatigue design of aluminium structures
4. EN 1993-1-8 — Design of steel structures: Design of joints
