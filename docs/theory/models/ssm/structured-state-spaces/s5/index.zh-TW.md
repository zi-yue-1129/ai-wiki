---
related:
- theory/models/ssm/structured-state-spaces
- theory/models/ssm
aliases:
  - Simplified State Space Layers
  - S5
  - 簡化狀態空間層
tags:
  - state-space models
  - sequence modelling
  - parallel scan
translation_reviewed: 2026-10-28
---

# S5：簡化狀態空間層

S5 是 Smith、Warrington 與 Linderman 在 2022 年的論文 "Simplified State Space Layers for Sequence Modeling" 中提出的簡化狀態空間層。它以一個多輸入、多輸出的對角 SSM，取代 S4 中單輸入、單輸出 SSM 的集合，並以時間域上的平行掃描計算遞迴。

## 問題

S4 層依賴一組彼此獨立的單輸入、單輸出（SISO）SSM，以及頻率域的卷積。論文的目標是保留 S4 處理長程依賴的能力，同時移除這些實作上相當複雜的機制。

## 核心想法

S5 以兩種方式簡化 S4 層。第一，它以一個潛在維度為 \(P\) 的多輸入、多輸出（MIMO）SSM，取代 SISO 集合。第二，它把狀態矩陣對角化為 \(A = V\Lambda V^{-1}\)，使遞迴可以用平行掃描計算，而不需要卷積核。共軛對稱性使需要儲存的特徵值與狀態數量減半。論文在初始化與時間尺度上也做了三項選擇：

- HiPPO-LegS 無法穩定地對角化，因此 S5 使用對角化的 HiPPO-N 矩陣。論文把 Gu 等人（2022）的一個結果推廣，說明在多輸入設定下，當 \(N\) 增大時，它會近似 HiPPO-LegS。
- 時間尺度是一組可學習的 \(P\) 個值，而非單一純量，論文發現這樣效果較好。
- 也使用由數個 HiPPO-N 區塊組成的區塊對角選項。

## 方程式或演算法

對角化後，系統使用 \(\tilde B = V^{-1}B\) 與 \(\tilde C = CV\)。以步長 \(\Delta\) 進行零階保持離散化，得到

\[
\bar\Lambda = \exp(\Lambda\Delta), \qquad \bar B = \Lambda^{-1}(\bar\Lambda - I)\tilde B ,
\]

遞迴為 \(x_k = \bar\Lambda x_{k-1} + \bar B u_k\)。由於每一步都是狀態上的仿射映射，多步的合成滿足結合律，因此平行掃描能以對數深度計算所有狀態。對於對角 \(A\)，論文給出的總運算量為 \(O(PL)\)。當 \(P = O(H)\)（其中 \(H\) 為模型寬度）時，論文指出 S5 的運行時間與記憶體複雜度與 S4 相當。

## 結果

在 Long Range Arena（LRA）上，論文報告 ListOps 為 62.15、Text 為 89.31、Retrieval 為 91.40、Image 為 88.00、Pathfinder 為 95.33、Path-X 為 98.58，平均為 87.46。同一表格中 S4-LegS 的平均為 86.09。在 16 kHz 的 Speech Commands 上，S5 以 28 萬參數得到 96.52，S4-LegS 為 96.08。在 8 kHz 的零樣本設定下，S5 得到 94.53，S4-LegS 為 91.32。論文還報告相對於 S4D 的訓練步速：ListOps 為 1.1，Text 為 1.0，Path-X 為 4.7。

## 限制

作者指出，HiPPO-LegS 無法穩定地對角化，因此 S5 依賴 HiPPO-N，而這只在狀態維度趨於無限的極限下才有依據。離散時間的 HiPPO-N 變體因穩定性問題而難以訓練，需要低很多的學習率。使用 S4D-Lin 初始化的變體在 Path-X 上得分為 65.60，標準差為 27.00，變異很大。擺錘的速度比較得益於 JAX 編譯，作者表示這並不能完全解釋運行時間的差距。此外，跨 S4 SSM 共用輸出矩陣會使模型變得更具或更不具表達力，目前並不清楚。

## 相關連結

S5 是 [S4](../s4/index.md) 層的簡化形式，與其同屬[結構化狀態空間](../index.md)家族。它的對角選擇承襲 [S4D](../s4d/index.md)，初始化則建立於 [HiPPO](../hippo/index.md) 之上。帶有平行掃描的對角循環，也是[線性循環單元](../linear-recurrent-units/index.md)所使用的設計。更廣的[狀態空間模型](../../index.md)家族涵蓋整個設計，依輸入而變的後繼設計見[選擇性狀態空間](../../selective-state-spaces/index.md)。

## 未解問題與更多變體

- **對角矩陣的選擇。** HiPPO-N 只在狀態維度增大時才有依據，而 S4D-Lin 初始化在 Path-X 上的高變異顯示，初始對角線的選擇很重要。
- **共用輸出。** 跨 S4 SSM 共用輸出矩陣是否改變表達力，論文並未定論。
- **訓練穩定性。** 論文報告離散時間的 HiPPO-N 變體需要低很多的學習率，而在所檢視的章節中，並未給出穩健的訓練方法。

## 參考文獻

### 開創性論文

- Gu, A., Goel, K. & Ré, C. (2021). "Efficiently Modeling Long Sequences with Structured State Spaces". [arXiv:2111.00396](https://arxiv.org/abs/2111.00396) — S4，具正規加低秩結構與快速卷積核。
- Gu, A., Gupta, A., Goel, K. & Ré, C. (2022). "On the Parameterization and Initialization of Diagonal State Space Models". [arXiv:2206.11893](https://arxiv.org/abs/2206.11893) — 仔細初始化的複數對角狀態矩陣，能以較簡單的實作匹敵 S4。
- Gu, A., et al. (2020). "HiPPO: Recurrent Memory with Optimal Polynomial Projections". [arXiv:2008.07669](https://arxiv.org/abs/2008.07669) — 推導 HiPPO 狀態矩陣，透過多項式投影使循環能記住歷史。

### 綜述與教科書

（本頁尚未核對）

### 講座與影片

（本頁尚未核對）

### 文章與文件

- Smith, J. T. H., Warrington, A. & Linderman, S. W. (2022). "Simplified State Space Layers for Sequence Modeling". [arXiv:2208.04933](https://arxiv.org/abs/2208.04933) — S5，帶有平行掃描的對角狀態空間層。
- Orvieto, A., et al. (2023). "Resurrecting Recurrent Neural Networks for Long Sequences". [arXiv:2303.06349](https://arxiv.org/abs/2303.06349) — 對對角線性循環做仔細初始化，在長程基準上與 S4 相當。
