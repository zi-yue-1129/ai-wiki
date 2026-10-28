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

I3D 是一個影片動作辨識模型，它把二維影像濾波器膨脹為三維。它的權重可以從影像預訓練的網路開始，並在 Kinetics 影片資料集上訓練。它為動作辨識建立了強勁的基準，至今仍是常見的參考點。

## 概觀

[影片章節](index.zh-TW.md)描述了這項任務。本頁說明模型。主要想法是取一個成功的影像架構，在每個濾波器上加入時間維度，並透過沿時間重複二維的預訓練權重，重用它們。

## 問題

三維卷積網路能直接學習運動，但很難從頭訓練，因為影片資料集與影像資料集相比很小。問題在於如何利用影像預訓練，同時仍能建模運動。

## 核心想法

每個二維的 $k \times k$ 濾波器會沿時間軸重複其權重並重新縮放，膨脹為三維的 $k \times k \times k$ 濾波器。膨脹後的網路一開始的行為，就等同於把影像網路套用到每一個影格上；之後在影片上訓練時，它再學習時間結構。作者採用雙流設計：一條流接收 RGB 影格，另一條流接收光流，並把兩者結合。

## 方程式

若一個二維濾波器 $W \in \mathbb{R}^{k \times k}$ 膨脹到 $T$ 個影格，則三維濾波器為

$$W_{\text{3D}}(t, i, j) = \frac{1}{T} W(i, j), \qquad t = 1, \ldots, T,$$

因此，一段由相同影格組成的影片，會產生與把影像網路套用到單一影格時相同的輸出。除以 $T$ 可使響應尺度保持穩定。

## 結果

論文報告，先在 Kinetics 上預訓練、再於較小的資料集上微調，能在 HMDB-51 與 UCF-101 上取得強勁結果，數字見摘要與結果表。確切數值請參考原論文。

## 限制

- 三維卷積在記憶體與計算上都很昂貴，這限制了片段長度與解析度。
- 局部核只能捕捉短時間窗內的運動，因此與注意力相比，較難建模長距離的依賴關係。
- 效能高度依賴大型標註資料集，資料集的偏差可能被學成捷徑。

[ViViT](vivit.zh-TW.md)以基於注意力的詞元取代了卷積設計。

## 關聯

膨脹的想法與[電腦視覺](../index.zh-TW.md)中的影像模型骨幹相連，它所依據的 Inception 式架構則見所引用的 GoogLeNet 論文。它的訓練使用了[正規化](../../../deep-learning/normalisation/index.zh-TW.md)中討論的批次正規化。

## 應用

體育與影片分析中的動作辨識、人類活動監測，以及作為影片檢索的特徵抽取器。

## 開放問題

- 在目前的基準上，卷積影片模型學到的是運動還是外觀捷徑？
- 膨脹應如何套用到 Inception 以外的架構？

## 參考文獻

### 奠基性論文

- Carreira 與 Zisserman，*Quo Vadis, Action Recognition? A New Model and the Kinetics Dataset*（2017）。https://arxiv.org/abs/1705.07750 — 提出 I3D 與 Kinetics 資料集。
- Szegedy 等人，*Going deeper with convolutions*，IEEE Conference on Computer Vision and Pattern Recognition（2015）。https://doi.org/10.1109/CVPR.2015.7298594 — I3D 所膨脹的 Inception 架構。
- Kay、Carreira、Simonyan、Zhang、Hillier、Vijayanarasimhan、Viola、Green、Back、Natsev、Suleyman 與 Zisserman，*The Kinetics Human Action Video Dataset*（2017）。https://arxiv.org/abs/1705.06950 — I3D 所用預訓練的資料集。
- Simonyan 與 Zisserman，*Two-Stream Convolutional Networks for Action Recognition in Videos*（2014）。https://arxiv.org/abs/1406.2199 — I3D 所延伸的雙流設計。
- Tran、Bourdev、Fergus、Torresani 與 Paluri，*Learning Spatiotemporal Features with 3D Convolutional Networks*（2015）。https://arxiv.org/abs/1412.0767 — C3D 模型，是早期的三維卷積基準。
