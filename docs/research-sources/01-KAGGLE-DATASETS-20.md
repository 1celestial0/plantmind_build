# 20 Real Enterprise-Class Kaggle Datasets
**Purpose:** Ground PlantMind and LTTS Hackathon projects in real industrial data across Plant, Mobility, Sustainability, MedTech
**Curated for:** LTTS Lakshya 31 · Equinox Hackathon · July 9, 2026
**Version:** 1.0 · 2026-06-20

---

## HOW TO USE THIS DOCUMENT

Each dataset below includes:
- **Direct Kaggle URL**
- **Why it's relevant** to LTTS Hackathon themes
- **What you can build** with it
- **PlantMind angle** — does it extend or validate our core approach?

---

## SEGMENT 1: PLANT / INDUSTRIAL PREDICTIVE MAINTENANCE

### Dataset 1 — NASA C-MAPSS Turbofan Engine
**URL:** https://www.kaggle.com/datasets/behrad3d/nasa-cmaps
**Size:** 1.3 MB | **Samples:** 100 engines, 26 sensors, run-to-failure
**Target:** Remaining Useful Life (RUL)
**Why:** This IS our primary dataset. Saxena 2008 standard. FD001 used in PlantMind.
**Build:** Our full 5-layer pipeline — this is ground zero.
**PlantMind angle:** Direct use. Götze engine validated on this.

---

### Dataset 2 — PHM 2008 Data Challenge (Bearing)
**URL:** https://www.kaggle.com/datasets/uysalserkan/fault-induction-motor-dataset
**Size:** ~50 MB | **Samples:** 4 bearings, vibration time-series to failure
**Target:** Time to failure, fault detection
**Why:** Bearing failure is the #1 cause of motor downtime in plant operations.
**Build:** RUL predictor for rotating machinery. Götze Engine adaptation for bearings.
**PlantMind angle:** Validates portability — can our Götze decision engine work on bearing data?

---

### Dataset 3 — CWRU Bearing Fault Dataset
**URL:** https://www.kaggle.com/datasets/brjapon/cwru-bearing-fault-dataset
**Size:** ~250 MB | **Samples:** 10,000+ vibration samples, 4 fault types
**Target:** Fault classification (inner race, outer race, ball, normal)
**Why:** Industry gold standard for bearing diagnosis. Used in GE, SKF papers.
**Build:** Fault classifier + severity scorer → feed into Götze Engine as health signal.
**PlantMind angle:** Replace NASA sensor data with vibration FFT features in Layer 2.

---

### Dataset 4 — Steel Plates Fault Detection
**URL:** https://www.kaggle.com/datasets/uciml/faulty-steel-plates
**Size:** 127 KB | **Samples:** 1,941 steel plates, 27 features, 7 fault types
**Target:** Fault type classification
**Why:** Manufacturing quality control in steel — core plant operations.
**Build:** Multi-class fault classifier + counterfactual: "what property change removes this fault?"
**PlantMind angle:** Extend counterfactual proof to manufacturing QC — different domain, same claim.

---

### Dataset 5 — Manufacturing Defect Detection
**URL:** https://www.kaggle.com/datasets/fahmidachowdhury/manufacturing-defects
**Size:** ~5 MB | **Samples:** 10,000+ manufactured parts
**Target:** Defect rate prediction, production efficiency
**Why:** Real enterprise manufacturing process data — directly aligns with LTTS plant clients.
**Build:** Defect predictor → Götze Engine decides: rework vs scrap vs pass.
**PlantMind angle:** New use case for Layer 4 decision engine beyond turbofan.

---

### Dataset 6 — Predictive Maintenance (Microsoft Azure)
**URL:** https://www.kaggle.com/datasets/arnabbiswas1/microsoft-azure-predictive-maintenance
**Size:** 2.7 MB | **Samples:** 1,000 machines, 87,000+ records
**Columns:** machineID, volt, rotate, pressure, vibration, 5 error types, failure type
**Target:** Failure type prediction (24h ahead)
**Why:** Microsoft's own benchmark. Multi-machine, multi-failure, time-series.
**Build:** Multi-machine fleet health monitor. Götze Engine at fleet scale.
**PlantMind angle:** Scale proof: our engine working across 1,000 machines simultaneously.

