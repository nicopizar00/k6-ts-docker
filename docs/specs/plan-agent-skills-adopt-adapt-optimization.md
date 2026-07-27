# Plan — Agent Skills adopt-adapt reliability and efficiency

> **Status:** Approved (human, manual edits — G-02 omitted, 2026-07-21).
> Omitting G-02 leaves Spec Acceptance Criterion 2 (background skills hidden
> via `user-invocable: false`) undelivered by this Plan — the 23 domain/
> lifecycle skills stay visible in the slash-command menu. Not reconciled
> here; a future Plan may pick it back up.
> **Owner agent:** `punch-ai-governance` (self-executes; no `punch-builder`
> hand-off — this Plan stays entirely inside the governance domain per
> `punch-ai-governance.agent.md`'s "Complete admin over `.github/**` +
> `docs/**`" scope). Each task below is a Build unit `punch-ai-governance`
> performs directly in ≤3-file steps (its own guard), not routed to
> `punch-runtime-engineer` / `punch-performance-test-engineer`.
> **Location:** `docs/specs/plan-<topic>.md`, matching the Spec's own location
> note and every prior plan doc in this repo — `docs/architecture/specs/`
> named by the older template does not exist.
> **Source Spec:** [`spec-agent-skills-adopt-adapt-optimization.md`](spec-agent-skills-adopt-adapt-optimization.md)
> (Approved, `punch-ai-governance` Spec-phase audit, 2026-07-21).

- **Goal** (from Spec): Make Punch's adopted/adapted Agent Skills and personas
  reliably discoverable, selectively loaded, executable within declared agent
  boundaries, source-traceable, and demonstrably worth their maintenance cost
  without changing Punch runtime behavior.

## Pre-flight evidence (gathered for this Plan, not restated per-task)

- `punch-debugging-and-error-recovery/SKILL.md` is the **only** skill/dir name
  mismatch (verified: 24 other skills match).
- 23 of 25 `.github/skills/*/SKILL.md` carry **no** `user-invocable` field at
  all (defaults visible); only `caveman` and `graphify` declare
  `user-invocable: true` deliberately.
- `punch-ship.prompt.md` and `punch-release-captain.agent.md` fan out the
  Test/Review/Security trio **unconditionally** — no evidence-freshness reuse
  logic exists yet. This is a real gap versus Spec FR8, not just documentation
  drift.
- `punch-test-engineer.agent.md` already states its `/punch-ship` fan-out
  permission explicitly (description line + body line 62).
  `punch-code-reviewer.agent.md` and `punch-security-auditor.agent.md` do
  **not** — grepped for `Ship`/`release-captain`, no hits in either body. Gap
  versus Spec FR7/AC6.
- `AGENTS.md:54` reads `Spec → Plan → Build → Verify → Review → Ship` (uses
  **Verify**) and `AGENTS.md:96` claims **"9 prompts: spec, plan, build, test,
  verify, review, ship, document, init"** — both wrong. Only 8 prompt files
  exist; `docs/ai/prompt-registry.md:27` already correctly states "no separate
  Verify prompt." `AGENTS.md` is the stale file.
- `docs/ai/skill-registry.md` still carries live rows for
  `punch-code-simplification`, `punch-idea-refine`,
  `punch-observability-and-instrumentation`, and `punch-using-agent-skills` —
  all four are named "Absorb then retire" in the approved Spec's disposition
  table.
- No provenance/disposition manifest exists yet (`docs/ai/decisions/` has only
  three unrelated ADRs: 0001, 0002, 0004).

## Tasks

### G-01 — Fix the one skill-identity mismatch

- **Goal** — Make `punch-debugging-and-error-recovery`'s frontmatter `name`
  match its parent directory so VS Code discovers it reliably (Spec FR1, AC1).
- **Allowed edit paths:** `.github/skills/punch-debugging-and-error-recovery/SKILL.md`
- **Read-only context paths:** `docs/ai/skill-registry.md`
- **Forbidden paths:** every other `.github/skills/**`, all `.github/prompts/**`,
  `.github/agents/**`, `src/**`, `docker/**`, `docker-compose.yml`, `bin/**`
- **Expected diff size:** 1 line.
- **Validation commands:**
  `grep -n "^name:" .github/skills/punch-debugging-and-error-recovery/SKILL.md`
  must print `name: punch-debugging-and-error-recovery`.
- **Rollback notes:** revert the single-line frontmatter change.
- **Human checkpoint:** required before Build.
- **Build via:** `punch-ai-governance` (self, no engineer hand-off).

### G-02 — Omitted (human decision at approval, 2026-07-21)

Originally: hide background skills from the slash-command menu
(`user-invocable: false` sweep across 23 skills, Spec FR2/AC2). Cut at
approval. Leaves Spec AC2 undelivered by this Plan — see Status note above.

### G-03 — Correct Build's selective-activation language

- **Goal** — Ensure Build documentation states trigger-only activation for
  TDD, source-driven development, debugging, doubt-driven development, and
  context engineering — no eager-loading default (Spec FR3, FR4, AC3).
- **Allowed edit paths:** `.github/prompts/punch-build.prompt.md`,
  `.github/agents/punch-builder.agent.md`,
  `.github/agents/punch-runtime-engineer.agent.md`,
  `.github/agents/punch-performance-test-engineer.agent.md`
- **Read-only context paths:** `docs/ai/skill-registry.md`,
  `docs/ai/scoped-build-policy.md`,
  `.github/skills/punch-incremental-implementation/SKILL.md`
- **Forbidden paths:** `src/**`, `docker/**`, `docker-compose.yml`, `bin/**`,
  every `.github/skills/*/SKILL.md` body (activation triggers are declared in
  the prompt/agent, not rewritten in the skill body)
- **Acceptance details:** each of the four trigger-only skills names its exact
  activation condition (behavioral change/bug proof for TDD; version-sensitive
  framework/API work for source-driven; after a failure for debugging;
  high-risk decision for doubt-driven; new session/task-switch/cross-file
  reasoning for context engineering) in at least one of the edited files —
  no unconditional "always load" phrasing survives for these five.
- **Validation commands:** `git diff --check`; manual read confirming
  `punch-incremental-implementation` remains the only *default* Build method
  named without a trigger condition.
- **Rollback notes:** revert the prompt/agent diff; skill bodies untouched.
- **Human checkpoint:** required before Build.
- **Build via:** `punch-ai-governance` (self).

### G-04 — Narrow a Plan-scoped service-change route

- **Goal** — Give a future Plan a documented, narrowly-scoped path to route
  `src/services/**` work to `punch-runtime-engineer` without widening its
  default read-only treatment (Spec FR5, AC4).
- **Allowed edit paths:** `.github/agents/punch-runtime-engineer.agent.md`,
  `docs/ai/scoped-build-policy.md`
- **Read-only context paths:** `docs/architecture/punch-boundaries.md`,
  `.github/agents/punch-architect.agent.md`
- **Forbidden paths:** `src/services/**` itself, `.github/agents/punch-performance-test-engineer.agent.md`,
  every other agent/prompt file
- **Acceptance details:** the added language is conditional ("only when an
  approved Plan task explicitly names `src/services/**` in its allowed edit
  paths") — default scope for `punch-runtime-engineer` stays read-only for
  services; no blanket widening.
- **Validation commands:** `git diff --check`; confirm no unconditional
  `src/services/**` entry appears under "Allowed" in
  `punch-runtime-engineer.agent.md` — only under a named conditional clause.
- **Rollback notes:** revert; default read-only-for-services behavior resumes
  immediately (no other file depends on this addition).
- **Human checkpoint:** required before Build.
- **Build via:** `punch-ai-governance` (self).

### G-05 — Reconcile delegation depth and the Ship fan-out exception

- **Goal** — Make `punch-code-reviewer` and `punch-security-auditor` state
  their registered `/punch-ship` fan-out permission explicitly, matching
  `punch-test-engineer`'s existing language, while keeping delegation depth at
  1 everywhere (Spec FR6, FR7, AC5, AC6).
- **Allowed edit paths:** `.github/agents/punch-code-reviewer.agent.md`,
  `.github/agents/punch-security-auditor.agent.md`
- **Read-only context paths:** `.github/agents/punch-test-engineer.agent.md`
  (the pattern to match), `.github/agents/punch-release-captain.agent.md`,
  `docs/ai/agent-guards.md`
- **Forbidden paths:** `.github/agents/punch-release-captain.agent.md` itself
  (already correct — do not edit), `.github/agents/punch-cavecrew-*.agent.md`
- **Acceptance details:** each edited file adds one explicit line (matching
  `punch-test-engineer`'s "Invoked by `/punch-<phase>` (and fan-out from
  `/punch-ship`)" pattern) without loosening "verdict is its own, never
  delegated" or the depth-1 cavecrew-worker rule already present in both
  files.
- **Validation commands:**
  `grep -l "punch-ship" .github/agents/punch-code-reviewer.agent.md .github/agents/punch-security-auditor.agent.md`
  must return both files; `git diff --check`.
- **Rollback notes:** revert; each file's existing verdict-ownership language
  is untouched by this addition.
- **Human checkpoint:** required before Build.
- **Build via:** `punch-ai-governance` (self).

### G-06 — Add Ship's evidence-freshness reuse rule

- **Goal** — Stop `/punch-ship` from unconditionally rerunning
  Test/Review/Security when valid evidence for an unchanged diff already
  exists (Spec FR8, AC7) — currently a real behavioral gap, not just wording.
- **Allowed edit paths:** `.github/prompts/punch-ship.prompt.md`,
  `.github/agents/punch-release-captain.agent.md`
- **Read-only context paths:** `docs/workflows/validation.md`,
  `reports/state/punch-run.json` (schema reference only)
- **Forbidden paths:** `.github/agents/punch-test-engineer.agent.md`,
  `.github/agents/punch-code-reviewer.agent.md`,
  `.github/agents/punch-security-auditor.agent.md` (their own verdict-ownership
  text is untouched by this task), `src/**`, `bin/**`
- **Acceptance details:** add an explicit reuse rule — rerun a specialist only
  when its evidence is missing, stale, invalidated by a changed diff, required
  by a sensitive-surface rule, or explicitly requested; otherwise consume the
  existing fresh verdict. GO/NO-GO and rollback-plan requirements stay
  mandatory regardless of reuse.
- **Validation commands:** `git diff --check`; manual read confirming the new
  rule doesn't remove the "any REQUEST CHANGES/FAIL → stop" language.
- **Rollback notes:** revert to the current always-fan-out behavior; no data
  or runtime impact either way.
- **Human checkpoint:** required before Build.
- **Build via:** `punch-ai-governance` (self).

### G-07 — Absorb Observability into Data Harvest; retire the standalone skill

- **Goal** — One canonical owner for structured logs/RED/correlation-ID
  guidance for this didactic runtime, folded into the lean diagnostic
  discipline `punch-data-harvest` already owns (Spec FR9, FR11 row 3, AC8,
  AC9).
- **Allowed edit paths:** `.github/skills/punch-data-harvest/SKILL.md`
  (absorb essential content), `.github/skills/punch-observability-and-instrumentation/SKILL.md`
  (delete), `docs/ai/skill-registry.md` (remove the Lifecycle-skills row and
  the "instrumenting a service" discovery-table row, point it at
  `punch-data-harvest` instead)
- **Read-only context paths:** none beyond the files above.
- **Forbidden paths:** `.github/agents/**`, `.github/prompts/**`, `src/**`,
  `docker/**`
- **Acceptance details:** no essential guidance is lost — anything
  `punch-observability-and-instrumentation` uniquely stated (structured
  service logs, RED read from k6 run, `reports/logs/**` role) is present in
  `punch-data-harvest` before the old file is deleted. Production-style
  service instrumentation stays explicitly deferred, per Spec FR9, until a
  real recurring use case is approved.
- **Validation commands:**
  `grep -rln "punch-observability-and-instrumentation" .github docs --include="*.md" | grep -v docs/specs`
  must return empty after this task; `git diff --check`.
- **Rollback notes:** restore the deleted `SKILL.md` from git history and
  revert the registry/data-harvest edits together (they're one logical
  change).
- **Human checkpoint:** required before Build.
- **Build via:** `punch-ai-governance` (self).

### G-08 — Absorb Code Simplification into Review; absorb Idea Refine into Spec's clarify step

- **Goal** — Retire two lifecycle skills whose guidance already belongs to an
  existing phase owner, per the Spec's disposition table (FR11 rows 1–2,
  AC9).
- **Allowed edit paths:**
  - `.github/skills/punch-code-review-and-quality/SKILL.md` (absorb simplicity
    axis content)
  - `.github/skills/punch-code-simplification/SKILL.md` (delete)
  - `.github/agents/punch-code-reviewer.agent.md` (drop the now-retired skill
    reference in its Skill-activation section)
  - `.github/prompts/punch-review.prompt.md` (drop the reference)
  - `.github/prompts/punch-document.prompt.md` (drop the reference)
  - `.github/skills/punch-spec-driven-development/SKILL.md` (absorb idea-refine
    clarify-step content)
  - `.github/skills/punch-idea-refine/**` (delete directory, including
    `scripts/idea-refine.sh`)
  - `.github/agents/punch-architect.agent.md` (point its clarify step at
    `punch-spec-driven-development` instead of the retired skill)
  - `.github/prompts/punch-spec.prompt.md` (same reference fix)
  - `docs/ai/skill-registry.md` (remove both Lifecycle-skills rows; update the
    "writing a spec" / "reviewing a diff" discovery-table rows)
- **Read-only context paths:** none beyond the files above.
- **Forbidden paths:** `.github/agents/punch-release-captain.agent.md`,
  `.github/skills/punch-using-agent-skills/SKILL.md` (retired in G-09, not
  here — avoid touching twice in one step), `src/**`, `docker/**`
- **Acceptance details:** the "divergent → convergent" idea-refine method and
  the Chesterton's-Fence simplification method both survive, just relocated —
  no content silently dropped. `punch-idea-refine`'s script asset
  (`scripts/idea-refine.sh`) is deleted, not orphaned.
- **Validation commands:**
  `grep -rln "punch-code-simplification\|punch-idea-refine" .github docs --include="*.md" | grep -v docs/specs`
  must return empty; `ls .github/skills/punch-idea-refine 2>&1` must fail;
  `git diff --check`.
- **Rollback notes:** restore both deleted directories from git history and
  revert the seven reference-fix files together.
- **Human checkpoint:** required before Build.
- **Build via:** `punch-ai-governance` (self).

### G-09 — Retire the meta-routing skill

- **Goal** — `docs/ai/skill-registry.md` stays the canonical skill-discovery
  index and `punch-builder` + `agent-guards.md` stay the canonical engineer-
  delegation canon; `punch-using-agent-skills` stops duplicating or
  half-claiming either authority (Spec FR10, FR11 row 4, AC9).
- **Allowed edit paths:** `.github/skills/punch-using-agent-skills/SKILL.md`
  (delete), `.github/prompts/punch-build.prompt.md` (drop its Skill-activation
  reference), `docs/ai/skill-registry.md` (remove the Lifecycle-skills row)
- **Read-only context paths:** `docs/ai/agent-guards.md`,
  `.github/agents/punch-builder.agent.md`
- **Forbidden paths:** historical Plan docs that reference this skill as a
  point-in-time decision record — `docs/specs/plan-context-engineering-preservation.md`,
  `docs/specs/plan-decouple-punch-build-from-caveman.md` — leave untouched
  (frozen record of a prior approved Plan, not an active caller); `src/**`,
  `docker/**`
- **Acceptance details:** any unique, still-true guidance in
  `punch-using-agent-skills` (the skill-discovery decision tree, the
  delegation-roster canon pointer) is already present in
  `docs/ai/skill-registry.md`'s "Skill discovery" table and
  `docs/ai/agent-guards.md` respectively before deletion — confirm, don't
  duplicate.
- **Validation commands:**
  `grep -rln "punch-using-agent-skills" .github docs --include="*.md" | grep -v docs/specs`
  must return empty; `git diff --check`.
- **Rollback notes:** restore the deleted file and revert the two reference
  edits together.
- **Human checkpoint:** required before Build.
- **Build via:** `punch-ai-governance` (self).

### G-10 — Reproducible provenance and disposition manifest

- **Goal** — One tracked, static record mapping the pinned upstream commit to
  every one of the 24 source skills, the 3 adopted upstream personas
  (`code-reviewer`, `security-auditor`, `test-engineer`), and the Punch-native
  `punch-release-captain` wrapper — each with an explicit disposition (Spec
  FR12, FR13, AC11).
- **Allowed edit paths:** new file `docs/ai/agent-skills-provenance.md`,
  `docs/ai/skill-registry.md` (add one pointer line to the new manifest from
  the "Adopted upstream skills" section intro)
- **Read-only context paths:** `.ai-upstream/agent-skills/**` (local staging
  snapshot, read for the mapping — never edited), the four upstream/VS Code
  source URLs already cited in the Spec.
- **Forbidden paths:** `.ai-upstream/**` (no writes — gitignored local
  staging stays user-refreshed only), every `.github/**` file, `src/**`,
  `docker/**`
- **Acceptance details:** manifest columns — upstream repo URL, pinned commit
  (`2fbfa004a0192529bc997d103fc12f19a3804aab`), adoption date, mapped Punch
  asset (or "unadopted"/"deferred"), disposition
  (adopted / already-covered / irrelevant-to-Punch / superseded-by-Punch /
  deferred), checksum or byte-diff verdict vs the pinned commit. All 24 source
  skills covered, including the 6 kept-unadopted and the 4 absorbed-then-
  retired (G-07/G-08/G-09) marked `superseded-by-Punch`, not silently dropped.
  `punch-release-captain` is recorded explicitly as a **native wrapper around
  the vendor `/ship` fan-out pattern**, not a direct upstream `release-captain`
  persona adoption — matching the Spec's own baseline-evidence note. No
  automatic-fetch script, cache, or CI step is added alongside the manifest.
- **Validation commands:** manual row-count check (24 skill rows + 3 persona
  rows + 1 release-captain row = 28); `git diff --check`; confirm the file is
  plain Markdown with no executable content.
- **Rollback notes:** delete the new file and revert the one registry pointer
  line; nothing else depends on it yet.
- **Human checkpoint:** required before Build.
- **Build via:** `punch-ai-governance` (self).

### G-11 — Reconcile lifecycle documentation

- **Goal** — `AGENTS.md`, `docs/ai/skill-registry.md`,
  `docs/ai/prompt-registry.md`, prompts, agents, and `agent-guards.md` agree on
  six phases, eight prompts, the post-G-07/08/09 live skill inventory,
  `punch-release-captain`'s true provenance, and the delegation-depth setting
  (Spec FR14, AC12). Runs **after** G-07/G-08/G-09 so the registry rows it
  checks are already final.
- **Allowed edit paths:** `AGENTS.md`, `docs/ai/prompt-registry.md`,
  `docs/ai/skill-registry.md` (final consistency pass only — row removals
  already done in earlier tasks), `.github/copilot-instructions.md`
  (lifecycle table only)
- **Read-only context paths:** every file touched by G-01 through G-10 (for
  cross-reference confirmation), `docs/ai/agent-guards.md`
- **Forbidden paths:** `docs/specs/**` (historical/approved Spec and Plan docs
  stay frozen), `src/**`, `docker/**`, `.github/prompts/*.prompt.md` bodies
  beyond the phase-table row itself
- **Acceptance details:**
  - `AGENTS.md:54` reads `Spec → Plan → Build → Test → Review → Ship`.
  - `AGENTS.md:96` reads "8 prompts: spec, plan, build, test, review, ship,
    document, init" (drop the stray `verify`).
  - No file states or implies a separate Verify prompt/phase.
  - `docs/ai/skill-registry.md` contains no row for any skill deleted in
    G-07/G-08/G-09.
  - `chat.subagents.allowInvocationsFromSubagents` is stated as false/default
    consistently everywhere it's mentioned.
- **Validation commands:**
  `grep -rn "Verify\b" AGENTS.md` returns no phase-name usage (verb usage like
  "Verify through Punch official commands" is fine — only the phase-name
  usage is in scope); `grep -c "prompt" docs/ai/prompt-registry.md` sanity
  check against 8 rows; `git diff --check`.
- **Rollback notes:** revert the four-file diff; no functional/runtime
  behavior depends on it.
- **Human checkpoint:** required before Build.
- **Build via:** `punch-ai-governance` (self).

### G-12 — Final governance and runtime verification

- **Goal** — Close the Plan with a clean read-only governance audit and an
  unchanged official runtime verification (Spec AC14, AC15).
- **Allowed edit paths:** `reports/state/punch-run.json`, `reports/**`
  (generated verification artifacts only)
- **Read-only context paths:** every file touched by G-01 through G-11.
- **Forbidden paths:** all of `.github/**` and `docs/**` (no further edits
  once G-11 lands, unless verification finds a documented defect and this
  Plan is reopened), `src/**`, `docker/**`, `docker-compose.yml`, `bin/**`
- **Verification scenarios:**

  | Scenario | Expected result |
  |---|---|
  | `punch-ai-governance` full audit procedure re-run | Verdict: "Governance is clean" |
  | `./bin/punch doctor` | Passes |
  | `./bin/punch run smoke` | Passes; `reports/state/punch-run.json` `passed: true` |

- **Validation commands:**
  ```bash
  ./bin/punch doctor
  ./bin/punch run smoke
  git diff --check
  ```
- **Rollback notes:** if the audit returns drift or runtime verification
  regresses, reopen this Plan at the failing task ID rather than patching
  ad hoc.
- **Expected diff size:** no intentional diff beyond generated reports.
- **Human checkpoint:** review final diff and verification evidence before
  `/punch-ship`.
- **Build via:** `punch-ai-governance` (self) + Test evidence.

## Order of execution

1. G-01 (identity fix — cheap, foundational)
2. G-03 (Build activation language) — G-02 omitted, skip
3. G-04 (service-change route)
4. G-05 (delegation/Ship-exception wording)
5. G-06 (Ship evidence-freshness behavior)
6. G-07 (observability → data-harvest)
7. G-08 (code-simplification + idea-refine absorption)
8. G-09 (using-agent-skills retirement)
9. G-10 (provenance manifest — reflects the final adopted/retired set from
   G-07–G-09)
10. G-11 (lifecycle documentation reconciliation — depends on G-07–G-10 being
    final)
11. G-12 (closing governance + runtime verification gate)

Each task is independently revertible; later tasks depend on earlier ones
landing (G-10/G-11/G-12 explicitly read the post-absorption state), so this
order is not arbitrary — do not reorder without re-checking those
dependencies.

## Cross-cutting risks

- **Missed cross-reference on delete (G-07/G-08/G-09).** Each deletion task's
  validation grep is scoped to catch stragglers; if any later task's grep
  finds a leftover reference, stop and fix it in that same task rather than
  deferring to G-11.
- **Historical-doc overreach.** Prior approved Plan docs
  (`docs/specs/plan-*.md`) and the approved Spec itself are frozen references
  — no task may edit them to "clean up" a since-retired skill name; only
  `docs/ai/skill-registry.md` and other *active* canon get updated.
- **Provenance drift claim (from Spec).** The Spec's per-commit table
  (20/24 at `a5f0b17`, four later, 13 differing from head `2fbfa00`) was
  flagged unverified at Spec approval. G-10 should record it as-is with a
  "not independently re-verified against live GitHub" note rather than
  re-asserting it as confirmed.
- **Self-execution, no engineer hand-off.** Every task here stays inside
  `punch-ai-governance`'s own admin scope — if any task is found mid-Build to
  require touching `src/**`/`docker/**`/`bin/**` beyond the read-only context
  already listed, stop and return to this Plan; do not silently widen scope
  or hand off to `punch-builder`.
- **No new runtime dependency.** None of G-01–G-12 adds npm, pip, k6, MCP,
  hook, watcher, or automatic network/fetch behavior — G-10's manifest is
  static Markdown only.

## Rollback plan

Revert in reverse order: G-12, G-11, G-10, G-09, G-08, G-07, G-06, G-05, G-04,
G-03, G-01 (G-02 omitted). Because G-10/G-11 depend on the absorption tasks, reverting
out of order (e.g. G-08 alone after G-11 has landed) will reintroduce a
registry/reality mismatch — revert contiguously from the top of the stack
down to the task being undone.

**Gate:** approved when human confirms → Build proceeds task-by-task, each
requiring its own human checkpoint before `punch-ai-governance` executes it.
