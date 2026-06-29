# PLANTMIND — MASTER RESEARCH & DESIGN META-PROMPT
## LTTS × Databricks Hackathon | Parallel Research Protocol
### Version: 2.0 | Multi-Model Execution Architecture
### Project: PlantMind | Owner: LTTS Senior Data Engineer

---

## ╔══ HOW TO USE THIS PROMPT ══════════════════════════════════════════╗
##
##  This prompt is designed for PARALLEL execution across multiple AI
##  models. Do NOT paste the entire document into one model sequentially.
##  Instead, use the PARALLELISM MAP below to split phases across models.
##
##  Each PHASE is a self-contained sub-prompt. Every phase includes a
##  CONTEXT CAPSULE so it runs independently without the rest of the doc.
##
##  Recommended model routing:
##  ┌─────────────────────────────────────────────────────────────────┐
##  │ Kimi K2 / GLM-Z1        → Phase 1, 2, 5 (web research heavy)  │
##  │ Kimi K2 long context    → Phase 4       (data landscape)       │
##  │ GLM 5.2 / DeepSeek R1   → Phase 3       (technical deep-dive)  │
##  │ Claude Opus / Sonnet    → Phase 6       (synthesis + lock)     │
##  │ Perplexity Deep         → ROI figures with live citations      │
##  └─────────────────────────────────────────────────────────────────┘
##
##  After parallel phases complete → paste all outputs into Claude
##  and run the SYNTHESIS PROTOCOL (Section 3) to produce Phase 6.
##
## ╚═════════════════════════════════════════════════════════════════════╝

---

## SECTION 1 — PARALLELISM MAP

```
PARALLEL GROUP A — Run simultaneously, no dependencies
┌──────────────────────────────────────────────────────────────────┐
│  PHASE 1: Industry Pain Point Research    → PAIN_REGISTER.md    │
│  PHASE 2: Competitive Landscape           → COMPETITIVE_MAP.md  │
│  PHASE 5: ROI & Business Case             → ROI_BENCHMARKS.md   │
└──────────────────────────────────────────────────────────────────┘
         ↓ all three complete ↓

PARALLEL GROUP B — Run simultaneously after Group A
┌──────────────────────────────────────────────────────────────────┐
│  PHASE 3: Databricks Capability Deep-Dive → DATABRICKS_MAP.md   │
│  PHASE 4: Data Landscape Research         → DATA_REALITY.md     │
└──────────────────────────────────────────────────────────────────┘
         ↓ all five complete ↓

SEQUENTIAL — Synthesis only (Claude recommended)
┌──────────────────────────────────────────────────────────────────┐
│  PHASE 6: Architecture Lock               → ARCH_LOCK.md        │
│           (synthesizes all 5 artifacts)                          │
└──────────────────────────────────────────────────────────────────┘
         ↓ Phase 6 complete ↓

PARALLEL GROUP C — Build artifacts (post-lock)
┌──────────────────────────────────────────────────────────────────┐
│  BUILD-A: Synthetic data + DLT pipeline   → notebooks           │
│  BUILD-B: ML models + MLflow tracking     → notebooks           │
│  BUILD-C: Vector Search + RAG + Agents    → notebooks           │
│  COMMS-A: Pitch deck + demo script        → PPT + MD            │
└──────────────────────────────────────────────────────────────────┘
```

### Dependency Rules
| Phase | Depends On | Can Start When |
|---|---|---|
| Phase 1 | Nothing | Immediately |
| Phase 2 | Nothing | Immediately |
| Phase 5 | Nothing | Immediately |
| Phase 3 | Nothing | Immediately (Databricks docs are stable) |
| Phase 4 | Nothing | Immediately |
| Phase 6 | All 5 phases | All 5 artifacts delivered |
| Build Group C | Phase 6 | ARCH_LOCK.md approved |

### Output Contract Standard
Every phase must deliver its artifact in this exact structure so outputs from different models can be merged without reformatting:

```markdown
# [ARTIFACT_NAME]
## PlantMind — [Phase Name]
## Model Used: [model name]
## Execution Date: [date]
## Status: DRAFT | REVIEW | LOCKED

---
[Content per phase specification]
---

## ARTIFACT QUALITY CHECKLIST
- [ ] All claims have a source or are explicitly marked [INFERRED]
- [ ] All tables have headers and consistent column count
- [ ] All ROI figures have unit, timeframe, and citation
- [ ] All Databricks features have version/GA date noted
- [ ] No marketing language without engineering grounding
```

---

## SECTION 2 — PROJECT IDENTITY LOCK
### (Include this capsule in EVERY phase prompt)

```
PROJECT: PlantMind
OWNER: LTTS (L&T Technology Services) — Engineering Intelligence Division
CONTEXT: LTTS × Databricks strategic partnership hackathon entry

ONE-LINE DEFINITION:
PlantMind is an Engineering Intelligence framework for industrial assets
that converts multi-source plant, sensor, maintenance, and operational data
into explainable, actionable engineering decisions — with a Tier-1 reference
implementation built natively on Databricks.

TWO-LAYER ARCHITECTURE (Critical — read before designing anything):

  LAYER 0 — PlantMind Framework (Tool-Agnostic)
  ┌──────────────────────────────────────────────────────────────┐
  │  Interface contracts. Data schemas. Agent patterns.          │
  │  Governance requirements. Feedback loop design.              │
  │  This is the IP. This is what LTTS owns and can reuse       │
  │  across Databricks, Azure ML, Snowflake, or any runtime.   │
  │  Platform-independent. Potentially patentable.              │
  └──────────────────────────────────────────────────────────────┘

  LAYER 1 — PlantMind on Databricks (Tier-1 Reference Implementation)
  ┌──────────────────────────────────────────────────────────────┐
  │  Every framework interface implemented on Databricks.        │
  │  Auto Loader, DLT, MLflow, Vector Search, Mosaic AI,        │
  │  Unity Catalog, Workflows, Lakeview Dashboards.             │
  │  This is the hackathon deliverable. Working. Demoed.        │
  │  Chosen because Databricks is LTTS strategic partner AND    │
  │  best-in-class runtime for this problem class.              │
  └──────────────────────────────────────────────────────────────┘

PITCH FRAMING:
  "PlantMind is an open Engineering Intelligence framework.
   For this hackathon, we built the complete Tier-1 reference
   implementation on Databricks — because no other platform
   natively unifies lakehouse, ML lifecycle, vector search, and
   agentic AI at industrial scale today."

TARGET SECTORS (priority order):
  1. Petrochemical / Oil & Gas / Energy
  2. Industrial Manufacturing (Discrete + Process)
  3. Semiconductor Equipment Manufacturing
  4. Automotive Production Lines
  5. Utility / Power Grid Asset Monitoring

TARGET USERS:
  Plant Engineer, Reliability Engineer, Maintenance Engineer,
  Energy Manager, Quality Engineer, Operations Manager,
  Data Engineer (OT/IT boundary)

WHAT PLANTMIND IS NOT:
  - NOT a generic IoT dashboard
  - NOT a rule-based alerting system
  - NOT a chatbot
  - NOT locked to Databricks as the only runtime (see Layer 0)
  - NOT a point solution for one KPI
  - NOT dependent on custom hardware in v1

FRAMEWORK INTERFACE CONTRACTS (Layer 0 — reference for all phases):
  IngestorInterface(source, schema, target, quality_rules)
  FeatureStoreInterface(entity_key, features, point_in_time, ttl)
  AnomalyModelInterface(asset_id, window, threshold, confidence_method)
  KnowledgeRetrieverInterface(query, asset_context, top_k, filters)
  AgentOrchestratorInterface(trigger, tools, output_schema, audit_log)
  GovernanceInterface(lineage, access_policy, audit_trail, explainability)
  FeedbackLoopInterface(recommendation_id, outcome, label, retrain_trigger)

DATABRICKS IMPLEMENTATION MAP (Layer 1 — reference for Phase 3):
  IngestorInterface      → Auto Loader + Delta Live Tables
  FeatureStoreInterface  → Databricks Feature Store
  AnomalyModelInterface  → MLflow + Model Serving (batch)
  KnowledgeRetriever     → Vector Search + Foundation Model API
  AgentOrchestrator      → Mosaic AI Agents + LangChain on Databricks
  GovernanceInterface    → Unity Catalog + Lakehouse Monitoring
  FeedbackLoopInterface  → Delta tables + Workflows (scheduled retraining)
```

