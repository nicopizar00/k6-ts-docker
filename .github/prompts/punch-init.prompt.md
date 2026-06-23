---
agent: punch-ai-governance
description: Init — one-time, non-destructive bootstrap scan that guards repo readiness for the Punch lifecycle. Runs `./bin/punch init`, surfaces every pending adoption item, reconciles what is in governance scope, and hands the rest to /punch-document. Never reconciles docs itself.
---
# Punch — Init (bootstrap & adoption guard)

**Lifecycle phase:** Init (one-time bootstrap; precedes Spec → Ship, orthogonal to it)
**Mode:** Agent — runs `./bin/punch init` (read-only scan; `--write` persists maps)
**Owner skill:** [`punch-ai-governance`](../skills/punch-ai-governance/SKILL.md)
(decision authority) + [`punch-context-engineering`](../skills/punch-context-engineering/SKILL.md)
(Graphify readiness)
**Agent:** [`punch-ai-governance`](../agents/punch-ai-governance.agent.md) — **enforced**.
Phase runs **only** under that agent's full admin over `.github/` and
`docs/` (incl. write target `docs/ai/governance/init/`). No other agent runs Init.
**Operating comms:** Caveman **`lite`**. Canon: [`punch-build-caveman`](../skills/punch-build-caveman/SKILL.md).

## When to use

Once, when repo first adopts Punch (or after major drift), to learn
whether it can safely run lifecycle. Init **prepares**; not reconcile —
ongoing doc work is [`/punch-document`](punch-document.prompt.md).

## What to do

1. **Scan.** Run `./bin/punch init --dry-run` (default) to read readiness
   summary, then `./bin/punch init --write` to persist six bootstrap maps under
   `docs/ai/governance/init/` (gitignored, disposable). `--with-graphify` for
   optional availability marker.
2. **Canon adopt-adapt report** (read-only, **required**) — run the canon
   parity pass from
   [`punch-ai-governance`](../skills/punch-ai-governance/SKILL.md): classify
   every `.github/skills/*` against the `.ai-upstream` canon and emit the parity
   table + recommendations. Flag each **adapted-in-place** skill that diffs from
   canon yet keeps an agnostic name (owes `punch-`), and list **unadopted** canon
   skills. **Report only** — never rename or adopt here. `.ai-upstream` absent →
   `canon-unavailable`; refreshing it is a user action (does not block Init).
3. **Guard pending** (see gate below) — surface every unresolved item.
4. **Reconcile in scope** — only what safely governance agent's to settle
   now (record governance key, confirm `lifecycle_templates` present). Each
   write surfaced for approval first (agent guard).
5. **Hand off** — route doc debt, feature claims, asset adaptation (incl.
   `punch-` renames + canon adoptions from step 2) to `/punch-document`; never
   do that reconciliation here.

## Guard the pending (block before the lifecycle runs)

Init = **adoption gate**. No green-light Spec → Ship until each pending
item resolved or explicitly deferred by human:

- ⛔ **`overall.status: not_ready`** (exit 1) — repo lacks structure; block adoption.
- ⚠️ **governance key `needs_confirmation`** — confirm local key (Punch stays
  template origin, never active identity).
- ⚠️ **`lifecycle_templates` missing/partial** — adopt canon from
  [`docs/ai/templates/lifecycle/`](../../docs/ai/templates/lifecycle/README.md)
  (worked example: [`docs/ai/golden-lifecycle/`](../../docs/ai/golden-lifecycle/README.md)).
- ⚠️ **assets marked `adapt`/`review`/`duplicate`** — rebind `punch-*` → local key
  / human-review before use (via `/punch-document`, not here).
- ⚠️ **adapted-in-place skills missing `punch-` prefix** — canon adopt-adapt
  report (step 2) flags any `.github/skills` adaptation that diffs from
  `.ai-upstream` canon yet keeps an agnostic name; rename via `/punch-document`,
  not here.
- ℹ️ **canon snapshot refresh / adopt** — `.ai-upstream` sync and adopt/decline
  of unadopted canon skills are **user actions**; report degrades to
  `canon-unavailable` when absent — never blocks Init.
- ⚠️ **caveman/cavecrew vendor skills missing** — Build comms + the engineer→
  cavecrew delegation chain need them installed (manual). Required Punch assets +
  install command: [`.github/.ai-upstream/README.md`](../.ai-upstream/README.md).
- ⚠️ **VS Code sub-agent setting off** — the engineer→cavecrew→worker chain needs
  `chat.subagents.allowInvocationsFromSubagents: true` in VS Code settings.
  Markdown cannot set it; warn the user. If off, the `wenyan-full`/`wenyan-ultra`
  tiers do not fire — Build still runs (Builder → one engineer, no sub-spawn).
- ℹ️ **Graphify readiness** — optional; never blocks Init.
- ℹ️ **doc/tracking debt candidates** — queue for `/punch-document`.

## Expected output

- Init readiness summary: governance key + source, `overall.status`,
  readiness table, exit code.
- **canon adopt-adapt parity** verdict (clean / N owe `punch-` prefix) +
  unadopted-canon list (or `canon-unavailable`).
- **pending guard list** above with each item state (resolved / deferred).
- One next command: `/punch-document` (reconcile) or first lifecycle phase
  (`/punch-spec`) once `adoption_ready`/`document_ready`.

## Boundary rules (non-destructive)

- Init **never** renames, deletes, or rewrites existing files; only writes its
  own disposable maps under output dir.
- **Not** doc reconciliation, full feature classification, or lean
  cleanup — those are `/punch-document`.
- Runs **read-only** `./bin/punch init` only — never Punch runtime
  (`./bin/punch run`, Docker, k6).

## Validation gate

Init succeeds when `./bin/punch init` exits `0` and six maps generated.
`overall.status: not_ready` (exit 1) **blocks** adoption until pending items
resolved.
