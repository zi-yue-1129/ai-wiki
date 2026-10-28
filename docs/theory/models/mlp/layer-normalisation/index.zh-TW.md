---
related:
- theory/models/mlp
- theory/models/transformer
aliases:
  - Layer Normalisation
  - LayerNorm
  - 層正規化
tags:
  - normalisation
  - feedforward networks
  - sequence models
translation_reviewed: 2026-10-28
---

# 層正規化

層正規化是一種方法，對一個隱藏層的所有單元，針對單一訓練樣本一次一筆地做正規化，並對各個輸入加總後的值進行處理。Ba、Kiros 與 Hinton 在 2016 年的論文「Layer Normalization」中提出了它。由於它不依賴批次統計，因此適合序列模型。

## 問題

批次正規化的效益取決於小批次的大小。它如何應用於循環網路並不清楚，而且無法用於線上學習。

## 核心想法

對單一訓練樣本，在一層的所有隱藏單元上做正規化，然後為每個單元提供各自學習的增益與偏置。訓練與測試時使用相同的計算，因此一個輸入的結果不依賴批次中的其他樣本。

## 方程式或演算法

設有 \(H\) 個隱藏單元，其加總輸入為 \(a_i\)，該層在這些單元上計算平均值與標準差：

\[
\mu = \frac{1}{H}\sum_{i=1}^{H} a_i, \qquad
\sigma = \sqrt{\frac{1}{H}\sum_{i=1}^{H}(a_i - \mu)^2}.
\]

接著，每個單元的正規化激活值以其增益做縮放，並以其偏置做平移。

## 結果

在 MSCOCO 的順序嵌入（order embeddings）上，描述文字檢索的 R@1 從 46.6 提升到 48.5，影像檢索的 R@1 從 37.8 提升到 38.9。該模型在基準模型訓練時間的 60% 內達到最佳驗證結果。在使用 DRAW 的二值化 MNIST 上，經層正規化的模型在 200 個 epoch 後達到 82.09 nats，基準模型為 82.36。

## 限制

與批次正規化不同，層正規化對個別權重向量的重新縮放不具不變性。在 ConvNet 中，批次正規化表現較好，作者表示「需要進一步研究，才能讓 layer normalization 在 ConvNet 中運作良好」。

## 相關連結

[MLP](../index.md) 家族頁面將它與適合 [CNN](../../cnn/index.md) 的批次正規化做了對比。它也是與 [Transformer](../../transformer/index.md) 家族一同討論的正規化層，而 [高斯誤差線性單元](../gelu/index.md) 中介紹的激活函數出現在同樣的前饋區塊中。對於批次正規化難以應用的循環網路，見 [RNN](../../rnn/index.md) 家族頁面。

## 未解問題與更多變體

- **卷積網路。** 要讓層正規化在 ConvNet 中運作良好，仍需進一步研究；在論文的比較中，批次正規化在 ConvNet 的表現較好。
- **序列與線上設定。** 它不依賴批次大小，適合序列模型與線上學習。這項優勢在多大程度上適用於各種任務，仍待進一步研究。
- **重新縮放的不變性。** 缺乏對個別權重向量重新縮放的不變性，對某些架構可能有影響，對其他架構則未必，因此需要針對每個模型加以檢驗。

## 參考文獻

### 開創性論文

- Ba, J. L., Kiros, J. R. & Hinton, G. E. (2016). "Layer Normalization". [arXiv:1607.06450](https://arxiv.org/abs/1607.06450) — 在特徵上而非批次上做正規化。
- Ioffe, S. & Szegedy, C. (2015). "Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift". [arXiv:1502.03167](https://arxiv.org/abs/1502.03167) — 對每個小批次的激活值做正規化，層正規化即是為了替代它而提出的方法。
- He, K., et al. (2015). "Deep Residual Learning for Image Recognition". [arXiv:1512.03385](https://arxiv.org/abs/1512.03385) — 殘差連接，使深層網路能夠訓練。

### 綜述與教科書

- Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep Learning*. MIT Press. https://www.deeplearningbook.org/ — 第 6 章涵蓋前饋網路、激活函數與通用逼近結果。

### 講座與影片

（本頁尚未核對）

### 文章與文件

- Hendrycks, D. & Gimpel, K. (2016). "Gaussian Error Linear Units (GELUs)". [arXiv:1606.08415](https://arxiv.org/abs/1606.08415) — GELU 激活函數，被許多 Transformer 模型採用。
