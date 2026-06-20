# `.github/assets` — GitHub Copilot VS Code 治理範本（Hub-Spoke）

此目錄為**範本包**（template）。專供「未入治理」之倉採用，使 GitHub Copilot VS Code 得最小可運之治理面。範本不自動生效。

## ⚠ 警（caveman ultra）

> ⚠ TEMPLATE only. Human adapt before use. No ship as-is.
> ⚠ Target = GitHub Copilot VS Code ONLY. Other host no guarantee.
> ⚠ Prose = wenyan. Copilot may misread classical Chinese. Team review/translate first.
> ⚠ CAVEMAN / GRAPHIFY / AGENT-SKILL = external opt tools. NOT installed here. Install local host self. No real steps given.
> ⚠ Edit = human job. Fit to own repo rules after copy.

## 採用之法（adopt）

範本居 `.github/assets/`，不自動生效。採用者手移檔至真位：

| 範本 | 真位（adopt 後） |
|------|------------------|
| `assets/copilot-instructions.md` | `.github/copilot-instructions.md` |
| `assets/instructions/*.instructions.md` | `.github/instructions/` |
| `assets/prompts/*.prompt.md` | `.github/prompts/` |
| `assets/CLAUDE.md` | 倉根 `CLAUDE.md` |
| `assets/AGENTS.md` | 倉根 `AGENTS.md` |

移後，依本倉實情改 `<...>` 佔位。

## Hub-Spoke 構

- 中樞（hub）：`copilot-instructions.md` — always-on，唯載戒律與連。
- 輻（spoke）：`instructions/`、`prompts/`、`CLAUDE.md`、`AGENTS.md` — 細則居此。
- 改則改輻，中樞但連，勿復述。

## 啟（init）

入治理之門 = `/punch-init` prompt（`prompts/punch-init.prompt.md`）。於 GitHub Copilot VS Code Agent Mode 執之，掃倉、繪備度、引採此範本。非破壞，dry-run 為默。
