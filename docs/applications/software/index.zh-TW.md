# 軟體開發

軟體工程是受 LLM 影響最深的領域之一，因為程式碼是大量的訓練資料，而且輸出可以自動測試。

## 工具的演進

| 世代 | 例子 | 能力 |
|---|---|---|
| 自動完成 | IntelliSense、早期的機器學習補全 | 下一個 token 或識別字 |
| 行內程式碼生成 | GitHub Copilot（2021） | 依上下文產生數行或整個函式 |
| 聊天助理 | IDE 中的 ChatGPT、Claude、Gemini | 依要求解釋、重構、除錯 |
| AI 原生編輯器 | Cursor、Windsurf 等 | 結合程式碼庫脈絡進行多檔案編輯 |
| 程式碼代理人 | Claude Code、OpenAI Codex、GitHub Copilot 程式碼代理人、Devin、Jules | 自主完成多步驟任務：讀取儲存庫、編輯、執行測試、開 Pull Request |

## 基準評測

| 基準 | 衡量內容 |
|---|---|
| HumanEval／MBPP | 依文件字串撰寫短函式（現已飽和） |
| SWE-bench／SWE-bench Verified | 解決 Python 儲存庫中真實的 GitHub issue |
| LiveCodeBench、Codeforces 評分 | 競賽程式設計，且能抵抗資料污染 |
| Terminal-Bench 及其他代理式套件 | 在真實環境中工作 |


## 生產力證據

- 受控的任務研究在定義清楚的任務上發現速度提升，使用 Copilot 時（Peng et al., 2023）
- 大型公司的現場實驗發現，完成的任務數有實質增加，且對經驗較少的開發者效果更大（Cui et al., 2024）
- 一項隨機試驗讓有經驗的開源開發者在自己成熟的儲存庫上工作，結果發現使用 2025 年初的 AI 工具後，他們反而慢了約 19%，儘管他們認為自己變快了（Becker et al., 2025）。效果很大程度取決於任務、程式碼庫與經驗

## 有效的做法

- 給代理人清楚的規格、測試與儲存庫脈絡（例如描述慣例的 CLAUDE.md／AGENTS.md）
- 由人類審閱差異（diff），並要求測試通過
- 把工作拆成小而可驗證的步驟
- 為代理人使用沙箱與最小權限的憑證
- 追蹤缺陷與安全性指標，而不只是開發速度

## 風險

- 隱晦的錯誤與不安全的程式碼；幻覺出來的套件名稱，攻擊者可能註冊這些名稱
- 生成程式碼的授權與來源疑慮
- 技能退化，對學習者尤其明顯
- 大量生成程式碼造成的可維護性負債
- 代理人安全：透過 issue、註解或相依套件進行的提示注入（見[資訊安全](../cybersecurity/index.md)）

## 寫程式以外

需求分析、測試生成、程式碼審閱、舊程式碼遷移（例如從 COBOL 遷移到 Java）、文件撰寫、事件應變、形式化驗證的輔助。

## 關鍵方法

下列三種方法與本頁最相關。每一項都連結到解釋該方法的頁面。

- [代理人](../../theory/models/agents/index.md)：能讀取儲存庫、編輯檔案並執行測試的程式設計代理人，如 SWE-bench 所評測者（Jimenez et al., 2023）。
- [Transformer](../../theory/models/transformer/attention-is-all-you-need/index.md)：Codex 等程式碼模型背後的架構（Chen et al., 2021）。
- [InstructGPT 與 RLHF](../../theory/models/llm/instructgpt-rlhf/index.md)：IDE 中聊天式助手背後的指令微調（Ouyang et al., 2022）。

## 參考文獻

### 開創性論文

- Chen et al. (2021). Evaluating Large Language Models Trained on Code. arXiv. https://arxiv.org/abs/2107.03374 — 提出 Codex 模型與由文件字串撰寫函式的 HumanEval 基準。
- Peng et al. (2023). The Impact of AI on Developer Productivity: Evidence from GitHub Copilot. arXiv. https://arxiv.org/abs/2302.06590 — 受控實驗，發現使用 Copilot 能加快任務完成速度。
- Cui et al. (2024). The Effects of Generative AI on High Skilled Work: Evidence from Three Field Experiments with Software Developers. *SSRN*. https://doi.org/10.2139/ssrn.4945566 — 大型企業中的田野實驗，衡量 AI 輔助對開發者的影響。
- Becker et al. (2025). Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity. arXiv. https://arxiv.org/abs/2507.09089 — 隨機試驗發現，有經驗的開發者使用 AI 工具後反而變慢，儘管他們預期會變快。
- Jimenez et al. (2023). SWE-bench: Can Language Models Resolve Real-World GitHub Issues? arXiv. https://arxiv.org/abs/2310.06770 — 取自 Python 儲存庫真實 GitHub 議題的基準。
- Vaswani, A. et al. (2017). *Attention Is All You Need*. NeurIPS. https://arxiv.org/abs/1706.03762 — 提出 Transformer，以多頭自注意力為核心。
- Ouyang, L. et al. (2022). Training language models to follow instructions with human feedback. NeurIPS. https://arxiv.org/abs/2203.02155 — InstructGPT，以人類偏好回饋進行指令微調。
