---
related:
- theory/models/ssm/selective-state-spaces
- theory/models/ssm
aliases:
  - Mamba-2
  - Structured State Space Duality
  - SSD
  - 結構化狀態空間對偶
tags:
  - state-space models
  - structured matrices
  - attention duality
  - hardware-efficient training
translation_reviewed: 2026-10-28
---

# Mamba-2

Mamba-2 是 Dao 與 Gu 在 2024 年的論文 "Transformers are SSMs: Generalized Models and Efficient Algorithms Through Structured State Space Duality"（[arXiv:2405.21060](https://arxiv.org/abs/2405.21060)，ICML 2024）中提出的選擇性狀態空間架構。它把每個頭的狀態轉移限制為純量乘以單位矩陣，使該層成為一種結構化的遮罩注意力，且其計算大部分可以以矩陣乘法執行。

## 問題

Mamba 的選擇性掃描比早期的 SSM 實作快，但它是以循序掃描執行，無法使用現代加速器主要依賴的矩陣乘法單元。論文也指出，狀態空間模型與注意力通常被視為兩個分開的家族。作者想知道：重新表述計算能否讓選擇性 SSM 更快，而同一種重新表述能否說明兩個家族之間的關係。

## 核心想法

Mamba-2 把每個頭的狀態矩陣設為純量乘以單位矩陣，而 Mamba 使用的是對角矩陣。論文把由此產生的對應關係稱為狀態空間對偶（state space duality，SSD）。在純量轉移下，從輸入到輸出的映射是一個半可分矩陣（semiseparable matrix），可以用兩種等價的方式計算：作為作用於狀態的線性遞迴，或作為形狀與注意力相同的單一遮罩矩陣乘積。此層把序列切成數個區塊。區塊內部使用矩陣形式，能很好地對應到矩陣單元；區塊之間則透過一段短掃描傳遞壓縮後的狀態。論文報告，循環狀態可以在幾乎不損失速度的情況下加大。

## 方程式或演算法

在純量轉移 \(a_t\) 下，遞迴為

\[
h_t = a_t\, h_{t-1} + B_t\, x_t, \qquad y_t = C_t^{\top} h_t,
\]

整段序列上的映射為 \(y = Mx\)，其中

\[
M_{ji} = (a_j a_{j-1}\cdots a_{i+1})\,(C_j^{\top} B_i) \qquad (j \ge i)。
\]

以矩陣形式寫成 \(M = L \circ (C B^{\top})\)，其中 \(L\) 是由 \(a_t\) 的累積乘積構成的下三角遮罩。對偶的二次形式為 \((L \circ QK^{\top})V\)，其中 \(Q = C\)、\(K = B\)、\(V = X\)。分塊演算法以此二次形式計算 \(M\) 的對角區塊；非對角區塊則以低秩因子分三步處理：每個區塊從零初始狀態算出其最終狀態，一段跨區塊的短掃描傳播真正的狀態，最後每個區塊把進入的狀態映射為輸出。

## 結果

摘要指出，SSD 層比 Mamba 最佳化過的選擇性掃描實作快 "2-8X"（2 至 8 倍）。論文指出，其循環狀態可以是 Mamba 的 "8× the size of Mamba or even higher"（8 倍大小或更大），且 "with minimal slowdown"（速度僅有極小下降）。與 FlashAttention-2 相比，論文指出 SSD 實作具競爭力：在序列長度約 2K 時交叉，在長度 16K 時快 6 倍。在 Pile 上，2.7B 參數、訓練 300B token 的 Mamba-2，勝過在相同資料上訓練的 Mamba-2.8B、Pythia-2.8B 與 Pythia-6.9B。論文也主張，在 Chinchilla 式的擴展下，Mamba-2 在困惑度與牆鐘時間上帕累托支配 Mamba 與 Transformer++；但此主張的實驗細節未在本頁核對。

## 限制

純量轉移確實是一項限制。論文表示，此設計 "slightly decreasing the expressive power in return for significant training efficiency improvements"（以顯著的訓練效率提升，換取表達力的小幅下降）。與注意力的連結只涵蓋某些注意力變體，而對偶形式捨棄了 softmax。1-SS 形式的表達力嚴格弱於一般的半可分結構化遮罩注意力，且無法寫成標準的 SSM。對於短序列，二次模式可能比線性模式更有效率；在論文的比較中，約 2K token 以下時 SSD 實作慢於 FlashAttention-2。

## 相關連結

Mamba-2 是對 [Mamba](../mamba/index.md) 選擇性 SSM 的改良：保留依輸入而變的參數，但讓每個頭使用純量轉移。它位於[選擇性狀態空間](../index.md)家族之中，該家族屬於更大的[狀態空間模型](../../index.md)家族。此譜系所起源的靜態結構化模型是 [S4](../../structured-state-spaces/s4/index.md)。注意力對偶把 Mamba-2 與[注意力變體](../../../transformer/attention-variants/index.md)頁面連結起來，該頁面涵蓋另一條通往高效長上下文的路線。

## 未解問題與更多變體

- **純量轉移的代價。** 論文為了速度接受表達力的小幅損失。在同一個頭內需要許多不同衰減速率的任務上，此損失有多大，本頁未予量測。
- **對偶的適用範圍。** 此等價關係涵蓋某些注意力變體，並捨棄 softmax。類似結構是否適用於 softmax 注意力，以及一般半可分形式在 1-SS 之外增加了什麼，仍是開放問題。
- **短上下文的速度。** 區塊內的二次形式以記憶體換取矩陣單元上的速度。在約 2K token 以下，論文自己的 FlashAttention-2 比較對 FlashAttention-2 較有利；能縮小此差距的核心設計，本頁未涵蓋。

## 參考文獻

### 開創性論文

- Dao, T. & Gu, A. (2024). "Transformers are SSMs: Generalized Models and Efficient Algorithms Through Structured State Space Duality". [arXiv:2405.21060](https://arxiv.org/abs/2405.21060) — Mamba-2，以及選擇性 SSM 與結構化注意力之間的對偶關係。
- Gu, A. & Dao, T. (2023). "Mamba: Linear-Time Sequence Modeling with Selective State Spaces". [arXiv:2312.00752](https://arxiv.org/abs/2312.00752) — 依輸入而變的狀態空間參數，並以硬體感知的平行掃描實作。
- Gu, A., Goel, K. & Ré, C. (2021). "Efficiently Modeling Long Sequences with Structured State Spaces". [arXiv:2111.00396](https://arxiv.org/abs/2111.00396) — S4，具結構化狀態空間，能高效處理很長的序列。
- Gu, A., et al. (2020). "HiPPO: Recurrent Memory with Optimal Polynomial Projections". [arXiv:2008.07669](https://arxiv.org/abs/2008.07669) — 為狀態矩陣提供長程記憶的 HiPPO 框架。

### 綜述與教科書

（本頁尚未核對）

### 講座與影片

（本頁尚未核對）

### 文章與文件

- Orvieto, A., et al. (2023). "Resurrecting Recurrent Neural Networks for Long Sequences". [arXiv:2303.06349](https://arxiv.org/abs/2303.06349) — 仔細設計的線性循環單元，在長序列基準上能與 SSM 匹敵。
