# Agent Skills — provenance and disposition manifest

Static, tracked record mapping the pinned upstream Agent Skills commit to every
source skill and adopted persona. Written once (Plan task G-10,
[`plan-agent-skills-adopt-adapt-optimization.md`](../specs/plan-agent-skills-adopt-adapt-optimization.md)),
manually refreshed by a human — **no automatic fetch, cache, or CI step reads
or writes this file.**

## Source

- Upstream repository: <https://github.com/addyosmani/agent-skills>
- Audited head commit: `2fbfa004a0192529bc997d103fc12f19a3804aab`
- Audited release: `0.6.4` — <https://github.com/addyosmani/agent-skills/releases/tag/0.6.4>
- Local staging snapshot: `.ai-upstream/agent-skills/` (gitignored, user-refreshed
  only — this manifest reads it, never writes it)
- Adoption date: not tracked at initial adoption; this manifest was written
  retroactively on 2026-07-21. Treat all "adoption date" cells below as
  "on or before 2026-07-21" unless a later ADR/commit says otherwise.
- **Per-file commit provenance (20/24 at a prior commit `a5f0b17`, four later,
  13 differing from the audited head above) is the approved Spec's own
  baseline-evidence claim, flagged unverified at Spec approval** — recorded
  here as-is, **not independently re-verified against live GitHub** by this
  manifest. A future refresh should confirm it with a live diff, not assume it.

## 24 source skills

| Skill (upstream slug) | Mapped Punch asset | Disposition |
|---|---|---|
| `api-and-interface-design` | — | unadopted (deferred — no recurring interface-design decision yet) |
| `browser-testing-with-devtools` | `punch-browser-testing-with-devtools` | adopted (deferred until a Plan enables a browser-capable image/service/test/evidence path) |
| `ci-cd-and-automation` | — | unadopted (irrelevant-to-Punch — CI/CD external to Punch by design) |
| `code-review-and-quality` | `punch-code-review-and-quality` | adopted |
| `code-simplification` | `punch-code-review-and-quality` (readability/simplicity axis) | superseded-by-Punch — absorbed, standalone skill retired (Plan G-08) |
| `context-engineering` | `punch-context-engineering` | adopted |
| `debugging-and-error-recovery` | `punch-debugging-and-error-recovery` | adopted (frontmatter `name` mismatch fixed, Plan G-01) |
| `deprecation-and-migration` | — | unadopted (deferred — infrequent; handled by `punch-documentation-and-adrs` + `punch-git-workflow-and-versioning`) |
| `documentation-and-adrs` | `punch-documentation-and-adrs` | adopted |
| `doubt-driven-development` | `punch-doubt-driven-development` | adopted (trigger-only: high-risk/ambiguous decisions) |
| `frontend-ui-engineering` | — | unadopted (irrelevant-to-Punch — no frontend surface) |
| `git-workflow-and-versioning` | `punch-git-workflow-and-versioning` | adopted |
| `idea-refine` | `punch-spec-driven-development` (clarify step) | superseded-by-Punch — absorbed, standalone skill retired (Plan G-08) |
| `incremental-implementation` | `punch-incremental-implementation` | adopted (the one default Build method) |
| `interview-me` | — | unadopted (deferred — overlaps the absorbed idea-refine clarify step) |
| `observability-and-instrumentation` | `punch-data-harvest` (Observability discipline section) | superseded-by-Punch — absorbed, standalone skill retired (Plan G-07) |
| `performance-optimization` | `punch-performance-optimization` | adopted (trigger-only: threshold regression) |
| `planning-and-task-breakdown` | `punch-planning-and-task-breakdown` | adopted |
| `security-and-hardening` | `punch-security-and-hardening` | adopted |
| `shipping-and-launch` | — | unadopted (deferred — name/deploy-rollback model clashes with Punch's mechanical, human-gated `punch-ship`) |
| `source-driven-development` | `punch-source-driven-development` | adopted (trigger-only: version-sensitive API work) |
| `spec-driven-development` | `punch-spec-driven-development` | adopted |
| `test-driven-development` | `punch-test-driven-development` | adopted (trigger-only: behavioral change/bug proof) |
| `using-agent-skills` | `copilot-instructions.md` + `docs/ai/skill-registry.md` + `docs/ai/agent-guards.md` | superseded-by-Punch — absorbed across three canonical files, standalone meta-skill retired (Plan G-09) |

Row count: 24 (all source skills accounted for — 10 unadopted/deferred, 10 adopted
and retained standalone, 4 adopted-then-absorbed-and-retired).

## 3 adopted upstream personas

| Upstream persona | Punch agent | Disposition |
|---|---|---|
| `code-reviewer` | `punch-code-reviewer` | adopted, adapted to Punch's five-axis model + evidence contract |
| `security-auditor` | `punch-security-auditor` | adopted, adapted to Punch's surfaces (gateway input, Postgres, secrets/env, SSRF, supply chain — no web auth/XSS) |
| `test-engineer` | `punch-test-engineer` | adopted, adapted to Punch's k6 + `reports/state/punch-run.json` evidence model |

## Punch-native wrapper (not a direct persona adoption)

| Punch agent | What it is | Disposition |
|---|---|---|
| `punch-release-captain` | Native wrapper around the vendor `/ship` **fan-out pattern** (parallel invoke → synthesize → gate) | native — adapts a *pattern*, not a 1:1 upstream `release-captain` persona. Its own description already states this ("Adapts the vendor agent-skills release-captain to Punch"); recorded here explicitly per Spec baseline evidence so no future reader mistakes it for a direct persona port. |

Row count: 3 persona rows + 1 release-captain row = 4.

## Checksum / adaptation classification

Per `punch-ai-governance`'s canon adopt-adapt procedure: every adopted-and-retained
Punch skill above is **adapted-prefixed** (`punch-<name>` maps to a canon `<name>`,
already correctly named — no rename owed). None are byte-identical to the local
`.ai-upstream` snapshot; the aggregate reduction across the (now 14, post-G-07/08/09)
retained adapted lifecycle skills plus domain skills was 2,384 Punch lines vs 5,065
upstream-baseline lines at Spec approval (52.9% reduction) — re-verify this ratio
if upstream is refreshed, don't assume it holds.

## Refresh discipline

- This file is **not** auto-generated and **not** read by any script, hook, or CI
  job — a human edits it when an adoption/retirement decision changes.
- `.ai-upstream/**` stays gitignored local staging; refreshing it is a separate,
  explicit user action (see [`.github/.ai-upstream/README.md`](../../.github/.ai-upstream/README.md))
  that does not itself update this manifest — update both deliberately, together.
- A future `/punch-document` wave may re-verify the per-file commit provenance
  claim above against live GitHub; until then it stays flagged unverified.
