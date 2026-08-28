# Plan — VS Code GitHub Copilot Chat configuration alignment

> **Status:** Approved 2026-07-30 by Nicolás Pizarro, alongside the Spec. Task
> IDs still each require their own human checkpoint before Build executes
> them (see Execution rule below) — Plan approval authorizes the task list
> and path scoping, not unattended execution.
> **Owner:** `punch-ai-governance`, user-direct. These are AI-configuration
> tasks; they do not route through `punch-builder` or either product engineer.
> **Source Spec:**
> [`vscode-github-copilot-chat-alignment.md`](vscode-github-copilot-chat-alignment.md).
> **Execution rule:** Run one task ID at a time, in the order below. Every task
> requires a fresh human checkpoint. Return to Plan before touching any path not
> explicitly allowed.

- **Goal** (from Spec): Make the repository’s VS Code GitHub Copilot Chat
  behavior deterministic, internally consistent, and source-pinned by
  discovering only the intended `.github/**` project customizations while
  leaving every Claude-specific and generic Agents configuration untouched.

## Reviewed source pins

| Source | Stable release | Immutable commit | Adopted surface |
|---|---|---|---|
| Addy Osmani Agent Skills | `0.6.5` | `ff2df4c07e7836a092ed28e1e9b42f4d6009280c` | Punch-adapted methods/personas; disposition review, not blind copy |
| Graphify | `v0.9.30` | `ecfcd160d56b420eb8241430fa7b5b1951c7829f` | `graphify/skill-vscode.md` plus its VS Code references |
| Caveman | `v1.9.1` | `0d95a81d35a9f2d123a5e9430d1cfc43d55f1bb0` | `skills/caveman/SKILL.md` |

Source URLs and the official VS Code references are recorded in the Source
constraints section of the Spec. Build must fetch into a temporary directory,
verify the tag resolves to the listed commit, and compare before copying.

## Global forbidden path set

Every task inherits this forbidden set unless its own **Allowed edit paths**
explicitly names a narrower exception:

- `AGENTS.md`, `.agents/**`
- `CLAUDE.md`, `.claude/**`
- `.ai-upstream/**`, `.github/.ai-upstream/**`
- `.github/workflows/**`, `.github/copilot-setup-steps.yml`
- `.mcp.json`, `.codex/**`
- `src/**`, `bin/**`, `docker/**`, `docker-compose.yml`
- `package.json`, `tsconfig.json`
- `reports/**`, `graphify-out/**`
- `.gitignore`, `.graphifyignore`
- `docs/specs/**`, `docs/ai/history/**` (`docs/ai/history/**` does not exist on
  disk yet — pre-existing dangling reference, also present in
  `.github/agents/punch-ai-governance.agent.md:59`; not introduced by this
  Plan and out of this Plan's scope to create. Any validation command that
  assumes this path exists will find nothing and must not be read as a pass.)
- `docs/architecture/specs/**` during Build; changing this Spec or Plan requires
  an explicit return to the Spec/Plan phase

## Tasks

### VC-01 — Authorize the VS Code settings boundary in AI governance

- **Goal** — Narrowly add `.vscode/settings.json` to
  `punch-ai-governance`’s configuration scope and remove any active governance
  dependency on dismissed Claude/generic Agents config.
- **Allowed edit paths**
  - `.github/agents/punch-ai-governance.agent.md`
  - `.github/skills/punch-ai-governance/SKILL.md`
  - `docs/ai/agent-guards.md`
- **Read-only context paths**
  - `.github/prompts/punch-init.prompt.md`
  - `.github/copilot-instructions.md`
  - Official VS Code AI settings documentation
- **Forbidden paths** — global forbidden set; `.vscode/**`; every other
  `.github/**` and `docs/**` path not listed as allowed.
- **Implementation notes**
  - Add only `.vscode/settings.json`, not broad `.vscode/**`, to the governance
    agent’s allowed configuration scope.
  - State that the file controls VS Code GitHub Copilot Chat discovery only.
  - Remove `.agents/skills/**` from active adopted-vendor governance scope.
  - Keep `.github/agents/punch-cavecrew-*` governed as native Copilot custom
    agents; they do not depend on `.agents/**`.
