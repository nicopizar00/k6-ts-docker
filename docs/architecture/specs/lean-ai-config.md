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

| Target | Fix |
|---|---|
| `idea-refine/SKILL.md` | Add an "In Punch" framing section (runs at start of Spec, hands to spec-driven-development); trim generic upstream body toward the lean profile of peer skills (long-form stays in its companion `.md` files). |
| 5 punch-domain skills (`punch-compose-runtime`, `punch-data-harvest`, `punch-python-orchestration`, `punch-k6-testing`, `punch-ai-governance`) | Add a one-line "When NOT to use" negative trigger (reuse each skill's existing "does not own" targets). |
| All authored SKILL.md frontmatter | Standardize `applies-to` to a leading machine-readable token (path glob OR `lifecycle/<Phase>`) + optional note. |
| Agent `## Guards` sections | Keep only the agent-specific guard; replace the restated generic rules (approval / ≤3 files / 2-failure / leaf-depth) with the `docs/ai/agent-guards.md` pointer; add the pointer to the 5 agents missing it (`punch-architect-readonly`, `punch-planner`, `punch-reviewer`, `punch-verifier`, `security-auditor`). |
| `punch-build.prompt.md` absorbed tools/skills/paths block | Reduce to links to the two engineer agent files (the prompt already admits they "mirror the canonical agent files"). |
| Untrusted-output rule | Designate `debugging-and-error-recovery` canonical; have `security-and-hardening`, `punch-data-harvest`, `punch-context-engineering` link rather than restate. |

## Task-breakdown note

Each Wave-2/3 row is a candidate task. Break down via `punch-plan` when ready;
keep each as a small reviewable PR with the governance audit (`punch-ai-governance`)
as the gate. None require a `./bin/punch` runtime run (docs/config only).
