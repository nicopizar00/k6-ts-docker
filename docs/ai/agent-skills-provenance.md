# Agent Skills — provenance and disposition manifest

Static, tracked record mapping the pinned upstream Agent Skills commit to every
source skill and adopted persona. Written once (Plan task G-10,
[`plan-agent-skills-adopt-adapt-optimization.md`](../specs/plan-agent-skills-adopt-adapt-optimization.md)),
manually refreshed by a human — **no automatic fetch, cache, or CI step reads
or writes this file.**

## Source

- Upstream repository: <https://github.com/addyosmani/agent-skills>
- Audited head commit: `ff2df4c07e7836a092ed28e1e9b42f4d6009280c`
- Audited release: `0.6.5` — <https://github.com/addyosmani/agent-skills/releases/tag/0.6.5>
- Local staging snapshot: `.ai-upstream/agent-skills/` (gitignored, user-refreshed
  only — this manifest reads it, never writes it)
- Adoption date: not tracked at initial adoption; this manifest was written
  retroactively on 2026-07-21. Treat all "adoption date" cells below as
  "on or before 2026-07-21" unless a later ADR/commit says otherwise.
- **Re-pinned 2026-07-30** (VC-09) to a single reproducible commit, replacing
  the prior mixed-revision baseline (previously: audited head
  `2fbfa004a0192529bc997d103fc12f19a3804aab` / release `0.6.4`, with per-file
  state split across `a5f0b17` and 13 files differing from that head —
  unverified at the time it was recorded). The tag→commit resolution was
  verified live via the GitHub API at re-pin time. See *Changes since prior
  baseline* below for the real diff this re-pin surfaces.

## 24 source skills

| Skill (upstream slug) | Mapped Punch asset | Disposition |
|---|---|---|
| `api-and-interface-design` | — | unadopted (deferred — no recurring interface-design decision yet) |
| `browser-testing-with-devtools` | *(none — retired 2026-08-28)* | **retired** — was adopted, then stayed permanently dormant (zero `.github/` activation reference; its sole target `browser-smoke.ts.example` stays a deferred placeholder per CLAUDE.md). Deleted rather than kept as dead weight; see `skill-registry.md`. |
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

## Changes since prior baseline (`a5f0b17` → `ff2df4c0`, verified 2026-07-30)

Live `git diff a5f0b17..ff2df4c0 -- skills/` against the two most recent
tracked baselines shows **18 of 24** skill files changed (not the 6 the
approved Plan named — that list undercounted; all 6 it named are a subset of
the real 18). Every changed file gets an explicit disposition; none flip
adopted↔unadopted as a result of this re-pin:

| Skill (upstream slug) | Δ size | Disposition |
|---|---|---|
| `code-review-and-quality` | 53 lines | **Real, unabsorbed.** New "Structural Remedies" section, a dependency-upgrade review workflow, and a severity-label rename (Critical/Important/Suggestion → Critical/Required/Optional/Nit). Out of VC-09's allowed paths (`punch-code-review-and-quality` not editable here) — needs its own Plan task. |
| `git-workflow-and-versioning` | 57 lines | **Real, unabsorbed.** New "Release & Versioning" section (semver, tag-as-source-of-truth, changelog discipline). Punch's Ship phase is human-gated with no release/tag concept today, so relevance needs a human call — needs its own Plan task, not auto-adopted. |
| `security-and-hardening` | 36 lines | **Real, unabsorbed, relevant.** Package-manager-agnostic audit workflow, install-script blocking, registry-provenance checks — applicable to the documented host-`npm` exception for `punch-performance-test-engineer`. Needs its own Plan task. |
| `deprecation-and-migration` | 41 lines | New expand/contract DB-schema-migration pattern. Stays **unadopted** — Punch has no live-migrating schema (Postgres seeded once via `docker/postgres/init.sql`). No action. |
| `browser-testing-with-devtools` | 17 lines | New MCP profile-isolation guidance (`--isolated` vs `--autoConnect`, security boundaries). Real content, but this Punch adoption stays **dormant** (deferred until a Plan enables a browser-capable path — the k6 Browser placeholder is explicitly deferred). Refresh at activation time, not now. |
| `documentation-and-adrs` | 12 lines | New "match the existing ADR convention first" guidance. Punch already has one fixed convention (`docs/ai/decisions/`) — low priority. Optional future review, no action taken here. |
| `planning-and-task-breakdown` | 13 lines | New `tasks/plan.md` / `tasks/todo.md` output-path convention. **Conflicts with and is superseded by** Punch's own fixed plan-output contract (`docs/architecture/specs/plan-<topic>.md`, see `punch-plan.prompt.md`) — correctly not adopted. |
| `spec-driven-development` | 6 lines | Same `tasks/` convention (see row above, superseded) plus a cross-reference note to `planning-and-task-breakdown`. Correctly not adopted. |
| `incremental-implementation` | 4 lines | Adds a "See Also" pointer to a `references/definition-of-done.md` companion file Punch's snapshot doesn't carry. Optional, low priority, no action. |
| `performance-optimization` | 2 lines | Frontmatter description tweak only, still frontend/Web-Vitals-flavored (Punch's adaptation already strips that). **The approved Plan's instruction to absorb "remeasure, noise-awareness, attempt-ledger, and keep-or-revert discipline" does not correspond to any text anywhere in the upstream tree at this pin** (verified: zero matches, full-tree grep, 2026-07-30) — not absorbed; flagged for a Plan correction rather than invented. |
| `debugging-and-error-recovery` | 1 line | Step-number typo fix only (cosmetic). No action. |
| `shipping-and-launch` | 1 line | Adds a link to the same `definition-of-done.md` companion file. Stays **unadopted** per the approved Plan. No action. |
| `frontend-ui-engineering` | 2 lines | Frontmatter wording only. Stays **unadopted** (irrelevant-to-Punch). No action. |
| `idea-refine` | 2 lines | Script-path fix only. Retired/absorbed already (Plan G-08). No action. |
| `observability-and-instrumentation` | 2 lines | Adds a companion-checklist pointer. Retired/absorbed already (Plan G-07). No action. |
| `using-agent-skills` | 2 lines | Adds a "Definition of Done" pointer. Retired/absorbed already (Plan G-09). No action. |

6 skills unchanged since `a5f0b17`: `api-and-interface-design`,
`ci-cd-and-automation`, `context-engineering`, `doubt-driven-development`,
`interview-me`, `source-driven-development`.

**Open follow-up (not this task):** `code-review-and-quality`,
`git-workflow-and-versioning`, and `security-and-hardening` carry real,
unabsorbed upstream method improvements relevant to Punch's adopted skills of
the same name. Each needs its own Spec/Plan task to review and selectively
adopt — out of scope here since VC-09's allowed edit paths cover only this
manifest and `punch-performance-optimization`.

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
- Per-file commit provenance was live-verified against GitHub at the 2026-07-30
  re-pin (see *Changes since prior baseline*) — a future refresh should repeat
  a live diff against the new pin, not assume it still holds.
- Three real, unabsorbed upstream changes are queued as open follow-ups (not
  auto-adopted here): `code-review-and-quality`, `git-workflow-and-versioning`,
  `security-and-hardening`. Each needs its own Spec/Plan task.
