---
related:
- theory/models/transformer
aliases:
  - Message Passing
  - Graph Convolution
  - Graph Attention
  - 訊息傳遞
  - 圖卷積
tags:
  - graph neural networks
  - message passing
  - architecture
translation_reviewed: 2026-10-28
---

# 訊息傳遞

多數圖神經網路遵循同一個模板。每個節點持有一個特徵向量，在每一層它從鄰居收集訊息、聚合它們，然後更新自己的向量。Gilmer 等人（2017）為這個模板取了一個共同的名稱：訊息傳遞框架，並展示了許多早期的圖模型都是它的特例。各種變體的差別在於訊息如何形成、如何聚合，以及更新如何處理節點自身的狀態。這些選擇決定了網路能分辨什麼，以及在節點特徵模糊在一起之前能有多深。

## 核心想法

對於第 \(k\) 層的節點 \(v\)，更新形式為 \(h_v^{(k+1)} = \mathrm{UPDATE}\big(h_v^{(k)}, \mathrm{AGGREGATE}\{\mathrm{MESSAGE}(h_v^{(k)}, h_u^{(k)}, e_{uv}) : u \in \mathcal{N}(v)\}\big)\)。訊息可以依賴邊的特徵 \(e_{uv}\)，而聚合不能依賴鄰居的順序。

## 做法

| 變體 | 訊息與聚合 | 關鍵性質 |
|---|---|---|
| 圖卷積（GCN） | 依度數正規化的鄰居特徵加總 | 簡單，是譜濾波的一階近似 |
| GraphSAGE | 採樣的鄰居，搭配可學習的聚合器 | 可用於大型圖與未見過的節點 |
| 圖注意力（GAT） | 由可學習注意力對鄰居加權 | 對鄰居的加權是自適應的 |
| 圖同構網路（GIN） | 求和聚合，搭配 MLP 更新 | 在相同鄰域資訊下，訊息傳遞模型中表達力最強 |

### 正規化卷積

Kipf 與 Welling（2016）推導出一種以對稱度數正規化來平均鄰居特徵的層，並以譜濾波器的一階近似來說明它的動機。這個層很便宜，在引用圖上表現良好，但固定的權重無法強調特定鄰居。

### 採樣與注意力

GraphSAGE 採樣固定數量的鄰居，並以可學習的函數聚合，使得在無法使用完整鄰域的大圖上也能訓練，也能為訓練時未見過的節點產生嵌入。Veličković 等人（2017）以由兩端點特徵計算的注意力係數取代固定權重，使每個節點依相關性衡量鄰居。

### 表達力

Xu 等人（2018）探討哪些聚合函數能像 Weisfeiler–Leman 檢驗一樣分辨圖。他們證明，搭配 MLP 更新的求和聚合與該檢驗一樣強，而平均與最大值聚合則不然。這個結果解釋了為何在圖分類中常偏好基於求和的設計。

## 關鍵方法

| 方法 | 年份 | 核心想法 | 頁面 |
|---|---|---|---|
| 圖卷積網路（GCN） | 2016 | 依度數正規化的鄰居平均，是頻譜濾波的一階近似 | [GCN](gcn/index.md) |
| 圖注意力網路（GAT） | 2017 | 對鄰居學習注意力權重 | [GAT](gat/index.md) |
| 圖同構網路（GIN） | 2018 | 求和聚合加上 MLP 更新，表達力等同 WL 檢驗 | [GIN](gin/index.md) |
| GraphSAGE | 2017 | 採樣固定數量的鄰居再聚合，可用於未見過的節點 | [GraphSAGE](graphsage/index.md) |

## 取捨

- **表達力與成本。** 更豐富的訊息與注意力每條邊需要更多記憶體；簡單的正規化求和便宜，但表達力較弱。
- **深度。** 堆疊更多層能讓資訊傳得更遠，但重複的平均會使節點特徵趨於一致，這就是過度平滑問題。
- **規模。** 在稠密圖上做完整鄰域聚合很昂貴，因此大型圖會採用採樣。

## 相關連結

訊息傳遞的觀點是 [圖神經網路](../index.md) 家族的核心。對鄰居做注意力，是 Transformer 中 [注意力變體](../../transformer/attention-variants/index.md) 在圖上的對應，只是以圖的結構取代了完整的 token 集合。表達力的問題也與[符號 AI](../../../symbolic-ai/index.md)中關係推理的理論相連。

## 未解問題與更多變體

- **過度平滑。** Li 等人（2018）指出，在許多圖上，只要幾層圖卷積就會使節點特徵變得相似。殘差連接、正規化與跳躍知識設計能減輕這個效應，但完整的解法尚不存在。
- **長程互動。** 訊息傳遞需要很多層才能連接遠處的節點，而深度本身會造成過度平滑與壅塞，因此圖 Transformer 與全域注意力被用作替代方案。
- **基準。** 許多報告的增益很小，且取決於資料集的切分方式，使公平比較變得困難。

## 參考文獻

### 開創性論文

- Gilmer, J., et al. (2017). "Neural Message Passing for Quantum Chemistry". arXiv:1704.01212 — 提出訊息傳遞框架，並說明多種圖模型都符合它。
- Kipf, T. N. & Welling, M. (2016). "Semi-Supervised Classification with Graph Convolutional Networks". arXiv:1609.02907 — 依對稱度數正規化的 GCN 層。
- Hamilton, W., Ying, Z. & Leskovec, J. (2017). "Inductive Representation Learning on Large Graphs". arXiv:1706.02216 — GraphSAGE，對採樣鄰域做聚合，可用於未見過的節點。
- Veličković, P., et al. (2017). "Graph Attention Networks". arXiv:1710.10903 — 對鄰居學習注意力權重，權重由兩端點的特徵計算。

### 綜述與教科書

（本頁尚未核對）

### 講座與影片

（本頁尚未核對）

### 文章與文件

- Xu, K., et al. (2018). "How Powerful are Graph Neural Networks?". arXiv:1810.00826 — 顯示聚合函數的表達力限制，並提出基於求和的 GIN。
- Li, Q., Han, Z. & Wu, X.-M. (2018). "Deeper Insights into Graph Convolutional Networks for Semi-Supervised Learning". arXiv:1801.07606 — 分析重複圖卷積如何使節點特徵趨於一致。
