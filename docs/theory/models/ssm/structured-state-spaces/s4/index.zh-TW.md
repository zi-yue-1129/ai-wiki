---
related:
- theory/models/ssm/structured-state-spaces
- theory/models/ssm
aliases:
  - Structured State Spaces for Long Sequences
  - S4
  - 長序列結構化狀態空間
tags:
  - state-space models
  - long-range memory
  - efficient computation
translation_reviewed: 2026-10-28
---

# S4：長序列結構化狀態空間

S4 是一個用於長序列的結構化狀態空間模型。Gu、Goel 與 Ré 在 2021 年的論文 "Efficiently Modeling Long Sequences with Structured State Spaces" 中提出了它。它保留了以 HiPPO 初始化的循環所具備的長程記憶，並使訓練的速度與卷積相當，因此模型能處理非常長的輸入。

## 問題

當時的模型，包括 Long Range Arena（LRA）基準的基線，在長程依賴上表現不佳。較早的 LSSL 方法需要 \(O(N^2 L)\) 的運算與 \(O(NL)\) 的空間，因此不切實際。

## 核心想法

S4 把 HiPPO 狀態矩陣重新參數化為正規加低秩矩陣，\(A = V\Lambda V^* - PQ^\top\)。由此得到的卷積核可以快速計算，因此訓練的速度與卷積相當。

## 方程式或演算法

SSM 會展開成卷積核

\[
\bar K = (C\bar B,\; C\bar A\bar B,\; \dots,\; C\bar A^{L-1}\bar B).
\]

S4 透過在單位根上的生成函數來評估此核，對低秩項使用 Woodbury 恆等式，將問題化為 Cauchy 核，並以反向 FFT 還原 \(\bar K\)。

## 結果

S4 在 LRA 任務上的平均為 80.48%，論文指出每一個基線的平均都低於 60%。在 Path-X 上，它達到 88.10%，論文指出先前的工作約為 50%，即隨機猜測的水準。它最多快 30 倍，所用記憶體比 LSSL 少 400 倍。

## 限制

作者表示，S4 "may not necessarily be the most suitable model for all types of data"，即不一定是最適合所有資料類型的模型。它在語言建模上與 Transformer 仍有差距。論文的 GPU 實作使用樸素的 \(O(NL)\) Cauchy 演算法。

## 相關連結

S4 是 [結構化狀態空間](../index.md) 頁面所描述的結構化、不依輸入而變的模型，該頁面位於更大的[狀態空間模型](../../index.md)家族之中。它依輸入而變的後繼者是 [Mamba](../../selective-state-spaces/mamba/index.md)，後者放棄了 S4 所依賴的卷積形式。它的循環淵源則與 [RNN](../../../rnn/index.md) 家族中的長記憶問題相連。

## 未解問題與更多變體

- **測度的選擇。** HiPPO 對歷史使用特定的測度。其他測度是否適合其他資料類型，研究尚少。
- **對角形式。** 對角狀態矩陣在基準上效果接近，但它為何如此有效，尚未完全理解。
- **多維輸入。** 把結構推廣到影像與其他網格，有多種相互競爭的設計。

## 參考文獻

### 開創性論文

- Gu, A., Goel, K. & Ré, C. (2021). "Efficiently Modeling Long Sequences with Structured State Spaces". arXiv:2111.00396 — S4，具結構化狀態空間，能高效處理很長的序列。
- Gu, A., et al. (2020). "HiPPO: Recurrent Memory with Optimal Polynomial Projections". arXiv:2008.07669 — 為狀態矩陣提供長程記憶的 HiPPO 框架。
- Gu, A., Gupta, A., Goel, K. & Ré, C. (2022). "On the Parameterization and Initialization of Diagonal State Space Models". arXiv:2206.11893 — 仔細初始化的複數對角狀態矩陣，能以較簡單的實作匹敵 S4。

### 綜述與教科書

（本頁尚未核對）

### 講座與影片

（本頁尚未核對）

### 文章與文件

- Smith, J. T. H., Warrington, A. & Linderman, S. W. (2022). "Simplified State Space Layers for Sequence Modeling". arXiv:2208.04933 — S5，帶有平行掃描的對角狀態空間層。
- Orvieto, A., et al. (2023). "Resurrecting Recurrent Neural Networks for Long Sequences". arXiv:2303.06349 — 對對角線性循環做仔細初始化，在長程基準上與 S4 相當。