---

## SECTION 3 — SYNTHESIS PROTOCOL

### When to Use
After all 5 parallel phases are complete, paste this synthesis prompt into Claude (Opus preferred) along with all 5 artifact outputs.

```
SYNTHESIS PROMPT — Paste into Claude with all 5 artifacts attached:

You are synthesizing 5 research artifacts into a locked architecture
document for PlantMind, an Engineering Intelligence framework for
industrial assets with a Databricks-native reference implementation.

Attached artifacts:
- PAIN_REGISTER.md (Phase 1 output)
- COMPETITIVE_MAP.md (Phase 2 output)
- DATABRICKS_MAP.md (Phase 3 output)
- DATA_REALITY.md (Phase 4 output)
- ROI_BENCHMARKS.md (Phase 5 output)

Your task: Produce ARCHITECTURE_LOCK.md (Phase 6) by:

1. VALIDATION GATE — For each major PlantMind feature, verify:
   a. It solves a pain from PAIN_REGISTER (cite pain ID)
   b. It is differentiated from competitors in COMPETITIVE_MAP (cite gap)
   c. It has a Databricks implementation in DATABRICKS_MAP (cite capability)
   d. It has data to run on from DATA_REALITY (cite dataset)
   e. It has measurable ROI from ROI_BENCHMARKS (cite figure + source)
   Any feature that fails any gate is flagged [GATE FAIL — REVIEW].

2. FRAMEWORK LAYER — Produce the tool-agnostic interface contract table:
   For each of the 7 interfaces defined in the Project Identity section,
   define the contract signature and what it must guarantee, independent
   of Databricks. This is Layer 0. One paragraph per interface.

3. DATABRICKS IMPLEMENTATION — For each interface, map the exact
   Databricks service, justify why it is the best fit, and note any
   known limitation with its mitigation. This is Layer 1.

4. ARCHITECTURE DIAGRAM — Produce in both ASCII and Mermaid:
   Data sources → Auto Loader → Bronze DLT → Silver DLT → Gold features
   → MLflow anomaly detection → Vector Search → Agent orchestrator
   → Streamlit UI + Lakeview dashboard → Unity Catalog governance layer

5. AGENT DESIGN — For each of the 8 agents below, produce the full
   design specification in the template defined in Phase 6 of this doc.
   Agents: Data Quality, Asset Health, Root Cause, Energy Optimizer,
           OEE Intelligence, Quality Intelligence, Maintenance Planner,
           Executive Summarizer

6. MVP SCOPE TABLE — Locked 2-day scope: Must / Should / Could / Out

7. EXECUTION PLAN — Hour-by-hour, Day 1 and Day 2, per the template
   in this document.

Output format: Single markdown document (ARCHITECTURE_LOCK.md).
Quality gate: Every section must pass the 5-gate validation above.
```

---

## SECTION 4 — PHASE 1 SUB-PROMPT
### Industry Pain Point Research
### Recommended Model: Kimi K2 or GLM-Z1 (web search enabled)
### Estimated Time: 45–90 minutes with deep search
### Output: PAIN_REGISTER.md

---

### PASTE THIS INTO YOUR RESEARCH MODEL — START PHASE 1

```
=== PLANTMIND — PHASE 1: INDUSTRY PAIN POINT RESEARCH ===

PROJECT CONTEXT (read before researching):
PlantMind is an Engineering Intelligence framework for industrial assets.
Built by LTTS (L&T Technology Services). Tier-1 reference implementation
on Databricks. Two-layer design: tool-agnostic framework + Databricks build.
Target sectors: petrochemical, manufacturing, semiconductor equipment,
automotive production, utility grid.

YOUR TASK:
Research real, documented, financially quantified pain points faced by
plant engineers, reliability engineers, maintenance engineers, energy
managers, quality engineers, and operations managers in asset-intensive
industries. Do not invent pain. Source it from industry reports, analyst
firms, vendor white papers, academic papers, or documented case studies.

RESEARCH ANCHOR FACTS (validate, update, and expand these):
- Unplanned downtime costs: $260K–$500K+/hour depending on sector
  Source to verify: Aberdeen Group, Senseye/Siemens 2022 study
- Alarm flood: large plant averages 10,000+ alarms/day, operators
  process max ~1 alarm per 10 minutes. Source: ISA-18.2, EEMUA 191
- Knowledge loss: 50% of industrial workforce retirement-eligible
  within 10 years. Source: Deloitte manufacturing report
- Predictive vs reactive: 25–35% downtime reduction, 20–25% maintenance
  cost reduction. Source: McKinsey
- Energy waste: 20–30% of process plant energy is detectable waste
  Source: DOE / IEA reports
- Data utilization gap: <1% of generated industrial data is analyzed
  Source: IBM Institute for Business Value

ROLES TO RESEARCH PAIN FOR:
1. Plant Engineer / Process Engineer
2. Reliability Engineer
3. Maintenance Engineer (corrective + preventive)
4. Energy Manager
5. Quality Engineer
6. Operations Manager / Plant Director
7. Data Engineer at OT/IT boundary

RESEARCH QUESTIONS PER ROLE (answer all):

FOR PLANT ENGINEERS:
- What % of their shift is manual historian review vs. decision making?
- What tools are used today? (PI, Aspen, DCS, spreadsheets, paper?)
- How long to diagnose a process deviation: alarm to root cause?
- What is the quantified cost of alarm overload and operator fatigue?
- What happens when the senior process engineer retires?

FOR RELIABILITY ENGINEERS:
- What failure detection methods are standard today?
- What % of failures are detected before unplanned downtime occurs?
- What is the industry average MTTD (mean time to detect) by sector?
- What is the industry average MTTR by sector?
- How is failure history stored? (paper, CMMS, SAP PM, Oracle EAM?)
- What is the cost of a missed failure detection event, by sector?

FOR MAINTENANCE ENGINEERS:
- How is work order prioritization done today? How accurate is it?
- What % of planned maintenance is executed on time?
- How long does a maintenance engineer spend searching for the right
  SOP, manual, or part spec? (time-in-motion studies)
- What % of maintenance actions resolve root cause vs. treat symptoms?
- What is the "planner's dilemma" in industrial maintenance?

FOR ENERGY MANAGERS:
- How are energy baselines established today? What are the gaps?
- What % of energy anomalies go undetected in a typical plant?
- What is the regulatory pressure on energy reporting? (ISO 50001,
  EU ETS, US EPA, SEC climate disclosure)
- What is the business value of a 1% energy efficiency improvement
  in a medium petrochemical plant?

FOR QUALITY ENGINEERS:
- What % of defects are detected in-process vs. end-of-line today?
- What is COPQ (Cost of Poor Quality) as % of revenue by sector?
- How long does quality root cause analysis take on average?
- What is the cost of a quality escape to a downstream customer?
- How is "golden batch" knowledge documented and transferred today?

FOR OT/IT DATA ENGINEERS:
- What are the top 3 blockers to getting OT data into a cloud lakehouse?
- What is the typical time to connect a new plant data source?
- What are the dominant historian platforms? (PI, Aspen, GE, Honeywell)
- What data quality issues are endemic in industrial sensor data?
  (stuck sensors, drift, unit inconsistency, timestamp misalignment)

SECTOR-SPECIFIC RESEARCH:
For each target sector, find documented case studies of:
- A specific unplanned downtime event and its cost
- A predictive maintenance success story with quantified results
- An energy optimization project with before/after data
- A quality intelligence improvement with defect rate numbers

SECTORS: Petrochemical, Refining, Chemical, Automotive Assembly,
         Semiconductor Fab, Power Generation, Pulp & Paper, Pharma Mfg

OUTPUT FORMAT — PAIN_REGISTER.md:

Deliver a structured document with:

PART A: Pain Point Register Table
Columns: Pain_ID | Role | Pain Description | Current Workaround |
         Business Impact ($/yr or %) | Source/Citation |
         PlantMind Solution Hypothesis | Severity (1-5)

Minimum 30 pain points. At least 4 per sector. Each needs a $ figure.

PART B: Pain Clustering
Group pains into 5–7 themes (e.g., "Knowledge Silos",
"Alarm Overload", "Reactive Maintenance Trap"). For each theme:
- Theme name and description
- Pain IDs in this theme
- Combined estimated annual impact
- Which PlantMind agent or feature addresses it

PART C: Top 10 Most Valuable Pain Points
Ranked by: (Severity × Financial Impact × Frequency × Solvability)
For each: explain why PlantMind is better positioned than alternatives
to solve it.

PART D: Evidence Quality Assessment
Rate the research quality: Strong Evidence / Moderate / Weak Inference
Flag any pain point marked [INFERRED] where no direct source was found.

Include at end:
## ARTIFACT QUALITY CHECKLIST
- [ ] 30+ pain points documented
- [ ] All financial figures cited
- [ ] All sectors covered
- [ ] No pain invented without [INFERRED] flag
- [ ] Model used and date noted
```

