# WeldFatigue - Architecture

## Overview

WeldFatigue is a Python library for validating the fatigue resistance and shock resistance of welded metal assemblies, following IIW (International Institute of Welding) recommendations. It targets automotive applications at OPmobility C-Power: EV battery enclosures, hydrogen tank frames, and structural reinforcements.

## Module Architecture

```
src/weldfatigue/
├── core/              Foundation layer (schemas, enums, exceptions, units)
├── materials/         Material database (steel + aluminum grades, strain-rate models)
├── fatigue/           IIW fatigue assessment engine
├── shock/             Crash/shock analysis
├── fea/               FEA result processing
├── reporting/         PDF + HTML report generation
└── utils/             Rainflow counting, interpolation, validators
```

## Layer Diagram

```
┌─────────────────────────────────────────────────┐
│                 Streamlit UI (app/)             │
├─────────────────────────────────────────────────┤
│          Orchestrators (assessment.py,          │
│          crash_assessment.py)                   │
├──────────┬──────────┬───────────┬───────────────┤
│ fatigue/ │  shock/  │   fea/    │  reporting/   │
│ S-N      │ dynamic  │ readers   │  PDF / HTML   │
│ nominal  │ weld     │ stress    │  plots        │
│ hotspot  │ energy   │ hotspot   │               │
│ notch    │          │ extractor │               │
│ damage   │          │           │               │
├──────────┴──────────┴───────────┴───────────────┤
│         materials/ (database, strain_rate)      │
├─────────────────────────────────────────────────┤
│         core/ (schemas, enums, exceptions)      │
└─────────────────────────────────────────────────┘
```

## Core Module (`core/`)

| File | Purpose |
|------|---------|
| `schemas.py` | Pydantic data models (FatigueInput, FatigueResult, CrashResult, etc.) |
| `enums.py` | Type-safe enumerations (WeldType, LoadType, MaterialFamily, AssessmentMethod) |
| `exceptions.py` | Exception hierarchy (MaterialNotFoundError, InvalidFATClassError, etc.) |
| `units.py` | Unit conversion helpers (MPa↔ksi, mm↔inch) |

## Materials Module (`materials/`)

Manages a JSON-backed database of steel and aluminum grades with mechanical properties and strain-rate model parameters.

**Grades included:**
- **Steel (9):** DC04, DP600, DP780, DP980, HSLA340, HSLA420, 22MnB5, S355J2, 316L
- **Aluminum (5):** 6061-T6, 6082-T6, 5083-H111, 5754-O, 7075-T6

**Key classes:**
- `MaterialDatabase` — Load, query, search, filter grades
- `cowper_symonds_yield()` — Compute dynamic yield at a given strain rate
- `johnson_cook_flow_stress()` — Full J-C constitutive model

## Fatigue Module (`fatigue/`)

Implements all three IIW fatigue assessment methods:

1. **Nominal Stress** (`nominal_stress.py`) — Simplest method, uses weld detail FAT class
2. **Hot-Spot Stress** (`hotspot_stress.py`) — Structural stress extrapolation (Type a and b)
3. **Effective Notch Stress** (`notch_stress.py`) — r_ref = 1mm, single FAT 225 (steel) / FAT 71 (aluminum)

Supporting modules:
- `sn_curve.py` — IIW bilinear S-N curve with knee point handling
- `fat_classes.py` — FAT class catalog loaded from JSON
- `mean_stress.py` — Goodman, Gerber, Soderberg + IIW f(R)
- `damage.py` — Palmgren-Miner cumulative damage rule
- `assessment.py` — Top-level orchestrator that coordinates all methods

## Shock Module (`shock/`)

- `dynamic_material.py` — DynamicMaterialModel wrapping Cowper-Symonds and Johnson-Cook
- `weld_failure.py` — Force-based and stress-based (EN 1993-1-8) weld failure checks
- `energy.py` — Energy absorption metrics (SEA, CFE, Pm, Pmax)
- `crash_assessment.py` — Orchestrator for crash analysis

## FEA Module (`fea/`)

- `result_model.py` — Solver-agnostic FEAResult container
- `stress_tensor.py` — Von Mises, principal, max shear, hydrostatic, weld-local transform
- `generic_reader.py` — CSV / numpy / DataFrame reader
- `hotspot_extractor.py` — Surface stress extrapolation from nodal results
- `lsdyna_reader.py`, `abaqus_reader.py`, `nastran_reader.py` — Solver-specific parsers

## Reporting Module (`reporting/`)

- `plots.py` — matplotlib (for PDF) + plotly (for Streamlit) chart generators
- `pdf_report.py` — Professional PDF generation via fpdf2
- `html_report.py` — HTML reports via Jinja2 templates

## Data Flow

```
User Input → Material Lookup → FAT Class Selection → Method Dispatch
    ↓
[Nominal / Hot-Spot / Notch] → S-N Curve → Allowable Cycles
    ↓
Mean Stress Correction (optional) → Miner Damage (if VA) → Result
    ↓
Report Generation (PDF / HTML)
```

## Dependencies

| Package | Role |
|---------|------|
| numpy, scipy | Numerical computation |
| pandas | Data handling |
| pydantic | Input/output schemas |
| matplotlib, plotly | Charting |
| fpdf2 | PDF reports |
| jinja2 | HTML reports |
| streamlit | Web UI |
| loguru | Logging |

## Testing

- **242 tests** across all modules
- Tests validate against IIW published benchmark values
- Run with: `pytest tests/ -v`
