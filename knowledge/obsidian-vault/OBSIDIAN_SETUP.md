# How to Open This Vault in Obsidian

## Step 1: Install Obsidian (free)
Download from: https://obsidian.md/download
Available for Windows, Mac, Linux, iOS, Android.

## Step 2: Open as Vault
1. Launch Obsidian
2. Click **"Open folder as vault"**
3. Navigate to: `C:\Users\hp\Claude\Projects\PlantMind\Knowledge Graph\`
4. Click **Open**

## Step 3: Enable Graph View
1. Click the **graph icon** in the left sidebar (looks like connected dots)
2. You'll see all notes as nodes, all `[[links]]` as edges
3. Hover over a node to highlight its connections
4. Click a node to open that note

## Step 4: Recommended Plugins (optional but powerful)

| Plugin | What it does | How to install |
|---|---|---|
| **Dataview** | Query your notes like a database | Settings → Community Plugins → Browse → "Dataview" |
| **Templater** | Template system for new notes | Browse → "Templater" |
| **Tag Wrangler** | Better tag management | Browse → "Tag Wrangler" |
| **Excalidraw** | Draw diagrams inside notes | Browse → "Excalidraw" |

## How to Add New Notes

Every time you learn something new or make a new decision:

1. Create a new `.md` file in the right folder:
   - New concept → `Concepts/`
   - New engineering decision → `Decisions/`
   - New technology → `Technology/`
   - New patent idea → `Patents/`
   - New architecture detail → `Architecture/`

2. Link it to existing nodes with `[[Node Name]]`

3. Add it to `[[_Index]]` under the right section

## The Frontmatter Standard

Every note should start with:
```
---
tags: [tag1, tag2]
created: YYYY-MM-DD
---
```

## How Claude Grows This Knowledge Graph

In future sessions, say: **"Add this to the knowledge graph"** and I'll:
1. Create the right node file with the 5W structure
2. Add `[[links]]` to related existing nodes
3. Update `_Index.md` with a new entry

## Current Vault Structure

```
Knowledge Graph/
├── _Index.md                    ← Start here (Map of Content)
├── OBSIDIAN_SETUP.md            ← You are here
│
├── Concepts/
│   ├── Götze Score.md
│   ├── Counterfactual Proof.md
│   ├── Remaining Useful Life.md
│   ├── Surrogate Twin.md
│   └── RED-GREEN Transition.md
│
├── Architecture/
│   ├── Layer 3 - Prediction.md
│   └── Layer 4 - Götze Engine.md
│
├── Decisions/
│   ├── Decision - RandomForest over LSTM.md
│   ├── Decision - Deterministic over LLM Scoring.md
│   └── Decision - Clip RUL at 130.md
│
├── Patents/
│   ├── Patent 1 - Counterfactual Proof Engine.md
│   └── Patent 4 - Research Augmented MetaGPT.md
│
└── Technology/
    ├── NASA C-MAPSS.md
    └── MetaGPT.md
```

## Tags Reference

| Tag | Meaning |
|---|---|
| `core-ip` | Directly tied to patent claims |
| `ml` | Machine learning concepts |
| `decision` | Engineering decision + rationale |
| `why-not` | Notes that focus on alternatives rejected |
| `architecture` | System architecture layers |
| `patent` | Patent concept documents |
| `demo` | Demo-relevant notes |
| `technology` | External tools and platforms |
