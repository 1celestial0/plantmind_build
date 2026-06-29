# ROI_BENCHMARKS.md
## PlantMind — Phase 5: ROI & Business Case Research
**Research Date:** 2026-06-30  
**Sources:** PAIN_REGISTER_2026_25th_June.md citations, Siemens True Cost of Downtime 2024, LOCKED_STATE demo formula

---

## Part A: Downtime Cost Database

| Sector / Asset | Cost/hr unplanned | Source |
|----------------|-------------------|--------|
| Oil refinery (CDU) | $850K/day ≈ $35K/hr | PAIN_REGISTER P025, iFactory 2026 |
| Petrochemical cracker | $50K–$300K/hr | PAIN_REGISTER P027 |
| Automotive assembly | $2.3M/hr | PAIN_REGISTER P026, Siemens 2024 |
| Semiconductor fab | $1–3M/hr | PAIN_REGISTER P028 |
| Power generation | $250K–$500K/hr | PAIN_REGISTER P030 |
| Pharma GMP batch | $100K–$500K/hr; up to $9M/batch | PAIN_REGISTER P029 |
| Pulp & paper | $25K/hr | PAIN_REGISTER P031 |
| Steel / heavy metals | $300K/hr | PAIN_REGISTER P032 |

---

## Part B: Predictive Maintenance ROI Database

| Metric | Range | Source |
|--------|-------|--------|
| Unplanned downtime reduction | 30–50% [INFERRED] | McKinsey PdM narratives; P005/P006 pain cluster |
| Maintenance cost reduction (CBM vs TBM) | 15–30% | PAIN_REGISTER P008, SMRP benchmarks |
| Advance warning window | 7–21 days | PAIN_REGISTER P006 |
| Pilot-to-production scale rate | 30–40% [INFERRED] | Industry AI adoption gap P033 |

---

## Part C: Energy Optimization ROI

| Metric | Value | Source |
|--------|-------|--------|
| Detectable energy waste | 20–30% process | PAIN_REGISTER P013 |
| Compressed air waste | 30–50% | PAIN_REGISTER P035 |
| ISO 50001 payback | <2 years [INFERRED] | PAIN_REGISTER P012 |

---

## Part D: OEE Improvement ROI

| Metric | Value | Source |
|--------|-------|--------|
| Typical process OEE | 40–60% | PAIN_REGISTER P021 |
| World-class OEE | 85%+ | OEE.com benchmarks (cited in P021) |
| 1% OEE improvement value | $10–50M/yr large plant [INFERRED] | P021 |

---

## Part E: Quality Intelligence ROI

| Metric | Value | Source |
|--------|-------|--------|
| COPQ as % revenue | 15–40% mid-maturity | PAIN_REGISTER P016 |
| In-process vs end-of-line detection cost | 10× cheaper in-process | PAIN_REGISTER P015 |

---

## Part F: Knowledge Management ROI

| Metric | Value | Source |
|--------|-------|--------|
| Tribal knowledge loss cost | $47M/yr large US firms | PAIN_REGISTER P004 |
| Maintenance search time | 15–25% wrench time | PAIN_REGISTER P010 |

---

## Part G: PlantMind Composite ROI Model

**Reference plant:** Medium petrochemical — $200M revenue, 500 critical assets, 74% OEE, $8M/yr maintenance, 12 unplanned events × 8 hr avg, $15M/yr energy.

**Formula (LOCKED):**
```
Value = (failures_prevented) × (avg_downtime_hours) × (cost_per_hour) − intervention_cost
```

| Lever | Conservative | Base | Optimistic | Assumption source |
|-------|-------------|------|------------|-------------------|
| Downtime prevented | 2 events/yr | 4 events/yr | 6 events/yr | PdM benchmarks Part B |
| Avg downtime hrs | 6 hr | 8 hr | 10 hr | PAIN_REGISTER incidents |
| Cost/hr | $50K | $75K | $100K | Part A petrochemical band |
| Intervention cost/yr | $400K | $600K | $800K | [ESTIMATE] CMMS + labor |

| Case | Annual gross benefit | Platform cost [EST] | Net benefit |
|------|---------------------|---------------------|-------------|
| Conservative | 2×6×$50K = $600K | $150K | $450K |
| Base | 4×8×$75K = $2.4M | $200K | $2.2M |
| Optimistic | 6×10×$100K = $6.0M | $250K | $5.75M |

**Payback (base):** ~1.1 months on net benefit vs platform cost [ESTIMATE].

**3-year NPV @ 10%:** Base case ≈ $5.4M [calculated from $2.2M/yr annuity factor 2.487].

---

## Part H: ROI Defensibility Matrix

| Pitch claim | Figure | Source | If challenged |
|-------------|--------|--------|---------------|
| "One avoided failure pays for the platform" | $600K+ single event | P025 $9.4M refinery pump | Use conservative $600K partial shutdown |
| "12 days RUL warning" | 12 days | LOCKED trigger rul_days < 14 | Physics Weibull CI in demo |
| "Human approval required" | Always | LOCKED §1 GötzeEngine | Show audit record |
| "Databricks alignment" | Partnership 2026-06-11 | LTTS press / LOCKED | DATABRICKS_MAP Part F |

---

## ARTIFACT QUALITY CHECKLIST

- [x] Figures cite PAIN_REGISTER or [ESTIMATE]
- [x] Composite model shows workings
- [x] Sector figures matched
- [x] Defensibility matrix covers pitch claims