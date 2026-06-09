# AI Operating Protocol

This file defines **how** AI-assisted changes flow through this repository.
For the **rules** about what code may look like, see `CLAUDE.md` and the
path-specific instructions under `.github/instructions/`.

## Foundational model

This project's operating model is an adaptation of Addy Osmani's
**Agent Skills + Software Lifecycle** approach. Two ideas drive it:

1. **The lifecycle is the operating system.** Every change passes through
   six phases: **Understand → Shape → Build → Verify → Review → Ship**.
2. **Skills provide behavioral specialization, not phase specialization.**
   Skills exist when a real domain (orchestration, performance, governance)
   needs its own behavioral rules. They never substitute for the lifecycle.

The repository extends this baseline with Punch-specific concerns
(Python orchestration façade, k6 + Docker execution, evidence artifacts)
but does not replace it.

## The six phases

| Phase | Purpose | Mode | Edits allowed | Owner skill |
|---|---|---|---|---|
| Understand | Read code, trace flow, surface unknowns | Ask | No | — |
| Shape | Produce a scoped plan: in/out scope, steps, evidence | Plan | No | `punch-orchestration` or `punch-performance-k6` |
| Build | Implement one slice from the confirmed plan | Agent | Yes (scoped) | depends on slice |
| Verify | Run the orchestrator and capture evidence | Agent / Ask | Only if patching the change | `punch-orchestration` + `punch-performance-k6` |
| Review | Read-only critique of the diff before Ship | Ask | No | `punch-ai-governance-audit` when `.github/`/`docs/ai/` touched |
| Ship | Commit, push, open PR; **human merges** | Agent (mechanical only) | Yes (git/gh only) | `punch-orchestration` |

The prompts for each phase live in `.github/prompts/`. See
[`prompt-registry.md`](prompt-registry.md) for what each one does.

## Permission boundaries

- **No edits in Ask Mode.** If a phase says Ask, the agent reads and writes
  prose — not files.
- **Plan Mode produces a plan**, never edits. The plan is the artifact.
- **Agent Mode is bound to the plan.** If a Build slice needs to touch a
  file outside the plan's "In scope" list, the agent returns to Shape.
- **Ship is mechanical only.** Commits, push, `gh pr create`. No merges, no
  tags, no force pushes, no skipping hooks.

## Validation gates

Each phase has an explicit gate. A change cannot advance until the gate is
met.

- **Understand → Shape:** A clear, narrowed question.
- **Shape → Build:** A human-confirmed plan.
- **Build → Verify:** A focused diff in the plan's scope.
- **Verify → Review:** `reports/state/punch-run.json` with `passed: true`
  (or an equivalent named artifact for non-test changes).
- **Review → Ship:** Review verdict = Approve.
- **Ship → done:** Human-merged PR.

See [`../workflows/validation.md`](../workflows/validation.md) for the
mechanical steps.

## Where this differs from a generic agent setup

- The orchestrator is **Python stdlib only**. No agent should suggest adding
  a Python dependency.
- The execution chain is **strictly linear**: TS → bundle (in Docker) →
  k6 image → run → reports. Do not branch it.
- The reusable skill set is **deliberately capped at three** — see
  [`skill-registry.md`](skill-registry.md) for why.
- Lifecycle phases are **prompts, not skills**. Do not create a
  `punch-build` skill.

## Drift control

- Run `.github/prompts/punch-governance-audit.prompt.md` before merging any
  PR that touches `.github/` or `docs/ai/`.
- Update the skill registry and prompt registry in the same PR that adds or
  removes a skill / prompt.
- `CLAUDE.md` is the constitution. If a rule moves, it moves there; this
  file only describes the lifecycle.
