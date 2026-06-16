# Skill Registry

The MVP supports exactly **three** skills. Each entry below explains its
responsibility, scope, and why it earns a separate skill. The "Deferred"
section lists candidate skills that were intentionally **not** created.

## Active skills

| Skill | Owns | Defined in |
|---|---|---|
| [`punch-orchestration`](../../.github/skills/punch-orchestration/SKILL.md) | The `bin/punch` CLI, subprocess streaming, docker compose invocation, exit codes, evidence artifact | `.github/skills/punch-orchestration/SKILL.md` |
| [`punch-performance-k6`](../../.github/skills/punch-performance-k6/SKILL.md) | k6 test shape, thresholds, `handleSummary`, shared report builder, k6 image pin, Browser deferral | `.github/skills/punch-performance-k6/SKILL.md` |
| [`punch-ai-governance-audit`](../../.github/skills/punch-ai-governance-audit/SKILL.md) | Frontmatter contracts, three-skill cap, lifecycle alignment, duplication and conflict detection | `.github/skills/punch-ai-governance-audit/SKILL.md` |

## Why three and not more

Each active skill represents a distinct **decision domain**:

- **Orchestration** decides *how the run happens*.
- **Performance** decides *what "fast enough" means*.
- **Governance** decides *whether the operating model itself is healthy*.

These domains have different reviewers, different failure modes, and
different cadences. Splitting them isolates each concern. Splitting further
would fragment a single decision domain into nominal sub-skills — added
overhead without behavioral specialization.

## Why these are deferred (not created)

| Candidate | Why it does NOT exist as a skill |
|---|---|
| `punch-python` | `punch-orchestration` already owns Python. A separate Python skill would duplicate the rules in `.github/instructions/python-orchestration.instructions.md`. |
| `punch-docker` | Docker semantics are owned by `docker-compose.yml` and the per-service Dockerfiles. Path instructions cover the rules. No behavioral specialization that orchestration or performance lacks. |
| `punch-k6-http` and `punch-k6-browser` | Both are k6 conventions. Splitting fragments a single decision domain (performance semantics). |
| `punch-data-harvesting` | No real data harvesting use case yet. Premature. |
| `punch-reporting` | The HTML and JSON shape is owned by `src/tests/support/report.ts` and the `handleSummary` contract in `punch-performance-k6`. No separate decision domain. |
| `punch-documentation` | The `documentation.instructions.md` path file is enough. A skill would only restate it. |
| `punch-understand`, `punch-shape`, `punch-build`, `punch-verify`, `punch-review`, `punch-ship` | **Lifecycle phases are prompts, not skills.** Creating them would invert the operating model. |

## Cap enforcement

The `punch-ai-governance-audit` skill explicitly flags any new skill not in
the active list. To add a fourth skill, propose a Shape plan that:

1. Names the new skill.
2. Lists what existing skill could not absorb its responsibility.
3. Demonstrates a real, recurring decision the existing skills mishandle.
4. Updates this registry in the same PR.

If steps 2–3 cannot be answered concretely, the answer is "don't add it".
