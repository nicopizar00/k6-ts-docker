# Skill Registry

Punch skills sit on **two independent axes**:

- **Domain skills** — one per Punch *subsystem*. Capped at **six**; seventh
  needs killing one.
- **Lifecycle skills** — engineering *methods* adapted from upstream
  `agent-skills` set. Separate axis, **not** under domain cap; admitted in
  batches (absorption plan retired — see git history).

Each entry below: responsibility + why earns separate skill. "Deferred"
section lists candidates intentionally **not** created.

## Skill discovery — which skill when

Load skill matching task: **domain skill** for subsystem, **lifecycle skill**
for method. Multiple apply (k6 change uses `punch-k6-testing` +
`punch-incremental-implementation` + `punch-test-driven-development`).

| You are… | Skill(s) |
|---|---|
| new to the repo | `punch-context-engineering` |
| routing a repo-understanding / cross-file / architecture / governance task (before picking the sub-agent) | `punch-context-engineering` |
| refining a vague idea | `punch-spec-driven-development` (clarify step, absorbed) |
| writing a spec | `punch-spec-driven-development` |
| breaking a spec into tasks | `punch-planning-and-task-breakdown` |
| editing the orchestrator | `punch-python-orchestration` + `punch-incremental-implementation` |
| editing compose / Dockerfiles | `punch-compose-runtime` + `punch-incremental-implementation` |
| writing / changing a k6 test | `punch-k6-testing` + `punch-test-driven-development` + `punch-incremental-implementation` |
| changing an artifact / report | `punch-data-harvest` + `punch-incremental-implementation` |
| a run failed | `punch-debugging-and-error-recovery` |
| proving a fix RED→GREEN | `punch-test-driven-development` |
| reviewing a diff | `punch-code-review-and-quality` (readability/simplicity axis in-file, + `punch-security-and-hardening`) |
| committing / shipping | `punch-git-workflow-and-versioning` |
| recording a decision (ADR) | `punch-documentation-and-adrs` |
| a high-stakes / irreversible decision | `punch-doubt-driven-development` |
| coding against a k6/Docker/Postgres API | `punch-source-driven-development` |
| a gate/journey threshold regressed | `punch-performance-optimization` (+ `punch-k6-testing`) |
| instrumenting a service (logs/events) | `punch-data-harvest` (Observability discipline section) |
| writing a k6 Browser test (Plan task) | `punch-browser-testing-with-devtools` (+ `punch-k6-testing`) |
| auditing AI config | `punch-ai-governance` |

## Domain skills (six — capped)

| Skill | Owns | Defined in |
|---|---|---|
| [`punch-context-engineering`](../../.github/skills/punch-context-engineering/SKILL.md) | Pointer-list to canonical docs; lifecycle; scope-discipline principle | `.github/skills/punch-context-engineering/SKILL.md` |
| [`punch-python-orchestration`](../../.github/skills/punch-python-orchestration/SKILL.md) | `bin/punch` CLI, subprocess streaming, docker compose invocation, exit codes, evidence artifact | `.github/skills/punch-python-orchestration/SKILL.md` |
| [`punch-compose-runtime`](../../.github/skills/punch-compose-runtime/SKILL.md) | Service contracts, stable service names, healthchecks, multi-stage Dockerfiles, image pins | `.github/skills/punch-compose-runtime/SKILL.md` |
| [`punch-k6-testing`](../../.github/skills/punch-k6-testing/SKILL.md) | k6 test shape (HTTP + Browser), thresholds, `handleSummary`, shared report builder, k6 image pin, Browser deferral | `.github/skills/punch-k6-testing/SKILL.md` |
| [`punch-data-harvest`](../../.github/skills/punch-data-harvest/SKILL.md) | Artifact paths and schemas, terminal-vs-file noise discipline, JSON/CSV contracts, HTML report builder | `.github/skills/punch-data-harvest/SKILL.md` |
| [`punch-ai-governance`](../../.github/skills/punch-ai-governance/SKILL.md) | Frontmatter contracts, registry consistency, boundary compliance, scope discipline, handoff hygiene | `.github/skills/punch-ai-governance/SKILL.md` |

### Why six, and what each adds

Each domain skill names unique **decision domain**:

| Skill | Decision domain |
|---|---|
| `punch-context-engineering` | "What primer does any agent need?" |
| `punch-python-orchestration` | "How does the run happen?" |
| `punch-compose-runtime` | "What is the runtime contract?" |
| `punch-k6-testing` | "What does fast enough mean?" |
| `punch-data-harvest` | "What artifacts does the run produce?" |
| `punch-ai-governance` | "Is the AI operating model itself healthy?" |

