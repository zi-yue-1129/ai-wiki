---
related:
- theory/models/cnn/backbones-and-scaling
- theory/models/cnn
aliases:
  - Very Deep Convolutional Networks
  - VGG
  - VGG 網路
tags:
  - convolutional networks
  - model depth
  - computer vision
translation_reviewed: 2026-10-28
---

# VGG

VGG 是一族深層卷積網路，由 Simonyan 與 Zisserman 在 2015 年的論文《Very Deep Convolutional Networks for Large-Scale Image Recognition》（arXiv:1409.1556）中提出。論文顯示，以 3×3 卷積組成的簡單、統一堆疊，配合 11 到 19 層的權重層，就能在 ImageNet 上達到很強的準確率，並把深度變成主要的研究變數。

## 問題

論文要問的是：卷積網路的深度，如何影響大規模影像辨識的準確率？為了單獨觀察深度，作者讓其他架構選擇保持固定，只不斷加入卷積層。這之所以可行，是因為每一層都使用極小的 3×3 濾波器，因此深度可以增加，而濾波器的設計不必改變。

## 核心想法

每個卷積層都使用步幅 1 的 3×3 濾波器，並以最大池化分隔各組卷積。兩層堆疊的 3×3 卷積有 5×5 的有效感受野，三層則有 7×7。論文認為，三層 3×3 卷積比一層 7×7 多了三次非線性，「使決策函數更具辨別力」，而且權重較少：在輸入與輸出通道數皆為 C 時，三層 3×3 需要 27C² 個權重，一層 7×7 則需要 49C²。論文把這視為對 7×7 濾波器的一種正則化。

## 方程式或演算法

論文中的組態（表 1 的 A 至 E）主要差在每個階段包含多少卷積。各組態的前向流程形狀相同：

```
input: 224×224 RGB crop
for each of the 5 stages:
    repeat n_s times: 3×3 convolution (stride 1) followed by ReLU
    2×2 max pooling (stride 2)
flatten, then
    fully connected 4096 + ReLU
    fully connected 4096 + ReLU
    fully connected 1000, then softmax
```

支撐 3×3 選擇的權重比較為

\[
3 \cdot (3 \cdot 3 \cdot C^2) = 27C^2 \qquad \text{對比} \qquad 7 \cdot 7 \cdot C^2 = 49C^2 .
\]

## 結果

以下數字皆為論文報告的 ILSVRC（ImageNet）誤差率。

- 固定尺度 256 訓練的單一尺度評估（驗證集 top-1 與 top-5 誤差）：組態 B（13 層權重層）為 28.7% 與 9.9%，D（16 層）為 27.0% 與 8.8%，E（19 層）為 27.3% 與 9.0%。若訓練時做尺度抖動（256 至 512）並於 384 測試，D 為 25.6% 與 8.1%，E 為 25.5% 與 8.0%。
- 論文中最佳的單一網路在驗證集上的誤差為 top-1 24.8%、top-5 7.5%。
- 兩個網路的組合在驗證集上的誤差為 top-1 23.7%、top-5 6.8%。
- ILSVRC-2014 的提交（七個模型的組合）在測試集上的 top-5 誤差為 7.3%，論文稱此為該競賽的第二名。
- 論文表 2 的參數量：組態 A 與 B 為 1.33 億，組態 E 為 1.44 億。

## 限制

- 訓練成本高。論文報告在四張 NVIDIA Titan Black GPU 上，訓練單一網路需要 2 到 3 週。
- 誤差在 19 層時趨於飽和。作者認為更深的模型在更大的資料集上可能有幫助，但論文並未測試。
- 局部響應正規化沒有改善組態 A，反而增加了記憶體用量與運算時間。
- 多裁切評估的增益很小，作者認為實務上額外的運算不足以換取這些增益。
- 多數實驗以驗證集作為測試集使用。

## 相關連結

- [骨幹與縮放](../index.md)把 VGG 放在普通深層設計的位置。[ResNet](../resnet/index.md) 加入捷徑連接，讓網路可以加深；[EfficientNet](../efficientnet/index.md) 則同時縮放深度、寬度與解析度。
- [ConvNeXt](../convnext/index.md) 在類 ResNet 的設計中，以較大的 7×7 深度卷積重新審視堆疊卷積的想法。
- [卷積變體](../../convolution-variants/index.md)說明 VGG 所堆疊的標準卷積。
- [CNN](../../index.md) 提供家族的整體脈絡。
- [電腦視覺](../../../computer-vision/index.md)介紹 VGG 所針對的影像分類任務。

## 未解問題與更多變體

- **超過 19 層的深度。** 論文在 19 層時觀察到飽和。之後殘差連接讓深得多的網路可以訓練，因此普通堆疊何時不再有幫助，與最佳化有關，而不只是深度本身。
- **訓練成本。** 訓練需要數週、使用四張 GPU。如何以較低成本獲得同樣的深度與準確率取捨，仍是開放問題；後續的 EfficientNet 則直接比較準確率與運算量。

## 參考文獻

### 開創性論文

- Simonyan, K. & Zisserman, A. (2015). "Very Deep Convolutional Networks for Large-Scale Image Recognition". arXiv:1409.1556 — 堆疊小型 3×3 卷積的普通深層設計，即 VGG 的基礎。
- He, K., et al. (2015). "Deep Residual Learning for Image Recognition". arXiv:1512.03385 — 殘差連接，使極深的 CNN 能夠訓練。
- Huang, G., et al. (2017). "Densely Connected Convolutional Networks". arXiv:1608.06993 — 每一層都與其後所有層相連，重用特徵並改善梯度流。

### 綜述與教科書

- Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep Learning*. MIT Press. https://www.deeplearningbook.org/ — 第 9 章介紹卷積網路與卷積運算的標準說明。

### 講座與影片

（本頁尚未核對）

### 文章與文件

- Liu, Z., et al. (2022). "A ConvNet for the 2020s". arXiv:2201.03545 — ConvNeXt，一個現代化的純 CNN，與 Transformer 基線相當。