---

## SECTION 5 — PHASE 2 SUB-PROMPT
### Competitive Landscape Analysis
### Recommended Model: Kimi K2 or Perplexity Deep Research
### Estimated Time: 60–90 minutes
### Output: COMPETITIVE_MAP.md

---

### PASTE THIS INTO YOUR RESEARCH MODEL — START PHASE 2

```
=== PLANTMIND — PHASE 2: COMPETITIVE LANDSCAPE ANALYSIS ===

PROJECT CONTEXT:
PlantMind is a two-layer Engineering Intelligence framework for industrial
assets. Layer 0: tool-agnostic framework with interface contracts.
Layer 1: Databricks-native reference implementation by LTTS.

The pitch framing is critical: "PlantMind is not a Databricks app.
It is an Engineering Intelligence framework. We chose Databricks as
the Tier-1 reference implementation because no other platform natively
unifies lakehouse, ML lifecycle, vector search, and agentic AI for
industrial use cases at this level of integration."

YOUR TASK:
Research every significant competitor and adjacent solution in the
industrial AI, predictive maintenance, and plant intelligence market.
Be honest about their strengths. Identify specific gaps that PlantMind's
framework design fills that they do not.

COMPETITORS TO RESEARCH (go deep on each):

GROUP 1 — Industrial AI / Predictive Analytics Platforms
- AspenTech (PCAI, Aspen Mtell, Aspen Inmation)
- Emerson (DeltaV, Plantweb Optics, Boundless Automation)
- ABB (Ability GENIX, ABB Conversant)
- Honeywell (Forge, Honeywell Connected Plant, Experion)
- Siemens (MindSphere, Industrial Edge, Siemens Industrial Copilot)
- GE Vernova (formerly GE Digital — Predix, APM, Asset Performance)
- AVEVA (PI System, AVEVA Unified Operations Center, Insight)
- Seeq Corporation (advanced process analytics)
- C3.ai (industrial AI applications on Microsoft/AWS)
- Uptake (industrial AI for asset reliability)
- Palantir Foundry (operations intelligence)
- Cognite Data Fusion (industrial knowledge graph + GenAI)

GROUP 2 — Databricks-Native or Lakehouse-Native Solutions
- Existing Databricks Solution Accelerators for manufacturing/energy
  (research what exists: predictive maintenance, OEE, quality)
- Any documented Databricks customer case studies in industrial AI
- Competitors building on Databricks Lakehouse for industrial

GROUP 3 — Cloud Platform Industrial AI
- Microsoft Azure: Digital Twins + Azure OpenAI Industrial Copilot
- AWS: IoT TwinMaker + Bedrock for manufacturing
- Google: Vertex AI + Looker for industrial analytics

GROUP 4 — CMMS / EAM with AI Extensions
- IBM Maximo + Watson
- SAP PM + Asset Intelligence Network
- Oracle EAM
- Infor EAM

FOR EACH COMPETITOR ANSWER:
1. Core technical approach? (Rules? ML? GenAI? Digital Twin? Simulation?)
2. Data sources natively supported?
3. Deployment model? (SaaS? On-prem? Hybrid? Which cloud?)
4. Typical customer size and contract value range?
5. Documented weaknesses or customer complaints? (G2, Gartner Peer
   Insights, LinkedIn comments, Reddit, industry forums)
6. Do they explain root cause or just flag anomalies?
7. Do they generate natural language maintenance recommendations?
8. Are they locked to proprietary historian platforms? Which?
9. Databricks integration story — does it exist? How deep?
10. What requires external tools that aren't integrated?
11. Time to first insight from new installation?
12. AI reasoning depth — shallow rules or deep agent reasoning?

FRAMEWORK DIFFERENTIATION RESEARCH:
Research which competitors offer:
- Open framework / open interfaces (vs. proprietary lock-in)
- Portable intelligence across different runtime platforms
- Agentic root cause reasoning (not just anomaly flagging)
- Human-in-the-loop with audit trail
- Source-grounded LLM recommendations with citations
- Feedback loop from maintenance outcomes to model retraining

OUTPUT FORMAT — COMPETITIVE_MAP.md:

PART A: Competitor Profiles
For each of the 12+ competitors: 1-paragraph summary covering
approach, strengths, documented weaknesses, and Databricks story.

PART B: Feature Comparison Matrix
Rows: competitors + PlantMind Framework + PlantMind on Databricks
Columns:
- Anomaly detection (time-series)
- Root cause analysis (agentic reasoning)
- Natural language maintenance recommendation (LLM)
- Engineering knowledge RAG (manuals + SOPs)
- Energy optimization intelligence
- OEE intelligence
- Open framework / portable interfaces
- Databricks-native integration
- Human-in-the-loop with audit trail
- Source-grounded recommendations (citations)
- Feedback loop (outcome → model retraining)
- Time to first insight (new installation)
- Deployment flexibility (cloud-agnostic)

Rate each: ✓ Full | ~ Partial | ✗ None | ? Unknown

PART C: Positioning Map
2×2 matrix description (for diagram):
X-axis: Proprietary lock-in ←→ Open / Framework design
Y-axis: Shallow alerting ←→ Deep agentic reasoning
Position each competitor. PlantMind should be: Open + Deep.

PART D: Identified Market Gaps
List 7+ specific gaps that PlantMind fills that no current competitor
covers completely. For each gap:
- Gap description
- Which competitors partially address it and how
- Why PlantMind's framework design is the right answer
- Pain ID from Phase 1 this gap addresses (placeholder: PAIN-XX)

PART E: PlantMind Differentiation Statement
One paragraph. Copy-paste ready for the pitch deck.
Must cover: framework design, Databricks implementation, LTTS domain depth,
agentic reasoning, open interfaces, feedback loop.

PART F: Competitive Risk Assessment
Top 3 competitive risks to PlantMind and mitigation strategy for each.

Include at end:
## ARTIFACT QUALITY CHECKLIST
- [ ] 12+ competitors profiled
- [ ] Feature matrix complete with sources
- [ ] 7+ gaps identified and explained
- [ ] Differentiation statement is specific (no generic buzzwords)
- [ ] Competitive risks are honest
```

