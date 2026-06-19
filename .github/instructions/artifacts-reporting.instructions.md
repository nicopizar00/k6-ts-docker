---
applyTo: "src/tests/support/**,src/punch/**,reports/**,docs/validation/**"
description: Contract for artifacts, logs, summaries, and reports produced by Punch.
---
# Artifacts & Reporting — Path Instructions

Scope: producer side of every artifact Punch emit (`src/tests/support/`,
reporting/state code in `src/punch/`), artifact dir
(`reports/`), validation docs explain it
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

- **Stable artifact paths.** Five paths above part of public
  contract. Rename or split any = contract change — must
  update `docs/ai/maintenance-matrix.md` and every downstream
  consumer (CI workflow, this file, relevant skill).
- **Low-noise terminal output by default.** Terminal show progress
  and pass/fail, not every line of every container log. Full output
  go to `reports/logs/` when `--collect-logs` set.
- **Full logs to files, always.** Even when terminal quiet, log
  file complete. User debugging failure never need re-run
  to get missing detail.
- **JSON summaries are compact and stable-schema.** No raw k6 per-iteration
  dumps. Summary hold aggregates (counts, thresholds, durations) in
  shape that survive k6 upgrades.
- **HTML reports are self-contained.** Single `.html` file per test;
  no external CSS, no remote fetches, no `file://` assumptions.
- **State files are the canonical run record.** `passed: true|false` in
  `reports/state/punch-run.json` = verification gate; HTML for
  humans, JSON summaries for human inspection or future automation.
- **Naming convention.** `<test>.html`, `<test>.json` under `reports/`;
  `<service>.log` under `reports/logs/`. No date stamps or
  hashes in filenames — break CI validation lookup.
- **Don't write secrets into artifacts.** Run evidence and JSON summaries
  must not hold env vars, tokens, or external URLs verbatim.

## When this file activates

- Add new artifact.
- Change schema of existing artifact.
- Change terminal-vs-file output discipline.
- Touch `src/tests/support/report.ts` or reporting parts of
  `src/punch/`.

## Build prompt

Use [`punch-build`](../prompts/punch-build.prompt.md) — dispatcher route data-harvest tasks to `punch-runtime-engineer`.
