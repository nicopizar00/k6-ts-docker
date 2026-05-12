# AI Context

This file helps AI assistants understand the project philosophy and constraints.

## Read this first

1. `CLAUDE.md` — Rules for all changes.
2. This file — Why the project is shaped the way it is.
3. `architecture.md` — Folder map and execution chain.
4. `how-to-run.md` — Commands to build and run.

## Philosophy

**Small, reviewable, linear.** The execution chain is strictly: TypeScript → bundle → Docker → run → report. Every change should fit this flow. Do not add parallel paths, shortcuts, or hidden steps.

**No premature abstraction.** Three similar lines are better than a clever helper. If adding a helper, confirm it's needed for a third real use case.

**No unnecessary dependencies.** Every dependency must earn its place. Standard library or a few lines of code suffice? Use those.

**AI-friendly.** File names, directory layout, and scripts are self-describing. Avoid hidden conventions.

## Constraints

- **k6 runtime limitation** — k6 cannot require Node modules. Tests must be bundled to a single ES module. esbuild handles this.
- **Execution chain is sacred** — Do not shortcut, branch, or skip steps. The chain is: source → bundle → Docker → execution.
- **No abstractions ahead of use** — Wait for the third real scenario before extracting a helper.

## Before adding anything

Ask:
- Does it fit the execution chain?
- Is it necessary, or does code/stdlib suffice?
- Is it a premature abstraction?
- Does the structure in `CLAUDE.md` have room for it?

If uncertain, ask before implementing.

## Common tasks

**Adding a test scenario:** Create `src/tests/mytest.ts`. Follow k6 conventions (see `smoke.ts`). Build it separately or extend the bundling config.

**Changing the bundler:** Only if esbuild stops working. Document the decision in this file. Ensure single-bundle-file output is preserved.

**Adding a dependency:** Justify in a comment in `package.json`. Consider whether it's truly necessary.

**Changing the Docker image:** Document in `docs/architecture.md` why. The image must run the bundled script unchanged.

## Decision log

- **esbuild as bundler** — Lightweight, fast, minimal config. Single-file output matches k6's needs.
- **Docker Compose** — Simple orchestration for local and CI runs; keeps build and run commands readable.
- **No GitHub Actions yet** — CI workflow is a separate task to avoid scope creep. Will be added when tests are stable.
