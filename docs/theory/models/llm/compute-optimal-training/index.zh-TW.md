---
translation_reviewed: 2026-10-28
---

# 運算最佳化訓練（Hoffmann 等人，2022）

在固定的運算預算下，透過跨多次訓練的擬合，找出最佳的模型大小與訓練 token 數。此論文即 Chinchilla 研究，主張模型大小與訓練 token 數應該一起擴展。

## 概述

訓練大型語言模型需要運算，這筆預算可以花在更大的模型、更多的資料，或兩者之上。Hoffmann 等人問的是：固定的預算應如何分配，才能得到最好的最終模型，並以跨多次訓練的實證擬合來回答。

## 關鍵概念

- **運算預算（compute budget）**：訓練的總運算量，隨參數數量乘以訓練 token 數而增長。
- **訓練 token**：模型在訓練期間看過的文字數量。
- **擴展定律（scaling law）**：模型大小、資料與損失之間的擬合關係，用來選擇預算的分配方式。
- **運算最佳化（compute-optimal）**：在給定預算下，能達到最低損失的模型大小與 token 數。

## 問題

在固定的運算預算下，模型大小與訓練 token 數量應如何平衡？

## 運作方式

作者在一組大小與 token 數的網格上訓練一系列模型。對每個預算，找出損失最低的大小與 token 數，再擬合最佳大小與最佳 token 數如何隨預算變化。模型大小與訓練 token 應一起擴展，使其中任何一項都不會在預算增加時被壓抑。

## 核心方法

本頁涵蓋一個方法：在模型大小與 token 數上做的擬合式、運算量相同的掃描。促成此擬合的擴展定律背景見 Kaplan 等人（2020），而本問題所關心的規模所屬的模型家族則是 [GPT-3](../gpt-3-few-shot/index.md)。

## 演算法

1. 訓練超過 400 個語言模型，參數從 7,000 萬到 160 億以上，資料量從 50 億到 5,000 億 token 不等。
2. 對每個運算預算，找出損失最低的模型大小與 token 數。
3. 擬合最佳大小與最佳 token 數如何隨預算變化。
4. 套用擬合得到的規則：模型大小與訓練 token 應同步成長，因此模型大小加倍，資料也要加倍。

## 結果

- Chinchilla 有 700 億參數與四倍的資料，使用的運算量與 Gopher（2,800 億參數）相同。它在廣泛的下游評估任務上勝過 Gopher，在 MMLU 上比 Gopher 提升超過 7%。
- 根據摘要，Chinchilla 在 MMLU 基準上達到 67.5% 的最先進平均準確率。

## 限制

- 擬合涵蓋作者所訓練的範圍，即 7,000 萬到 160 億以上的參數，以及最多 5,000 億 token。把它延伸到大得多的預算，屬於外推。
- 結果只針對訓練階段的運算最佳化。它未考慮訓練後提供服務的成本，因此在實務上，基於其他理由而偏好「較小模型、較多資料」的做法，並不在此擬合的範圍內。
- 論文的比較是與特定模型（Gopher 等）在特定資料上訓練的結果相比。

## 變體與更多變體

- **運算最佳化擬合**：此處描述的方法，為固定預算選擇分配方式。

## 連結

- 母頁：[大型語言模型](../index.md)
- 同一主題的另一方法：[GPT-3 少樣本學習](../gpt-3-few-shot/index.md)
- 同一主題的另一方法：[InstructGPT 與 RLHF](../instructgpt-rlhf/index.md)

## 應用

- 規劃預訓練：在固定運算預算下，於模型大小與資料量之間分配。
- 比較已發表的模型：依其 token 數判斷一個模型是否接近運算最佳化的訓練。

## 開放問題

- 擬合的規則在超出論文範圍的模型大小與資料量上是否仍然成立？
- 若把提供服務的成本納入預算，選擇應如何改變？

## 參考文獻

### 開創性論文

- Hoffmann, J., et al.（2022）。*Training Compute-Optimal Large Language Models*. arXiv. https://arxiv.org/abs/2203.15556 — Chinchilla 研究，主張在固定運算預算下，模型大小與訓練 token 數應該同步成長，包含 400 個模型的掃描與 MMLU 67.5% 的結果。
- Kaplan, J., et al.（2020）。*Scaling Laws for Neural Language Models*. arXiv. https://arxiv.org/abs/2001.08361 — 顯示損失隨模型大小、資料量與運算量呈冪律縮放，是擬合運算最佳化分配的背景。
- Brown, T. B., et al.（2020）。*Language Models are Few-Shot Learners*. arXiv. https://arxiv.org/abs/2005.14165 — GPT-3 論文，即本頁規模問題所涉及的 1,750 億參數模型家族。
- Ouyang, L., et al.（2022）。*Training language models to follow instructions with human feedback*. arXiv. https://arxiv.org/abs/2203.02155 — InstructGPT，透過以人類回饋微調，使語言模型符合使用者意圖。

### 綜述與教科書

- Zhao, W. X., et al.（2023）。*A Survey of Large Language Models*. arXiv. https://arxiv.org/abs/2303.18223 — 對 LLM 的預訓練、適應與評估進行廣泛綜述，並附有模型時間線。

## 延伸學習

- Hugging Face. *LLM Course*. https://huggingface.co/learn/llm-course — 使用 Hugging Face 函式庫來使用、微調與建構 LLM 的實作課程。
- Karpathy, A. (2023). *[1hr Talk] Intro to Large Language Models*. YouTube. https://www.youtube.com/watch?v=zjkBMFhNj_g — 一小時、非技術性的概述，介紹 LLM 如何訓練、能做什麼、在哪裡失敗。
