# VS Code GitHub Copilot Customization Audit Prompt

Use this playbook to audit the complete VS Code GitHub Copilot customization
stack in the current repository: instructions, prompt files, custom agents,
Agent Skills and their resources, hooks, tool sets, MCP references, registries,
and provenance.

## Before running the audit

1. Open the repository in the latest stable VS Code and GitHub Copilot Chat.
2. Select the built-in Agent, not a repository custom agent being audited.
3. Keep normal approvals enabled. Do not use Bypass Approvals.
4. For prompt-file runtime tests, use a local VS Code extension-host session.
   Agent Host sessions do not load prompt files.
5. Run `Chat: Open Customizations`. Right-click the Chat view and select
   **Diagnostics** to inspect loaded assets and configuration errors.
6. For deeper runtime evidence, enable
   `github.copilot.chat.agentDebugLog.fileLogging.enabled` and open
   **Show Agent Debug Logs** from the Chat menu.
7. Paste the prompt below into a new chat.

## Audit prompt

```text
Act as an independent, evidence-driven auditor of the complete VS Code GitHub
Copilot customization stack in this repository.

This is a READ-ONLY audit. Do not edit, create, delete, rename, format, stage,
commit, push, open a PR, install dependencies, or clean generated files. Do not
alter the current working tree. If a useful test would modify state, describe it
as a manual test instead of running it.

Audit the CURRENT WORKING TREE, including staged, unstaged, untracked, and
deleted files. Use HEAD only as comparison evidence. Preserve pre-existing work
and record the initial and final `git status --short`.

Do not treat any repository custom agent as the sole authority for auditing
itself. Repository instructions are audit subjects too. Apply them while
operating, but judge their syntax and claims against official product
documentation, the actual repository, and documented upstream provenance.

Primary references

Consult the current versions of these official sources before judging
compatibility:

- https://code.visualstudio.com/docs/agents/concepts/customization
- https://code.visualstudio.com/docs/agent-customization/agent-skills
- https://code.visualstudio.com/docs/agent-customization/custom-agents
- https://code.visualstudio.com/docs/agent-customization/prompt-files
- https://code.visualstudio.com/docs/agent-customization/custom-instructions
- https://code.visualstudio.com/docs/agents/run/subagents
- https://code.visualstudio.com/docs/agents/agent-troubleshooting/chat-debug-view
- https://code.visualstudio.com/docs/agents/run/security
- https://agentskills.io/specification
- https://docs.github.com/en/copilot/reference/customization-cheat-sheet
- https://docs.github.com/en/copilot/reference/custom-agents-configuration
- https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills

Use only official VS Code, GitHub, Agent Skills specification, and declared
upstream-repository sources for compatibility findings. Record the access date.
If web access is unavailable, mark current-document verification as NOT RUN; do
not silently rely on memory.

Scope

Discover and audit every active or referenced AI customization, including:

- `.github/copilot-instructions.md`
- root and nested `AGENTS.md`
- `CLAUDE.md` and any compatibility bridges
- `.github/instructions/**/*.instructions.md`
- `.github/prompts/**/*.prompt.md`
- `.github/agents/**/*`
- `.github/skills/**/SKILL.md`
- every skill's scripts, references, examples, templates, and assets
- configured alternative locations such as `.agents/`, `.claude/`, or paths
  defined in VS Code settings
- `.github/hooks/**/*.json`
- tool-set and MCP configuration referenced by agents or prompts
- `.vscode/settings.json` and other settings that affect customization discovery
- registries, inventories, provenance records, ADRs, and documentation claiming
  which assets exist or are active
- deleted assets still referenced by active files
- duplicate assets that VS Code might discover from more than one location

Distinguish active operational files from frozen examples, historical ADRs,
generated documentation, vendored upstream snapshots, and superseded records.
Historical references are not dangling operational references unless they claim
to describe the current system.

Phase 1 — Baseline and discovery

1. Record:
   - repository root and current branch
   - `git status --short`
   - `git diff --name-status`
   - relevant VS Code and Copilot settings if visible
   - active customization search paths
   - whether this is a local extension-host session or Agent Host session
2. Inventory every relevant file. Include files deleted in the working tree.
3. Compare the filesystem inventory with:
   - VS Code Chat Customization Diagnostics
   - `/skills`, `/agents`, `/prompts`, and `/instructions` menus when observable
   - repository registries and documentation
4. If you cannot access a UI diagnostic directly, label it USER CHECK. Give the
   exact VS Code command or menu action required. Never infer "loaded
   successfully" merely because a file exists.

Produce an inventory table containing:

`type | identifier | path | discovery source | expected visibility | actual diagnostic status | target host | registry status | findings`

Phase 2 — Format and schema validation

Validate each asset against its own format. Do not mix schemas.

Agent Skills:

- `SKILL.md` exists with valid YAML frontmatter.
- Required `name` and `description` exist.
- `name` is 1–64 lowercase alphanumeric/hyphen characters, has no leading,
  trailing, or consecutive hyphen, and exactly matches the parent directory.
- Description is 1–1024 characters and explains both what the skill does and
  when to use it.
- Separate open-standard fields from documented VS Code extensions.
- Classify unknown top-level fields as unsupported unless an official source
  documents them.
- Treat recommended limits such as a concise `SKILL.md`, shallow reference
  chains, and progressive disclosure as recommendations, not hard failures.
- Check `user-invocable`, `disable-model-invocation`, and experimental
  `context: fork` behavior, including required VS Code settings.
- If `skills-ref` is already installed, run `skills-ref validate` read-only. Do
  not install it. Otherwise perform manual validation and mark tool validation
  NOT RUN.

Instruction files:

- Validate `.instructions.md` frontmatter using `name`, `description`, and
  `applyTo`.
- Check glob syntax and whether representative matching and nonmatching paths
  behave as intended.
- Check always-on `copilot-instructions.md`, `AGENTS.md`, and `CLAUDE.md`
  discovery and scope separately.
- Detect conflicting always-on rules because instruction ordering is not
  guaranteed.
- Flag duplicated, obvious, or lint-enforceable rules that unnecessarily
  consume context.

Prompt files:

- Validate `.prompt.md` fields: `name`, `description`, `argument-hint`, `agent`,
  `model`, and `tools`.
- Resolve the selected built-in or custom agent.
- Validate relative links and input variables.
- Apply documented tool priority: prompt tools override referenced-agent tools.
- Identify prompt files that are incorrectly claimed to work on Agent Host.

Custom agents:

- Validate fields according to their declared `target`.
- For dual-host agents, distinguish VS Code-supported, GitHub-cloud-supported,
  ignored, deprecated, and incompatible fields.
- Resolve tools, tool sets, MCP tools, models, handoffs, hooks, and target
  agents.
- Treat unavailable tools as configuration defects or portability gaps even if
  VS Code silently ignores them.
- Check `user-invocable`, `disable-model-invocation`, and deprecated `infer`.
- When `agents` is present, confirm the `agent` tool is available.
- Confirm agent names used by delegation and handoffs match exactly.

Hooks, MCP, and tool sets:

- Validate syntax, referenced commands/tools, feature settings, and host
  support.
- Review trust boundaries, secret handling, network access, and approval
  assumptions.

Phase 3 — Reference and execution graph

Build a compact reachability graph covering:

`instruction/prompt → agent → subagent → skill → script/reference/asset → repository command or output`

Check for:

- missing files and broken relative links
- stale references to deleted or renamed assets
- orphaned resources with no reachable consumer
- active files that reference frozen or superseded material as current policy
- duplicate names or search paths causing shadowing
- impossible handoffs or delegation
- agents allowed as subagents but never reachable
- agents intended as leaves that can accidentally delegate
- coordinators listing agents without the `agent` tool
- restrictive flags that contradict an explicit allowlist
- tool permissions broader or narrower than the documented job
- scripts or resources mentioned in prose but absent
- resources present but never referenced directly or transitively
- registry counts, names, and phase mappings that disagree with the filesystem

Do not label optional subagent delegation as mandatory unless official behavior
or the repository's concrete architecture requires it.

Phase 4 — Provenance and simplification

Locate every declared upstream repository URL, commit SHA, tag, vendored
snapshot, or provenance record.

For every adopted or adapted asset:

1. Compare against the exact pinned upstream revision when available.
2. Do not substitute upstream HEAD for a declared historical pin.
3. Classify it as:
   - verbatim
   - renamed only
   - minimally adapted
   - substantially forked
   - locally invented
   - provenance missing
4. Describe every material local delta.
5. Decide whether the delta is supported by:
   - official VS Code/GitHub behavior
   - the open Agent Skills specification
   - actual code, CI, security, or repository architecture
   - a documented project decision

Look specifically for unnecessary rigidity, including:

- blanket bans on delegation
- mandatory multi-phase ceremony for trivial work
- approval before every ordinary workspace write
- arbitrary maximum file counts
- arbitrary stop-after-N-failures rules
- forced personas where built-in Agent mode is sufficient
- duplicated lifecycle instructions
- rules copied into many files instead of referenced once
- policy claims not present upstream and unsupported by repository risk
- agents or skills that merely dispatch or restate another asset
- inactive assets retained only because they previously existed

Do not recommend deletion merely because something differs from upstream.
Recommend DELETE or SIMPLIFY only when the rule or asset is unsupported,
redundant, stale, unreachable, contradictory, or adds more complexity than
capability.

For every deletion candidate, identify any unique useful content that must be
preserved elsewhere. Do not silently discard unique operational knowledge.

Classify every asset:

`KEEP | FIX | SIMPLIFY | MERGE | RETIRE | DELETE | NEEDS DECISION`

Phase 5 — Skill-resource and security review

For every skill directory:

- trace all referenced scripts, references, templates, examples, schemas, and
  assets
- check that dependencies and environment requirements are documented
- check script syntax using non-mutating validation only
- do not execute a script that can write, delete, install, publish, push,
  deploy, access secrets, or contact external systems
- inspect scripts for destructive commands, unsafe globbing, command injection,
  untrusted-input execution, credential exposure, hidden downloads, unexpected
  network access, and writes outside documented paths
- verify helpful errors and edge-case handling where scripts are intended for
  execution
- verify examples match the current repository interfaces
- check that generated output paths are documented and ignored or intentionally
  tracked

If a real execution test is necessary, provide the exact command, effects,
prerequisites, cleanup, and approval needed. Mark it NOT RUN.

Phase 6 — Behavioral test design and execution

Static validity is not behavioral proof.

Create a runtime test matrix for every active skill, instruction, prompt, and
custom agent.

Use these status values only:

`PASS | FAIL | NOT RUN | USER CHECK | NOT APPLICABLE`

For each Agent Skill, define:

- discovery test
- explicit `/skill-name` test when user-invocable
- positive automatic-activation prompt when model-invocable
- near-miss negative prompt that should not activate it
- unrelated negative-control prompt
- expected resources to load
- resources that should remain unloaded
- expected fork/subagent behavior when applicable

For each custom agent, define:

- picker visibility test
- direct-selection test
- automatic/subagent invocation test
- negative routing test
- allowed-tool test
- unavailable/forbidden-tool test
- allowlist and handoff test

For each instruction file, define:

- matching-path test
- nonmatching-path test
- semantic-description activation test where applicable
- conflict/priority test

For each prompt file, define:

- slash-menu discovery
- editor play-button or slash execution
- input-variable handling
- selected agent
- effective tools after priority resolution
- expected output contract
- host compatibility

Behavioral tests must use fresh chats so prior context cannot cause false
activation. Use Chat Debug View or Agent Debug Logs to verify the actual system
prompt, context files, skill loading, tools, and agent flow.

Only mark a runtime test PASS when debug or diagnostic evidence was actually
observed. If you cannot create clean sessions or inspect the UI from this
session, output an exact test card for the user and mark USER CHECK or NOT RUN.
Do not simulate results.

Test-card columns:

`ID | asset | fresh-chat prompt | required agent/host | expected activation | forbidden activation | expected tools/resources | debug evidence to inspect | status`

Phase 7 — Repository validation

Run existing documented validation commands only when they are read-only or
have harmless, understood outputs.

Before running Docker, networked commands, commands that overwrite reports, or
any command with material side effects, list the command and its effects and
request approval.

Do not install missing tooling merely to complete the audit.

At minimum, perform safe checks such as:

- `git diff --check`
- registry-to-filesystem parity
- duplicate identifier detection
- reference resolution
- frontmatter inspection
- static script syntax checks where non-mutating
- final comparison of `git status --short` with the baseline

Output

Lead with separate verdicts:

- Static conformance
- VS Code discovery
- Behavioral activation
- Security
- Provenance
- Overall

Then provide:

1. Environment and scope
2. Complete inventory
3. Findings ordered by severity:
   - BLOCKER
   - HIGH
   - MEDIUM
   - LOW
4. Each finding must include:
   - stable ID
   - path and line
   - observed evidence
   - expected behavior
   - official or upstream source
   - impact
   - smallest reasonable remediation
   - classification: FIX/SIMPLIFY/MERGE/RETIRE/DELETE
5. Provenance-delta table
6. Reference/delegation/tool graph findings
7. Simplification and deletion candidates
8. Behavioral test matrix
9. Exact manual test cards for anything not run
10. Minimal change plan, but do not implement it
11. Commands executed and their results
12. Initial versus final working-tree status
13. Explicit limitations and unverified claims

Quality rules

- Report findings, not general impressions.
- Do not claim "clean" without showing inventory and test evidence.
- Do not treat an expected result as an observed result.
- Separate official requirements, recommendations, experimental behavior,
  repository policy, and reviewer preference.
- Prefer the smallest correction.
- Do not introduce new lifecycle layers, agents, registries, or policy documents
  unless a demonstrated gap cannot be solved by simplifying an existing asset.
- If no finding exists for a category, state what was checked and why it passed.
- Stop after the report. Make no changes.
```

