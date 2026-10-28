---
translation_reviewed: 2026-10-28
---

# 截斷 SVD 與 Eckart–Young 定理

截斷奇異值分解保留矩陣最大的 $k$ 個奇異值，捨棄其餘部分。得到的是與原矩陣最接近的秩為 $k$ 的矩陣，因此它是低秩壓縮的標準工具。它是[AI 的線性代數](../index.md)三個關鍵方法之一。

## 概述

AI 中許多矩陣接近低秩：權重矩陣可能主要沿少數方向作用，資料矩陣也可能主要沿少數軸變化。以保留大部分作用的較簡單矩陣取代它，即可節省儲存與計算。

關鍵在於「最接近」是什麼意思。Eckart 與 Young（1936）針對 Frobenius 範數（即所有元素平方和的平方根）回答了這個問題：保留前幾個奇異值及其向量，捨棄其餘部分。

## 核心概念

- **奇異值與奇異向量**：每個實矩陣 $A \in \mathbb{R}^{m\times n}$ 都可分解為 $A = U\Sigma V^\top$。向量 $u_i$ 與 $v_i$ 為正交單位向量，$\sigma_i$ 是由大到小排列的奇異值。
- **秩 $k$ 截斷**：由 SVD 前 $k$ 項組成的矩陣 $A_k$。
- **Frobenius 範數**：$\lVert M\rVert_F = \sqrt{\sum_{ij} M_{ij}^2}$。

## 運作方式

Eckart–Young 定理指出，在所有秩至多為 $k$ 的矩陣 $B$ 之中，

$$
\lVert A - A_k \rVert_F = \min_{\operatorname{rank}(B)\le k} \lVert A - B \rVert_F,
\qquad
\lVert A - A_k \rVert_F^2 = \sum_{i>k} \sigma_i^2 .
$$

因此誤差就是被捨棄的奇異值所承載的能量。舉一個小例子：取 $A = \begin{pmatrix} 3 & 0 \\ 0 & 1 \end{pmatrix}$。它的奇異值是 3 與 1，最佳的秩 1 近似保留 3 這一項，誤差在 Frobenius 範數與譜範數下都是 1。

此方法分四步進行：

1. 計算 SVD $A = U\Sigma V^\top$。古典演算法（Golub 與 Kahan，1965）在數值上是穩定的。
2. 依目標誤差或目標大小選擇 $k$。
3. 保留 $U$ 與 $V$ 的前 $k$ 行，以及前 $k$ 個奇異值。
4. 儲存因子 $U_k$、$\Sigma_k$ 與 $V_k$，而不儲存 $A$。對向量 $x$ 套用此近似的成本為 $U_k(\Sigma_k(V_k^\top x))$，所需儲存約為 $k(m+n)$ 個數字，而非 $mn$ 個。

對神經網路而言，同樣的步驟適用於權重矩陣 $W$，以兩個較瘦的因子取代，這是[模型壓縮](../../../model-compression/index.md)中的常見做法。

## 結果

這個定理是精確的，因此沒有基準測試。它的實用價值取決於重建誤差能在多大程度上預測訓練後網路的損失，以下三項證據與此相關。

- **權重的冗餘。** Denil 等人（2013）顯示，訓練完成的網路有大量參數冗餘。依其摘要，在最佳情況下，超過 95% 的權重可由一小部分學得的權重預測，而準確度不降。它不是截斷 SVD，但支持了權重可以被壓縮的前提。
- **學得的低秩更新。** LoRA（Hu 等人，2021）是相關但不同的方法。它在凍結的權重上訓練低秩更新，而非截斷權重。在 GPT-3 175B 上，摘要報告其可訓練參數減少為全參數微調（以 Adam 進行）的 1/10,000，GPU 記憶體減為 1/3；在 RoBERTa、DeBERTa、GPT-2 與 GPT-3 上，品質與微調相當或更好。

## 限制

- **重建誤差不等於準確度。** 這個定理最小化的是矩陣誤差，而非模型損失。若誤差落在網路依賴的方向上，即使很小，仍可能損害準確度。
- **衰減緩慢。** 許多訓練後的權重矩陣，其奇異值衰減得很慢，因此要達到小誤差需要很大的 $k$，壓縮的效益就會消失。
- **完整 SVD 的成本。** 稠密的 $m\times n$ 矩陣的精確 SVD 需要約 $mn\min(m,n)$ 次運算，這促成了[隨機化 SVD](../randomized-svd/index.md)的發展。
- **只適用於線性情形。** 層與層之間的非線性激活意味著一層的誤差會沿網路傳播。
- **常需重新訓練。** 若截斷後沒有微調，準確度可能大幅下降。

## 未解問題

- 每一層的秩應如何選擇，考慮到各層譜的差異？
- 權重的重建誤差很小，是否會轉化為網路計算內容的微小改變？
- 在同樣的準確度下，LoRA 所需的秩與截斷所需的秩相比如何？

## 參考文獻

### 開創性論文

- Eckart, C. & Young, G.（1936）. The Approximation of One Matrix by Another of Lower Rank. *Psychometrika*. https://doi.org/10.1007/BF02288367 — 最初的結果：矩陣的最佳低秩近似由其截斷 SVD 給出。
- Golub, G. & Kahan, W.（1965）. Calculating the Singular Values and Pseudo-Inverse of a Matrix. *Journal of the Society for Industrial and Applied Mathematics Series B Numerical Analysis*. https://doi.org/10.1137/0702016 — 提出計算 SVD 的穩定演算法，方法是先雙對角化再對角化。
- Denil, M. 等人（2013）. Predicting Parameters in Deep Learning. https://arxiv.org/abs/1306.0543 — 顯示數個深度網路的許多權重有冗餘，可由一小部分學得的權重預測。
- Hu, E. J. 等人（2021）. LoRA: Low-Rank Adaptation of Large Language Models. https://arxiv.org/abs/2106.09685 — 在凍結的預訓練權重上訓練低秩更新矩陣，以進行高效率的微調。

### 綜述與教科書

- Kolda, T. G. & Bader, B. W.（2009）. Tensor Decompositions and Applications. *SIAM Review*. https://doi.org/10.1137/07070111X — 綜述高階張量分解，以及它與矩陣 SVD 的關係。
- Halko, N., Martinsson, P. G. & Tropp, J. A.（2011）. Finding Structure with Randomness: Probabilistic Algorithms for Constructing Approximate Matrix Decompositions. *SIAM Review*. https://doi.org/10.1137/090771806 — 綜述隨機化演算法，在大型矩陣上比精確方法更快地近似截斷 SVD。
