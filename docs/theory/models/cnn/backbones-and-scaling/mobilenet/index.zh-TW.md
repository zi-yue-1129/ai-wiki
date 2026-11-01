---
related:
  - theory/models/cnn/backbones-and-scaling
  - theory/models/cnn/convolution-variants/depthwise-separable-convolution
  - engineering/on-device-edge/tinyml-and-mobile-runtimes
tags:
  - efficient architectures
  - mobile vision
  - computer vision
last_reviewed: 2026-11-01
translation_reviewed: 2026-11-01
aliases:
  - MobileNet
  - MobileNetV1
  - 行動網路
  - 深度可分離卷積網路
---

# MobileNets（Howard et al., 2017）

MobileNets 是一族以深度可分離卷積建構的影像分類網路。它以少量準確率換取大幅降低的運算量，使卷積網路能在手機或其他小型裝置上執行。Howard et al.（2017）提出這種設計，並附上兩個全域設定，用來選擇網路的大小。

## 概觀

標準卷積必須同時在空間與通道之間混合資訊。每個輸出值都取決於一個小的空間視窗以及所有輸入通道，因此成本是兩者的乘積。MobileNets 把這兩項工作拆成獨立的步驟，從而大幅降低成本。論文的目標是行動與嵌入式視覺，在這類場景中，延遲與準確率之間的取捨最為重要（Howard et al., 2017）。

## 關鍵概念

- **深度卷積（depthwise convolution）**：對每個輸入通道分別套用一個空間濾波器。
- **逐點卷積（pointwise convolution）**：1×1 卷積，在每個位置上混合通道。
- **寬度乘數（width multiplier，α）**：縮放每一層的通道數。
- **解析度乘數（resolution multiplier，ρ）**：縮放輸入影像的大小，進而縮放每個特徵圖的空間尺寸。

## 問題

作者希望建立一族適用於行動與嵌入式視覺的網路，使延遲與準確率之間的取捨能夠依照給定的預算來設定。他們的做法是用一種架構加上兩個全域超參數，而不必為每種預算重新設計網路（Howard et al., 2017）。

## 核心想法

把每個標準卷積換成深度可分離卷積：先以深度卷積對每個通道做空間濾波，再以逐點卷積混合通道。若將深度卷積與逐點卷積分別計為一層，整個網路共有 28 層。兩個全域設定可進一步降低成本：寬度乘數讓每一層變窄，解析度乘數縮小輸入影像（Howard et al., 2017）。

## 方程式

設卷積核為 D_K × D_K，輸入有 M 個通道，輸出有 N 個通道，特徵圖為 D_F × D_F。標準卷積的成本為

\[
D_K^2 \cdot M \cdot N \cdot D_F^2
\]

深度可分離卷積的成本為

\[
D_K^2 \cdot M \cdot D_F^2 + M \cdot N \cdot D_F^2
\]

兩者的比值為

\[
\frac{1}{N} + \frac{1}{D_K^2}
\]

對 3×3 卷積核而言，當 N 很大時這個比值趨近於 1/9，這就是論文把節省描述為少 8 到 9 倍運算量的原因（Howard et al., 2017）。

兩個乘數會進入同一個公式。設寬度乘數為 α、解析度乘數為 ρ，成本變為

\[
D_K^2 \cdot \alpha M \cdot \rho D_F^2 + \alpha M \cdot \alpha N \cdot \rho D_F^2
\]

論文指出，寬度乘數大約以 α² 的比例降低運算量與參數量，解析度乘數則以 ρ² 的比例降低運算量。寬度乘數的取值範圍為 (0, 1]，常用設定為 1、0.75、0.5 與 0.25。解析度乘數通常設定為使輸入為 224、192、160 或 128 像素（Howard et al., 2017）。

## 結果

下表列出輸入為 224 像素時的 ImageNet top-1 準確率，以及各寬度設定的 Mult-Adds 與參數量：

