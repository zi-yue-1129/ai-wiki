---
related:
  - theory/models/gnn
  - theory/models/gnn/message-passing
  - theory/models/gnn/message-passing/gcn
tags:
  - graph neural networks
  - message passing
  - quantum chemistry
aliases:
  - MPNN
  - Message passing neural networks
  - Neural message passing for quantum chemistry
  - 訊息傳遞神經網路
translation_reviewed: 2026-11-01
---

# MPNN：量子化學的神經訊息傳遞

訊息傳遞神經網路（MPNN）是一種圖模型，由三個可學習的函數組成：訊息函數、頂點更新與讀出。Gilmer 等人（2017）提出這個框架，並將其應用於預測小分子的性質。論文顯示，數個較早的圖模型都符合這個模板，並在 QM9 基準上測試它。整個模型家族的介紹見[訊息傳遞](index.md)頁面；本頁說明框架本身與分子上的結果。

## 概述

2017 年的多數圖模型使用固定的鄰域運算，例如正規化平均或有閘控的更新。Gilmer 等人想知道，是否能用一套通用的描述涵蓋所有這些模型，並讓訊息與更新函數的選擇針對特定任務調整。答案是一個帶有可學習部分的單一模板，以及一組比較各種選擇的實驗。

## 問題

論文探討如何建構一個尊重分子對稱性、並預測其量子力學性質的網路。基準是 QM9，包含約 134,000 個小型有機分子，每個分子有 13 個目標。每個目標都近似於密度泛函理論（DFT）的結果，DFT 準確但計算昂貴。論文以 DFT 的誤差，以及化學精度（論文為每個性質設定的目標誤差）來衡量成效。

## 核心想法

每個節點 \(v\) 持有一個隱藏狀態 \(h_v\)，每條邊 \(vw\) 帶有一個特徵向量 \(e_{vw}\)。在 \(T\) 步中，每個節點收集鄰居的訊息，然後更新自己的狀態。最後一步之後，讀出函數將所有節點狀態的集合映射為一個預測。讀出必須與節點的順序無關。

## 演算法

前向傳播為

\[
m_v^{t+1} = \sum_{w \in \mathcal{N}(v)} M_t\big(h_v^t, h_w^t, e_{vw}\big), \qquad h_v^{t+1} = U_t\big(h_v^t, m_v^{t+1}\big), \qquad \hat y = R\big(\{h_v^T : v \in G\}\big)
\]

其中 \(M_t\) 是訊息函數，\(U_t\) 是頂點更新，\(R\) 是讀出。論文第 5 節比較了幾種選擇。

- **矩陣乘法**，如閘控圖神經網路（GG-NN）：訊息是每種邊類型的矩陣乘以鄰居的狀態。
- **邊網路**：一個小網路把邊特徵向量映射為矩陣 \(A(e_{vw})\)，訊息為 \(A(e_{vw})\,h_w\)。這是論文中表現最好的訊息函數。
- **成對訊息**：同時依賴兩端節點與邊的函數 \(f(h_w, h_v, e_{vw})\)。
- **讀出**：GG-NN 的讀出，以及 Set2Set（Vinyals 等人，2015），它對節點集合使用注意力，且與順序無關。

## 結果

論文表 2 報告每個目標的誤差比，即平均絕對誤差除以化學精度目標。誤差比低於 1 表示該目標達到化學精度。下表節錄論文表 2 的部分內容，完整結果還包含其他基準。

| 目標 | 化學精度 | GG-NN | enn-s2s | enn-s2s-ens5 |
|---|---|---|---|---|
| mu | 0.1 | 1.22 | 0.30 | 0.20 |
| alpha | 0.1 | 1.55 | 0.92 | 0.68 |
| HOMO | 0.043 | 1.17 | 0.99 | 0.74 |
| gap | 0.043 | 1.70 | 1.60 | 1.23 |
| U0 | 0.043 | 0.83 | 0.45 | 0.33 |
| ZPVE | 0.0012 | 2.52 | 1.27 | 1.10 |
| Omega | 10.0 | 0.53 | 0.19 | 0.15 |
| **平均** | | 1.36 | 0.68 | 0.52 |

