# Upstream Agent Skills — Inventory

> **Reconciled 2026-06-17 (post-restructure).** Some "relevance to Punch"
> notes below superseded by executed restructure: prompts now
> command-mapped (`punch-define`/`punch-refine` deleted; `idea-refine` runs inside
> `punch-spec`), lifecycle now **6 phases** (Spec absorbs Define),
> `punch-builder-scoped` became **5 builder agents** (9 agents total), and —
> verified against VS Code docs — prompt frontmatter is **`agent:`**, not `mode:`.
> Canonical record: [`agent-skills-absorption-plan.md` § Execution status](agent-skills-absorption-plan.md).
> Upstream asset inventory itself unchanged, still accurate.

> **Status:** Review artifact (no runtime AI config changed). Made
> 2026-06-16 on branch `feat/agent-skills`. Companion to
> [`punch-ai-config-inventory.md`](punch-ai-config-inventory.md),
> [`skill-absorption-matrix.md`](skill-absorption-matrix.md),
> [`ai-config-conflict-report.md`](ai-config-conflict-report.md),
> [`copilot-adaptation-plan.md`](copilot-adaptation-plan.md), and
> [`recommended-target-ai-architecture.md`](recommended-target-ai-architecture.md).

This **Core B** in absorption model: upstream lifecycle skill set
that should generally win for *methodology*, subject to Punch's
architecture constraints.

## Upstream root path

```
.ai-upstream/agent-skills/
```

Tracked in git (appears in `git ls-files` top-level dirs). Near-verbatim
copy of public `agent-skills` package (docs reference
`https://github.com/addyosmani/agent-skills`). Evidence: `docs/getting-started.md`
clone instructions and `agent-skills:<skill>` invocation namespace used by
every file in `commands/`.

## Asset categories found

| Category | Path | Count | Format |
|---|---|---|---|
| Skills | `.ai-upstream/agent-skills/skills/<name>/SKILL.md` | 24 | Markdown + frontmatter (`name`, `description`) |
| Agents (personas) | `.ai-upstream/agent-skills/agents/*.md` | 4 | Markdown, **plain `.md`** |
| Commands (slash) | `.ai-upstream/agent-skills/commands/*.md` | 8 | Claude Code slash-command Markdown |
| Reference docs | `.ai-upstream/agent-skills/docs/*.md` | 4 | Markdown (setup/explainers) |
| Reference checklists | `.ai-upstream/agent-skills/references/*.md` | 5 | Markdown supporting material |
| Scripts | `.ai-upstream/agent-skills/scripts/*.js` | 1 | Node.js (`validate-skills.js`) |
| Cross-agent contract | `.ai-upstream/agent-skills/AGENTS.md` | 1 | Markdown (OpenCode/skill-driven model) |

## Upstream skills (24)

Frontmatter `name` / `description` verified by reading each `SKILL.md`.
**Tier** = this review's initial relevance judgment to Punch (see filtering
logic in task brief and [absorption matrix](skill-absorption-matrix.md)).

