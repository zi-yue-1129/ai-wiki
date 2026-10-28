---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - few-shot
---

# 少樣本基準

少樣本基準測試學習者能否從少量有標籤的範例中辨識新類別。它們通常以 N-way K-shot 情節執行，分數是許多隨機情節的平均，因此協定與數字同樣重要。

| 基準 | 影像來源 | 主要指標 |
|---|---|---|
| [miniImageNet](mini-imagenet.md) | ImageNet 的子集 | 附信賴區間的情節準確率 |
| [Omniglot](omniglot.md) | 多種書寫系統的手寫字元 | 附信賴區間的情節準確率 |

## 常見問題

- **協定漂移。** 各論文的類別切分、骨幹網路與情節數都不同。
- **飽和。** 頂尖方法留下的空間很小，因此差異需要區間。

## 相關

- [基準概述](../index.md) 列出所有家族。
- [ImageNet](../vision/imagenet.md) 是影像的來源。

## 參考文獻

### 開創性論文

- Vinyals, O. et al. (2016). *Matching Networks for One Shot Learning*. arXiv. https://arxiv.org/abs/1606.04080 — 定義在 ImageNet 與 Omniglot 上的單樣本評估，之後的基準都沿用此設定。
- Lake, B. M. et al. (2015). *Human-level concept learning through probabilistic program induction*. Science. https://doi.org/10.1126/science.aab3050 — 介紹用於從少量範例學習的 Omniglot。

### 文章與文件

- Snell, J. et al. (2017). *Prototypical Networks for Few-shot Learning*. arXiv. https://arxiv.org/abs/1703.05175 — 使用 N-way K-shot 情節，並報告 miniImageNet 上的結果。
- Finn, C. et al. (2017). *Model-Agnostic Meta-Learning for Fast Adaptation of Deep Networks*. arXiv. https://arxiv.org/abs/1703.03400 — 報告一種元學習方法在 miniImageNet 上的少樣本結果。
- Russakovsky, O. et al. (2015). *ImageNet Large Scale Visual Recognition Challenge*. International Journal of Computer Vision. https://doi.org/10.1007/s11263-015-0816-y — miniImageNet 背後的來源資料集。
