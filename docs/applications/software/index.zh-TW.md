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

SWE-bench Verified 的分數從 2023 年的幾個百分點，到 2025 年領先的代理人已能完成超過一半的任務。

## 生產力證據

- 受控的任務研究發現，在定義清楚的任務上速度大幅提升（例如 Copilot 在一項 HTTP 伺服器任務上快約 56%，Peng et al., 2023）
- 大型公司的現場實驗發現，完成的任務數有實質增加，且對經驗較少的開發者效果更大（Cui et al., 2024）
- 一項隨機試驗讓有經驗的開源開發者在自己成熟的儲存庫上工作，結果發現他們使用 2025 年初的 AI 工具後反而慢了約 19%，儘管他們自認變快了（METR, 2025）——效果高度取決於任務、程式碼庫與經驗

## 有效的做法

- 給代理人清楚的規格、測試與儲存庫脈絡（例如描述慣例的 CLAUDE.md／AGENTS.md）
- 由人類審閱差異（diff），並要求測試通過
- 把工作拆成小而可驗證的步驟
- 為代理人使用沙箱與最小權限的憑證
- 追蹤缺陷與安全性指標，而不只是開發速度

## 風險

- 隱晦的錯誤與不安全的程式碼；幻覺出來的套件名稱（「slopsquatting」）
- 生成程式碼的授權與來源疑慮
- 技能退化，對學習者尤其明顯
- 大量生成程式碼造成的可維護性負債
- 代理人安全：透過 issue、註解或相依套件進行的提示注入（見[資訊安全](../cybersecurity/index.md)）

## 寫程式以外

需求分析、測試生成、程式碼審閱、舊程式碼遷移（例如從 COBOL 遷移到 Java）、文件撰寫、事件應變、形式化驗證的輔助。

## 學習資源

- [SWE-bench](https://www.swebench.com/)
- Anthropic，"Building effective agents"；Claude Code 與 OpenAI Codex 的文件
- METR (2025), "Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity"
