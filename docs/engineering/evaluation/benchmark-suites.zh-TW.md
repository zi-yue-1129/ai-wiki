---
status: complete
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
tags:
  - evaluation
  - benchmarks
  - language models
aliases:
  - Benchmark Suites
  - MMLU
  - HELM
  - 基準套件
  - 基準測試套件
---

# 基準套件：MMLU、HELM 與後繼者

基準套件（benchmark suite）把許多任務，常常跨越多個學科或情境，整合成一次評估。套件讓模型能在廣泛的能力上互相比較，而不只是單一能力，並已成為語言模型的常見參考點。套件的結果，其資訊量取決於涵蓋範圍、衡量指標，以及報告時的謹慎程度。

本頁是[評估與基準](index.zh-TW.md)的一部分。各基準的一般定義，見[語言基準](../../theory/evaluation/benchmarks/language/index.zh-TW.md)。

## 概述

早期的語言基準每個只衡量一項任務，例如情感或蘊含。大型模型讓單一任務變得容易，於是注意力轉向測試跨多個學科之知識與推理的套件。兩個套件展示了這個範圍。MMLU（Hendrycks 等人，2021）測試跨 57 個學科的多任務準確率，包括數學、歷史、電腦科學與法律。HELM（Liang 等人，2022）則跨越多種情境與多種指標進行評估，因此不會只報告準確率。

## 關鍵概念

- **情境：**一種使用場景，例如問答或摘要，由其資料與任務界定。
- **指標：**品質的衡量，例如準確率、校準、穩健性、公平性、偏見、毒性或效率。
- **涵蓋範圍：**套件包含多少學科、語言或情境，以及遺漏了什麼。
- **後繼套件：**因為舊套件已飽和或被污染而建立的較新基準。

## 關鍵方法

- [MMLU](../../theory/evaluation/benchmarks/language/mmlu.zh-TW.md)：跨 57 個學科的選擇題套件。它是模型比較中最常見的單一數字，其限制與任何單一題型的測試相同。
- [HELM](helm.zh-TW.md)：整體性框架，為 16 個核心情境各報告七項指標，使指標之間的取捨清楚可見。
- 後繼者：較新的套件提高難度或移除薄弱的題目。MMLU-Pro（Wang 等人，2024）是比 MMLU 更穩健、更具挑戰性的版本。BIG-bench（Srivastava 等人，2022）則彙集了許多研究者貢獻的廣泛任務，用來衡量模型規模增長時的能力。

## 如何解讀套件分數

- **檢查版本與協定。**少樣本提示、答案解析與子集的選擇，都會改變分數。
- **檢查資料污染。**公開的套件可能出現在訓練資料中。一般性的處理見[評估與基準](index.zh-TW.md)。
- **閱讀標題數字以外的指標。**一個準確但在某些情境下校準不佳或不公平的模型，與一個只有準確率的模型是不同的系統。
- **比較相同的條件。**不同協定下的分數不可直接比較。

## 關聯

- 評估的一般實務，包括以 LLM 為評審與人工審查，見[評估與基準](index.zh-TW.md)。
- 推理與代理的基準，見[推理與代理基準](../../theory/evaluation/benchmarks/reasoning-agents/index.zh-TW.md)。
- 評估設計與指標定義，在理論章節的[評估](../../theory/evaluation/index.zh-TW.md)。

## 應用

- 透過比較多個套件，為通用助理選擇模型。
- 以固定的套件與協定，追蹤模型在各版本間的表現。

## 開放問題

- 哪一組情境與指標最能反映實務使用？
- 公開套件在污染使其不可靠之前，能維持有用多久？

## 參考文獻

### 開創性論文

- Hendrycks, D. 等人（2021）。*Measuring Massive Multitask Language Understanding*。ICLR。https://arxiv.org/abs/2009.03300 — 提出 MMLU，一項跨 57 個學科的多任務準確率測試。
- Liang, P. 等人（2022）。*Holistic Evaluation of Language Models*。arXiv。https://arxiv.org/abs/2211.09110 — 提出 HELM，在 16 個核心情境中衡量七項指標。
- Srivastava, A. 等人（2022）。*Beyond the Imitation Game: Quantifying and extrapolating the capabilities of language models*。arXiv。https://arxiv.org/abs/2206.04615 — 提出 BIG-bench，一套廣泛、由多方共同建立的任務，用來衡量模型規模增長時的能力。
- Wang, Y. 等人（2024）。*MMLU-Pro: A More Robust and Challenging Multi-Task Language Understanding Benchmark*。arXiv。https://arxiv.org/abs/2406.01574 — MMLU 更穩健、更具挑戰性的後繼者。

### 調查與教科書

- Liang, P. 等人（2022）。*Holistic Evaluation of Language Models*。arXiv。https://arxiv.org/abs/2211.09110 — 上文已引用，作為衡量框架與情境範圍的依據。
