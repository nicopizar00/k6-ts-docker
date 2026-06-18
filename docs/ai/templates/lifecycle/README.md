# Lifecycle artifact templates 🧩

Blank, schema-faithful skeletons for each Punch lifecycle phase. Copy one, fill it
in, save it to its canonical location. Each template mirrors the **Expected
output** section of the matching prompt in `.github/prompts/` — **the prompt is the
source of truth; these are convenience scaffolds** (no rule is restated, only the
output shape).

| Phase | Template | Canonical save location | Caveman |
|---|---|---|---|
| Spec   | `spec.template.md`   | `docs/architecture/specs/<topic>.md`        | `lite` |
| Plan   | `plan.template.md`   | `docs/architecture/specs/plan-<topic>.md`   | `full` |
| Build  | `build.template.md`  | chat / PR (canon example → golden-lifecycle) | `ultra` (sub-agents `wenyan`) |
| Verify | `verify.template.md` | chat / PR (evidence under `reports/`)        | evidence verbatim |
| Review | `review.template.md` | chat / PR                                    | `full` |
| Ship   | `ship.template.md`   | PR description                               | `full` |

- A **filled, real worked example** (the health-smoke golden path) lives in
  [`../../golden-lifecycle/`](../../golden-lifecycle/README.md).
- These templates and the golden example are **canon doc-output patterns** maintained
  by `/punch-document` and detected by `/punch-init` (readiness:
  `lifecycle_templates`).
- Caveman: persisted artifacts use `lite`/`full`, **never Wenyan**; emojis/ASCII
  emoticons are allowed in docs (the `/document` carve-out).
