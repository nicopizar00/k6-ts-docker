# Plan — punch-document-graphify-ownership

> Pattern source: `.github/prompts/punch-plan.prompt.md` (Caveman `full`).
> Governance plan — no product code. Tasks execute via `punch-ai-governance`
> directly (user-direct maintainer, never through `punch-builder`/engineers);
> "Build prompt" field below is N/A for that reason, noted per task.

- **Goal:** Make `/punch-document` (via `punch-ai-governance`) the sole owner
  of Graphify write operations (build / `--update` / full regen). Every other
  consumer — `punch-context-engineering`, Spec/`punch-architect`, Build/Test/
  Review/Ship — may query an existing graph and detect drift/staleness, but
  must never generate, update, delete, or otherwise modify it.

## Current-state findings

- `/punch-document` is already the intended decision authority (ADR 0002,
  `docs/ai/prompt-registry.md`: "no new agent, no new skill"). The gap is
  `.github/copilot-instructions.md` §graphify, which currently attributes
  "the decision of whether [graphify] runs" to the Context Engineering gate.
- `.github/skills/punch-context-engineering/SKILL.md` Graphify gate steps 1
  and 3 instruct build (`/graphify .`) and `graphify update` directly — the
  actual write-authority leak to fix.
- No live capability leak today: `docs/ai/agent-guards.md` grants host-`graphify`
  only to `punch-ai-governance`. No other custom-agent persona can execute it
  as an autonomous tool call. The leak is at the policy/skill-text layer —
  `/graphify` is a chat-level slash command invocable regardless of active
  persona, so the skill text is the real (and sufficient) enforcement surface.
- No `punch-document` skill exists, and creating one would violate
  `docs/ai/skill-registry.md`'s explicit rule: "Phases are prompts and agents,
  not skills — never create `punch-<phase>` skill." Repository-equivalent is
  `.github/skills/punch-ai-governance/SKILL.md` (already scoped to
  `.github/**` + `docs/**`, already the decision authority).
- No standalone `punch-spec` skill exists; Spec's method skill is
  `punch-spec-driven-development`.
- "First wave / bootstrap-only" framing does not exist in
  `punch-document.prompt.md` today — that belongs to `./bin/punch init` /
  `/punch-init`, a different one-time prompt. No strip-language task needed;
  DOC-01 only adds what's missing (free-form-instruction input, explicit
  query/update/regen decision rule).
- Resolved: Architect's relationship to Document is **boundary-owner**, not
  executor — Architect's new text patterns off `punch-ai-governance`'s
  existing admin-rights model (sole `.github/`+`docs/` admin, sole Graphify
  writer); it does not inherit that write scope. `punch-ai-governance.agent.md`
  itself is unchanged.
- Resolved: no live committed `graphify-out/graph.json` exists in this repo —
  no reconciliation task needed against a committed graph.

## Target ownership model

```
                 ┌───────────────────────┐
                 │   punch-ai-governance  │  ← sole Graphify WRITE owner
                 │   (via /punch-document)│     (build / --update / regen)
                 └───────────┬───────────┘
                              │ delegates 1-deep
                              ▼
                    ┌─────────────────┐
                    │  punch-graphify  │  executes what Document asks;
                    │  (tool skill)    │  never decides doc content
                    └─────────────────┘
                              ▲
                    query / path / explain (read-only)
                              │
        ┌─────────────────────┼─────────────────────────┐
        │                     │                          │
┌───────────────┐   ┌──────────────────┐        ┌────────────────┐
│ punch-context- │   │  punch-architect  │        │ Build/Test/     │
│ engineering    │   │  (Spec + Plan)    │        │ Review/Ship     │
│ (consumer only)│   │  (consumer only,  │        │ (consumer only, │
│                │   │  records gaps for │        │  unchanged)     │
│ detects drift, │   │  Document)        │        │                 │
│ recommends     │   │                   │        │                 │
│ /punch-document│   │                   │        │                 │
└───────────────┘   └──────────────────┘        └────────────────┘
```

