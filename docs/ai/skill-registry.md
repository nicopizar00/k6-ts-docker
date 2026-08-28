# Skill Registry

Punch skills sit on **two independent axes**:

- **Domain skills** — one per Punch *subsystem* that genuinely needs a
  reusable, activatable procedure beyond what a path instruction can carry.
  No fixed cap — each one earns its place by naming a decision domain no
  path instruction or agent file already owns.
- **Lifecycle skills** — engineering *methods* adapted from upstream
  `agent-skills` set. Separate axis, admitted in batches (absorption plan
  retired — see git history).

Each entry below: responsibility + why it earns a separate skill (not a
path instruction, not agent prose).

## Skill discovery — which skill when

Load skill matching task: **domain skill** for subsystem, **lifecycle skill**
for method. Multiple apply (k6 change uses `punch-k6-testing` +
`punch-incremental-implementation` + `punch-test-driven-development`).

| You are… | Skill(s) / where to look |
|---|---|
| new to the repo | `.github/copilot-instructions.md` (always-on hub) + `docs/architecture/punch-boundaries.md` |
| refining a vague idea | `punch-spec-driven-development` (clarify step, absorbed) |
| writing a spec | `punch-spec-driven-development` |
| breaking a spec into tasks | `punch-planning-and-task-breakdown` |
| editing the orchestrator | [`python-orchestrator.instructions.md`](../../.github/instructions/python-orchestrator.instructions.md) + `punch-incremental-implementation` |
| editing compose / Dockerfiles | [`docker-compose.instructions.md`](../../.github/instructions/docker-compose.instructions.md) + `punch-incremental-implementation` |
| writing / changing a k6 test | `punch-k6-testing` + `punch-test-driven-development` + `punch-incremental-implementation` |
| changing an artifact / report | [`artifacts-reporting.instructions.md`](../../.github/instructions/artifacts-reporting.instructions.md) + `punch-incremental-implementation` |
| a run failed | `punch-debugging-and-error-recovery` |
| proving a fix RED→GREEN | `punch-test-driven-development` |
| reviewing a diff | `punch-code-review-and-quality` (readability/simplicity axis in-file, + `punch-security-and-hardening`) |
| committing / shipping | `punch-git-workflow-and-versioning` |
| recording a decision (ADR) | `punch-documentation-and-adrs` |
| a high-stakes / irreversible decision | `punch-doubt-driven-development` |
| coding against a k6/Docker/Postgres API | `punch-source-driven-development` |
| a gate/journey threshold regressed | `punch-performance-optimization` (+ `punch-k6-testing`) |
| instrumenting a service (logs/events) | [`artifacts-reporting.instructions.md`](../../.github/instructions/artifacts-reporting.instructions.md) (Observability discipline section) |
| auditing AI config | [`punch-ai-governance`](../../.github/agents/punch-ai-governance.agent.md) agent |

## Domain skills

| Skill | Owns | Defined in |
|---|---|---|
| [`punch-k6-testing`](../../.github/skills/punch-k6-testing/SKILL.md) | k6 test shape (HTTP + Browser), thresholds, `handleSummary`, shared report builder, k6 image pin, Browser deferral | `.github/skills/punch-k6-testing/SKILL.md` |

### Why only one

A 2026-08-28 governance sweep retired five domain skills that turned out to
be either always-on context or thin wrappers around content a path
instruction could carry just as well:

| Retired skill | What happened to its content |
|---|---|
| `punch-context-engineering` | Deleted outright — it was a pointer-list primer to canonical docs, which is what the always-on hub (`copilot-instructions.md`) already is. No content survived; agents just read the hub. |
| `punch-python-orchestration` | Streaming-subprocess pattern + rules folded into [`python-orchestrator.instructions.md`](../../.github/instructions/python-orchestrator.instructions.md). |
| `punch-compose-runtime` | Service-contract template + rules folded into [`docker-compose.instructions.md`](../../.github/instructions/docker-compose.instructions.md). |
| `punch-data-harvest` | Artifact-schema table + Observability discipline folded into [`artifacts-reporting.instructions.md`](../../.github/instructions/artifacts-reporting.instructions.md). |
| `punch-ai-governance` (the skill) | Its audit procedure, canon adopt-adapt report, and output format folded directly into the [`punch-ai-governance`](../../.github/agents/punch-ai-governance.agent.md) agent — the agent was the only thing that ever activated it, so the split added a hop with no reader benefit. |

`punch-k6-testing` earns standalone status because performance semantics
(what "fast enough" means, threshold design) is a genuinely distinct
decision domain with its own reviewers and failure modes — not something a
path instruction's rule-list format fits well.

