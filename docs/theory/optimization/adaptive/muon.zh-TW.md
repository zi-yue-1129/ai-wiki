---
translation_reviewed: 2026-10-28
---

# Muon

Muon 以正交化後的動量來更新每個權重矩陣，使更新在矩陣的各個方向上大小相等。正交化以少數幾次 Newton–Schulz 迭代近似計算。Liu 等人（2025）顯示它能擴展到大型語言模型，並報告其運算效率約為 AdamW 的兩倍。上層概述見[自適應方法](index.md)。

## 概述

Muon 適用於矩陣形狀的參數，例如線性層與注意力層的權重矩陣。它是一種動量方法，其更新方向被改為正交，從而移除已經佔主導的更新方向。

## 問題

對權重矩陣的動量更新，常由少數奇異方向主導，因此大部分步長都花在這些方向上。問題在於，讓更新的奇異值相等，是否能提高訓練效率。

## 核心想法

照常計算動量，再把動量矩陣換成它的正交因子，也就是由其奇異值分解 \(M = U\Sigma V^\top\) 得出的 \(UV^\top\)。如此一來，更新的所有奇異值都等於一，每個方向得到相等的權重。

## 演算法

對權重矩陣 \(W\)，其梯度為 \(G_t\)，保留動量 \(M_t = \mu M_{t-1} + G_t\)。正交因子 \(O_t\) 以 Newton–Schulz 迭代計算，這不需要顯式的奇異值分解。Liu 等人（2025）使用五次迭代，從 \(M_t / \|M_t\|_F\) 出發，採用固定的多項式係數，並將 Nesterov 式的動量餵入迭代。

有兩項改動讓 Muon 能用於大規模。更新加上與 AdamW 相同的解耦權重衰減。更新也被重新縮放，使其均方根與典型的 AdamW 更新相符，因此 Muon 可以沿用 AdamW 的學習率與權重衰減。對形狀為 \(A \times B\) 的權重矩陣、權重衰減為 \(\lambda\)，論文的最終規則為

\[
W_t = W_{t-1} - \eta_t\big(0.2\, O_t \sqrt{\max(A, B)} + \lambda W_{t-1}\big).
\]

論文預訓練時的權重衰減為 0.1。

## 主要結果

摘要報告，在計算最優的訓練下，Muon 的運算效率約為 AdamW 的 2 倍，依據的是縮放定律實驗。作者也提出 Moonlight，一個以 Muon 在 5.7 兆個詞元上訓練的 3B/16B 參數混合專家模型，他們報告其以更少的訓練 FLOPs 達到比既有模型更好的表現。

## 限制

- 正交化只適用於矩陣參數。其他參數，例如向量與嵌入，需要另一種最佳化器或規則。
- Newton–Schulz 迭代每步都增加運算量，必須由效率增益來抵消。
- 效率數字是針對語言模型的計算最優訓練報告的，因此不會自動轉移到其他任務。

## 關聯

- [自適應方法](index.md)是上層概述，Muon 與 Adam、Lion 及省記憶體的變體並列於其中。
- [Shampoo](../shampoo.md)與 [SOAP](soap.md)同樣使用矩陣結構，但是透過預條件子，而非正交化。
- [Adam](adam.md)是效率比較的基準。
- [Transformer](../../models/transformer/index.md)是 Muon 所針對的矩陣參數最常見的架構。

## 應用

- 預訓練大型語言模型，包括稀疏的混合專家模型。

## 開放問題

- 哪些參數應該正交化？其餘參數應如何處理？
- Newton–Schulz 迭代的成本，如何隨矩陣大小與模型規模變化？

## 參考文獻

### 開創性論文

- Liu, J., Su, J., Yao, X., 等人（2025）。*Muon is Scalable for LLM Training*。arXiv。https://arxiv.org/abs/2502.16982 — 顯示加上權重衰減與更新尺度調整後，Muon 可擴展到大型語言模型，並報告相對 AdamW 約 2 倍的運算效率。
- Gupta, V., Koren, T. & Singer, Y.（2018）。*Shampoo: Preconditioned Stochastic Tensor Optimization*。ICML 2018，PMLR 80。https://proceedings.mlr.press/v80/gupta18a.html — 針對同一類參數的矩陣結構方法。查核：PMLR 條目的標題與作者相符；arXiv 1802.09568 亦相符。
- Vyas, N., 等人（2024）。*SOAP: Improving and Stabilizing Shampoo using Adam*。arXiv。https://arxiv.org/abs/2409.11321 — 另一種矩陣結構方法，與 Muon 的正交化作比較。
- Kingma, D. P. & Ba, J.（2015）。*Adam: A Method for Stochastic Optimization*。ICLR。https://arxiv.org/abs/1412.6980 — 效率比較的基準。

### 綜述與教科書

- Bottou, L., Curtis, F. E. & Nocedal, J.（2018）。*Optimization Methods for Large-Scale Machine Learning*。SIAM Review。https://arxiv.org/abs/1606.04838 — 隨機方法及其在大規模訓練中取捨的綜述。
