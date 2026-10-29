---
related:
- theory/models/gnn/message-passing
- theory/models/gnn
aliases:
  - Graph Convolutional Networks
  - GCN
  - 圖卷積網路
tags:
  - graph neural networks
  - spectral convolution
  - semi-supervised learning
  - message passing
translation_reviewed: 2026-10-29
---

# 圖卷積網路（GCN）

圖卷積網路（GCN）在只有少數節點有標籤時，對圖中的節點進行分類。此模型由 Kipf 與 Welling（2016）提出。每一層都沿著圖的鄰接矩陣傳播節點特徵，因此網路以圖的結構為條件。傳播步驟會加入自迴圈（self-loop），並在兩側依節點度數做正規化。

## 問題

只有少數節點有標籤時，節點分類很困難。早期的圖方法以加入 Laplacian 正則項來處理，此做法假設相連的節點傾向共享標籤。

## 核心想法

GCN 不再依此假設加入懲罰項，而是讓網路以鄰接矩陣為條件。每一層都用加入自迴圈並做對稱度數正規化的矩陣來傳播特徵。作者把此結果描述為局部化頻譜卷積的一階近似。

### 動態概念解說

![GCN 四階段教學動畫：加入自迴圈、對稱度數正規化、鄰居訊息聚合，以及目標節點的特徵更新。](../../../../../assets/concept-animations/gcn-aggregation-motion.svg)

*原創 CC BY-SA 4.0 教學動畫，依據 Kipf 與 Welling（2016；見參考文獻）。四階段依序呈現加入自迴圈、依度數計算係數、聚合鄰居訊息，以及更新目標節點特徵。MkDocs 網站提供支援鍵盤操作的**播放／暫停**按鈕；偏好減少動態效果時，預設顯示 [GitHub 可閱讀的靜態概覽](../../../../../assets/concept-animations/gcn-aggregation-still.svg)。[開啟完整動畫](../../../../../assets/concept-animations/gcn-aggregation-motion.svg)。*

圖中採用四個節點的星狀圖，目標節點為 $i$，其餘為 $A,B,C$。示意純量特徵分別為 $h_i=0.5,\ h_A=1,\ h_B=1.5,\ h_C=2$。加入自迴圈後，目標節點度數為 $4$，每個葉節點度數為 $2$，因此自身訊息係數為 $1/4$，各鄰居訊息係數為 $1/\sqrt{4\cdot2}$。設定 $W=1$ 並使用 ReLU 時，更新結果為 $0.25(0.5)+(1+1.5+2)/\sqrt{8}\approx1.716$。這些對稱正規化係數**不一定加總為一**，與 softmax 不同。圖中的特徵與數值均為手算教學示例，不是學習所得的嵌入向量或效能實測。

## 方程式或演算法

令 Ã = A + I（I 為單位矩陣，即在鄰接矩陣 A 上加入自迴圈），D̃ 為 Ã 的對角度數矩陣，則一層的計算為

\[
H^{(l+1)} = \sigma\!\left(\tilde{D}^{-1/2}\,\tilde{A}\,\tilde{D}^{-1/2}\,H^{(l)}\,W^{(l)}\right)
\]

此處 H^(l) 為第 l 層的節點特徵堆疊，W^(l) 為該層的權重矩陣，σ 為非線性函數。輸出的每一列，都是節點特徵與鄰居特徵的混合，權重由兩端點的度數決定。

## 結果

在 Citeseer、Cora、Pubmed 與 NELL 上，論文報告的測試準確率依序為 70.3%、81.5%、79.0% 與 66.0%。這些是論文所比較的方法中最好的結果。

## 限制

全批次（full-batch）訓練所需的記憶體隨資料集線性成長。此模型不支援邊的特徵。最佳結果來自兩到三層；若沒有殘差連接，訓練超過約七層的更深模型會變得困難。

## 相關連結

GCN 是訊息傳遞架構中以一階、頻譜為動機的特例，其鄰居聚合是固定的、依度數加權的求和。一般框架見[訊息傳遞](../index.md)頁面，更完整的家族見[圖神經網路](../../index.md)頁面。以注意力與求和為基礎的替代方法，分別見 [GAT](../gat/index.md) 與 [GIN](../gin/index.md) 頁面。

## 未解問題與更多變體

- **邊的特徵。** 如上定義的層沒有接收邊特徵的位置，而[圖神經網路](../../index.md)頁面中的一般訊息函數則包含邊項。如何把邊資訊加入 GCN 層，此頁未涵蓋。
- **深度。** 結果在兩到三層時最好，沒有殘差連接的更深堆疊難以訓練。此頁不涵蓋如何使深層圖卷積可訓練。
- **大圖。** 全批次訓練受記憶體限制。家族頁所列的擴展方法是鄰居採樣，例如 GraphSAGE。

## 參考文獻

### 開創性論文

- Gilmer, J., et al. (2017). "Neural Message Passing for Quantum Chemistry". [arXiv:1704.01212](https://arxiv.org/abs/1704.01212) — 提出訊息傳遞框架，並說明多種圖模型都符合它。
- Kipf, T. N. & Welling, M. (2016). "Semi-Supervised Classification with Graph Convolutional Networks". [arXiv:1609.02907](https://arxiv.org/abs/1609.02907) — 依對稱度數正規化的 GCN 層。
- Hamilton, W., Ying, Z. & Leskovec, J. (2017). "Inductive Representation Learning on Large Graphs". [arXiv:1706.02216](https://arxiv.org/abs/1706.02216) — GraphSAGE，對採樣鄰域做聚合，可用於未見過的節點。
- Veličković, P., et al. (2017). "Graph Attention Networks". [arXiv:1710.10903](https://arxiv.org/abs/1710.10903) — 對鄰居學習注意力權重，權重由兩端點的特徵計算。

### 綜述與教科書

（本頁未查核任何項目）

### 講座與影片

（本頁未查核任何項目）

### 文章與文件

- Xu, K., et al. (2018). "How Powerful are Graph Neural Networks?". [arXiv:1810.00826](https://arxiv.org/abs/1810.00826) — 顯示聚合函數的表達力限制，並提出基於求和的 GIN。
- Li, Q., Han, Z. & Wu, X.-M. (2018). "Deeper Insights into Graph Convolutional Networks for Semi-Supervised Learning". [arXiv:1801.07606](https://arxiv.org/abs/1801.07606) — 分析重複圖卷積如何使節點特徵趨於一致。