---

## SECTION 6 — PHASE 3 SUB-PROMPT
### Databricks Capability Deep-Dive
### Recommended Model: GLM 5.2 / DeepSeek R1 / Claude (technical reasoning)
### Estimated Time: 60–90 minutes
### Output: DATABRICKS_MAP.md

---

### PASTE THIS INTO YOUR RESEARCH MODEL — START PHASE 3

```
=== PLANTMIND — PHASE 3: DATABRICKS CAPABILITY DEEP-DIVE ===

PROJECT CONTEXT:
PlantMind uses a two-layer architecture:
- Layer 0: tool-agnostic framework with 7 interface contracts
- Layer 1: Databricks-native reference implementation

Layer 1 uses ONLY Databricks services. No external ML platforms.
No external vector DBs. No Azure ML. No SageMaker. No Pinecone.
Databricks is the full stack.

Your task is NOT to write a Databricks brochure.
Your task is rigorous technical capability assessment:
- What does each Databricks service do well?
- What are its documented limitations?
- Why is it the right choice vs. the alternative?
- What is the workaround if it falls short?

FRAMEWORK INTERFACES TO MAP (Layer 0 → Layer 1):
1. IngestorInterface      → Auto Loader + Delta Live Tables
2. FeatureStoreInterface  → Databricks Feature Store
3. AnomalyModelInterface  → MLflow + Databricks Model Serving
4. KnowledgeRetriever     → Databricks Vector Search + Foundation Model API
5. AgentOrchestrator      → Mosaic AI Agent Framework + LangChain
6. GovernanceInterface    → Unity Catalog + Lakehouse Monitoring
7. FeedbackLoopInterface  → Delta tables + Databricks Workflows

CAPABILITIES TO RESEARCH IN DEPTH:

1. AUTO LOADER & STRUCTURED STREAMING
   - What file formats does Auto Loader support natively?
   - What is the maximum sustainable ingestion throughput?
   - How does it handle schema evolution in industrial sensor data?
   - What is the realistic minimum latency (file landing to Delta)?
   - How does it compare to Kafka source for micro-batch ingestion?
   - Cost model: what drives DBU consumption in streaming workloads?

2. DELTA LIVE TABLES (DLT)
   - What is DLT vs. standard Spark streaming notebooks?
   - How are data quality expectations defined? (EXPECT, EXPECT OR DROP)
   - What are DLT's known limitations? (debugging, cost, flexibility)
   - How does DLT handle late-arriving industrial sensor data?
   - Enhanced vs. Core DLT — what is the feature/cost difference?
   - How do you implement Bronze/Silver/Gold with DLT?

3. DELTA TABLES FOR TIME-SERIES
   - Best partitioning strategy for sensor data (asset_id + date? hour?)
   - ZORDER vs. Liquid Clustering — which for time-series queries?
   - Delta OPTIMIZE VACUUM — how often for high-frequency sensor tables?
   - Time travel for historical anomaly investigation — row limits?
   - Change Data Feed — how does it support streaming feature engineering?
   - What are the query latency characteristics at 10M rows/day scale?

4. DATABRICKS FEATURE STORE
   - Point-in-time lookups — exact mechanics, critical for avoiding
     data leakage in predictive maintenance models
   - Feature serving for real-time vs. batch inference
   - Feature lineage and discoverability within Unity Catalog
   - Limitations: what kinds of features are NOT well-served here?
   - How does Feature Store handle time-series window features?
   - Cross-notebook feature reuse — how does it work in practice?

5. MLFLOW ON DATABRICKS
   - Autologging support: which frameworks? (sklearn, XGBoost, Prophet,
     PyTorch, statsmodels, tsfresh)
   - MLflow Model Registry — promotion lifecycle, approval gates
   - Custom PyFunc models — when needed for industrial AI?
   - Experiment comparison across asset types and plant locations
   - Model retraining triggers via Workflows
   - What CANNOT be tracked easily in MLflow?

6. DATABRICKS MODEL SERVING (MOSAIC AI)
   - Latency profile: p50/p95 for a simple sklearn model endpoint?
   - Autoscaling behavior — cold start time?
   - Cost: DBU/hour for a provisioned model serving endpoint
   - External model integration: Claude, GPT-4o, Gemini via AI Gateway
   - AI Gateway: what models are supported? Rate limiting? Cost control?
   - When to use batch inference vs. online serving for PlantMind?

7. DATABRICKS VECTOR SEARCH
   - Delta Sync Index vs. Direct Vector Access — when to use each?
   - Embedding generation: which Databricks Foundation Model API
     models are available for text embedding? What are their specs?
   - Index creation time for 100K document chunks?
   - Query latency: p50 for a nearest-neighbor search?
   - Hybrid search (semantic + keyword) — is it natively supported?
   - Metadata filtering during vector search — how does it work?
   - What are the known limitations vs. Pinecone or Weaviate?

8. MOSAIC AI AGENT FRAMEWORK
   - What is the Databricks Agent Framework exactly?
   - LangChain on Databricks — what is natively supported?
   - Tool definition pattern — how do agents call Delta SQL, Vector
     Search, and Model Serving in a single reasoning chain?
   - Multi-agent patterns — supervisor agent orchestrating specialists?
   - Human-in-the-loop approval — what is the native pattern?
   - Agent tracing and observability — MLflow tracing?
   - Structured output from LLM agents — how to enforce JSON schema?
   - Known failure modes of LangChain tool-calling in production?

9. UNITY CATALOG
   - Three-level namespace (catalog.schema.table) — how to structure
     for PlantMind multi-plant, multi-client scenario?
   - Delta Sharing — for LTTS sharing PlantMind data with clients?
   - Column-level masking for OT security-sensitive tags?
   - Row-level security across plant locations?
   - Tag-based governance for safety-critical asset data?
   - Data lineage — how granular? Column-level or table-level?
   - Unity Catalog for models and volumes — what does this enable?

10. DATABRICKS LAKEHOUSE MONITORING
    - What drift types are detected natively? (PSI, KS, Chi-square?)
    - Drift detection for time-series anomaly model outputs?
    - Monitoring a model's prediction distribution over time?
    - Alert configuration and notification integration (email, Slack)?
    - Limitations: what monitoring requires external tools?
    - How does it integrate with MLflow model registry?

11. DATABRICKS WORKFLOWS
    - Trigger types: scheduled, file arrival, API, DLT completion?
    - Retry logic and error notification?
    - Job cluster vs. all-purpose cluster cost implications?
    - Dependent task chaining — for PlantMind pipeline orchestration?
    - How to implement a retraining pipeline triggered by drift alert?

12. DATABRICKS SQL / LAKEVIEW DASHBOARDS
    - Serverless SQL vs. SQL warehouse — when to use each?
    - Lakeview dashboards — what visualization types are available?
    - Dashboard alert rules — can they trigger agent workflows?
    - What is NOT possible in Lakeview that requires Streamlit?
    - Performance of Databricks SQL for a plant engineer's ad-hoc query
      on 6 months of sensor data (10M rows, 3 joins)?

OUTPUT FORMAT — DATABRICKS_MAP.md:

PART A: Capability Assessment Table
For each of the 12 capabilities above:
| Capability | PlantMind Use Case | Databricks Service |
| Why Best Choice | Known Limitations | Mitigation |
| Hackathon Demo-ability (H/M/L) | Setup Time (hrs) |

PART B: Framework-to-Databricks Mapping Table
For each of the 7 framework interfaces:
| Interface | Contract Guarantee | Databricks Implementation |
| Justification | Gap/Limitation | Workaround |

PART C: Databricks Solution Accelerator Inventory
List every existing Databricks Solution Accelerator relevant to:
predictive maintenance, manufacturing quality, OEE, energy,
IoT time-series, industrial AI.
For each: name, what it does, whether PlantMind can build on it.

PART D: Known Gaps (Honest Assessment)
What CANNOT Databricks do natively that PlantMind needs?
For each gap: describe, severity (blocking/workaround/minor),
and the specific mitigation PlantMind uses.

PART E: Pricing Model Summary
Key cost drivers for PlantMind on Databricks at scale:
- DLT pipeline: estimated DBU/hour for a medium plant
- MLflow model serving: estimated DBU/hour for always-on endpoint
- Vector Search: cost model for 100K chunks, 100 queries/day
- Workflows: cost for daily retraining job
- Unity Catalog: additional cost or included?

PART F: "Why Databricks" Defense Statement
One paragraph. Answer this judge question: "Why Databricks and not
Snowflake + SageMaker + Pinecone?" Copy-paste ready.

Include at end:
## ARTIFACT QUALITY CHECKLIST
- [ ] All 12 capabilities assessed with limitations noted
- [ ] Framework-to-Databricks mapping is complete
- [ ] Gap assessment is honest (not a sales document)
- [ ] Pricing estimates are realistic (not minimized)
- [ ] "Why Databricks" statement is specific and defensible
```