These domains have different reviewers, failure modes, cadences. Splitting
keeps each concern isolated.

### Why the cap moved from 3 to 6

Previous registry capped at three (`punch-orchestration`,
`punch-performance-k6`, `punch-ai-governance-audit`). Redesign deliberately
lifted cap to admit three previously-deferred decision domains:

| New skill | What it admits |
|---|---|
| `punch-context-engineering` | Common entry point so each Build prompt no longer duplicates "load this primer first". |
| `punch-compose-runtime` | Compose contracts (service names, healthchecks, image pins) were implied in path-instruction file but had no skill to activate during Build. Contract template makes cost of Compose changes visible at Plan time. |
| `punch-data-harvest` | Artifacts were owned half by `punch-orchestration` (state files), half by `punch-performance-k6` (HTML/JSON). Centralizing artifact *contract* in one skill keeps downstream consumers (CI, future automation) coherent. |

Renames (`orchestration` → `python-orchestration`, `performance-k6` →
`k6-performance`, `ai-governance-audit` → `governance-review`) align names with
spec, broaden governance skill's remit from "cap enforcement" to "boundary
discipline + handoff hygiene".

## Lifecycle skills (method axis — not capped)

Lifecycle skills encode reusable engineering *methods* adapted from upstream
`agent-skills` set. Phase prompt activates **one lifecycle skill** (method)
plus relevant **domain skill** (Punch specifics) — how skill-first execution
coexists with Punch's phase/scope governance. Punch's path-instructions always
win on stack specifics; lifecycle skill supplies method, not stack rules.

| Lifecycle skill | Method | Activated by | Defined in |
|---|---|---|---|
| [`punch-spec-driven-development`](../../.github/skills/punch-spec-driven-development/SKILL.md) | Spec before code — surface assumptions, reframe as success criteria | [`punch-spec`](../../.github/prompts/punch-spec.prompt.md) | `.github/skills/punch-spec-driven-development/SKILL.md` |
| [`punch-planning-and-task-breakdown`](../../.github/skills/punch-planning-and-task-breakdown/SKILL.md) | Decompose spec into scoped, verifiable tasks | [`punch-plan`](../../.github/prompts/punch-plan.prompt.md) | `.github/skills/punch-planning-and-task-breakdown/SKILL.md` |
| [`punch-incremental-implementation`](../../.github/skills/punch-incremental-implementation/SKILL.md) | Thin vertical slices; Build edits, Test runs, Ship commits | [`punch-build`](../../.github/prompts/punch-build.prompt.md) + builder agents | `.github/skills/punch-incremental-implementation/SKILL.md` |
| [`punch-test-driven-development`](../../.github/skills/punch-test-driven-development/SKILL.md) | RED→GREEN via k6 checks/thresholds + `punch-run.json`; Prove-It for bugs | [`punch-test`](../../.github/prompts/punch-test.prompt.md), `punch-build` (via `punch-performance-test-engineer`) | `.github/skills/punch-test-driven-development/SKILL.md` |
| [`punch-debugging-and-error-recovery`](../../.github/skills/punch-debugging-and-error-recovery/SKILL.md) | Root-cause triage: reproduce → localize → fix → guard | [`punch-test`](../../.github/prompts/punch-test.prompt.md), `punch-test-engineer` | `.github/skills/punch-debugging-and-error-recovery/SKILL.md` |
| [`punch-code-review-and-quality`](../../.github/skills/punch-code-review-and-quality/SKILL.md) | Five-axis review before merge; AI-config axis → `punch-ai-governance` | [`punch-review`](../../.github/prompts/punch-review.prompt.md), `punch-code-reviewer` | `.github/skills/punch-code-review-and-quality/SKILL.md` |
| [`punch-git-workflow-and-versioning`](../../.github/skills/punch-git-workflow-and-versioning/SKILL.md) | Atomic commits, short-lived branches, conventional messages | [`punch-ship`](../../.github/prompts/punch-ship.prompt.md), `punch-release-captain` | `.github/skills/punch-git-workflow-and-versioning/SKILL.md` |
| [`punch-documentation-and-adrs`](../../.github/skills/punch-documentation-and-adrs/SKILL.md) | Record decisions (ADRs) + why; keep docs/contracts current | decisions/contract changes; `documentation.instructions.md` | `.github/skills/punch-documentation-and-adrs/SKILL.md` |
| [`punch-security-and-hardening`](../../.github/skills/punch-security-and-hardening/SKILL.md) | Threat-model + harden Punch surfaces (gateway input, Postgres, secrets, supply chain) | Review security axis; `punch-security-auditor` | `.github/skills/punch-security-and-hardening/SKILL.md` |
| [`punch-doubt-driven-development`](../../.github/skills/punch-doubt-driven-development/SKILL.md) | Fresh-context adversarial review of non-trivial/high-stakes decisions | Plan + Build (on-demand) | `.github/skills/punch-doubt-driven-development/SKILL.md` |
| [`punch-source-driven-development`](../../.github/skills/punch-source-driven-development/SKILL.md) | Ground framework code (k6/Docker/Postgres) in official docs + cite | Build (on-demand) | `.github/skills/punch-source-driven-development/SKILL.md` |
| [`punch-performance-optimization`](../../.github/skills/punch-performance-optimization/SKILL.md) | Measure-first k6 perf work; threshold-RED → fix backend bottleneck → re-run → guard | Build/Test (on threshold regression) | `.github/skills/punch-performance-optimization/SKILL.md` |
| [`punch-browser-testing-with-devtools`](../../.github/skills/punch-browser-testing-with-devtools/SKILL.md) | Method for k6 Browser tests via `./bin/punch` (placeholder stays deferred until a Plan task) | Build/Test (k6 Browser task only) | `.github/skills/punch-browser-testing-with-devtools/SKILL.md` |

