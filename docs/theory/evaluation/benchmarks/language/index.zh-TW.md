---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - language
---

# 語言基準

語言基準涵蓋三種不同的事：句子層級的理解（GLUE 與 SuperGLUE）、以選擇題形式測量的廣泛知識（MMLU），以及專家層級的推理（GPQA 與人類的最後考試）。不同團隊的分數不能互相替換，因為它們測量的技能不同。

| 基準 | 任務 | 主要指標 |
|---|---|---|
| [GLUE](glue.md) | 九個理解任務 | 各任務分數的平均 |
| [SuperGLUE](superglue.md) | 八個較困難的理解任務 | 各任務分數的平均 |
| [MMLU](mmlu.md) | 57 個科目的知識 | 準確率 |
| [GPQA](gpqa.md) | 研究所程度的科學 | 準確率 |
| [人類的最後考試](hle.md) | 跨學科的專家題目 | 自動評分的準確率 |

## 常見問題

- **飽和。** 這些基準多數在發布後幾年內就達到高分。
- **污染。** 公開的題目可能出現在預訓練資料中，因此分數可能部分反映記憶。
- **提示敏感。** 少樣本範例、答案擷取與評分器都會改變結果，因此必須報告協定。

## 相關

- [基準概述](../index.md) 列出所有家族。
- [準確率](../../metrics/classification/accuracy.md) 是多數基準使用的指標。

## 參考文獻

### 開創性論文

- Wang, A. et al. (2018). *GLUE: A Multi-Task Benchmark and Analysis Platform for Natural Language Understanding*. arXiv. https://arxiv.org/abs/1804.07461 — 介紹多任務的理解基準。
- Wang, A. et al. (2019). *SuperGLUE: A Stickier Benchmark for General-Purpose Language Understanding Systems*. arXiv. https://arxiv.org/abs/1905.00537 — 介紹較困難的後繼基準及其人類基線。
- Hendrycks, D. et al. (2021). *Measuring Massive Multitask Language Understanding*. ICLR. https://arxiv.org/abs/2009.03300 — 介紹 57 科目的知識測試。

### 文章與文件

- Rein, D. et al. (2023). *GPQA: A Graduate-Level Google-Proof Q&A Benchmark*. arXiv. https://arxiv.org/abs/2311.12022 — 介紹專家撰寫的科學題目與專家基線。
- Phan, L. et al. (2025). *Humanity's Last Exam*. arXiv. https://arxiv.org/abs/2501.14249 — 介紹 2,500 題、用以取代已飽和基準的後繼基準。
