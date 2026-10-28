---
status: complete
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
  - society/interpretability
tags:
  - interpretability
  - probing
  - representations
aliases:
  - 線性探測器
  - Linear probes
  - Linear classifier probes
---

# 線性探測器

!!! info "屬於探測分類器"
    本方法頁屬於[探測分類器與表徵分析](probing.md)。它詳細說明此方法；上層頁面則比較各種探測方法。

線性探測器（linear probe）是在凍結的網路某一層激活上訓練的線性分類器，用來預測外部標籤。如果探測成功，表示該層可以被線性解碼出這項資訊。Alain 與 Bengio（2016）提出這種方法，用來追蹤類別資訊如何隨深度發展。

## 問題

深度網路的中間層難以直接閱讀。問題在於：當表徵經過各層時，關於輸出類別的資訊是如何組織的。目標是在不改變網路的前提下進行測量，並且讓各層之間易於比較。

## 核心想法

凍結訓練好的網路。對每個關注的層，用帶標籤的樣本，在該層的激活上訓練一個線性分類器。探測器獨立於模型訓練，因此它的準確率反映的是該層所含的內容，而非網路被訓練去做的事。

## 方程式

對所選層的激活向量 $h$，探測器預測

$$
\hat{y} = \mathrm{softmax}(W h + b),
$$

其中只學習 $W$ 與 $b$。訓練最小化 $\hat{y}$ 與真實標籤之間的交叉熵。

## 結果

Alain 與 Bengio 報告，特徵的線性可分性隨深度單調增加。他們在 ResNet-50 與 Inception v3 上觀察到這一點，在一個於 MNIST 上訓練的小型卷積網路上也是如此。結論是關於類別資訊如何跨層發展，而不是關於網路的最終準確率。後續研究顯示同一測量的另一面：Li 等人（2023）發現，對於以 Othello 棋步訓練的序列模型，線性探測器無法恢復棋盤狀態，而非線性探測器可以。

## 限制

- **存在，不等於使用。** 可被解碼的特徵，不一定是模型所依賴的特徵。Belinkov（2022）回顧了探測的這項一般性限制；要檢驗是否被使用，需要介入實驗。
- **探測器的選擇。** 線性探測器只讀取線性結構。非線性映射能讀出的資訊會被遺漏，而更強的探測器則可能讀出模型並未使用的資訊。
- **標籤品質。** 探測器會繼承標籤中的錯誤，而抽象性質的標籤難以定義。

## 相關連結

線性探測器是[探測分類器](probing.md)家族中最簡單的成員。[表徵相似度分析](representational-similarity-analysis.md)比較的是整體表徵，而非預測單一標籤；[控制任務](control-tasks.md)則是為了判斷探測的準確率反映的是表徵，還是探測器本身的容量。以因果測試檢驗表徵被如何使用，則連到[機械式可解釋性](mechanistic-interpretability.md)。關於各種解釋方法的整體比較，見[可解釋性總覽](index.md)。

## 應用

- 追蹤語言模型在各層何時首次表徵句法或語意性質。
- 為除錯，檢查視覺模型在最後一層之前的中間層是否已含有某個概念。
- 量測微調後的模型，是否保留或遺失了預訓練各層的資訊。

## 開放問題

- 需要多大的探測容量，才能說某項性質被表徵，又不會讀出模型從未使用的資訊？
- 探測結果在多大程度上能預測對表徵的介入是否改變行為？
- 能否以某種方式訓練探測器，避免讀出標籤中的虛假相關？

## 參考文獻

### 開創性論文

- Alain, G. & Bengio, Y. (2016). Understanding intermediate layers using linear classifier probes. arXiv:1610.01644. https://arxiv.org/abs/1610.01644 — Introduces linear probes at each depth and shows that linear separability of class information grows with depth.
- Hewitt, J. & Manning, C. D. (2019). A Structural Probe for Finding Syntax in Word Representations. *Proceedings of NAACL-HLT 2019*. https://doi.org/10.18653/v1/N19-1419 — Uses a linear probe on contextual embeddings to recover parse-tree structure.
- Hewitt, J. & Liang, P. (2019). Designing and Interpreting Probes with Control Tasks. *Proceedings of EMNLP-IJCNLP 2019*. https://doi.org/10.18653/v1/D19-1275 — Shows that probe accuracy must be read against control tasks.

### 綜述與教科書

- Belinkov, Y. (2022). Probing Classifiers: Promises, Shortcomings, and Advances. *Computational Linguistics*, 48(1), 207–219. https://doi.org/10.1162/coli_a_00422 — Critically reviews the probing framework, its promises, shortcomings and advances.
- Li, K. et al. (2023). Emergent World Representations: Exploring a Sequence Model Trained on a Synthetic Task. *Proceedings of ICLR 2023*. https://arxiv.org/abs/2210.13382 — Probes a model for board state, finds that nonlinear probes recover it, and tests the representation with interventions.
