---
agent: punch-code-reviewer
description: Phase 6 — Review. Read-only five-axis critique of the diff against the Plan before Ship. Owner punch-code-reviewer holds the verdict; cavecrew allowed only as a bounded pre-scan.
---
# Punch — Review

**Lifecycle phase:** Review
**Mode:** Read-only — no product edits (enforced by agent definition)
**Owner skill:** [`punch-code-review-and-quality`](../skills/punch-code-review-and-quality/SKILL.md) (five-axis method, with [`punch-code-simplification`](../skills/punch-code-simplification/SKILL.md) for simplicity axis);
[`punch-ai-governance`](../skills/punch-ai-governance/SKILL.md) when
diff touches `.github/` or `docs/ai/`; else matching domain skill
**Agent:** [`punch-code-reviewer`](../agents/punch-code-reviewer.agent.md) — the Review verdict owner (five-axis, adapted from vendor `code-reviewer`).
**Required skill:** [`punch-code-review-and-quality`](../skills/punch-code-review-and-quality/SKILL.md).
**Operating comms:** Caveman **`full`** (per-phase canon). Lead normal prose for risk/architecture judgment. Brief cavecrew (any other sub-agent nesting) in `wenyan-ultra`; cavecrew reports **non-guarded (lazy)** — use the artifact as-is. Canon: [`punch-build-caveman`](../skills/punch-build-caveman/SKILL.md).

## When to use

Test passed. Before open or merge PR, audit diff for
correctness, simplicity, scope discipline, boundary compliance,
lifecycle hygiene. Dedicated security pass on diffs touching
`src/services/**`, env, or `docker/**` → invoke `@punch-security-auditor`.

## Inputs

- Diff (working tree, branch vs `main`, or PR URL).
- Plan task(s) that drove change.
- Test report.

## What to do

1. **Scope check.** All changed files within Plan's allowed
   paths? Flag out-of-scope edits.
2. **Boundary check.** Diff respects layer ownership in
   [`punch-boundaries.md`](../../docs/architecture/punch-boundaries.md)?
   Flag cross-layer changes Plan did not authorize.
3. **Rule check.** Diff respects `.github/copilot-instructions.md`,
   `punch-architecture.instructions.md`, and path-specific
   instructions?
4. **Duplication check.** Any AI asset, doc, or helper
   duplicated?
5. **Evidence check.** `reports/state/punch-run.json` exists and
   shows `passed: true`?
6. **Simplicity check.** Diff introduced premature abstraction,
   unneeded dependencies, or speculative config?
7. **Ownership check.** Change respects each layer's domain?
8. **Governance check** (when `.github/` or `docs/ai/` touched).
   Activate [`punch-ai-governance`](../skills/punch-ai-governance/SKILL.md):
   frontmatter complete, registries match files, agents and skills
   referenced consistently.
9. **Doc check.** Docs and maintenance matrix updated for any
   contract change?

## Expected output

Review report with:

- **Verdict** — Approve / Request Changes.
- **Files changed** — list.
- **Boundary compliance** — pass or specific violations.
- **Risk assessment** — one paragraph.
- **Validation coverage** — Test evidence link + pass/fail.
- **Unintended coupling** — none, or specifics.
- **Missing docs** — none, or specifics.
- **Required follow-ups** — none, or numbered list.

## Delegation (bounded workers only)

`punch-code-reviewer` is the Review coordinator. cavecrew is allowed **only as a
bounded, optional pre-scan** — it never replaces the five-axis review. It may
spawn **read-only** cavecrew leaf workers (depth-1) over a large diff:
[`cavecrew-investigator`](../agents/cavecrew-investigator.agent.md) (locate the
diff's touched defs / tests) and
[`cavecrew-reviewer`](../agents/cavecrew-reviewer.agent.md) (compact per-file
diff smoke check). **Not** `cavecrew-builder` — reviewer has no edit tool, so an
editing worker is not ⊆ its scope. Workers inherit the coordinator's read-only
scope by injected brief (`wenyan-ultra`) and report **non-guarded (lazy)**; the
coordinator may use their findings as-is. Findings feed the review — the
Approve / Request Changes **verdict stays punch-code-reviewer's own**.

## Validation gate

Approve → Ship.
Request Changes → Plan (corrective task) → Build.