---

## SEGMENT 2: MOBILITY

### Dataset 7 — EV Battery Degradation & Charge
**URL:** https://www.kaggle.com/datasets/bertnardomariouskono/electric-vehicle-ev-battery-degradation-and-charge
**Size:** 5 MB | **Samples:** 10,000 samples, NMC & LFP batteries
**Target:** State of Health (SoH), remaining battery life
**Why:** EV battery degradation is the #1 concern for EV OEMs — LTTS Mobility vertical.
**Build:** Battery RUL predictor → Götze decision: replace / condition / monitor
**PlantMind angle:** Direct port of our approach: RUL → Götze Score → action. Same architecture, new domain.

---

### Dataset 8 — Uber Lyft Rideshare Data (NYC)
**URL:** https://www.kaggle.com/datasets/ravi72munde/uber-lyft-cab-prices
**Size:** 693 MB | **Samples:** 693K rides, weather, demand
**Target:** Price prediction, demand forecasting
**Why:** Mobility fleet optimization — LTTS Mobility AI use case.
**Build:** Dynamic fleet dispatch optimizer → agent decides: reposition / charge / idle.
**PlantMind angle:** Götze-style decision scoring for fleet management decisions.

---

### Dataset 9 — Vehicle Sensor Data (OBD-II)
**URL:** https://www.kaggle.com/datasets/vortexkol/vehicle-sensor-data-for-predictive-maintenance
**Size:** ~10 MB | **Samples:** Real OBD-II logs, 20+ sensor channels
**Target:** Anomaly detection, fault prediction
**Why:** OBD-II is the actual data stream in every modern vehicle. LTTS Mobility clients use this.
**Build:** In-vehicle predictive maintenance agent → same pipeline as PlantMind, vehicle context.
**PlantMind angle:** Strongest mobility extension — same sensor→RUL→decision pattern.

---

### Dataset 10 — NYC Taxi Trip Data
**URL:** https://www.kaggle.com/datasets/elemento/nyc-yellow-taxi-trip-data
**Size:** 1.2 GB | **Samples:** 1.4M trips
**Target:** Trip duration, demand patterns, route optimization
**Why:** Fleet AI, route intelligence — LTTS connected mobility clients.
**Build:** Fleet health scoring under load → maintenance scheduling optimizer.
**PlantMind angle:** Scheduling layer: when to pull vehicles for maintenance based on usage patterns.

---

## SEGMENT 3: SUSTAINABILITY

### Dataset 11 — Global Data on Sustainable Energy (2000-2020)
**URL:** https://www.kaggle.com/datasets/anshtanwar/global-data-on-sustainable-energy
**Size:** 500 KB | **Samples:** 176 countries, 21 years, 20 energy metrics
**Target:** Energy access, renewables %, CO2 intensity
**Why:** LTTS Sustainability vertical — enterprise energy intelligence.
**Build:** Country/facility energy health score → Götze-style: switch to renewables / optimize grid / reduce intensity.
**PlantMind angle:** Götze Score applied to energy portfolio decisions.

---

### Dataset 12 — Low-Carbon Industrial Park Energy
**URL:** https://www.kaggle.com/datasets/ziya07/low-carbon-industrial-park-energy-dataset
**Size:** ~2 MB | **Samples:** 30 days × hourly, solar/wind/grid/EV/storage metrics
**Target:** Grid reliability, renewable integration, energy storage optimization
**Why:** Exact LTTS use case: industrial park energy AI with renewables.
**Build:** Real-time energy flow optimizer. Götze Engine decides: draw from grid / discharge storage / curtail load.
**PlantMind angle:** Layer 4 directly applicable — deterministic scoring over energy mix decisions.

