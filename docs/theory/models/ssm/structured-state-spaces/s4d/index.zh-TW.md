---
related:
- theory/models/ssm/structured-state-spaces
- theory/models/ssm
aliases:
  - Diagonal S4
  - S4D
  - 對角結構化狀態空間
tags:
  - state-space models
  - long-range memory
  - initialisation
translation_reviewed: 2026-10-28
---

# S4D：S4 的對角版本

S4D 是 Gu、Gupta、Goel 與 Ré 在 2022 年的論文 "On the Parameterization and Initialization of Diagonal State Space Models" 中提出的對角狀態空間模型。它保留了 S4 的計算方式與參數化，但把對角加低秩的狀態矩陣換成複數對角矩陣。它的效能主要取決於對角線如何初始化。

## 問題

S4 是處理長程依賴的強大模型，但它的狀態矩陣是對角加低秩（DPLR），而計算其卷積核需要複雜的演算法。對角狀態矩陣會簡單得多，但較早的對角模型表現不佳。DSS 顯示，由 HiPPO-LegS 導出的對角矩陣可以接近 S4 的表現。然而，DSS 使用複數 softmax 核，而對角近似為何有效，當時並未解釋。

## 核心想法

S4D 把 S4 的計算方式與參數化，和 DSS 的初始化結合起來。它的核是一個 Vandermonde 矩陣與向量的乘積，複雜度與 S4 相同。論文強調初始化至關重要，因此對角矩陣 \(A\) 的選擇最為關鍵。其理論顯示，從 HiPPO-LegS 移除低秩項會得到一個對角矩陣 HiPPO-D。當狀態大小 \(N\) 增大時，這個對角模型的核會收斂到 S4-LegS 的核。論文提出三種初始化：

- **S4D-LegS**，即對角化的 HiPPO-LegS 矩陣，與 DSS 相同。
- **S4D-Inv**，其虛部依反比律排列，用來近似 S4D-LegS。
- **S4D-Lin**，其虛部線性等距排列，用來近似 S4 的傅立葉式初始化。

## 方程式或演算法

連續系統為 \(x'(t) = Ax(t) + Bu(t)\)、\(y(t) = Cx(t)\)，其核為 \(K(t) = Ce^{tA}B\)。雙線性離散化給出 \(\bar A = (I - \tfrac{\Delta}{2}A)^{-1}(I + \tfrac{\Delta}{2}A)\)。當 \(\bar A\) 為對角矩陣時，離散核是一個 Vandermonde 乘積，\(\bar K = (\bar B^\top \circ C)\,V_L(\bar A)\)，其中 \(V_L(\bar A)_{n,\ell} = \bar A_n^{\ell}\)。逐項寫出為

\[
\bar K_\ell = \sum_{n=1}^{N} C_n\,\bar B_n\,\bar A_n^{\ell}, \qquad \ell = 0, \dots, L-1 .
\]

兩種具名初始化使用以下對角元素：

\[
A_n^{\text{Inv}} = -\tfrac{1}{2} + i\,\tfrac{N}{\pi}\left(\tfrac{N}{2n+1} - 1\right), \qquad A_n^{\text{Lin}} = -\tfrac{1}{2} + i\pi n .
\]

## 結果

摘要指出，S4D 在 Long Range Arena（LRA）上的平均為 85%。LRA 表格中，S4D-Inv 為 85.50，S4D-LegS 為 84.89，原始 S4 為 80.48。在 8 kHz 的 Speech Commands 上，S4D-Inv 為 91.80，S4-LegS 為 91.32。在 sCIFAR 上，S4-LegS 為 91.80，S4D-Inv 為 90.69，S4D-Lin 為 90.42。論文報告，在其 LRA 設定下，只有 S4D-Inv 在 Path-X 上高於隨機水準。

## 限制

作者指出，可對角化並不足夠。幾乎所有矩陣都可對角化，但隨機的對角或稠密實數初始化表現不佳，因此效能取決於初始化。證明忽略了數值表示，這正是 S4 需要低秩修正的原因。即使譜相同，實數變體的表現仍較差。S4D-LegS 是 S4-LegS 的帶雜訊近似，通常略差。收斂結果只對 HiPPO-LegS 成立，而隨機的秩一擾動會產生發散的核。虛部的漸近律是一個由實驗支持的推測。凍結 \(A\) 與 \(B\) 會明顯損害 Speech Commands，而不約束 \(\Re(A)\) 則可能造成不穩定。

## 相關連結

S4D 是 [S4](../s4/index.md) 層的對角情形，位於[結構化狀態空間](../index.md)家族中，而該家族又屬於更廣的[狀態空間模型](../../index.md)家族。它的初始化源自 [HiPPO](../hippo/index.md)。帶有平行計算的對角循環，也是 [S5](../s5/index.md) 與[線性循環單元](../linear-recurrent-units/index.md)的設計。其依輸入而變的後繼設計見[選擇性狀態空間](../../selective-state-spaces/index.md)。

## 未解問題與更多變體

- **對角形式為何有效。** 論文未解釋雙線性離散化為何能使核變得平滑而與 S4 相符，也未確定其他初始化是否同樣有效。
- **初始化設計。** 虛部的規律有實驗支持但未經證明，其他對角選擇可能更好。
- **Path-X。** 在 LRA 設定下，多數 S4D 變體在 Path-X 上失敗，這標示了對角形式在最困難任務上的極限。

## 參考文獻

### 開創性論文

- Gu, A., Gupta, A., Goel, K. & Ré, C. (2022). "On the Parameterization and Initialization of Diagonal State Space Models". arXiv:2206.11893 — 仔細初始化的複數對角狀態矩陣，能以較簡單的實作匹敵 S4。
- Gu, A., et al. (2020). "HiPPO: Recurrent Memory with Optimal Polynomial Projections". arXiv:2008.07669 — 推導 HiPPO 狀態矩陣，透過多項式投影使循環能記住歷史。
- Gu, A., Goel, K. & Ré, C. (2021). "Efficiently Modeling Long Sequences with Structured State Spaces". arXiv:2111.00396 — S4，具正規加低秩結構與快速卷積核。

### 綜述與教科書

（本頁尚未核對）

### 講座與影片

（本頁尚未核對）

### 文章與文件

- Smith, J. T. H., Warrington, A. & Linderman, S. W. (2022). "Simplified State Space Layers for Sequence Modeling". arXiv:2208.04933 — S5，帶有平行掃描的對角狀態空間層。
- Orvieto, A., et al. (2023). "Resurrecting Recurrent Neural Networks for Long Sequences". arXiv:2303.06349 — 對對角線性循環做仔細初始化，在長程基準上與 S4 相當。
