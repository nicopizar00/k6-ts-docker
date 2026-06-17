# Skill Registry

Punch skills sit on **two independent axes**:

- **Domain skills** — one per Punch *subsystem*. Capped at **six**; adding a
  seventh requires killing one.
- **Lifecycle skills** — engineering *methods* adapted from the upstream
  `agent-skills` set. A separate axis, **not** subject to the domain cap;
  admitted in batches by the [absorption plan](agent-skills-absorption-plan.md).

Each entry below explains its responsibility and why it earns a separate skill.
The "Deferred" section lists candidates that were intentionally **not** created.

## Domain skills (six — capped)

| Skill | Owns | Defined in |
|---|---|---|
| [`punch-context`](../../.github/skills/punch-context/SKILL.md) | Pointer-list to canonical docs; the lifecycle; the scope-discipline principle | `.github/skills/punch-context/SKILL.md` |
| [`punch-python-orchestration`](../../.github/skills/punch-python-orchestration/SKILL.md) | The `bin/punch` CLI, subprocess streaming, docker compose invocation, exit codes, evidence artifact | `.github/skills/punch-python-orchestration/SKILL.md` |
| [`punch-docker-compose`](../../.github/skills/punch-docker-compose/SKILL.md) | Service contracts, stable service names, healthchecks, multi-stage Dockerfiles, image pins | `.github/skills/punch-docker-compose/SKILL.md` |
| [`punch-k6-performance`](../../.github/skills/punch-k6-performance/SKILL.md) | k6 test shape (HTTP + Browser), thresholds, `handleSummary`, shared report builder, k6 image pin, Browser deferral | `.github/skills/punch-k6-performance/SKILL.md` |
| [`punch-data-harvest`](../../.github/skills/punch-data-harvest/SKILL.md) | Artifact paths and schemas, terminal-vs-file noise discipline, JSON/CSV contracts, HTML report builder | `.github/skills/punch-data-harvest/SKILL.md` |
| [`punch-governance-review`](../../.github/skills/punch-governance-review/SKILL.md) | Frontmatter contracts, registry consistency, boundary compliance, scope discipline, handoff hygiene | `.github/skills/punch-governance-review/SKILL.md` |

### Why six, and what each adds

Each domain skill names a unique **decision domain**:

| Skill | Decision domain |
|---|---|
| `punch-context` | "What primer does any agent need?" |
| `punch-python-orchestration` | "How does the run happen?" |
| `punch-docker-compose` | "What is the runtime contract?" |
| `punch-k6-performance` | "What does fast enough mean?" |
| `punch-data-harvest` | "What artifacts does the run produce?" |
| `punch-governance-review` | "Is the AI operating model itself healthy?" |

These domains have different reviewers, different failure modes, and
different cadences. Splitting them keeps each concern isolated.

### Why the cap moved from 3 to 6

The previous registry capped skills at three (`punch-orchestration`,
`punch-performance-k6`, `punch-ai-governance-audit`). The redesign
deliberately lifted that cap to admit three previously-deferred decision
domains:

| New skill | What it admits |
|---|---|
| `punch-context` | A common entry point so each Build prompt does not duplicate the "load this primer first" instruction. |
| `punch-docker-compose` | Compose contracts (service names, healthchecks, image pins) were previously implied in the path-instruction file but had no skill to activate during Build. The contract template makes the cost of Compose changes visible at Plan time. |
| `punch-data-harvest` | Artifacts were previously owned half by `punch-orchestration` (state files) and half by `punch-performance-k6` (HTML/JSON). Centralizing the artifact *contract* in one skill keeps downstream consumers (CI, future automation) coherent. |

The skill renames (`orchestration` → `python-orchestration`,
`performance-k6` → `k6-performance`, `ai-governance-audit` →
`governance-review`) align names with the spec and broaden the
governance skill's remit from "cap enforcement" to "boundary discipline
+ handoff hygiene".

## Lifecycle skills (method axis — not capped)

