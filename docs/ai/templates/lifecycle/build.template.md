# Build — <task ID>

> **Template.** Build report (`punch-builder` evidence contract).
> Pattern source: `.github/prompts/punch-build.prompt.md` (Caveman `ultra`;
> engineers `wenyan-lite`, cavecrew `wenyan-full`, workers `wenyan-ultra`;
> **evidence never compressed**).

- **Result** — <what done; or "verification-only task — no product code change">
- **Changed Files** — <paths, or "none">
- **Evidence** — <commands + run output, quoted verbatim>
  ```
  <verbatim>
  ```
- **Unresolved Assumptions** — <list, or "none">
- **Recommended Next Step** — <one line → Test>

**Gate:** done only when `reports/state/punch-run.json` records `passed: true`
(claimed at Test, not here). Any edit outside task allowed paths → stop,
back to Plan.
