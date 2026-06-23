---
name: punch-code-simplification
description: Simplifies code for clarity without changing behavior. Use during Review (the readability/simplicity axis) or Build (simplicity-first) when code works but is harder to read or extend than it should be. Stack-neutral method; CLAUDE.md is the canonical "no premature abstraction" rule.
applies-to: lifecycle/Review + Build — invoked by punch-code-review-and-quality and punch-incremental-implementation; not path-scoped
---

# Code Simplification

## In Punch

This is the **method** behind the simplicity/readability axis of
[`punch-code-review-and-quality`](../punch-code-review-and-quality/SKILL.md) (Review) and Rule 0
of [`punch-incremental-implementation`](../punch-incremental-implementation/SKILL.md) (Build).
There is no dedicated prompt — it runs inside Review or Build. Punch specifics:

- `CLAUDE.md` is the canonical rule ("no premature abstraction; three similar lines
  beat a clever helper") — this skill is the *procedure* for applying it.
- **Verify behavior is unchanged** by re-running `./bin/punch run <test>` —
  `reports/state/punch-run.json` must stay `passed: true` with no test edits.
- **Scope discipline:** simplify only what the task touched (the allowed paths);
  drive-by refactors of unrelated code are out of scope (return to Plan to broaden).

## Overview

Reduce complexity while preserving **exact** behavior. The goal is not fewer lines —
it's code easier to read, modify, and debug. Every simplification must pass: "Would
a new contributor understand this faster than the original?"

## When to Use

- After a change works but the implementation feels heavier than needed.
- During Review when readability/complexity is flagged.
- Deep nesting, long functions, unclear names, or duplication accumulated under pressure.

**When NOT to use:** code is already clear; you don't yet understand what it does;
it's performance-critical and the simpler form is measurably slower; or you're about
to rewrite the module anyway.

## The Five Principles

1. **Preserve behavior exactly.** Same inputs/outputs/side-effects/errors. If unsure
   a change preserves behavior, don't make it. All existing checks must still pass
   without modification.
2. **Follow project conventions.** Read `CLAUDE.md` and neighboring code; match its
   style. Simplification that breaks consistency is churn, not improvement.
3. **Prefer clarity over cleverness.** Explicit beats compact when compact needs a
   mental pause to parse.
4. **Maintain balance.** Over-simplification is a failure mode — don't inline a
   helper that named a concept, merge unrelated logic, or optimize for line count.
5. **Scope to what changed.** Default to recently-modified code; no unscoped
   drive-by refactors.

## The Process

### Step 1: Understand before touching (Chesterton's Fence)

Before changing anything, know why it exists: its responsibility, callers, edge
cases, the checks that define its behavior, and `git blame` context. If you can't
answer these, read more first — don't simplify.

### Step 2: Identify opportunities (concrete signals)

| Pattern | Signal | Simplification |
|---------|--------|----------------|
| Deep nesting (3+ levels) | hard to follow flow | guard clauses / early return |
| Long functions (50+ lines) | multiple responsibilities | split into focused functions |
| Nested ternaries | mental-stack to parse | if/else, or a lookup |
| Generic names (`data`, `tmp`, `res`) | no meaning | rename to the content |
| Duplicated logic (5+ lines) | repetition | extract a shared function (after the 3rd use) |
| Dead code / unused vars / commented blocks | noise | remove after confirming truly dead |
| Wrapper that adds no value | needless indirection | inline it |
| Comments restating the code | redundant | delete; keep only *why* comments |

### Step 3: Apply incrementally

One simplification at a time; re-run `./bin/punch run <test>` after each.
**Separate refactoring from behavior change** — in Punch that's a separate task
(return to Plan). The Rule of 500: a refactor touching 500+ lines wants automation,
not hand edits.

### Step 4: Verify the result

Is it genuinely easier to understand? Diff clean? If the "simpler" version is harder
to follow, revert — not every attempt succeeds.

## Example (Python orchestrator — guard clauses)

```python
# Before: nested conditionals
def classify(run):
    if run is not None:
        if run.exit_code == 0:
            if run.evidence_written():
                return "passed"
            else:
                raise EvidenceError("no punch-run.json")
        else:
            return "failed"
    else:
        raise ValueError("no run")

# After: early returns, one responsibility per branch
def classify(run):
    if run is None:
        raise ValueError("no run")
    if run.exit_code != 0:
        return "failed"
    if not run.evidence_written():
        raise EvidenceError("no punch-run.json")
    return "passed"
```

(Apply the same guard-clause / extract-helper / descriptive-name moves to k6
scenarios and the report builder — keeping k6 readable matters most when debugging a
regression at 2am.)

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "It works, no need to touch it" | Hard-to-read working code is hard to fix when it breaks. |
| "Fewer lines is always simpler" | A 1-line nested ternary isn't simpler than a 5-line if/else. Comprehension, not line count. |
| "I'll simplify this unrelated code too" | Unscoped change creates noisy diffs and regression risk. Stay in the task's paths. |
| "This abstraction might be useful later" | Speculative abstraction is complexity without value. Re-add when the 3rd use arrives. |
| "I'll refactor while adding the feature" | Separate refactor from behavior change — they're different Punch tasks. |

## Red Flags

- A "simplification" that requires editing checks/thresholds to pass (you changed behavior).
- "Simplified" code that's longer or harder to follow than the original.
- Removing error handling because it "looks cleaner".
- Renaming to personal preference rather than `CLAUDE.md` conventions.
- Refactoring outside the task's scope without being asked.

## Verification

- [ ] `./bin/punch run <test>` still `passed: true` with **no** check/threshold edits.
- [ ] Each simplification is an incremental, reviewable change.
- [ ] Follows `CLAUDE.md` conventions; no error handling weakened; no dead code left.
- [ ] The diff is clean — no unrelated changes mixed in.