## Ownership matrix

| Actor | Query graph | Build graph | `--update` | Full regen | Decide doc content | Notes |
|---|---|---|---|---|---|---|
| **Punch Document** (`/punch-document` → `punch-ai-governance`) | yes | yes | yes | yes | yes | Sole write owner; only sanctioned host-`graphify` exception (ADR 0002) |
| **Graphify** (`punch-graphify` skill) | executes | executes | executes | executes | never | Tool only |
| **Context Engineering** | yes | no | no | no | no | Detects missing/stale graph, recommends `/punch-document` |
| **Spec** (`punch-architect`) | yes (via Context Eng.) | no | no | no | no | May record a gap for a later Document wave |
| **Architect** (boundary owner) | yes (via Context Eng.) | no | no | no | no | Patterns off `punch-ai-governance`'s admin model; recommends, never executes |
| **Build / Test / Review / Ship** | yes (via Context Eng., unchanged) | no | no | no | no | Untouched by this plan |

## Tasks

### DOC-01
- **Goal** — Make `.github/prompts/punch-document.prompt.md` a free-form,
  instruction-driven doc utility with an explicit query/incremental/full-regen
  decision rule, restated as the sole graph write entry point.
- **Allowed edit paths** — `.github/prompts/punch-document.prompt.md`
- **Read-only context paths** — `.github/skills/punch-ai-governance/SKILL.md`,
  `.github/skills/punch-graphify/SKILL.md`,
  `.github/agents/punch-ai-governance.agent.md`,
  `docs/ai/decisions/0002-graphify-host-tool.md`
- **Forbidden paths** — every other prompt/agent/skill file
- **Expected diff size** — ~20-40 lines
- **Validation commands** — N/A (no runtime); `punch-ai-governance` audit
  procedure (frontmatter, cross-reference, duplication checks) + manual diff
  review against prompt contract shape (`docs/ai/prompt-registry.md`)
- **Rollback notes** — single-file revert, no downstream state
- **Human checkpoint** — human approval required before write
- **Build prompt** — N/A; executed via `punch-ai-governance` directly

### GOV-01
- **Goal** — State sole Graphify write-rights and localized/full-wave
  reconciliation support at skill level in
  `.github/skills/punch-ai-governance/SKILL.md` (repository-equivalent of the
  nonexistent `punch-document` skill).
- **Allowed edit paths** — `.github/skills/punch-ai-governance/SKILL.md`
- **Read-only context paths** — `.github/agents/punch-ai-governance.agent.md`,
  `.github/skills/punch-graphify/SKILL.md`,
  `.github/skills/punch-context-engineering/SKILL.md`
- **Forbidden paths** — all other skills/agents/prompts
- **Expected diff size** — ~15-25 lines
- **Validation commands** — N/A; governance audit duplication/conflict check
- **Rollback notes** — single-file revert
- **Human checkpoint** — human approval required before write
- **Build prompt** — N/A; executed via `punch-ai-governance` directly

### GRAPH-01
- **Goal** — State in `.github/skills/punch-graphify/SKILL.md` that Graphify
  executes what Document requests and never decides content; write
  subcommands run only through `/punch-document`.
- **Allowed edit paths** — `.github/skills/punch-graphify/SKILL.md`
- **Read-only context paths** — `.github/agents/punch-ai-governance.agent.md`,
  `docs/ai/decisions/0002-graphify-host-tool.md`
- **Forbidden paths** — everything else
- **Expected diff size** — ~10-15 lines
- **Validation commands** — re-run existing 7-check Team Share validation
  checklist against a test graph; governance audit
- **Rollback notes** — single-file revert
- **Human checkpoint** — human approval required before write
- **Build prompt** — N/A; executed via `punch-ai-governance` directly

### CTX-01 (core fix)
- **Goal** — Strip build/update authority from
  `.github/skills/punch-context-engineering/SKILL.md`'s Graphify gate; make it
  query-only with drift/staleness detection that recommends `/punch-document`.
