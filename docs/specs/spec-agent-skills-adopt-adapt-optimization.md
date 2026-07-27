# Spec — Agent Skills adopt-adapt reliability and efficiency

> **Status:** Approved (`punch-ai-governance` Spec-phase audit, 2026-07-21)
> **Location:** Saved in `docs/specs/`, the repository's active Spec/Plan
> convention; `docs/architecture/specs/` named by the older template does not
> exist.
> **AI Governance audit note:** skill/prompt counts (25 skills, 8 prompts),
> the 24-upstream / 6-unadopted / 18-adapted split, the 2,384 vs 5,065 line
> total (52.9% reduction), and the sole `punch-debugging-and-error-recovery`
> frontmatter `name` mismatch were verified against the live repo and
> `.ai-upstream/agent-skills` snapshot — all exact. The per-file commit
> provenance table (20/24 at `a5f0b17`, four later, 13 differing from head
> `2fbfa00`) could not be verified against local state alone (requires a live
> GitHub compare) — carry it into Plan as evidence to (re)fetch, not a Spec
> blocker.

- **Goal** — Make Punch's adopted/adapted Agent Skills and personas reliably
  discoverable, selectively loaded, executable within declared agent boundaries,
  source-traceable, and demonstrably worth their maintenance cost without
  changing Punch runtime behavior.

- **Non-goals**
  - Do not implement the governance/configuration changes in this Spec; an
    approved Plan with scoped task IDs is required first.
  - Do not change `src/**`, `bin/**`, `docker/**`, `docker-compose.yml`, k6
    behavior, service behavior, workflows, or runtime report schemas.
  - Do not blindly synchronize generic upstream text into Punch adaptations.
    Upstream changes must be reviewed and dispositioned against Punch's actual
    Docker/k6/Postgres surfaces.
  - Do not adopt the currently excluded upstream API/interface, CI/CD,
    migration, frontend, interview, or shipping-and-launch skills merely to
    increase parity.
  - Do not add another Build engineer, lifecycle phase, prompt, or generic
    router unless a later Plan proves that the two-engineer model cannot safely
    absorb the required responsibility.
  - Do not enable recursive/nested subagents, automatic upstream fetching,
    host-side package installation, or new runtime dependencies.
  - Do not alter the native Caveman, Cavecrew, or Graphify skill bodies as part
    of this work.

- **Baseline evidence**
  - The upstream Addy Osmani inventory contains 24 skills. Punch currently maps
    18 as `punch-`-prefixed adaptations and deliberately leaves six unadopted.
  - The 18 adapted Punch skill bodies contain 2,384 lines versus 5,065 lines in
    their local upstream baselines, a 52.9% reduction.
  - `.github/skills/` currently exposes 25 project skills to the slash-command
    menu by default, in addition to eight Punch prompt entry points.
  - `punch-debugging-and-error-recovery/SKILL.md` declares an unprefixed `name`
    that does not match its parent directory and therefore is not reliably
    discoverable by VS Code.
  - The local `.ai-upstream/agent-skills/` snapshot is not a single pinned
    revision: 20 of 24 skill files match upstream commit `a5f0b17`, four are
    later, and 13 differ from the audited current upstream head.
  - The upstream `code-reviewer`, `security-auditor`, and `test-engineer`
    persona baselines match the audited current upstream files. Punch's
    `punch-release-captain` is a native wrapper around the upstream `/ship`
    fan-out pattern, not an upstream `release-captain` persona.

