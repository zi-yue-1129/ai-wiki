---
related:
- theory/models/cnn/backbones-and-scaling
- theory/models/cnn
aliases:
  - A ConvNet for the 2020s
  - ConvNeXt
  - ConvNeXt 網路
tags:
  - convolutional networks
  - architecture design
  - computer vision
translation_reviewed: 2026-10-28
---

# ConvNeXt

ConvNeXt 是一種純卷積網路，由 Liu 等人於 2022 年在《A ConvNet for the 2020s》（[arXiv:2201.03545](https://arxiv.org/abs/2201.03545)）中提出。作者從 ResNet 出發，逐步現代化其設計，並借用 Transformer 的選擇。得到的網路在 ImageNet-1K、COCO 偵測與 ADE20K 分割上，都優於規模相近的 Swin Transformer 基線。

## 問題

Swin 等 Transformer 模型已成為視覺任務的強基線，問題是它們的優勢有多少來自核心運算（自注意力），又有多少來自設計與訓練的選擇。論文回答的是後半部分：以現代的配方與設計重新檢視卷積網路，並在 ImageNet-1K 上衡量每一項改動。

## 核心想法

論文從 ResNet-50 出發，依序套用一系列改動，每一步都以 ImageNet-1K 準確率衡量：

- 宏觀設計：階段比例改為 3:3:9:3，並以 4×4、步幅 4 的「patchify」層作為網路的起始層。
- 區塊設計：採用 ResNeXt 風格的深度卷積，寬度增加到 96；並使用倒瓶頸，隱藏寬度為輸入寬度的四倍。
- 核大小：使用 7×7 的深度卷積，並把它移到區塊的前段。論文指出，增益在 7×7 時趨於飽和。
- 激活與正規化：以 GELU 取代 ReLU，每個區塊只保留一個激活函數；以一個 LayerNorm 取代 BatchNorm；降採樣由獨立的 2×2、步幅 2 的層負責。

論文中的 ResNet-50 基線在其配方下達到 76.13% top-1，完整的改動序列在相同的 ImageNet-1K 設定下，讓 ConvNeXt-T 達到 81.97%。作者在同一表格中指出 Swin-T 為 81.30%。

## 方程式或演算法

依論文所述的形式，ConvNeXt 區塊是一個殘差區塊，其步驟如下：

\[
y = x + \text{PWConv}_2\!\left(\text{GELU}\!\left(\text{PWConv}_1\!\left(\text{LN}\!\left(\text{DWConv}_{7\times 7}(x)\right)\right)\right)\right)
\]

其中 DWConv 為 7×7 深度卷積，LN 為層正規化，兩個逐點（1×1）卷積構成倒瓶頸，先將寬度擴張為四倍，再投影回原寬度。

## 結果

所有數字皆取自論文的表格。除非另外註明，top-1 準確率皆為 ImageNet-1K。

- 在 224² 解析度下，ConvNeXt-T 達到 82.1%，參數 29M、4.5G FLOPs；Swin-T 為 81.3%，參數 28M、4.5G FLOPs。ConvNeXt-B 達到 83.8%，參數 89M、15.4G FLOPs；Swin-B 為 83.5%，參數 88M、15.4G FLOPs。ConvNeXt-L 達到 84.3%，參數 198M、34.4G FLOPs。
- 使用 ImageNet-22K 預訓練時，ConvNeXt-XL（350M 參數）在 224² 達到 87.0%，在 384² 達到 87.8%。
- COCO 物件偵測（Cascade Mask R-CNN，22K 預訓練）的 box AP：ConvNeXt-B 為 54.0，Swin-B 為 53.0；ConvNeXt-L 為 54.8，Swin-L 為 53.9。
- ADE20K 分割（UperNet，22K 預訓練）的 mIoU：ConvNeXt-B 為 53.1，Swin-B 為 51.7。
- 論文報告，在相近參數量下，ConvNeXt 在 V100 上比 Swin 更快；在 A100 上，其吞吐量可以高出許多。

## 限制

- 作者指出，「ConvNeXt 可能較適合某些任務，而 Transformer 對其他任務可能較有彈性」。他們認為，多模態學習可能較適合交叉注意力；對於離散、稀疏或結構化的輸出，Transformer 可能較有彈性。
- 已知深度卷積模型在 FLOPs 相同時較慢且較耗記憶體。論文報告其在各任務上的吞吐量與 Swin 相當或更高；並指出在 Cascade Mask R-CNN 中，ConvNeXt-B 的訓練記憶體為 17.4 GB，Swin-B 為 18.5 GB。
- 每一項設計選擇先前都已被研究過。論文的貢獻在於把它們組合起來，作者把其縮放結果描述為「令人鼓舞，但尚未完全令人信服」。

## 相關連結

- [骨幹與縮放](../index.md)將 ConvNeXt 列為現代化的純 CNN，與殘差連接及複合縮放並列。
- [ResNet](../resnet/index.md) 是現代化改造的起點，最終設計中仍保留殘差區塊。
- [VGG](../vgg/index.md) 是 3×3 卷積的普通堆疊。ConvNeXt 使用較大的 7×7 深度卷積，而論文與 Transformer 的比較，是與 VGG 的深度研究不同的問題。
- [EfficientNet](../efficientnet/index.md) 以縮放而非重新設計區塊，處理同一個骨幹問題。
- [卷積變體](../../convolution-variants/index.md)說明深度卷積，ConvNeXt 以 7×7 核使用它。
- [CNN](../../index.md) 提供卷積模型與 Transformer 相比的更廣脈絡。

## 未解問題與更多變體

- **對預訓練的依賴。** 沒有 ImageNet-22K 預訓練時，增益很小。在 COCO box AP 上，ConvNeXt-T 與 Swin-T 同為 50.4；在 ADE20K 上，ConvNeXt-T 為 46.7，Swin-T 為 45.8。這個優勢在其他資料情境下是否成立，仍是開放問題。
- **卷積與注意力。** 論文認為 Transformer 的大部分優勢可與注意力分開，但注意力運算對多模態或結構化輸出是否重要，本研究尚未確定。
- **大核與硬體。** 7×7 深度卷積的增益已趨於飽和，而深度卷積核在某些硬體上會增加記憶體與速度成本。這個取捨在其他硬體上如何變化，是實務上的開放問題。

## 參考文獻

### 開創性論文

- Liu, Z., et al. (2022). "A ConvNet for the 2020s". [arXiv:2201.03545](https://arxiv.org/abs/2201.03545) — ConvNeXt，一個現代化的純 CNN，與 Transformer 基線相當。
- He, K., et al. (2015). "Deep Residual Learning for Image Recognition". [arXiv:1512.03385](https://arxiv.org/abs/1512.03385) — 殘差連接，使極深的 CNN 能夠訓練。
- Simonyan, K. & Zisserman, A. (2015). "Very Deep Convolutional Networks for Large-Scale Image Recognition". [arXiv:1409.1556](https://arxiv.org/abs/1409.1556) — 堆疊小型 3×3 卷積的普通深層設計，即 VGG 的基礎。
- Tan, M. & Le, Q. V. (2019). "EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks". [arXiv:1905.11946](https://arxiv.org/abs/1905.11946) — 同時縮放深度、寬度與輸入解析度的複合縮放。

### 綜述與教科書

- Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep Learning*. MIT Press. https://www.deeplearningbook.org/ — 第 9 章介紹卷積網路與卷積運算的標準說明。

### 講座與影片

（本頁尚未核對）

### 文章與文件

（本頁尚未核對）
