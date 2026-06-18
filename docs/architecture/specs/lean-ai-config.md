# Spec — Lean the Punch AI config (`.github/`)

**Status:** Wave 1 in progress · Waves 2–3 pending task breakdown
**Source:** `/enhance` pass over `.github/` (agent · skills · prompt · claudemd ·
cross-file analyzers), 2026-06-18.
**Constraint:** Functionality stays untouched — every item is a *link-don't-restate*
consolidation or a factual correction. No routing, scope, guard, evidence, or
execution-chain behavior changes.

## Problem

Caveman guidance is restated in ~13 places (9 agents byte-for-byte identical, plus
`copilot-instructions.md`, `AGENTS.md`, `punch-build.prompt.md`, and the canonical
`punch-build-caveman/SKILL.md`). This duplication is the guard-overload that keeps
Caveman from being adopted in plain Copilot Chat (only `copilot-instructions.md`
auto-loads; the strong rules live in unreachable spokes). Secondary: stale "5 build
prompts" references in always-on memory, `copilot-instructions.md` bloat, and
`idea-refine` drift.

## Wave 1 — Caveman single-source + ultra/wenyan tiering + expand to `/punch-test`

See the active plan. Summary: make `punch-build-caveman/SKILL.md` the canonical
source; collapse every restatement to a pointer; set `/punch-build` + `/punch-test`
default `ultra` with build/test **execution sub-agents** at `wenyan`; add an
enforced Operating-comms section to `/punch-test`; reconcile ADR 0003 + registries.

## Wave 2 — Fix stale architecture (factual)

| File | Fix |
|---|---|
| `CLAUDE.md` lines 98, 100, 162-165 | Replace obsolete "Build split into five domain-specialized prompts (orchestrator, compose, k6-http, k6-browser, data-harvest)" + "4 core + 5 builders" with the real single-`punch-build`-prompt + dispatcher → 2 engineers model. |
| `README.md` operating-model section | Update stale "seven-phase Define→… / five Build prompts / six skills + five agents" to six phases, single build prompt, current skill/agent counts (or link `docs/ai/operating-model.md`). |
| `docs/ai/skill-registry.md:101` | `punch-build-k6-*` (deleted split prompts) → `punch-build (via punch-performance-test-engineer)`. |
| `AGENTS.md` line ~70 | `punch-ai-governance` caption "no terminal" → "graphify-only terminal (ADR 0002)" (frontmatter declares `execute/runInTerminal`). |
| `docs/architecture/specs/plan-bff-checkout-journey*.md` | `punch-build-k6-http` / `punch-build-orchestrator` refs → `punch-build`, or archive to `docs/ai/history/`. |

## Wave 3 — Skill / guard polish

| Target | Fix | Status |
|---|---|---|
| `idea-refine/SKILL.md` | Add an "In Punch" framing section (runs at start of Spec, hands to spec-driven-development; long-form stays in companion `.md` files). | **Done** (framing added; deep body-trim skipped — companions already hold long-form, low value) |
| 5 punch-domain skills | Add a one-line "Not for:" negative trigger reusing each skill's "does not own" targets. | **Done** |
| Agent `## Guards` sections | Add the `agent-guards.md` pointer to the 5 agents missing it. | **Done** (pointer added to all 9; restated-generic-rule trimming in the 4 builders skipped — higher risk, low value) |
| All authored SKILL.md frontmatter | Standardize `applies-to` to a leading machine-readable token. | **Deferred** — cosmetic, ~19-file churn, no current consumer keys off it. |
| `punch-build.prompt.md` absorbed tools/skills/paths block | Reduce to links to the engineer agent files. | **Dropped** — the owner explicitly directed this block be **absorbed mandatory** into the Build prompt; reducing it would reverse that directive. |
| Untrusted-output rule | Consolidate the restatements to link `debugging-and-error-recovery`. | **Deferred** — "functionality untouched either way" (analyzer); low value. |

### Follow-up noted during Wave 3

`punch-ai-governance/SKILL.md` "Replaces" section hard-codes a stale asset count
("10 agents … 11 prompts" — actual: 9 agents, 8 prompts). Factual drift, same class
as Wave 2; out of the Wave-3 clear-win scope. Fix in a small follow-up (replace the
hard count with a pointer to the registries).

## Task-breakdown note

Each remaining row is a candidate task. Break down via `punch-plan` when ready;
keep each as a small reviewable PR with the governance audit (`punch-ai-governance`)
as the gate. None require a `./bin/punch` runtime run (docs/config only).
