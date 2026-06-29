# Obsidian KB Mastery + Dataview Deep Dive
**Purpose:** Turn Obsidian into a living second brain for PlantMind — learn faster, build better, patent stronger
**Version:** 1.0 · 2026-06-20

---

## PART 1: OBSIDIAN AS A LEARNING SYSTEM

### The Mental Model

Obsidian is not a note-taking app. It is a **knowledge graph** where every idea is a node and every `[[link]]` is an edge. Your job is not to write notes — it is to build a *navigable map of how you think*.

```
Conventional notes          Obsidian KB
─────────────────          ────────────
Linear, chronological   →  Graph, by concept
Isolated entries        →  Everything connects
Hard to retrieve        →  Click to traverse
Forgotten after writing →  Re-surfaces via links
```

### The PlantMind KB Architecture

Open your vault at `PlantMind/Knowledge Graph/`. The structure:

```
_Index.md            ← Start here every session (Map of Content)
Concepts/            ← "What is X?" nodes
Architecture/        ← "How does Layer N work?" nodes  
Decisions/           ← "Why did we choose X over Y?" nodes
Patents/             ← "What can we claim?" nodes
Technology/          ← "How does Tool T work?" nodes
Research/            ← NEW: Papers, datasets, repos (add as you learn)
```

**Rule:** Every time you learn something non-obvious, add a node. Every time you make a decision, add a Decision node. The KB is a patent log as much as a knowledge store.

---

## PART 2: THE OBSIDIAN LEARNING LOOP

### How to use Obsidian to actually learn faster

**When you read a paper:**
1. Create `Research/Paper - [Title].md`
2. Fill: WHAT it claims, HOW it proves it, WHY it matters to PlantMind, PRIOR ART it cites
3. Link to existing nodes: `This challenges [[Counterfactual Proof]] because...`
4. Tag: `#paper #rul #xai #prior-art`

**When you learn a concept:**
1. Create `Concepts/[Concept].md`
2. Write: 5W header, mechanism, connections, what breaks if you remove it
3. Link forward (what this enables) and backward (what this depends on)

**When you make an engineering decision:**
1. Create `Decisions/Decision - [Topic].md`
2. Fill: chosen path, alternatives table, why-not for each alternative
3. This is your *patent diary* — the decision is dated by file creation time

**When you find a dataset:**
1. Create `Research/Dataset - [Name].md`
2. Fill: source URL, size, sensors/features, target variable, download command, why relevant to PlantMind

---

## PART 3: OBSIDIAN GRAPH NAVIGATION

### Opening the Graph

`Ctrl+G` → opens the full graph view
`Ctrl+Shift+G` → opens local graph (connections of current note)

### Graph Filters (power user)

In graph view → Filters panel:
- **Tag filter:** type `#core-ip` → see only IP-critical nodes
- **Orphan filter:** find unlinked nodes (ideas not yet connected)
- **Folder filter:** isolate just `Architecture/` or just `Decisions/`

### Key Shortcuts

| Action | Shortcut |
|---|---|
| Open graph | Ctrl+G |
| Follow link | Ctrl+click |
| Back-link panel | Ctrl+Shift+B |
| Search all notes | Ctrl+Shift+F |
| Create new note | Ctrl+N |
| Quick switcher | Ctrl+O |
| Command palette | Ctrl+P |
| Toggle reading mode | Ctrl+E |

---

## PART 4: DATAVIEW — QUERY YOUR KNOWLEDGE GRAPH

### What Dataview Is

Dataview treats your vault as a **database**. Every `.md` file is a row. Every YAML frontmatter field is a column. You write SQL-like queries inline in notes.

**Install:** Settings → Community Plugins → Browse → "Dataview" → Install + Enable

### The Frontmatter Standard

Every note MUST have this frontmatter for Dataview to work:

```yaml
---
tags: [concept, core-ip, rul]
created: 2026-06-20
status: draft           # draft | active | archived
layer: 4                # which PlantMind layer (1-5) this belongs to
patent_relevant: true   # true | false
priority: high          # high | medium | low
---
```

---

## PART 5: DATAVIEW QUERY TEMPLATES

### Template 1: All Core IP Nodes

```dataview
TABLE created, tags, status
FROM #core-ip
SORT created DESC
```

**Use in:** `_Index.md` → always shows latest core IP work

---

### Template 2: Decision Log (patent diary)

```dataview
TABLE file.name, created, file.folder
FROM "Decisions"
SORT created ASC
```

**Use in:** `Patents/_IP_Timeline.md` → chronological list proves prior art dates

---

### Template 3: Open Research Items

```dataview
TABLE file.name, created, priority
FROM "Research"
WHERE status = "draft"
SORT priority DESC, created DESC
```

**Use in:** `_Index.md` → shows what you haven't processed yet

---

### Template 4: Everything Tagged to a Layer