---

### Dataset 13 — Building Energy Efficiency (NYC)
**URL:** https://www.kaggle.com/datasets/new-york-city/nyc-energy-efficiency-ratings
**Size:** ~5 MB | **Samples:** 18,000+ buildings, ENERGY STAR scores
**Target:** Energy efficiency rating, consumption prediction
**Why:** Smart buildings — major LTTS sustainability initiative for commercial RE clients.
**Build:** Building health score → recommended retrofit action → counterfactual: "this HVAC upgrade saves X kWh."
**PlantMind angle:** Our counterfactual proof concept maps directly here.

---

### Dataset 14 — Air Quality Index (AQI) Time Series
**URL:** https://www.kaggle.com/datasets/threnjen/40-years-of-air-quality-index-from-the-epa
**Size:** 400 MB | **Samples:** 40 years of daily AQI across US cities
**Target:** AQI prediction, pollutant anomaly detection
**Why:** Environmental monitoring — sustainability compliance for LTTS industrial clients.
**Build:** Facility emission health monitor → triggers Götze decision on process changes.
**PlantMind angle:** Environmental RUL concept: how many days until emission threshold breach?

---

## SEGMENT 4: MEDTECH

### Dataset 15 — MIT-BIH Arrhythmia (ECG)
**URL:** https://www.kaggle.com/datasets/shayanfazeli/heartbeat
**Size:** 67 MB | **Samples:** 109,446 ECG heartbeats, 5 classes
**Target:** Arrhythmia classification
**Why:** Cardiac monitoring — LTTS MedTech AI for wearable/ICU devices.
**Build:** Real-time cardiac anomaly detector → Götze decision: escalate / monitor / alert.
**PlantMind angle:** RUL of patient stability. Counterfactual: "if medication adjusted, trajectory changes."

---

### Dataset 16 — IoMT Alert Dataset (Medical IoT)
**URL:** https://www.kaggle.com/datasets/prokashbarmancu/iomt-alert
**Size:** ~3 MB | **Samples:** Medical IoT readings with alert labels
**Target:** Anomaly/alert classification in real-time health monitoring
**Why:** IoMT = Internet of Medical Things. LTTS MedTech vertical core use case.
**Build:** Medical device health score → Götze Engine: alert / recalibrate / escalate to clinician.
**PlantMind angle:** 1:1 mapping with PlantMind — sensor stream → RUL of patient status → decision.

---

### Dataset 17 — Multi-Sensor Medical IoT
**URL:** https://www.kaggle.com/datasets/programmer3/smart-health-iot-sensor-dataset
**Size:** ~5 MB | **Samples:** Multiple biometric sensor streams, health outcomes
**Target:** Patient health classification, anomaly detection
**Why:** Multi-sensor fusion for health — mirrors our 21-sensor industrial setup.
**Build:** Multi-signal health degradation predictor. Layer 2 (feature engineering) identical pattern.
**PlantMind angle:** Prove generalization: same feature engineering pipeline, clinical data.

---

### Dataset 18 — Diabetes Prediction (Pima Indians)
**URL:** https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database
**Size:** 23 KB | **Samples:** 768 patients, 8 biomarkers
**Target:** Diabetes onset prediction
**Why:** Chronic disease risk scoring — LTTS remote patient monitoring use case.
**Build:** Health trajectory scorer + Götze-style intervention ranking (lifestyle vs medication vs monitoring).
**PlantMind angle:** Götze Score with medical weight factors. Counterfactual: "this lifestyle change delays onset X years."

---

## SEGMENT 5: CROSS-DOMAIN / ADVANCED

