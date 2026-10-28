---
related:
- theory/models/gnn/message-passing
- theory/models/gnn
aliases:
  - Graph Isomorphism Networks
  - GIN
  - 圖同構網路
tags:
  - graph neural networks
  - expressivity
  - message passing
  - graph isomorphism
translation_reviewed: 2026-10-28
---

# 圖同構網路（GIN）

圖同構網路（GIN）是一種訊息傳遞設計，目標是達到 Weisfeiler–Lehman（WL）圖同構測試的區辨能力。此模型由 Xu 等人（2018）提出，他們也說明了基於聚合的 GNN 的能力上限。

## 問題

哪些聚合方式能讓 GNN 具有 WL 同構測試的區辨能力？論文的第一個結果是：任何基於聚合的 GNN，其能力至多與該測試相當。

## 核心想法

能力最強的 GNN 必須把不同的鄰域映射到不同的表徵，這需要單射（injective）的聚合。求和聚合可以表示多重集合上的單射函數，而平均與最大值一般做不到。

## 方程式或演算法

每一層將節點自身的特徵乘以（1 + ε）後，與鄰居的特徵相加，再經過一個 MLP 得到更新結果：

\[
h_v^{(k)} = \text{MLP}^{(k)}\!\Big((1+\epsilon^{(k)})\cdot h_v^{(k-1)} + \sum_{u\in\mathcal{N}(v)} h_u^{(k-1)}\Big)
\]

GIN-0 是固定 ε = 0 的變體。

## 結果

在 REDDIT-BINARY、COLLAB、MUTAG 與 NCI1 這些基準上，GIN-0 分別達到 92.4 ± 2.5、80.2 ± 1.9、89.4 ± 5.6 與 82.7 ± 1.7。平均聚合的變體在 REDDIT-BINARY 上得 50.0，論文將此歸因於平均聚合無法捕捉結構。

## 限制

理論假設輸入特徵是可數的，且未討論泛化。基於聚合的 GNN 仍受 WL 測試限制，作者將超越鄰域聚合列為未來工作。

## 相關連結

GIN 是訊息傳遞架構中採用求和聚合的特例。[訊息傳遞](../index.md)頁面涵蓋基於求和聚合的表達力，[圖神經網路](../../index.md)頁面則把表達力限制列為已知問題之一。以正規化與注意力加權的聚合方式，分別見 [GCN](../gcn/index.md) 與 [GAT](../gat/index.md) 頁面。

## 未解問題與更多變體

- **超越 WL 上限。** 論文將超越鄰域聚合列為未來工作，此頁未描述此類方法。
- **泛化。** 理論未討論泛化，因此此頁的證明無法解釋基準上的結果。
- **連續特徵。** 理論假設輸入特徵是可數的。此分析如何延伸到連續輸入，此頁未涵蓋。

## 參考文獻

### 開創性論文

- Xu, K., et al. (2018). "How Powerful are Graph Neural Networks?". [arXiv:1810.00826](https://arxiv.org/abs/1810.00826) — 顯示聚合函數的表達力限制，並提出基於求和的 GIN。
- Kipf, T. N. & Welling, M. (2016). "Semi-Supervised Classification with Graph Convolutional Networks". [arXiv:1609.02907](https://arxiv.org/abs/1609.02907) — 依對稱度數正規化的 GCN 層。
- Gilmer, J., et al. (2017). "Neural Message Passing for Quantum Chemistry". [arXiv:1704.01212](https://arxiv.org/abs/1704.01212) — 提出訊息傳遞框架，並說明多種圖模型都符合它。
- Veličković, P., et al. (2017). "Graph Attention Networks". [arXiv:1710.10903](https://arxiv.org/abs/1710.10903) — 對鄰居學習注意力權重，權重由兩端點的特徵計算。

### 綜述與教科書

（本頁未查核任何項目）

### 講座與影片

（本頁未查核任何項目）

### 文章與文件

- Hamilton, W., Ying, Z. & Leskovec, J. (2017). "Inductive Representation Learning on Large Graphs". [arXiv:1706.02216](https://arxiv.org/abs/1706.02216) — GraphSAGE，對採樣鄰域做聚合，可用於未見過的節點。
- Li, Q., Han, Z. & Wu, X.-M. (2018). "Deeper Insights into Graph Convolutional Networks for Semi-Supervised Learning". [arXiv:1801.07606](https://arxiv.org/abs/1801.07606) — 分析重複圖卷積如何使節點特徵趨於一致。
