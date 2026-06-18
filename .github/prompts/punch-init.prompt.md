---
agent: punch-ai-governance
description: Init — one-time, non-destructive bootstrap scan that guards repo readiness for the Punch lifecycle. Runs `./bin/punch init`, surfaces every pending adoption item, reconciles what is in governance scope, and hands the rest to /punch-document. Never reconciles docs itself.
---

# Punch — Init (bootstrap & adoption guard)

**Lifecycle phase:** Init (one-time bootstrap; precedes Spec → Ship, orthogonal to it)
**Mode:** Agent — runs `./bin/punch init` (read-only scan; `--write` persists maps)
**Owner skill:** [`punch-ai-governance`](../skills/punch-ai-governance/SKILL.md)
(the decision authority) + [`punch-context-engineering`](../skills/punch-context-engineering/SKILL.md)
(Graphify readiness)
**Agent:** [`punch-ai-governance`](../agents/punch-ai-governance.agent.md) — **enforced**.
This phase runs **only** under that agent's complete admin over `.github/` and
`docs/` (incl. the write target `docs/ai/governance/init/`). No other agent may run Init.
**Operating comms:** Caveman **`lite`**; evidence (readiness, exit codes, the
generated maps) quoted verbatim. Canon: [`punch-build-caveman`](../skills/punch-build-caveman/SKILL.md).

## When to use

Once, when a repository first adopts Punch (or after a major drift), to learn
whether it can safely run the lifecycle. Init **prepares**; it does not reconcile —
the ongoing documentation work is [`/punch-document`](punch-document.prompt.md).

## What to do

1. **Scan.** Run `./bin/punch init --dry-run` (default) to read the readiness
   summary, then `./bin/punch init --write` to persist the six bootstrap maps under
   `docs/ai/governance/init/` (gitignored, disposable). `--with-graphify` for the
   optional availability marker.
2. **Guard pending** (see the gate below) — surface every unresolved item.
3. **Reconcile in scope** — only what is safely the governance agent's to settle
   now (record the governance key, confirm `lifecycle_templates` present). Each
   write is surfaced for approval first (agent guard).
4. **Hand off** — route documentation debt, feature claims, and asset adaptation to
   `/punch-document`; never do that reconciliation here.

## Guard the pending (block before the lifecycle runs)

Init is the **adoption gate**. Do not green-light Spec → Ship until each pending
item is resolved or explicitly deferred by a human:

- ⛔ **`overall.status: not_ready`** (exit 1) — repo lacks structure; block adoption.
- ⚠️ **governance key `needs_confirmation`** — confirm the local key (Punch stays
  the template origin, never the active identity).
- ⚠️ **`lifecycle_templates` missing/partial** — adopt the canon from
  [`docs/ai/templates/lifecycle/`](../../docs/ai/templates/lifecycle/README.md)
  (worked example: [`docs/ai/golden-lifecycle/`](../../docs/ai/golden-lifecycle/README.md)).
- ⚠️ **assets marked `adapt`/`review`/`duplicate`** — rebind `punch-*` → local key
  / human-review before use (via `/punch-document`, not here).
- ℹ️ **Graphify readiness** — optional; never blocks Init.
- ℹ️ **doc/tracking debt candidates** — queue for `/punch-document`.

## Expected output

- The Init readiness summary: governance key + source, `overall.status`, the
  readiness table, exit code — verbatim.
- The **pending guard list** above with each item's state (resolved / deferred).
- One next command: `/punch-document` (reconcile) or the first lifecycle phase
  (`/punch-spec`) once `adoption_ready`/`document_ready`.

## Boundary rules (non-destructive)

- Init **never** renames, deletes, or rewrites existing files; it only writes its
  own disposable maps under the output dir.
- It is **not** documentation reconciliation, full feature classification, or lean
  cleanup — those are `/punch-document`.
- It runs the **read-only** `./bin/punch init` only — never the Punch runtime
  (`./bin/punch run`, Docker, k6).

## Validation gate

Init succeeded when `./bin/punch init` exits `0` and the six maps are generated.
`overall.status: not_ready` (exit 1) **blocks** adoption until the pending items
are resolved.
