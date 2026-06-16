# AI Operating Model

This file defines **how** AI-assisted changes flow through Punch.
For the **rules** about what code may look like, see `CLAUDE.md` and the
path-specific instructions under `.github/instructions/`.

(Previously `operating-protocol.md`. The rename is part of the redesigned
lifecycle: Define → Spec → Plan → Build → Verify → Review → Ship.)

## Foundational principle

> The AI may explore broadly to understand. The AI may plan structurally to
> delimit. The AI may only build inside an explicit scoped boundary. The AI
> must verify through Punch's official runtime contract. The AI must not
> expand implementation scope without returning to planning.

This is the single sentence the entire operating model is shaped around.

## The seven phases

| Phase | Purpose | Mode | Edits allowed |
|---|---|---|---|
| Define   | Read code, trace flow, surface unknowns, name the problem | Ask | No |
| Spec     | Translate the problem into goals, non-goals, and constraints | Ask | Only the spec doc, if requested |
| Plan     | Produce scoped tasks with allowed / read-only / forbidden paths | Ask (Plan discipline) | Only the plan doc, if requested |
| Build    | Implement one approved task within its declared scope | Agent (scoped) | Yes — only allowed paths |
| Verify   | Run official Punch commands and confirm evidence | Agent / Ask | Only if patching the change |
| Review   | Read-only critique of the diff against the plan | Ask | No |
| Ship     | Commit, push, open PR; **human merges** | Agent (mechanical only) | Yes (git/gh only) |

Each phase has a matching prompt under `.github/prompts/`. See
[`prompt-registry.md`](prompt-registry.md) for what each one does and
[`workflow.md`](workflow.md) for a walkthrough.

## Four kinds of AI asset

Punch's AI configuration uses four distinct artifact types. They are not
interchangeable.

| Kind | Lives in | Answers | Lifetime |
|---|---|---|---|
| **Instructions** | `.github/instructions/` (path-scoped) and `CLAUDE.md` (global) | "What rules apply when I touch this code?" | Long — change rarely. |
| **Prompts** | `.github/prompts/` | "How do I run *this phase* of the lifecycle?" | Long — one per phase/domain. |
| **Skills** | `.github/skills/<skill>/SKILL.md` | "What does an expert in *this domain* always do?" | Long — one per decision domain. |
| **Agents** | `.github/agents/` | "Which behavioral profile fits *this phase*?" | Long — one per persona. |

Rule of thumb: **instructions** are passive (loaded whenever a file is
touched). **Prompts** are active (the human runs them). **Skills** are
behavioral (the prompt or agent activates them). **Agents** are persona
constraints (which tools, which mode, which handoff rules).

## Permission boundaries

- **No edits in Ask Mode.** If a phase says Ask, the agent reads and writes
  prose — not files.
- **Plan output is the plan, not edits.** The plan doc itself is the
  artifact. Build refuses to edit files outside the plan's allowed list.
- **Build is scoped.** Each Build prompt declares allowed / read-only /
  forbidden paths. Scope expansion → stop, return to Plan.
- **Verify uses official Punch commands.** No ad-hoc `docker run`. No host
  `k6` or `npm`. See [`docs/architecture/punch-boundaries.md`](../architecture/punch-boundaries.md).
- **Ship is mechanical only.** Commits, push, `gh pr create`. No merges, no
  tags, no force pushes, no skipping hooks.

## Validation gates

A change cannot advance until its gate is met.

| Transition | Gate |
|---|---|
| Define → Spec | A clear, narrowed problem statement. |
| Spec → Plan | Goals, non-goals, and acceptance criteria documented. |
| Plan → Build | Plan approved by a human; allowed paths listed. |
| Build → Verify | A focused diff inside the plan's allowed paths. |
| Verify → Review | `reports/state/punch-run.json` with `passed: true` (or an equivalent named artifact for non-test changes). |
| Review → Ship | Review verdict = Approve. |
| Ship → done | Human-merged PR. |

Mechanical steps: see [`../workflows/validation.md`](../workflows/validation.md).

## Adopting this in a team

1. **Start with one phase.** Most teams under-do Plan and over-do Build.
   Begin by enforcing "no Build without Plan" for one sprint.
2. **One agent per phase, not one agent per ticket.** The 5 agents in
   `.github/agents/` are reusable across all work. Resist adding a sixth.
3. **Promote prompts, not prose.** When you find yourself pasting the same
   guidance into chat, that's a missing prompt — file a small PR.
4. **Audit before adding.** New skill / new agent / new prompt should answer:
   *which existing one could not absorb this?* If the answer is fuzzy, don't add.

## Avoiding agent sprawl

This redesign deliberately moved from a 3-skill cap to a 6-skill / 5-agent
setup. The new ceiling is enforced by *function*, not *count*:

- Each **skill** must name a unique decision domain (architecture,
  orchestration, runtime, performance, artifacts, governance). Six is the
  full domain set; adding more should require killing one.
- Each **agent** must name a unique behavioral persona (architect-readonly,
  planner, scoped builder, verifier, reviewer). Five is the full persona
  set; adding more should require killing one.
- Each **prompt** is either a lifecycle phase or a build-domain
  specialization. Eleven covers the matrix; new prompts must show why an
  existing one cannot stretch.

The `punch-governance-review` skill checks new additions against this rule
during Review.

## Where this differs from a generic agent setup

- The orchestrator is **Python stdlib only**. No agent should suggest adding
  a Python dependency.
- The execution chain is **strictly linear**: TS → bundle (in Docker) →
  k6 image → run → reports. Do not branch it.
- CI/CD is **external** to Punch. Punch provides reusable local/CI-compatible
  container contracts; it does not own GitHub Actions workflows.

## Drift control

- Run `punch-governance-review` (via the Review phase) before merging any PR
  that touches `.github/` or `docs/ai/`.
- Update `skill-registry.md` and `prompt-registry.md` in the same PR that
  adds or removes an asset.
- `CLAUDE.md` is the constitution. If a rule moves, it moves there; this
  file only describes the lifecycle.