- **Functional requirements**
  1. **Host-compatible skill identity.** Every retained project skill's
     frontmatter `name` must exactly match its parent directory and satisfy the
     current VS Code Agent Skills naming contract. Every adapted source skill
     remains `punch-`-prefixed; native upstream skills retain their native name.
  2. **One public lifecycle interface.** Punch prompts remain the normal
     user-facing phase entry points. Background domain and lifecycle skills are
     hidden from the slash-command menu with `user-invocable: false` while
     remaining available for model invocation when relevant. Explicit manual
     tool skills such as Caveman and Graphify retain their existing invocation
     controls.
  3. **Selective activation.** A phase activates one primary lifecycle method
     plus the relevant Punch domain skill. Build must not eagerly load TDD,
     source-driven development, debugging, doubt-driven development, or the
     context primer when their documented trigger is absent.
  4. **Build activation rules.** `punch-incremental-implementation` remains the
     Build method. TDD activates only for behavioral changes or bug proof;
     source-driven development only for version-sensitive framework/API work;
     debugging only after a failure; doubt-driven development only for
     high-risk decisions; context engineering only for a new session, task
     switch, or cross-file/repository reasoning.
  5. **Service-change capability.** A Plan-scoped Build route must exist for
     future changes under `src/services/**` required by performance,
     observability, browser diagnosis, or security findings. Prefer a narrowly
     expanded `punch-runtime-engineer` service-task boundary over a new persona.
     Default read-only treatment remains for unrelated tasks, and a Plan may
     never widen the route implicitly.
  6. **Consistent delegation depth.** `chat.subagents.allowInvocationsFromSubagents`
     remains false/default. Top-level Review, Test, and Security coordinators may
     use their registered read-only Cavecrew workers; when those specialists run
     under Ship they are report-only leaves and cannot nest further.
  7. **Explicit Ship exception.** The test, review, and security personas may be
     invoked directly by their phase prompt and by the registered
     `punch-release-captain` fan-out. Their instructions must not simultaneously
     forbid that registered Ship invocation.
  8. **No duplicate gates.** Ship consumes fresh, unchanged Test and Review
     reports when available. It reruns a specialist only when evidence is
     missing, stale, invalidated by a changed diff, required by a sensitive
     surface, or explicitly requested. A rollback plan and final GO/NO-GO remain
     mandatory.
  9. **Single observability contract.** The active guidance must make one
     unambiguous choice about structured service logs, correlation IDs, RED
     signals, and the role of `reports/logs/**`. For the current didactic
     runtime, absorb the lean diagnostic discipline into `punch-data-harvest`
     and defer production-style service instrumentation until a real recurring
     service use case is approved.
  10. **Remove redundant meta-routing.** Skill discovery remains canonical in
      `docs/ai/skill-registry.md`; engineer delegation remains canonical in
      `punch-builder` plus `agent-guards.md`. Retire or reduce
      `punch-using-agent-skills` so it does not duplicate both or claim authority
      it does not hold.
  11. **Right-sized adopted set.** Preserve the distinct methods that directly
      support Punch; merge methods already covered by a phase owner; defer
      capabilities with no executable surface. Essential retained guidance must
      be linked or absorbed before any redundant skill is removed.
  12. **Reproducible provenance.** Track the upstream repository URL, exact
      commit, adoption date, mapped Punch asset, and checksum/disposition for
      each adopted skill and persona. `.ai-upstream/**` remains gitignored local
      staging, manually refreshed, and never becomes runtime or automatic-fetch
      infrastructure.
  13. **Selective upstream review.** Record each upstream change as adopted,
      already-covered, irrelevant-to-Punch, superseded-by-Punch, or deferred.
      Current upstream drift is a review input, not an automatic failure and not
      authorization to overwrite a Punch adaptation.
  14. **Accurate lifecycle documentation.** `AGENTS.md`, registries, prompts,
      agents, guards, and ADR links must agree on Test versus Verify, prompt and
      skill inventories, invocation defaults, delegation depth, and the true
      provenance of `punch-release-captain`.

- **Adopted-skill disposition**

  | Decision | Skills |
  |---|---|
  | Retain | `punch-spec-driven-development`, `punch-planning-and-task-breakdown`, `punch-incremental-implementation`, `punch-test-driven-development`, `punch-debugging-and-error-recovery`, `punch-code-review-and-quality`, `punch-git-workflow-and-versioning`, `punch-documentation-and-adrs`, `punch-security-and-hardening`, `punch-source-driven-development` |
  | Retain, trigger-only | `punch-context-engineering`, `punch-doubt-driven-development`, `punch-performance-optimization` |
  | Absorb then retire | `punch-code-simplification` into Review; `punch-idea-refine` into the Spec clarify step; `punch-observability-and-instrumentation` into data-harvest's lean diagnostic rules; `punch-using-agent-skills` into the registry/builder canons |
  | Defer until executable | `punch-browser-testing-with-devtools` until a Plan enables a browser-capable image, Compose service, test, and evidence path |
  | Keep unadopted | `api-and-interface-design`, `ci-cd-and-automation`, `deprecation-and-migration`, `frontend-ui-engineering`, `interview-me`, `shipping-and-launch` |

- **Technical constraints**
  - GitHub Copilot/VS Code remains the primary host and `.github/**` remains the
    canonical AI configuration surface.
  - Use current official VS Code documentation for skill identity, invocation,
    and subagent behavior; use the pinned Addy Osmani commit for source parity.
  - Keep Python orchestration stdlib-only and Docker-first. This work adds no
    npm, pip, k6, MCP, hook, watcher, or automatic network requirement.
  - Preserve Spec → Plan → Build → Test → Review → Ship, human approval before
    Build, scoped allowed/read-only/forbidden paths, and human-only merge.
  - Preserve `reports/state/punch-run.json` as the verification record and do
    not weaken existing k6 checks or thresholds.
  - Prefer deletion, absorption, and cross-links over new assets or duplicated
    rules. Every retained skill must name a unique recurring decision or method.
  - Implementation must use governance-owned, reviewable steps and must not
    edit `.ai-upstream/**` to make parity appear clean.

