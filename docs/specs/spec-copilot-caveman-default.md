# Spec — Copilot-only Caveman default

> **Status:** Draft for human approval  
> **Scope exception:** The human approved writing this Spec to `docs/specs/`
> even though the current `punch-spec` prompt names
> `docs/architecture/specs/` as its permitted destination.

- **Goal** — Make upstream Caveman the concise-prose default for VS Code GitHub
  Copilot Chat, under Punch governance, while keeping the user-facing skill name
  `caveman`, preserving normal prose for Build, and preventing Caveman activation
  through other-agent configuration surfaces.

- **Non-goals**
  - Do not rename the skill or slash command to `punch-caveman` or
    `/punch-caveman`.
  - Do not activate or configure Caveman for Claude Code, Codex, Cursor,
    Windsurf, Copilot CLI, Copilot coding agent, or any host other than VS Code
    GitHub Copilot Chat.
  - Do not run the upstream unified installer or `--with-init`; those paths can
    write parallel rules into `AGENTS.md`, `.claude/`, and other host locations.
  - Do not change Punch lifecycle authority, phase ownership, tool access,
    delegation, evidence requirements, or verdicts.
  - Do not enable Caveman in the `punch-build` chain.
  - Do not change product code, Docker Compose, k6 tests, workflows, runtime
    behavior, or report schemas.
  - Do not decide or implement Cavecrew removal in this change; that remains a
    separate governance decision.

- **Functional requirements**
  1. The user-facing skill remains named `caveman`; Punch governance is expressed
     through Copilot instructions and documentation, not by forking its public
     identity into “Punch Caveman.”
  2. The project skill is located at `.github/skills/caveman/SKILL.md`, the
     Copilot-oriented project-skill location documented by VS Code. The existing
     portable `.agents/skills/caveman/` copy is retired so the repository does
     not advertise Caveman as a cross-agent project skill.
  3. The skill preserves upstream Caveman behavior and provenance, with only the
     minimum VS Code access adaptation recorded in its frontmatter and registry:
     `user-invocable: true` and `disable-model-invocation: true`.
  4. `.github/copilot-instructions.md` contains one short, self-contained
     Caveman rule that applies `lite` to assistant prose by default in VS Code
     GitHub Copilot Chat.
  5. The default rule does not require automatic loading of the full skill on
     every request. Explicit `/caveman <mode>` invocation loads the skill and
     overrides `lite` for the conversation; `stop caveman` or `normal mode`
     disables it for the conversation.
  6. Build remains normal prose. Caveman never compresses code, commands, paths,
     logs, errors, exit codes, thresholds, JSON, YAML, CSV, acceptance criteria,
     blockers, next actions, or `reports/state/punch-run.json`.
  7. Security warnings, irreversible-action confirmations, architecture
     tradeoffs, and any ambiguous content use normal prose.
  8. Caveman activation and mode instructions are removed from `AGENTS.md`,
     `CLAUDE.md`, `.claude/**`, and other non-Copilot configuration surfaces.
     General Punch rules and the thin Claude Guard bridge remain otherwise
     unchanged.
  9. The Punch-specific `punch-comms-policy` skill is retired after its essential
     clarity, evidence, artifact, and Build-exclusion constraints are reconciled
     into the single Copilot instruction block. No second Caveman-branded policy
     skill remains active.
  10. The skill registry and upstream manifest describe the Copilot-only
      location, upstream source, allowed frontmatter adaptation, refresh method,
      and absence of automatic cross-host installation.

- **Technical constraints**
  - VS Code GitHub Copilot Chat is the only supported host for this capability.
  - Prefer upstream Caveman documentation for Caveman semantics and Microsoft
    VS Code documentation for discovery, instruction, and invocation behavior.
    Punch may narrow activation but must not silently contradict either source.
  - Use `.github/copilot-instructions.md` as the only always-on Caveman activation
    surface. Do not duplicate the activation rule in `AGENTS.md`, `CLAUDE.md`,
    `.claude/**`, or user-level configuration.
  - Keep always-on instructions short. The default `lite` behavior must not
    require loading the full `SKILL.md`; explicit slash invocation is the path
    to heavier modes.
  - Preserve the existing rule that Build is fully decoupled from Caveman.
    Enabling Caveman in Build requires a separate human-approved Punch rule
    change.
  - Use no host-side npm, k6, pip, hooks, MCP servers, watchers, or global
    configuration.
  - Any implementation must follow a separately approved Plan with explicit
    allowed, read-only, and forbidden paths.

- **Affected layers**
  - AI configuration: Copilot instructions and Copilot project-skill discovery.
  - AI governance: skill registry, upstream provenance, asset validation, and
    stale-reference cleanup.
  - Claude Guard bridge and `AGENTS.md`: removal of Caveman activation only; no
    change to their non-Caveman project rules.
  - Product runtime, Compose, k6, data harvest, and report contracts: unaffected.

- **Artifact / log / reporting implications**
  - No runtime artifact path, schema, log, threshold, or reporting behavior
    changes.
  - Caveman must preserve all runtime evidence verbatim, including
    `reports/state/punch-run.json`.
  - Static AI-governance validation may produce review evidence, but it must not
    create a new persistent report format.

- **Source constraints**
  - Caveman installation and Copilot always-on behavior:
    <https://github.com/JuliusBrussee/caveman/blob/main/INSTALL.md>
  - Upstream static activation rule:
    <https://github.com/JuliusBrussee/caveman/blob/main/src/rules/caveman-activate.md>
  - VS Code Agent Skills locations and invocation frontmatter:
    <https://code.visualstudio.com/docs/agent-customization/agent-skills>
  - VS Code always-on custom instructions:
    <https://code.visualstudio.com/docs/agent-customization/custom-instructions>

- **Acceptance criteria**
  1. Exactly one active project skill is named `caveman`, located at
     `.github/skills/caveman/SKILL.md`; no active copy remains under
     `.agents/skills/caveman/` or `.claude/skills/`.
  2. The skill declares `user-invocable: true` and
     `disable-model-invocation: true`, remains available through `/caveman`, and
     is not automatically loaded by Copilot based only on prompt relevance.
  3. `.github/copilot-instructions.md` makes `lite` the default for VS Code
     GitHub Copilot Chat, honors explicit mode/stop overrides, preserves exact
     technical evidence, and excludes Build.
  4. `AGENTS.md`, `CLAUDE.md`, and `.claude/**` contain no Caveman activation,
     mode, skill-path, or obsolete `punch-build-caveman` instruction.
  5. No live reference to `punch-comms-policy` remains after its retirement, and
     all essential evidence/clarity constraints remain in the Copilot rule.
  6. Registries, governance checks, and upstream documentation agree on the
     skill name, Copilot-only location, invocation controls, and source.
  7. Build prompts and Build agents contain no Caveman dependency and continue
     to use normal prose.
  8. `git diff --check` passes, and a Punch AI-governance review reports no
     broken links, duplicate activation blocks, orphaned skills, or stale agent
     references.
  9. Official verification remains available through `./bin/punch doctor` and
     `./bin/punch run smoke`; when runtime verification is performed,
     `reports/state/punch-run.json` exists and records `passed: true`.

**Gate:** approved when Goal, Non-goals, Functional requirements, and Acceptance
criteria are agreed. An approved `/punch-plan` is required before configuration
changes begin.
