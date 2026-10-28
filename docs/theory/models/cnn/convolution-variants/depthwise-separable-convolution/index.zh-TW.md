---
related:
- theory/models/cnn/convolution-variants
- theory/models/cnn
aliases:
  - Depthwise Separable Convolution
  - DSC
  - 深度可分離卷積
tags:
  - convolution
  - efficient inference
  - mobile vision
translation_reviewed: 2026-10-28
---

# 深度可分離卷積

深度可分離卷積把一般卷積拆成兩步：先對每個通道分別套用一個空間濾波器，再用 1×1 卷積混合通道。Chollet（2016）在 "Xception: Deep Learning with Depthwise Separable Convolutions" 中把這種設計推到極致：Xception 以深度可分離卷積取代 Inception 模組，並加入殘差連接。

## 問題

一般卷積在一次運算中同時做空間濾波與通道混合，因此成本隨核大小增長，也隨輸入與輸出通道數的乘積增長。Inception 模組顯示，把這兩件事拆開可以運作得很好，但 Inception 家族仍混用多種運算。Xception 論文問的是：若把這種拆分推到極致，會發生什麼事。

## 核心想法

Xception 論文把深度可分離卷積描述為「對輸入的每個通道獨立進行的空間卷積」，接著是「把深度卷積的輸出通道投影到新通道空間的 1×1 卷積」。論文指出，這種卷積「可以理解為具有最大數量分支的 Inception 模組」。Xception 之名即 "Extreme Inception"（極致 Inception）：整個架構由這些區塊與殘差連接組成。MobileNets（Howard 等人，2017）則以同樣的分解作為高效裝置端視覺的建構單元。

## 方程式或演算法

對於輸入通道數 \(C_{\text{in}}\)、輸出通道數 \(C_{\text{out}}\)、\(k \times k\) 的核，以及大小為 \(H \times W\) 的輸出，一般卷積的成本約為 \(k^2 C_{\text{in}} C_{\text{out}} HW\) 次乘加。深度可分離形式的成本為深度卷積的 \(k^2 C_{\text{in}} HW\) 加上 1×1 步驟的 \(C_{\text{in}} C_{\text{out}} HW\)，因此與一般卷積成本的比值為 \(1/C_{\text{out}} + 1/k^2\)。此比值由上述定義推出，並非論文報告的數字。

## 結果

在 ImageNet 上，採單一裁剪、單一模型的評估，Xception 的 top-1 分數為 0.790，top-5 為 0.945；Inception V3 則為 0.782 與 0.941。論文指出兩者的參數量幾乎相同：Inception V3 為 23,626,728，Xception 為 22,855,952（見其表 3）。論文的結論是，增益來自更有效率地使用模型參數，而非額外的容量。在 JFT 資料集上，論文報告 FastEval14k MAP@100 相對提升 4.3%（有全連接層時為 6.50 對 6.78）。

## 限制

論文自己指出幾項限制。其最佳化設定是為 Inception V3 調校的，作者也沒有為 Xception 調校最佳化的超參數。ImageNet 結果是在驗證集上報告的，JFT 的模型「沒有訓練到完全收斂」。移除深度步驟與逐點步驟之間的非線性，在 ImageNet 上帶來更快的收斂與更好的最終表現，但作者認為該非線性的有無「可能很重要」。依論文自己的計時，Xception 略慢於 Inception V3（表 3 中為每秒 28 步對 31 步），儘管參數量相近。

## 相關連結

[卷積變體](../index.md)頁面把這種分解與其他形式並列比較，[CNN 家族](../../index.md)頁面說明它是 CNN 的建構單元之一。高效骨幹網路的做法，以及如何縮放這些骨幹，見[骨幹與縮放](../../backbones-and-scaling/index.md)頁面，其中包括 [EfficientNet](../../backbones-and-scaling/efficientnet/index.md)。[空洞卷積](../dilated-convolution/index.md)與[可變形卷積](../deformable-convolution/index.md)頁面涵蓋另外兩種形式的改變，它們改變的是取樣位置，而非通道的混合方式。[注意力變體](../../../transformer/attention-variants/index.md)頁面則介紹另一條提升效率的路線，即局部窗口。

## 未解問題與更多變體

- **非線性的位置。** 論文仍未確定深度步驟與逐點步驟之間的非線性是否重要。實驗中移除它在 ImageNet 上有幫助，但效果的原因未獲解釋。
- **中間形式的設計。** 論文表示「沒有理由相信深度可分離卷積是最佳的」，並把 Inception 式模組與完全深度可分離形式之間的中間形式留待未來研究。
- **運算量與速度。** 較少的運算量不必然代表較低的延遲。卷積變體頁面指出，深度運算在許多加速器上受記憶體限制；論文自己的計時也顯示，儘管大小相近，Xception 仍略慢。

## 參考文獻

### 開創性論文

- Chollet, F. (2016). "Xception: Deep Learning with Depthwise Separable Convolutions". arXiv:1610.02357 — 顯示把空間與通道混合分解後，能以較低成本超越 Inception 式設計。
- Howard, A. G., et al. (2017). "MobileNets: Efficient Convolutional Neural Networks for Mobile Vision Applications". arXiv:1704.04861 — 深度可分離卷積，作為高效裝置端視覺的建構單元。
- Tan, M. & Le, Q. V. (2019). "EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks". arXiv:1905.11946 — 同時縮放深度、寬度與輸入解析度。

### 綜述與教科書

- Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep Learning*. MIT Press. https://www.deeplearningbook.org/ — 第 9 章介紹卷積網路與卷積運算的標準說明。

### 講座與影片

（本頁尚未核對）

### 文章與文件

- Liu, Z., et al. (2022). "A ConvNet for the 2020s". arXiv:2201.03545 — ConvNeXt，一個現代化的純 CNN，與 Transformer 基線相當。