- **Source constraints**
  - Audited upstream Agent Skills head:
    <https://github.com/addyosmani/agent-skills/commit/2fbfa004a0192529bc997d103fc12f19a3804aab>
  - Audited upstream release 0.6.4:
    <https://github.com/addyosmani/agent-skills/releases/tag/0.6.4>
  - VS Code Agent Skills identity, access, and progressive loading:
    <https://code.visualstudio.com/docs/agent-customization/agent-skills>
  - VS Code subagent nesting and `agents:` behavior:
    <https://code.visualstudio.com/docs/agents/subagents>

- **Affected layers**
  - AI configuration: authored Punch skills, phase prompts, custom agents,
    always-on Copilot instructions, and invocation metadata.
  - AI governance: skill/prompt registries, delegation guards, provenance and
    parity procedure, link/frontmatter validation, and lifecycle documentation.
  - Build authorization model: configuration-only correction of the future
    `src/services/**` ownership route; no service code changes in this work.
  - Product runtime, Compose runtime, k6 suite, CI workflows, and data/report
    schemas: unaffected.

- **Artifact / log / reporting implications**
  - No runtime artifact path, schema, threshold, terminal-output contract, or
    service log format changes as part of this configuration work.
  - Add one tracked, static upstream provenance/disposition record; do not add a
    generated cache or automatic downloader.
  - Existing verification remains authoritative. Any runtime verification run
    must update `reports/state/punch-run.json` and record `passed: true` before
    the change advances to Review.

- **Acceptance criteria**
  1. Every retained `.github/skills/*/SKILL.md` declares a valid `name` exactly
     matching its parent directory; `punch-debugging-and-error-recovery` loads
     under its prefixed identity.
  2. Background Punch skills declare `user-invocable: false`; the normal slash
     menu exposes the eight Punch phase/maintenance prompts plus only explicitly
     approved manual tool skills.
  3. Build documentation and agents agree on one primary Build method, one
     selected domain, and trigger-only activation for TDD, source, debugging,
     doubt, and context guidance.
  4. An approved, explicitly service-scoped Plan task can be routed to an
     authorized existing Build engineer without weakening unrelated task
     boundaries or adding a third engineer.
  5. All live AI configuration agrees that recursive subagents are disabled;
     Review/Test/Security may use Cavecrew only when top-level, and Ship's three
     specialist children cannot spawn grandchildren.
  6. `punch-test-engineer`, `punch-code-reviewer`, and
     `punch-security-auditor` explicitly permit their registered Ship fan-out
     while retaining their own verdict ownership and read-only/no-fix rules.
  7. Ship reuses valid Test/Review evidence for an unchanged diff and reruns only
     the specialists required by the freshness/sensitivity rules; GO/NO-GO and
     rollback remain mandatory.
  8. No contradictory observability scope remains between data-harvest and a
     standalone method; essential current diagnostic rules survive in one
     canonical owner.
  9. `punch-using-agent-skills`, `punch-code-simplification`,
     `punch-idea-refine`, and `punch-observability-and-instrumentation` are
     removed only after their retained Punch-specific guidance is absorbed or
     linked by the named canonical owner.
  10. Browser testing is absent from the active skill set until the executable
      browser prerequisites are approved; its source remains available through
      provenance and the existing deferred example.
  11. A tracked manifest pins one upstream commit and maps all 24 source skills,
      the three adopted upstream personas, and the Punch-native Ship wrapper to
      an explicit disposition with no unmapped asset.
  12. `AGENTS.md`, `skill-registry.md`, `prompt-registry.md`, prompts, agents,
      and `agent-guards.md` agree on the six phases, eight prompts, live skill
      inventory, source attribution, and delegation setting.
  13. Authored AI-config frontmatter and registry-to-disk parity are clean; no
      adapted-in-place source skill, orphaned asset, or broken local Markdown
      link remains.
  14. `git diff --check` passes and a read-only `punch-ai-governance` review
      returns **Governance is clean** for the implemented scope.
  15. Official runtime verification remains unchanged: `./bin/punch doctor` and
      `./bin/punch run smoke` pass when run by Test, and
      `reports/state/punch-run.json` records `passed: true`.

**Gate:** approved when Goal, Non-goals, Functional requirements, adopted-skill
disposition, and Acceptance criteria are agreed. An approved `/punch-plan` with
allowed/read-only/forbidden paths is required before any AI-configuration change.
