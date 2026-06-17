---
agent: punch-reviewer
description: Phase 6 — Review. Read-only critique of the diff against the Plan before Ship.
---

# Punch — Review

**Lifecycle phase:** Review
**Mode:** Read-only — no product edits (enforced by agent definition)
**Owner skill:** [`code-review-and-quality`](../skills/code-review-and-quality/SKILL.md) (the five-axis method, with [`code-simplification`](../skills/code-simplification/SKILL.md) for the simplicity axis);
[`punch-governance-review`](../skills/punch-governance-review/SKILL.md) when the
diff touches `.github/` or `docs/ai/`; otherwise the matching domain skill
**Agent:** [`punch-reviewer`](../agents/punch-reviewer.agent.md)

## When to use

Verify has passed. Before opening or merging a PR, audit the diff for
correctness, simplicity, scope discipline, boundary compliance, and
lifecycle hygiene. For a dedicated security pass on diffs touching
`src/services/**`, env, or `docker/**`, invoke `@security-auditor`.

## Inputs

- The diff (working tree, branch vs `main`, or PR URL).
- The Plan task(s) that drove the change.
- The Verify report.

## What to do

1. **Scope check.** Are all changed files within the Plan's allowed
   paths? Flag any out-of-scope edits.
2. **Boundary check.** Does the diff respect the layer ownership in
   [`punch-boundaries.md`](../../docs/architecture/punch-boundaries.md)?
   Flag cross-layer changes that the Plan did not authorize.
3. **Rule check.** Does the diff respect `CLAUDE.md`,
   `punch-architecture.instructions.md`, and the path-specific
   instructions?
4. **Duplication check.** Did any AI asset, doc, or helper get
   duplicated?
5. **Evidence check.** Does `reports/state/punch-run.json` exist and
   show `passed: true`?
6. **Simplicity check.** Did the diff introduce premature abstraction,
   unnecessary dependencies, or speculative configuration?
7. **Ownership check.** Does the change respect each layer's domain?
8. **Governance check** (when `.github/` or `docs/ai/` is touched).
   Activate [`punch-governance-review`](../skills/punch-governance-review/SKILL.md):
   frontmatter complete, registries match files, agents and skills are
   referenced consistently.
9. **Doc check.** Are docs and the maintenance matrix updated for any
   contract change?

## Expected output

A Review report with:

- **Verdict** — Approve / Request Changes.
- **Files changed** — list.
- **Boundary compliance** — pass or specific violations.
- **Risk assessment** — one paragraph.
- **Validation coverage** — Verify evidence link + pass/fail.
- **Unintended coupling** — none, or specifics.
- **Missing docs** — none, or specifics.
- **Required follow-ups** — none, or numbered list.

## Validation gate

Approve → Ship.
Request Changes → Plan (corrective task) → Build.
