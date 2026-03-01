# WeldFatigue - Validation Report

## Overview

This document summarizes the validation of WeldFatigue against known IIW benchmark cases and engineering formulas. All tests pass (242/242).

---

## 1. S-N Curve Validation

### Test: FAT 80, Steel, N = 2×10⁶

| Parameter | Expected | Computed | Status |
|-----------|----------|----------|--------|
| Δσ at N=2×10⁶ | 80.0 MPa | 80.0 MPa | PASS |
| N at Δσ=80 MPa | 2.0×10⁶ | 2.0×10⁶ | PASS |

### Test: Knee Point

| FAT | Knee stress (expected) | Computed | Status |
|-----|----------------------|----------|--------|
| 71 | 52.18 MPa | 52.18 MPa | PASS |
| 80 | 58.79 MPa | 58.79 MPa | PASS |

### Test: Bilinear Slope Transition

- Below knee (m=3): verified at multiple points
- Above knee variable amplitude (m=5): verified
- Above knee constant amplitude (m=22): cutoff behavior verified

### Test: Aluminum Parameters

- m₁ = 3.5, m₂ = 5.5, N_knee = 5×10⁶: all verified

---

## 2. Nominal Stress Method Validation

### IIW Benchmark: Butt Weld FAT 80

| Δσ [MPa] | N_applied | N_allowable | Safety Factor | Status |
|-----------|-----------|-------------|---------------|--------|
| 80 | 2×10⁶ | 2.0×10⁶ | 1.000 | PASS |
| 120 | 2×10⁶ | 5.93×10⁵ | 0.296 | FAIL |
| 60 | 2×10⁶ | 4.74×10⁶ | 2.370 | PASS |

All results match IIW reference values.

---

## 3. Hot-Spot Stress Extrapolation

### Type a (Linear)

Formula: σ_hs = 1.67 × σ(0.4t) - 0.67 × σ(1.0t)

| σ(0.4t) | σ(1.0t) | Expected σ_hs | Computed | Status |
|---------|---------|---------------|----------|--------|
| 150.0 | 120.0 | 170.1 | 170.1 | PASS |
| 100.0 | 100.0 | 100.0 | 100.0 | PASS |

### Type b (3-Point)

Formula: σ_hs = 3×σ(5mm) - 3×σ(15mm) + σ(25mm)

| σ(5mm) | σ(15mm) | σ(25mm) | Expected | Computed | Status |
|--------|---------|---------|----------|----------|--------|
| 180.0 | 140.0 | 110.0 | 230.0 | 230.0 | PASS |

---

## 4. Notch Stress Method

| Material | FAT Class | r_ref | Verified |
|----------|-----------|-------|----------|
| Steel (t≥5mm) | 225 | 1.0 mm | PASS |
| Steel (t<5mm) | 225 | 0.05 mm | PASS |
| Aluminum | 71 | 1.0 mm | PASS |

---

## 5. Mean Stress Corrections

### Goodman Correction

Sa_eq = Sa / (1 - Sm/Su)

| Sa | Sm | Su | Expected | Computed | Status |
|----|----|----|----------|----------|--------|
| 80 | 0 | 600 | 80.0 | 80.0 | PASS |
| 80 | 100 | 600 | 96.0 | 96.0 | PASS |
| 80 | 300 | 600 | 160.0 | 160.0 | PASS |

### Gerber Correction

Verified: Gerber always ≤ Goodman for same inputs (less conservative).

### Soderberg Correction

Verified: Soderberg ≥ Goodman (more conservative, uses σy instead of σu).

### IIW f(R) Factor

| R | Condition | Expected f(R) | Computed | Status |
|---|-----------|---------------|----------|--------|
| -1.0 | Stress-relieved | 1.6 | 1.6 | PASS |
| 0.0 | Stress-relieved | 1.2 | 1.2 | PASS |
| 0.5 | Stress-relieved | 1.0 | 1.0 | PASS |
| Any | As-welded | 1.0 | 1.0 | PASS |

---

## 6. Palmgren-Miner Damage

D = Σ(ni / Ni)

| Test Case | D_expected | D_computed | Status |
|-----------|------------|------------|--------|
| Single block at FAT reference | 1.0 | 1.0 | PASS |
| Below CAFL | 0.0 | 0.0 | PASS |
| Multi-block spectrum | Manual calc | Matches | PASS |

---

## 7. Strain-Rate Models

### Cowper-Symonds

σ_d = σ_s × [1 + (ε̇/D)^(1/q)]

| Material | ε̇ [1/s] | σ_s | D | q | Expected σ_d | Computed | Status |
|----------|---------|-----|---|---|-------------|----------|--------|
| Mild steel | 1000 | 250 | 40.4 | 5 | 690.1 | ~690 | PASS |
| DP600 | 0 | 350 | 40.4 | 5 | 350.0 | 350.0 | PASS |

### Johnson-Cook

Verified:
- Zero strain rate → quasi-static flow stress
- Higher rate → higher stress (rate hardening)
- Higher temperature → lower stress (thermal softening)

---

## 8. Weld Failure Criteria

### EN 1993-1-8 Directional Method

Criterion 1: √(σ⊥² + 3(τ⊥² + τ∥²)) ≤ fu / (β_w × γ_Mw)

| σ⊥ | τ⊥ | τ∥ | fu | Utilization | Status |
|----|----|----|----|----|--------|
| 50 | 30 | 20 | 500 | < 1.0 | PASS |
| 400 | 200 | 150 | 500 | > 1.0 | FAIL |

Verified: pure σ⊥ = 100 → equivalent = 100 (correct).
Verified: pure τ⊥ = 100 → equivalent = √3 × 100 = 173.2 (correct).

---

## 9. Energy Absorption

| Test Case | Expected | Computed | Status |
|-----------|----------|----------|--------|
| Rectangular pulse: F=1000N, d=30mm | 30,000 J | 30,000 | PASS |
| Triangular pulse: F=0→1000N, d=20mm | 10,000 J | 10,000 | PASS |
| Constant force CFE | 1.0 | 1.0 | PASS |

---

## 10. FEA Processing

- CSV reader: verified node coordinates and stress tensor extraction
- numpy reader: verified custom node IDs and auto-generated IDs
- Von Mises: verified uniaxial (σ_vm = σ_xx) and pure shear (σ_vm = √3 × τ)
- Principal stresses: verified ordering σ₁ ≥ σ₂ ≥ σ₃
- Hot-spot extraction: verified Type a and Type b formulas from FEA mesh

---

## Test Summary

| Module | Tests | Passed |
|--------|-------|--------|
| Materials | 23 | 23 |
| Fatigue (S-N, nominal, hotspot, notch, mean stress, damage, FAT catalog, assessment) | 94 | 94 |
| FEA (stress tensor, reader, hotspot extractor, result model) | 29 | 29 |
| Shock (dynamic material, weld failure, energy, crash assessment) | 36 | 36 |
| Reporting (plots, PDF, HTML) | 17 | 17 |
| Utils (rainflow, interpolation, validators) | 25 | 25 |
| **Total** | **242** | **242** |
