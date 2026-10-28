---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - few-shot
---

# Omniglot

Omniglot 是來自多種書寫系統的手寫字元集合，每個字元只有少數幾個手繪範例。它的建立目的，是測試學習者看過一個或少數幾個範例後，能否辨識新字元，這正是少樣本學習的設定（Lake et al., 2015）。Matching networks 在其上報告單樣本結果，使它成為標準的少樣本基準（Vinyals et al., 2016）。

## 任務與資料

資料集包含來自 50 種書寫系統的 1,623 個字元，每個字元由 20 位不同的人手繪。一個情節會抽出數個字元，向學習者展示每個字元的少數有標籤範例，再要求它分類同一字元的新手繪圖（Lake et al., 2015; Vinyals et al., 2016）。

## 協定與指標

常見協定是 N-way K-shot 分類，例如 20-way one-shot，即每類只看到一個有標籤範例（Vinyals et al., 2016）。指標是多個隨機情節的平均準確率，通常附信賴區間。訓練字母與測試字母的選擇必須說明，因為它決定測試類別與訓練類別的距離。

## 它能說明什麼

它顯示方法能否在極少範例下泛化到新字元，而這些影像簡單且幾乎是二值的。在此表現良好的方法，不會自動適用於自然影像；後者由 miniImageNet 提供較困難的測試（Snell et al., 2017）。

## 限制

- **影像簡單。** 平底背景上的筆畫與自然照片相距甚遠，因此這個基準比名稱所示的更容易解決。
- **飽和。** 近期方法已接近完美準確率，留給比較的空間很小。
- **切分漂移。** 各論文劃分字母為訓練與測試集的方式不同，因此分數不一定可比。

## 相關

- [少樣本概述](index.md) 比較少樣本基準。
- [miniImageNet](mini-imagenet.md) 是自然影像的對應基準。

## 參考文獻

### 開創性論文

- Lake, B. M. et al. (2015). *Human-level concept learning through probabilistic program induction*. Science. https://doi.org/10.1126/science.aab3050 — 介紹 Omniglot，作為從少數範例學習的基準。
- Vinyals, O. et al. (2016). *Matching Networks for One Shot Learning*. arXiv. https://arxiv.org/abs/1606.04080 — 定義在 Omniglot 與 ImageNet 上的單樣本評估，後續基準沿用此方式。

### 文章與文件

- Snell, J. et al. (2017). *Prototypical Networks for Few-shot Learning*. arXiv. https://arxiv.org/abs/1703.05175 — 以 N-way K-shot 情節在 Omniglot 與 miniImageNet 上報告結果。
- Finn, C. et al. (2017). *Model-Agnostic Meta-Learning for Fast Adaptation of Deep Networks*. arXiv. https://arxiv.org/abs/1703.03400 — 在 Omniglot 上報告一種元學習方法的少樣本結果。

### 補充來源

- Recht, B. et al. (2019). *Do ImageNet Classifiers Generalize to ImageNet?* arXiv. https://arxiv.org/abs/1902.10811 — 顯示重新蒐集的測試集能揭露模型對原始蒐集方式的適配程度。
