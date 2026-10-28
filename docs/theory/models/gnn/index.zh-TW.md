# 圖神經網路（GNN）

## 為什麼需要圖？

許多資料天生是圖：分子（原子＝節點、鍵＝邊）、社群網路、知識圖譜、交通路網、論文引用、蛋白質交互作用、**大腦連結體**。CNN 與 RNN 假設格狀或序列結構，GNN 則處理任意圖。

## 訊息傳遞（Message Passing）

每一層，節點從鄰居收集訊息、聚合、更新自己的表徵：

\[
h_v^{(k+1)} = \text{UPDATE}\Big(h_v^{(k)},\; \text{AGG}_{u\in\mathcal{N}(v)}\, \text{MSG}(h_u^{(k)}, h_v^{(k)}, e_{uv})\Big)
\]

聚合函數必須**置換不變**（sum、mean、max、attention）。

## 組件與變體

訊息如何形成與聚合，以及網路在節點特徵變得模糊之前能有多深，這些在[訊息傳遞](message-passing/index.md)頁面中介紹。該頁比較了正規化卷積、鄰居採樣、注意力，以及基於求和聚合的表達能力。

## 代表模型

| 模型 | 特點 |
|---|---|
| GCN（Kipf & Welling, 2017） | 頻譜圖卷積的一階近似 |
| GraphSAGE | 鄰居取樣，可擴展到大圖、歸納式學習 |
| GAT | 以注意力加權鄰居 |
| GIN | 表達力等同 1-WL 圖同構測試 |
| MPNN | 統一的訊息傳遞框架（量子化學） |
| 等變 GNN（EGNN、NequIP、MACE） | 對 3D 旋轉平移等變，分子模擬 |
| Graph Transformer | 全域注意力＋結構編碼 |

## 任務

- 節點分類（論文主題、詐欺帳戶）
- 邊預測（推薦、藥物交互作用、知識圖譜補全）
- 圖分類／迴歸（分子性質、毒性）
- 圖生成（分子設計）

## 已知問題

- **過度平滑**：層數一多，節點表徵趨於相同
- **過度壓縮（over-squashing）**：遠距資訊被擠在固定大小的向量中
- **表達力上限**：標準訊息傳遞無法區分某些非同構圖

## 重要應用

- **AlphaFold 2** 的結構模組含圖式推理；**GNoME**（2023）用 GNN 預測出大量新穩定晶體
- **GraphCast**（2023）：以 GNN 做全球中期天氣預報，在多數指標上優於傳統數值預報
- 推薦系統（Pinterest PinSage）、Google Maps 到達時間預測
- 藥物發現、材料科學（見 [生命科學](../../../applications/life-science/index.md)、[科學研究](../../../applications/science/index.md)）

## 與神經科學：連結體學

- **連結體（connectome）**：大腦神經元與突觸的完整連線圖。秀麗隱桿線蟲（302 個神經元）早已完成；**果蠅全腦連結體**（FlyWire，約 14 萬個神經元）於 2024 年在 *Nature* 發表
- 研究者以連結體約束的網路模型預測果蠅視覺系統的神經活動（Lappalainen et al., 2024）
- **網路神經科學**：用圖論分析大腦的小世界性、模組化、樞紐（hub）
- MICrONS 計畫（2025）發表小鼠視覺皮質一立方毫米的結構與功能連結資料

## 學習資源

- Stanford CS224W《Machine Learning with Graphs》
- [PyTorch Geometric](https://pyg.org/)、[DGL](https://www.dgl.ai/)
- Hamilton《Graph Representation Learning》（免費 PDF）
- Bronstein et al.《Geometric Deep Learning》（免費線上）

## 參考文獻

### 開創性論文

- Gilmer, J., et al. (2017). "Neural Message Passing for Quantum Chemistry". arXiv:1704.01212 — 提出訊息傳遞框架，並說明多種圖模型都符合它。
- Kipf, T. N. & Welling, M. (2016). "Semi-Supervised Classification with Graph Convolutional Networks". arXiv:1609.02907 — 依對稱度數正規化的 GCN 層。
- Hamilton, W., Ying, Z. & Leskovec, J. (2017). "Inductive Representation Learning on Large Graphs". arXiv:1706.02216 — GraphSAGE，對採樣鄰域做聚合，可用於未見過的節點。
- Veličković, P., et al. (2017). "Graph Attention Networks". arXiv:1710.10903 — 對鄰居學習注意力權重，權重由兩端點的特徵計算。

### 文章與文件

- Xu, K., et al. (2018). "How Powerful are Graph Neural Networks?". arXiv:1810.00826 — 顯示聚合函數的表達力限制，並提出基於求和的 GIN。
- Li, Q., Han, Z. & Wu, X.-M. (2018). "Deeper Insights into Graph Convolutional Networks for Semi-Supervised Learning". arXiv:1801.07606 — 分析重複圖卷積如何使節點特徵趨於一致。