Lifecycle skills encode reusable engineering *methods* adapted from the upstream
`agent-skills` set. A phase prompt activates **one lifecycle skill** (the method)
plus the relevant **domain skill** (the Punch specifics) — this is how
skill-first execution coexists with Punch's phase/scope governance. Punch's
path-instructions always win on stack specifics; the lifecycle skill supplies the
method, not the stack rules.

| Lifecycle skill | Method | Activated by | Defined in |
|---|---|---|---|
| [`idea-refine`](../../.github/skills/idea-refine/SKILL.md) | Refine a raw idea before Spec (divergent → convergent) | invoked within Spec (no standalone prompt) | `.github/skills/idea-refine/SKILL.md` |
| [`spec-driven-development`](../../.github/skills/spec-driven-development/SKILL.md) | Spec before code — surface assumptions, reframe as success criteria | [`punch-spec`](../../.github/prompts/punch-spec.prompt.md) | `.github/skills/spec-driven-development/SKILL.md` |
| [`planning-and-task-breakdown`](../../.github/skills/planning-and-task-breakdown/SKILL.md) | Decompose a spec into scoped, verifiable tasks | [`punch-plan`](../../.github/prompts/punch-plan.prompt.md) | `.github/skills/planning-and-task-breakdown/SKILL.md` |
| [`incremental-implementation`](../../.github/skills/incremental-implementation/SKILL.md) | Thin vertical slices; Build edits, Verify runs, Ship commits | the 5 `punch-build-*` prompts + builder agents | `.github/skills/incremental-implementation/SKILL.md` |
| [`test-driven-development`](../../.github/skills/test-driven-development/SKILL.md) | RED→GREEN via k6 checks/thresholds + `punch-run.json`; Prove-It for bugs | [`punch-test`](../../.github/prompts/punch-test.prompt.md), `punch-build-k6-*` | `.github/skills/test-driven-development/SKILL.md` |

More lifecycle skills (`debugging-and-error-recovery`, `code-review-and-quality`,
`code-simplification`, `git-workflow-and-versioning`, `documentation-and-adrs`,
`security-and-hardening`, …) are admitted in
[`agent-skills-absorption-plan.md`](agent-skills-absorption-plan.md) Phase 3 and
registered in this table in the same PR that adds each one.

## Why these are still deferred (not created)

| Candidate | Why it does NOT exist as a skill |
|---|---|
| `punch-k6-http` and `punch-k6-browser` | Splitting `punch-k6-performance` again would fragment a single decision domain (performance semantics). HTTP and Browser live in one skill with sub-sections. |
| `punch-monitoring` / `punch-injectables` | No real monitoring or fault-injection use case yet. Premature. The layer slot is reserved in `punch-boundaries.md`. |
| `punch-documentation` | The `documentation.instructions.md` path file is enough. A skill would only restate it. |
| `punch-(define\|spec\|plan\|build\|verify\|review\|ship)` | **Phases are prompts and agents, not skills** — we never create a `punch-<phase>` skill. A phase prompt may *activate* a lifecycle method skill (e.g. `punch-spec` → `spec-driven-development`); the phase stays a prompt+agent, the method is the skill. |

## Cap-lifting discipline (domain axis)

The domain cap moved from 3 to 6 because the new skills each named a *unique
decision domain* that was previously absorbed into another skill at the cost of
clarity. To add a **seventh domain** skill, propose a Plan that:

1. Names the new skill and its decision domain.
2. Lists which of the six existing domain skills could not absorb its
   responsibility.
3. Demonstrates a real, recurring decision the existing skills mishandle.
4. Updates this registry in the same PR.

If steps 2–3 cannot be answered concretely, the answer is "don't add it".

**Lifecycle skills** are governed by the absorption plan, not the domain cap, but
each must (1) name a unique engineering method, (2) not duplicate a domain skill
or a path-instruction, and (3) be registered in the Lifecycle-skills table in the
same PR that adds it.

The [`punch-governance-review`](../../.github/skills/punch-governance-review/SKILL.md)
skill flags any skill on disk without a row in either skills table during Review.