---

## SECTION 7 — PHASE 4 SUB-PROMPT
### Data Landscape Research
### Recommended Model: Kimi K2 long context (data engineering depth)
### Estimated Time: 60–90 minutes
### Output: DATA_REALITY.md

---

### PASTE THIS INTO YOUR RESEARCH MODEL — START PHASE 4

```
=== PLANTMIND — PHASE 4: DATA LANDSCAPE RESEARCH ===

PROJECT CONTEXT:
PlantMind ingests multi-source industrial data and processes it through
a Bronze/Silver/Gold lakehouse on Databricks. Understanding what data
actually exists in industrial environments — in what format, quality,
volume, and with what integration constraints — is the most underestimated
phase. More industrial AI projects fail from data reality shock than
algorithm problems. This phase must be brutally realistic.

YOUR TASK:
Research the actual data reality in industrial environments.
Produce a data landscape report AND design 10 synthetic datasets for
the hackathon with domain-accurate schemas and sample data.

DATA SOURCE REALITY RESEARCH:

HISTORIAN PLATFORMS (most common in target sectors):
- OSIsoft PI / AVEVA PI System — market share, data format, API
- Aspen InfoPlus.21 / IP.21 — market share, data format, query method
- GE Historian (Proficy) — market share, data format
- Honeywell PHD — market share, data format
- Yokogawa Exaquantum — market share
- What are the standard ways to get data out of each to a cloud lakehouse?
- What is the cost and complexity of each integration path?
- What are the licensing restrictions on data egress?

SCADA SYSTEMS:
- Wonderware (AVEVA) — most common industries?
- Ignition by Inductive Automation — growing market share, open?
- GE iFIX / CIMPLICITY
- Siemens WinCC / WinCC OA
- Honeywell Experion PKS
- Yokogawa CENTUM VP
- Schneider Electric EcoStruxure

CMMS / EAM PLATFORMS:
- IBM Maximo — data model for work orders, assets, failure history
- SAP PM (Plant Maintenance) — data structures, integration complexity
- Oracle EAM — data structures
- Infor EAM (formerly Datastream)
- Hexagon EAM (formerly Intergraph)
- What does a typical CMMS work order record contain?

INDUSTRIAL DATA PROTOCOLS:
- OPC-UA: what data can be accessed? What is the cloud bridge path?
- OPC-DA: legacy, still how common in 2024-2025?
- MQTT: how common in modern industrial IoT? Which platforms?
- MODBUS: prevalence in legacy equipment
- PROFINET / PROFIBUS: scope of data accessible
- EtherNet/IP: prevalence in manufacturing

DOCUMENT STORAGE FOR ENGINEERING KNOWLEDGE:
- Where do P&IDs live? (PDF, SVG, paper scans, AutoCAD, Visio)
- Where do SOPs live? (SharePoint, Documentum, paper binders, PDF)
- Where do equipment manuals live? (OEM provided, scan archives)
- Where does FMEA / FMECA data live? (Excel, dedicated software, CMMS)
- Where does failure history narrative live? (CMMS comments, emails, nowhere)

DATA QUALITY REALITY (quantified where possible):
- What % of industrial sensor readings are missing, null, or stuck?
- What is the "stuck sensor" failure rate in process plants?
- How common is timestamp misalignment between systems?
- What engineering unit inconsistencies are most common?
- How is asset tag naming inconsistency documented and estimated?
- What is the realistic data completeness for maintenance records?
  (% of work orders with root cause documented, failure mode coded)

DATA VOLUME ESTIMATES:
For a medium-sized petrochemical plant with:
- 10,000 active sensor tags at 1-minute sampling frequency
- 50,000 tags at 1-hour sampling
- 2,000 work orders/year
- 5,000 alarm events/day
Calculate:
- Annual row count for sensor_readings table
- Annual storage in GB (Delta Parquet format estimate)
- Annual storage cost on Databricks (estimate)
- Query time for "get last 30 days of data for 100 tags" on Delta

OT/IT INTEGRATION PATTERNS:
- Purdue model (ISA-95) — what are the data diode constraints?
- DMZ patterns for historian data replication to cloud
- PI Cloud Connect / PI Web API → cloud lakehouse patterns
- AWS Greengrass, Azure IoT Hub, GCP IoT Core — which is most common
  in industrial settings?
- Typical time to connect a new plant to a cloud data platform
  (realistic range from industry experience)
- Security constraints: what data CAN leave the plant? What cannot?

SYNTHETIC DATASET DESIGN:
For each of the 10 datasets below, produce:
- Full schema: column name | data type | description |
  realistic value range | nullable | notes
- 20 sample rows with domain-accurate values
  (not random — use real industrial value ranges)
- 3 intentional data quality issues embedded
  (to demonstrate the Data Quality Agent)
- Partitioning recommendation for Delta
- Expected row count for a medium plant over 90 days
- Foreign key relationships to other datasets

DATASET 1: asset_master
  Purpose: Master registry of all plant assets/equipment
  Key columns include: asset_id, asset_name, asset_class, asset_type,
  manufacturer, model, install_date, plant_id, unit_id, criticality_class,
  design_pressure, design_temperature, rated_power_kw, last_inspection_date,
  maintenance_strategy (reactive/preventive/predictive), sap_floc

DATASET 2: sensor_readings
  Purpose: High-frequency sensor time-series from historians
  Key columns: reading_id, asset_id, tag_id, tag_name, timestamp,
  value, engineering_unit, quality_code, source_historian, plant_id
  Note: embed stuck sensor values, missing readings, and unit errors

DATASET 3: alarm_logs
  Purpose: DCS/SCADA alarm and event log
  Key columns: alarm_id, asset_id, tag_id, alarm_type, priority,
  alarm_text, set_timestamp, clear_timestamp, duration_sec,
  operator_acknowledged, operator_comment, plant_id
  Note: embed alarm flood scenario (>50 alarms in 10 min)

DATASET 4: maintenance_workorders
  Purpose: CMMS work order records
  Key columns: wo_id, asset_id, wo_type (corrective/preventive/predictive),
  priority, description, requested_date, planned_date, completed_date,
  actual_duration_hr, technician_id, failure_code, cause_code,
  action_taken (free text), parts_used, labor_cost, downtime_hr

DATASET 5: failure_history
  Purpose: Historical equipment failure events with cause and resolution
  Key columns: failure_id, asset_id, failure_date, failure_mode,
  failure_class (mechanical/electrical/instrument/process/external),
  root_cause_code, root_cause_description (free text), detection_method,
  lead_time_to_failure_hr, downtime_hr, production_loss_units,
  financial_impact_usd, corrective_action, recurrence_flag

DATASET 6: energy_consumption
  Purpose: Energy metering data at asset and unit level
  Key columns: meter_id, asset_id, unit_id, timestamp, interval_min,
  kwh_consumed, peak_demand_kw, power_factor, steam_consumption_kg,
  compressed_air_nm3, baseline_kwh, variance_pct, shift_code, plant_id
  Note: embed 3 energy anomaly spikes correlated with production events

DATASET 7: production_oee
  Purpose: OEE components at production line level
  Key columns: oee_id, line_id, plant_id, shift_date, shift_code,
  planned_production_time_hr, actual_run_time_hr, total_downtime_hr,
  scheduled_downtime_hr, unscheduled_downtime_hr, ideal_cycle_time_sec,
  actual_cycle_time_sec, total_units_produced, good_units, defect_units,
  availability_pct, performance_pct, quality_pct, oee_pct

DATASET 8: quality_defects
  Purpose: Product quality inspection and defect records
  Key columns: defect_id, asset_id, line_id, inspection_point
  (in-process/end-of-line/customer), defect_code, defect_description,
  severity (critical/major/minor), detection_date, batch_id,
  process_parameter_1..5 (values at time of defect), rework_required,
  scrap_cost_usd, corrective_action, root_cause_category

DATASET 9: engineering_documents_metadata
  Purpose: Index of engineering knowledge documents for RAG
  Key columns: doc_id, doc_title, doc_type (SOP/manual/P&ID/FMEA/
  alarm_response/engineering_spec), asset_class, asset_id (if specific),
  plant_id (if specific), revision_date, author, file_path,
  chunk_count, last_embedded_date, language, status (active/superseded)

DATASET 10: sop_document_chunks
  Purpose: Chunked text from SOPs and manuals for vector embedding
  Key columns: chunk_id, doc_id, chunk_sequence, chunk_text,
  asset_class, asset_id, procedure_type, safety_criticality,
  keyword_tags, embedding_model, embedded_at

OUTPUT FORMAT — DATA_REALITY.md:

PART A: Data Source Taxonomy by Sector
PART B: Protocol and Format Reference Table
PART C: Data Quality Profile (issues, rates, mitigations)
PART D: Data Volume Estimates (medium plant, 90-day horizon)
PART E: OT/IT Integration Architecture Patterns (top 3)
PART F: Synthetic Dataset Specifications (all 10, full schema + 20 rows each)
PART G: Data Assumptions Register
  (what we assume for hackathon vs. production reality, for each assumption)

Include at end:
## ARTIFACT QUALITY CHECKLIST
- [ ] All 10 datasets have full schema
- [ ] All datasets have 20 sample rows with realistic values
- [ ] Each dataset has 3 embedded quality issues documented
- [ ] All integration patterns are real (not invented)
- [ ] Data volume estimates are calculated with shown workings
```

