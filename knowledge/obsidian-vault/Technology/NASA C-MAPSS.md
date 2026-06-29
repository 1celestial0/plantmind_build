---
tags: [technology, dataset, data]
created: 2026-06-20
---

# NASA C-MAPSS Dataset

## What It Is

**Commercial Modular Aero-Propulsion System Simulation (C-MAPSS)** — a run-to-failure dataset of turbofan engine sensor readings published by NASA in 2008.

## Key Facts

| Property | Value |
|---|---|
| Publisher | NASA Ames Prognostics Center of Excellence |
| Year | 2008 (Saxena & Goebel) |
| Engines | 100 training engines (FD001), run to failure |
| Sensors | 21 sensors per engine per cycle |
| Operating settings | 3 (op1, op2, op3) |
| Subsets | FD001 (1 condition), FD002 (6 conditions), FD003, FD004 |
| PlantMind uses | FD001 (simplest: 1 operating condition, 1 fault type) |
| Label | No explicit RUL — computed as `max_cycle - current_cycle` |

## The 21 Sensors

```
s1  : T2  total temperature at fan inlet
s2  : T24 total temperature at LPC outlet  ← degrading
s3  : T30 total temperature at HPC outlet  ← degrading
s4  : T50 total temperature at LPT outlet  ← degrading
s5  : P2  pressure at fan inlet
s6  : P15 total pressure in bypass-duct
s7  : P30 total pressure at HPC outlet     ← degrading
s8  : Nf  physical fan speed
s9  : Nc  physical core speed              ← degrading
s10 : epr engine pressure ratio
s11 : Ps30 static pressure at HPC outlet   ← degrading
s12 : phi ratio of fuel flow to Ps30       ← degrading
s13 : NRf corrected fan speed              ← degrading
s14 : NRc corrected core speed             ← degrading
s15 : BPR bypass ratio                     ← degrading
s16 : farB burner fuel-air ratio
s17 : htBleed bleed enthalpy               ← degrading
s18 : Nf_dmd demanded fan speed
s19 : PCNfR_dmd demanded corrected fan speed
s20 : W31 HPT coolant bleed                ← degrading
s21 : W32 LPT coolant bleed                ← degrading
```

Sensors marked ← degrading are the informative ones. s1, s5, s6, s10, s16, s18, s19 are near-constant across all cycles in FD001 — filtered out in [[Layer 2 - Features]].

## Why It's the Right Dataset

- **Real NASA data** → judges can't challenge validity
- **Public** → no IP/licensing issues for the demo
- **Ground truth labels** → we know exactly when each engine failed
- **21 sensors** → rich enough to show multi-dimensional degradation
- **Small enough** → runs on a laptop in seconds

## Why We Use FD001, Not FD002–FD004

FD002, FD003, FD004 add multiple operating conditions and fault types — more realistic but harder. For a hackathon demo, FD001's clarity (1 condition, 1 fault) makes the degradation signal cleaner and the story simpler. "Works on FD001" is sufficient for proof of concept.

## Connected Nodes

- Used in → [[Layer 1 - Data]]
- Provides labels for → [[Remaining Useful Life]]
- Informs → [[Decision - Clip RUL at 130]] (130 = Saxena 2008 standard)
- Stored on → [[Databricks]] DBFS at `/FileStore/plantmind/cmapss/`
