---
translation_reviewed: 2026-10-28
---

# 大批次與分散式最佳化

批次大小與平行化會改變最佳化器的行為。較大的批次給出雜訊較少的梯度，也讓更多硬體同時運作，但超過某個點後，多出來的樣本不再減少所需的步數。本子章討論這種情況何時出現，以及為何極大批次需要逐層縮放與較長的預熱。

## 概述

本子章屬於[最佳化](index.md)資料夾。每種方法都有獨立的頁面，本頁負責比較它們，並說明各自適用的情境。同一問題的學習率面向見[學習率排程](learning-rate-schedules.md)。

## 核心概念

- **批次大小 \(B\)**：一次梯度估計所用的樣本數。\(B\) 越大，梯度雜訊越低，每一步可平行的工作也越多。
- **資料平行**：每個裝置在批次的一部分上計算梯度，然後把梯度平均。有效批次大小是所有裝置的總和。
- **梯度雜訊尺度**：梯度相對於其真值的雜訊程度的統計量。McCandlish 等人（2018）指出，它能預測仍能減少步數的最大批次大小。其定義見 [SGD 雜訊尺度](sgd-noise-scale.md)頁。
- **泛化差距**：以大批次、與小批次相同的排程訓練時，測試準確率的下降。

## 運作方式

批次大小為 \(B\) 時，每一步使用 \(B\) 個樣本。低於臨界批次大小時，把 \(B\) 加倍大致會使所需步數減半，因此多出來的硬體得到有效運用。高於它之後，多出來的樣本幫助變小，步數也不再下降。McCandlish 等人把這個門檻與梯度雜訊尺度連結起來。

實務上有兩個問題。第一是最佳化問題：學習率固定時，極大批次可能使訓練初期不穩定，因此會使用線性學習率縮放與預熱。第二是泛化問題。Hoffer 等人（2017）把大部分差距歸因於更新次數較少，而非批次本身，並顯示調整訓練方式就能消除這個差距。

Shallue 等人（2019）在數種批次大小與工作負載下，量測達到目標誤差所需的步數。他們報告，文獻中關於批次大小的許多分歧能被解釋，並且沒有證據顯示較大的批次會使樣本外表現變差。

## 關鍵方法

下列每個方法各有獨立頁面。本表進行比較。

| 方法 | 處理的問題 | 子頁 |
|---|---|---|
| 線性縮放加預熱（Goyal 等人，2017） | 隨著 \(B\) 增加，維持訓練初期的穩定 | [漸進式預熱](gradual-warm-up.md) |
| 梯度雜訊尺度（McCandlish 等人，2018） | 預測有用的批次大小 | [SGD 雜訊尺度](sgd-noise-scale.md) |
| LARS（You 等人，2017） | 極大 \(B\) 時的逐層步長，適用於 SGD 類更新 | [LARS](lars.md) |
| LAMB（You 等人，2019） | 把逐層縮放用於 Adam 類更新 | [LAMB](lamb.md) |

## 關聯

- [梯度裁剪與正規化更新](gradient-clipping-and-normalisation.md)是上層概述，LARS 與 LAMB 與範數裁剪並列於其中。
- [學習率排程](learning-rate-schedules.md)涵蓋大批次訓練所依賴的預熱與衰減。
- [尖銳極小值](sharp-minima.md)是對泛化差距的一種解釋。
- [Adam](adaptive/adam.md)提供 LAMB 逐層縮放的逐座標更新。
- [聯邦學習](../paradigms/federated/index.md)是另一種把運算分散到多個裝置的設定，但對通訊與資料有不同的限制。

## 應用

- 以 LAMB 或 LARS 加上預熱，在許多加速器上預訓練大型語言與視覺模型。
- 如 Goyal 等人（2017）所述，以大批次在約一小時內訓練 ImageNet 上的 ResNet-50。
- 如 You 等人（2019）所述，以極大批次訓練 BERT。

## 開放問題

- 除了梯度雜訊尺度之外，還有什麼決定臨界批次大小？能否在訓練開始前估計？
- 在各種架構中，若更新次數相同，泛化差距是否就會消失？某些模型是否需要更多更新？

## 參考文獻

### 開創性論文

- McCandlish, S., Kaplan, J., Amodei, D. & OpenAI Dota Team（2018）。*An Empirical Model of Large-Batch Training*。arXiv。https://arxiv.org/abs/1812.06162 — 顯示梯度雜訊尺度能預測多個領域中有用的最大批次大小。
- Shallue, C. J., 等人（2019）。*Measuring the Effects of Data Parallelism on Neural Network Training*。arXiv。https://arxiv.org/abs/1811.03600 — 在多種批次大小與工作負載下量測達到目標誤差所需的步數，並未發現較大批次會降低樣本外表現的證據。
- Hoffer, E., Hubara, I. & Soudry, D.（2017）。*Train longer, generalize better: closing the generalization gap in large batch training of neural networks*。arXiv。https://arxiv.org/abs/1705.08741 — 把大批次的泛化差距歸因於更新次數較少，並顯示調整訓練方式即可消除它。
- Goyal, P., 等人（2017）。*Accurate, Large Minibatch SGD: Training ImageNet in 1 Hour*。arXiv。https://arxiv.org/abs/1706.02677 — 線性學習率縮放加預熱，使大批次訓練保持穩定。
- You, Y., Gitman, I. & Ginsburg, B.（2017）。*Large Batch Training of Convolutional Networks*。arXiv。https://arxiv.org/abs/1708.03888 — 提出 LARS，為大批次下的 SGD 類更新提供逐層步長。
- You, Y., 等人（2019）。*Large Batch Optimization for Deep Learning: Training BERT in 76 Minutes*。ICLR。https://arxiv.org/abs/1904.00962 — 提出 LAMB，把逐層信任比延伸到 Adam。

### 綜述與教科書

- Bottou, L., Curtis, F. E. & Nocedal, J.（2018）。*Optimization Methods for Large-Scale Machine Learning*。SIAM Review。https://arxiv.org/abs/1606.04838 — 隨機梯度方法的綜述，討論批次大小與步長的選擇。
