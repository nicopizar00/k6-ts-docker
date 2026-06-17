# Agent Skills Absorption — Full Implementation Plan

> **Status:** Plan artifact (Ask/Plan discipline — **no runtime AI config
> changed in this pass**). Produced 2026-06-16 on branch `feat/agent-skills`.
> Expands the implementation order in
> [`recommended-target-ai-architecture.md`](recommended-target-ai-architecture.md)
> into scoped, reviewable tasks. Grounded in the five companion review docs in
> this folder.

## Ratified decisions (apply to every task below)

1. **Skills stay in `.github/skills/`** — no migration to `.agents/skills/`.
2. **Two-axis skill model** — *domain skills* (Punch's 6) + *lifecycle skills*
   (adapted upstream). Prompts stay thin and activate one of each.
3. **Punch constraints win on stack; upstream wins on method.** `punch-ship`
   stays mechanical; CI/CD stays external; evidence stays `punch-run.json`.

## Execution status (updated 2026-06-16 — supersedes parts of this plan)

A user-directed restructure landed ahead of the phased plan and changes some
assumptions below:

- **Prompts are now command-mapped** to `.ai-upstream/agent-skills/commands`:
  `punch-spec`, `punch-plan`, 5× `punch-build-*`, `punch-test` (new),
  `punch-verify`, `punch-review`, `punch-ship`. **`punch-define` and
  `punch-refine` were deleted**; `idea-refine` is now a skill invoked *within*
  `punch-spec`. The lifecycle is **6 phases** (Spec absorbs Define).
- **`punch-builder-scoped` was replaced by 5 per-domain builder agents**
  (`punch-builder-orchestrator|compose|k6-http|k6-browser|data-harvest`), each
  with a Copilot `tools:` scope. Agent set is now 9 (4 core + 5 builders).
- **P4.0 correction (verified against VS Code docs):** prompt files use the
  **`agent:`** field, *not* `mode:`. So the reconciliation went toward `agent:`
  (Punch's existing convention was right); the 4 contract docs that said `mode:`
  were the drift and have been fixed. Any `mode:` recommendation elsewhere in
  these review docs is **obsolete** — read it as `agent:`.
- **Committed across `492b170` → `1b4b747`.** Phase 1 (drift + governance), the
  builder/Define/P4.0 restructure, and **all of Phase 3** (13 lifecycle skills —
  Tier-A + the P3 set) are done and committed. **Phase 5 underway:** the
  `security-auditor` specialist agent is added; upstream `code-reviewer` is folded
  into `punch-reviewer` + `code-review-and-quality`; `test-engineer` and
  `web-performance-auditor` are excluded. **Phase 6 done** — Tier-B methods folded
  into domain skills (`context-engineering`→`punch-context`,
  `observability-and-instrumentation`→`punch-data-harvest`,
  `performance-optimization`→`punch-k6-performance`); web/CI-only skills excluded
  and recorded in `skill-registry.md`. **Phase 7 done** — `AGENTS.md` slimmed to a
  pointer contract; a *which skill when* discovery index added to
  `skill-registry.md` with a `CLAUDE.md` pointer; the upstream Node
  `validate-skills.js` folded into `punch-governance-review` (no host Node).
  **The absorption is complete.** (Phase 4 — slimming the phase-prompt *bodies* to
  remove prompt↔skill duplication — remains optional.)

## How "Build" works for this absorption (important)

This work edits the **AI-config layer itself** (`.github/**`, `docs/ai/**`,
`AGENTS.md`, `CLAUDE.md`), not product code. Therefore:

- The five `punch-build-*` prompts (orchestrator/compose/k6-*/data-harvest) **do
  not apply** — they are for product code. AI-config edits are governed by
  [`agentic-workflow.instructions.md`](../../.github/instructions/agentic-workflow.instructions.md)
  ("a new prompt/skill/agent/instruction is itself a Spec→Plan→Build cycle").
- **Verify gate for AI-config tasks** = `punch-governance-review` reports
  **clean** (this is the "equivalent named artifact for non-test changes" that
  `operating-model.md:75` allows in place of `punch-run.json`).
- **`punch-run.json` is still required** for any task that also touches product
  code (only F6.3 touches a domain skill's templates; none change runtime
  behavior — but run `./bin/punch run smoke` anyway as a no-regression check).

### Per-task scope legend
- **Allowed** — may create/modify/delete here.
- **Read-only** — may read for context, must not edit.
- **Forbidden** — must refuse; touching one = stop & return to Plan.

### Standing forbidden set (every task)
`src/services/**`, `src/punch/**`, `docker/**`, `docker-compose.yml`,
`src/tests/**`, `.github/workflows/**` — unless a task explicitly lists one as
Allowed. Rationale: absorption must not change product/runtime behavior
(`punch-architecture.instructions.md`).

---

## Phase 1 — Fix drift + ratify governance *(P1 — unblocks everything)*

Goal: a clean governance baseline and a skill taxonomy that *permits* lifecycle
skills. **No new skills are added until this phase passes.**

| Task | Goal | Allowed | Read-only | Validation | Rollback | Checkpoint |
|---|---|---|---|---|---|---|
| **G1.1** | Register `idea-refine`; add `applies-to:`; delete the `/mnt/skills/...` line | `.github/skills/idea-refine/SKILL.md`, `docs/ai/skill-registry.md` | `agentic-workflow.instructions.md`, upstream `idea-refine` | governance-review: idea-refine has a registry row + complete frontmatter | revert commit (docs only) | human confirms registry wording |
| **G1.2** (superseded) | `punch-refine` was **deleted** rather than fixed — `idea-refine` now runs inside `punch-spec`, with no standalone prompt; `prompt-registry.md` updated | `.github/prompts/punch-refine.prompt.md` (deleted), `docs/ai/prompt-registry.md` | — | governance-review clean (11 files = 11 rows) | done |
| **G1.3** | Introduce two-axis skill model: reframe cap + refine "phases-are-not-skills" | `docs/ai/skill-registry.md`, `docs/ai/operating-model.md` | conflict report C1, all instructions | governance-review clean; cap now reads "6 domain + N lifecycle" | revert commit | **human ratifies the governance change** (this edits Punch's own rules) |
| **G1.4** | Sync `AGENTS.md` + `copilot-instructions.md` lifecycle/asset wording to the new model (no duplication) | `AGENTS.md`, `.github/copilot-instructions.md` | `operating-model.md` | governance-review: no rule restated; cross-refs resolve | revert commit | human confirms no semantic drift |

**Phase-1 exit gate:** `punch-governance-review` verdict = **"Governance is
clean"**, with the registries matching disk and the cap reframed. Diff size
≈120–180 lines, docs/config only.

---

## Phase 2 — Skills home *(decided — no work)*

Keep `.github/skills/`. No tasks. (Recorded so the phase numbering matches the
target-architecture map.)

---

## Phase 3 — Absorb Tier-A lifecycle skills (adapted) *(P2)*

One skill = one folder under `.github/skills/<name>/` + one `skill-registry.md`
row, **registered in the same commit** (the rule the `idea-refine` precedent
broke). Adaptation = copy `SKILL.md`, add `applies-to:`, replace web/Node
examples with Punch commands, strip Claude runtime paths, cross-link to
instructions instead of restating them. Batched into reviewable PRs.

**Common scope for every A3.x task**
- Allowed: `.github/skills/<name>/**`, `docs/ai/skill-registry.md`
- Read-only: `.ai-upstream/agent-skills/skills/<name>/**`, all
  `.github/instructions/**`, `CLAUDE.md`
- Forbidden: standing set + **`.ai-upstream/**` is read-only** (never edit
  provenance) + other skills' folders
- Validation: governance-review clean + the skill's `applies-to` resolves +
  no `/mnt/`, `npm`, `jest`, `subagent_type`, or `$ARGUMENTS` leakage (grep)
- Rollback: delete the skill folder + its registry row (self-contained)
- Checkpoint: human reviews the *adaptation diff vs upstream* per skill

| Task | Skills (batch) | Phase served | Key adaptation note |
|---|---|---|---|
| **A3.1** | `spec-driven-development`, `planning-and-task-breakdown` | Spec, Plan | Map "tasks" to allowed/read-only/forbidden; drop "this is a web app" default |
| **A3.2** | `incremental-implementation`, `test-driven-development` | Build, Verify | **Heaviest adapt:** "test" → k6 checks/thresholds + `punch-run.json`; keep Prove-It; drop jest/vitest |
| **A3.3** | `debugging-and-error-recovery`, `code-review-and-quality` | Verify, Review | Code-review defers the AI-config axis to `punch-governance-review`; align debugging with `punch-verify` failure classification |
| **A3.4** | `code-simplification`, `git-workflow-and-versioning` | Review, Ship | git skill must keep human-merge + no-`--no-verify`; simplification matches "no premature abstraction" |
| **A3.5** *(P3)* | `documentation-and-adrs`, `security-and-hardening`, `doubt-driven-development`, `source-driven-development` | cross-cutting | security scoped to real surfaces (gateway/orders/Postgres/env), no web-auth |

**Phase-3 exit gate:** each batch ships governance-clean; `skill-registry.md`
lists "6 domain + N lifecycle"; `using-agent-skills`-style index updated in C7.2.

---

## Phase 4 — Slim prompts to delegate *(P2)*

Make prompts thin entry points that activate `<lifecycle skill> + <domain
skill>` and state Punch overrides. **Procedure moves into skills, not prompts.**

> **DONE (2026-06-17).** The `mode:`-vs-`agent:` contradiction is resolved. VS
> Code prompt files use **`agent:`** (verified against the VS Code docs), so the
> prompts were already correct and the 4 contract docs that said `mode:` were
> fixed to `agent:`. Every prompt now binds to a specific custom agent. P4.0 is
> complete.

| Task | Goal | Allowed | Read-only | Validation | Checkpoint |
|---|---|---|---|---|---|
| **P4.0** ✅ done | Reconciled prompt frontmatter to Copilot-native **`agent:`** (not `mode:`) across all prompts; each binds a specific custom agent; fixed the 4 contract docs | `.github/prompts/*.prompt.md`, `docs/ai/prompt-registry.md`, `docs/ai/copilot-mode-mapping.md`, `.github/skills/punch-governance-review/SKILL.md`, `.github/instructions/agentic-workflow.instructions.md` | `copilot-setup.md`, all agents | governance-review check #1 passes (every prompt has `agent:`) | done |
| **P4.1** | Slim `punch-spec`, `punch-plan`, `punch-review` to activate A3.1/A3.3 skills | those 3 `.prompt.md` | the skills, `prompt-registry.md` | governance-review clean; prompts ≤ ~30 lines; gates preserved | human diff review |
| **P4.2** | Update the 5 `punch-build-*` prompts to activate `incremental-implementation`+`test-driven-development` (A3.2) + their domain skill | `.github/prompts/punch-build-*.prompt.md` | A3.2 skills, `scoped-build-policy.md` | governance-review clean; **scope tables unchanged**; **no `/build auto`** | human confirms scopes intact |
| **P4.3** | Add new thin `punch-simplify.prompt.md` (activates `code-simplification`) + registry row | new prompt, `prompt-registry.md` | A3.4 skill | governance-review: 13 files = 13 rows | human confirms a new prompt is warranted |

**Phase-4 exit gate:** prompt registry in sync; no procedure duplicated between a
prompt and its skill (conflict report D4).

---

## Phase 5 — Agents *(P3)*

| Task | Goal | Allowed | Read-only | Validation | Checkpoint |
|---|---|---|---|---|---|
| **AG5.1** | Add `security-auditor.agent.md` (adapted, Punch-scoped, read-only persona) + `AGENTS.md` row | `.github/agents/security-auditor.agent.md`, `AGENTS.md` | upstream agent, `security-and-hardening` skill | governance-review: agent listed in `AGENTS.md`; `*.agent.md` naming | human confirms persona is non-duplicative |
| **AG5.2** | Fold upstream `code-reviewer` five-axis framing into `punch-reviewer` (no new persona) | `.github/agents/punch-reviewer.agent.md` | upstream `code-reviewer`, `code-review-and-quality` skill | governance-review clean; persona count still 6 | human confirms merge over duplication |

Excluded (recorded, no task): `test-engineer`, `web-performance-auditor`.

---

## Phase 6 — Fold overlaps, exclude non-fits *(P3)*

| Task | Goal | Allowed | Read-only | Validation | Checkpoint |
|---|---|---|---|---|---|
| **F6.1** | Fold `context-engineering` method into `punch-context`; `observability-and-instrumentation` into `punch-data-harvest` | those 2 domain `SKILL.md`(+supporting) | upstream skills | governance-review clean; **no new skill dirs** | human confirms fold, not new skill |
| **F6.2** | Salvage measure→fix→verify loop + N+1/backend from `performance-optimization` into `punch-k6-performance`; drop CWV/React | `.github/skills/punch-k6-performance/**` | upstream skill, `k6-performance.instructions.md` | governance-review clean; `./bin/punch run gate` still green | human confirms scope |
| **F6.3** | Record exclusions explicitly in `skill-registry.md` "Deferred/Excluded" (ci-cd, frontend-ui, browser-testing, webperf, accessibility) | `docs/ai/skill-registry.md` | conflict report C3/C5 | governance-review clean | human confirms exclusions |

---

## Phase 7 — Contracts, index, validator *(P3)*

| Task | Goal | Allowed | Read-only | Validation | Checkpoint |
|---|---|---|---|---|---|
| **C7.1** | Slim `AGENTS.md` to a pointer contract (de-dup vs copilot-instructions/operating-model) | `AGENTS.md` | `operating-model.md` | governance-review: no restated rule | human diff review |
| **C7.2** | Build a Punch skill index (adapted `using-agent-skills`) spanning domain + lifecycle skills; add CLAUDE.md skill-discovery pointer | new `.github/skills/using-punch-skills/SKILL.md` (or `skill-registry.md` section), `CLAUDE.md` | all skills | governance-review clean; index lists every registered skill | human confirms index location |
| **C7.3** | Reimplement `validate-skills.js` as **stdlib Python** or fold checks into `punch-governance-review` (no host Node) | `src/punch/**` *(if CLI)* **or** `.github/skills/punch-governance-review/**` | upstream `scripts/validate-skills.js` | if CLI: `python3 -m punch --help` + `./bin/punch run smoke` → `punch-run.json passed:true`; else governance-review clean | human chooses CLI vs skill-only |

> C7.3 is the **only task that may touch `src/punch/**`** (and only if a CLI
> validator is chosen). If so, it follows the *product-code* rules: use
> `punch-build-orchestrator`, stdlib-only, and it **must** produce
> `reports/state/punch-run.json`. Otherwise keep it inside the governance skill.

---

## Dependency order

```
Phase 1 (G1.1→G1.4)  ──►  Phase 3 (A3.1..A3.5)  ──►  Phase 4 (P4.1..P4.3)
   │  (unblocker)              │                         │
   └──────────────────────────┴─►  Phase 5 (AG5.x)  ─────┤
                                    Phase 6 (F6.x)   ─────┤
                                                          └─►  Phase 7 (C7.x)
```
- Phase 1 is a hard prerequisite for everything.
- A3.2 must land before P4.2 (Build prompts activate its skills).
- AG5.1 should follow A3.5 (security agent references the security skill).
- C7.2 (index) closes after all skills exist.

## Risk register

| Risk | Likelihood | Mitigation |
|---|---|---|
| Skill sprawl breaches the (reframed) cap | Med | Each A3.x must name its decision/method domain in `skill-registry.md`; F6.x folds rather than adds |
| Lifecycle skill restates a Punch stack rule (drift) | Med | Adaptation rule: cross-link to instructions; governance-review duplication pass |
| Prompt slimming drops a Build scope table | Low | P4.2 validation asserts scope tables unchanged |
| Web examples leak into Punch skills | Med | grep gate for `npm`/`jest`/CWV/`/mnt/`/`subagent_type` in every A3.x |
| `punch-ship` accidentally gains review fan-out | Low | C2 resolution explicit; AG/P4 tasks never touch `punch-ship` |
| Provenance edited by mistake | Low | `.ai-upstream/**` is Forbidden in every task |

## Global rollback strategy

Every task is a single, self-contained commit touching only its Allowed paths
(skill folder + registry row, or one prompt + registry row). Rollback = `git
revert` that commit; no schema/contract/runtime change is introduced by any
Phase 1–7 task except optional C7.3 (which carries its own `punch-run.json`
evidence and standard orchestrator rollback).

## Definition of done

The absorption is complete when the acceptance checklist in
[`recommended-target-ai-architecture.md`](recommended-target-ai-architecture.md#acceptance-for-the-absorption-as-a-whole)
passes **and** a worked task flows Spec→Ship using one lifecycle skill + one
domain skill, producing `reports/state/punch-run.json`.
