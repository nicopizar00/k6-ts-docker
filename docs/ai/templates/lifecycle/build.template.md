# Build — <task ID>

> **Template.** Build report (`punch-builder` evidence contract).
> Pattern source: `.github/prompts/punch-build.prompt.md` (Caveman `ultra`;
> execution sub-agents `wenyan`; **evidence never compressed**).

- **Result** — <what done; or "verification-only task — no product code change">
- **Changed Files** — <paths, or "none">
- **Evidence** — <commands + run output, quoted verbatim>
  ```
  <verbatim>
  ```
- **Unresolved Assumptions** — <list, or "none">
- **Recommended Next Step** — <one line → Verify>

**Gate:** done only when `reports/state/punch-run.json` records `passed: true`
(claimed at Verify, not here). Any edit outside task allowed paths → stop,
back to Plan.
