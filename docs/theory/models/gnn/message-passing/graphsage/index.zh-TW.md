---
related:
- theory/models/gnn/message-passing
- theory/models/gnn
aliases:
  - Graph Sample and Aggregate
  - GraphSAGE
  - 圖採樣與聚合
tags:
  - graph neural networks
  - inductive learning
  - neighbourhood sampling
translation_reviewed: 2026-10-28
---

# GraphSAGE

GraphSAGE 是一種歸納式（inductive）的節點嵌入方法，由 Hamilton、Ying 與 Leskovec 在 2017 年的論文 "Inductive Representation Learning on Large Graphs"（arXiv:1706.02216）中提出。它不為每個節點學習一個嵌入向量，而是學習一組函數：透過對局部鄰域進行採樣並聚合其特徵，來建構節點的表示。因此，同一組函數也能為訓練時未出現的節點產生嵌入。

## 問題

早期的節點嵌入方法屬於直推式（transductive）。它們為訓練時見過的每個節點學習一個嵌入，並且訓練時需要所有節點都存在，因此無法直接為之後才出現的節點產生嵌入。在大型圖上，對每個節點的所有鄰居做聚合也很昂貴。論文同時處理這兩個問題：它要為未見過的節點產生嵌入，並且要能在鄰域過大、無法完整聚合的圖上運作。

## 核心想法

每個節點的表示是逐層建構的。在每一深度，節點把自己前一深度的表示，與其採樣鄰居表示的聚合結果結合起來，所用的學習權重則在所有節點間共享。由於參數是函數而非每個節點各自的查找表，未見過的節點只要把同一組函數套用到其特徵與鄰域上，就能取得嵌入。鄰居以固定大小的均勻隨機樣本取出，因此無論節點的度數多高，每個批次的成本都固定。論文指出，平均聚合器接近卷積層，而串接節點自身的表示則相當於一種簡單的跳接（skip connection）。

## 方程式或演算法

對每個深度 \(k = 1, \dots, K\)，節點 \(v\) 先聚合其採樣鄰居，再與自身前一深度的表示結合：

\[
h_{\mathcal{N}(v)}^{k} = \mathrm{AGGREGATE}_k\big(\{h_u^{k-1}, \forall u \in \mathcal{S}_{\mathcal{N}(v)}\}\big), \qquad
h_v^{k} = \sigma\big(W^{k} \cdot \mathrm{CONCAT}(h_v^{k-1},\, h_{\mathcal{N}(v)}^{k})\big),
\]

其中 \(\mathcal{S}_{\mathcal{N}(v)}\) 是每次迭代重新抽取的固定大小隨機鄰居樣本。之後每個 \(h_v^{k}\) 進行 L2 正規化，輸出嵌入為 \(z_v = h_v^{K}\)。

論文給出以下聚合器：

- **平均（Mean）：** \(h_v^{k} = \sigma\big(W \cdot \mathrm{MEAN}(\{h_v^{k-1}\} \cup \{h_u^{k-1}, \forall u \in \mathcal{N}(v)\})\big)\)，此形式省略串接步驟。
- **池化（Pool）：** \(\mathrm{AGGREGATE}^{\mathrm{pool}}_k = \max\big(\{\sigma(W_{\mathrm{pool}}\, h_{u_i}^{k-1} + b), \forall u_i \in \mathcal{N}(v)\}\big)\)，即先經過共享的全連接層，再逐元素取最大值。
- **LSTM：** 將 LSTM 套用於鄰居的隨機排列。論文未給出此聚合器的方程式。

無監督訓練時，論文使用基於圖的損失函數。節點 \(u\) 會被拉向與它出現在同一條短隨機漫步上的節點 \(v\)，並被推離負樣本：

\[
J_G(z_u) = -\log\big(\sigma(z_u^{\top} z_v)\big) - Q\, \mathbb{E}_{v_n \sim P_n(v)}\big[\log\big(\sigma(-z_u^{\top} z_{v_n})\big)\big],
\]

