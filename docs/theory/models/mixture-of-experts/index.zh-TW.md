---
translation_reviewed: 2026-10-28
---

# 混合專家

混合專家（MoE）層包含許多子網路（稱為專家），以及一個很小、可訓練的路由器，它只把每個輸入送到其中少數幾個專家。因此模型的總參數量可以很大，而每個輸入所花費的運算量仍然適中。這個想法可追溯到 1990 年代初的自適應混合模型，在稀疏路由被擴展之後，才成為大型語言模型的核心。

## 概述

MoE 是建構一個層的方式，而不是獨立的模型家族。它最常用於 [Transformer](../transformer/index.md) 內，取代前饋區塊。下列每個方法頁說明一種有影響力的設計。

## 核心概念

- **專家**：一般的前饋網路，是該層中數個網路之一。
- **路由器（閘道）**：可訓練的網路，為每個輸入對各專家評分。它的輸出決定哪些專家會執行。
- **稀疏啟動**：只有分數最高的少數專家（通常一或兩個）處理每個詞元，因此對任何一個輸入，大部分參數都是閒置的。
- **容量**：限制一個批次中專家能處理的詞元數，以維持各專家之間的工作量平衡。
- **負載平衡**：路由器把大多數輸入送到少數專家，使其他專家閒置的問題。訓練通常會加入項來避免。

## 運作方式

對於輸入 \(x\)，路由器為每個專家計算分數，保留前 \(k\) 名，並以正規化權重合併它們的輸出。只有被選中的專家會被計算，因此每個輸入的運算量取決於 \(k\)，而非專家總數。路由器與專家一起訓練，通常透過其所選權重的梯度下降。

稀疏路由在實務上使層難以擴展。專家必須分散在不同的加速器上，而每一步都要把詞元送到正確的專家再送回來，這是一種全對全（all-to-all）的通訊模式。因此 MoE 的代價有一部分落在記憶體與通訊上，而非算術，這也是硬體與互連設計對它很重要的原因。

![稀疏混合專家路由示意：一個詞元經路由器選取四名專家中的兩名，最後合併所選專家的輸出。](../../../assets/concept-animations/moe-sparse-routing.svg)

*原創稀疏路由概念圖，CC BY-SA 4.0。* 此單一詞元的 **top-2** 示意只啟動 E2 與 E3；其他專家不處理這個詞元。被選中專家的輸出需依**路由權重加權合併**（圖中以加總符號簡化）。虛線代表未選取的候選連線，**不是實際派送的詞元**。專家數量、連線及顏色均為教學示意，不是量測所得的路由機率或模型啟動值；路由器通常會對每個詞元分別評分。參見 [Shazeer 等人（2017）](https://arxiv.org/abs/1701.06538) 與 [Jiang 等人（2024）](https://arxiv.org/abs/2401.04088)。

## 關鍵方法

| 方法 | 貢獻 | 路由方式 | 頁面 |
|---|---|---|---|
| 自適應局部專家混合（Jacobs 等人，1991） | 含閘控網路的原始混合模型 | 對所有專家做軟權重 | 本頁 |
| 稀疏閘控 MoE（Shazeer 等人，2017） | 在極大規模下使用稀疏 top-k 閘控 | Top-k | [稀疏閘控 MoE](sparsely-gated.md) |
| Switch Transformer（Fedus 等人，2021） | 把每個詞元路由到單一專家 | Top-1 | [Switch Transformer](switch-transformer.md) |
| Mixtral 8x7B（Jiang 等人，2024） | 具八個專家的開放權重稀疏 Transformer | Top-2 | [Mixtral](mixtral.md) |

## 關聯

- [Transformer](../transformer/index.md)是 MoE 通常取代前饋區塊的架構。
- [大型語言模型](../llm/index.md)是 MoE 使用最多的地方，因為它增加參數，卻不增加每個詞元的運算量。
- [模型壓縮](../../model-compression/index.md)的目標相反，是使用較少的參數；但稀疏專家與壓縮模型都有「不是每個輸入都用到所有權重」的想法。
- [互連](../../../engineering/hardware/interconnects/index.md)說明為何專家路由的全對全流量會限制擴展。

## 應用

- 開放權重語言模型，結合大的總參數量與每個詞元較小的啟動參數量。
- 多語言機器翻譯，GShard 以稀疏專家擴展到超過 6,000 億參數。

## 開放問題

- 路由器應如何訓練，才能讓專家專業化，同時避免有專家閒置？
- 當啟動的專家數相對於總數很少時，MoE 的效益有多少能保留？

## 參考文獻

### 開創性論文

- Jacobs, R. A., Jordan, M. I., Nowlan, S. J. & Hinton, G. E.（1991）。Adaptive Mixtures of Local Experts。*Neural Computation*，3(1)，79–87。https://doi.org/10.1162/neco.1991.3.1.79 — 原始的混合專家模型，由閘控網路為一組局部專家加權。
- Shazeer, N., 等人（2017）。*Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer*。arXiv。https://arxiv.org/abs/1701.06538 — 稀疏 top-k 閘控，把一個層擴展到數十億參數，且效率損失不大。
- Lepikhin, D., 等人（2020）。*GShard: Scaling Giant Models with Conditional Computation and Automatic Sharding*。arXiv。https://arxiv.org/abs/2006.16668 — 以自動分片把稀疏 Transformer 翻譯模型擴展到超過 6,000 億參數。
- Fedus, W., Zoph, B. & Shazeer, N.（2021）。*Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity*。arXiv。https://arxiv.org/abs/2101.03961 — 把路由簡化為每個詞元一個專家，並報告預訓練速度的大幅提升。
- Jiang, A. Q., 等人（2024）。*Mixtral of Experts*。arXiv。https://arxiv.org/abs/2401.04088 — 具八個專家、每個詞元啟動兩個的開放權重稀疏模型。

### 綜述與教科書

- Fedus, W., Dean, J. & Zoph, B.（2022）。*A Review of Sparse Expert Models in Deep Learning*。arXiv。https://arxiv.org/abs/2209.01667 — 稀疏專家模型及其常用演算法的綜述。