此處 enn-s2s 是單一的邊網路模型，搭配 Set2Set 讀出；enn-s2s-ens5 是五個模型的集成。單一模型在 13 個目標中有 11 個達到化學精度，只有 gap 與 ZPVE 未達標。集成模型在相同的 11 個目標上達到化學精度。論文中其他基準的平均誤差比，HDAD 為 1.35，圖卷積（GC）為 2.59。

論文也測試了不使用空間資訊的模型。以部分電荷作為輸入時，Set2Set 模型的平均誤差比為 2.57，且 13 個目標中有 5 個達到化學精度。作者指出，部分電荷本身是 DFT 的輸出，因此這種設定在實際應用中無法使用。

## 限制

- **較大的分子。** 作者表示，未來工作「應聚焦於含有較大分子的資料集，或更準確的真實標籤」。若使用空間資訊，分子變大時原子對距離的分布會改變，而全連接圖也會隨原子數增長。
- **推廣到較大的圖。** 第 9 節將此列為重要方向。作者建議，可以考慮對進入的訊息使用注意力。
- **塔式結構。** 在論文的實驗中，將隱藏狀態切分為數個塔，與邊網路的結合效果不佳。作者表示，塔式變體「在擴展到大得多的圖時仍會需要」。
- **標籤來源。** 化學精度是以 DFT 推導的標籤來衡量，而非實驗量測。

## 關聯

- 此模板涵蓋 [GCN](gcn/index.md) 的正規化鄰居卷積、[GAT](gat/index.md) 的注意力、[GIN](gin/index.md) 的加總聚合，以及 [GraphSAGE](graphsage/index.md) 的抽樣。
- 此模板的家族層級說明與表達能力限制，見[訊息傳遞](index.md)頁面；更廣的模型家族見[圖神經網路](../index.md)頁面。
- 分子的空間模型，例如 SchNet（Schütt 等人，2017），在同類資料上使用連續濾波卷積，是很自然的比較對象。

## 未解問題

- 當原子相距較遠時，如何形成訊息，又不必付出全連接圖的成本？
- 邊網路的訊息能否從 QM9 推廣到較大的分子與其他性質？
- 準確度有多少來自讀出，有多少來自訊息函數？

## 參考文獻

### 奠基論文

- Gilmer, J., Schoenholz, S. S., Riley, P. F., Vinyals, O. & Dahl, G. E. (2017). Neural Message Passing for Quantum Chemistry. ICML, PMLR 70, 頁 1263–1272. [arXiv:1704.01212](https://arxiv.org/abs/1704.01212) — 定義訊息、更新與讀出的框架，並報告 QM9 上的結果。
- Li, Y., Tarlow, D., Brockschmidt, M. & Zemel, R. (2015). Gated Graph Sequence Neural Networks. [arXiv:1511.05493](https://arxiv.org/abs/1511.05493) — GG-NN 模型，其矩陣乘法訊息是論文比較的變體之一。
- Kipf, T. N. & Welling, M. (2016). Semi-Supervised Classification with Graph Convolutional Networks. [arXiv:1609.02907](https://arxiv.org/abs/1609.02907) — 本框架所推廣的正規化鄰居平均。
- Vinyals, O., Bengio, S. & Kudlur, M. (2015). Order Matters: Sequence to Sequence for Sets. [arXiv:1511.06391](https://arxiv.org/abs/1511.06391) — 提出 Set2Set，即最佳模型所用的順序無關讀出。
- Schütt, K. T. 等人（2017）。SchNet: A Continuous-filter Convolutional Neural Network for Modeling Quantum Interactions. [arXiv:1706.08566](https://arxiv.org/abs/1706.08566) — 分子的空間模型，論文的空間資訊實驗與之相關。

### 綜述與教科書

（本頁未核對）

### 講座與影片

（本頁未核對）

### 文章與文件

- Ramakrishnan, R. 等人（2014）。Quantum Chemistry Structures and Properties of 134 Kilo Molecules. Scientific Data, 1. [DOI 10.1038/sdata.2014.22](https://doi.org/10.1038/sdata.2014.22) — 論文作為基準使用的 QM9 資料集與其 13 個目標。
