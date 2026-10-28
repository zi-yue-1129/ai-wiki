---
status: complete
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
    本方法頁屬於[探測分類器與表徵分析](probing.md)。它詳細說明此方法；上層頁面則比較各種探測方法。

表徵相似度分析（representational similarity analysis，RSA）以兩個系統（例如一個大腦區域與一個網路層）對相同刺激的反應結構來比較它們，而不是逐個單元比對。Kriegeskorte、Mur 與 Bandettini（2008）為系統神經科學提出了這個框架，現在也用來比較人工網路與大腦。

## 問題

神經記錄與網路激活的格式不同，單元數量也不同，因此無法逐個單元比較。問題在於：在不要求單元彼此對應的前提下，把它們放在共同的基礎上比較。

## 核心想法

對每個系統，計算每一對刺激反應之間的不相似度，得到表徵不相似度矩陣（RDM）。若兩個系統的 RDM 結構相似，它們就相似，無論各自有多少單元。因此比較的是表徵的幾何。

## 方程式

對刺激 $i$ 與 $j$ 的反應 $r_i$ 與 $r_j$，常用的不相似度是一減去反應模式之間的相關：

$$
\mathrm{RDM}_{ij} = 1 - \mathrm{corr}(r_i, r_j).
$$

比較兩個系統時，計算其 RDM 上三角的相關。

## 結果

Kriegeskorte 等人把 RSA 呈現為比較系統的框架，透過其反應幾何來比較。論文的貢獻是方法及其比較用途，而非某一項量測的效應。後續研究把同一種比較應用於人工網路，問題是某一層的幾何是否與某個大腦區域相符。

## 限制

- **依賴刺激。** RDM 只在所用的刺激上有定義，因此結論取決於所選的刺激集合。
- **度量的選擇。** 不相似度的度量會影響哪些結構可見，不同的選擇可能給出不同的答案。
- **相似不等於機制。** 兩個表徵可以有相同的幾何，卻計算不同的函數。

## 相關連結

RSA 是單一標籤的[線性探測器](linear-probes.md)及檢驗它們的[控制任務](control-tasks.md)之外，另一種以幾何為基礎的做法。它與[探測分類器](probing.md)屬於同一類表徵分析。它源自系統神經科學，與[神經AI](../../brain-mind/neuroai/index.md)比較人工與生物網路的研究相連。Park 等人（2023）關於語言模型中線性幾何的工作，則探討相關的概念方向問題。

## 應用

- 比較視覺模型的表徵與視覺皮質對同一批影像的反應。
- 檢查兩個訓練好的網路是否以相似的方式組織同一批輸入，無論架構為何。
- 追蹤語言模型各層的幾何在訓練過程中如何變化。

## 開放問題

- 應如何選擇刺激集合，才能讓 RSA 結果推廣到該集合之外？
- 哪一種不相似度度量最符合所問的問題？
- 共享的幾何何時意味著共享的計算，何時則不然？

## 參考文獻

### 開創性論文

- Kriegeskorte, N., Mur, M. & Bandettini, P. (2008). Representational similarity analysis – connecting the branches of systems neuroscience. *Frontiers in Systems Neuroscience*, 2. https://doi.org/10.3389/neuro.06.004.2008 — Defines RSA for comparing systems through the geometry of their responses.
- Alain, G. & Bengio, Y. (2016). Understanding intermediate layers using linear classifier probes. arXiv:1610.01644. https://arxiv.org/abs/1610.01644 — A different way to read the layers of a network, against which RSA is often compared.
- Park, K., Choe, Y. J. & Veitch, V. (2023). The Linear Representation Hypothesis and the Geometry of Large Language Models. arXiv:2311.03658. https://arxiv.org/abs/2311.03658 — Studies concepts as linear directions in a language model's representation space, and the inner product that gives them geometric meaning.

### 綜述與教科書

- Belinkov, Y. (2022). Probing Classifiers: Promises, Shortcomings, and Advances. *Computational Linguistics*, 48(1), 207–219. https://doi.org/10.1162/coli_a_00422 — Reviews probing, one of the main tools for comparing representations with other systems.
- Hewitt, J. & Liang, P. (2019). Designing and Interpreting Probes with Control Tasks. *Proceedings of EMNLP-IJCNLP 2019*. https://doi.org/10.18653/v1/D19-1275 — Shows the need for controls when interpreting how well a representation matches a property.
