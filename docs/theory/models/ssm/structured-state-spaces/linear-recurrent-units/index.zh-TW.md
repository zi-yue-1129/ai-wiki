---
related:
- theory/models/ssm/structured-state-spaces
- theory/models/ssm
aliases:
  - Linear Recurrent Unit
  - LRU
  - 線性循環單元
tags:
  - state-space models
  - recurrent neural networks
  - initialisation
translation_reviewed: 2026-10-28
---

# 線性循環單元

線性循環單元（LRU）是一個對角的線性循環層，由 Orvieto 等人在 2023 年的論文 "Resurrecting Recurrent Neural Networks for Long Sequences" 中提出。它的問題是：一旦找出深層 SSM 中真正重要的特徵，深層 RNN 能否在長序列上追上它們。答案是移除遞迴中的非線性，並採用穩定的複數對角參數化。

## 問題

循環網路在長序列上推論很快，但很難最佳化，訓練也慢。S4 等深層 SSM 在長程任務上表現良好，而且可以平行訓練，但不清楚是哪些特徵帶來這些表現。論文提問：深層 RNN 能否匹敵深層連續時間 SSM 的表現與效率。

## 核心想法

作者從標準的深層 RNN 出發，逐項套用一系列改動並分別做消融實驗。最後得到的 LRU 位於與 S4 類模型相同的區塊結構中，即正規化、循環、GLU 與跳接。這些改動包括：

1. **線性循環。** 把遞迴中的非線性移除，改由逐位置的 MLP 或 GLU 區塊提供非線性。
2. **複數對角循環。** 以對角矩陣取代稠密的循環矩陣，使平行掃描成為可能。
3. **穩定的指數參數化。** 分別控制每個特徵值的模長與相位，使特徵值在訓練中保持在單位圓盤內。
4. **環狀初始化。** 特徵值從半徑為 \(r_{\min}\) 與 \(r_{\max}\) 的環上均勻取樣；對於很長的序列，相位被限制在接近零的細片段內。
5. **正規化。** 輸入以一個可學習的因子 \(\gamma\) 縮放，使特徵值接近單位圓時前向傳播不會爆炸。

## 方程式或演算法

展開後，線性遞迴為 \(x_k = \sum_{j=0}^{k-1} A^j B u_{k-j}\)，當所有特徵值滿足 \(|\lambda_j| < 1\) 時是穩定的。LRU 把每個特徵值參數化為

\[
\lambda_j = \exp\!\left(-\exp(\nu_j) + i\,\exp(\theta_j)\right),
\]

並使用遞迴

\[
x_k = \Lambda\,x_{k-1} + \exp(\gamma)\odot(B u_k), \qquad y_k = C x_k + D u_k .
\]

初始化時，正規化因子為 \(\gamma_j = \log\sqrt{1 - |\lambda_j|^2}\)。環狀初始化取樣 \(\nu = -\tfrac{1}{2}\log\left(u_1(r_{\max}^2 - r_{\min}^2) + r_{\min}^2\right)\) 與 \(\theta = 2\pi u_2\)，其中 \(u_1, u_2 \sim U[0,1]\) 彼此獨立。論文指出，當 \(r_{\min} = r_{\max} = r\) 時，此初始化的前向傳播期望增益在 \(r \to 1\) 時趨近於 \(1/(1 - r^2)\)。

## 結果

在 LRA 上，論文以平均數與標準誤差報告測試準確率。LRU 在 sCIFAR 上為 89.0、ListOps 為 60.2、Text 為 89.4、Retrieval 為 89.9、Pathfinder 為 95.1、Path-X 為 94.2。論文重現的 S4D 在 Path-X 上為 97.5，論文中 S5 的結果為 98.6。論文沒有報告單一的 LRA 平均值。作者表示，LRU 在所有 LRA 任務上「達到與這些深層 SSM 相近的表現」。他們還指出，同時使用 \(\gamma\) 正規化與限制初始相位，對解決 Path-X 至關重要。在 sCIFAR 上，對角線性 RNN 的訓練速度約為使用 ReLU 的稠密 RNN 的 8 倍，作者表示這與他們的 S4D 與 S5 實作相當。

## 限制

在後續修改之前，單獨的線性 RNN 區塊在 sCIFAR、Pathfinder 與 Path-X 上遠遠落後於 S4。沒有正規化時 Path-X 會失敗，只有正規化時模型仍無法泛化。沒有 \(\gamma\) 正規化的受限相位無法被學習。相位限制只在 Path-X 上探索過。在圓盤上均勻的初始化只在寬度趨於無限的極限下才與 Glorot 初始化相符。對角模型的訓練穩定性可能低於稠密模型，作者指出，學習率夠小時系統較不容易不穩定。複數參數必須以兩個實數浮點數的成對形式儲存。實驗只涵蓋 LRA，使用六層網路與三個隨機種子，作者表示他們的目標不是超越以 S4 為基礎的模型。

## 相關連結

LRU 是具平行計算的對角複數循環，因此與 [S4D](../s4d/index.md) 及 [S5](../s5/index.md) 同屬[結構化狀態空間](../index.md)家族，而該家族又屬於更廣的[狀態空間模型](../../index.md)家族。它的初始化與 [HiPPO](../hippo/index.md) 不同，採用的是環狀取樣而非多項式投影。它也是現代化的深層 RNN，因而連結到 [RNN](../../../rnn/index.md) 家族，以及如何訓練長記憶循環的問題。

## 未解問題與更多變體

- **相位限制是否適用於 Path-X 以外的任務。** 論文未在其他 LRA 任務上測試較小的初始相位，因此在那些任務上的效益並不清楚。
- **規模。** 結果來自六層網路與三個隨機種子的 LRA。更大規模的行為，以及在語言上的表現，論文並未涵蓋。
- **初始化理論。** 環狀初始化與標準初始化之間的對應，只在寬度趨於無限的極限下獲得證明，因此有限寬度下的行為仍依賴實驗。

## 參考文獻

### 開創性論文

- Gu, A., Goel, K. & Ré, C. (2021). "Efficiently Modeling Long Sequences with Structured State Spaces". arXiv:2111.00396 — S4，具正規加低秩結構與快速卷積核。
- Gu, A., Gupta, A., Goel, K. & Ré, C. (2022). "On the Parameterization and Initialization of Diagonal State Space Models". arXiv:2206.11893 — 仔細初始化的複數對角狀態矩陣，能以較簡單的實作匹敵 S4。
- Gu, A., et al. (2020). "HiPPO: Recurrent Memory with Optimal Polynomial Projections". arXiv:2008.07669 — 推導 HiPPO 狀態矩陣，透過多項式投影使循環能記住歷史。

### 綜述與教科書

（本頁尚未核對）

### 講座與影片

（本頁尚未核對）

### 文章與文件

- Smith, J. T. H., Warrington, A. & Linderman, S. W. (2022). "Simplified State Space Layers for Sequence Modeling". arXiv:2208.04933 — S5，帶有平行掃描的對角狀態空間層。
- Orvieto, A., et al. (2023). "Resurrecting Recurrent Neural Networks for Long Sequences". arXiv:2303.06349 — 仔細設計的線性循環單元，在長序列基準上能與 SSM 匹敵。
