---
translation_reviewed: 2026-10-28
---

# Lion

Lion 是一種由程式搜尋發現的最佳化器，其更新只使用以動量為基礎之量的符號。因此每個參數在每一步的移動量都相同。它只保存一個動量緩衝，Adam 則保存兩個。Chen 等人（2023）提出此方法，報告在影像、語言與擴散任務上取得準確率與運算量的改善。上層概述見[自適應方法](index.md)。

## 概述

Lion 以符號運算取代 Adam 的逐座標縮放。這移除了二階矩狀態，並使各參數的更新大小一致，因此學習率的設定方式也隨之改變。

## 問題

Adam 的兩個狀態緩衝使最佳化器所需的記憶體加倍。對大型模型而言，這些狀態可能限制批次大小或模型大小，因此只有一個緩衝且品質相當的方法很有吸引力。

## 核心想法

以動量與目前梯度的內插量之符號來計算更新。符號使每個座標都有相同的步長，而動量緩衝則以另一個衰減率單獨更新。

## 演算法

令動量為 \(m_t\)，內插係數為 \(\beta_1\)，動量衰減為 \(\beta_2\)，更新為

\[
c_t = \beta_1 m_{t-1} + (1 - \beta_1) g_t,\qquad
\theta_{t+1} = \theta_t - \eta\,\big(\operatorname{sign}(c_t) + \lambda\theta_t\big),\qquad
m_t = \beta_2 m_{t-1} + (1 - \beta_2) g_t,
\]

其中 \(\lambda\) 為解耦的權重衰減。\(c_t\) 的符號在每個座標上為 \(\pm 1\)，因此每個座標的步長大小相同。

## 主要結果

摘要報告，Lion 把 ViT 在 ImageNet 上的準確率提高最多 2%，並在 JFT 上節省最多 5 倍的預訓練運算量。它報告擴散模型的 FID 改善，並減少最多 2.3 倍的訓練運算量；在語言任務上，其表現與 Adam 相近或更好。摘要指出，由於符號更新的範數較大，Lion 需要比 Adam 更小的學習率。

## 限制

- 符號捨棄了大小資訊，因此梯度尺度差異很大的座標在每一步中被同等對待。
- 學習率與權重衰減需要相對 Adam 重新調校，因為更新的範數不同。
- 結果涵蓋特定任務，摘要並未對所有架構作出主張。

## 關聯

- [自適應方法](index.md)是上層概述，Lion 與 Adam、AdamW 及省記憶體的變體並列於其中。
- [Adam](adam.md)是 Lion 所簡化的雙緩衝方法。
- [AdamW](adamw.md)提供 Lion 也使用的解耦權重衰減。
- [Adafactor](adafactor.md)是另一種省記憶體的方法，它是分解二階矩而非移除它。

## 應用

- 訓練視覺 Transformer 與擴散模型，論文報告有改善。
- 預訓練大型模型，此時最佳化器記憶體是瓶頸。

## 開放問題

- 符號更新為何有效？它能否推廣到所報告任務以外的情境？
- 在 Adam 與 Lion 之間切換時，學習率應如何縮放？

## 參考文獻

### 開創性論文

- Chen, X., Liang, C., Huang, D., Real, E., Wang, K., Liu, Y., Pham, H., Dong, X., Luong, T., Hsieh, C.-J., Lu, Y. & Le, Q. V.（2023）。*Symbolic Discovery of Optimization Algorithms*。arXiv。https://arxiv.org/abs/2302.06675 — 提出 Lion，一種只保存單一動量緩衝的符號式最佳化器。
- Kingma, D. P. & Ba, J.（2015）。*Adam: A Method for Stochastic Optimization*。ICLR。https://arxiv.org/abs/1412.6980 — Lion 所比較的雙緩衝方法。
- Loshchilov, I. & Hutter, F.（2017）。*Decoupled Weight Decay Regularization*。ICLR。https://arxiv.org/abs/1711.05101 — Lion 更新中所用的解耦權重衰減。
- Shazeer, N. & Stern, M.（2018）。*Adafactor: Adaptive Learning Rates with Sublinear Memory Cost*。arXiv。https://arxiv.org/abs/1804.04235 — 另一種省記憶體的自適應方法，用於比較。

### 綜述與教科書

- Bottou, L., Curtis, F. E. & Nocedal, J.（2018）。*Optimization Methods for Large-Scale Machine Learning*。SIAM Review。https://arxiv.org/abs/1606.04838 — 自適應隨機方法及其在大規模訓練中取捨的綜述。