- **Expected diff size** — approximately 25–50 lines.
- **Validation commands**
  - `rg -n "\\.vscode/settings\\.json" .github/agents/punch-ai-governance.agent.md .github/skills/punch-ai-governance/SKILL.md docs/ai/agent-guards.md`
  - `rg -n "\\.agents/skills|CLAUDE\\.md|AGENTS\\.md" .github/agents/punch-ai-governance.agent.md .github/skills/punch-ai-governance/SKILL.md`
    returns no active dependency/canon statement.
  - `git diff --check`
- **Rollback notes** — revert these three governance declarations; do not
  proceed to VC-02.
- **Human checkpoint** — human approval required before Build.
- **Build via** — `punch-ai-governance` directly.

### VC-02 — Add the workspace-local Copilot discovery policy

- **Goal** — Configure VS Code Chat to discover repository customizations from
  `.github/**` and ignore repository Claude/generic Agents surfaces.
- **Allowed edit paths**
  - `.vscode/settings.json`
- **Read-only context paths**
  - `.github/copilot-instructions.md`
  - `.github/instructions/**`
  - `.github/prompts/**`
  - `.github/agents/**`
  - `.github/skills/**`
  - Official VS Code AI settings documentation
- **Forbidden paths** — global forbidden set; every other `.vscode/**`; all
  `.github/**` and `docs/**`.
- **Required setting decisions**
  - `chat.useAgentsMdFile: false`
  - `chat.useNestedAgentsMdFiles: false`
  - `chat.useClaudeMdFile: false`
  - `chat.useCustomizationsInParentRepositories: false`
  - `github.copilot.chat.codeGeneration.useInstructionFiles: true`
  - `chat.includeApplyingInstructions: true`
  - `chat.instructionsFilesLocations` enables `.github/instructions` and
    disables `.claude/rules` and `~/.claude/rules`.
  - `chat.promptFilesLocations` enables `.github/prompts`.
  - `chat.agentFilesLocations` enables `.github/agents` and disables
    `.claude/agents` and `.agents/agents`.
  - `chat.useAgentSkills: true`
  - `chat.agentSkillsLocations` enables `.github/skills` and disables
    `.claude/skills`, `.agents/skills`, `~/.claude/skills`, and
    `~/.agents/skills`.
  - Do not change organization-managed settings or disable GitHub Copilot user
    profile assets outside the named Claude/generic Agents paths.
- **Expected diff size** — approximately 25–40 lines.
- **Validation commands**
  - `python3 -m json.tool .vscode/settings.json`
  - Open VS Code’s Agent Customizations diagnostics and confirm project
    instructions/prompts/agents/skills resolve from `.github/**`.
  - Confirm no project source under `.claude/**` or `.agents/**` is loaded.
  - `git diff --check`
- **Rollback notes** — remove `.vscode/settings.json`; VS Code returns to
  default discovery. Do not delete or edit the dismissed external-host files.
- **Human checkpoint** — human approval required before Build.
- **Build via** — `punch-ai-governance` directly, after VC-01.

### VC-03 — Make the live Copilot hub and Init sweep Chat-only

- **Goal** — Declare the `.github/**` roots plus the workspace discovery guard
  as the complete repository-local VS Code Chat surface.
- **Allowed edit paths**
  - `.github/copilot-instructions.md`
  - `.github/prompts/punch-init.prompt.md`
- **Read-only context paths**
  - `.vscode/settings.json`
  - `.github/agents/**`
  - `.github/skills/**`
  - `docs/ai/prompt-registry.md`
  - `docs/ai/skill-registry.md`
- **Forbidden paths** — global forbidden set; every other `.github/**`,
  `.vscode/**`, and `docs/**`.
- **Implementation notes**
  - Keep `copilot-instructions.md` concise and link-driven.
  - State that root `AGENTS.md`/`CLAUDE.md` and `.agents/**`/`.claude/**` are
    disabled for this VS Code workspace and are not Punch Chat canon.
  - Remove the vendor `.agents/skills/cavecrew` capability/install check from
    `/punch-init`.
  - Retain `.github/agents/punch-cavecrew-*` as optional, self-contained,
    read-only Copilot custom agents.
  - Add a readiness check for the required `.vscode/settings.json` values and
    the four `.github` customization roots.
  - Keep Graphify and Caveman explicit-only and non-blocking for unrelated
    lifecycle work.