Phase 3 of the absorption plan (Tier-A +
P3 set) **complete** — every lifecycle skill above absorbed and registered.
**Phase 6 originally folded** `context-engineering`→`punch-context-engineering`
(still folded); `punch-performance-optimization` and `punch-observability-and-instrumentation`
were folded then **promoted back to standalone** lifecycle skills (per owner
direction), and `punch-browser-testing-with-devtools` **adopted** — adapted to
Punch (k6/Docker, no frontend). `punch-observability-and-instrumentation` was
**re-folded and retired** (Spec `spec-agent-skills-adopt-adapt-optimization.md`,
Plan task G-07) — its guidance now lives entirely in `punch-data-harvest`'s
"Observability discipline" section; one canonical owner instead of two
overlapping files. See *Deferred / excluded* below for what stays out.

## Adopted upstream skills (tool axis)

Full provenance — pinned upstream commit, all 24 source skills, the 3 adopted
personas, and the `punch-release-captain` native wrapper, each with an explicit
disposition — lives in
[`agent-skills-provenance.md`](agent-skills-provenance.md). Not restated here.

External skills either **reused as-is** (upstream-maintained, registered for
parity only, **exempt from authored-canon checks**, refresh from upstream —
never hand-edit) or **leaned/adapted for Punch** (authored content, **subject
to the full authored-canon checks**, refresh-from-upstream no longer
applies). Each row states which.

