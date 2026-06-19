# Skill Absorption Matrix

> **Reconciled 2026-06-17 (post-restructure).** Several P1 rows now done:
> `idea-refine` registered; `punch-refine` **deleted** (not "fix frontmatter");
> `punch-define` deleted; `punch-builder-scoped` replaced by 5 builder agents.
> Prompt frontmatter is **`agent:`**, not `mode:`. Canonical record:
> [`agent-skills-absorption-plan.md` § Execution status](agent-skills-absorption-plan.md).
> Tier-A/B/C skill rows below still pending (Phase 3).

> **Status:** Review artifact (no runtime AI config changed). Made
> 2026-06-16 on branch `feat/agent-skills`. Decisions here =
> **recommendations for later planned migration**, grounded in files
> inspected this pass. See companions in this folder.

**Legend — Action:** `keep` (no change) · `copy` (verbatim into runtime) ·
`adapt` (rewrite examples/scope for Punch) · `merge` (fold into existing
asset) · `rewrite` (new Punch asset informed by upstream) ·
`deprecate` (retire after replacement lands) · `delete` · `exclude` (don't
absorb).
**Priority:** P1 (foundation/unblock) · P2 (core lifecycle value) ·
P3 (selective/nice-to-have).
**Canonical skill home below = `.github/skills/`** (decided 2026-06-16 — no
migration; see [target architecture](recommended-target-ai-architecture.md)).

## A. Upstream lifecycle skills → Punch methodology skills

| Source | Type | Origin | Current purpose | Recommended destination | Action | Reason | Risk | Pri |
|---|---|---|---|---|---|---|---|:--:|
| `skills/spec-driven-development` | skill | upstream | Spec before code (6-area spec) | `.github/skills/spec-driven-development` | **adapt** | Spec-phase core; strip "web app"/`npm` defaults; point at `punch-spec` outputs | Med — examples assume web stack | P2 |
| `skills/planning-and-task-breakdown` | skill | upstream | Decompose into verifiable tasks | `.github/skills/planning-and-task-breakdown` | **adapt** | Plan-phase core; map to allowed/read-only/forbidden + `tasks/plan.md` | Med — must not soften scope rules | P2 |
| `skills/incremental-implementation` | skill | upstream | Thin vertical slices, test each | `.github/skills/incremental-implementation` | **adapt** | Build-phase core; bind to scoped allow-list | Low | P2 |
| `skills/test-driven-development` | skill | upstream | Failing test → pass; Prove-It | `.github/skills/test-driven-development` | **adapt** | Verify/Build; reframe "test" as k6 checks/thresholds + `punch-run.json` | **High** — jest/vitest ≠ Punch evidence model | P2 |
| `skills/debugging-and-error-recovery` | skill | upstream | Reproduce→localize→fix→guard | `.github/skills/debugging-and-error-recovery` | **adapt** | Verify failure handling; align with failure classification in `punch-verify` | Low | P2 |
| `skills/code-review-and-quality` | skill | upstream | Five-axis review | `.github/skills/code-review-and-quality` | **adapt** | Review-phase core; defer AI-config axis to `punch-governance-review` | Med — overlap with governance skill | P2 |
| `skills/code-simplification` | skill | upstream | Simplify w/o behavior change | `.github/skills/code-simplification` | **adapt** | Matches Punch "no premature abstraction"; back new `punch-simplify` prompt | Low | P2 |
| `skills/documentation-and-adrs` | skill | upstream | Record decisions/ADRs | `.github/skills/documentation-and-adrs` | **adapt** | Docs phase; ADRs under `docs/`; respect `documentation.instructions.md` | Low | P3 |
| `skills/git-workflow-and-versioning` | skill | upstream | Atomic commits, clean history | `.github/skills/git-workflow-and-versioning` | **adapt** | Ship phase; align with "mechanical only / humans merge / no `--no-verify`" | Med — must keep human-merge gate | P2 |
| `skills/security-and-hardening` | skill | upstream | Harden against vulns | `.github/skills/security-and-hardening` | **adapt** | Real surfaces (gateway/orders/Postgres/env); drop web-auth-heavy parts | Med — large file, web-leaning | P3 |
| `skills/shipping-and-launch` | skill | upstream | Pre-launch checklist, rollback | `.github/skills/` (Review-readiness) | **adapt** | Map to Punch **Review** go/no-go; deploy/rollback mostly N/A (CI external) | **High** — name clashes with Punch Ship | P3 |
| `skills/idea-refine` | skill | upstream **and** Punch (verbatim copy) | Refine vague ideas | `.github/skills/idea-refine` | **keep + register** | Already absorbed; just **fix drift** (registry row, add `applies-to`, drop `/mnt/...` path) | Low | **P1** |
| `skills/interview-me` | skill | upstream | Extract true intent (1 Q at a time) | `.github/skills/interview-me` | **adapt** | Define-phase support; reconcile with `idea-refine` to avoid two "refine" skills | Med — overlap | P3 |
| `skills/doubt-driven-development` | skill | upstream | Adversarial fresh-context review | `.github/skills/doubt-driven-development` | **adapt** | Aligns with Punch "stop and ask" on high-stakes/irreversible changes | Low | P3 |
| `skills/source-driven-development` | skill | upstream | Ground code in official docs | `.github/skills/source-driven-development` | **adapt** | Useful for k6/Docker/Postgres correctness | Low | P3 |
| `skills/api-and-interface-design` | skill | upstream | Stable interface contracts | `.github/skills/api-and-interface-design` | **adapt** | Punch services expose HTTP; selective use | Low | P3 |
| `skills/deprecation-and-migration` | skill | upstream | Retire/migrate safely | `.github/skills/deprecation-and-migration` | **adapt** | Legacy `bin/*` retirement; Postgres schema moves | Low | P3 |

