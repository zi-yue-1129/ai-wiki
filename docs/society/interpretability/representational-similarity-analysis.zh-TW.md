---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
  - society/interpretability
  - brain-mind/neuroai
tags:
  - interpretability
  - neuroscience
  - representations
aliases:
  - 表徵相似度分析
  - RSA
  - Representational similarity analysis
---

# 表徵相似度分析

!!! info "屬於探測分類器"
    本方法頁屬於[探測分類器與表徵分析](probing.md)。它詳細說明此方法；概述頁則比較各種探測方法。

表徵相似度分析（RSA）透過兩個系統對相同刺激的回應結構來比較它們，例如一個大腦區域與一個網路層，而非逐一比對單一單元。Kriegeskorte、Mur 與 Bandettini（2008）為系統神經科學提出此架構，現在也用來比較人工網路與大腦。

## 問題

神經記錄與網路啟動值的格式不同，單元數目也不同，因此無法逐一單元比較。問題是在不要求單元彼此對應的共同基礎上比較它們。

## 核心想法

對每個系統，計算每一對刺激回應之間的相異度，得到表徵相異度矩陣（RDM）。若兩個系統的 RDM 結構相似，則兩者相似，無論各自有多少單元。因此比較是在表徵的幾何之間進行。

## 公式

對刺激 \(i\) 與 \(j\) 的回應 \(r_i\) 與 \(r_j\)，常用的相異度是一減去兩者回應模式之間的相關：

\[
\mathrm{RDM}_{ij} = 1 - \mathrm{corr}(r_i, r_j).
\]

兩個系統透過比較各自 RDM 的上三角來進行比較。

## 結果

論文描述此架構，並顯示它能將不同測量模式的活動模式加以關聯，也能跨越受試者與物種。這是一篇架構論文，因此其貢獻是方法本身，而非某個單一測得的效應。

## 限制

- **依賴刺激。** RDM 只對所用的刺激有定義，因此結論取決於所選的刺激集。
- **度量的選擇。** 相異度的量測決定哪些結構可見，不同的選擇可能得出不同的答案。
- **相似不等於機制。** 兩種表徵可能有相同的幾何，卻計算不同的函數。

## 參考文獻

### 開創性論文

- Kriegeskorte, N., Mur, M. & Bandettini, P. (2008). Representational similarity analysis – connecting the branches of systems neuroscience. *Frontiers in Systems Neuroscience*. https://doi.org/10.3389/neuro.06.004.2008 — 定義表徵相似度分析，透過回應幾何來比較系統。
- Alain, G. & Bengio, Y. (2016). Understanding intermediate layers using linear classifier probes. *arXiv preprint*. https://arxiv.org/abs/1610.01644 — 讀取網路各層的另一種方式，RSA 常與之比較。
- Park, K., Choe, Y. J. & Veitch, V. (2023). The Linear Representation Hypothesis and the Geometry of Large Language Models. *arXiv preprint*. https://arxiv.org/abs/2311.03658 — 研究語言模型中概念表徵的幾何。

### 綜述與教科書

- Belinkov, Y. (2022). Probing Classifiers: Promises, Shortcomings, and Advances. *Computational Linguistics*, 48(1), 207–219. https://doi.org/10.1162/coli_a_00422 — 回顧探測方法，它是比較表徵與其他系統的主要工具之一。
- Hewitt, J. & Liang, P. (2019). Designing and Interpreting Probes with Control Tasks. *Proceedings of EMNLP-IJCNLP 2019*. https://doi.org/10.18653/v1/D19-1275 — 顯示在解讀表徵與某性質的吻合程度時，需要控制。