- **Expected diff size** — approximately 90–150 lines.
- **Validation commands**
  - `rg -n "\\.agents/skills|\\.claude/|CLAUDE\\.md|AGENTS\\.md" .github/copilot-instructions.md .github/prompts/punch-init.prompt.md`
    returns only the short workspace-exclusion statement, not an active
    dependency, resolver, or canon.
  - `rg -n "punch-cavecrew-(investigator|reviewer)" .github/prompts/punch-init.prompt.md`
    confirms optional Copilot custom-agent treatment.
  - `git diff --check`
- **Rollback notes** — revert both files together so hub and readiness sweep
  do not disagree.
- **Human checkpoint** — human approval required before Build.
- **Build via** — `punch-ai-governance` directly.

### VC-04 — Remove external-host resolver assets from the Chat export template

- **Goal** — Make `.github/assets/**` an exportable VS Code Chat bundle without
  `AGENTS.md` or `CLAUDE.md` mirrors.
- **Allowed edit paths**
  - `.github/assets/README.md`
  - `.github/assets/prompts/punch-init.prompt.md`
  - `.github/assets/resolve/AGENTS.md` (delete)
  - `.github/assets/resolve/CLAUDE.md` (delete)
- **Read-only context paths**
  - `.github/copilot-instructions.md`
  - `.github/prompts/punch-init.prompt.md`
  - `.vscode/settings.json`
- **Forbidden paths** — global forbidden set; every other `.github/assets/**`,
  `.github/**`, `.vscode/**`, and `docs/**`.
- **Implementation notes**
  - Delete only the two resolver stubs; do not touch the real root files.
  - Remove their resolve-table rows and adoption instructions.
  - Keep the real `punch-boundaries` and validation-document resolver entries
    if still required by the export template.
- **Expected diff size** — approximately 55–100 lines, mostly deletions.
- **Validation commands**
  - `test ! -e .github/assets/resolve/AGENTS.md`
  - `test ! -e .github/assets/resolve/CLAUDE.md`
  - `rg -n "AGENTS\\.md|CLAUDE\\.md|\\.agents/|\\.claude/" .github/assets`
    returns no matches.
  - `git diff --check`
- **Rollback notes** — restore the two stubs and their exact table/prompt rows
  together.
- **Human checkpoint** — human approval required before Build.
- **Build via** — `punch-ai-governance` directly.

### VC-05 — Correct prompt-level lifecycle names and phase numbers

- **Goal** — Make Plan, Review, and Ship prompts describe the current
  six-phase lifecycle and single Build entry point.
- **Allowed edit paths**
  - `.github/prompts/punch-plan.prompt.md`
  - `.github/prompts/punch-review.prompt.md`
  - `.github/prompts/punch-ship.prompt.md`
- **Read-only context paths**
  - `.github/prompts/punch-build.prompt.md`
  - `docs/ai/prompt-registry.md`
  - `docs/ai/operating-model.md`
- **Forbidden paths** — global forbidden set; every other `.github/**` and
  `docs/**`.
- **Implementation notes**
  - Replace “which of 5 build-* prompts” with the single `punch-build` prompt
    and its dispatcher.
  - Label Review phase 5 and Ship phase 6.
  - Do not add a Define or Verify prompt.
- **Expected diff size** — approximately 5–15 lines.
- **Validation commands**
  - `rg -n "5 build|build-\\*|Phase 7|Phase 6 — Review" .github/prompts`
    returns no matches.
  - Confirm all eight prompt frontmatter `agent:` values name existing custom
    agents.
  - `git diff --check`
- **Rollback notes** — revert the three prompt edits as one lifecycle unit.
- **Human checkpoint** — human approval required before Build.
- **Build via** — `punch-ai-governance` directly.

### VC-06 — Correct lifecycle-skill handoffs to the single Build prompt

- **Goal** — Remove obsolete `punch-build-*` handoffs and the broken Context
  Engineering anchor from the Spec/Plan methods.
- **Allowed edit paths**
  - `.github/skills/punch-planning-and-task-breakdown/SKILL.md`
  - `.github/skills/punch-spec-driven-development/SKILL.md`
- **Read-only context paths**
  - `.github/prompts/punch-build.prompt.md`
  - `.github/skills/punch-context-engineering/SKILL.md`
  - `docs/ai/scoped-build-policy.md`
