---
related:
- theory/models/cnn/backbones-and-scaling
- theory/models/cnn
aliases:
  - Compound Scaling
  - EfficientNet
  - 複合縮放
tags:
  - model scaling
  - efficiency
  - computer vision
translation_reviewed: 2026-10-28
---

# EfficientNet 與複合縮放

EfficientNet 是 Tan 與 Le 於 2019 年在〈EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks〉中提出的卷積網路家族。論文提出複合縮放：用同一個係數一起擴大網路的深度、寬度與輸入解析度，而不是只縮放單一維度。

## 問題

只縮放一個維度（深度、寬度或輸入解析度）帶來的增益會遞減，而且逐一手動調整多個維度既繁瑣，又常常不是最佳。

## 核心想法

用同一個係數 φ 一起縮放三個維度，使網路以固定比例成長。這些常數是在基準網路 EfficientNet-B0 上透過小型網格搜尋找到的，而 EfficientNet-B0 本身是由多目標架構搜尋產生的。

## 方程式或演算法

\[
d = \alpha^{\phi}, \qquad w = \beta^{\phi}, \qquad r = \gamma^{\phi}
\]

其中 d、w 與 r 分別縮放深度、寬度與輸入解析度。常數滿足 \(\alpha \cdot \beta^2 \cdot \gamma^2 \approx 2\)，且 \(\alpha, \beta, \gamma \geq 1\)。FLOPS 因此大約以 \(2^{\phi}\) 的速度成長。當 φ = 1 時，搜尋得到 α = 1.2、β = 1.1 與 γ = 1.15。

## 結果

- EfficientNet-B7 在 ImageNet 上達到 84.3% top-1 準確率，參數量為 66M，FLOPS 為 37B。
- 論文報告，它在推論時比 GPipe 小 8.4 倍、快 6.1 倍；GPipe 以 557M 參數達到 84.3%。

## 限制

- 直接在大型模型上搜尋常數的成本太高，因此常數只在基準網路上搜尋一次。
- 論文指出，縮放的效果「高度取決於基準網路」。
- 架構搜尋最佳化的是 FLOPS，而不是延遲。

## 相關連結

- [骨幹與縮放](../index.md)把複合縮放與殘差連接，以及後來現代化的 CNN 並列介紹。
- [Residual Networks（殘差網路）](../resnet/index.md)介紹讓極深骨幹能夠訓練的殘差連接。兩頁回答的是不同問題：如何訓練深層網路，以及如何選擇它們的大小。
- [卷積變體](../../convolution-variants/index.md)介紹深度可分離卷積，它能減少行動與嵌入式裝置上的運算量。
- [CNN](../../index.md)提供更廣的家族脈絡，包括卷積模型的取捨。
- [電腦視覺](../../../computer-vision/index.md)介紹這些骨幹所用的任務。

## 未解問題與更多變體

- **大型模型上的常數。** 直接在大型模型上搜尋常數成本太高，因此常數固定在基準網路上。它們能否遷移到其他基準網路，仍是開放問題。
- **FLOPS 與延遲。** 架構搜尋最佳化的是 FLOPS 而非延遲，因此搜尋目標與硬體上真正重要的速度可能不同。
- **訓練速度。** 同一作者的後續研究 EfficientNetV2 搜尋的模型，既更小也訓練更快（見參考文獻）。

## 參考文獻

### 開創性論文

- Tan, M. & Le, Q. V. (2019). "EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks". [arXiv:1905.11946](https://arxiv.org/abs/1905.11946) — 同時縮放深度、寬度與輸入解析度。
- Howard, A. G., et al. (2017). "MobileNets: Efficient Convolutional Neural Networks for Mobile Vision Applications". [arXiv:1704.04861](https://arxiv.org/abs/1704.04861) — 深度可分離卷積，作為高效裝置端視覺的建構單元。

### 綜述與教科書

- Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep Learning*. MIT Press. https://www.deeplearningbook.org/ — 第 9 章介紹卷積網路與卷積運算的標準說明。

### 講座與影片

（本頁尚未核對）

### 文章與文件

- Liu, Z., et al. (2022). "A ConvNet for the 2020s". [arXiv:2201.03545](https://arxiv.org/abs/2201.03545) — ConvNeXt，一個現代化的純 CNN，與 Transformer 基線相當。
- Tan, M. & Le, Q. V. (2021). "EfficientNetV2: Smaller Models and Faster Training". [arXiv:2104.00298](https://arxiv.org/abs/2104.00298) — 同一作者的後續研究，搜尋既更小又訓練更快的模型。
