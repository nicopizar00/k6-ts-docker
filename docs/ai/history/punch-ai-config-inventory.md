# Punch AI Configuration — Inventory

> **Reconciled 2026-06-17.** The tables below are the **pre-restructure baseline**
> (the starting state this review captured). The config has since been
> restructured: **11 prompts** (`punch-define`/`punch-refine` deleted, `punch-test`
> added), **9 agents** (`punch-builder-scoped` → 5 builder agents + 4 core
> personas), **6-phase** lifecycle (Spec absorbs Define), and prompt frontmatter
> is **`agent:`** (not `mode:`). The drift findings in §9 are now **resolved** —
> see the per-item notes there. Canonical current record:
> [`agent-skills-absorption-plan.md` § Execution status](agent-skills-absorption-plan.md).

> **Status:** Review artifact (no runtime AI config changed). Produced
> 2026-06-16 on branch `feat/agent-skills`. Companion to
> [`upstream-agent-skills-inventory.md`](upstream-agent-skills-inventory.md)
> and the other four review docs in this folder.

This is **Feature A** in the absorption model: the existing, deliberately
governed Punch AI configuration. It is **mature and largely Copilot-best-practice
already** — the absorption must preserve it, not overwrite it.

## 1. Global Copilot instructions

| File | Lines | Role | Health |
|---|--:|---|---|
| `.github/copilot-instructions.md` | 111 | Always-on global rules; deliberately short; links out to `docs/ai/` and `CLAUDE.md` | **Good.** Already follows upstream's "keep instructions concise" advice (`copilot-setup.md:84`). Not a workflow dump. |

Notable content: Critical Rules (Docker First, stdlib Python, mandatory
`punch-run.json` evidence, human-approves-Ship, no secrets); architecture
ownership table; agentic rules; lifecycle entry-point table.

## 2. Path-specific instructions (`.github/instructions/`, 7)

These encode the **Punch architecture constraints that must override generic
upstream examples** (Decision policy #1). All carry `applyTo:` + `description:`.

| File | `applyTo` | Owns |
|---|---|---|
| `punch-architecture.instructions.md` | `**` | Always-on ownership map + anti-patterns. |
| `agentic-workflow.instructions.md` | `.github/**,docs/ai/**,CLAUDE.md,AGENTS.md` | Phase/mode discipline; **frontmatter contract**; "when adding an AI asset" gate. |
| `python-orchestrator.instructions.md` | `src/punch/**,bin/punch` | Stdlib-only; streaming; exit codes; mandatory evidence artifact. |
| `docker-compose.instructions.md` | (compose/docker) | Service contracts, healthchecks, image pins. |
| `k6-performance.instructions.md` | `src/tests/**/*.ts*` | HTTP vs Browser separation; thresholds; `handleSummary`; no host k6. |
| `artifacts-reporting.instructions.md` | `src/tests/support/**,src/punch/**,reports/**,docs/validation/**` | Stable artifact paths; low-noise console/full-file logs; compact JSON. |
| `documentation.instructions.md` | (docs) | Documentation conventions. |

## 3. Prompt files (`.github/prompts/`, 12 on disk)

`prompt-registry.md` declares **11**. There are **12 files**. The extra is
`punch-refine.prompt.md` — **unregistered** (see Stale/drift below).

| Prompt | Phase | Mode | Registered? | Note |
|---|---|---|:--:|---|
| `punch-define` | Define | Ask | ✅ | |
| `punch-spec` | Spec | Ask | ✅ | Slim candidate → delegate to `spec-driven-development`. |
| `punch-plan` | Plan | Ask (Plan discipline) | ✅ | Slim candidate → `planning-and-task-breakdown`. |
| `punch-build-orchestrator` | Build | Agent | ✅ | |
| `punch-build-compose` | Build | Agent | ✅ | |
| `punch-build-k6-http` | Build | Agent | ✅ | |
| `punch-build-k6-browser` | Build | Agent | ✅ | (deferred domain) |
| `punch-build-data-harvest` | Build | Agent | ✅ | |
| `punch-verify` | Verify | Agent/Ask | ✅ | |
| `punch-review` | Review | Ask | ✅ | Slim candidate → `code-review-and-quality`. |
| `punch-ship` | Ship | Agent (mechanical) | ✅ | **Mechanical only** — do not import upstream `/ship` fan-out here. |
| `punch-refine` | (Define-ish) | — | ❌ → deleted | **Drift (resolved):** had `name:`/`argument-hint:` frontmatter; since **deleted** (idea-refine runs inside `punch-spec`). Verified prompt field is `agent:`, not `mode:`. |

Prompts are currently **heavy** (57–94 lines) and restate procedure — the
opposite of upstream's 15–22-line wrappers. This is the main "slim and
delegate" target.

## 4. Custom agents (`.github/agents/`, 5)

All correctly named `*.agent.md` (Copilot-compatible) with `name:` +
`description:`.

| Agent | Persona | Phases |
|---|---|---|
| `punch-architect-readonly` | Read-only investigator | Define, Spec |
| `punch-planner` | Scoped-task planner | Plan |
| `punch-builder-scoped` | Scope-bound builder | Build (all 5 domains) |
| `punch-verifier` | Evidence collector | Verify |
| `punch-reviewer` | Diff critic + ship mechanic | Review, Ship |

Capped at 5 personas by `operating-model.md:100-102`.

## 5. Skills (`.github/skills/`, 7 dirs)

Skills live in **`.github/skills/`** (a Copilot-valid location per
`copilot-setup.md:7`), **not** `.agents/skills/` (which does not exist).
`skill-registry.md` declares **6**. There are **7 dirs** — the extra is
`idea-refine` (**unregistered**).

| Skill dir | Registered? | Decision domain | Frontmatter |
|---|:--:|---|---|
| `punch-context` | ✅ | Project primer / pointer list | `name`,`description` |
| `punch-python-orchestration` | ✅ | The `bin/punch` CLI + subprocess control | `name`,`description` |
| `punch-docker-compose` | ✅ | Compose/Dockerfile runtime contracts | `name`,`description` |
| `punch-k6-performance` | ✅ | k6 HTTP+Browser, thresholds, `handleSummary` | `name`,`description` |
| `punch-data-harvest` | ✅ | Artifact paths/schemas, log noise discipline | `name`,`description` |
| `punch-governance-review` | ✅ | AI-config health audit | `name`,`description`,`applies-to`,`allowed-tools` |
| `idea-refine` | ❌ | (upstream lifecycle skill) | `name`,`description` only — **missing `applies-to`** required by `agentic-workflow.instructions.md:50` |

Supporting files present: `punch-k6-performance` (http/browser templates,
thresholds.md), `punch-docker-compose` (compose-contract.md), `punch-data-harvest`
(artifact-contract.md), `punch-python-orchestration` (streaming example),
`idea-refine` (examples/frameworks/refinement-criteria + a `scripts/idea-refine.sh`).

## 6. Claude Code config (`.claude/`, `CLAUDE.md`)

| Path | Content | Note |
|---|---|---|
| `.claude/settings.json` | `{ enabledPlugins: { enhance@agentsys } }` | Harness-level only. No `.claude/skills`, `.claude/commands`, or `.claude/agents`. |
| `.claude/settings.local.json` | local settings | Harness-level. |
| `CLAUDE.md` | 170 lines | **The "constitution".** Referenced as canonical by `copilot-instructions.md:13` and `operating-model.md:125`. **Not** a thin compat layer today — it is the source many files link to. |

Implication: the generic guidance "CLAUDE.md should be minimal" conflicts with
Punch's deliberate use of CLAUDE.md as the canonical constitution. This review
recommends **preserving CLAUDE.md's constitutional role** (see
[target architecture](recommended-target-ai-architecture.md)).

