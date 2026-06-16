---
mode: ask
description: Phase 5 — Review. Read-only critique of the staged change before Ship.
---

# Punch — Review

**Lifecycle phase:** Review
**Mode:** Ask (read-only — no edits permitted)
**Owner skill:** `punch-ai-governance-audit` when the change touches
`.github/` or `docs/ai/`; otherwise no skill required.

## When to use

Verify has passed. Before opening or merging a PR, audit the diff for
correctness, simplicity, and lifecycle compliance.

## Inputs

- The diff (working tree, branch vs `main`, or PR URL).
- The Shape plan that drove the change.

## What to do

1. **Scope check.** Are all changed files in the plan's "In scope" list?
2. **Rule check.** Does the diff respect `CLAUDE.md` and the relevant
   `.github/instructions/` files?
3. **Duplication check.** Did any AI asset, doc, or helper get duplicated?
4. **Evidence check.** Does `reports/state/punch-run.json` exist and pass?
5. **Simplicity check.** Did the diff introduce premature abstraction,
   unnecessary dependencies, or speculative configuration?
6. **Ownership check.** Does the change respect the architectural boundary?
   (Python = control flow; compose = container execution; k6 = perf; reports
   = evidence; AI assets = workflow guidance.)

## Expected output

A review note with:

- **Verdict:** Approve / Request changes.
- **Findings:** numbered list, each with file path and rationale.
- **Required follow-ups** (if any) before Ship.

## Validation gate

Ship is the next phase only if verdict is Approve.
