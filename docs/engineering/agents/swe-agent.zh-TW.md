---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
tags:
  - agents
  - software engineering
  - interfaces
aliases:
  - SWE-agent
  - Agent-Computer Interface
  - 代理電腦介面
  - 軟體工程代理
---

# SWE-agent（Yang 等人，2024）

SWE-agent 是一個語言模型代理，用來解決軟體儲存庫中的問題。它的主要貢獻是代理電腦介面（agent-computer interface，ACI）：一組為模型設計的指令，例如檢視檔案、編輯程式碼與執行測試，而不是人類工程師所用的原始終端機。Yang 等人（2024）報告，這種介面設計對代理的表現有強烈影響。

本頁是[代理工程](index.zh-TW.md)的一部分，也是本節的命名方法之一，並顯示介面與模型一樣，是可以設計的變數。

## 概述

軟體工程代理必須在龐大的儲存庫中找到相關程式碼、編輯檔案，並透過執行測試來檢查結果。當時多數代理只給模型一個標準的 shell。Yang 等人認為，語言模型代理是有自身需求與能力的新型使用者，就像人類工程師受益於整合開發環境一樣，它們也受益於為它們量身設計的介面。

## 問題

問題是介面設計如何改變代理能做的事。指令太粗會隱藏模型所需的資訊，太細則使長任務變慢。論文研究的正是這種設計對表現的影響。

## 核心想法

ACI 給代理一組小而有文件的指令。根據摘要，其關鍵功能包括：建立與編輯程式檔案、瀏覽儲存庫，以及執行測試與其他程式。這項設計的評估方式，是比較代理在不同介面下的行為，從而顯示介面如何塑造代理的步驟與結果。

## 方程式或演算法

代理執行觀察與行動的標準迴圈：

1. 透過介面讀取問題與儲存庫狀態。
2. 選擇一個指令，例如搜尋符號、開啟檔案或編輯行。
3. 讀取指令的輸出，該輸出已由介面格式化給模型。
4. 執行測試，並重複直到測試通過或達到嘗試上限。

每個指令輸出的格式本身，也是論文所研究的設計的一部分。

## 結果

摘要指出，論文在 SWE-bench 與 HumanEvalFix 上評估 SWE-agent，SWE-bench 的 pass@1 為 12.5%，HumanEvalFix 為 87.7%。作者稱這在當時兩者皆為最先進結果，遠高於先前非互動式語言模型的結果。論文也說明了介面設計如何改變代理的行為與表現。

## 限制

- **結果只限於特定基準。**結果來自 SWE-bench 與 HumanEvalFix。SWE-bench 衡量解決真實問題的能力，但未涵蓋所有軟體工作。
- **依賴模型。**結果取決於所用的語言模型，而模型會隨時間更替。
- **介面成本。**每個環境都需要設計並維護一套客製介面。
- **執行的安全性。**執行測試與程式需要沙箱，見[沙箱與電腦操作代理](sandboxing-and-computer-use.zh-TW.md)。

## 關聯

- SWE-agent 所評估的基準是 [SWE-bench](../../theory/evaluation/benchmarks/math-and-code/swe-bench.zh-TW.md)，程式基準 HumanEval 見 [HumanEval](../../theory/evaluation/benchmarks/math-and-code/humaneval.zh-TW.md)。
- 它所使用的推理與行動迴圈是 [ReAct](react.zh-TW.md)。
- 實務中的程式助理，見[AI 程式助理](../coding-assistants/index.zh-TW.md)。
- 把此類指令提供給模型的工具協定，見[工具呼叫與模型上下文協定](tool-calling-and-mcp.zh-TW.md)。

## 應用

- 在開源儲存庫中自動解決問題。
- 在持續整合中修復錯誤與修復測試。

## 開放問題

- 哪些介面特性最重要？能否在不同的軟體環境之間遷移？
- 當介面隱藏了代理所需的資訊時，代理應如何復原？

## 參考文獻

### 開創性論文

- Yang, J. 等人（2024）。*SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering*。arXiv。https://arxiv.org/abs/2405.15793 — 提出 SWE-agent 與代理電腦介面，並報告在 SWE-bench 與 HumanEvalFix 上的結果。
- Jimenez, C. E. 等人（2024）。*SWE-bench: Can Language Models Resolve Real-World GitHub Issues?*。ICLR。https://arxiv.org/abs/2310.06770 — 用於評估代理的真實 GitHub 問題基準。
- Chen, M. 等人（2021）。*Evaluating Large Language Models Trained on Code*。arXiv。https://arxiv.org/abs/2107.03374 — 提出 HumanEval，HumanEvalFix 即以此為基礎。
- Yao, S. 等人（2023）。*ReAct: Synergizing Reasoning and Acting in Language Models*。ICLR。https://arxiv.org/abs/2210.03629 — 互動式程式代理所依循的推理與行動迴圈。

### 調查與教科書

- Xi, Z. 等人（2023）。*The Rise and Potential of Large Language Model Based Agents: A Survey*。arXiv。https://arxiv.org/abs/2309.07864 — 對以 LLM 為基礎之代理的廣泛調查，涵蓋其與工具和環境的介面。
