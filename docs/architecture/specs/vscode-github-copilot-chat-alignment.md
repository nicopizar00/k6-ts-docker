# Spec — VS Code GitHub Copilot Chat configuration alignment

> **Status:** Approved 2026-07-30 by Nicolás Pizarro, after a repo-state +
> upstream-commit audit of all baseline evidence, source pins, and Plan task
> paths. Four precision fixes applied pre-approval (lifecycle-drift wording,
> Caveman version sourcing, `docs/ai/history/**` dangling-path note, VC-16
> validation-regex scoping). Implementation requires the accompanying approved
> Plan and each task's own human checkpoint.
> **Source audit date:** 2026-07-30.
> **Scope interpretation:** “Agents config” outside GitHub Copilot means the
> repository-root `AGENTS.md` file and `.agents/**`. GitHub Copilot custom
> agents under `.github/agents/**` remain in scope because they are native
> VS Code Chat assets.

- **Goal** — Make the repository’s VS Code GitHub Copilot Chat behavior
  deterministic, internally consistent, and source-pinned by discovering only
  the intended `.github/**` project customizations while leaving every
  Claude-specific and generic Agents configuration untouched.

- **Assumptions**
  - The target host is current VS Code Stable with GitHub Copilot Chat.
  - Repository-owned Copilot customizations are:
    `.github/copilot-instructions.md`, `.github/instructions/**`,
    `.github/prompts/**`, `.github/agents/**`, and `.github/skills/**`.
  - `.vscode/settings.json` may define the repository’s VS Code customization
    discovery boundary.
  - `CLAUDE.md`, `.claude/**`, `AGENTS.md`, and `.agents/**` may remain for
    other hosts, but VS Code Copilot Chat must not load them in this workspace.
  - User-profile and organization-provided GitHub Copilot policy remains under
    the user’s or organization’s control. This work governs repository-local
    discovery and does not claim to suppress centrally managed policy or
    extension-contributed assets.

- **Non-goals**
  - Do not edit, move, delete, mirror, or reconcile `CLAUDE.md`, `.claude/**`,
    `AGENTS.md`, or `.agents/**`.
  - Do not make Claude Code, generic Agents hosts, Codex, Copilot CLI, or the
    GitHub Copilot cloud coding agent consume Punch assets.
  - Do not fix or otherwise change
    `.github/workflows/copilot-setup-steps.yml`,
    `.github/copilot-setup-steps.yml`, or any other workflow. Those files serve
    the Copilot cloud-agent/Actions surface, not VS Code Chat.
  - Do not change `src/**`, `bin/**`, `docker/**`, `docker-compose.yml`,
    `package.json`, k6 tests, services, report schemas, or runtime behavior.
  - Do not edit `.ai-upstream/**`; it remains gitignored, local staging rather
    than active VS Code configuration.
  - Do not install or run Graphify, Caveman, hooks, watchers, MCP servers,
    plugins, or external graph databases as part of this work.
  - Do not build or refresh `graphify-out/**`.
  - Do not move or rewrite historical Spec/Plan artifacts under `docs/specs/**`
    or historical records under `docs/ai/history/**`.
  - Do not automatically overwrite Punch-adapted Addy Osmani skills with
    upstream text. Every upstream change needs an explicit disposition.

