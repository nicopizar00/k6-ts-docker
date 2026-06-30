# `ai.ingest/freeze/` — transversal Adopt Adapt freeze

A **frozen baseline snapshot** of every current Punch GitHub-Copilot asset, captured
from the working tree as source of truth. It is a **log only**: no upstream fetch, no
`compare` run, no skill upgrade, no behavior mutation. It exists so a later pass can
diff the live tree against this recorded baseline.

This sits alongside `../adopt.lock.json` (per-adopted-skill index) but is wider: the
lock tracks individual *adopted external* skills (graphify, …); this freeze records the
**whole Punch asset surface** in one file.

## File

- `punch-assets-freeze.json` — strict JSON, stdlib-consumable. Header (`schema_version`,
  `profile`, `frozen_at`, `source_of_truth`, `asset_count`) + an `assets` array, one
  row per file.

## Profile

`profile: "caveman-full"` — the baseline was frozen under the caveman **full** voice
level. Every row also carries `caveman_full: true` as the per-asset baseline marker.

## Covered sets (80 files)

| Set | Glob | `type` |
|---|---|---|
| Skills | `.github/skills/**/SKILL.md` (+ references) | `skill` / `skill-reference` |
| Prompts | `.github/prompts/*.prompt.md` | `prompt` |
| Agents | `.github/agents/*.agent.md` | `agent` |
| Instructions | `.github/instructions/*.instructions.md` | `instruction` |
| Copilot root | `.github/copilot-instructions.md`, `.github/PULL_REQUEST_TEMPLATE.md` | `global-rule` / `template` |
| Registries | `docs/ai/*.md` | `registry` |
| Existing Adopt Adapt | `ai.ingest/**` (tracked) | `adopt-adapt` |

## Row fields

`path` · `type` · `category` · `owner` (governing `punch-*` agent) · `caveman_full` ·
`sha256` · `lines` · `words` · `status` · `notes`.

- `sha256` — over raw file bytes.
- `lines` — newline count. `words` — whitespace-split token count.
- `status` — `frozen` for this snapshot. Reserved for later compare: `unchanged` /
  `changed` / `added` / `removed`.

## Provenance / regeneration

Values were computed one-shot from the working tree (sha256 + `wc`-equivalent counts).
**No generator script is committed** — the artifact is static data. `category`/`owner`
are best-effort attributions; ambiguity is recorded in `notes`, not guessed silently.
This freeze writes nothing under `.github/` — those assets are read-only here.
