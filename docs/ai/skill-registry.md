# Skill Registry

Punch supports **six** skills. Each entry below explains its
responsibility and why it earns a separate skill. The "Deferred" section
lists candidates that were intentionally **not** created.

## Active skills

| Skill | Owns | Defined in |
|---|---|---|
| [`punch-context`](../../.github/skills/punch-context/SKILL.md) | Pointer-list to canonical docs; the lifecycle; the scope-discipline principle | `.github/skills/punch-context/SKILL.md` |
| [`punch-python-orchestration`](../../.github/skills/punch-python-orchestration/SKILL.md) | The `bin/punch` CLI, subprocess streaming, docker compose invocation, exit codes, evidence artifact | `.github/skills/punch-python-orchestration/SKILL.md` |
| [`punch-docker-compose`](../../.github/skills/punch-docker-compose/SKILL.md) | Service contracts, stable service names, healthchecks, multi-stage Dockerfiles, image pins | `.github/skills/punch-docker-compose/SKILL.md` |
| [`punch-k6-performance`](../../.github/skills/punch-k6-performance/SKILL.md) | k6 test shape (HTTP + Browser), thresholds, `handleSummary`, shared report builder, k6 image pin, Browser deferral | `.github/skills/punch-k6-performance/SKILL.md` |
| [`punch-data-harvest`](../../.github/skills/punch-data-harvest/SKILL.md) | Artifact paths and schemas, terminal-vs-file noise discipline, JSON/CSV contracts, HTML report builder | `.github/skills/punch-data-harvest/SKILL.md` |
| [`punch-governance-review`](../../.github/skills/punch-governance-review/SKILL.md) | Frontmatter contracts, registry consistency, boundary compliance, scope discipline, handoff hygiene | `.github/skills/punch-governance-review/SKILL.md` |

## Why six, and what each adds

Each skill names a unique **decision domain**:

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

## Why the cap moved from 3 to 6

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

## Why these are still deferred (not created)

| Candidate | Why it does NOT exist as a skill |
|---|---|
| `punch-k6-http` and `punch-k6-browser` | Splitting `punch-k6-performance` again would fragment a single decision domain (performance semantics). HTTP and Browser live in one skill with sub-sections. |
| `punch-monitoring` / `punch-injectables` | No real monitoring or fault-injection use case yet. Premature. The layer slot is reserved in `punch-boundaries.md`. |
| `punch-documentation` | The `documentation.instructions.md` path file is enough. A skill would only restate it. |
| `punch-(define|spec|plan|build|verify|review|ship)` | **Lifecycle phases are prompts and agents, not skills.** Creating them would invert the operating model. |

## Cap-lifting discipline

The cap moved from 3 to 6 because the new skills each named a *unique
decision domain* that was previously absorbed into another skill at the
cost of clarity. To add a seventh skill, propose a Plan that:

1. Names the new skill and its decision domain.
2. Lists which of the six existing skills could not absorb its
   responsibility.
3. Demonstrates a real, recurring decision the existing skills
   mishandle.
4. Updates this registry in the same PR.

If steps 2–3 cannot be answered concretely, the answer is "don't add it".

The [`punch-governance-review`](../../.github/skills/punch-governance-review/SKILL.md)
skill flags any new skill not in the active list during Review.
