---
status: draft
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
    本方法頁屬於[探測分類器與表徵分析](probing.md)。它詳細說明此方法；概述頁則比較各種探測方法。

線性探測器是在網路某一層凍結的啟動值上訓練的線性分類器，用來預測外部標籤。若探測成功，表示該層的資訊可以被線性解碼。Alain 與 Bengio（2016）提出此方法，用來追蹤類別資訊如何隨深度發展。

## 問題

深層網路的中間層難以直接閱讀。問題在於：隨著表徵經過各層，關於輸出類別的資訊是如何組織的？問題是在不改變網路的前提下衡量這一點，並且能在各層之間方便比較。

## 核心想法

凍結訓練好的網路。對每個感興趣的層，以該層的啟動值與有標籤的樣本訓練一個線性分類器。探測器獨立於模型訓練，因此其準確率反映的是該層所含的內容，而非網路被訓練去做的事。

## 公式

對所選層的啟動向量 \(h\)，探測器預測

\[
\hat{y} = \mathrm{softmax}(W h + b),
\]

只有 \(W\) 與 \(b\) 會被學習。訓練會最小化 \(\hat{y}\) 與真實標籤之間的交叉熵。

## 結果

論文報告，特徵的線性可分性隨深度單調增加，並以 Inception v3 與 ResNet-50 進行實驗驗證。此結論是關於類別資訊如何跨層發展，而非網路最終的準確率。

## 限制

- **存在而非使用。** 可解碼的特徵未必是模型所依賴的特徵。Belinkov（2022）回顧了探測方法的這項限制。
- **探測器的選擇。** 線性探測器只讀取線性結構。非線性映射能讀出的資訊會被漏掉；而更強的探測器則可能讀出模型並未使用的資訊。
- **標籤品質。** 探測器會承襲標籤中的任何錯誤，而抽象性質的標籤很難定義。

## 參考文獻

### 開創性論文

- Alain, G. & Bengio, Y. (2016). Understanding intermediate layers using linear classifier probes. *arXiv preprint*. https://arxiv.org/abs/1610.01644 — 引入各深度的線性探測器，顯示類別資訊的線性可分性如何隨深度增加。
- Hewitt, J. & Manning, C. D. (2019). A Structural Probe for Finding Syntax in Word Representations. *Proceedings of NAACL-HLT 2019*. https://doi.org/10.18653/v1/N19-1419 — 在上下文嵌入上使用線性探測器，以恢復剖析樹結構。
- Hewitt, J. & Liang, P. (2019). Designing and Interpreting Probes with Control Tasks. *Proceedings of EMNLP-IJCNLP 2019*. https://doi.org/10.18653/v1/D19-1275 — 顯示探測的準確率必須對照控制任務來解讀。

### 綜述與教科書

- Belinkov, Y. (2022). Probing Classifiers: Promises, Shortcomings, and Advances. *Computational Linguistics*, 48(1), 207–219. https://doi.org/10.1162/coli_a_00422 — 批判性地回顧探測分類器框架，包括其優點、缺點與進展。
- Li, K. et al. (2023). Emergent World Representations: Exploring a Sequence Model Trained on a Synthetic Task. *Proceedings of ICLR 2023*. https://arxiv.org/abs/2210.13382 — 對棋盤狀態進行探測，並以介入來測試此表徵。
