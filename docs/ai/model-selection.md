# Model Selection

This guide is model-agnostic and tool-agnostic. It does not pin specific
vendor model names. Use it to decide *which class* of model fits *which
phase* — adapt to whatever your team has access to.

## Match the model to the phase

| Phase | Cognitive load | Suggested model class |
|---|---|---|
| Spec     | High — clarifying the request (former Define), then translating ambiguity into constraints | Strongest reasoning model |
| Plan     | High — partitioning work, predicting risks | Strongest reasoning model |
| Build    | Medium — execution within a defined scope | Strong coding model |
| Verify   | Low — running commands, reading results | Fast / cheap model is fine |
| Review   | High — adversarial reading | Strongest reasoning model |
| Ship     | Low — mechanical git/gh actions | Fast / cheap model is fine |

## Why bias toward reasoning models in Spec / Plan / Review

These phases drive every downstream decision. Cheaping out here is a false
economy — a poorly-shaped Plan multiplies Build cost. The cost saved on a
weaker reasoning model is paid many times over in Build / Verify cycles.

## Why a coding-capable model for Build

Build needs precision over allowed paths, awareness of the surrounding
file's style, and reliable diff editing. A reasoning model that lacks
strong code-editing reliability will produce diffs that pass review but
fail Verify.

## Why a fast / cheap model is fine for Verify and Ship

Verify mostly:

- Runs commands.
- Reads exit codes and JSON.
- Reports pass/fail.

Ship is purely:

- `git add`, `git commit`, `git push`, `gh pr create`.

Neither needs a long reasoning chain. Reserve budget for the planning
phases.

## Keep the model stable within a phase

Mid-phase model swaps cause subtle drift:

- Two different models can produce two different Plans for the same Spec.
- Two different models can choose different abstractions during Build,
  producing a diff that looks inconsistent with itself.

The rule: **lock the model for the duration of one phase**. Swap only at
phase boundaries (and document the swap in the PR description if it
matters).

## Don't mix models inside one implementation task

A "task" here means one Plan → one Build → one Verify cycle. Treat the
trio as a unit. Mixing models inside a task tends to:

- Break naming conventions across slices.
- Re-litigate decisions the previous slice already made.
- Cause Review to flag "internally inconsistent diff" that is really
  "two-model fingerprint".

## Cost shape (rule of thumb)

Across a complete lifecycle (Spec → Ship) on a real task:

- ~60% of *cognitive* effort sits in Spec + Plan + Review.
- ~30% sits in Build (often spread across multiple Build calls).
- ~10% sits in Verify + Ship.

A model-allocation budget that follows this distribution tends to produce
the most reliable outcomes. Inverting it (cheap planner, expensive shipper)
is the most common anti-pattern.

## Worked example

For a small Python orchestrator task:

- Spec / Plan / Review: strong reasoning model.
- Build (one `punch-build-orchestrator` call): strong coding model.
- Verify (`./bin/punch doctor`, `./bin/punch run smoke`, read JSON):
  fast model.
- Ship (commit, push, PR): fast model.

For a multi-task integration (e.g. new test + new compose service + new
orchestrator subcommand):

- Spec / Plan: strong reasoning model.
- Build O-01, Build C-01, Build K-01: strong coding model, **same model
  across all three Build calls** to avoid cross-slice drift.
- Verify: fast model.
- Review: strong reasoning model.
- Ship: fast model.