| 寬度乘數 | Top-1 準確率 | Mult-Adds | 參數量 |
|---|---|---|---|
| 1.0 | 70.6% | 5.69 億 | 420 萬 |
| 0.5 | 63.7% | 1.49 億 | 130 萬 |
| 0.25 | 50.6% | 4,100 萬 | 50 萬 |

這些數字來自論文本身（Howard et al., 2017，表 6）。寬度 1.0 的完整模型是參照點，較小的設定則顯示此乘數所控制的取捨。

論文也把 MobileNets 應用於物件偵測、細粒度分類、人臉屬性與大規模地理定位，並報告其與其他常見模型相比的強勁表現（Howard et al., 2017）。

## 後續版本

Sandler et al.（2018）提出 MobileNetV2，採用倒置殘差區塊與線性瓶頸。摘要指出，在狹窄的層中移除非線性十分重要。它也建構了用於偵測的 SSDLite，以及精簡版的 DeepLabv3 用於分割（Sandler et al., 2018）。Howard et al.（2019）則以架構搜尋設計 MobileNetV3（Howard et al., 2019）。

## 相關連結

- [深度可分離卷積](../../convolution-variants/depthwise-separable-convolution/index.md) 是讓 MobileNets 變得便宜的運算，它有自己的頁面。
- [ResNet](../resnet/index.md) 與 [EfficientNet](../efficientnet/index.md) 追求更大規模下的準確率。MobileNets 位於同一族取捨中偏向高效率的一端。
- [微型機器學習與行動執行環境](../../../../../engineering/on-device-edge/tinyml-and-mobile-runtimes/index.md) 說明在裝置上執行此類模型的軟體。

## 應用

MobileNets 面向裝置端視覺。論文將它們應用於影像分類、物件偵測、分割、細粒度辨識、人臉屬性與地理定位（Howard et al., 2017; Sandler et al., 2018）。

## 限制

- **窄寬度時的準確率。** 0.25 的設定比完整模型低約 20 個百分點的 top-1 準確率，因此取捨在低端非常陡峭。
- **成本只是代理指標。** 論文報告的是 multiply-adds 與參數量。這些數字描述運算與儲存，並非在特定裝置上實際測得的延遲。
- **後續修訂。** MobileNetV2 與 MobileNetV3 改變了區塊設計與搜尋流程，因此比較時必須註明版本，不應把第一版的結果直接與後續版本相比。

## 未解問題

- multiply-adds 在新型加速器上能多好地預測延遲，以及深度卷積是否能像其低成本所暗示的那樣有效率地執行。
- 像 MobileNetV3 那樣的架構搜尋，是否能在相同成本下得到手工設計的區塊無法達到的增益。

## 參考文獻

### 開創性論文

- Howard, A. G. et al. (2017). *MobileNets: Efficient Convolutional Neural Networks for Mobile Vision Applications*. arXiv. https://arxiv.org/abs/1704.04861 — 提出深度可分離卷積，並在一族具有寬度與解析度乘數的網路中使用。
- Sandler, M. et al. (2018). *MobileNetV2: Inverted Residuals and Linear Bottlenecks*. arXiv. https://arxiv.org/abs/1801.04381 — 第二版，採用倒置殘差區塊與線性瓶頸，並應用於偵測與分割。
- Howard, A. et al. (2019). *Searching for MobileNetV3*. arXiv. https://arxiv.org/abs/1905.02244 — 第三版，以架構搜尋設計。

### 綜述與相關模型

- Chollet, F. (2016). *Xception: Deep Learning with Depthwise Separable Convolutions*. arXiv. https://arxiv.org/abs/1610.02357 — 以深度可分離卷積建構大型網路，與 MobileNets 使用相同的運算。
- Iandola, F. N. et al. (2016). *SqueezeNet: AlexNet-level accuracy with 50x fewer parameters and <0.5MB model size*. arXiv. https://arxiv.org/abs/1602.07360 — 同期的精簡網路，為較小的參數預算而設計，從另一種設計達成相同目標。
