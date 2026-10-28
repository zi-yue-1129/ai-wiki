---
translation_reviewed: 2026-10-28
---

# 奇異值分解（SVD）

奇異值分解把任意實矩陣分解為兩次旋轉與一次對角拉伸，即 \(A = U\Sigma V^\top\)。只保留其中最大的幾項，就得到該矩陣的最佳低秩近似。主成分分析、低秩壓縮與 LoRA 都以此結果為基礎。本頁是[線性代數](index.md)的一部分。

## 概述

任意 \(m\times n\) 實矩陣 \(A\) 都可寫成 \(A = U\Sigma V^\top\)。矩陣 \(U\) 與 \(V\) 為正交矩陣，只會旋轉或反射向量。矩陣 \(\Sigma\) 為對角矩陣，其元素為非負的奇異值 \(\sigma_1 \ge \sigma_2 \ge \dots \ge 0\)。從右往左看，這個映射先旋轉輸入，再沿座標軸依奇異值拉伸，最後再旋轉一次。

與特徵值分解不同，奇異值分解對每個矩陣都存在，包括非方陣，因此適用於資料矩陣與權重矩陣。

## 關鍵概念

- **奇異值與奇異向量**：\(\sigma_i\) 為奇異值，\(\mathbf{v}_i\) 為右奇異向量，\(\mathbf{u}_i\) 為左奇異向量，滿足 \(A\mathbf{v}_i = \sigma_i \mathbf{u}_i\)。
- **秩**：非零奇異值的個數。
- **弗羅貝尼烏斯範數**：\(\|A\|_F^2 = \sum_i \sigma_i^2\)，即所有元素平方和的平方根。
- **偽逆**：\(A^+ = V\Sigma^+U^\top\)，其中 \(\Sigma^+\) 對非零奇異值取倒數。它給出最小平方解。

## 運作方式

奇異值分解與特徵值分解密切相關。由於 \(A^\top A = V\Sigma^2 V^\top\)，右奇異向量是 \(A^\top A\) 的特徵向量，而奇異值平方則是其特徵值。計算奇異值分解時，可先把矩陣化為雙對角形式，再執行迭代的 QR 型演算法，參見 [Golub 與 Van Loan](index.md) 的演算法章節。

關鍵性質是 Eckart–Young 結果。保留前 \(k\) 項：

\[
A_k = \sum_{i=1}^{k} \sigma_i \mathbf{u}_i \mathbf{v}_i^\top
\]

在所有秩不超過 \(k\) 的矩陣 \(B\) 中，\(A_k\) 在弗羅貝尼烏斯範數下最接近 \(A\)，誤差為

\[
\|A - A_k\|_F = \sqrt{\sum_{i>k} \sigma_i^2}.
\]

Eckart 與 Young（1936）在最小平方準則下證明了此最佳性。被捨棄的奇異值正說明截斷會引入多少誤差。奇異值快速衰減的矩陣可以在損失很少的情況下壓縮；奇異值平坦的矩陣則不行。

## 主要方法

- [特徵值分解](eigendecomposition.md)：把方陣對稱矩陣分解為正交的特徵向量。奇異值分解將其推廣到任意矩陣；對半正定對稱矩陣而言，兩種分解一致。
- [截斷奇異值分解](../../model-compression/low-rank-and-efficient-architectures/truncated-svd/index.md)：把 Eckart–Young 結果用於縮小已訓練權重矩陣的實際做法。
- [低秩適應（LoRA）](../../model-compression/low-rank-and-efficient-architectures/lora/index.md)：微調時把權重更新限制為低秩乘積 \(BA\)，而不是在訓練後分解已訓練矩陣。

## 與其他頁面的連結

- [主成分分析](../../paradigms/unsupervised/dimensionality-reduction/pca.md)取中心化資料矩陣的前幾個右奇異向量作為主方向。
- [線性代數](index.md)概述奇異值分解在各種矩陣工具中的位置。
- 就腦而言，奇異值分解是分析神經群體資料的工具，不是神經運算的模型。

## 應用

- **壓縮**：對權重矩陣做截斷奇異值分解，可減少部署模型的儲存與乘法成本。
- **微調**：LoRA 學習秩為 \(r\) 的更新，其中 \(r\) 遠小於矩陣維度（Hu et al., 2021）。
- **降維**：對高維資料做主成分分析，透過中心化資料矩陣的奇異值分解計算。
- **最小平方法**：偽逆給出線性系統的最小範數最小平方解。

## 開放問題

- 如何為特定任務選擇秩 \(k\)。奇異值譜能告訴我們每個選擇的誤差，卻無法說明下游準確率能接受多大的誤差。
- 訓練後網路的奇異值譜衰減是否足夠快，使截斷在各層與各任務上都安全。

## 參考文獻

### 奠基性論文

- Eckart, C. & Young, G. (1936). The approximation of one matrix by another of lower rank. *Psychometrika* 1(3), 211–218. https://doi.org/10.1007/BF02288367 — 給出矩陣在最小平方意義下的最佳秩-k 近似，是截斷奇異值分解的基礎。
- Hu, E. J. et al. (2021). *LoRA: Low-Rank Adaptation of Large Language Models*. arXiv:2106.09685. https://arxiv.org/abs/2106.09685 — 微調時學習低秩權重更新，是截斷秩概念的現代應用。

### 綜述與教科書

- Stewart, G. W. (1993). On the early history of the singular value decomposition. *SIAM Review*. https://epubs.siam.org/doi/10.1137/1035134 — 奇異值分解的歷史。本草稿僅取得摘要頁，未取得全文。
- Golub, G. H. & Van Loan, C. F. (2013). *Matrix Computations*, 4th ed. Johns Hopkins University Press. https://www.press.jhu.edu/books/title/10678/matrix-computations — 涵蓋奇異值分解的計算及其在最小平方問題中的應用。
- Trefethen, L. N. & Bau, D. (1997). *Numerical Linear Algebra*. SIAM. https://people.maths.ox.ac.uk/trefethen/text.html — 研究所程度教材，涵蓋奇異值分解及其數值行為。

### 講義

- Strang, G., *18.06 Linear Algebra*, MIT. https://web.mit.edu/18.06/www/ — 課程講次包含一講奇異值分解。
