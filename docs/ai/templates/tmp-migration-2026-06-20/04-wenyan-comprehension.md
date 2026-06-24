# 04 · 文言誤讀險 · 雙語 · 翻譯（wenyan comprehension risk）

> ⚠ IDEA scratch。Render OK ≠ comprehension OK。README 已警。

文言(wenyan)之險,易漏：

- **Copilot 誤讀**：範本散文皆文言。Render 無誤(UTF-8、GFM),然 Copilot **語義**或誤判古漢。考：關鍵戒律(security、boundary)宜雙語或英,勿純文言。
- **雙語鏡照**：resolve snapshot + prompt 加一行英 gloss 於文言標題下。考：保 house style 又予 Copilot 明錨。成本低,值。
- **persistent vs output**：canon 雲「wenyan forbidden in persistent artifacts(docs/ADR/prompt/skill)」。考：範本 assets 自身即文言 prompt —— 與 canon 衝！assets = 特例(export template)否？文清此例外,免後人困。
- **團隊母語**：採隊讀文言否？考：非華語隊 → 翻譯為英/本地語,或保英 gloss。
- **CJK 字型/終端**：terminal 渲 CJK 否？等寬對齊亂否？考：報告若入 terminal,fullwidth 標點破表。
- **搜尋/grep**：文言鍵不易 grep(無空格分詞)。考：英 anchor 助檢索。
- **diff 可讀**：PR review 文言 diff 難審。考：reviewer 英摘。
- **模型漂移**：他 LLM(若日後採)更弱於文言。考：Copilot-only 假設鎖否。
- **caveman 與 wenyan 混**：`caveman-wenyan` 雙壓 → 更密、更難解。考：壓過頭傷可用性。trade-off。

> ⚠ Miss → Copilot「讀」文言戒律卻誤行。Render pass,behavior fail。最隱之險。