- **Forbidden paths** — global forbidden set; every other `.github/**` and
  `docs/**`.
- **Implementation notes**
  - Use `punch-build` plus `punch-builder` dispatcher terminology.
  - Keep task-specific agent routing in the Plan contract.
  - Link Context Engineering to a real heading/file, not the removed
    `#graphify-gate`.
- **Expected diff size** — approximately 8–20 lines.
- **Validation commands**
  - `rg -n "punch-build-\\*|graphify-gate" .github/skills/punch-planning-and-task-breakdown/SKILL.md .github/skills/punch-spec-driven-development/SKILL.md`
    returns no matches.
  - `git diff --check`
- **Rollback notes** — revert both method files together.
- **Human checkpoint** — human approval required before Build.
- **Build via** — `punch-ai-governance` directly.

### VC-07 — Align Build checks with the independent Test verdict

- **Goal** — State one execution contract: Build may run scoped checks; Test
  independently owns the final PASS/FAIL verdict.
- **Allowed edit paths**
  - `.github/skills/punch-incremental-implementation/SKILL.md`
  - `.github/prompts/punch-build.prompt.md`
- **Read-only context paths**
  - `.github/agents/punch-builder.agent.md`
  - `.github/agents/punch-runtime-engineer.agent.md`
  - `.github/agents/punch-performance-test-engineer.agent.md`
  - `.github/prompts/punch-test.prompt.md`
- **Forbidden paths** — global forbidden set; every other `.github/**` and
  `docs/**`.
- **Implementation notes**
  - Remove claims that builders have no terminal, never run tests, or hand off
    without commands.
  - Distinguish implementation checks from `punch-test`’s final verdict.
  - Remove Graphify from Build’s trigger list because Graphify is
    `disable-model-invocation: true` and user-invoked only.
- **Expected diff size** — approximately 20–45 lines.
- **Validation commands**
  - `rg -n "builders carry no terminal|builders do not run tests|does not run commands" .github/skills/punch-incremental-implementation/SKILL.md`
    returns no matches.
  - `rg -n "\\[graphify\\]" .github/prompts/punch-build.prompt.md` returns no
    matches.
  - `rg -n "independent|final.*verdict|punch-test" .github/skills/punch-incremental-implementation/SKILL.md .github/prompts/punch-build.prompt.md`
    confirms the handoff.
  - `git diff --check`
- **Rollback notes** — revert both files; do not change agent tool lists.
- **Human checkpoint** — human approval required before Build.
- **Build via** — `punch-ai-governance` directly.

### VC-08 — Repair the validation-document scopes

- **Goal** — Point all active artifact/reporting configuration at the real
  validation documentation.
- **Allowed edit paths**
  - `.github/instructions/artifacts-reporting.instructions.md`
  - `.github/skills/punch-data-harvest/SKILL.md`
  - `.github/prompts/punch-document.prompt.md`
- **Read-only context paths**
  - `docs/workflows/validation.md`
  - `.github/skills/punch-data-harvest/artifact-contract.md`
- **Forbidden paths** — global forbidden set; every other `.github/**` and
  `docs/**`.
- **Implementation notes**
  - Replace `docs/validation/**` with the exact active path or correct glob for
    `docs/workflows/validation.md`.
  - Keep runtime artifact names and schemas unchanged.
- **Expected diff size** — approximately 5–15 lines.
- **Validation commands**
  - `rg -n "docs/validation" .github/instructions/artifacts-reporting.instructions.md .github/skills/punch-data-harvest/SKILL.md .github/prompts/punch-document.prompt.md`
    returns no matches.
  - `test -f docs/workflows/validation.md`
  - `git diff --check`
- **Rollback notes** — revert the three path-only changes.
- **Human checkpoint** — human approval required before Build.
- **Build via** — `punch-ai-governance` directly.

### VC-09 — Re-pin and disposition Addy Osmani Agent Skills

- **Goal** — Replace the mixed/older provenance claim with the reviewed stable
  `0.6.5` source pin and selectively absorb relevant method improvements.
- **Allowed edit paths**
  - `docs/ai/agent-skills-provenance.md`
  - `.github/skills/punch-performance-optimization/SKILL.md`
