# DATABRICKS_MAP.md
## PlantMind — Phase 3: Databricks Capability Deep-Dive
**Research Date:** 2026-06-30  
**Model Used:** Synthesis from LOCKED_STATE, CONSOLIDATED-PROJECT-BLUEPRINT, LTTS×Databricks partnership (2026-06-11)  
**Status:** Hackathon reference — verify GA features at build time

---

## PART A: Capability Assessment Table

| Capability | PlantMind Use Case | Databricks Service | Why Best Choice | Known Limitations | Mitigation | Demo (H/M/L) | Setup (hrs) |
|------------|-------------------|-------------------|-----------------|-------------------|------------|--------------|-------------|
| 1. Streaming ingest | OT sensor files, historian exports | Auto Loader + Structured Streaming | Native Delta landing, schema evolution | Not sub-second OT; file latency | Micro-batch + buffer table | M | 4 |
| 2. Medallion pipeline | Bronze/Silver/Gold sensor quality | Delta Live Tables (DLT) | EXPECT constraints, lineage | Debugging harder than notebooks | Hybrid: DLT Silver + notebook Gold | M | 6 |
| 3. Time-series storage | 10M rows/day sensor history | Delta + Liquid Clustering | Z-order/cluster on asset_id+date | Vacuum schedule discipline | OPTIMIZE weekly job | H | 3 |
| 4. Feature engineering | Rolling windows, RUL labels | Feature Store | Point-in-time lookups anti-leakage | Window features need batch materialization | Offline store + on-demand compute | M | 8 |
| 5. Model lifecycle | Weibull + anomaly models | MLflow | Registry, autolog sklearn | Custom physics PyFunc needed | Wrap Weibull as PyFunc | H | 4 |
| 6. Online inference | Health score API | Model Serving (Mosaic AI) | Unity Catalog integration | Cold start latency | Warm endpoint + batch fallback | L | 6 |
| 7. RAG / manuals | RootCauseAnalyst corpus | Vector Search + FM API | Delta Sync indexes | Hybrid search less mature than dedicated DB | Metadata filters per asset_class | M | 8 |
| 8. Agent orchestration | 5-agent LangGraph flow | Mosaic AI Agent Framework | Tool routing to SQL/VS/Serving | LangChain tool reliability | Deterministic IIS path outside LLM | M | 12 |
| 9. Governance | Multi-plant catalog | Unity Catalog | Lineage, masking, sharing | Row-level security config overhead | Catalog per client schema | H | 4 |
| 10. Drift monitoring | Model + sensor drift | Lakehouse Monitoring | PSI/KS on predictions | Time-series drift needs custom jobs | Workflows trigger retrain | L | 6 |
| 11. Orchestration | Retrain, scenario batch | Workflows | Depends on DLT completion | Job cluster spin-up delay | Job clusters sized for hackathon | M | 4 |
| 12. BI / exec view | ExecutiveSummarizer rollup | Databricks SQL + Lakeview | SQL on Gold tables | Less custom UX than Streamlit | Streamlit for hackathon; Lakeview prod | M | 4 |

---

## PART B: Framework-to-Databricks Mapping

| Interface | Contract Guarantee | Databricks Implementation | Justification | Gap | Workaround |
|-----------|-------------------|---------------------------|---------------|-----|------------|
| IngestorInterface | Schema-validated ingest | Auto Loader → Bronze Delta | Handles evolving OT schemas | Real-time OPC-UA | Edge gateway + file drop |
| FeatureStoreInterface | PIT-correct features | Databricks Feature Store | Prevents RUL leakage | Complex window features | Materialized feature tables |
| AnomalyModelInterface | Scored anomalies | MLflow + Model Serving | Versioned models | Sub-100ms SLA | Batch scoring + cache |
| KnowledgeRetriever | Cited retrieval | Vector Search + UC volumes | Manuals in Delta | PDF parsing quality | Pre-chunked corpus |
| AgentOrchestrator | Typed agent flow | Mosaic AI + LangGraph adapter | Human-in-loop hooks | Tool-call failures | IIS deterministic core |
| GovernanceInterface | Immutable audit | Unity Catalog + audit Delta | Lineage to source | Column-level OT tags | Tag-based policies |
| FeedbackLoopInterface | Outcome → retrain | Delta outcomes + Workflows | Closed loop narrative | Label delay in plants | Synthetic outcomes demo |

**PlantMind hackathon contracts (LOCKED_STATE §4):** `src/contracts/` maps to Gold tables + JSON API responses.

---

## PART C: Solution Accelerator Inventory

| Accelerator | Relevance | PlantMind Use |
|-------------|-----------|---------------|
| Predictive Maintenance (Databricks) | High | Weibull + feature pipeline template |
| Manufacturing OEE | Medium | Fleet health narrative |
| IoT Time Series | High | Sensor ingest patterns |
| LLM RAG Chatbot | Medium | RootCauseAnalyst pattern |
| Quality Analytics | Low (hackathon) | Post-hackathon Quality Intelligence segment |

---

## PART D: Known Gaps (Honest)

| Gap | Severity | Mitigation |
|-----|----------|------------|
| Sub-second OT closed-loop | Workaround | PlantMind recommends; human approves; CMMS executes |
| Full OPC-UA native ingest | Workaround | Historian export → Auto Loader |
| PINN training on CE free tier | Minor | Analytical Weibull ships first (LOCKED) |
| Always-on serving cost | Workaround | Batch inference for demo; serving for pilot |

---

## PART E: Pricing Model Summary [ESTIMATE]

| Workload | Driver | Medium plant estimate |
|----------|--------|----------------------|
| DLT pipeline | DBU × pipeline hours | 8–15 DBU/hr during ingest windows |
| Model Serving | Provisioned endpoint | 4–8 DBU/hr if always-on |
| Vector Search | Storage + queries | Low at 100K chunks / 100 queries/day |
| Workflows | Daily retrain job | 1–2 DBU per run |
| Unity Catalog | Included in platform | No separate line item |

---

## PART F: "Why Databricks" Defense Statement

PlantMind needs one platform where sensor lakehouse, feature lineage, model registry, vector RAG, and agent orchestration share Unity Catalog governance — not Snowflake for SQL plus SageMaker for ML plus Pinecone for RAG with three security models. LTTS and Databricks announced Industrial AI partnership (2026-06-11) across predictive reliability, OEE, and quality — PlantMind is the reference implementation of that joint story.

---

## ARTIFACT QUALITY CHECKLIST

- [x] All 12 capabilities assessed with limitations noted
- [x] Framework-to-Databricks mapping complete
- [x] Gap assessment honest
- [x] Pricing estimates flagged [ESTIMATE]
- [x] "Why Databricks" statement specific and defensible