```dataview
TABLE file.name, tags, patent_relevant
FROM ""
WHERE layer = 4
SORT file.name ASC
```

**Use in:** `Architecture/Layer 4 - Götze Engine.md` → see all Layer 4 nodes

---

### Template 5: Patent-Relevant Nodes Only

```dataview
TABLE file.name, created, tags
FROM ""
WHERE patent_relevant = true
SORT created ASC
```

**Use in:** `Patents/_Patent_Dashboard.md` → your entire IP footprint

---

### Template 6: Research Papers with Prior Art Flag

```dataview
TABLE file.name, created, tags
FROM "Research"
WHERE contains(tags, "prior-art")
SORT created DESC
```

---

### Template 7: Unlinked Nodes (Orphan Finder)

```dataview
TABLE file.name, created
FROM ""
WHERE length(file.inlinks) = 0 AND length(file.outlinks) = 0
```

**Use monthly:** any node with zero links is not in your graph — either link it or delete it.

---

### Template 8: All Datasets Loaded

```dataview
TABLE file.name, created, status
FROM "Research"
WHERE contains(tags, "dataset")
SORT file.name ASC
```

---

## PART 6: BUILDING A LIVING DASHBOARD

Create `_Index.md` with this structure (using Dataview inline):

```markdown
# PlantMind Knowledge Graph

## 🔴 Open Decisions (draft)
\`\`\`dataview
TABLE file.name, created
FROM "Decisions"
WHERE status = "draft"
\`\`\`

## 🟡 Research Inbox
\`\`\`dataview
TABLE file.name, priority
FROM "Research"
WHERE status = "draft"
SORT priority DESC
\`\`\`

## 🟢 Core IP Nodes
\`\`\`dataview
TABLE file.name, created
FROM ""
WHERE patent_relevant = true
SORT created DESC
\`\`\`

## Latest Activity
\`\`\`dataview
TABLE file.name, file.mtime
FROM ""
SORT file.mtime DESC
LIMIT 10
\`\`\`
```

---

## PART 7: OBSIDIAN PLUGINS STACK FOR PLANTMIND

| Plugin | What it does for PlantMind |
|---|---|
| **Dataview** | Query any field as a database — dashboards, patent logs |
| **Templater** | Auto-fill frontmatter when creating new nodes |
| **Calendar** | Visualize when decisions were made (patent diary) |
| **Kanban** | Turn open items into a sprint board |
| **Excalidraw** | Draw layer diagrams inside notes |
| **Advanced Tables** | Edit markdown tables without pain |
| **Git** | Auto-commit vault to GitHub — timestamps = prior art |
| **Periodic Notes** | Daily engineering log tied to calendar |

### Templater: New Concept Node Template

Create `Templates/New Concept.md`:

```markdown
---
tags: [concept]
created: <% tp.date.now("YYYY-MM-DD") %>
status: draft
layer: 
patent_relevant: false
priority: medium
---

# <% tp.file.title %>

## WHAT
What is this concept?

## WHY
Why does it matter to PlantMind?

## HOW
The mechanism — algorithm, formula, or process.

## WHEN
When does this concept activate in the pipeline?

## WHY NOT
What alternatives exist and why are they inferior?

## Connected Nodes
- Depends on → 
- Enables → 
- Challenges → 
- Evidence in code → 
```

---

## PART 8: THE OBSIDIAN → PATENT PIPELINE

This is the most powerful use: **Obsidian as a patent diary**.

1. Every Decision node is timestamped (file creation date)
2. Every Research node documents prior art you've *already found*
3. Every Concept node shows your conceptual development
4. Dataview query on `patent_relevant = true` → instant IP portfolio view
5. Git plugin commits every change → GitHub shows invention timeline

When you file the provisional patent, you can export your vault's git log as evidence of prior invention date. **This is how independent inventors win disputes.**

---

## PART 9: GROWING THE PLANTMIND VAULT

**Nodes not yet created (create these next):**

```
Architecture/
  Layer 1 - Data.md
  Layer 2 - Features.md
  Layer 5 - Proof and Learn.md

Decisions/
  Decision - Window Size 30.md
  Decision - RED Threshold 30.md

Technology/
  MLflow.md
  Delta Lake.md
  Databricks.md
  Streamlit.md

Research/          ← NEW FOLDER
  Dataset - NASA C-MAPSS.md
  Dataset - PHM 2008 Bearing.md
  Paper - Saxena 2008 RUL.md
  Paper - Wachter 2018 Counterfactual.md
  Paper - Hong 2023 MetaGPT.md
```

**Command to Claude:** "Add [X] to the knowledge graph" → I'll create the node, add `[[links]]`, and update `_Index.md`.

---

*Guide v1.0 · PlantMind · 2026-06-20*
*Next: Run Ctrl+G in Obsidian and spend 5 minutes clicking around the graph. Every node you open teaches you something.*