- **Read-only context paths**
  - `.github/skills/punch-debugging-and-error-recovery/SKILL.md`
  - `.github/skills/punch-incremental-implementation/SKILL.md`
  - `.github/skills/punch-planning-and-task-breakdown/SKILL.md`
  - `.github/skills/punch-test-driven-development/SKILL.md`
  - Temporary checkout/archive of Addy Osmani Agent Skills at the reviewed pin
- **Forbidden paths** — global forbidden set; every other `.github/**` and
  `docs/**`.
- **Implementation notes**
  - Pin release `0.6.5` and commit
    `ff2df4c07e7836a092ed28e1e9b42f4d6009280c`.
  - Record the six source skills changed since the prior audited head:
    debugging, incremental implementation, performance optimization, planning,
    shipping, and TDD.
  - Classify stack-neutral command discovery as already covered by Punch’s
    fixed `./bin/punch` contract where applicable.
  - Keep shipping unadopted.
  - Add upstream’s remeasure, noise-awareness, attempt-ledger, and
    keep-or-revert discipline to `punch-performance-optimization` only where it
    does not duplicate existing Punch rules.
  - Do not edit or claim to normalize `.ai-upstream/**`.
- **Expected diff size** — approximately 60–120 lines.
- **Validation commands**
  - Verify tag `0.6.5` resolves to the listed commit through the GitHub API.
  - `rg -n "0\\.6\\.5|ff2df4c07e7836a092ed28e1e9b42f4d6009280c" docs/ai/agent-skills-provenance.md`
  - Confirm all 24 upstream skills and adopted personas still have a
    disposition.
  - `git diff --check`
- **Rollback notes** — revert the provenance and performance-method edits
  together; the prior pin remains documented but stale.
- **Human checkpoint** — human approval required before Build.
- **Build via** — `punch-ai-governance` directly.

### VC-10 — Refresh the Graphify core VS Code skill

- **Goal** — Update the Graphify entrypoint, version marker, and extraction
  contract from stable `v0.9.30`.
- **Allowed edit paths**
  - `.github/skills/graphify/SKILL.md`
  - `.github/skills/graphify/.graphify_version`
  - `.github/skills/graphify/references/extraction-spec.md`
- **Read-only context paths**
  - Temporary checkout/archive of Graphify
    `ecfcd160d56b420eb8241430fa7b5b1951c7829f`
  - `.github/copilot-instructions.md`
  - `docs/ai/graphify-install.md`
- **Forbidden paths** — global forbidden set; every other
  `.github/skills/graphify/**`, `.github/**`, and `docs/**`.
- **Implementation notes**
  - Source `SKILL.md` from `graphify/skill-vscode.md`, not a generic or
    different-host variant.
  - Preserve the upstream body and add only `user-invocable: true` and
    `disable-model-invocation: true`.
  - Set the version marker to `0.9.30`.
- **Expected diff size** — upstream-driven; approximately 150–300 lines.
- **Validation commands**
  - Verify tag `v0.9.30` resolves to the listed commit.
  - Compare normalized `SKILL.md` against upstream after removing only the two
    approved frontmatter fields.
  - `test "$(tr -d '[:space:]' < .github/skills/graphify/.graphify_version)" = "0.9.30"`
  - `git diff --check`
- **Rollback notes** — restore the three `0.8.41` files as one unit.
- **Human checkpoint** — human approval required before Build.
- **Build via** — `punch-ai-governance` directly, refresh-from-upstream mode.

### VC-11 — Refresh Graphify query and export references

- **Goal** — Update the first bounded set of Graphify VS Code references from
  the same stable source pin.
- **Allowed edit paths**
  - `.github/skills/graphify/references/add-watch.md`
  - `.github/skills/graphify/references/exports.md`
  - `.github/skills/graphify/references/query.md`
- **Read-only context paths**
  - `.github/skills/graphify/SKILL.md`
  - Temporary Graphify source at the reviewed pin
- **Forbidden paths** — global forbidden set; every other
  `.github/skills/graphify/**`, `.github/**`, and `docs/**`.
- **Expected diff size** — upstream-driven; approximately 50–180 lines.
- **Validation commands**
  - Byte-compare each file to the corresponding upstream VS Code reference.
  - Confirm every reference linked by the refreshed `SKILL.md` exists.
  - `git diff --check`
