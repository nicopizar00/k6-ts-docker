# Skill Registry

Punch skills sit on **two independent axes**:

- **Domain skills** — one per Punch *subsystem*. Capped at **six**; seventh
  needs killing one.
- **Lifecycle skills** — engineering *methods* adapted from upstream
  `agent-skills` set. Separate axis, **not** under domain cap; admitted in
  batches by [absorption plan](history/agent-skills-absorption-plan.md).

Each entry below: responsibility + why earns separate skill. "Deferred"
section lists candidates intentionally **not** created.

## Skill discovery — which skill when

Load skill matching task: **domain skill** for subsystem, **lifecycle skill**
for method. Multiple apply (k6 change uses `punch-k6-testing` +
`incremental-implementation` + `test-driven-development`).

| You are… | Skill(s) |
|---|---|
| new to the repo | `punch-context-engineering` |
| routing a repo-understanding / cross-file / architecture / governance task (before picking the sub-agent) | `punch-context-engineering` (the Graphify gate) |
| refining a vague idea | `idea-refine` |
| writing a spec | `spec-driven-development` |
| breaking a spec into tasks | `planning-and-task-breakdown` |
| editing the orchestrator | `punch-python-orchestration` + `incremental-implementation` |
| editing compose / Dockerfiles | `punch-compose-runtime` + `incremental-implementation` |
| writing / changing a k6 test | `punch-k6-testing` + `test-driven-development` + `incremental-implementation` |
| changing an artifact / report | `punch-data-harvest` + `incremental-implementation` |
| a run failed | `debugging-and-error-recovery` |
| proving a fix RED→GREEN | `test-driven-development` |
| reviewing a diff | `code-review-and-quality` (+ `code-simplification`, `security-and-hardening`) |
| committing / shipping | `git-workflow-and-versioning` |
| recording a decision (ADR) | `documentation-and-adrs` |
| a high-stakes / irreversible decision | `doubt-driven-development` |
| coding against a k6/Docker/Postgres API | `source-driven-development` |
| a gate/journey threshold regressed | `performance-optimization` (+ `punch-k6-testing`) |
| instrumenting a service (logs/events) | `observability-and-instrumentation` (+ `punch-data-harvest`) |
| writing a k6 Browser test (Plan task) | `browser-testing-with-devtools` (+ `punch-k6-testing`) |
| auditing AI config | `punch-ai-governance` |

## Domain skills (six — capped)

