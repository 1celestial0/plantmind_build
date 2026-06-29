# Model API Registry — all external models in one place

> Add a row before wiring any new model. Never hardcode API choices in agent files without an entry here.

---

## Registry

| ID | Provider | Model | Use case | Lane | Config key | Fallback | Status |
|---|---|---|---|---|---|---|---|
| `narrative-primary` | Groq | Llama 3.3 70B | Götze reason, agent narrative | 1 | `GROQ_API_KEY` | Templated string per action | [PLANNED] |
| `summary-fast` | Groq | Llama 3.2 3B | DataSentinel type labels, summaries | 1 | `GROQ_API_KEY` | Rule-based label | [PLANNED] |
| `reasoning-heavy` | DeepSeek | R1 | RootCauseAnalyst causal chains | 1 | `DEEPSEEK_API_KEY` | Groq 70B | [PLANNED] |
| `embeddings-local` | sentence-transformers | all-MiniLM-L6-v2 | RAG embeddings | 2 | — (local) | — | [PLANNED] |
| `architect-docs` | Anthropic | Claude | Architecture / IP writing only | ops | — | — | [ACTIVE via IDE] |
| `rul-ml-v1` | scikit-learn | RandomForest | v1 FORGE RUL (legacy) | — | — | — | [BUILT in FORGE] |
| `health-physics-v2` | scipy | Weibull analytical | v2 health + RUL | 2 | `plant_config.yaml` | — | [PLANNED] |
| `health-stretch` | PyTorch | PINN | Optional RUL refinement | 2 | — | Weibull baseline | [STRETCH] |

---

## How to add a new model

1. **Add a row** to the table above with ID, provider, use case, lane, config key, fallback.
2. **Add env var** to `.env.example` (never commit `.env`).
3. **Create adapter** in `src/agents/_llm.py` or `src/rag/_embeddings.py` — one function per registry ID.
4. **Document limits** (rate, cost, context window) in this file under the row.
5. **Update** `LOCKED_STATE.md` §5 stack only if it's a locked production choice.

---

## Adapter pattern (code convention)

```python
# src/agents/_llm.py
# Registry ID: narrative-primary

def call_narrative_primary(prompt: str) -> str:
    """Route through MODEL-REGISTRY id `narrative-primary`. Fallback: template."""
    ...
```

Agents import registry functions — never `openai.Client()` directly in agent files.

---

## Environment template

See `.env.example` at project root. Copy to `.env` locally.

```ini
GROQ_API_KEY=
DEEPSEEK_API_KEY=
CHROMA_PERSIST_DIR=ml/data/chroma
PLANT_CONFIG=src/physics/plant_config.yaml
```

---

## v1 note

FORGE uses deterministic G-score (no LLM in decision path). v2 adds LLM for **narrative only** — IIS math stays deterministic per `LOCKED_STATE`.