其中 \(\sigma\) 為 sigmoid，\(P_n\) 為負採樣分布，\(Q\) 為負樣本數。監督式變體則改用交叉熵損失。實驗中 \(K = 2\)，兩個深度分別採樣 \(S_1 = 25\) 與 \(S_2 = 10\) 個鄰居。每個批次的採樣成本為 \(\prod_i S_i\)；當節點的度數低於樣本大小時，鄰居以有放回的方式抽取。

## 結果

論文報告的是微平均 F1（micro-averaged F1）分數。在其表 1 中，無監督的 GraphSAGE-pool 在引文資料上達到 0.798，而帶特徵的 DeepWalk 為 0.701，原始特徵為 0.575。在 Reddit 上，監督式的 GraphSAGE-LSTM 達到 0.954，GraphSAGE-mean 為 0.950，原始特徵為 0.585。在多圖的 PPI 資料集上（此設定測試對完全未見過之圖的泛化），監督式 GraphSAGE-LSTM 達到 0.612，GraphSAGE-pool 為 0.600，原始特徵為 0.422。論文指出，無監督 GraphSAGE-pool 在引文資料上比帶特徵的 DeepWalk 高出 13.8%，在 Reddit 上高出 29.1%。表中沒有任何單一聚合器在每一欄都最佳。

## 限制

均勻的鄰域採樣會增加變異，非均勻的採樣器留待未來工作。LSTM 聚合器需要鄰居的隨機排列，論文指出其速度約為池化的兩倍慢。把深度增加到 \(K = 2\) 以上，效益遞減而運算成本大增。作者也指出其顯著性檢定較弱，因為只基於六種設定。理論結果是可辨識性（identifiability）論證，並非證明所需函數可以被高效學習，且所需維度在最壞情況下可能是 \(O(|V|)\)。DeepWalk 無法套用於多圖的 PPI 設定，這也是論文比較範圍受限的原因之一。

## 相關連結

GraphSAGE 是[訊息傳遞](../index.md)框架中採用採樣與學習型聚合器的成員。它的平均聚合器，是 [GCN](../gcn/index.md) 中全鄰域平均的歸納式對應做法（GCN 為直推式）。它的池化與 LSTM 聚合器從資料學習其行為，但不像 [GAT](../gat/index.md) 那樣以注意力為鄰居加權。基於求和的替代方法及其表達力結果，見 [GIN](../gin/index.md) 頁面。更完整的家族見[圖神經網路](../../index.md)頁面。

## 未解問題與更多變體

- **採樣策略。** 均勻採樣會增加變異，論文把非均勻採樣器留待未來工作。對於特定的圖，應如何選擇採樣器，目前仍無定論。
- **聚合器的選擇。** 表 1 顯示沒有任何單一聚合器在所有資料集上都最佳，而本頁未提供選擇準則。在論文比較的選項中，LSTM 速度最慢。
- **深度與樣本大小。** 論文發現兩層之後幾乎沒有增益，並使用固定的樣本大小 25 與 10。這些設定如何轉移到度數分布不同的圖上，本頁未予核對。

## 參考文獻

### 開創性論文

- Hamilton, W., Ying, Z. & Leskovec, J. (2017). "Inductive Representation Learning on Large Graphs". arXiv:1706.02216 — GraphSAGE，對採樣鄰域做聚合，可用於未見過的節點。
- Kipf, T. N. & Welling, M. (2016). "Semi-Supervised Classification with Graph Convolutional Networks". arXiv:1609.02907 — 依對稱度數正規化的 GCN 層。
- Veličković, P., et al. (2017). "Graph Attention Networks". arXiv:1710.10903 — 對鄰居學習注意力權重，權重由兩端點的特徵計算。
- Gilmer, J., et al. (2017). "Neural Message Passing for Quantum Chemistry". arXiv:1704.01212 — 提出訊息傳遞框架，並說明多種圖模型都符合它。

### 綜述與教科書

（本頁尚未核對）

### 講座與影片

（本頁尚未核對）

### 文章與文件

- Xu, K., et al. (2018). "How Powerful are Graph Neural Networks?". arXiv:1810.00826 — 顯示聚合函數的表達力限制，並提出基於求和的 GIN。
