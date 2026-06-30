---
wave: document-2026-06-28
scope: global graphify track — full repo
status: complete — all 4 actionable findings closed
owner: punch-ai-governance
graph: graphify-out/graph.json (560 nodes · 819 edges · 51 communities)
---

# Document Wave — 2026-06-28

**Steps complete:** Map & Gather (1) · Classify (2)\
**Evidence source:** `graphify-out/GRAPH_REPORT.md` · god-node traversal · `graphify path` / `graphify explain` · filesystem cross-check

---

## Finding F-001 — Graphify readiness vocabulary: three parallel implementations

| Field | Value |
|---|---|
| **Classification** | stale-risk · hidden maintenance coupling |
| **Severity** | medium — silent drift, no runtime failure |
| **Status** | ✅ closed — comment added `src/punch/init_scan.py:L70` (mirrors `punch-document.prompt.md` Step 2 classify vocabulary) |

### What the graph found

`graphify_readiness()` (`src/punch/init_scan.py:L409`) has an INFERRED `conceptually_related_to` edge to `Graphify Skill Definition` (`.ai-upstream/graphify/SKILL.md`). Tracing the bridge revealed a three-arm maintenance triangle:

```
.github/prompts/punch-document.prompt.md
  classify vocabulary: orphan · stale · evidence · disconnect
          │
          │  conceptual mirror (no import, no citation)
          ▼
src/punch/init_scan.py:L70  GRAPHIFY_QUERIES constant
  "Which docs appear disconnected from code, tests, prompts, or skills?"
  "Which feature claims have no code or test evidence?"
          │
          │  INFERRED link (scan() calls graphify_readiness())
          ▼
.ai-upstream/graphify/SKILL.md
  CLI syntax only — no query vocabulary
```

### Files involved

| File | Role | Lines |
|---|---|---|
| `src/punch/init_scan.py` | Python owner of `GRAPHIFY_QUERIES` constant | L70–78 |
| `.github/prompts/punch-document.prompt.md` | Governance owner of classify vocabulary | Step 2 |
| `.ai-upstream/graphify/SKILL.md` | Upstream skill — CLI syntax, no queries | (no queries section) |

### Risk

`punch-document.prompt.md` classify vocabulary evolves → `GRAPHIFY_QUERIES` silently goes stale. No enforcing mechanism. The Python constant was authored independently — it mirrors the governance prompt's intent without referencing it.

### Proposed resolution (Step 3, next wave)

Single source for graphify query vocabulary. Options:

1. **Promote to `punch-document.prompt.md`** — add a `## Suggested graphify queries` block; `init_scan.py` reads it at runtime (stdlib `re` parse of the prompt file).
2. **Extract to shared reference** — new `docs/ai/governance/graphify-queries.md`; both files cite it.
3. **Accept divergence, add comment** — add a `# mirrors punch-document.prompt.md Step 2 classify vocabulary` comment in `init_scan.py:L70`; cheapest, no runtime coupling.

Recommend option 3 (cheapest, no new abstraction) unless the vocabulary is expected to change frequently.

**Decision required from `punch-ai-governance` before any edit.**

---

## Step 2 — Classification

| ID | Classification | File(s) | Description | Actionable |
|---|---|---|---|---|
| F-001 | canonical-candidate · stale-risk | `init_scan.py:L70` · `punch-document.prompt.md` · `.ai-upstream/graphify/SKILL.md` | GRAPHIFY_QUERIES vocabulary mirrors doc-phase classify terms with no shared source | ✅ closed — comment added `init_scan.py:L70` |
| F-002 | stale | `SPEC.md` (root) | BFF Checkout Journey spec at root — feature already implemented in `src/tests/bff-checkout-journey.ts` | ✅ closed — deleted |
| F-003 | partial | `docs/architecture/specs/adopt-adapt-caveman-cavecrew.md` | Spec "awaiting approval", untracked in git — not advanced to Plan | ✅ closed — already committed (`b67c70d`); git status snapshot was stale |
| F-004 | stale (temporal) | `docs/ai/templates/tmp-migration-2026-06-20/` (11 files) | Self-labeled `TEMPORAL / disposable` scratch pad — intended to be deleted after graduating items to ADRs | ✅ closed — deleted; all matured items already in ADRs 0001–0004 |
| F-005 | duplicate (graph artifact) | `src/punch/__main__.py` | `cmd_init()` extracted twice: AST node `punch_main_cmd_init` + semantic node `punch___main___cmd_init` — ID format mismatch at merge | ⚠️ graph quality, not doc |
| F-006 | orphaned (by design) | `.ai-upstream/agent-skills/docs/` (Cursor, Windsurf, OpenCode, Copilot setup guides) | Upstream content not adapted to `.github/` — quarantine zone, expected disconnection | ❌ no action |
| F-007 | partial (acceptable) | `.mcp.json` | Empty MCP config `{"mcpServers": {}}` — no servers configured | ❌ no action unless MCP planned |

### F-002 detail — `SPEC.md` stale

Root `SPEC.md` is a BFF Checkout Journey spec written before implementation. `src/tests/bff-checkout-journey.ts` exists and is shipped. Spec at root has no ongoing purpose — should be deleted or moved to `docs/architecture/specs/` as a closed record.

### F-003 detail — `docs/architecture/specs/adopt-adapt-caveman-cavecrew.md` partial

Spec is untracked in git (confirmed via git status). Status line reads "awaiting approval. Plan = next phase." Two options: (a) approve and commit, advancing to Plan; (b) discard if superseded. Not stale — actively in-flight.

### F-004 detail — `docs/ai/templates/tmp-migration-2026-06-20/` temporal scratch

11 files prefixed with numbered topics (00–10). README explicitly marks folder `TEMPORAL / disposable`. Intended lifecycle: pick useful items → graduate to ADR/plan → delete folder. Folder still present — either items weren't graduated or deletion was deferred.

---

## Step 3 — Reconcile queue (approval required before each edit)

Priority order (lowest blast radius first):

1. ~~**F-001**~~ ✅ closed — comment added `src/punch/init_scan.py:L70`.
2. ~~**F-002**~~ ✅ closed — `SPEC.md` deleted.
3. ~~**F-003**~~ ✅ closed — already committed; no action needed.
4. ~~**F-004**~~ ✅ closed — `docs/ai/templates/tmp-migration-2026-06-20/` deleted (11 files); nothing to graduate.

Each requires `punch-ai-governance` approval before write. Surface change → wait → execute.

---

## God nodes (orientation for next wave)

Top cross-community bridges from this graph:

| Node | Edges | Community |
|---|---|---|
| `Skill Registry (Domain + Lifecycle Axes)` | 24 | Skill Registry |
| `using-agent-skills meta-skill` | 16 | Upstream Agent Skills |
| `scan()` | 13 | Punch Init Scan Pipeline |
| `Skill: punch-k6-testing` | 13 | Context + Graphify Skills |
| `Guard skill — Claude Code ↔ GitHub Copilot bridge` | 13 | Context + Graphify Skills |
