---
translation_reviewed: 2026-10-28
---

# GPT-3：從提示中進行少樣本學習（Brown 等人，2020）

一個 1,750 億參數的自回歸 Transformer，以提示中的零、一或少數範例進行測試，且不針對該任務微調。

## 概述

過去讓語言模型學會新任務，通常需要該任務的微調資料集。GPT-3 論文問的是：一個夠大的語言模型，能否只靠提示中寫入的幾個範例學會該任務，完全不更新權重。論文的答案是，對許多任務來說可以，並測量了其能力的範圍。

## 關鍵概念

- **自回歸 Transformer**：根據前面的 token 預測下一個 token 的模型。
- **零樣本（zero-shot）**：提示中只描述任務，不提供範例。
- **單樣本（one-shot）**：在新輸入之前，提示中放入一個範例。
- **少樣本（few-shot）**：在新輸入之前，提示中放入少量範例。
- **情境學習（in-context learning）**：從提示中學會任務，不需梯度更新。

## 問題

語言模型能否只靠提示中的少量範例學會新任務，而不需要任何梯度更新？

## 核心想法

將自迴歸 Transformer 擴大到 1,750 億參數，並在提示中提供零個、一個或少數幾個範例來測試。模型並未針對該任務微調。

## 運作方式

提示中包含任務描述與幾組輸入–輸出配對。模型接著續寫文字，其續寫即被讀為答案。網路本身不會改變，因此同一個模型只要改變提示，就能切換任務。

## 核心方法

論文在同一個模型上比較三種提示設定。它把這些設定與針對任務特定資料集的微調相比，而摘要指出，先前的方法需要這樣的微調。三種設定是零樣本、單樣本與少樣本，差別只在提示中範例的數量。

## 演算法

1. 在提示中寫入任務描述與幾組輸入–輸出範例。
2. 接上新的輸入。
3. 讓模型逐個 token 生成輸出。權重不變。

## 結果

- 摘要指出，GPT-3 在許多 NLP 資料集上表現強勁，包括翻譯、問答與填空任務。
- 摘要也指出，它在需要即時推理或領域適應的任務上有良好表現，例如重新排列字母、在句子中使用新詞，或進行 3 位數的算術。

## 限制

- 摘要指出，有些資料集上 GPT-3 的少樣本學習仍然吃力。
- 摘要也指出，有些資料集上 GPT-3 面臨與大型網路語料訓練相關的方法學問題。
- 摘要說明，先前的方法仍需要數千至數萬筆的任務特定微調資料。GPT-3 降低了這個需求，但並非在每項任務上都能免除。

## 變體與更多變體

- **零樣本**：只描述任務，不示範。
- **單樣本**：只展示一個範例。
- **少樣本**：展示數個範例，論文以此設定作為主要的少樣本結果。

## 連結

- 母頁：[大型語言模型](../index.md)
- 同一主題的另一方法：[運算最佳化訓練](../compute-optimal-training/index.md)
- 同一主題的另一方法：[InstructGPT 與 RLHF](../instructgpt-rlhf/index.md)

## 應用

- 以單一的通用模型進行翻譯、問答等任務，不必為每項任務訓練新模型。
- 以幾個範例快速建立新任務的原型，再決定是否值得花成本微調。

## 開放問題

- 哪些任務能從情境範例中獲益，哪些仍需要微調？
- 效能有多少來自訓練資料，又有多少來自情境學習本身？

## 參考文獻

### 開創性論文

- Brown, T. B., et al.（2020）。*Language Models are Few-Shot Learners*. arXiv. https://arxiv.org/abs/2005.14165 — GPT-3 論文，顯示 1,750 億參數的模型能從提示中給出的少量範例學會新任務。
- Kaplan, J., et al.（2020）。*Scaling Laws for Neural Language Models*. arXiv. https://arxiv.org/abs/2001.08361 — 顯示隨著模型大小、資料與運算量增加，損失如何可預測地下降，這是擴大到 1,750 億參數的趨勢依據。
- Hoffmann, J., et al.（2022）。*Training Compute-Optimal Large Language Models*. arXiv. https://arxiv.org/abs/2203.15556 — Chinchilla 研究，主張在固定運算預算下，模型大小與訓練 token 數應該同步成長。
- Ouyang, L., et al.（2022）。*Training language models to follow instructions with human feedback*. arXiv. https://arxiv.org/abs/2203.02155 — InstructGPT，透過以人類回饋微調，使語言模型符合使用者意圖。
- Wei, J., et al.（2022）。*Chain-of-Thought Prompting Elicits Reasoning in Large Language Models*. arXiv. https://arxiv.org/abs/2201.11903 — 顯示要求模型寫出中間推理步驟，可改善多步驟問題的解題能力。

### 綜述與教科書

- Zhao, W. X., et al.（2023）。*A Survey of Large Language Models*. arXiv. https://arxiv.org/abs/2303.18223 — 對 LLM 的預訓練、適應與評估進行廣泛綜述，並附有模型時間線。

## 延伸學習

- Hugging Face. *LLM Course*. https://huggingface.co/learn/llm-course — 使用 Hugging Face 函式庫來使用、微調與建構 LLM 的實作課程。
- Karpathy, A. (2023). *[1hr Talk] Intro to Large Language Models*. YouTube. https://www.youtube.com/watch?v=zjkBMFhNj_g — 一小時、非技術性的概述，介紹 LLM 如何訓練、能做什麼、在哪裡失敗。
