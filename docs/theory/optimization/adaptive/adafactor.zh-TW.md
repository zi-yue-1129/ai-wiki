---
translation_reviewed: 2026-10-28
---

# Adafactor

Adafactor 是一種以因式分解形式保存二階矩估計的自適應最佳化器。對於權重矩陣，它只保留平方梯度平均的列和與行和，而不是每個參數一個值。Shazeer 與 Stern（2018）提出它，用於在最佳化器狀態過大而無法完整保存時訓練大型模型。上層概述見[自適應方法](index.md)。

## 概述

Adam 對每個參數保存兩個狀態值，即一階矩與二階矩。對大型模型而言，這些狀態可能與模型本身一樣大。Adafactor 把二階矩部分從完整矩陣縮減為一個列向量與一個行向量，並且還可以捨棄一階矩。

## 問題

每個參數的二階矩所用的記憶體，等於參數的數量。對於極大的模型，這可能超過加速器能同時容納權重與啟動值的量，因而迫使使用較小的模型或批次。

## 核心想法

對於矩陣參數 \(W \in \mathbb{R}^{n \times m}\)，平方梯度的二階矩 \(V\) 以秩一分解近似，其由列和 \(R\) 與行和 \(C\) 建構：

\[
\hat V_{ij} \approx \frac{R_i\, C_j}{\sum_k R_k}.
\]

因此只需儲存 \(n + m\) 個值，而非 \(n m\) 個。向量參數（如偏置）仍保留完整的二階矩，因為這種分解不適用於向量。

## 演算法

每一步以指數平均更新平方梯度的列和與行和，形成因式分解後的估計 \(\hat V\)，再把梯度以 \(1/\sqrt{\hat V}\) 縮放。論文還使用更新裁剪規則與相對步長，本頁不完整重現。

## 主要結果

摘要報告，在捨棄動量的情況下，此方法在 Transformer 的 WMT 2014 英德翻譯任務上，結果與已發表的 Adam 設定相當。摘要也描述其輔助儲存非常少。本頁不引用更具體的數字。

## 限制

- 秩一分解是近似，因此逐參數的縮放比 Adam 不精確。
- 向量參數仍保留完整的二階矩，因此節省主要適用於矩陣。
- 此方法有數項設計選擇，例如裁剪與步長排程，會改變行為，需要謹慎設定。

## 關聯

- [自適應方法](index.md)是上層概述，Adafactor 與 Adam 及其他變體並列於其中。
- [Adam](adam.md)是 Adafactor 在記憶體上所近似的完整狀態方法。
- [AdaGrad](adagrad.md)是較早的逐座標方法，Adafactor 同樣縮減其累加器。
- [Shampoo](../shampoo.md)以矩陣統計量縮放更新，但記憶體成本較高。

## 應用

- 預訓練大型 Transformer 模型，此時最佳化器的記憶體限制了批次大小或模型大小。

## 開放問題

- 在極大規模下，分解會損失多少準確率，與完整二階矩相比？
- 能否讓分解更貼近注意力與前饋層的矩陣結構？

## 參考文獻

### 開創性論文

- Shazeer, N. & Stern, M.（2018）。*Adafactor: Adaptive Learning Rates with Sublinear Memory Cost*。ICML 2018，PMLR 80，頁 4596–4604。https://proceedings.mlr.press/v80/shazeer18a.html — 把矩陣參數的二階矩估計分解為列和與行和，使記憶體相對於參數數量為次線性。
- Kingma, D. P. & Ba, J.（2015）。*Adam: A Method for Stochastic Optimization*。ICLR。https://arxiv.org/abs/1412.6980 — Adafactor 在記憶體上近似的完整二階矩方法。
- Chen, X., 等人（2023）。*Symbolic Discovery of Optimization Algorithms*。arXiv。https://arxiv.org/abs/2302.06675 — Lion，另一種以記憶體使用為動機的最佳化器，與 Adafactor 的節省作比較。
- Duchi, J., Hazan, E. & Singer, Y.（2011）。Adaptive Subgradient Methods for Online Learning and Stochastic Optimization。*Journal of Machine Learning Research*，12，2121–2159。https://jmlr.org/papers/v12/duchi11a.html — Adafactor 的分解估計所推廣的累積逐座標累加器。

### 綜述與教科書

- Bottou, L., Curtis, F. E. & Nocedal, J.（2018）。*Optimization Methods for Large-Scale Machine Learning*。SIAM Review。https://arxiv.org/abs/1606.04838 — 自適應隨機方法及其在大規模訓練中取捨的綜述。