## 7. Cross-agent contract (`AGENTS.md`)

| File | Lines | Note |
|---|--:|---|
| `AGENTS.md` | 123 | Cross-agent guide (Claude/Cursor/Copilot/Codex). **Partially duplicates** `copilot-instructions.md` and `operating-model.md` (lifecycle tables, agent/skill lists, rules). Slim-to-pointer candidate. |

## 8. AI governance docs (`docs/ai/`, 8 + these 6 review docs)

| Doc | Lines | Role |
|---|--:|---|
| `operating-model.md` | 126 | The lifecycle + 4-asset taxonomy + anti-sprawl ceilings. |
| `workflow.md` | 223 | Step-by-step lifecycle walkthrough + worked example. |
| `scoped-build-policy.md` | 154 | Allowed/read-only/forbidden paths per Build domain. |
| `model-selection.md` | 99 | Model class per phase (vendor-neutral). |
| `copilot-mode-mapping.md` | 70 | Phase → Ask/Agent mapping. |
| `maintenance-matrix.md` | 85 | File-level change cascade. |
| `skill-registry.md` | 78 | The 6-skill register + cap-lifting discipline. |
| `prompt-registry.md` | 80 | The 11-prompt register + contract. |

Also referenced but **outside `docs/ai/`**: `docs/architecture/punch-boundaries.md`
(layer ownership), `docs/workflows/validation.md`, `docs/validation/README.md`.

## 9. Possible stale / duplicated / drifting files

Concrete, evidence-backed findings (verified at review time). **Findings 1–3 are
now RESOLVED (2026-06-17):** `idea-refine` registered + `applies-to` added +
`/mnt` path removed; `punch-refine` deleted (idea-refine runs inside `punch-spec`).

1. **`idea-refine` skill is unregistered.** Present in `.github/skills/` but
   absent from `skill-registry.md` (which lists 6, none being idea-refine). By
   `punch-governance-review`'s own rule "every file in `.github/skills/*/SKILL.md`
   has a row in `skill-registry.md`" (`SKILL.md:65-67`) this is **current
   governance drift**.
2. **`punch-refine` prompt is unregistered and off-contract.** Not in
   `prompt-registry.md` (11 rows vs 12 files); its frontmatter used
   `name:`/`argument-hint:` instead of the contract field (**`agent:`** — the
   contract docs then wrongly said `mode:`). **Resolved: `punch-refine` deleted.**
3. **`idea-refine` carries a Claude-only path.** `idea-refine/SKILL.md:22`
   references `/mnt/skills/user/idea-refine/scripts/idea-refine.sh` — a claude.ai
   runtime path that does nothing in Punch's Docker-first model.
4. **`AGENTS.md` ↔ `copilot-instructions.md` ↔ `operating-model.md` overlap.**
   The lifecycle table, agent list, and "rules for AI assistants" appear in all
   three (e.g. `AGENTS.md:84-102` vs `copilot-instructions.md:78-91`). Not a
   contradiction, but a duplication the governance skill is meant to forbid
   ("no rule restated across files", `copilot-instructions.md:74-76`).
5. **CLAUDE.md is in context but `docs/ai/ai-context.md` and other docs are
   referenced inconsistently.** `CLAUDE.md` "For AI assistants" lists
   `docs/ai-context.md`; `copilot-instructions.md` lists `docs/ai/operating-model.md`.
   Worth a cross-reference pass during absorption (not blocking).

> Findings 1–3 share one root cause: a **prior, partial, Claude-Code-style
> absorption of `idea-refine`** that was never reconciled with Punch's
> Copilot-first governance (no registry row, no `applies-to`, no `mode`). It is
> the cautionary precedent for this larger absorption: **copy without
> registering = drift.**
