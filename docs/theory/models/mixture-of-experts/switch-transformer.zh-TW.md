---
translation_reviewed: 2026-10-28
---

# Switch Transformer

Switch Transformer 把每個詞元路由到單一專家，而不是多個專家。Fedus、Zoph 與 Shazeer（2021）顯示，這種更簡單的路由能讓每個詞元的運算量保持不變，同時參數量成長到兆級規模，並報告相對稠密 T5 模型有大幅的預訓練加速。上層概述見[混合專家](index.md)。

## 概述

早期的稀疏層使用 top-k 閘控，k 為二或更大，這會增加每個詞元的運算量，並使路由變得複雜。Switch 保留稀疏的想法，並把 k 降為一。作者把這種做法稱為 Switch 層。

## 問題

k 為二或更大的 top-k 路由，會使每個詞元的運算量倍增，並在通訊與批次處理上增加複雜度。問題在於，單一專家的選擇是否已足以獲得稀疏性的容量好處，而不承擔其成本。

## 核心想法

對每個詞元，路由器產生一組專家上的機率，並只把詞元送到機率最高的專家。該專家的輸出以此機率縮放，因此路由器仍然能接收到梯度訊號。於是每個詞元只使用一個專家的參數，運算量與同樣大小的稠密層相同。

## 演算法

對於詞元表示 \(x\) 與路由器權重矩陣 \(W_r\)，路由器計算 \(p = \mathrm{softmax}(W_r x)\)，選擇 \(i = \arg\max_j p_j\)，並輸出 \(p_i\, E_i(x)\)。論文使用負載平衡損失來鼓勵路由器把詞元分散到各專家，並設有每個專家的容量上限。

## 主要結果

摘要報告，稀疏模型可達兆參數規模，並在相同的運算資源下，相對 T5-Base 與 T5-Large 達到最多 7 倍的預訓練速度提升。兆參數模型相對 T5-XXL 達到 4 倍加速。摘要也指出，大型稀疏模型首次可以用較低精度的 bfloat16 格式訓練。

## 限制

- Top-1 的選擇是離散的，因此路由器的決定不可微，梯度只能透過所選機率的縮放回傳給它。
- 每個詞元在每一層只看到一個專家，這可能限制該層結合多位專家知識的能力。
- 即使運算量不增加，參數記憶體仍會隨專家數增加。

## 關聯

- [混合專家](index.md)是上層概述，這種單一專家路由與 top-k 設計並列於其中。
- [稀疏閘控 MoE](sparsely-gated.md)使用本論文所簡化的 top-k 閘控。
- [Mixtral](mixtral.md)使用 top-2 路由，而非 top-1。
- [Transformer](../transformer/index.md)是前饋區塊所屬的架構。

## 應用

- 在每個詞元的運算量必須固定的情況下，預訓練極大的語言模型。
- 大規模多語言預訓練，本論文的加速效益最明顯。

## 開放問題

- Top-1 的選擇是否會在需要多位專家同時參與的任務上限制品質？在相同運算量下，它與 top-2 相比如何？
- 容量上限應如何設定，才不會因丟棄的詞元而損害訓練？

## 參考文獻

### 開創性論文

- Fedus, W., Zoph, B. & Shazeer, N.（2021）。*Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity*。arXiv。https://arxiv.org/abs/2101.03961 — 把每個詞元路由到單一專家，並報告在每個詞元運算量固定時，預訓練速度最多提升 7 倍。
- Shazeer, N., 等人（2017）。*Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer*。arXiv。https://arxiv.org/abs/1701.06538 — 本論文所簡化的 top-k 稀疏閘控。
- Jacobs, R. A., Jordan, M. I., Nowlan, S. J. & Hinton, G. E.（1991）。Adaptive Mixtures of Local Experts。*Neural Computation*，3(1)，79–87。https://doi.org/10.1162/neco.1991.3.1.79 — 原始的混合專家模型，具稠密閘控網路。
- Lepikhin, D., 等人（2020）。*GShard: Scaling Giant Models with Conditional Computation and Automatic Sharding*。arXiv。https://arxiv.org/abs/2006.16668 — 在 Transformer 規模下的稀疏專家與自動分片，Switch 較簡單的路由也以此設定為目標。
- Jiang, A. Q., 等人（2024）。*Mixtral of Experts*。arXiv。https://arxiv.org/abs/2401.04088 — 之後使用 top-2 路由的稀疏 Transformer，用於比較。

### 綜述與教科書

- Fedus, W., Dean, J. & Zoph, B.（2022）。*A Review of Sparse Expert Models in Deep Learning*。arXiv。https://arxiv.org/abs/2209.01667 — 稀疏專家模型及其常用演算法的綜述。
