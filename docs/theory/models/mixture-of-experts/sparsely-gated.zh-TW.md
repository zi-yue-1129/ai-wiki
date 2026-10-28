---
translation_reviewed: 2026-10-28
---

# 稀疏閘控混合專家

Shazeer 等人（2017）提出稀疏閘控混合專家層，其中包含多達數千個專家網路，由一個可訓練的閘控網路為每個樣本只選出少數幾個。他們把它以卷積方式應用在堆疊的 LSTM 層之間，該層的參數量最多達 1,370 億。上層概述見[混合專家](index.md)。

## 概述

論文顯示，條件運算（每個樣本只使用網路的一部分）能大幅提高模型容量。其閘控設計成為後來稀疏 Transformer 所依循的範本。

## 問題

模型品質通常隨參數數量提高，但運算與記憶體也隨之增加，因為每個參數都要用於每個樣本。因此稠密模型限制了容量。問題在於，一個層能否持有大量參數，同時對每個輸入只使用其中的一小部分。

## 核心想法

以一組專家加上一個閘控網路取代稠密層。閘控對每個專家輸出一個分數，只保留最大的幾個，並以閘控值為權重，把這些專家的輸出加總。未被選中的專家對該樣本不做任何工作。

## 演算法

對於輸入 \(x\)，該層計算

\[
y = \sum_{i \in \mathrm{TopK}(G(x))} G(x)_i\, E_i(x),
\]

其中 \(E_i\) 是第 \(i\) 個專家，\(G(x)\) 是閘控的輸出向量，前 \(k\) 名以外的分量設為零。閘控與專家以梯度下降共同訓練，而閘控的稀疏性使該層的成本接近一個小網路。

## 主要結果

摘要報告，混合專家的參數量最多達 1,370 億，應用在堆疊的 LSTM 層之間。它宣稱模型容量提高超過一千倍，而運算效率只有輕微損失，並且這些模型以較低的運算成本取得顯著優於當時最先進方法的結果。摘要未給出具體的困惑度或 BLEU 分數，因此本頁不引用任何數字。

## 限制

- 專家的使用可能不均勻，閘控偏好其中少數幾個。需要平衡項來避免這種情況。
- 專家必須分散在多個裝置上，因此該層依賴裝置間的通訊，這在實務上限制了擴展。
- 效果是以 LSTM 為基礎的語言與翻譯模型展示的，移植到 Transformer 是之後以其他設計完成的。

## 關聯

- [混合專家](index.md)是上層概述，本論文的閘控設計與原始的自適應混合及後來的路由變體並列於其中。
- [Switch Transformer](switch-transformer.md)把這個閘控簡化為每個詞元一個專家。
- [Mixtral](mixtral.md)在 Transformer 中使用 top-2 閘控。
- [Transformer](../transformer/index.md)是後來採用此層的架構。

## 應用

- 在稠密網路無法以同樣成本達到的規模上，進行語言建模與翻譯。

## 開放問題

- 哪些平衡項能讓專家獲得最多的專業化，同時避免閒置容量？
- 在大規模下，top-k 的選擇如何在品質與通訊成本之間取捨？

## 參考文獻

### 開創性論文

- Shazeer, N., Mirhoseini, A., Maziarz, K., Davis, A., Le, Q., Hinton, G. & Dean, J.（2017）。*Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer*。arXiv。https://arxiv.org/abs/1701.06538 — 提出稀疏閘控混合專家，參數量最多達 1,370 億，且效率損失不大。
- Jacobs, R. A., Jordan, M. I., Nowlan, S. J. & Hinton, G. E.（1991）。Adaptive Mixtures of Local Experts。*Neural Computation*，3(1)，79–87。https://doi.org/10.1162/neco.1991.3.1.79 — 本層使其稀疏化的原始稠密閘控混合。
- Lepikhin, D., 等人（2020）。*GShard: Scaling Giant Models with Conditional Computation and Automatic Sharding*。arXiv。https://arxiv.org/abs/2006.16668 — 把稀疏閘控專家應用到 Transformer 翻譯，參數量超過 6,000 億。
- Fedus, W., Zoph, B. & Shazeer, N.（2021）。*Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity*。arXiv。https://arxiv.org/abs/2101.03961 — 把 top-k 閘控簡化為每個詞元一個專家。
- Jiang, A. Q., 等人（2024）。*Mixtral of Experts*。arXiv。https://arxiv.org/abs/2401.04088 — 具八個專家、每個詞元啟動兩個的開放權重稀疏 Transformer。

### 綜述與教科書

- Fedus, W., Dean, J. & Zoph, B.（2022）。*A Review of Sparse Expert Models in Deep Learning*。arXiv。https://arxiv.org/abs/2209.01667 — 稀疏專家模型及其常用演算法的綜述。
