---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - language
---

# GPQA

GPQA 是 448 道研究所程度的選擇題，涵蓋生物、物理與化學。題目由專家撰寫，並刻意設計成難以靠網路搜尋回答，因此名稱中有「Google-proof」（Rein et al., 2023）。

## 任務與資料

每題有四個選項。題目由具博士學位或博士訓練背景的人撰寫。基準分為三個科學領域，規模刻意保持不大，讓每一題都能被仔細驗證。

## 協定與指標

指標是**準確率**。論文也報告了人類的表現：具博士學位的專家達到 65%，若扣除他們事後指出的明顯錯誤則為 74%。有能力的非專家驗證者即使花超過 30 分鐘、可無限制使用網路，也只有 34%。以 GPT-4 為基礎的基線得分為 39%（Rein et al., 2023）。

## 它能說明什麼

這個基準的難度尺度是以人類專家為錨，而非一般大眾。它是為了檢驗系統能否回答需要專業知識與審慎推理的問題，而非單純的記憶回想。

## 限制

- **樣本小。** 只有 448 題，幾個百分點的差距可能只是抽樣雜訊。應報告信賴區間，[評估協定](../../protocols/index.md)一節有說明。
- **涵蓋範圍窄。** 基準只涵蓋三個科學領域，未涵蓋其他需要專家推理的領域。
- **搜尋存取。** 「Google-proof」的性質是在撰寫時以可上網的人來檢驗的。具備瀏覽工具的模型可能需要不同的評估方式，因此必須說明評估設定。

## 相關

- [MMLU](mmlu.md) 涵蓋更廣的知識，難度較低。
- [人類的最後考試](hle.md) 是規模更大、難度更高的後繼基準。
- [語言家族概述](index.md) 比較各語言基準。

## 參考文獻

### 開創性論文

- Rein, D. et al. (2023). *GPQA: A Graduate-Level Google-Proof Q&A Benchmark*. arXiv. https://arxiv.org/abs/2311.12022 — 介紹 448 道專家撰寫的題目，以及專家與非專家的基線。
- Hendrycks, D. et al. (2021). *Measuring Massive Multitask Language Understanding*. ICLR. https://arxiv.org/abs/2009.03300 — GPQA 所針對的較早期選擇題知識基準。

### 文章與文件

- Phan, L. et al. (2025). *Humanity's Last Exam*. arXiv. https://arxiv.org/abs/2501.14249 — 規模更大的後繼基準，題目設計為持續保持困難。
- Wei, J. et al. (2022). *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models*. arXiv. https://arxiv.org/abs/2201.11903 — 顯示中間推理步驟如何改變推理基準上的分數。

### 補充來源

- Srivastava, A. et al. (2022). *Beyond the Imitation Game: Quantifying and extrapolating the capabilities of language models*. arXiv. https://arxiv.org/abs/2206.04615 — 廣泛的基準集合，把專家程度的題目與其他任務並列。