- **Allowed edit paths** — `.github/skills/punch-context-engineering/SKILL.md`
- **Read-only context paths** — `.github/skills/punch-graphify/SKILL.md`,
  `.github/skills/punch-ai-governance/SKILL.md`
- **Forbidden paths** — everything else
- **Expected diff size** — ~25-40 lines
- **Validation commands** — manual walkthrough of test scenarios 4 and 5
  below; governance audit; grep confirms no remaining imperative
  "run `/graphify`" / "graphify update" instruction in this file
- **Rollback notes** — single-file revert; highest-care task, this primer is
  loaded by nearly every agent ("Skill activation: Always:
  `punch-context-engineering`")
- **Human checkpoint** — human approval required before write
- **Build prompt** — N/A; executed via `punch-ai-governance` directly

### SPEC-01
- **Goal** — Add a surgical boundary note to
  `.github/skills/punch-spec-driven-development/SKILL.md`: Spec may query
  docs/graph via Context Engineering, must not clean/regenerate, may record a
  gap for a later Document wave.
- **Allowed edit paths** — `.github/skills/punch-spec-driven-development/SKILL.md`
- **Read-only context paths** — CTX-01 output
- **Forbidden paths** — everything else, including this file's Plan-phase
  handoff text (Stage 2/3) — do not touch
- **Expected diff size** — ~5-10 lines
- **Validation commands** — governance audit; confirm `punch-spec.prompt.md`
  still matches (untouched, no drift)
- **Rollback notes** — single-file revert
- **Human checkpoint** — human approval required before write
- **Build prompt** — N/A; executed via `punch-ai-governance` directly

### ARCH-01
- **Goal** — Add a "Graph & documentation boundary" subsection to
  `.github/agents/punch-architect.agent.md` patterning Architect's
  read-only/recommend-only stance off `punch-ai-governance`'s existing
  admin-rights model, without granting Architect that write scope.
- **Allowed edit paths** — `.github/agents/punch-architect.agent.md`
- **Read-only context paths** — `.github/agents/punch-ai-governance.agent.md`,
  GOV-01 + CTX-01 output
- **Forbidden paths** — its own Forbidden-list scope stays as-is; do not add
  `.github`/`docs/ai` write rights; `punch-ai-governance.agent.md` itself
  (unchanged, per resolved Q1)
- **Expected diff size** — ~10-20 lines
- **Validation commands** — governance audit boundary-declaration check;
  confirm no contradiction with `punch-ai-governance.agent.md`'s
  never-delegated-to line
- **Rollback notes** — single-file revert
- **Human checkpoint** — human approval required before write
- **Build prompt** — N/A; executed via `punch-ai-governance` directly

### REG-01
- **Goal** — Update `docs/ai/prompt-registry.md` Document row for the
  sole-writer clarification.
- **Allowed edit paths** — `docs/ai/prompt-registry.md`
- **Read-only context paths** — DOC-01 output
- **Forbidden paths** — everything else in the file
- **Expected diff size** — ~1-3 lines
- **Validation commands** — governance audit §"Asset inventory matches registries"
- **Rollback notes** — single-file revert
- **Human checkpoint** — human approval required before write
- **Build prompt** — N/A; executed via `punch-ai-governance` directly

### REG-02
- **Goal** — Update `docs/ai/skill-registry.md` one-line descriptions for
  `punch-ai-governance`, `punch-graphify`, `punch-context-engineering` rows.
- **Allowed edit paths** — `docs/ai/skill-registry.md`
- **Read-only context paths** — GOV-01, GRAPH-01, CTX-01 output
- **Forbidden paths** — everything else in the file, incl. domain/lifecycle
  cap discussion sections
- **Expected diff size** — ~3-6 lines
- **Validation commands** — governance audit; confirm skill count unchanged
  (still 6 domain skills, no new skill — F4 held)
- **Rollback notes** — single-file revert
- **Human checkpoint** — human approval required before write
- **Build prompt** — N/A; executed via `punch-ai-governance` directly

### REG-03
- **Goal** — Rewrite `.github/copilot-instructions.md` §graphify (lines
  ~124-133) to match CTX-01 — the always-on hub currently misattributes
  build/update authority to Context Engineering.
- **Allowed edit paths** — `.github/copilot-instructions.md` (graphify
  section only)
- **Read-only context paths** — CTX-01, DOC-01 output
- **Forbidden paths** — every other section of this file (Critical Rules,
  lifecycle table, Caveman section)
- **Expected diff size** — ~10-15 lines
- **Validation commands** — governance audit; re-read full file after edit to
  confirm no adjacency damage to Critical Rules
- **Rollback notes** — single-file revert; always-on file, high-care edit
- **Human checkpoint** — human approval required before write
- **Build prompt** — N/A; executed via `punch-ai-governance` directly

### DOCADR-01 (optional — decide at Build time)
- **Goal** — If GOV-01's cross-link leaves ambiguity, add one sentence to
  `.github/skills/punch-documentation-and-adrs/SKILL.md` scoping graph writes
  out of the writing-method skill.
- **Allowed edit paths** — `.github/skills/punch-documentation-and-adrs/SKILL.md`
- **Read-only context paths** — GOV-01 output
- **Forbidden paths** — everything else
- **Expected diff size** — ~1-2 lines, or zero (skip) if GOV-01 already
  unambiguous
- **Validation commands** — governance audit
- **Rollback notes** — single-file revert
- **Human checkpoint** — human approval required before write
- **Build prompt** — N/A; executed via `punch-ai-governance` directly

## Order of execution

1. **DOC-01** alone — establishes target language.
2. **GOV-01 + GRAPH-01 + CTX-01** (3 files) — core ownership triangle, must
   land together for consistent wording.
3. **SPEC-01 + ARCH-01** (2 files) — depend on batch 2.
4. **REG-01 + REG-02 + REG-03** (3 files) — registries, last, once source
   text is final.
5. **DOCADR-01** — only if still needed after batch 2, decided at Build time.

Each batch respects `punch-ai-governance`'s own guard (≤3 files/logical step,
mandatory approval before write) and runs its own
Plan-confirmed → Build → Test(governance audit) → Review → Ship cycle.