| Skill | Owns | Defined in |
|---|---|---|
| [`punch-context-engineering`](../../.github/skills/punch-context-engineering/SKILL.md) | Pointer-list to canonical docs; lifecycle; scope-discipline principle; Graphify gate | `.github/skills/punch-context-engineering/SKILL.md` |
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
| [`idea-refine`](../../.github/skills/idea-refine/SKILL.md) | Refine raw idea before Spec (divergent → convergent) | invoked within Spec (no standalone prompt) | `.github/skills/idea-refine/SKILL.md` |
| [`spec-driven-development`](../../.github/skills/spec-driven-development/SKILL.md) | Spec before code — surface assumptions, reframe as success criteria | [`punch-spec`](../../.github/prompts/punch-spec.prompt.md) | `.github/skills/spec-driven-development/SKILL.md` |
| [`planning-and-task-breakdown`](../../.github/skills/planning-and-task-breakdown/SKILL.md) | Decompose spec into scoped, verifiable tasks | [`punch-plan`](../../.github/prompts/punch-plan.prompt.md) | `.github/skills/planning-and-task-breakdown/SKILL.md` |
| [`incremental-implementation`](../../.github/skills/incremental-implementation/SKILL.md) | Thin vertical slices; Build edits, Test runs, Ship commits | [`punch-build`](../../.github/prompts/punch-build.prompt.md) + builder agents | `.github/skills/incremental-implementation/SKILL.md` |
| [`test-driven-development`](../../.github/skills/test-driven-development/SKILL.md) | RED→GREEN via k6 checks/thresholds + `punch-run.json`; Prove-It for bugs | [`punch-test`](../../.github/prompts/punch-test.prompt.md), `punch-build` (via `punch-performance-test-engineer`) | `.github/skills/test-driven-development/SKILL.md` |
| [`punch-debugging-and-error-recovery`](../../.github/skills/punch-debugging-and-error-recovery/SKILL.md) | Root-cause triage: reproduce → localize → fix → guard | [`punch-test`](../../.github/prompts/punch-test.prompt.md), `punch-test-engineer` | `.github/skills/punch-debugging-and-error-recovery/SKILL.md` |
| [`code-review-and-quality`](../../.github/skills/code-review-and-quality/SKILL.md) | Five-axis review before merge; AI-config axis → `punch-ai-governance` | [`punch-review`](../../.github/prompts/punch-review.prompt.md), `punch-code-reviewer` | `.github/skills/code-review-and-quality/SKILL.md` |
| [`code-simplification`](../../.github/skills/code-simplification/SKILL.md) | Reduce complexity without changing behavior (Chesterton's Fence) | Review simplicity axis + Build Rule 0 | `.github/skills/code-simplification/SKILL.md` |
| [`git-workflow-and-versioning`](../../.github/skills/git-workflow-and-versioning/SKILL.md) | Atomic commits, short-lived branches, conventional messages | [`punch-ship`](../../.github/prompts/punch-ship.prompt.md), `punch-release-captain` | `.github/skills/git-workflow-and-versioning/SKILL.md` |
| [`documentation-and-adrs`](../../.github/skills/documentation-and-adrs/SKILL.md) | Record decisions (ADRs) + why; keep docs/contracts current | decisions/contract changes; `documentation.instructions.md` | `.github/skills/documentation-and-adrs/SKILL.md` |
| [`security-and-hardening`](../../.github/skills/security-and-hardening/SKILL.md) | Threat-model + harden Punch surfaces (gateway input, Postgres, secrets, supply chain) | Review security axis; `punch-security-auditor` | `.github/skills/security-and-hardening/SKILL.md` |
| [`doubt-driven-development`](../../.github/skills/doubt-driven-development/SKILL.md) | Fresh-context adversarial review of non-trivial/high-stakes decisions | Plan + Build (on-demand) | `.github/skills/doubt-driven-development/SKILL.md` |
| [`source-driven-development`](../../.github/skills/source-driven-development/SKILL.md) | Ground framework code (k6/Docker/Postgres) in official docs + cite | Build (on-demand) | `.github/skills/source-driven-development/SKILL.md` |
| [`performance-optimization`](../../.github/skills/performance-optimization/SKILL.md) | Measure-first k6 perf work; threshold-RED → fix backend bottleneck → re-run → guard | Build/Test (on threshold regression) | `.github/skills/performance-optimization/SKILL.md` |
| [`observability-and-instrumentation`](../../.github/skills/observability-and-instrumentation/SKILL.md) | Structured service logs + RED read from k6 run; feeds `reports/logs/**` (pairs with `punch-data-harvest`) | Build (adding service/route/query) | `.github/skills/observability-and-instrumentation/SKILL.md` |
| [`browser-testing-with-devtools`](../../.github/skills/browser-testing-with-devtools/SKILL.md) | Method for k6 Browser tests via `./bin/punch` (placeholder stays deferred until a Plan task) | Build/Test (k6 Browser task only) | `.github/skills/browser-testing-with-devtools/SKILL.md` |
| [`punch-using-agent-skills`](../../.github/skills/punch-using-agent-skills/SKILL.md) | The *agents* canon: how a coordinator delegates to engineers + bounded `cavecrew-*` workers (depth-1, tool-subset, lazy nesting) | [`punch-build`](../../.github/prompts/punch-build.prompt.md), `punch-builder` | `.github/skills/punch-using-agent-skills/SKILL.md` |

Phase 3 of [absorption plan](history/agent-skills-absorption-plan.md) (Tier-A +
P3 set) **complete** — every lifecycle skill above absorbed and registered.
**Phase 6 originally folded** `context-engineering`→`punch-context-engineering`
(still folded); `performance-optimization` and `observability-and-instrumentation`
were folded then **promoted back to standalone** lifecycle skills (per owner
direction) and `browser-testing-with-devtools` **adopted** — all three adapted to
Punch (k6/Docker, no frontend). See *Deferred / excluded* below for what stays out.

## Adopted upstream skills (tool axis)

External skills reused **as-is** — neither Punch domain nor Punch method.
Registered here for parity only; content upstream-maintained, **exempt from
authored-canon checks** (frontmatter completeness, naming, duplication,
cross-reference) — refresh from upstream, never hand-edit.

| Skill | What it provides | Reused from | Defined in |
|---|---|---|---|
| [`graphify`](../../.github/skills/graphify/SKILL.md) | Knowledge-graph mapping of repo for Context Engineering orientation; runs in IDE session (no API key). **Punch-leaned adaptation** — trimmed to in-IDE build/update/query subset (no remote-clone/merge, media transcription, external-DB push, MCP/wiki/obsidian exports) | upstream `graphifyy`, leaned for Punch — pristine snapshot (local staging) [`.ai-upstream/graphify/`](../../.ai-upstream/graphify/UPSTREAM.md) | `.github/skills/graphify/SKILL.md` |
| `caveman` (canonical install) | Upstream Caveman skill invoked as `/caveman lite\|full\|ultra\|wenyan-*`; loaded by VS Code GitHub Copilot. Installed via official installer (`--only copilot`), trimmed to the core skill | upstream `caveman` — official installer | `.agents/skills/caveman/SKILL.md` |
| `cavecrew` (canonical install) | Upstream cavecrew sub-agent delegation skill; invoked by the Build engineers to spawn workers with caveman compression. Vendor skill kept as-is | upstream `caveman` — official installer | `.agents/skills/cavecrew/SKILL.md` |
| [`punch-build-caveman`](../../.github/skills/punch-build-caveman/SKILL.md) | **Canonical Caveman policy (single source).** Repo default `lite`; per-phase voice — Spec/Document `lite`, Plan/Review/Ship `full`, Build/Test `ultra`. Builder→engineer `wenyan-lite`; the two engineers→cavecrew `wenyan-full`; any other sub-agent nesting→cavecrew `wenyan-ultra`; cavecrew reports non-guarded (lazy). Wenyan avoided in committed docs. Prompts/agents/copilot-instructions link here; never compresses evidence | upstream `caveman` — provenance (local staging) [`.ai-upstream/caveman/`](../../.ai-upstream/caveman/UPSTREAM.md) | `.github/skills/punch-build-caveman/SKILL.md` |

`graphify` gated through [`punch-context-engineering`](../../.github/skills/punch-context-engineering/SKILL.md)
Graphify gate; scoped Rule-1 host-tool exception ([ADR 0002](decisions/0002-graphify-host-tool.md)).
**Punch-leaned adaptation** of upstream `graphifyy`, trimmed to in-IDE
build/update/query subset for Copilot-plug-in-ready footprint (removed:
remote-clone/cross-repo merge, media transcription, Neo4j/FalkorDB push, MCP server,
wiki/SVG/GraphML/obsidian exports). Pristine upstream stays in
`.ai-upstream/graphify/`; leaned skill **authored — subject to governance
checks** (no longer refresh-verbatim).
Canonical `.agents/skills/caveman/` install upstream-maintained (adopted —
exempt from authored-canon checks). **`cavecrew` retained** alongside `caveman`:
the Build engineers invoke it to spawn workers with caveman compression. Other
auxiliary upstream packs (`caveman-compress` with host Python scripts,
`caveman-commit`/`-help`/`-review`/`-stats`) **removed** to keep the install
Copilot-scoped and Docker-First-minimal.

### `punch-build-caveman` — governance metadata

| Field | Value |
|---|---|
| Classification | `punch-build-caveman` = **authored Punch adapter** (checked); `.agents/skills/caveman` = **adopted upstream** (exempt) |
| Status | **repo default `lite`** · per-phase voice · never compresses evidence · Wenyan forbidden in persistent artifacts |
| Scope | Per-phase voice: Spec/Document `lite`, Plan/Review/Ship `full`, Build/Test `ultra`. Delegation: Builder→humans `ultra`, Builder→engineer `wenyan-lite`, the two engineers→cavecrew `wenyan-full`, any other nesting→cavecrew `wenyan-ultra`; cavecrew reports non-guarded (lazy). All sub-agent reports keep evidence verbatim. Caveman is output style only |
| Role | communication / token-efficiency utility — **not core runtime behavior, not required for Punch execution** |
| Default mode | repo **`lite`**; per-phase overrides (Plan/Review/Ship `full`, Build/Test `ultra`); delegation tiers `wenyan-lite` / `wenyan-full` / `wenyan-ultra` (allowed: `lite` / `full` / `ultra` / `wenyan-lite` / `wenyan-full` / `wenyan-ultra`; `stop caveman` reverts) |
| Governed by | `punch-ai-governance` (refresh + drift) |
| Decision | live policy = this skill + the Build chain (`punch-build` → `punch-builder` → engineer → cavecrew); no standalone ADR |
| Provenance | upstream repo https://github.com/JuliusBrussee/caveman · required-asset manifest [`.github/.ai-upstream/README.md`](../../.github/.ai-upstream/README.md) |
| Install method | **manual, Copilot-scoped** (see manifest): `npx -y skills add JuliusBrussee/caveman --skill caveman\|cavecrew --agent github-copilot --yes`. Do **not** run `install.sh --with-init` (appends always-on rules + parallel rule files) |
| Files changed by installer | added `.agents/skills/caveman/` + `.agents/skills/cavecrew/` (both kept); appended to `.github/copilot-instructions.md` + `AGENTS.md` (both reconciled by hand); created `.cursor`/`.windsurf`/`.clinerules`/`.opencode` + other skill packs + `skills-lock.json` (all **removed**) |
| Copilot instruction file edited manually | yes — two duplicated caveman blocks merged into one canonical Copilot-scoped section *below* Critical Rules (no Critical Rule altered) |

`punch-build-caveman` **adapter** Punch-authored, therefore **subject** to
frontmatter / naming / duplication checks. Upstream `.agents/skills/caveman/`
install and pristine `.ai-upstream/caveman/` snapshot upstream-maintained,
**exempt** from those checks (refresh from upstream, never hand-edit).

## Why these are still deferred (not created)

| Candidate | Why it does NOT exist as a skill |
|---|---|
| `punch-k6-http` and `punch-k6-browser` | Splitting `punch-k6-testing` again fragments single decision domain (performance semantics). HTTP and Browser live in one skill with sub-sections. |
| `punch-monitoring` / `punch-injectables` | No real monitoring or fault-injection use case yet. Premature. Layer slot reserved in `punch-boundaries.md`. |
| `punch-documentation` | `documentation.instructions.md` path file enough. Skill would only restate it. |
| `punch-(define\|spec\|plan\|build\|verify\|review\|ship)` | **Phases are prompts and agents, not skills** — never create `punch-<phase>` skill. Phase prompt may *activate* lifecycle method skill (e.g. `punch-spec` → `spec-driven-development`); phase stays prompt+agent, method is skill. |
| `context-engineering` (upstream) | **Folded** — transferable method lives in `punch-context-engineering`. (`observability-and-instrumentation` + `performance-optimization` were folded but are now **standalone** — see Lifecycle table.) |
| `ci-cd-and-automation` (upstream) | **Excluded** — CI/CD external to Punch (`punch-architecture.instructions.md`); npm/Prisma/Playwright stack doesn't fit. |
| `frontend-ui-engineering`, `webperf`, `web-performance-auditor` (upstream) | **Excluded** — Punch has no frontend. (`browser-testing-with-devtools` is **adopted**, adapted to k6 Browser — see Lifecycle table.) |
| `interview-me` (upstream) | **Deferred** — overlaps `idea-refine`, which already owns pre-Spec intent extraction. Second "refine" skill would split one decision domain (absorption matrix §A, P3). |
| `shipping-and-launch` (upstream) | **Deferred** — name and deploy/rollback model clash with Punch's deliberately mechanical, human-gated `punch-ship`; go/no-go decision lives in Review phase (`code-review-and-quality`), not a skill. |
| `api-and-interface-design` (upstream) | **Deferred** — Punch's only interface surface is gateway/orders HTTP contract, already governed by `punch-compose-runtime` + `security-and-hardening`. No recurring interface-design decision yet (absorption matrix §A, P3). |
| `deprecation-and-migration` (upstream) | **Deferred** — legacy `bin/*` retirement and Postgres schema moves infrequent, handled by `documentation-and-adrs` + `git-workflow-and-versioning`. Revisit if migration cadence grows (absorption matrix §A, P3). |

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
