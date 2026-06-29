# DATA_REALITY.md
## PlantMind — Phase 4: Data Landscape Research
**Research Date:** 2026-06-30  
**Model Used:** Synthesis from LOCKED_STATE §6, PAIN_REGISTER P022–P023, hackathon synthetic spec

---

## PART A: Data Source Taxonomy by Sector

| Sector | Primary OT sources | Typical formats | PlantMind path |
|--------|-------------------|-----------------|----------------|
| Petrochemical | PI, Aspen, DCS | Historian export, OPC batch | Auto Loader Bronze |
| Automotive | MES, Andon, PLC | CSV, MQTT JSON | Synthetic + C-MAPSS seed |
| Power | DCS, vibration CMS | Time-series CSV | PRONOSTIA calibration |
| Pharma | Batch records, CMMS | PDF SOPs, SQL | RAG corpus + synthetic batch |

---

## PART B: Protocol and Format Reference

| Protocol/Format | Prevalence | PlantMind handling |
|-----------------|------------|-------------------|
| OPC-UA | High (new plants) | Edge → file landing (hackathon) |
| PI AF export | High | CSV → Bronze |
| MQTT JSON | Medium (IIoT) | Structured Streaming |
| C-MAPSS whitespace | Benchmark | `ml/synthesis/` seed |
| PDF manuals | Universal | Chunk → ChromaDB / Vector Search |

---

## PART C: Data Quality Profile

| Issue | Rate [ESTIMATE] | Detection | Mitigation |
|-------|-----------------|-------------|------------|
| Stuck sensor | 5–10% tags | Z-score flatline | DataSentinel flag |
| Timestamp skew | 10–15% batches | Ingest EXPECT | Silver alignment UDF |
| Unit mismatch | 5% cross-plant | Schema registry | Unity Catalog comments |
| Missing values | 3–8% | DLT EXPECT OR DROP | Impute + confidence downgrade |

---

## PART D: Data Volume Estimates (medium plant, 90 days)

| Asset class | Assets | Signals/asset | Interval | 90-day rows |
|-------------|--------|---------------|----------|-------------|
| Pumps | 12 | 20 | 1 min | ~3.1M |
| Compressors | 8 | 20 | 1 min | ~2.1M |
| Motors | 6 | 15 | 1 min | ~1.2M |
| Valves | 4 | 10 | 5 min | ~0.1M |
| **Total** | **30** | — | — | **~6.5M** |

Calculation: `assets × signals × (90×24×60/interval)` — aligns LOCKED_STATE 30×20 synthetic spec.

---

## PART E: OT/IT Integration Patterns (top 3)

1. **Historian export batch** — OT stays air-gapped; daily CSV to landing zone (lowest risk, hackathon default).
2. **Edge gateway stream** — OPC-UA → MQTT → Databricks (production target).
3. **CMMS feedback loop** — Work order outcomes → Gold `maintenance_outcomes` (FeedbackLoopInterface).

---

## PART F: Synthetic Dataset Specifications (hackathon core)

### Dataset 1: `sensor_readings`
| Column | Type | Example |
|--------|------|---------|
| asset_id | string | pump_07 |
| timestamp | datetime | 2026-06-30T08:00:00Z |
| signal_id | string | bearing_temp |
| value | float | 72.4 |
| unit | string | degC |
| quality_flag | string | OK |

Sample rows (5 of 20 target):

| asset_id | timestamp | signal_id | value | unit | quality_flag |
|----------|-----------|-----------|-------|------|--------------|
| pump_07 | 2026-06-30T08:00:00Z | bearing_temp | 72.4 | degC | OK |
| pump_07 | 2026-06-30T08:00:00Z | vibration_rms | 2.1 | mm/s | OK |
| pump_07 | 2026-06-30T08:01:00Z | bearing_temp | 72.5 | degC | OK |
| comp_02 | 2026-06-30T08:00:00Z | discharge_pressure | 14.2 | bar | OK |
| valve_11 | 2026-06-30T08:00:00Z | position_pct | 87.0 | % | STUCK |

Embedded quality issues: (1) STUCK flag valve_11, (2) unit drift comp_02, (3) missing row pump_07 08:02.

### Dataset 2: `asset_health_snapshots`
| asset_id | health_score | rul_days | ci_low | ci_high | model_version |
|----------|--------------|----------|--------|---------|---------------|
| pump_07 | 38.2 | 12.4 | 9.1 | 16.2 | weibull-v1 |
| bearing_3 | 22.0 | 4.1 | 2.8 | 6.0 | weibull-v1 |
| motor_2 | 91.0 | 120.0 | 95.0 | 145.0 | weibull-v1 |

### Dataset 3: `gotze_decisions`
| decision_id | asset_id | top_intervention | iis_score | requires_approval |
|-------------|----------|------------------|-----------|-------------------|
| GD-001 | pump_07 | reduce_load | 0.74 | true |

### Datasets 4–10 (schemas locked for build)

| ID | Name | Purpose |
|----|------|---------|
| 4 | anomaly_events | DataSentinel outputs |
| 5 | root_cause_reports | RAG citations |
| 6 | audit_records | Governance lineage |
| 7 | maintenance_outcomes | Feedback loop |
| 8 | plant_config | Thresholds per asset class |
| 9 | document_registry | Manual/SOP index |
| 10 | sop_document_chunks | Vector embedding source |

Full 20-row samples per dataset → generated in `ml/synthesis/` during Lane 2 build.

---

## PART G: Data Assumptions Register

| Assumption | Hackathon | Production |
|------------|-----------|------------|
| RUL unit = days | Yes (LOCKED §6a) | Yes |
| 30 assets sufficient | Yes | Scale to 500+ |
| Synthetic physics-seeded | Yes | Kaggle + plant historian |
| 10–20 manual PDFs | Yes | Full CMMS doc store |
| Real-time = 1-min batch | Simulated | Sub-minute with gateway |

---

## ARTIFACT QUALITY CHECKLIST

- [x] Core datasets have schema + sample rows
- [x] Quality issues documented per dataset 1
- [x] Integration patterns are industry-standard
- [x] Volume estimates show workings
- [ ] Full 20 rows × 10 datasets — deferred to Lane 2 `ml/synthesis/`