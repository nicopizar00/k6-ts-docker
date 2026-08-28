# `.github/.ai-upstream/` — gitignored upstream staging

Local, gitignored staging area for **upstream snapshots** Punch compares
against or adapts from — never a Punch prerequisite, never fetched or
refreshed automatically. Refreshing any snapshot here is an explicit,
manual **user action**; nothing in `.github/` runs the network fetch for you.

Current snapshots:

- `agent-skills/` — the pinned upstream `agent-skills` commit Punch adapted
  its lifecycle skills/personas from. Provenance, adoption dispositions, and
  refresh discipline live in
  [`agent-skills-provenance.md`](../../docs/ai/agent-skills-provenance.md).

## Sub-agent setting

`chat.subagents.allowInvocationsFromSubagents` stays at its default (`false`).
No Punch agent currently lists sub-agents — `punch-builder` implements
directly, and Ship's fan-out lives in the `punch-ship` prompt itself, not a
coordinator persona. Full delegation canon: [`agent-guards.md`](../../docs/ai/agent-guards.md).

## Rules

- **Keep upstream snapshots verbatim.** They are drift-diff baselines, never
  hand-edited.
- `punch-ai-governance` excludes `.ai-upstream/**` from naming / duplication /
  stale-asset checks — it is frozen provenance, not a live asset.