- **Rollback notes** — restore these three references together.
- **Human checkpoint** — human approval required before Build.
- **Build via** — `punch-ai-governance` directly, refresh-from-upstream mode.

### VC-12 — Refresh Graphify integration references

- **Goal** — Update the second bounded set of Graphify VS Code references from
  the same stable source pin.
- **Allowed edit paths**
  - `.github/skills/graphify/references/github-and-merge.md`
  - `.github/skills/graphify/references/hooks.md`
  - `.github/skills/graphify/references/transcribe.md`
- **Read-only context paths**
  - `.github/skills/graphify/SKILL.md`
  - Temporary Graphify source at the reviewed pin
- **Forbidden paths** — global forbidden set; every other
  `.github/skills/graphify/**`, `.github/**`, and `docs/**`.
- **Implementation notes**
  - Preserve upstream reference text for source parity.
  - Other-host integration text remains inert upstream material: no Punch
    instruction may auto-load it, invoke it, or treat it as repository canon.
- **Expected diff size** — upstream-driven; approximately 50–180 lines.
- **Validation commands**
  - Byte-compare each file to the corresponding upstream VS Code reference.
  - Confirm no Punch-authored auto-hook or external-host dependency is added.
  - `git diff --check`
- **Rollback notes** — restore these three references together.
- **Human checkpoint** — human approval required before Build.
- **Build via** — `punch-ai-governance` directly, refresh-from-upstream mode.

### VC-13 — Refresh Graphify update guidance and current documentation

- **Goal** — Complete the Graphify refresh and supersede stale source/version
  documentation without rewriting historical decisions.
- **Allowed edit paths**
  - `.github/skills/graphify/references/update.md`
  - `docs/ai/graphify-install.md`
  - `docs/ai/decisions/0002-graphify-host-tool.md`
- **Read-only context paths**
  - `.github/skills/graphify/**`
  - Temporary Graphify source at the reviewed pin
  - `.github/copilot-instructions.md`
- **Forbidden paths** — global forbidden set; every other `.github/**` and
  `docs/**`.
- **Implementation notes**
  - Byte-copy the current upstream `update.md`.
  - Update active install/version text to `Graphify-Labs/graphify` `v0.9.30`.
  - Append a dated superseding note to ADR 0002 for current VS Code Chat
    behavior; do not rewrite its historical body.
  - Correct the live broken `punch-graphify` link in the superseding/current
    section.
  - Preserve explicit-only, local-first, approval-gated behavior.
- **Expected diff size** — approximately 90–180 lines.
- **Validation commands**
  - Byte-compare `update.md` to upstream.
  - `rg -n "0\\.8\\.41|github\\.com/safishamsi/graphify|punch-graphify" docs/ai/graphify-install.md`
    returns no active matches.
  - Confirm the ADR preserves its original decision and adds a superseding
    dated section.
  - `git diff --check`
- **Rollback notes** — restore `update.md` and revert only the new documentation
  appendix/current install text.
- **Human checkpoint** — human approval required before Build.
- **Build via** — `punch-ai-governance` directly.

### VC-14 — Refresh the Caveman project skill

- **Goal** — Update the explicit-only Caveman skill to stable `v1.9.1` and
  remove the broken relocated README.
- **Allowed edit paths**
  - `.github/skills/caveman/SKILL.md`
  - `.github/skills/caveman/README.md` (delete)
- **Read-only context paths**
  - Temporary Caveman source at
    `0d95a81d35a9f2d123a5e9430d1cfc43d55f1bb0`
  - `.github/copilot-instructions.md`
  - `docs/ai/skill-registry.md`
- **Forbidden paths** — global forbidden set; every other `.github/**` and
  `docs/**`.
- **Implementation notes**
  - Preserve upstream `skills/caveman/SKILL.md`, adding only
    `user-invocable: true` and `disable-model-invocation: true`.
  - Use the upstream measured 65% description and current clarity rules.
  - Delete the unreferenced relocated README rather than patching an upstream
    repository-relative link.
- **Expected diff size** — approximately 45–100 lines.
- **Validation commands**
  - Verify tag `v1.9.1` resolves to the listed commit.
  - Compare normalized `SKILL.md` to upstream after removing only the two
    approved fields.
  - `rg -n "75%" .github/skills/caveman` returns no matches.
  - `test ! -e .github/skills/caveman/README.md`
  - `git diff --check`
