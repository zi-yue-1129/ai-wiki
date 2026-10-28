---
translation_reviewed: 2026-10-28
---

# 平均場變分推論

平均場變分推論以每個潛在變數一個獨立因子的乘積來近似後驗。各因子依序以閉式規則更新，形成對 ELBO 的座標上升。本頁是[變分推論](index.md)的一部分。

## 概述

平均場分布族假設潛在變數在 \(q\) 之下彼此獨立：\(q(z)=\prod_j q_j(z_j)\)。這是很強的假設，因為真實後驗中變數之間往往有相關性。作為代價，ELBO 變得夠簡單，使許多具共軛先驗的模型中，每個因子的更新都能以閉式計算。

## 關鍵概念

- **因式分解的分布族**：\(q(z)=\prod_j q_j(z_j)\)，每個潛在變數或變數區塊對應一個因子。
- **座標上升**：固定其他因子，一次只更新一個因子。每一步都不會使 ELBO 下降。
- **共軛性**：當先驗與概似共軛時，更新會停留在已知的分布族中。
- **低估的變異數**：因式分解的分布族通常使近似後驗比真實後驗更窄。

## 運作方式

在其他因子固定時，因子 \(j\) 的最佳更新為

\[
\log q_j^{*}(z_j) = \mathbb{E}_{\prod_{k\ne j} q_k}\big[\log p(x, z)\big] + \text{const}.
\]

演算法依序循環各因子，用其他因子的當前值重新計算每一個，直到 ELBO 不再增加。Jordan 等人（1999）為圖模型推導了這些更新，其中期望只需要局部項。

## 主要方法

- [隨機變分推論](stochastic-variational-inference.md)：保留共軛模型的因式分解結構，但以小批次資料的雜訊自然梯度步取代完整的座標更新。
- [變分自編碼器（VAE）](../../unsupervised/density-and-generative-models/vae/index.md)：以網路輸出各因子，取代逐變數的更新，即攤銷推論。

## 與其他頁面的連結

- [變分推論](index.md)說明 ELBO 與其他近似分布族。
- [機率與統計](../../../math/probability-statistics/index.md)提供更新所需的共軛先驗與指數族背景。
- 就腦而言，平均場的想法是描述神經元群體如何以局部計算近似聯合後驗的一種方式。這是建模假說，而非既定結果。

## 應用

- **主題模型**：潛在狄利克雷分配及相關共軛模型的平均場更新（Blei et al., 2017）。
- **圖模型**：貝氏網路上以局部訊息傳遞進行的近似推論（Jordan et al., 1999）。

## 開放問題

- 因式分解可能嚴重低估後驗的相關性。常用的補救方法是結構化平均場與較豐富的分布族。
- 更新順序與局部最優會影響結果，大型模型的收斂也可能很慢。

## 參考文獻

### 奠基性論文

- Jordan, M. I., Ghahramani, Z., Jaakkola, T. S. & Saul, L. K. (1999). An introduction to variational methods for graphical models. *Machine Learning* 37(2), 183–233. https://doi.org/10.1023/A:1007665907178 — 為圖模型推導平均場座標更新。
- Blei, D. M., Kucukelbir, A. & McAuliffe, J. D. (2017). Variational inference: a review for statisticians. *Journal of the American Statistical Association* 112(518), 859–877. https://doi.org/10.1080/01621459.2017.1285773 — 以範例說明平均場分布族及其座標上升演算法。

### 綜述與教科書

- Wainwright, M. J. & Jordan, M. I. (2008). Graphical models, exponential families, and variational inference. *Foundations and Trends in Machine Learning*. https://nowpublishers.com/article/Details/MAL-001 — 把平均場近似與指數族連結起來。
- Bishop, C. M. (2006). *Pattern Recognition and Machine Learning*. Springer. https://www.microsoft.com/en-us/research/wp-content/uploads/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf — 近似推論一章涵蓋具因式分解後驗的變分貝氏。
- Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. MIT Press. https://github.com/probml/pml-book — 免費教科書；把平均場變分推論介紹為標準的近似推論方法。