## B. Upstream skills that overlap a Punch domain skill → fold, don't duplicate

| Source | Type | Origin | Current purpose | Recommended destination | Action | Reason | Risk | Pri |
|---|---|---|---|---|---|---|---|:--:|
| `skills/context-engineering` | skill | upstream | Right context at right time | `punch-context` skill | **merge** | `punch-context` already owns "primer/what to load"; fold method, don't add 2nd skill | Med — cap discipline | P3 |
| `skills/observability-and-instrumentation` | skill | upstream | Logs/metrics/traces/alerts | `punch-data-harvest` skill | **merge** | `punch-data-harvest` owns log noise + evidence; fold RED-metric ideas | Med | P3 |
| `skills/performance-optimization` | skill | upstream | Measure→fix→verify (CWV/React) | `punch-k6-performance` skill | **merge (partial) / exclude (web)** | Keep measure-first loop + N+1/backend; drop Core Web Vitals/React | Med — mostly web | P3 |
| `skills/using-agent-skills` | meta-skill | upstream | Task→skill discovery flowchart | `.github/skills/` index + `punch-context` | **rewrite** | Build Punch skill index spanning domain + lifecycle skills; don't duplicate lifecycle table | Med | P2 |

## C. Upstream skills to EXCLUDE from Punch core

| Source | Type | Origin | Current purpose | Recommended destination | Action | Reason | Risk | Pri |
|---|---|---|---|---|---|---|---|:--:|
| `skills/ci-cd-and-automation` | skill | upstream | Author CI/CD pipelines | — (leave in `.ai-upstream/`) | **exclude** | **Conflicts** "CI/CD is external to Punch" (`punch-architecture.instructions.md:36`); npm/Prisma/Playwright stack | High if absorbed | P3 |
| `skills/frontend-ui-engineering` | skill | upstream | Build production UIs | — | **exclude** | No frontend in Punch | Low | — |
| `skills/browser-testing-with-devtools` | skill | upstream | Chrome DevTools MCP testing | — (revisit if k6-browser revived) | **exclude/defer** | Distinct from deferred k6-browser; needs MCP | Low | — |

## D. Upstream agents → Copilot custom agents (`.github/agents/*.agent.md`)

| Source | Type | Origin | Current purpose | Recommended destination | Action | Reason | Risk | Pri |
|---|---|---|---|---|---|---|---|:--:|
| `agents/security-auditor.md` | persona | upstream | Vulnerability/threat audit | `.github/agents/security-auditor.agent.md` | **adapt** | New persona Punch lacks; rename to `.agent.md`; scope to Punch surfaces | Med — keep scope realistic | P3 |
| `agents/code-reviewer.md` | persona | upstream | Five-axis review | `punch-reviewer.agent.md` (augment) | **merge** | Don't duplicate review persona; fold 5-axis framing into existing reviewer / review skill | Med — persona cap | P3 |
| `agents/test-engineer.md` | persona | upstream | Test strategy/coverage | — | **exclude** | Overlaps `punch-verifier`; Punch has no unit suite; keep "Prove-It" in TDD skill | Low | — |
| `agents/web-performance-auditor.md` | persona | upstream | Core Web Vitals audit | — | **exclude** | Frontend/CWV only | Low | — |

## E. Upstream commands → Copilot prompt files (`.github/prompts/*.prompt.md`)

| Source | Type | Origin | Current purpose | Recommended destination | Action | Reason | Risk | Pri |
|---|---|---|---|---|---|---|---|:--:|
| `commands/spec.md` | command | upstream | `/spec` → spec skill | `punch-spec.prompt.md` | **merge** | Slim existing prompt to delegate to `spec-driven-development` | Low | P2 |
| `commands/plan.md` | command | upstream | `/plan` → planning skill | `punch-plan.prompt.md` | **merge** | Slim to delegate to `planning-and-task-breakdown` | Low | P2 |
| `commands/build.md` | command | upstream | `/build` → impl + TDD | `punch-build-*.prompt.md` | **merge** | Delegate to skills; **drop `/build auto`** (conflicts one-task/human-approve) | Med | P2 |
| `commands/review.md` | command | upstream | `/review` → review skill | `punch-review.prompt.md` | **merge** | Slim to delegate to `code-review-and-quality` | Low | P2 |
| `commands/code-simplify.md` | command | upstream | `/code-simplify` | `punch-simplify.prompt.md` (new) | **rewrite** | No Punch equivalent; thin new prompt + registry row | Low | P3 |
| `commands/test.md` | command | upstream | `/test` → TDD | — | **merge** | Fold into Build/Verify; no separate prompt (avoid prompt sprawl) | Low | P3 |
| `commands/ship.md` | command | upstream | `/ship` parallel review fan-out | `punch-review.prompt.md` (optional) | **adapt** | Fan-out belongs to **Review**, not Punch Ship; keep `punch-ship` mechanical | **High** — semantic clash | P3 |
| `commands/webperf.md` | command | upstream | `/webperf` | — | **exclude** | Frontend | — | — |