| # | Skill | Lines | Tier | Initial relevance to Punch |
|---|---|--:|:--:|---|
| 1 | `spec-driven-development` | 200 | A | Spec phase core. Adapt: strip "this is a web application" default + `npm` commands. |
| 2 | `planning-and-task-breakdown` | 223 | A | Plan phase core. Adapt to Punch allowed/read-only/forbidden path model. |
| 3 | `incremental-implementation` | 245 | A | Build phase core. Vertical slices inside scoped allow-list. |
| 4 | `test-driven-development` | 383 | A | Verify/Build. **Heavy adapt**: Punch "tests" are k6 + `punch-run.json`, not jest/vitest. |
| 5 | `debugging-and-error-recovery` | 300 | A | Verify failure handling. Mostly generic; light adapt. |
| 6 | `code-review-and-quality` | 347 | A | Review phase core. Reconcile with `punch-reviewer` + `punch-governance-review`. |
| 7 | `code-simplification` | 331 | A | Aligns with Punch "no premature abstraction". New `punch-simplify` prompt. |
| 8 | `documentation-and-adrs` | 278 | A | Docs phase. ADRs new to Punch; adapt to `docs/` conventions. |
| 9 | `git-workflow-and-versioning` | 300 | A | Ship phase. Align with Punch "mechanical only / humans merge". |
| 10 | `security-and-hardening` | 461 | A | Review/security. Adapt: Punch has gateway/orders/Postgres but no web auth. |
| 11 | `shipping-and-launch` | 309 | A→Review | **Semantic clash**: maps to Punch *Review* go/no-go, NOT Punch *Ship* (mechanical). |
| 12 | `idea-refine` | 178 | A | **Already copied verbatim** into `.github/skills/` (see conflict report). |
| 13 | `interview-me` | 225 | A/B | Define-phase requirement extraction. Overlaps Define + idea-refine. |
| 14 | `performance-optimization` | 350 | B/C | Mostly Core Web Vitals + React. Overlaps `punch-k6-performance`. Fold useful parts; exclude web. |
| 15 | `observability-and-instrumentation` | 201 | B | Overlaps `punch-data-harvest` (logs/evidence). Fold RED-metric ideas. |
| 16 | `ci-cd-and-automation` | 390 | C | **Conflicts** "CI/CD is external to Punch". npm/Prisma/Playwright stack. Exclude from core. |
| 17 | `api-and-interface-design` | 294 | B | Punch services expose HTTP APIs. Selective, low priority. |
| 18 | `source-driven-development` | 194 | B | "Ground code in official docs" (k6/Docker/Postgres). Light adapt, low priority. |
| 19 | `context-engineering` | 289 | B | Overlaps `punch-context` skill. Merge concept; no duplicate. |
| 20 | `deprecation-and-migration` | 206 | B | Relevant (retire legacy `bin/*`; schema migration). Low priority. |
| 21 | `doubt-driven-development` | 243 | B | Adversarial review of high-stakes decisions. Aligns with Punch "stop and ask". |
| 22 | `frontend-ui-engineering` | 328 | C | **Exclude** — Punch has no frontend. |
| 23 | `browser-testing-with-devtools` | 304 | C | **Exclude/defer** — Chrome DevTools MCP; distinct from deferred k6-browser. |
| 24 | `using-agent-skills` | 189 | Meta | Discovery meta-skill (task→skill flowchart). Adapt into Punch skill index; no duplicate of lifecycle table. |

Notes from reading skills:
- `using-agent-skills` lifecycle map (`SKILL.md:138-159`) **nearly
  isomorphic** to Punch's Define→Spec→Plan→Build→Verify→Review→Ship — strongest
  argument absorption natural, not grafted.
- Several Tier-A skills carry **web/Node defaults** in examples
  (`spec-driven-development/SKILL.md:42-47` assumes web app; `ci-cd` and
  `performance-optimization` npm/React-centric). *Workflow* reusable;
  *examples* must yield to Punch's path-instructions.
- `idea-refine` ships `scripts/idea-refine.sh` referencing claude.ai
  runtime path `/mnt/skills/user/idea-refine/...` — inert under Punch's
  Docker-first model.

## Upstream agents (4 personas)

Plain `.md` (not `.agent.md`). Each has `name` + `description` frontmatter and
"Composition" block. **GitHub Copilot requires `*.agent.md`** (upstream's own
`docs/copilot-setup.md:22-25`), so all four need renaming on adaptation.

| Agent | Lines | Role | Punch mapping |
|---|--:|---|---|
| `code-reviewer.md` | 97 | Five-axis reviewer | Overlaps `punch-reviewer`. **Merge/augment**, no duplicate persona. |
| `security-auditor.md` | 112 | Vulnerability/threat review | **New persona** Punch lacks. Adapt scope to Punch surfaces. |
| `test-engineer.md` | 95 | Test strategy/coverage | Overlaps `punch-verifier`. Punch has no unit suite — likely **exclude as persona**, keep "Prove-It" in TDD skill. |
| `web-performance-auditor.md` | 184 | Core Web Vitals audit | **Exclude** — frontend/CWV only. |