## Why runtime checks are separate

A single conversation cannot reliably prove automatic activation for every
skill because earlier messages can influence later routing. Run activation and
negative-control tests in fresh sessions and use Chat Debug View or Agent Debug
Logs to verify which instructions, skills, tools, and agents were actually
loaded.

## Official references

- [Agent customization](https://code.visualstudio.com/docs/agents/concepts/customization)
- [Agent Skills in VS Code](https://code.visualstudio.com/docs/agent-customization/agent-skills)
- [Custom agents in VS Code](https://code.visualstudio.com/docs/agent-customization/custom-agents)
- [Prompt files in VS Code](https://code.visualstudio.com/docs/agent-customization/prompt-files)
- [Custom instructions in VS Code](https://code.visualstudio.com/docs/agent-customization/custom-instructions)
- [Subagents in VS Code](https://code.visualstudio.com/docs/agents/run/subagents)
- [Debug chat interactions](https://code.visualstudio.com/docs/agents/agent-troubleshooting/chat-debug-view)
- [AI security in VS Code](https://code.visualstudio.com/docs/agents/run/security)
- [Agent Skills specification](https://agentskills.io/specification)
- [GitHub Copilot customization cheat sheet](https://docs.github.com/en/copilot/reference/customization-cheat-sheet)
- [GitHub custom agents configuration](https://docs.github.com/en/copilot/reference/custom-agents-configuration)
