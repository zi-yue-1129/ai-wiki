---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - few-shot
---

# miniImageNet

miniImageNet 是由 ImageNet 影像建立的少樣本影像分類基準。它用來測試模型能否從少數有標籤的範例辨識新類別。多數少樣本論文都會在它上面報告結果，通常以 N-way K-shot 的情節（episode）評估（Snell et al., 2017；Finn et al., 2017）。

## 任務與資料

每個評估情節會抽出 N 個模型在訓練中未見過的類別，並為每個類別提供 K 個有標籤的範例作為支持集。模型接著要對這些類別中的新查詢影像進行分類。情節是從保留的類別集合中隨機抽樣，因此訓練與測試的類別不重疊。

最常見的切分為 64 個訓練類別、16 個驗證類別與 20 個測試類別，由 Ravi 與 Larochelle（2017）定義。其他論文可能使用不同切分，因此在比較結果前，必須先檢查該論文使用的切分。

## 協定與指標

指標是查詢影像上的**準確率**，在許多隨機情節上取平均，通常附上信賴區間。結果取決於骨幹網路、訓練情節數與輸入解析度，因此只有在這些條件相同時，比較才有效。

Vinyals et al.（2016）為 ImageNet 與 Omniglot 上的單樣本評估設定了範本。他們報告的 ImageNet 單樣本準確率，相對於比較中的競爭方法，從 87.6% 提升到 93.2%。該設定使用自己的類別切分，與 miniImageNet 並不相同。

## 它能說明什麼

少樣本基準測試學習者能否從少量資料中調適，這是一般的監督式訓練做不到的。miniImageNet 成為元學習方法的標準測試，例如原型網路（Snell et al., 2017）與 MAML（Finn et al., 2017）。

## 限制

- **低解析度與細粒度類別。** 影像很小，類別也細緻，因此分數取決於所用的解析度。
- **協定漂移。** 各論文的切分、骨幹網路與訓練技巧都不同，使許多報告的進步難以比較。
- **飽和。** 近期的方法分數很高，若沒有區間，很難解讀小的差異。

## 相關

- [Omniglot](https://doi.org/10.1126/science.aab3050) 是 Lake et al.（2015）的手寫字元基準，是另一個標準少樣本測試。
- [ImageNet](../vision/imagenet.md) 是影像的來源。
- [少樣本家族概述](index.md) 說明此領域。

## 參考文獻

### 開創性論文

- Vinyals, O. et al. (2016). *Matching Networks for One Shot Learning*. arXiv. https://arxiv.org/abs/1606.04080 — 定義在 ImageNet 與 Omniglot 上的單樣本評估，之後的基準都沿用此設定。
- Lake, B. M. et al. (2015). *Human-level concept learning through probabilistic program induction*. Science. https://doi.org/10.1126/science.aab3050 — 介紹 Omniglot 手寫字元基準，用於從少量範例學習。
- Ravi, S. & Larochelle, H. (2017). *Optimization as a Model for Few-Shot Learning*. ICLR. https://openreview.net/forum?id=rJY0-Kcll — 定義多數 miniImageNet 論文所用的 64/16/20 類別切分。

### 文章與文件

- Snell, J. et al. (2017). *Prototypical Networks for Few-shot Learning*. arXiv. https://arxiv.org/abs/1703.05175 — 使用 N-way K-shot 情節，並報告 miniImageNet 上的結果。
- Finn, C. et al. (2017). *Model-Agnostic Meta-Learning for Fast Adaptation of Deep Networks*. arXiv. https://arxiv.org/abs/1703.03400 — 報告一種元學習方法在 miniImageNet 上的少樣本結果。

### 補充來源

- Russakovsky, O. et al. (2015). *ImageNet Large Scale Visual Recognition Challenge*. International Journal of Computer Vision. https://doi.org/10.1007/s11263-015-0816-y — miniImageNet 所建立的影像來源。