---

## SECTION 8 — PHASE 5 SUB-PROMPT
### ROI & Business Case Research
### Recommended Model: Perplexity Deep Research or Kimi K2
### Estimated Time: 45–60 minutes with live citations
### Output: ROI_BENCHMARKS.md

---

### PASTE THIS INTO YOUR RESEARCH MODEL — START PHASE 5

```
=== PLANTMIND — PHASE 5: ROI & BUSINESS CASE RESEARCH ===

PROJECT CONTEXT:
PlantMind is an Engineering Intelligence framework for industrial assets
built by LTTS on Databricks. Every ROI claim in the hackathon pitch must
be backed by cited, defensible numbers. Judges will challenge ROI claims.
Have the sources ready before the pitch.

CRITICAL INSTRUCTION:
Do NOT make up numbers. Do NOT use round numbers without citation.
Mark every figure with its source. If you cannot find a source, mark it
[INFERRED — no source found] and give your reasoning.

RESEARCH MANDATE:
Find real, cited business impact figures for industrial AI and predictive
maintenance deployments. Use analyst reports, vendor case studies, academic
papers, government energy reports, and documented enterprise deployments.

SECTION 1: DOWNTIME COST BENCHMARKS
Research and cite the cost per hour of unplanned downtime for:
- Oil refinery / Crude distillation unit
- Petrochemical / Ethylene cracker
- Chemical plant (specialty chemicals)
- Automotive assembly line
- Semiconductor fab (200mm and 300mm)
- Power generation plant (gas turbine, coal, nuclear)
- Pulp and paper mill
- Food and beverage processing
- Pharmaceutical manufacturing (GMP facility)
Primary sources to check: Aberdeen Group, Senseye/Siemens 2022 "The True
Cost of Downtime" study, Emerson Process Management survey, McKinsey
manufacturing reports, Plant Engineering magazine surveys

SECTION 2: PREDICTIVE MAINTENANCE ROI BENCHMARKS
Research and cite all of the following:
- Average reduction in unplanned downtime: predictive vs. reactive (%)
- Average reduction in total maintenance costs: condition-based vs. time-based (%)
- Average extension of asset life from predictive maintenance program (%)
- Typical ROI timeline (months to positive ROI)
- Typical 3-year ROI multiple from predictive maintenance programs
- Cost of predictive maintenance programs per asset or per plant
- Success rate of predictive maintenance implementations
  (what % of pilots scale to production?)
Sources: McKinsey "Predictive Maintenance", Deloitte, ARC Advisory,
Verdantix, LNS Research, documented vendor case studies (GE, Emerson,
ABB, Siemens, AspenTech)

SECTION 3: ENERGY OPTIMIZATION ROI BENCHMARKS
Research and cite:
- Average energy waste % in process industries (petrochem, chemical, refining)
- Average savings from AI-driven energy optimization (% of energy bill)
- Typical payback period for industrial energy management systems
- Carbon credit / ESG premium value of energy reduction
- Value of ISO 50001 certification for industrial companies
- Cost of EU ETS compliance for a mid-size European petrochemical plant
Sources: IEA Energy Efficiency reports, DOE Better Plants program,
Schneider Electric case studies, Emerson energy management white papers,
ENERGY STAR Industrial reports

SECTION 4: OEE IMPROVEMENT BENCHMARKS
Research and cite:
- World-class OEE benchmark (by industry: process vs. discrete)
- Average OEE in petrochemical process manufacturing (%)
- Average OEE in automotive discrete manufacturing (%)
- Typical OEE improvement from AI-driven production intelligence (%)
- Financial value of 1% OEE improvement for a medium-sized plant ($)
- Value of shifting from reactive downtime response to predictive ($)
Sources: LNS Research, Manufacturing.net OEE benchmarks,
Siemens/Aveva OEE case studies, ISA technical papers

SECTION 5: QUALITY INTELLIGENCE ROI BENCHMARKS
Research and cite:
- COPQ (Cost of Poor Quality) as % of revenue by sector
- Defect reduction from AI-driven in-process quality intelligence (%)
- Value of shifting detection from end-of-line to in-process
- Cost of a quality escape to a downstream OEM customer ($)
- Cost of a product recall in automotive and pharma ($)
- First-time yield improvement from AI-assisted process control (%)
Sources: ASQ Quality Progress, Aberdeen Group quality reports,
J.D. Power, AIAG quality cost studies

SECTION 6: KNOWLEDGE MANAGEMENT ROI BENCHMARKS
Research and cite:
- Cost of tribal knowledge loss per retiring senior engineer ($)
- Time spent searching for engineering information per engineer per day (hrs)
- Time saved with AI-assisted knowledge retrieval vs. manual (%)
- Time-to-competency reduction for new engineers with AI knowledge base
- Value of capturing "golden batch" knowledge in process manufacturing
Sources: Deloitte human capital research, McKinsey knowledge management,
IDC "information worker" productivity studies

SECTION 7: PLANTMIND COMPOSITE ROI MODEL
Build a 3-year ROI model for a reference case:
  Reference plant: Medium petrochemical plant
  - Plant value: $500M replacement cost
  - Annual revenue: $200M
  - Number of critical assets: 500
  - Current OEE: 74%
  - Current maintenance spend: $8M/year
  - Current unplanned downtime incidents: 12/year, avg 8 hours each
  - Current energy bill: $15M/year

For each of 5 value levers, calculate:
  Conservative case (cite source for assumption)
  Base case (cite source for assumption)
  Optimistic case (cite source for assumption)

Value Levers:
1. Unplanned downtime reduction (use downtime cost from Section 1)
2. Maintenance cost reduction (use benchmark from Section 2)
3. OEE improvement (use benchmark from Section 4)
4. Energy savings (use benchmark from Section 3)
5. Quality improvement (use benchmark from Section 5)

Then calculate:
- Annual value: Conservative / Base / Optimistic ($)
- PlantMind platform cost estimate (research SaaS pricing comps)
- Net annual benefit
- 3-year NPV at 10% discount rate
- Payback period in months

SECTION 8: ROI CLAIM DEFENSIBILITY MATRIX
For each key ROI claim in the pitch deck:
| Claim | Stated Figure | Source | Confidence Level |
| How to Defend to a Judge | What to Say if Challenged |

OUTPUT FORMAT — ROI_BENCHMARKS.md:

Part A: Downtime Cost Database (table, cited)
Part B: Predictive Maintenance ROI Database (table, cited)
Part C: Energy Optimization ROI Database (table, cited)
Part D: OEE Improvement ROI Database (table, cited)
Part E: Quality Intelligence ROI Database (table, cited)
Part F: Knowledge Management ROI Database (table, cited)
Part G: PlantMind Composite ROI Model (full calculation, shown workings)
Part H: ROI Defensibility Matrix

Include at end:
## ARTIFACT QUALITY CHECKLIST
- [ ] Every figure has a source citation or [INFERRED] flag
- [ ] Composite ROI model shows calculation workings
- [ ] All industry-specific figures are matched to correct sector
- [ ] No round numbers without justification
- [ ] Defensibility matrix covers all pitch deck claims
```

