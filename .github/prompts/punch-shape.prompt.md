---
mode: ask
description: Phase 2 — Shape. Produce a scoped implementation plan; no edits.
---

# Punch — Shape

**Lifecycle phase:** Shape
**Mode:** Plan (read-only — output is a plan, not edits)
**Owner skill:** `punch-orchestration` (control-flow shape) or
`punch-performance-k6` (test shape) depending on the change

## When to use

You have an Understand summary and need a tight implementation plan before
touching files. Use this before every non-trivial Build.

## Inputs

- The Understand summary (or a clear problem statement).
- The constraint set: relevant files in `CLAUDE.md`, applicable path
  instructions, and the execution chain.

## What to do

1. State the goal in one sentence.
2. List the **smallest** set of files to change. Each entry: path + one-line
   reason.
3. List the files **deliberately not changed** and why.
4. Identify the validation evidence the Verify phase will produce
   (e.g. `reports/state/punch-run.json`, an HTML report, a doctor check).
5. Call out risks, rollback steps, and any rule in `CLAUDE.md` the plan
   tests against.

## Expected output

A plan document with:

- **Goal**
- **In scope** (file list)
- **Out of scope** (file list + reason)
- **Steps** (numbered, each step independently reviewable)
- **Validation evidence** (commands + artifacts)
- **Risks / rollback**

## Validation gate

The plan must be confirmed by a human before any Build step runs. Build
prompts refuse to edit files outside the "In scope" list.
