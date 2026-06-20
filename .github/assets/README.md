# `.github/assets` — GitHub Copilot Chat 匯出範本（VS Code · Hub-Spoke）

最小範本,使 `.github` GitHub Copilot 資產可作 VS Code GitHub Copilot Chat 範本匯出。匯出 = copy-paste `.github/` + `docs/ai/`。唯一標的 = **GitHub Copilot VS Code**。

## ⚠ 警（caveman ultra）

> ⚠ TEMPLATE only. Human adapt before use. No ship as-is.
> ⚠ Target = GitHub Copilot VS Code Chat ONLY. Other tool (Claude/Codex/agent) NOT in scope.
> ⚠ resolve/ stub = link-fix only, NOT real content. Human fill on adopt.
> ⚠ Prose = wenyan. Copilot may misread classical Chinese. Team review first.

## 內容（essentials）

### Copilot Chat native 資產

| 範本 | 真位（adopt 後） |
|------|------------------|
| `copilot-instructions.md` | `.github/copilot-instructions.md`（中樞 hub） |
| `instructions/governance.instructions.md` | `.github/instructions/`（輻,`applyTo: '**'`） |
| `prompts/punch-init.prompt.md` | `.github/prompts/`（AI 治理代理） |

### `resolve/` — 倉內出域文鏈 stub

匯出時,`docs/ai/` 外被引之倉內文 → 斷。鏡射真路補之。

| 出域標的（引處數） | resolve/ 鏡射 |
|--------------------|---------------|
| `docs/architecture/punch-boundaries.md`（7） | `resolve/docs/architecture/punch-boundaries.md` |
| `docs/workflows/validation.md`（2） | `resolve/docs/workflows/validation.md` |

## Hub-Spoke

中樞(hub)= `.github/copilot-instructions.md`,唯載戒律與連。輻載細則。改則改輻,勿復述。

## 範圍外（out of scope · 不解）

> ⚠ NOT resolved (intentional lean): root CLAUDE.md / AGENTS.md / CODEX.md (other tools); .ai-upstream caveman / graphify (external — official guide, install local host self). Links to these stay dangling on export; fix on maintenance.
> ⚠ Pre-existing broken ref: `docs/ai/history/agent-skills-absorption-plan.md:59` — off-by-one `../../` → `../../../`. Fix at source.
