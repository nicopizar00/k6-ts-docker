# Lifecycle artifact templates 🧩

Blank, schema-faithful skeletons for each Punch lifecycle phase. Copy one, fill,
save to canonical location. Each template mirror **Expected output** section of
matching prompt in `.github/prompts/` — **prompt is source of truth; these
convenience scaffolds** (no rule restated, only output shape).

| Phase | Template | Canonical save location | Caveman |
|---|---|---|---|
| Spec   | `spec.template.md`   | `docs/architecture/specs/<topic>.md`        | `lite` |
| Plan   | `plan.template.md`   | `docs/architecture/specs/plan-<topic>.md`   | `full` |
| Build  | `build.template.md`  | chat / PR (canon example → golden-lifecycle) | `ultra` (engineers `wenyan-lite`) |
| Test   | `test.template.md`   | chat / PR (evidence under `reports/`)        | `ultra`; evidence verbatim |
| Review | `review.template.md` | chat / PR                                    | `full` |
| Ship   | `ship.template.md`   | PR description                               | `full` |

- **Filled, real worked example** (health-smoke golden path) lives at
  [`../../golden-lifecycle/`](../../golden-lifecycle/README.md).
- These templates + golden example = **canon doc-output patterns** maintained
  by `/punch-document`, detected by `/punch-init` (readiness:
  `lifecycle_templates`).
- Caveman: persisted artifacts use `lite`/`full`, **never Wenyan**; emojis/ASCII
  emoticons allowed in docs (the `/document` carve-out).
- **Provenance.** Lifecycle shapes are **adapted** (not hard-forked) from upstream
  [agent-skills](https://github.com/addyosmani/agent-skills) to fit Punch; the
  `.github/prompts/` files remain the behavior source of truth.