## Cross-cutting risks

- **CTX-01 and REG-03 are the widest-blast-radius edits** — both are loaded
  or read on nearly every session (Context Engineering primer; always-on
  hub). Review diffs closely; do not batch either with unrelated changes.
- **Wording drift across GOV-01/GRAPH-01/CTX-01** if batch 2 isn't landed
  together — inconsistent "who owns what" language would recreate F1/F2.
- **Hard constraint check** — diff `punch-build`/`punch-test`/`punch-review`/
  `punch-ship` prompts + agents before/after; expect zero change (test
  scenario 7).

## Test / verification scenarios

1. Localized documentation cleanup — free-form-scoped `/punch-document` call,
   no full-surface rebuild triggered.
2. Incremental graph refresh — moderate drift signal chooses `--update`, not
   full rebuild.
3. Full graph regeneration — major structural change triggers full rebuild
   with stated reason.
4. Stale/incomplete graph detection — Context Engineering flags stale graph,
   recommends `/punch-document`, does not rebuild itself.
5. Refusal by Context Engineering to write — graph missing, Context
   Engineering declines to build, continues without it, recommends
   `/punch-document`.
6. Confirmation required before edits — `/punch-document` pauses for explicit
   go-ahead before any disk write.
7. Unchanged Build/Test/Review/Ship behavior — zero diff on those prompts/agents.

## Rollback plan

Every task is a single-file, additive-text edit with no schema/runtime
surface — revert via `git revert` per commit, no cascade beyond the
registries touched in batch 4 (revert those in the same order, last-in
first-out, to keep cross-references consistent).

**Gate:** approved when human confirms → Build (per task ID).