- **Baseline evidence**
  - The repository has no `.vscode/settings.json`, so VS Code’s default
    discovery behavior currently applies.
  - Current VS Code documentation states that repository `AGENTS.md` and
    `CLAUDE.md` files are always-on by default, and that multiple instruction
    sources are combined without guaranteed ordering.
  - Current VS Code project-skill discovery recognizes `.github/skills/**`,
    `.claude/skills/**`, and `.agents/skills/**`; the vendor Cavecrew skill
    under `.agents/skills/cavecrew/**` is therefore discoverable unless the
    workspace explicitly excludes it.
  - The active GitHub Copilot layout is structurally healthy: prompt-to-agent
    bindings, skill directory names, and required frontmatter fields validate.
  - Lifecycle text has drifted in five specific, narrow spots, not across the
    lifecycle hub: `.github/prompts/punch-review.prompt.md:3` labels itself
    "Phase 6 — Review" and `.github/prompts/punch-ship.prompt.md:3` labels
    itself "Phase 7 — Ship" (both retired seven-phase numbers);
    `.github/prompts/punch-plan.prompt.md:39`,
    `.github/skills/punch-spec-driven-development/SKILL.md:141`, and
    `.github/skills/punch-planning-and-task-breakdown/SKILL.md:16,95` still
    route to "the `punch-build-*` prompt" (a retired multi-prompt glob, not
    today's single `punch-build`). `.github/copilot-instructions.md` is
    already six-phase and Define-absorbed. Separately, a Build method
    (`.github/skills/punch-incremental-implementation/SKILL.md:14-17,51`)
    incorrectly says builders have no terminal and run no checks.
  - Artifact instructions still target nonexistent `docs/validation/**`;
    the real validation document is `docs/workflows/validation.md`.
  - The Addy Osmani provenance manifest records release `0.6.4` and a
    mixed-revision local staging set rather than one reproducible stable pin.
  - The committed Graphify skill is version `0.8.41`; the reviewed current
    stable release is `v0.9.30`.
  - The committed Caveman skill derives from the old `0.1.0` snapshot
    (sourced: commit `1d6e042`, 2026-06-18, "adopt Caveman as a Build-only
    prose-compression adapter", pristine upstream marker
    `.ai-upstream/caveman/.caveman_version` = `0.1.0`; the live
    `.github/skills/caveman/SKILL.md` carries no version marker of its own)
    and claims approximately 75% savings; the reviewed `v1.9.1` release
    reports a measured 65% average output-token reduction.

- **Functional requirements**
  1. **Explicit VS Code discovery boundary.** Add workspace settings that keep
     GitHub Copilot Chat enabled while selecting `.github/instructions`,
     `.github/prompts`, `.github/agents`, and `.github/skills` as the only
     repository-local customization roots.
  2. **Dismiss external-host instructions.** Set `chat.useAgentsMdFile`,
     `chat.useNestedAgentsMdFiles`, and `chat.useClaudeMdFile` to `false` for
     this workspace. Disable `.claude/**` and `.agents/**` entries in the
     corresponding instruction, custom-agent, and Agent Skills location maps.
  3. **No parent-repository bleed-through.** Keep
     `chat.useCustomizationsInParentRepositories` disabled so opening this
     repository does not import parent-folder customizations.
  4. **One always-on repository hub.** `.github/copilot-instructions.md` is the
     only repository-owned always-on Copilot instruction source. Detailed rules
     remain path-scoped under `.github/instructions/**` and are linked rather
     than duplicated.
  5. **Copilot-native asset taxonomy.** Live governance and `/punch-init`
     certify only `.github` instructions, prompts, custom agents, and skills,
     plus the `.vscode/settings.json` discovery guard. They must not require,
     certify, mirror, or invoke `AGENTS.md`, `CLAUDE.md`, `.agents/**`, or
     `.claude/**`.
  6. **Retain GitHub Copilot custom agents.** `.github/agents/**`, including
     the optional `punch-cavecrew-*` read-only workers, remains a Copilot-native
     surface. Those workers must be self-contained and must not depend on the
     vendor `.agents/skills/cavecrew` skill being loaded.
  7. **Chat-only export template.** `.github/assets/**` must export only VS Code
     GitHub Copilot Chat assets. Resolver stubs for `AGENTS.md` and `CLAUDE.md`
     must be removed after active template links no longer require them.
  8. **Six-phase lifecycle alignment.** Every active prompt, agent, skill, and
     live AI document must agree on:
     `Spec → Plan → Build → Test → Review → Ship`; Review is phase 5, Ship is
     phase 6, Spec absorbs Define, and Build has one `punch-build` prompt.
  9. **Build/Test responsibility alignment.** Builders and engineers may run
     scoped checks during implementation; `punch-test` remains the independent
     final verdict owner. No active method may claim builders lack terminal
     access or never run commands.
  10. **Reference integrity.** Every active `.github` cross-reference and every
      registry link must resolve. Artifact guidance must target
      `docs/workflows/validation.md`; broken relocated-skill links must be
      removed or corrected.
  11. **Stable Addy Osmani source pin.** Pin the reviewed stable Agent Skills
      release `0.6.5` at commit
      `ff2df4c07e7836a092ed28e1e9b42f4d6009280c`. Record a disposition for each
      upstream change relative to the Punch adaptation. Adopt only improvements
      that preserve Punch’s fixed command and evidence contracts.
  12. **Current Graphify VS Code skill.** Refresh the explicit-only Graphify
      project skill from stable `v0.9.30` at commit
      `ecfcd160d56b420eb8241430fa7b5b1951c7829f`, using the upstream VS Code
      variant and matching references. Preserve only the two approved Punch
      frontmatter additions: `user-invocable: true` and
      `disable-model-invocation: true`.
  13. **Current Caveman skill.** Refresh the manual-only Caveman project skill
      from stable `v1.9.1` at commit
      `0d95a81d35a9f2d123a5e9430d1cfc43d55f1bb0`. Preserve only the two approved
      invocation-control fields and use the upstream measured 65% claim.
  14. **No automatic external-tool behavior.** Graphify and Caveman remain
      explicit slash commands. No Punch prompt, agent, or skill invokes them
      automatically, pre-approves terminal use, or enables their optional
      hooks/integrations.
  15. **Reproducible provenance.** Tracked AI documentation must name each
      upstream repository, release tag, immutable commit, adopted file variant,
      Punch additions, and reviewed disposition. A moving branch or mixed local
      snapshot is not an acceptable pin.
  16. **Governance-owned implementation.** The user-direct
      `punch-ai-governance` agent owns these configuration changes. Its declared
      scope must be expanded narrowly to `.vscode/settings.json`; no product
      builder or runtime engineer receives `.vscode/**` or AI-governance scope.

- **Technical constraints**
  - Use only settings documented by the current official VS Code AI settings,
    custom instructions, prompt files, custom agents, and Agent Skills
    references.
  - Keep `github.copilot.chat.codeGeneration.useInstructionFiles`,
    `chat.includeApplyingInstructions`, `chat.useAgentSkills`, and the intended
    `.github` location entries enabled.
  - Do not claim workspace settings can override organization-managed policy,
    extension-contributed customizations, or a user’s global Copilot policy.
  - Do not add host npm, pip, k6, Graphify, Caveman, or other dependency
    requirements. JSON and Markdown validation use existing VS Code facilities,
    shell text checks, and Python 3 stdlib only.
  - Preserve project-skill directory/name parity and current VS Code
    frontmatter contracts.
  - Imported upstream skill bodies remain source-reviewable. Punch-specific
    behavior belongs in `.github/copilot-instructions.md` or a `punch-*`
    adaptation, not as undocumented edits to a native upstream skill.
  - Third-party upstream references may mention other hosts as upstream
    material, but no Punch-authored asset may treat those hosts or their files
    as canonical, required, automatically invoked, or part of readiness.
  - Keep each implementation step within the approved Plan task’s allowed
    paths and the governance agent’s three-file logical-step guard.
  - Historical ADR statements remain historical. If current behavior changes,
    append a superseding note rather than rewriting the original decision.

- **Source constraints**
  - VS Code AI settings:
    <https://code.visualstudio.com/docs/agents/reference/ai-settings>
  - VS Code custom instructions:
    <https://code.visualstudio.com/docs/agent-customization/custom-instructions>
  - VS Code prompt files:
    <https://code.visualstudio.com/docs/agent-customization/prompt-files>
  - VS Code custom agents:
    <https://code.visualstudio.com/docs/agent-customization/custom-agents>
  - VS Code Agent Skills:
    <https://code.visualstudio.com/docs/agent-customization/agent-skills>
  - Addy Osmani Agent Skills `0.6.5`:
    <https://github.com/addyosmani/agent-skills/releases/tag/0.6.5>
  - Graphify `v0.9.30`:
    <https://github.com/Graphify-Labs/graphify/releases/tag/v0.9.30>
  - Caveman `v1.9.1`:
    <https://github.com/JuliusBrussee/caveman/releases/tag/v1.9.1>

- **Affected layers**
  - VS Code workspace configuration: one repository
    `.vscode/settings.json` discovery policy.
  - GitHub Copilot Chat configuration:
    `.github/copilot-instructions.md`, instructions, prompts, custom agents,
    project skills, and export assets.
  - AI governance documentation: live registries, operating-model documents,
    source provenance, and current decision appendices.
  - Punch product/runtime, Docker Compose, services, k6 tests, CI workflows,
    and runtime artifacts: unaffected.

- **Artifact / log / reporting implications**
  - Add one tracked VS Code workspace settings file and update tracked
    Markdown-based Copilot assets.
  - No runtime artifact, log, threshold, report path, or
    `reports/state/punch-run.json` schema changes.
  - No Punch runtime run is required to prove Chat customization discovery.
    Validation evidence is JSON parsing, frontmatter/link checks,
    `git diff --check`, and the VS Code Agent Customizations diagnostics view.

- **Acceptance criteria**
  1. `.vscode/settings.json` is valid JSON and explicitly disables
     `AGENTS.md`, nested `AGENTS.md`, and `CLAUDE.md` discovery.
  2. Workspace location maps enable the four `.github` customization roots and
     disable repository/user Claude and generic Agents roots without disabling
     GitHub Copilot Chat itself.
  3. VS Code’s Agent Customizations diagnostics shows no repository
     instruction, prompt, custom-agent, or skill source under `.claude/**` or
     `.agents/**`; `.agents/skills/cavecrew/SKILL.md` is not loaded.
  4. `AGENTS.md`, `.agents/**`, `CLAUDE.md`, and `.claude/**` have no diff.
  5. `.github/copilot-instructions.md` is the sole repository-owned always-on
     Chat hub, with path-specific detail under `.github/instructions/**`.
  6. `/punch-init` grades only VS Code GitHub Copilot Chat assets and no longer
     treats a vendor Cavecrew skill or external-host config as a capability,
     prerequisite, resolver target, or canon.
  7. `.github/assets/**` contains no `AGENTS.md` or `CLAUDE.md` resolver stub
     and no template requirement to create either file.
  8. All eight Punch prompts bind existing `.github/agents` custom agents and
     all prompt/agent/skill frontmatter satisfies the current VS Code contract.
  9. No active asset mentions five `punch-build-*` prompts, a seven-phase
     lifecycle, Review as phase 6, Ship as phase 7, or a separate Define/Verify
     phase.
  10. Build guidance consistently permits scoped implementation checks and
      reserves the independent PASS/FAIL verdict for `punch-test`.
  11. All active artifact/reporting scopes point at the real validation
      document, and all active local Markdown links resolve.
  12. The Addy Osmani provenance record pins `0.6.5` and its immutable commit,
      with every changed source skill classified against the Punch adaptation.
  13. Graphify reports version `0.9.30`; its committed VS Code skill and
      references match the reviewed upstream release except for the two
      approved invocation-control fields.
  14. Caveman matches the reviewed `v1.9.1` skill body except for the two
      approved invocation-control fields, states 65% rather than approximately
      75%, and has no broken relocated README link.
  15. Graphify and Caveman remain user-invocable and model-invocation-disabled;
      no Punch lifecycle prompt automatically invokes either skill.
  16. Active registries match files on disk and contain no active
      `.agents/skills/cavecrew` project-skill entry.
  17. No file under `.github/workflows/**`, `src/**`, `bin/**`, `docker/**`,
      `reports/**`, `graphify-out/**`, `.ai-upstream/**`, or the dismissed
      external-host configuration surfaces changes.
  18. `git diff --check`, JSON validation, frontmatter validation, active-link
      validation, and a read-only `punch-ai-governance` audit pass.

**Gate:** approved when the Goal, scope interpretation, Non-goals, Functional
requirements, source pins, and Acceptance criteria are accepted. Implementation
requires the accompanying approved Plan and a task-specific human checkpoint.