### Adding a new domain skill

Propose a Plan that:

1. Names the new skill and its decision domain.
2. Shows which existing path instruction or agent file could **not** absorb
   the responsibility (the 2026-08-28 sweep's bar — a skill earns its place
   only when a path instruction genuinely can't carry it).
3. Demonstrates a real, recurring decision existing assets mishandle.
4. Updates this registry in the same PR.

If steps 2–3 cannot be answered concretely, answer is "don't add it".

## Lifecycle skills (method axis — not capped)

Lifecycle skills encode reusable engineering *methods* adapted from upstream
`agent-skills` set. Phase prompt activates **one lifecycle skill** (method)
plus the relevant **domain skill or path instructions** (Punch specifics) —
how skill-first execution coexists with Punch's phase/scope governance.
Punch's path-instructions always win on stack specifics; lifecycle skill
supplies method, not stack rules.

| Lifecycle skill | Method | Activated by | Defined in |
|---|---|---|---|
| [`punch-spec-driven-development`](../../.github/skills/punch-spec-driven-development/SKILL.md) | Spec before code — surface assumptions, reframe as success criteria | [`punch-spec`](../../.github/prompts/punch-spec.prompt.md) | `.github/skills/punch-spec-driven-development/SKILL.md` |
| [`punch-planning-and-task-breakdown`](../../.github/skills/punch-planning-and-task-breakdown/SKILL.md) | Decompose spec into scoped, verifiable tasks | [`punch-plan`](../../.github/prompts/punch-plan.prompt.md) | `.github/skills/punch-planning-and-task-breakdown/SKILL.md` |
| [`punch-incremental-implementation`](../../.github/skills/punch-incremental-implementation/SKILL.md) | Thin vertical slices; Build edits, Test runs, Ship commits | [`punch-build`](../../.github/prompts/punch-build.prompt.md) + `punch-builder` | `.github/skills/punch-incremental-implementation/SKILL.md` |
| [`punch-test-driven-development`](../../.github/skills/punch-test-driven-development/SKILL.md) | RED→GREEN via k6 checks/thresholds + `punch-run.json`; Prove-It for bugs | [`punch-test`](../../.github/prompts/punch-test.prompt.md), `punch-build` (via `punch-builder`) | `.github/skills/punch-test-driven-development/SKILL.md` |
| [`punch-debugging-and-error-recovery`](../../.github/skills/punch-debugging-and-error-recovery/SKILL.md) | Root-cause triage: reproduce → localize → fix → guard | [`punch-test`](../../.github/prompts/punch-test.prompt.md), `punch-test-engineer` | `.github/skills/punch-debugging-and-error-recovery/SKILL.md` |
| [`punch-code-review-and-quality`](../../.github/skills/punch-code-review-and-quality/SKILL.md) | Five-axis review before merge; AI-config axis → `punch-ai-governance` agent | [`punch-review`](../../.github/prompts/punch-review.prompt.md), `punch-code-reviewer` | `.github/skills/punch-code-review-and-quality/SKILL.md` |
| [`punch-git-workflow-and-versioning`](../../.github/skills/punch-git-workflow-and-versioning/SKILL.md) | Atomic commits, short-lived branches, conventional messages | [`punch-ship`](../../.github/prompts/punch-ship.prompt.md) | `.github/skills/punch-git-workflow-and-versioning/SKILL.md` |
| [`punch-documentation-and-adrs`](../../.github/skills/punch-documentation-and-adrs/SKILL.md) | Record decisions (ADRs) + why; keep docs/contracts current | decisions/contract changes; `documentation.instructions.md` | `.github/skills/punch-documentation-and-adrs/SKILL.md` |
| [`punch-security-and-hardening`](../../.github/skills/punch-security-and-hardening/SKILL.md) | Threat-model + harden Punch surfaces (gateway input, Postgres, secrets, supply chain) | Review security axis; `punch-security-auditor` | `.github/skills/punch-security-and-hardening/SKILL.md` |
| [`punch-doubt-driven-development`](../../.github/skills/punch-doubt-driven-development/SKILL.md) | Fresh-context adversarial review of non-trivial/high-stakes decisions | Plan + Build (on-demand) | `.github/skills/punch-doubt-driven-development/SKILL.md` |
| [`punch-source-driven-development`](../../.github/skills/punch-source-driven-development/SKILL.md) | Ground framework code (k6/Docker/Postgres) in official docs + cite | Build (on-demand) | `.github/skills/punch-source-driven-development/SKILL.md` |
| [`punch-performance-optimization`](../../.github/skills/punch-performance-optimization/SKILL.md) | Measure-first k6 perf work; threshold-RED → fix backend bottleneck → re-run → guard | Build/Test (on threshold regression) | `.github/skills/punch-performance-optimization/SKILL.md` |

Every lifecycle skill above absorbed and registered. `punch-performance-optimization`
was folded then **promoted back to standalone** (per owner direction), same
for `punch-observability-and-instrumentation` before it was **re-folded and
retired** into `artifacts-reporting.instructions.md`'s "Observability
discipline" section — one canonical owner instead of two overlapping files.
`punch-browser-testing-with-devtools` was adopted, adapted, then **retired**
(2026-08-28) — zero `.github/` activation reference was ever wired in, and
its sole target (`browser-smoke.ts.example`) stays a deferred placeholder
per CLAUDE.md, so there was nothing left for it to gate.

## Full provenance

Pinned upstream commit, all 24 source skills, the 3 adopted personas, each
with an explicit disposition — lives in
[`agent-skills-provenance.md`](agent-skills-provenance.md). Not restated
here. Two upstream-maintained vendor skills (`graphify`, `caveman`) were
adopted and later **retired** (2026-08-28) — a general-purpose external
visualization utility and a personal comms-style preference, neither a
Punch-specific capability; both now ship their own official installers for
a user who wants them, entirely outside Punch's `.github/` config.

## Why these are still deferred (not created)

| Candidate | Why it does NOT exist as a skill |
|---|---|
| `punch-k6-http` and `punch-k6-browser` | Splitting `punch-k6-testing` again fragments single decision domain (performance semantics). HTTP and Browser live in one skill with sub-sections. |
| `punch-monitoring` / `punch-injectables` | No real monitoring or fault-injection use case yet. Premature. Layer slot reserved in `punch-boundaries.md`. |
| `punch-documentation` | `documentation.instructions.md` path file enough. Skill would only restate it. |
| `punch-(define\|spec\|plan\|build\|verify\|review\|ship)` | **Phases are prompts and agents, not skills** — never create `punch-<phase>` skill. Phase prompt may *activate* lifecycle method skill (e.g. `punch-spec` → `punch-spec-driven-development`); phase stays prompt+agent, method is skill. |
| `context-engineering` (upstream) | **Retired** (2026-08-28) — was folded into `punch-context-engineering`, but that skill itself was deleted as redundant with the always-on hub. No skill maps this upstream slug today. |
| `ci-cd-and-automation` (upstream) | **Excluded** — CI/CD external to Punch (`punch-architecture.instructions.md`); npm/Prisma/Playwright stack doesn't fit. |
| `frontend-ui-engineering`, `webperf`, `web-performance-auditor` (upstream) | **Excluded** — Punch has no frontend. |
| `browser-testing-with-devtools` (upstream) | **Deferred (retired 2026-08-28)** — adopted once for future k6 Browser tests, but its only target (`browser-smoke.ts.example`) stays an explicitly deferred placeholder per CLAUDE.md and it never got a single `.github/` activation reference. Re-adopt if a Plan ever actually enables k6 Browser. |
| `interview-me` (upstream) | **Deferred** — overlaps `punch-spec-driven-development`'s absorbed clarify step, which already owns pre-Spec intent extraction. Second "refine" skill would split one decision domain (absorption matrix §A, P3). |
| `shipping-and-launch` (upstream) | **Deferred** — name and deploy/rollback model clash with Punch's deliberately mechanical, human-gated `punch-ship`; go/no-go decision lives in Review phase (`punch-code-review-and-quality`), not a skill. |
| `api-and-interface-design` (upstream) | **Deferred** — Punch's only interface surface is gateway/orders HTTP contract, already governed by `docker-compose.instructions.md` + `punch-security-and-hardening`. No recurring interface-design decision yet (absorption matrix §A, P3). |
| `deprecation-and-migration` (upstream) | **Deferred** — legacy `bin/*` retirement and Postgres schema moves infrequent, handled by `punch-documentation-and-adrs` + `punch-git-workflow-and-versioning`. Revisit if migration cadence grows (absorption matrix §A, P3). |

## Adding a new lifecycle skill

Governed by absorption plan, not domain cap, but each must (1) name unique
engineering method, (2) not duplicate domain skill or path-instruction, (3)
be registered in the Lifecycle-skills table in the same PR that adds it.

The [`punch-ai-governance`](../../.github/agents/punch-ai-governance.agent.md)
agent flags any skill on disk without a row in either skills table during
Review.
