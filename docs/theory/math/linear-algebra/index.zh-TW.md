---
translation_reviewed: 2026-10-28
---

# AI 所需的線性代數

線性代數把資料描述為向量，把轉換描述為矩陣。神經網路幾乎每一層、每個嵌入（embedding）與每個注意力分數，都由向量與矩陣的乘積構成，因此本頁涵蓋 AI 最常用的部分。它是[數學基礎概述](../index.md)中篇幅最大的一部分。

## 概述

向量是一串有順序的數字，可以看成空間中的一個點，也可以看成一個方向。矩陣是作用在向量上的數表：以矩陣乘以向量，會旋轉、拉伸或投影該向量。神經網路的一層計算 \(y = \sigma(Wx + b)\)，其中 \(W\) 是轉換輸入的矩陣，\(\sigma\) 是非線性函數。訓練與推論的大部分運算，都花在這類矩陣乘積上。

本主題圍繞三個問題展開。一個轉換會如何改變空間？它拉伸最多的方向，由特徵向量與奇異向量給出。一個矩陣實際承載多少資訊？答案是它的秩。如何衡量向量之間的距離與相似度？這是範數與內積的工作。

## 關鍵概念

- **內積與餘弦相似度**：\(\mathbf{a}\cdot\mathbf{b} = \sum_i a_i b_i\)。以向量長度正規化後即為餘弦相似度，用於語意搜尋與比較嵌入。
- **矩陣形狀**：\(m\times n\) 矩陣乘以 \(n\times p\) 矩陣，得到 \(m\times p\) 矩陣。深度學習程式中的許多錯誤都是形狀錯誤。
- **秩**：線性獨立的欄數。秩為 \(r\) 的矩陣可寫成 \(r\) 個秩一矩陣之和。
- **範數**：\(\|\mathbf{x}\|_2 = \sqrt{\sum_i x_i^2}\) 與 \(\|\mathbf{x}\|_1 = \sum_i |x_i|\)。以範數構成的懲罰項可以正規化權重。
- **投影**：子空間中離某向量最近的點。最小平方回歸就是把目標投影到特徵所張成的空間上。

## 運作方式

有兩種分解在 AI 中扮演最重要的角色：

- [特徵值分解](eigendecomposition.md) 把方陣與對稱矩陣寫成 \(A = Q\Lambda Q^\top\)。\(Q\) 的欄是正交的特徵向量，\(\Lambda\) 的對角線是特徵值。它描述共變異數矩陣與損失函數的曲率。
- [奇異值分解](svd.md) 把任意矩陣寫成 \(A = U\Sigma V^\top\)。\(\Sigma\) 對角線上的奇異值依重要性排序，只保留最大的幾個，即得到最佳的低秩近似：

\[
A_k = \sum_{i=1}^{k} \sigma_i\, \mathbf{u}_i \mathbf{v}_i^\top
\]

把資料投影到前 \(k\) 個右奇異向量上，就是主成分分析（PCA）。[LoRA](../../model-compression/low-rank-and-efficient-architectures/lora/index.md) 等低秩配接器則把同樣的低秩概念套用在微調時的權重更新上。

## 主要方法

兩個代表性的矩陣分解承載了本主題的大部分內容，各自有獨立的頁面。

- [奇異值分解](svd.md)：適用於任意矩陣，包括非方陣，並給出最佳低秩近似。
- [特徵值分解](eigendecomposition.md)：只適用於方陣；對稱矩陣的特徵向量彼此正交，給出拉伸的正交方向。

資料矩陣與權重矩陣通常是非方陣，用奇異值分解；共變異數矩陣與海森矩陣是方陣且對稱，用特徵值分解。

## 與其他頁面的連結

- [機率與統計](../probability-statistics/index.md) 使用共變異數矩陣，它是對稱且半正定的。
- [微積分與最佳化](../calculus/index.md) 使用海森矩陣，其特徵值描述各方向上的曲率。
- [主成分分析](../../paradigms/unsupervised/dimensionality-reduction/pca.md) 是非監督學習中奇異值分解與特徵值分解的標準應用。
- [截斷奇異值分解](../../model-compression/low-rank-and-efficient-architectures/truncated-svd/index.md) 以相同的秩截斷來壓縮已訓練的權重矩陣。
- 腦與認知：許多神經元在一段時間內的記錄會形成矩陣。PCA 等降維方法常用來找出這類記錄中的低維結構。這是分析工具，不是關於大腦如何運算的主張。

## 應用

- **低秩微調**：LoRA 凍結預訓練的權重矩陣，只學習低秩的更新，使可訓練參數維持在很小的規模（Hu et al., 2021）。
- **模型壓縮**：以截斷奇異值分解取代大型權重矩陣，可減少儲存與乘法成本，代價是些許近似誤差。
- **最小平方法**：偽逆 \(A^+ = V\Sigma^+U^\top\) 給出超定線性系統的最小平方解，實務上透過奇異值分解計算。
- **嵌入**：相似度搜尋以內積比較向量，通常會先正規化。

## 開放問題

- 應保留多大的秩？截斷會保留奇異值最大的方向，但沒有通用規則告訴我們，對某項任務應保留幾個。
- 微調時的權重更新本質上是否為低秩？在許多已報告的情境中低秩方法表現良好，但答案取決於模型與任務。
- 數值精度：訓練時使用的 [量化](../../model-compression/quantisation/index.md) 等低精度運算會改變矩陣乘積的精確度，其對分解的影響尚未完全釐清。

## 參考文獻

### 奠基性論文

- Eckart, C. & Young, G. (1936). The approximation of one matrix by another of lower rank. *Psychometrika* 1(3), 211–218. https://doi.org/10.1007/BF02288367 — 證明在最小平方意義下，矩陣的最佳秩-k 近似由截斷分解給出，是截斷奇異值分解的基礎。
- Hu, E. J. et al. (2021). *LoRA: Low-Rank Adaptation of Large Language Models*. arXiv:2106.09685. https://arxiv.org/abs/2106.09685 — 凍結預訓練權重並學習低秩更新，是低秩結構在 AI 中最主要的現代應用。

### 綜述與教科書

- Stewart, G. W. (1993). On the early history of the singular value decomposition. *SIAM Review*. https://epubs.siam.org/doi/10.1137/1035134 — 追溯奇異值分解的歷史。本草稿僅取得摘要頁，未取得全文。
- Golub, G. H. & Van Loan, C. F. (2013). *Matrix Computations*, 4th ed. Johns Hopkins University Press. https://www.press.jhu.edu/books/title/10678/matrix-computations — 數值矩陣演算法的標準參考，適合想實作或分析分解方法的讀者。
- Trefethen, L. N. & Bau, D. (1997). *Numerical Linear Algebra*. SIAM. https://people.maths.ox.ac.uk/trefethen/text.html — 研究所程度的數值線性代數教科書，兼顧理論與實際行為。

### 講義

- Strang, G., *18.06 Linear Algebra*, MIT. https://web.mit.edu/18.06/www/ — 課程講次包含消去法、特徵值、奇異值分解與投影，適合作為第一門課程。
