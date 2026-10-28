---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - neuroscience
---

# 神經科學基準

神經科學基準測試模型的內部反應與量測到的神經或行為資料有多接近。它問的問題與準確率不同：模型可能很會分類影像，但在表徵方式上仍與大腦不同。

| 基準 | 任務 | 主要指標 |
|---|---|---|
| [Brain-Score](brain-score.md) | 預測對物體影像的神經與行為反應 | 留出的神經與行為資料之可預測性 |

## 常見問題

- **映射選擇。** 分數取決於模型單元如何映射到神經位點，因此必須報告所用的迴歸與層。
- **量測資料有限。** 位點與影像少，不確定性就大，因此模型之間的小差異並不可靠。
- **相似不等於機制。** 分數高只說明表徵在測試上相似，不代表模型與大腦的運作方式相同（Yamins et al., 2014）。

## 相關

- [基準測試概述](../index.md) 列出所有家族。
- [視覺](../vision/index.md) 涵蓋模型常用的影像基準。
- [協定](../../protocols/index.md) 說明切分與報告方式。

## 參考文獻

### 開創性論文

- Schrimpf, M. et al. (2018). *Brain-Score: Which Artificial Neural Network for Object Recognition is most Brain-Like?* bioRxiv. https://doi.org/10.1101/407007 — 介紹基準及其神經與行為分數。
- Yamins, D. L. K. et al. (2014). *Performance-optimized hierarchical models predict neural responses in higher visual cortex*. PNAS. https://doi.org/10.1073/pnas.1403112111 — 顯示物體辨識模型能預測高階視覺皮層的反應。

### 文章與文件

- Raji, I. D. & Bender, E. M. et al. (2021). *AI and the Everything in the Whole Wide World Benchmark*. arXiv. https://arxiv.org/abs/2111.15366 — 探討構念效度，以及由基準推出廣泛結論的限制。

### 補充來源

- Liang, P. & Bommasani, R. et al. (2022). *Holistic Evaluation of Language Models*. arXiv. https://arxiv.org/abs/2211.09110 — 跨情境與指標評估模型，揭露其取捨。
- Recht, B. et al. (2019). *Do ImageNet Classifiers Generalize to ImageNet?* arXiv. https://arxiv.org/abs/1902.10811 — 顯示重新蒐集的測試集能揭露模型對原始蒐集方式的適配程度。