### Dataset 19 — PHM Data Challenge 2012 (Pronostia Bearing)
**URL:** https://www.kaggle.com/datasets/kvdgansai/pronostia-bearing-dataset
**Size:** ~100 MB | **Samples:** 17 bearings, 3 operating conditions, vibration + temp to failure
**Target:** RUL prediction under varying conditions
**Why:** PHM (Prognostics & Health Management) Society benchmark. Used in 100+ papers.
**Build:** Transfer learning: train on one operating condition, test on another.
**PlantMind angle:** Layer 2 feature generalization across operating conditions — validates Patent 1 claim scope.

---

### Dataset 20 — Awesome Industrial Datasets (Meta-Repo)
**URL:** https://github.com/jonathanwvd/awesome-industrial-datasets
**Note:** This is a GitHub repo cataloging 50+ industrial datasets across all domains.
**Why:** A meta-resource — browse it to find domain-specific datasets beyond these 20.
**Categories:** Predictive maintenance, quality control, energy, aerospace, water treatment, semiconductor.
**PlantMind angle:** Use to find domain-specific data when extending PlantMind to new LTTS verticals.

---

## SUMMARY TABLE

| # | Dataset | Segment | Size | PlantMind Layer | Key Use |
|---|---|---|---|---|---|
| 1 | NASA C-MAPSS | Plant | 1.3 MB | All | Primary dataset |
| 2 | PHM Bearing | Plant | 50 MB | 1-4 | Bearing RUL |
| 3 | CWRU Bearing | Plant | 250 MB | 1-3 | Fault classification |
| 4 | Steel Plates | Plant | 127 KB | 3-4 | Mfg QC decision |
| 5 | Mfg Defects | Plant | 5 MB | 4 | Defect scoring |
| 6 | Azure PdM | Plant | 2.7 MB | All | Fleet scale |
| 7 | EV Battery | Mobility | 5 MB | All | Battery RUL |
| 8 | Rideshare NYC | Mobility | 693 MB | 4 | Fleet dispatch |
| 9 | OBD-II Vehicle | Mobility | 10 MB | All | In-vehicle PdM |
| 10 | NYC Taxi | Mobility | 1.2 GB | 4-5 | Fleet scheduling |
| 11 | Sustainable Energy | Sustainability | 500 KB | 4 | Energy portfolio |
| 12 | Industrial Park | Sustainability | 2 MB | All | Grid energy AI |
| 13 | NYC Buildings | Sustainability | 5 MB | 4-5 | Retrofit decisions |
| 14 | AQI 40yr | Sustainability | 400 MB | 1-3 | Emission monitoring |
| 15 | ECG Arrhythmia | MedTech | 67 MB | All | Cardiac anomaly |
| 16 | IoMT Alert | MedTech | 3 MB | All | Medical IoT |
| 17 | Multi-Sensor Health | MedTech | 5 MB | 1-2 | Feature fusion |
| 18 | Diabetes Pima | MedTech | 23 KB | 4 | Intervention scoring |
| 19 | PHM 2012 Pronostia | Cross-domain | 100 MB | 1-3 | Transfer learning |
| 20 | Awesome Industrial | Meta | N/A | All | Discovery resource |

---

## DOWNLOAD PROTOCOL

```bash
# Install Kaggle CLI
pip install kaggle --break-system-packages

# Set up API key (download from kaggle.com → Account → API)
mkdir ~/.kaggle && cp kaggle.json ~/.kaggle/ && chmod 600 ~/.kaggle/kaggle.json

# Download datasets (examples)
kaggle datasets download behrad3d/nasa-cmaps -p data/plant/cmapss/
kaggle datasets download bertnardomariouskono/electric-vehicle-ev-battery-degradation-and-charge -p data/mobility/ev-battery/
kaggle datasets download ziya07/low-carbon-industrial-park-energy-dataset -p data/sustainability/industrial-park/
kaggle datasets download prokashbarmancu/iomt-alert -p data/medtech/iomt/

# Unzip
for f in data/**/*.zip; do unzip "$f" -d "${f%.zip}"; done
```

---

*Dataset guide v1.0 · PlantMind · LTTS Lakshya 31 Hackathon · 2026-06-20*