## Upstream commands (8 slash commands)

These **thin wrappers** (15–72 lines) that invoke a skill — exactly the
"prompt = thin entry point" shape Punch prompts should move toward. Claude
Code format: `Invoke the agent-skills:<skill> skill`, `$ARGUMENTS`, subagent
fan-out.

| Command | Lines | Invokes | Punch prompt mapping |
|---|--:|---|---|
| `spec.md` | 15 | `spec-driven-development` | `punch-spec` (exists) |
| `plan.md` | 16 | `planning-and-task-breakdown` | `punch-plan` (exists) |
| `build.md` | 44 | `incremental-implementation` + `test-driven-development` | `punch-build-*` (exists). **`/build auto` autonomous mode conflicts** with Punch "one task, human approves". |
| `test.md` | 19 | `test-driven-development` | Fold into `punch-verify`/Build — no new prompt. |
| `review.md` | 16 | `code-review-and-quality` | `punch-review` (exists) |
| `code-simplify.md` | 22 | `code-simplification` | **New** `punch-simplify` prompt. |
| `ship.md` | 72 | `shipping-and-launch` (parallel fan-out to 3 personas) | Maps to Punch **Review**, not Ship. Don't overwrite `punch-ship` (mechanical). |
| `webperf.md` | 32 | `web-performance-auditor` | **Exclude** — frontend. |

## Upstream reference docs (4)

| Doc | Lines | Purpose | Use to Punch |
|---|--:|---|---|
| `docs/getting-started.md` | 146 | Universal setup + lifecycle | Provenance; informs adaptation plan. |
| `docs/copilot-setup.md` | 87 | **Copilot-specific wiring** | Primary source for `.github/agents/*.agent.md` rule and `.github/skills`/`.agents/skills` validity. |
| `docs/agents.md` | 123 | Persona/skill/command decision matrix | Informs agent composition rules. |
| `docs/skill-anatomy.md` | 149 | SKILL.md format spec | Informs Punch's SKILL.md frontmatter contract. |

## Notable assets / resources / templates / scripts

| Asset | Path | Note |
|---|---|---|
| `validate-skills.js` | `scripts/` | Node validator for skill frontmatter. **Conflicts** with Punch "no host Node". Reimplement in stdlib Python or fold into `punch-governance-review`. |
| `testing-patterns.md` | `references/` | Supports adapted TDD skill. |
| `security-checklist.md` | `references/` | Supports adapted `security-and-hardening`. |
| `performance-checklist.md` | `references/` | Web-leaning; salvage non-web parts for perf work. |
| `accessibility-checklist.md` | `references/` | **Exclude** — frontend only. |
| `orchestration-patterns.md` | `references/` | 370-line Claude-Code multi-agent catalog. Keep as reference; Copilot-adapt fan-out claims. |
| `idea-refine/scripts/idea-refine.sh` | `skills/idea-refine/scripts/` | claude.ai `/mnt/skills/...` path; inert in Punch. |

## Headline observations

1. **Philosophical match.** Upstream's three layers — Skills (*how*),
   Personas (*who*), Commands (*when*) (`docs/agents.md:13-23`) — same
   taxonomy Punch already uses (Skills/Agents/Prompts in
   `docs/ai/operating-model.md:36-50`). Absorption a *reconciliation*, not
   transplant.
2. **Skill-first vs prompt-first.** Upstream skill-first, mandates "if a
   task matches a skill, you MUST invoke it" (`AGENTS.md:16`). Punch
   prompt-first, **caps skills at 6 domains**, explicitly states "lifecycle
   phases are prompts and agents, not skills"
   (`docs/ai/skill-registry.md:60`). Central conflict — see
   [conflict report](ai-config-conflict-report.md).
3. **Stack mismatch in examples.** Lifecycle *workflows* stack-neutral;
   *examples* assume web/Node. Punch's `.github/instructions/**` must win
   on stack specifics (Decision policy #1).