---

## SECTION 9 — PHASE 6 SYNTHESIS PROMPT
### Architecture Lock
### Use: Paste this + all 5 artifact outputs into Claude Opus/Sonnet
### Output: ARCHITECTURE_LOCK.md

*(Use the SYNTHESIS PROTOCOL defined in Section 3 above.
Paste all 5 artifacts before this prompt.)*

```
=== PLANTMIND — PHASE 6: ARCHITECTURE LOCK (SYNTHESIS) ===

You are now synthesizing 5 research artifacts into a locked architecture
document. The 5 artifacts are attached above this prompt.

PROJECT IDENTITY (canonical — do not deviate):
PlantMind is a two-layer Engineering Intelligence framework:
  Layer 0: Tool-agnostic framework with 7 interface contracts (the IP)
  Layer 1: Databricks-native Tier-1 reference implementation (the demo)

Pitch: "PlantMind is an open Engineering Intelligence framework.
We built the Tier-1 reference implementation on Databricks — because
Databricks provides the tightest native integration between lakehouse,
ML lifecycle, vector search, and agentic AI for industrial use cases."

TASK 1 — VALIDATION GATE:
For each of PlantMind's 8 major capabilities below, run the 5-gate check.
If any gate fails, flag it [GATE FAIL — RESOLVE BEFORE BUILD].

Capabilities to validate:
1. Real-time anomaly detection per asset
2. Agentic root cause analysis with source citation
3. Natural language maintenance recommendation generation
4. Engineering knowledge RAG (manuals, SOPs, failure logs)
5. Energy optimization insights
6. OEE intelligence and bottleneck detection
7. Human-in-the-loop approval with audit trail
8. Feedback loop: outcome → model retraining

Gates per capability:
  Gate 1: Maps to pain ID in PAIN_REGISTER (cite it)
  Gate 2: Differentiated from competitors in COMPETITIVE_MAP (cite gap)
  Gate 3: Has Databricks implementation in DATABRICKS_MAP (cite service)
  Gate 4: Has data source in DATA_REALITY (cite dataset)
  Gate 5: Has ROI benchmark in ROI_BENCHMARKS (cite figure + source)

TASK 2 — LAYER 0 FRAMEWORK DOCUMENTATION:
For each of the 7 interface contracts, write a technical specification:
  - Interface name and purpose
  - Method signatures (pseudocode)
  - Input/output contracts
  - Quality guarantees (latency, reliability, explainability)
  - What the interface must NOT do (constraints)
  - How a non-Databricks implementation would satisfy this interface

TASK 3 — LAYER 1 DATABRICKS IMPLEMENTATION:
For each interface:
  - Exact Databricks service used
  - Why it is the best fit (reference DATABRICKS_MAP evidence)
  - Known limitation and mitigation
  - Configuration notes for hackathon setup

TASK 4 — ARCHITECTURE DIAGRAMS:
Produce in both Mermaid and ASCII:
Diagram A: Full system architecture (data flow)
Diagram B: Agent interaction diagram (8 agents)
Diagram C: Bronze/Silver/Gold pipeline (DLT)
Diagram D: RAG pipeline (document → chunk → embed → index → retrieve)

TASK 5 — AGENT DESIGN SPECIFICATIONS:
For each of the 8 agents, use this exact template:

  AGENT: [Name]
  PURPOSE: [One sentence — what problem does this agent solve?]
  TRIGGER: [Event/schedule/API call that activates this agent]
  LAYER 0 INTERFACE: [Which framework interface this agent implements]
  LAYER 1 DATABRICKS TOOLS:
    Tool 1: [Databricks service + purpose]
    Tool 2: [Databricks service + purpose]
    Tool 3: [Databricks service + purpose]
  REASONING CHAIN:
    Step 1: [What does the agent retrieve? From where? Why?]
    Step 2: [How does it process or correlate? What logic?]
    Step 3: [How does it generate the recommendation?]
    Step 4: [How does it validate and confidence-score?]
    Step 5: [How does it decide human approval is needed?]
  OUTPUT SCHEMA (JSON):
    {
      "recommendation_id": "string",
      "asset_id": "string",
      "agent_name": "string",
      "recommendation_text": "string",
      "confidence_score": 0.0-1.0,
      "confidence_method": "string",
      "supporting_evidence": ["citation_1", "citation_2"],
      "retrieved_doc_chunks": ["chunk_id_1", "chunk_id_2"],
      "requires_human_approval": boolean,
      "approval_threshold": 0.0-1.0,
      "estimated_business_impact": "string",
      "generated_at": "ISO timestamp",
      "audit_delta_table": "plantmind_gold.agent_audit_log"
    }
  EXAMPLE OUTPUT: [One realistic example recommendation paragraph]

  Agents to specify:
  1. Data Quality Agent
  2. Asset Health Agent
  3. Root Cause Analysis Agent ← HERO AGENT
  4. Energy Optimization Agent
  5. OEE Intelligence Agent
  6. Quality Intelligence Agent
  7. Maintenance Planner Agent
  8. Executive Summarizer Agent

TASK 6 — DELTA PIPELINE DESIGN:
For each pipeline stage, define:
  Bronze layer:
    - Table names (plantmind_bronze.*)
    - Source type (Auto Loader cloudFiles)
    - DLT expectation rules (min 3 per table)
    - Partitioning
    - Trigger / schedule

  Silver layer:
    - Table names (plantmind_silver.*)
    - Transformation logic (cleaning, typing, standardization)
    - DLT expectation rules (min 3 per table)
    - What the Data Quality Agent checks here

  Gold layer:
    - Table names (plantmind_gold.*)
    - Feature engineering logic
    - ML scoring output tables
    - Agent audit log table
    - Partitioning for query performance

TASK 7 — MVP SCOPE TABLE:
| Feature | Priority | Effort (hrs) | Demo-critical? | Owner |
|---|---|---|---|---|
Must-Have / Should-Have / Could-Have / Out of Scope

TASK 8 — HOUR-BY-HOUR EXECUTION PLAN:
Day 1 (10 hours): Setup → Data → Pipeline → ML → RAG → Core Agent
Day 2 (10 hours): UI → Dashboard → Integration → Demo → Pitch

For each hour block: task, tool, expected output, risk, backup plan.

TASK 9 — PATENT/IDF CONCEPTS:
5 innovation claims based on the architecture just locked.
For each: title, claim statement, what makes it novel,
prior art that exists and how this differs.
```

