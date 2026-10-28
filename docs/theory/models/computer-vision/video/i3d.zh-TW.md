---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
  - theory/models/computer-vision/video
tags:
  - I3D
  - action recognition
  - 3D convolution
aliases:
  - 膨脹三維卷積
  - I3D
  - Inflated 3D ConvNet
---

# I3D：膨脹的三維卷積網路

I3D 是一個影片動作辨識模型，它把二維影像濾波器膨脹為三維。它的三維濾波器由二維濾波器初始化，並在 Kinetics 影片資料集上訓練。摘要報告，在 Kinetics 上預訓練後，HMDB-51 的準確度為 80.9%，UCF-101 為 98.0%。

## 概觀

[影片章節](index.zh-TW.md)描述了這項任務。本頁說明模型：把影像網路的濾波器沿時間膨脹，並重用其預訓練權重。

## 問題

三維卷積網路能直接學習運動，但在影片上從頭訓練很困難。問題在於如何重用影像預訓練，同時仍能建模運動。

## 核心想法

每個二維濾波器沿時間軸膨脹。它的權重沿時間重複，並除以時間長度，得到三維濾波器。論文指出，對於由相同影格組成的「無聊影片」，膨脹後的網路給出的響應，與把影像網路套用到單一影格時相同。論文稱之為無聊影片的不動點。

## 方程式

對於一個 $N \times N$ 濾波器 $W$，論文沿時間重複 $N$ 次並除以 $N$，得到 $N \times N \times N$ 濾波器：

$$W_{\text{3D}}(t, i, j) = \frac{1}{N} W(i, j), \qquad t = 1, \ldots, N$$

對常數輸入的 $N$ 個時間副本求和，即得到 $W$，這就是上述的不動點性質。

## 結果

摘要報告，在 Kinetics 上預訓練後，HMDB-51 為 80.9%，UCF-101 為 98.0%。論文的表格給出完整比較。

## 限制

- 報告的準確度是在 Kinetics 預訓練之後得到的，摘要並未報告沒有此預訓練的結果。
- 膨脹規則是針對這種形式的濾波器所述。其他架構需要各自推導。

## 關聯

被膨脹的影像網路是[電腦視覺](../index.zh-TW.md)中涵蓋的卷積骨幹。若要看只使用注意力的影片模型，見 [ViViT](vivit.zh-TW.md)。

## 應用

在 HMDB-51、UCF-101 等影片基準上進行動作辨識，數字見論文報告。

## 開放問題

- 膨脹規則如何套用到論文所用以外的架構？
- 準確度有多少來自 Kinetics 預訓練，又有多少來自膨脹後的架構？

## 參考文獻

### 奠基性論文

- Carreira 與 Zisserman，*Quo Vadis, Action Recognition? A New Model and the Kinetics Dataset*（2017）。https://arxiv.org/abs/1705.07750 — 提出 I3D 與 Kinetics 資料集。
- Szegedy 等人，*Going deeper with convolutions*，IEEE Conference on Computer Vision and Pattern Recognition（2015）。https://doi.org/10.1109/CVPR.2015.7298594 — Inception 架構，即 I3D 所膨脹的影像網路。
- Kay、Carreira、Simonyan、Zhang、Hillier、Vijayanarasimhan、Viola、Green、Back、Natsev、Suleyman 與 Zisserman，*The Kinetics Human Action Video Dataset*（2017）。https://arxiv.org/abs/1705.06950 — 提出 I3D 所用預訓練的 Kinetics 資料集。
- Simonyan 與 Zisserman，*Two-Stream Convolutional Networks for Action Recognition in Videos*（2014）。https://arxiv.org/abs/1406.2199 — 提出用於影片動作辨識的雙流卷積設計。
- Tran、Bourdev、Fergus、Torresani 與 Paluri，*Learning Spatiotemporal Features with 3D Convolutional Networks*（2015）。https://arxiv.org/abs/1412.0767 — 提出 C3D，一個早期的影片三維卷積模型。
