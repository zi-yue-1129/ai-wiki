---
translation_reviewed: 2026-10-28
---

# Darwin Gödel Machine（Zhang 等人，2025）

Darwin Gödel Machine（DGM）是一個程式碼代理人，它會修改自己的程式碼，以基準測試檢驗每一次修改，並把有效的修改保存在一個不斷成長的檔案庫中。Jenny Zhang 及其同事於 2025 年發表此方法。它是父頁面[AI 用於 AI 研究](../index.md)中的自我改進方法。

## 概述

自我改進 AI 的想法由來已久。Schmidhuber（2003）描述了一台哥德爾機，它在找到證明某次改寫有益之後，才會改寫自身程式碼的任何部分。Zhang 等人（2025）指出，要證明大多數修改有益，在實際上是不可能的。DGM 以實證驗證取代證明：每一次修改都以執行程式設計基準來判斷。

它的設計借鑑了達爾文演化與開放式演化的研究。它不只保留最佳的代理人，而是保存一個多樣化的檔案庫，使搜尋空間中的許多不同路徑能夠同時探索。相關工作包括 ADAS（Hu 等人，2024），它在以程式碼撰寫的代理人設計中進行搜尋；以及演化式程式碼代理人 AlphaEvolve（Novikov 等人，2025）。較早的自我改進系統 STOP（Zelikman 等人，2023）改進了呼叫語言模型的程式，但沒有改變模型本身。[演化方法](../../../theory/paradigms/evolutionary/index.md)是此搜尋策略的一般背景。

## 關鍵概念

- **哥德爾機**：一種理論上的自我改進者，只有在能證明某項修改有益時才會改變自身的程式碼。
- **檔案庫**：到目前為止所產生的代理人的儲存集合。每個新代理人都是較早代理人的子代，因此檔案庫會成長為一棵樹。
- **自我修改**：代理人編輯自身的程式碼，其中也可以包括它用來進行後續編輯的工具。
- **實證驗證**：一項修改是否保留，取決於它在程式設計基準上的結果，而不是取決於證明。
- **開放性**：搜尋偏好多樣化的代理人，而不只是分數最高的代理人，因此死路仍可能通向其他地方。

## 運作方式

循環的簡化版本如下：

1. 以初始程式代理人開始建立檔案庫。
2. 從檔案庫中抽樣一個代理人。抽樣並不限於最佳代理人。
3. 請基礎模型透過修改程式碼，建立該抽樣代理人的新版本。報告中的修改包括更好的程式碼編輯工具、更好的長上下文管理，以及同儕審查機制。
4. 在 SWE-bench 與 Polyglot 等程式設計基準上執行新代理人。
5. 若新代理人能執行並取得分數，就將其加入檔案庫，然後從第 2 步重複。

以符號表示，設 $A$ 為檔案庫、$M$ 為基礎模型、$\mathrm{eval}$ 為基準分數，則：

$$
p \sim A, \qquad c = M(p), \qquad A \leftarrow A \cup \{c\} \text{ 若 } c \text{ 能執行且 } \mathrm{eval}(c) \text{ 有定義}
$$

保留子代的規則是簡化版本。論文中父代的選擇更為複雜。

## 結果

摘要報告，DGM 將 SWE-bench 的表現從 20.0% 提升至 50.0%，並將 Polyglot 的表現從 14.2% 提升至 30.7%。摘要指出，DGM 明顯勝過沒有自我改進，或沒有開放式探索的基準方法。這些改進來自代理人程式碼的修改，例如更好的編輯工具。所有實驗都在安全防護下進行，包括沙箱與人工監督。

## 限制

- **範圍狹窄。** 收益是在程式設計基準上衡量的，也就是代理人所改進的那類任務。它們並不能說明一般性的自我改進。
- **基準過度擬合。** 依基準挑選修改，可能使代理人只適配該基準。在保留的任務上的結果更為重要。
- **需要大量評估。** 每一個新代理人都必須在基準上執行，因此此方法需要大量運算。
- **自我修改的安全性。** 會重寫自身的程式碼必須在隔離環境中執行。作者使用了沙箱與人工監督，任何此類系統都需要相當的防護。參見[沙箱與電腦使用](../../../engineering/agents/sandboxing-and-computer-use/index.md)。

## 開放問題

- 以檔案庫為基礎的搜尋在長時間執行後是否仍持續改進，還是會停滯？
- 對程式設計代理人的改進，能否遷移到其他類型的任務？
- 隨著代理人的程式碼變得更複雜，人類是否仍能稽核每一次自我修改？
- 結果在多大程度上取決於該基準是否為真實軟體品質的良好代理指標？

## 參考文獻

### 開創性論文

- Zhang, J. 等人（2025）。Darwin Godel Machine: Open-Ended Evolution of Self-Improving Agents。arXiv。https://arxiv.org/abs/2505.22954 — 經基準實證驗證的自我修改程式代理人，將 SWE-bench 的表現從 20.0% 提升至 50.0%。
- Schmidhuber, J.（2003）。Goedel Machines: Self-Referential Universal Problem Solvers Making Provably Optimal Self-Improvements。arXiv。https://arxiv.org/abs/cs/0309048 — 提出一種自我參照的求解器，只有在證明改寫有益之後才改寫自身程式碼。
- Zelikman, E. 等人（2023）。Self-Taught Optimizer (STOP): Recursively Self-Improving Code Generation。arXiv。https://arxiv.org/abs/2310.02304 — 語言模型改進呼叫它的鷹架程式，作者並討論這一步的限制。
- Hu, S., Lu, C. & Clune, J.（2024）。Automated Design of Agentic Systems。arXiv。https://arxiv.org/abs/2408.08435 — 提議以自動搜尋取代手工設計，搜尋以程式碼撰寫的代理式系統設計。

### 文章與文件

- Novikov, A. 等人（2025）。AlphaEvolve: A coding agent for scientific and algorithmic discovery。arXiv。https://arxiv.org/abs/2506.13131 — 關於一套演化式程式碼代理人的白皮書，該代理人透過自動評估器改進演算法。