## F. Upstream docs / references / scripts

| Source | Type | Origin | Current purpose | Recommended destination | Action | Reason | Risk | Pri |
|---|---|---|---|---|---|---|---|:--:|
| `docs/copilot-setup.md` | doc | upstream | Copilot wiring guide | `docs/ai/copilot-adaptation-plan.md` (distilled) | **merge** | Source of `.agent.md` + skills-dir facts; don't copy wholesale | Low | P2 |
| `docs/skill-anatomy.md` | doc | upstream | SKILL.md format spec | `docs/ai/` (reference) | **adapt** | Reconcile with Punch frontmatter contract (`applies-to`) | Low | P3 |
| `docs/agents.md` / `docs/getting-started.md` | doc | upstream | Persona matrix / setup | leave in `.ai-upstream/` | **keep** | Provenance; cite, don't duplicate | Low | — |
| `references/testing-patterns.md` | ref | upstream | Test patterns | beside adapted TDD skill | **adapt** | Supports TDD skill if absorbed | Low | P3 |
| `references/security-checklist.md` | ref | upstream | Security checklist | beside adapted security skill | **adapt** | Supports `security-and-hardening` | Low | P3 |
| `references/performance-checklist.md` | ref | upstream | Perf checklist (web-leaning) | salvage non-web parts | **adapt** | Partial value for k6 perf | Low | P3 |
| `references/accessibility-checklist.md` | ref | upstream | a11y checklist | — | **exclude** | Frontend only | — | — |
| `references/orchestration-patterns.md` | ref | upstream | Multi-agent patterns (Claude) | `docs/ai/` (reference) | **keep** | Informs agent composition; Copilot-adapt fan-out claims | Med | P3 |
| `scripts/validate-skills.js` | script | upstream | Validate skill frontmatter (Node) | `punch-governance-review` or stdlib Python | **rewrite** | **Conflicts** "no host Node"; reimplement or fold into governance audit | Med | P3 |

## G. Punch existing assets requiring action (drift / reconciliation)

| Source | Type | Origin | Current purpose | Recommended destination | Action | Reason | Risk | Pri |
|---|---|---|---|---|---|---|---|:--:|
| `.github/skills/idea-refine` | skill | Punch (verbatim upstream) | Idea refinement | register in `skill-registry.md`; add `applies-to`; drop `/mnt/...` | **keep + adapt** | Resolve existing governance drift before adding more | Low | **P1** |
| `.github/prompts/punch-refine.prompt.md` | prompt | Punch | Wrapped idea-refine | **deleted** — idea-refine now runs inside `punch-spec` | **delete** ✅ | Superseded by command-mapped prompts | Low | **P1 done** |
| `docs/ai/skill-registry.md` | governance | Punch | 6-skill register + cap | reframe cap: "domain skills (6) + lifecycle skills (N)" | **rewrite** | Cap currently blocks lifecycle absorption (see conflict report) | **High** — central governance change | **P1** |
| `docs/ai/operating-model.md` | governance | Punch | Lifecycle + asset taxonomy | add "lifecycle/methodology skill" as sanctioned skill kind | **adapt** | Resolves "phases are not skills" vs skill-first | High | **P1** |
| `.github/prompts/punch-spec|plan|review` (+ build) | prompt | Punch | Phase entry (heavy, 57–94 ln) | slim to thin wrappers that activate skills | **adapt** | Move procedure into skills (skill-first) | Med | P2 |
| `AGENTS.md` | contract | Punch | Cross-agent guide (123 ln) | slim to pointer + `.github/skills/` note | **adapt** | De-duplicate vs `copilot-instructions`/`operating-model` | Med | P2 |
| `CLAUDE.md` | constitution | Punch | Architectural constitution (170 ln) | keep as constitution; add minimal skill-discovery pointer | **keep** | Preserve canonical role; don't gut it | Low | P2 |
| `.github/skills/*` (6 domain) | skill | Punch | Domain decision ownership | stay in `.github/skills/` | **keep** | Decided 2026-06-16: no migration; lifecycle skills join them here | Low | P2 |

> Three **P1 governance rows in section G = unblockers**: until
> skill taxonomy/cap reframed and existing `idea-refine` drift fixed,
> absorbing more skills only multiplies drift. See
> [implementation order](recommended-target-ai-architecture.md#implementation-order).