---

## SECTION 10 — GOVERNANCE CONSTRAINTS
### (Embed in every agent and build artifact)

```
PLANTMIND SAFETY CONSTRAINTS — NON-NEGOTIABLE:

C1: NO AUTONOMOUS ACTION ON SAFETY-CRITICAL SYSTEMS
  PlantMind recommends. It never executes physical commands.
  All actions on safety-critical assets require explicit human approval.
  UI must make this unmistakably clear.

C2: CONFIDENCE THRESHOLD
  Confidence < 0.60 → displayed as "Requires Expert Review"
  Confidence < 0.40 → not displayed; logged to audit only
  Confidence ≥ 0.80 → displayed as "High Confidence Recommendation"
  Threshold is configurable per asset criticality class.

C3: SOURCE GROUNDING IS MANDATORY
  Every LLM-generated claim must cite its source:
  (Delta table row ID, document chunk ID, or historical failure ID)
  If LLM cannot cite a source, it cannot make the claim.
  "Grounding score" is a required output field.

C4: IMMUTABLE AUDIT TRAIL
  Every agent recommendation + its full context (inputs, retrieved chunks,
  LLM response, confidence score, human decision) → append-only Delta table.
  This table is never deleted. Unity Catalog governs access.

C5: FAILURE MODE IS CONSERVATIVE
  If agent system fails (timeout, model error, retrieval failure):
  Default output = "Manual review required — AI system unavailable"
  NEVER return a degraded or partially-grounded response.

C6: EXPLAINABILITY OVER PERFORMANCE
  Where a complex model outperforms a simple model by <5% AUC but
  the simple model is more explainable: choose simple.
  Plant engineers must trust the system. Trust requires explanation.

C7: LAYER 0 GOVERNANCE INTERFACE
  GovernanceInterface guarantees:
  - Full data lineage (sensor → feature → model → recommendation)
  - Role-based access (plant engineer sees own plant only)
  - Safety-critical tags masked from unauthorized access
  - All PII-adjacent data (operator IDs) anonymized in demo
```

---

## SECTION 11 — ARTIFACT REGISTRY
### Track completion status across models

| Artifact | Phase | Model | Status | Location |
|---|---|---|---|---|
| PAIN_REGISTER.md | 1 | Kimi K2 | ☐ Pending | |
| COMPETITIVE_MAP.md | 2 | Kimi K2 | ☐ Pending | |
| DATABRICKS_MAP.md | 3 | GLM 5.2 | ☐ Pending | |
| DATA_REALITY.md | 4 | Kimi K2 | ☐ Pending | |
| ROI_BENCHMARKS.md | 5 | Perplexity | ☐ Pending | |
| ARCHITECTURE_LOCK.md | 6 | Claude | ☐ Pending | |
| synthetic_data_gen.py | Build-A | Claude | ☐ Pending | |
| dlt_pipeline.py | Build-A | Claude | ☐ Pending | |
| feature_engineering.py | Build-B | Claude | ☐ Pending | |
| anomaly_detection.py | Build-B | Claude | ☐ Pending | |
| vector_search_setup.py | Build-C | Claude | ☐ Pending | |
| root_cause_agent.py | Build-C | Claude | ☐ Pending | |
| streamlit_app.py | Build-C | Claude | ☐ Pending | |
| DEMO_SCRIPT.md | Comms | Claude | ☐ Pending | |
| PITCH_DECK.pptx | Comms | Claude | ☐ Pending | |
| QA_PLAYBOOK.md | Comms | Claude | ☐ Pending | |

---

## SECTION 12 — JUDGE Q&A PLAYBOOK SKELETON
### Expand after Phase 6 is locked

**Q: "Why Databricks?"**
Foundation: See DATABRICKS_MAP Part F "Why Databricks Defense Statement"
PlantMind framing: "We chose Databricks as our Tier-1 implementation
because no other platform natively unifies [fill from DATABRICKS_MAP].
And critically — PlantMind's framework is not locked to it. Layer 0
interfaces mean a client on Snowflake + SageMaker can run the same
framework. But for this hackathon, and for LTTS's Databricks partnership,
Databricks is the right and best runtime."

**Q: "What makes this better than AspenTech?"**
Foundation: See COMPETITIVE_MAP Part D (gap analysis) and Part E (diff statement)
Answer built from: [gap IDs + PlantMind capabilities]

**Q: "How do you handle hallucination?"**
Foundation: See Governance Constraints C2, C3, C4
Answer: Three controls: source grounding requirement, confidence threshold,
immutable audit trail. If the LLM cannot cite a source, it cannot speak.

**Q: "What data did you use?"**
Foundation: See DATA_REALITY Part G (assumptions register)
Answer: Synthetic data generated using domain-accurate distributions from
industrial engineering references. Modeled on OSIsoft PI historian structure.
Embedded real failure patterns from published case studies.

**Q: "Is this actually new? AspenTech does predictive maintenance."**
Foundation: COMPETITIVE_MAP Part C (positioning) + Part D (gaps)
Answer: "AspenTech does detection. PlantMind does reasoning. Detection says
'something is wrong.' PlantMind says 'here is the root cause, here is the
SOP page, here is the work order, here is the business impact — and here
is the audit trail of how I concluded that.' That's the gap."

**Q: "How does this scale to 50 plants?"**
Foundation: DATABRICKS_MAP Part A (Unity Catalog, Vector Search scaling)
Answer: [built from capability assessment after Phase 3 complete]

---

*End of PLANTMIND_MASTER_RESEARCH_PROMPT_v2.md*
*Version 2.0 | Multi-Model Parallel Execution | LTTS × Databricks*
*Start with Parallel Group A. Synthesize in Phase 6. Build only after lock.*
