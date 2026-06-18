---
applyTo: "src/tests/support/**,src/punch/**,reports/**,docs/validation/**"
description: Contract for artifacts, logs, summaries, and reports produced by Punch.
---

# Artifacts & Reporting — Path Instructions

Scope: the producer side of every artifact Punch emits (`src/tests/support/`,
the reporting/state code in `src/punch/`), the artifact directory
(`reports/`), and the validation docs that explain it
(`docs/validation/`).

## What counts as an artifact

| Artifact | Path | Producer | Reader |
|---|---|---|---|
| Run evidence (machine) | `reports/state/punch-run.json` | `src/punch/__main__.py` | CI validation job, automation |
| Journey context (machine) | `reports/state/test-context.json` | `src/tests/order-journey.ts` | Subsequent journey assertions |
| HTML report (per test) | `reports/<test>.html` | `src/tests/support/report.ts` | Humans |
| JSON summary (per test) | `reports/<test>.json` | k6 `handleSummary` | Humans + automation |
| Docker logs | `reports/logs/<service>.log` | `src/punch/` with `--collect-logs` | Humans debugging failures |

## Rules

- **Stable artifact paths.** The five paths above are part of the public
  contract. Renaming or splitting any of them is a contract change — it
  must update `docs/ai/maintenance-matrix.md` and every downstream
  consumer (CI workflow, this file, the relevant skill).
- **Low-noise terminal output by default.** The terminal shows progress
  and pass/fail, not every line of every container's log. Full output
  goes to `reports/logs/` when `--collect-logs` is set.
- **Full logs to files, always.** Even when terminal is quiet, the log
  file is complete. A user debugging a failure should never need to re-run
  to get the missing detail.
- **JSON summaries are compact and stable-schema.** No raw k6 per-iteration
  dumps. The summary holds aggregates (counts, thresholds, durations) in
  a shape that survives k6 upgrades.
- **HTML reports are self-contained.** A single `.html` file per test;
  no external CSS, no remote fetches, no `file://` assumptions.
- **State files are the canonical run record.** `passed: true|false` in
  `reports/state/punch-run.json` is the verification gate; HTML is for
  humans, JSON summaries are for human inspection or future automation.
- **Naming convention.** `<test>.html`, `<test>.json` under `reports/`;
  `<service>.log` under `reports/logs/`. Don't introduce date stamps or
  hashes in filenames — that breaks the CI validation lookup.
- **Don't write secrets into artifacts.** Run evidence and JSON summaries
  must not contain env vars, tokens, or external URLs verbatim.

## When this file activates

- Adding a new artifact.
- Changing the schema of an existing artifact.
- Changing terminal-vs-file output discipline.
- Touching `src/tests/support/report.ts` or the reporting parts of
  `src/punch/`.

## Build prompt

Use [`punch-build`](../prompts/punch-build.prompt.md) — the dispatcher routes data-harvest tasks to `punch-runtime-engineer`.
