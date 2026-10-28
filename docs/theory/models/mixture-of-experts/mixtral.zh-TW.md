---
translation_reviewed: 2026-10-28
---

# Mixtral 8x7B

Mixtral 8x7B 是一個開放權重的稀疏 Transformer，每一層有八個前饋專家，以及一個為每個詞元選出其中兩個的路由器。Jiang 等人（2024）報告，每個詞元可以取用 470 億個參數，但推論時只使用其中 130 億。上層概述見[混合專家](index.md)。

## 概述

Mixtral 把稀疏的想法應用到現代的僅解碼器 Transformer。模型保有比它大得多的稠密模型的總容量，而每個詞元的運算量接近一個 130 億參數模型。

## 問題

700 億參數的稠密語言模型在推論時成本很高。問題在於，一個總容量相近的稀疏模型，能否在每個詞元只啟動一小部分參數的情況下，達到相當的表現。

## 核心想法

在每一層，路由器為目前的詞元對八個專家評分，並把它送到分數最高的兩個專家。它們的輸出以路由器正規化後的權重合併。由於選擇是逐詞元、逐層進行的，不同詞元可以使用不同的專家。

## 演算法

對於某詞元的隱藏狀態 \(h\)，路由器對八個專家計算分數，選出前兩名，並回傳它們前饋輸出的加權和。在這個設計中只有前饋區塊是稀疏的，注意力層是一般的稠密層。每一層都套用同樣的 top-2 路由。

## 主要結果

摘要報告，每個詞元可以使用 470 億參數，但推論時只使用 130 億。它表示該模型在所有評估的基準上，表現優於或相當於 Llama 2 70B 與 GPT-3.5。摘要以文字描述比較，因此本頁不引用個別的基準分數。

## 限制

- 總參數量仍需儲存，因此記憶體需求與大得多的模型相當，即使運算量較低。
- 服務此模型時，詞元需要在專家之間移動，當專家分散在多個裝置上時，會產生通訊成本。
- 結果是針對特定基準線報告的，摘要並未給出完整的訓練流程。

## 關聯

- [混合專家](index.md)是上層概述，Mixtral 的 top-2 路由與 top-1 及 top-k 設計並列於其中。
- [Switch Transformer](switch-transformer.md)路由到一個專家，Mixtral 則路由到兩個。
- [稀疏閘控 MoE](sparsely-gated.md)提出了 Mixtral 所用的 top-k 閘控。
- [大型語言模型](../llm/index.md)是 Mixtral 所處的脈絡，它是最知名的開放權重範例之一。

## 應用

- 部署開放權重的大型模型，使每個詞元的運算量接近較小模型。

## 開放問題

- Mixtral 的品質有多少來自稀疏設計，又有多少來自訓練資料與流程？
- 專家的專業化模式如何隨專家數與 top-k 的選擇而改變？

## 參考文獻

### 開創性論文

- Jiang, A. Q., Sablayrolles, A., Roux, A., 等人（2024）。*Mixtral of Experts*。arXiv。https://arxiv.org/abs/2401.04088 — 具八個專家、每個詞元啟動兩個、總參數 470 億的開放權重稀疏 Transformer。
- Shazeer, N., 等人（2017）。*Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer*。arXiv。https://arxiv.org/abs/1701.06538 — Mixtral 每一層所用的稀疏 top-k 閘控。
- Fedus, W., Zoph, B. & Shazeer, N.（2021）。*Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity*。arXiv。https://arxiv.org/abs/2101.03961 — Top-1 路由，用於與 Mixtral 的 top-2 作比較。
- Lepikhin, D., 等人（2020）。*GShard: Scaling Giant Models with Conditional Computation and Automatic Sharding*。arXiv。https://arxiv.org/abs/2006.16668 — 大規模稀疏 Transformer 專家，並有自動分片。
- Jacobs, R. A., Jordan, M. I., Nowlan, S. J. & Hinton, G. E.（1991）。Adaptive Mixtures of Local Experts。*Neural Computation*，3(1)，79–87。https://doi.org/10.1162/neco.1991.3.1.79 — 原始的混合專家模型。

### 綜述與教科書

- Fedus, W., Dean, J. & Zoph, B.（2022）。*A Review of Sparse Expert Models in Deep Learning*。arXiv。https://arxiv.org/abs/2209.01667 — 稀疏專家模型及其常用演算法的綜述。