| Skill | What it provides | Reused from | Defined in |
|---|---|---|---|
| [`graphify`](../../.github/skills/graphify/SKILL.md) | Knowledge-graph mapping of any corpus (code, docs, media) into a queryable graph with community detection — explicit-only (`/graphify`), never auto-loaded. **Native upstream skill — adopted, not Punch-authored**; only `user-invocable`/`disable-model-invocation` frontmatter added | upstream [`Graphify-Labs/graphify`](https://github.com/Graphify-Labs/graphify), installed via `uv tool install graphifyy` — pristine snapshot (local staging) [`.ai-upstream/graphify/`](../../.ai-upstream/graphify/UPSTREAM.md) | `.github/skills/graphify/SKILL.md` |
| `caveman` (canonical install, Copilot project-skill location) | Upstream Caveman skill invoked as `/caveman lite\|full\|ultra\|wenyan-*`; default `lite` for VS Code GitHub Copilot Chat prose (rule in `copilot-instructions.md`). Installer drops it at `.agents/skills/caveman/`; Punch relocates it once to `.github/skills/caveman/` (only `user-invocable`/`disable-model-invocation` frontmatter added — no other change) | upstream `caveman` — official installer, relocated | `.github/skills/caveman/SKILL.md` |
| `cavecrew` (canonical install) | Upstream cavecrew sub-agent delegation skill; optional Review/Test/Security coordinators may invoke it to spawn read-only workers with caveman compression. Never invoked by Build. Vendor skill kept as-is, at its installer-default location | upstream `caveman` — official installer | `.agents/skills/cavecrew/SKILL.md` |

`graphify` is explicit-only (`/graphify`), never auto-loaded for unrelated
work; scoped Rule-1 host-tool exception ([ADR 0002](decisions/0002-graphify-host-tool.md)).
**Native upstream skill, adopted as-is** — full upstream `SKILL.md` +
`references/` committed unchanged, only `user-invocable` /
`disable-model-invocation` frontmatter added. Pristine upstream snapshot for
drift comparison stays in `.ai-upstream/graphify/`; the committed skill is
**exempt from authored-canon checks** (refresh from upstream, never hand-edit),
like `.github/skills/caveman/`.
`.github/skills/caveman/` install upstream-maintained (adopted — exempt from
authored-canon checks), same pattern as `graphify`: the upstream installer has
no notion of `.github/skills/`, so it still drops `caveman` at
`.agents/skills/caveman/` — Punch performs one manual relocate step (move +
add the two frontmatter fields) immediately after install; the pinned upstream
body otherwise stays byte-identical. Its default-`lite` voice rule for VS Code
GitHub Copilot Chat lives directly in `copilot-instructions.md` — no separate
Punch presentation-adapter skill.
**`cavecrew` retained** alongside `caveman`, at its installer-default location
`.agents/skills/cavecrew/`: an optional non-Build coordinator
(Review/Test/Security) may invoke it to spawn read-only workers with caveman
compression — Build never does. Other auxiliary upstream packs
(`caveman-compress` with host Python scripts,
`caveman-commit`/`-help`/`-review`/`-stats`) **removed** to keep the install
Copilot-scoped and Docker-First-minimal.

## Why these are still deferred (not created)

| Candidate | Why it does NOT exist as a skill |
|---|---|
| `punch-k6-http` and `punch-k6-browser` | Splitting `punch-k6-testing` again fragments single decision domain (performance semantics). HTTP and Browser live in one skill with sub-sections. |
| `punch-monitoring` / `punch-injectables` | No real monitoring or fault-injection use case yet. Premature. Layer slot reserved in `punch-boundaries.md`. |
| `punch-documentation` | `documentation.instructions.md` path file enough. Skill would only restate it. |
| `punch-(define\|spec\|plan\|build\|verify\|review\|ship)` | **Phases are prompts and agents, not skills** — never create `punch-<phase>` skill. Phase prompt may *activate* lifecycle method skill (e.g. `punch-spec` → `punch-spec-driven-development`); phase stays prompt+agent, method is skill. |
| `context-engineering` (upstream) | **Folded** — transferable method lives in `punch-context-engineering`. (`punch-observability-and-instrumentation` + `punch-performance-optimization` were folded but are now **standalone** — see Lifecycle table.) |
| `ci-cd-and-automation` (upstream) | **Excluded** — CI/CD external to Punch (`punch-architecture.instructions.md`); npm/Prisma/Playwright stack doesn't fit. |
| `frontend-ui-engineering`, `webperf`, `web-performance-auditor` (upstream) | **Excluded** — Punch has no frontend. (`punch-browser-testing-with-devtools` is **adopted**, adapted to k6 Browser — see Lifecycle table.) |
| `interview-me` (upstream) | **Deferred** — overlaps `punch-spec-driven-development`'s absorbed clarify step, which already owns pre-Spec intent extraction. Second "refine" skill would split one decision domain (absorption matrix §A, P3). |
| `shipping-and-launch` (upstream) | **Deferred** — name and deploy/rollback model clash with Punch's deliberately mechanical, human-gated `punch-ship`; go/no-go decision lives in Review phase (`punch-code-review-and-quality`), not a skill. |
| `api-and-interface-design` (upstream) | **Deferred** — Punch's only interface surface is gateway/orders HTTP contract, already governed by `punch-compose-runtime` + `punch-security-and-hardening`. No recurring interface-design decision yet (absorption matrix §A, P3). |
| `deprecation-and-migration` (upstream) | **Deferred** — legacy `bin/*` retirement and Postgres schema moves infrequent, handled by `punch-documentation-and-adrs` + `punch-git-workflow-and-versioning`. Revisit if migration cadence grows (absorption matrix §A, P3). |

## Cap-lifting discipline (domain axis)

Domain cap moved 3 → 6 because new skills each named *unique decision domain*
previously absorbed into another skill at cost of clarity. To add **seventh
domain** skill, propose a Plan that:

1. Names new skill and its decision domain.
2. Lists which of six existing domain skills could not absorb its
   responsibility.
3. Demonstrates real, recurring decision existing skills mishandle.
4. Updates this registry in same PR.

If steps 2–3 cannot be answered concretely, answer is "don't add it".

**Lifecycle skills** governed by absorption plan, not domain cap, but each must
(1) name unique engineering method, (2) not duplicate domain skill or
path-instruction, (3) be registered in Lifecycle-skills table in same PR that
adds it.

The [`punch-ai-governance`](../../.github/skills/punch-ai-governance/SKILL.md)
skill flags any skill on disk without row in either skills table during Review.
