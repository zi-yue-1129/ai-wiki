---
related:
- brain-mind/neuroai
aliases:
  - Convolution Variants
  - Depthwise Separable Convolution
  - Dilated Convolution
  - 卷積變體
  - 深度可分離卷積
tags:
  - convolution
  - efficient inference
  - computer vision
translation_reviewed: 2026-10-28
---

# 卷積變體

卷積運算有數種變體，每一種改變三個性質之一：取樣的位置集合（感受野）、通道混合的方式，或輸出的空間佈局。選擇哪種變體，會決定某深度下的感受野大小、參數數量與每層成本。多數影像架構由其中一兩種形式組成。

## 概觀

| 變體 | 改變的部分 | 主要好處 | 主要代價 |
|---|---|---|---|
| 標準 | 鄰域上的稠密核，所有通道混合 | 表達力強，理解透徹 | 成本隨核大小與通道數增長 |
| 空洞 | 核的取樣點之間留有間隔 | 感受野變大，參數不變 | 使用不當會出現網格偽影 |
| 深度可分離 | 每個通道一個空間濾波器，再用 1×1 混合通道 | 成本大幅降低 | 每層表達力較弱 |
| 轉置 | 可學習的上採樣 | 解碼器與生成 | 棋盤狀偽影 |
| 可變形 | 每個位置學習取樣點 | 能適應物件形狀 | 記憶體存取不規則，較慢 |

## 做法

### 空洞卷積

空洞卷積把核的取樣點間隔開來。Yu 與 Koltun（2015）用堆疊的空洞層做密集預測，使感受野隨深度呈指數成長，同時保持特徵圖的全解析度。這適合需要像素級輸出的分割，但堆疊的空洞可能遺漏某些像素，後來的設計會以混合的空洞率來處理。

### 深度可分離卷積

標準卷積在一步中同時混合空間與通道。深度可分離卷積把兩者拆開：每個通道一個空間濾波器，接著用 1×1 卷積混合通道。把這種設計推到極致的 Xception 架構，在 ImageNet 上的準確率優於參數量相近的 Inception V3。MobileNet 系列的網路使用同樣的分解做裝置端推論。

### 可變形卷積

一般的核會在每個位置周圍取固定的網格。可變形卷積為每個取樣點學習偏移量，使核能貼合物件的形狀。Dai 等人（2017）在偵測與分割上展示了增益，代價是不規則的記憶體存取，使它在某些硬體上較慢。

### 轉置卷積

轉置卷積用於解碼器中的特徵圖上採樣，常見於分割與生成。常見問題是步幅無法整除核大小時出現的棋盤狀圖樣。常用的替代做法是先調整大小再卷積，以避免這個問題。

## 取捨

- **感受野與解析度。** 空洞與下採樣都能擴大感受野，但下採樣會損失空間細節，空洞則保留細節。
- **參數與準確率。** 可分離卷積節省參數與運算，但只由它們組成的網路若不增加寬度，容量可能下降。
- **硬體。** 深度運算在許多加速器上受記憶體限制，因此運算量較少不一定代表延遲較低。

## 相關連結

這些變體是 [CNN 家族](../index.md)的建構單元，同樣的局部性想法也出現在[注意力變體](../../transformer/attention-variants/index.md)中，局部窗口取代了固定核。感受野問題也與更廣的[電腦視覺](../../computer-vision/index.md)任務相連。

## 未解問題與更多變體

- **學習取樣模式。** 可變形卷積學習取樣位置，但會增加不規則的運算。對硬體友善的學習式取樣仍是待解的工程問題。
- **全域脈絡。** 空洞與大核卷積擴展了脈絡，但在需要長程關係的任務上，仍不如完整注意力。
- **等變性。** 標準與空洞卷積只對平移等變。把它們推廣到旋轉與其他變換，是活躍的研究方向。

## 參考文獻

### 開創性論文

- Yu, F. & Koltun, V. (2015). "Multi-Scale Context Aggregation by Dilated Convolutions". arXiv:1511.07122 — 用於密集預測的空洞卷積，感受野隨深度指數成長。
- Dai, J., et al. (2017). "Deformable Convolutional Networks". arXiv:1703.06211 — 學習取樣偏移量，使卷積能適應物件形狀。
- Chollet, F. (2016). "Xception: Deep Learning with Depthwise Separable Convolutions". arXiv:1610.02357 — 顯示把空間與通道混合分解後，能以較低成本超越 Inception 式設計。
- Howard, A. G., et al. (2017). "MobileNets: Efficient Convolutional Neural Networks for Mobile Vision Applications". arXiv:1704.04861 — 深度可分離卷積，作為高效裝置端視覺的建構單元。
- Chen, L.-C., et al. (2016). "DeepLab: Semantic Image Segmentation with Deep Convolutional Nets, Atrous Convolution, and Fully Connected CRFs". arXiv:1606.00915 — 空洞卷積搭配全連接條件隨機場，用於密集分割。

### 綜述與教科書

（本頁尚未核對）

### 講座與影片

（本頁尚未核對）

### 文章與文件

（本頁尚未核對）
