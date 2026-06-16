---
mode: ask
description: Phase 1 — Understand. Read-only investigation of an area of the repo.
---

# Punch — Understand

**Lifecycle phase:** Understand
**Mode:** Ask (read-only — no edits permitted)
**Owner skill:** none required; uses default Copilot capabilities

## When to use

You need to understand an area of the repo, a behavior, or a failure before
proposing a change. Examples:

- "How does `bin/punch run smoke` flow into k6?"
- "Why does the order journey test write `test-context.json`?"
- "Where does the build break if I change `tsconfig.json`?"

## Inputs

- The question or area of focus.
- (Optional) a failing log, artifact path, or PR diff to read.

## What to do

1. Read the relevant files only. Do not edit.
2. Trace the execution chain: source → bundle → image → run → report.
3. Surface assumptions, hidden coupling, and any rule from `CLAUDE.md` or
   `.github/instructions/` that constrains the area.
4. Identify the smallest unknown that would unblock a Shape step.

## Expected output

A short written summary containing:

- **What the code currently does** (file paths + line refs).
- **What is known vs. assumed.**
- **Open questions** that Shape must answer.
- **Suggested next prompt** (almost always `punch-shape`).

## Validation gate

None — no edits to verify. Shape is the next phase.
