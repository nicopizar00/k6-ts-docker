---
mode: agent
description: Phase 3 — Build. Implement ONE slice from a confirmed Shape plan.
---

# Punch — Build Slice

**Lifecycle phase:** Build
**Mode:** Agent (edits permitted, scoped to the plan)
**Owner skill:** `punch-orchestration` or `punch-performance-k6` depending on
the slice

## When to use

You have a **confirmed** Shape plan and want to execute one numbered step.
One slice per invocation — do not bundle slices.

## Inputs

- The confirmed plan (link or paste).
- The slice number / name to implement.

## What to do

1. Re-read the plan's "In scope" list.
2. Edit **only** the files in that list. If you discover the change requires
   a file outside scope, stop and return to Shape.
3. Match existing style and naming. Do not introduce abstractions beyond
   what the slice requires.
4. Run the relevant doctor/check command (`bin/punch doctor`,
   `docker compose config`, `npm run build` inside the builder stage) where
   cheap. Do not run the full suite yet — Verify will do that.

## Expected output

- A focused diff covering only the slice.
- A short note describing what the next slice is (or "all slices done →
  Verify").

## Validation gate

Verify is the next phase. Do not claim success here; Build only produces
candidate changes.
