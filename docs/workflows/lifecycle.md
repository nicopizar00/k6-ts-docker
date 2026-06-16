# Lifecycle Workflow

The Punch lifecycle drives every non-trivial change. The phases are:

```
Understand → Shape → Build → Verify → Review → Ship
```

For the *rules* about each phase (mode, edits allowed, owner skill), see
[`../ai/operating-protocol.md`](../ai/operating-protocol.md). This file
describes the **workflow** — what a developer actually does.

## Entry points

| Phase | Prompt | Skill (if any) | Resulting artifact |
|---|---|---|---|
| Understand | `punch-understand`         | — | A written summary of behavior + open questions |
| Shape      | `punch-shape`              | `punch-orchestration` or `punch-performance-k6` | A scoped plan with "In scope" / "Out of scope" / steps / evidence |
| Build      | `punch-build-slice`        | depends on slice | A focused diff for ONE slice |
| Verify     | `punch-verify`             | `punch-orchestration` + `punch-performance-k6` | `reports/state/punch-run.json` + HTML reports |
| Review     | `punch-review`             | `punch-ai-governance-audit` if AI assets changed | A review note: Approve / Request changes |
| Ship       | `punch-ship`               | `punch-orchestration` | A commit + PR; human merges |

## End-to-end walk-through

A typical change to a k6 threshold:

1. **Understand**
   - Run `punch-understand` against the failing CI run or the threshold to
     change.
   - Output: "p95 in `catalog-gate.ts` is 500ms; the gateway adds ~120ms
     round-trip; the headroom is 380ms before the gate fires."

2. **Shape**
   - Run `punch-shape` with that summary.
   - Output: a plan listing exactly the files to change
     (`src/tests/catalog-gate.ts`) and the evidence
     (`reports/state/punch-run.json` with `passed: true`).

3. **Build**
   - Run `punch-build-slice` for the one numbered step.
   - Edit only `src/tests/catalog-gate.ts`.

4. **Verify**
   - Run `punch-verify`:
     - `bin/punch doctor`
     - `bin/punch run gate`
   - Confirm `reports/state/punch-run.json` records `passed: true`.

5. **Review**
   - Run `punch-review` against the diff.
   - Output: a verdict with any findings.

6. **Ship**
   - Run `punch-ship`. The agent commits, pushes, and opens a PR.
   - **A human merges.**

## When to use `punch-governance-audit`

Outside the linear flow:

- Before merging any PR that touches `.github/` or `docs/ai/`.
- On a periodic cadence (recommended: quarterly).

This audit catches duplication, lifecycle drift, missing frontmatter, and
unjustified new skills. It does not edit; fixes go through a normal Build
slice.

## Failure handling

- **Understand surfaces a contradiction** → re-read the relevant
  instructions and `CLAUDE.md`. If the contradiction is real, file a Shape
  plan to fix it.
- **Shape exceeds three files in scope** → consider splitting into two
  plans. Large plans correlate with bad Verify signals.
- **Build needs a file outside scope** → stop. Update the Shape plan first.
- **Verify fails** → return to Shape (or Understand). Never patch silently.
- **Review requests changes** → loop back to Build for the specific
  finding; do not bundle unrelated fixes.
- **Ship's CI is red** → human investigates. The agent does not chase CI
  failures without a new Shape plan.

## Why this discipline

The lifecycle exists to keep AI-assisted edits **reviewable**. Each phase
produces a small, well-formed artifact (summary, plan, diff, evidence,
review note, PR). If a phase produces something larger or fuzzier, the
agent skipped a step.
