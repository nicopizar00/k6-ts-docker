# Lifecycle Workflow

The Punch lifecycle drives every non-trivial change. The phases are:

```
Define → Spec → Plan → Build → Verify → Review → Ship
```

For the *rules* about each phase (mode, edits allowed, agent persona,
owner skills), see [`../ai/operating-model.md`](../ai/operating-model.md).
For the *walkthrough* with a worked example, see
[`../ai/workflow.md`](../ai/workflow.md). This file covers the
**execution mechanics** — validation gates, failure handling, and the
discipline that keeps each step reviewable.

## Entry points

| Phase | Prompt | Agent | Resulting artifact |
|---|---|---|---|
| Define | `punch-define`                       | `punch-architect-readonly` | A written problem statement |
| Spec   | `punch-spec`                         | `punch-architect-readonly` | A spec doc (goals / non-goals / acceptance criteria) |
| Plan   | `punch-plan`                         | `punch-planner`            | A plan with scoped tasks and allowed/forbidden paths |
| Build  | one of `punch-build-*` (5 domains)    | `punch-builder-scoped`     | A focused diff for ONE task |
| Verify | `punch-verify`                       | `punch-verifier`           | `reports/state/punch-run.json` + HTML reports |
| Review | `punch-review`                       | `punch-reviewer`           | A review note: Approve / Request Changes |
| Ship   | `punch-ship`                         | `punch-reviewer`           | A commit + PR + ship-readiness summary; human merges |

## Validation gates

Each phase has an explicit gate. A change cannot advance until the gate
is met. The mechanical evidence contract lives in
[`validation.md`](validation.md).

| Transition | Gate |
|---|---|
| Define → Spec | A narrowed problem statement. |
| Spec → Plan | Agreed goals + acceptance criteria. |
| Plan → Build | Human-approved plan with per-task scope. |
| Build → Verify | Focused diff inside the task's allowed paths. |
| Verify → Review | `reports/state/punch-run.json` with `passed: true`. |
| Review → Ship | Verdict = Approve. |
| Ship → done | Human-merged PR. |

## Failure handling

- **Define surfaces a contradiction** → re-read the relevant
  instructions and `CLAUDE.md`. If the contradiction is real, file a
  Plan to fix it.
- **Plan exceeds three files in allowed-paths** → consider splitting
  into two tasks. Large tasks correlate with bad Verify signals.
- **Build needs a file outside scope** → stop. Update the Plan first.
  Do not edit a forbidden or read-only file as a "small fix".
- **Verify fails (implementation)** → return to Plan with a corrective
  task; then Build → Verify again.
- **Verify fails (environment)** → human triage; probably a Doctor
  check to add.
- **Verify fails (pre-existing)** → human triage; this PR is not
  blocked.
- **Review requests changes** → loop back to Plan for the specific
  finding; do not bundle unrelated fixes.
- **Ship's CI is red** → human investigates. The agent does not chase
  CI failures without a new Plan.

## When to use `punch-ai-governance`

The governance audit lives inside the Review phase. It activates
automatically when the diff touches `.github/` or `docs/ai/`. There is
no standalone audit prompt — Review is the audit gate.

Periodic governance review (recommended quarterly) is done by invoking
Review on a diff like `git diff main~30 main -- .github docs/ai`.

## Why this discipline

The lifecycle exists to keep AI-assisted edits **reviewable**. Each
phase produces a small, well-formed artifact (problem statement, spec,
plan, diff, evidence, review note, PR). If a phase produces something
larger or fuzzier, the agent skipped a step.
