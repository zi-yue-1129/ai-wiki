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

對權重矩陣 \(W\)，其梯度為 \(G_t\)，先更新動量 \(M_t = \mu M_{t-1} + G_t\)。接著以少數幾次 Newton–Schulz 迭代近似地正交化 \(M_t\)，這種做法不需要顯式的奇異值分解，然後套用 \(W_{t+1} = W_t - \eta\,\mathrm{Orth}(M_t)\)。Liu 等人（2025）報告，要讓 Muon 能擴展，需要兩個要素：權重衰減，以及對各參數更新尺度的仔細調整。

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
- Gupta, V., Koren, T. & Singer, Y.（2018）。*Shampoo: Preconditioned Stochastic Tensor Optimization*。ICML。https://arxiv.org/abs/1802.09568 — 針對同一類參數的矩陣結構方法。
- Vyas, N., 等人（2024）。*SOAP: Improving and Stabilizing Shampoo using Adam*。arXiv。https://arxiv.org/abs/2409.11321 — 另一種矩陣結構方法，與 Muon 的正交化作比較。
- Kingma, D. P. & Ba, J.（2015）。*Adam: A Method for Stochastic Optimization*。ICLR。https://arxiv.org/abs/1412.6980 — 效率比較的基準。

### 綜述與教科書

- Bottou, L., Curtis, F. E. & Nocedal, J.（2018）。*Optimization Methods for Large-Scale Machine Learning*。SIAM Review。https://arxiv.org/abs/1606.04838 — 隨機方法及其在大規模訓練中取捨的綜述。