- **Rollback notes** — restore the prior skill and README together.
- **Human checkpoint** — human approval required before Build.
- **Build via** — `punch-ai-governance` directly, refresh-from-upstream mode.

### VC-15 — Reconcile live lifecycle and mode documentation

- **Goal** — Make the live Copilot operating documents agree with the corrected
  prompts and VS Code’s current Plan/custom-agent model.
- **Allowed edit paths**
  - `docs/ai/operating-model.md`
  - `docs/ai/prompt-registry.md`
  - `docs/ai/copilot-mode-mapping.md`
- **Read-only context paths**
  - `.github/copilot-instructions.md`
  - `.github/prompts/**`
  - `.github/agents/**`
  - Official VS Code prompt/custom-agent documentation
- **Forbidden paths** — global forbidden set; every other `.github/**` and
  `docs/**`.
- **Implementation notes**
  - Make `.github/copilot-instructions.md` and path instructions the active
    rules sources; remove `CLAUDE.md` constitution/global-instruction claims.
  - Describe six phases and eight prompts accurately.
  - Replace `punch-builder-*` with `punch-builder`.
  - Acknowledge built-in `plan` as a supported prompt `agent:` value while
    retaining the custom read-only `punch-architect` design.
  - Keep GitHub Copilot cloud-agent and CLI behavior out of these Chat docs.
- **Expected diff size** — approximately 50–100 lines.
- **Validation commands**
  - `rg -n "CLAUDE\\.md|seven lifecycle|7 phases|punch-builder-\\*|no .*plan.*mode" docs/ai/operating-model.md docs/ai/prompt-registry.md docs/ai/copilot-mode-mapping.md`
    returns no active stale claim.
  - Confirm the prompt registry has exactly eight active prompt rows.
  - `git diff --check`
- **Rollback notes** — revert the three live documentation files together.
- **Human checkpoint** — human approval required before Build.
- **Build via** — `punch-ai-governance` directly.

### VC-16 — Reconcile boundaries, skill registry, and maintenance cascades

- **Goal** — Finish live-document parity for lifecycle, active skills, and
  Chat-only maintenance ownership.
- **Allowed edit paths**
  - `docs/architecture/punch-boundaries.md`
  - `docs/ai/skill-registry.md`
  - `docs/ai/maintenance-matrix.md`
- **Read-only context paths**
  - `.github/skills/**`
  - `.github/agents/**`
  - `.github/prompts/**`
  - `docs/workflows/validation.md`
  - `docs/ai/agent-skills-provenance.md`
- **Forbidden paths** — global forbidden set; every other `.github/**` and
  `docs/**`.
- **Implementation notes**
  - Remove the retired Define/seven-phase wording from the boundary document.
  - Remove `.agents/skills/cavecrew` from the active project-skill registry.
  - Keep `punch-cavecrew-*` rows/mentions only as `.github/agents` Copilot
    custom agents, not as vendor-skill dependents.
  - Update Graphify/Caveman source pins and current locations.
  - Replace stale `docs/validation/README.md` and root setup-placeholder links.
  - Remove maintenance requirements that make `AGENTS.md` or `CLAUDE.md` part
    of the VS Code Chat asset cascade; use the `.github` hub/registries instead.
  - Do not treat a bare "Phase 6" hit as drift by itself: under the six-phase
    model, Ship is legitimately Phase 6 (see
    `docs/ai/golden-lifecycle/06-ship.md:3`, `docs/ai/skill-registry.md:113`).
    Only "Phase 6 — Review" or "Phase 7" (Review/Ship carrying the retired
    seven-phase numbers) is stale.
- **Expected diff size** — approximately 60–130 lines.
- **Validation commands**
  - Confirm skill-registry rows match `.github/skills/*/SKILL.md` exactly.
  - `rg -n "\\.agents/skills/cavecrew|docs/validation|\\.github/copilot-setup-steps\\.yml|Define → Spec|seven-phase|Phase 6 — Review|Phase 7" docs/architecture/punch-boundaries.md docs/ai/skill-registry.md docs/ai/maintenance-matrix.md`
    returns no active stale claim. Do not use a bare `seven` or bare
    `Phase 6` pattern — both produce false positives against legitimate
    six-phase text.
  - `git diff --check`
