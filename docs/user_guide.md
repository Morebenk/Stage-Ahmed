# WeldFatigue - User Guide

## Installation

```bash
# Clone and install in development mode
cd STAGE
pip install -e ".[dev]"
```

Required Python version: 3.10+

## Quick Start

### Python API

```python
from weldfatigue.fatigue.assessment import FatigueAssessment

assessor = FatigueAssessment()
result = assessor.run(
    method="nominal",
    material_name="DP600",
    weld_type="fillet",
    load_type="tension",
    stress_range=80.0,
    num_cycles=2_000_000,
)

print(f"Status: {result['single_block_result']['status']}")
print(f"Safety factor: {result['single_block_result']['safety_factor']:.2f}")
```

### Streamlit UI

```bash
streamlit run app/main.py
```

Navigate to http://localhost:8501 to access the interactive dashboard with 5 pages.

---

## Module Usage

### 1. Material Database

```python
from weldfatigue.materials.database import MaterialDatabase

db = MaterialDatabase()

# Look up a grade
mat = db.get("DP600")
print(mat.yield_strength)  # 350 MPa

# Search by criteria
high_strength = db.search(min_yield=500, family="steel")

# Get strain-rate parameters
params = db.get_strain_rate_params("DP600", model="cowper_symonds")
```

**Available grades:**
- Steel: DC04, DP600, DP780, DP980, HSLA340, HSLA420, 22MnB5, S355J2, 316L
- Aluminum: 6061-T6, 6082-T6, 5083-H111, 5754-O, 7075-T6

### 2. S-N Curves

```python
from weldfatigue.fatigue.sn_curve import SNCurve

sn = SNCurve(fat_class=80, material_type="steel")

# Allowable cycles at a stress range
N = sn.cycles_to_failure(stress_range=100.0)

# Stress at a given number of cycles
ds = sn.stress_range_at_cycles(1e6)

# Plot data
N_vals, stress_vals = sn.get_curve_points()
```

### 3. Fatigue Assessment

#### Nominal Stress Method

```python
from weldfatigue.fatigue.nominal_stress import NominalStressAssessment

assessor = NominalStressAssessment(fat_class=80, material="steel")
result = assessor.evaluate(stress_range=80.0, num_cycles=2_000_000)
# result.status -> "PASS"
# result.safety_factor -> 1.0
```

#### Hot-Spot Stress Method

```python
from weldfatigue.fatigue.hotspot_stress import HotSpotStressAssessment

hs = HotSpotStressAssessment(fat_class=100, material="steel")

# Manual extrapolation
sigma_hs = hs.extrapolate_type_a(s_04t=150.0, s_10t=120.0)

# Assessment
result = hs.evaluate(stress_range=sigma_hs, num_cycles=1_000_000)
```

#### Notch Stress Method

```python
from weldfatigue.fatigue.notch_stress import EffectiveNotchStressAssessment

notch = EffectiveNotchStressAssessment(material="steel", plate_thickness=10.0)
# Automatically uses FAT 225, r_ref = 1mm
result = notch.evaluate(stress_range=200.0, num_cycles=1_000_000)
```

### 4. Variable Amplitude (Palmgren-Miner)

```python
from weldfatigue.fatigue.damage import PalmgrenMiner
from weldfatigue.fatigue.sn_curve import SNCurve

sn = SNCurve(fat_class=80, material_type="steel", variable_amplitude=True)
miner = PalmgrenMiner(sn, damage_limit=1.0)

spectrum = [
    (120.0, 100_000),   # (stress_range_MPa, n_cycles)
    (100.0, 500_000),
    (80.0, 1_000_000),
]

result = miner.compute_damage(spectrum)
print(f"D = {result.total_damage:.4f} -> {result.status}")
```

### 5. Mean Stress Correction

```python
from weldfatigue.fatigue.mean_stress import MeanStressCorrection

# Goodman correction
Sa_eq = MeanStressCorrection.goodman(Sa=80, Sm=100, Su=600)

# IIW enhancement factor
f_R = MeanStressCorrection.iiw_enhancement_factor(R=-0.5, condition="stress_relieved")
```

### 6. Crash/Shock Analysis

```python
from weldfatigue.shock.crash_assessment import CrashAssessment
import numpy as np

crash = CrashAssessment()

# Dynamic material
result = crash.evaluate_dynamic_material("DP600", strain_rate=500.0)
print(f"Dynamic yield: {result.dynamic_yield:.0f} MPa")

# Weld failure check (EN 1993-1-8)
weld = crash.check_weld_failure(
    criterion="stress_based",
    sigma_perp=150, tau_perp=80, tau_parallel=50,
    fu=600,
)
print(f"Weld: {weld.status} (utilization={weld.utilization:.2f})")

# Energy absorption
force = np.array([0, 5000, 10000, 8000, 6000], dtype=float)
disp = np.array([0, 5, 10, 15, 20], dtype=float)
energy = crash.evaluate_energy(force, disp, mass=2.5)
print(f"SEA = {energy.specific_energy_absorption:.0f} J/kg")
```

### 7. FEA Post-Processing

```python
from weldfatigue.fea.generic_reader import GenericCSVReader
from weldfatigue.fea.stress_tensor import StressTensorOps

reader = GenericCSVReader()
fea = reader.read_stress_csv("results.csv")

# Compute derived quantities
stress = fea.get_stress_tensor()
vm = StressTensorOps.von_mises(stress)
principals = StressTensorOps.principal_stresses(stress)
```

### 8. Report Generation

```python
from weldfatigue.reporting.pdf_report import FatigueReport
from weldfatigue.reporting.html_report import HTMLReportGenerator
from pathlib import Path

# PDF report
report = FatigueReport("My Project", "Engineer Name", "2024-06-15")
report.add_cover_page("Fatigue Assessment", "Weld Joint A3")
report.add_fatigue_summary([...])
report.generate(Path("report.pdf"))

# HTML report
gen = HTMLReportGenerator()
gen.generate_fatigue_report(
    project_name="My Project", author="Engineer", date="2024-06-15",
    material_info={...}, fatigue_results=[...],
    output_path=Path("report.html"),
)
```

---

## Streamlit UI Pages

| Page | Description |
|------|-------------|
| Material Database | Browse grades, search by properties, plot strain-rate curves |
| Fatigue Analysis | Run all 3 IIW methods, S-N curve explorer, FAT catalog |
| Shock Analysis | Dynamic yield, weld failure check, energy absorption |
| FEA Post-Processing | CSV upload, stress tensor operations, hot-spot extraction |
| Report Generation | Configure and download PDF/HTML reports |

---

## Running Tests

```bash
# All tests
pytest tests/ -v

# Specific module
pytest tests/test_fatigue/ -v

# With coverage
pytest tests/ --cov=weldfatigue --cov-report=html
```

---

## Jupyter Notebooks

| Notebook | Topic |
|----------|-------|
| 01 | Material database exploration |
| 02 | S-N curve parameter study |
| 03 | Nominal stress benchmark (IIW) |
| 04 | Hot-spot stress benchmark (IIW) |
| 05 | Notch stress method example |
| 06 | Palmgren-Miner damage calculation |
| 07 | Mean stress correction comparison |
| 08 | Crash strain-rate effects |
| 09 | FEA CSV import workflow |
| 10 | Full end-to-end pipeline |