- **Rollback notes** — revert these three documents together; do not revert the
  already-refreshed source skills without also reverting their source tasks.
- **Human checkpoint** — human approval required before Build.
- **Build via** — `punch-ai-governance` directly.

## Order of execution

1. VC-01 authorizes the narrow governance scope.
2. VC-02 installs the discovery boundary before any external-host references
   are removed from Chat readiness.
3. VC-03 and VC-04 align the live hub, Init, and export template.
4. VC-05 through VC-08 correct lifecycle and path contracts.
5. VC-09 pins the Addy source and selectively updates its Punch adaptation.
6. VC-10 through VC-13 refresh Graphify in bounded source-parity slices.
7. VC-14 refreshes Caveman.
8. VC-15 and VC-16 reconcile live documentation and registries against the
   settled configuration.
9. Run the final validation gate below; then hand off to Review.

Tasks are sequential because several later registry/document decisions depend
on the exact asset state produced by earlier tasks. Do not parallelize them.

## Final validation gate

Run after VC-01 through VC-16 are complete:

1. `python3 -m json.tool .vscode/settings.json`
2. `git diff --check`
3. Run the read-only `punch-ai-governance` frontmatter, registry-parity, and
   active-link audit over `.github/**`, `.vscode/settings.json`, and the live
   docs changed by this Plan.
4. Confirm `git diff --name-only` contains no path in the global forbidden set.
5. Confirm Graphify/Caveman normalized source parity and immutable tag commits.
6. In current VS Code Stable, open Agent Customizations diagnostics:
   - repository instructions come from `.github/copilot-instructions.md` and
     `.github/instructions/**`;
   - prompt files come from `.github/prompts/**`;
   - custom agents come from `.github/agents/**`;
   - project skills come from `.github/skills/**`;
   - no repository source under `.claude/**` or `.agents/**` is loaded.
7. Invoke `/punch-init` in read-only mode and require all mandatory Chat asset
   checks to PASS. Optional Graphify/Caveman executable availability may WARN,
   but cannot block unrelated Punch lifecycle use.
8. Confirm no Punch runtime, Docker, k6, workflow, report, or graph build was
   run or modified. `reports/state/punch-run.json` is not evidence for this
   Chat-configuration-only Plan.

If the current VS Code version ignores a documented `false` location entry and
still loads `.agents/**` or `.claude/**`, stop and return to Plan. Do not solve
that mismatch by editing or deleting the dismissed external-host files.

## Cross-cutting risks

- **VS Code version drift.** AI customization settings evolve quickly.
  Validate against current Stable and the official settings reference during
  Build; an unrecognized setting is a blocker, not permission to guess.
- **Object-setting merge behavior.** User, workspace, and default object
  values can merge. Diagnostics, not the JSON text alone, is the acceptance
  evidence for actual discovery.
- **Imported upstream references.** Graphify’s upstream reference set may
  mention other hosts. Source parity is preserved, but Punch must keep those
  references manual/inert and must never declare them repository canon.
- **Registry timing.** The skill registry is intentionally updated after both
  upstream skill refreshes. Until VC-16 lands, temporary registry drift is
  expected inside the unreviewed worktree and must not be shipped.
- **Historical records.** Historical Spec/Plan/ADR text can contain retired
  decisions. Audit active configuration and live docs; do not rewrite history
  to make broad text searches artificially clean.
- **Scope ambiguity.** `.github/agents/**` is in scope as native GitHub Copilot
  custom-agent configuration. Root `AGENTS.md` and `.agents/**` are not.

## Rollback plan

- Each task is independently revertible except the Graphify sequence
  VC-10–VC-13, which must roll back as one versioned unit.
- If workspace discovery regresses, revert VC-02 first; external-host files
  were never changed and remain available to their own hosts.
- If an upstream refresh fails parity or Chat smoke validation, restore the
  previous complete skill version and its documentation before Review.
- If lifecycle reconciliation creates a conflict, revert VC-15/VC-16 and
  return to Plan with the exact conflicting source; do not change product code.
- No data migration, runtime rollback, report cleanup, container teardown, or
  workflow rollback is required.

**Gate:** human approves this Plan, then authorizes each task ID before
`punch-ai-governance` implements it. Completion advances to a read-only
governance Review, not directly to Ship.
