---
translation_reviewed: 2026-10-28
related:
  - applications/robotics/navigation
  - theory/models/world-models
tags:
  - robotics
  - navigation
  - topological map
aliases:
  - SPTM
  - Semi-parametric Topological Memory
  - 半參數拓撲記憶
---

# SPTM：半參數拓撲記憶

SPTM 由 Savinov、Dosovitskiy 與 Koltun（arXiv 2018）提出，是一種用於未見過環境導航的記憶架構。它把環境儲存為一張圖：節點是觀測，邊記錄哪些觀測相連，圖中不含度量資訊；另外使用一個學習得到的網路，判斷目前的視野與哪個已儲存的節點相符。所屬的子主題是 [以視覺目標導航](index.md)。

## 概述

此架構的靈感來自動物以地標導航。作者把記憶分成兩部分：第一部分是非參數的圖，也就是一組地點與它們之間的連接；第二部分是參數化的深度網路，輸入一個觀測並檢索對應的節點。由於圖中沒有距離或座標，代理是沿著已見過的地點移動，而不是跟隨度量地圖（Savinov et al., 2018）。

論文的主要結果是：只給五分鐘、未見過的迷宮影片，代理就能建立拓撲地圖，並在測試環境中抵達目標，平均成功率約為最佳基線的三倍。

## 問題

度量導航需要精確的建圖、定位與規劃，而且對環境中的小變化很敏感。只需要地點之間連接關係的方法，可以從環境的一段影片快速建立，並且能容忍不精確的位置。問題在於，學習得到的檢索網路能否可靠地辨識地點，使這種方法可行。

## 核心想法

從一段走訪建立圖：在連續的幀之間加邊，並在學習網路判定為視覺捷徑的幀之間加邊。導航時，在圖中定位目前的視野與目標，找出兩者之間的最短路徑，然後朝路徑上仍與目前視野相似、且最遠的那個節點移動。

## 方程式或演算法

方法包含三個學習或計算的部分：

1. **記憶圖。** 每個節點儲存一張觀測影像。走訪影片以四倍的間隔抽樣。連續的節點相連。當檢索網路判斷兩個觀測在時間上相距很遠但外觀相似時，就加入視覺捷徑，門檻的選擇使約產生 2,000 條捷徑。
2. **檢索網路。** 一個 Siamese 網路，以 ResNet-18 編碼器為每個觀測產生 512 維的嵌入。兩個嵌入串接後通過全連接層，並由二路 softmax 預測兩個觀測在時間上是否接近。它以自監督方式使用交叉熵訓練。正例配對至多相距 20 步，負例配對至少相距 100 步。
3. **移動網路與規劃。** 第二個網路以目前的觀測與下一個路點的觀測為輸入，對七個離散動作輸出 softmax：無動作、前進、後退、向左平移、向右平移、左轉與右轉。代理在圖中定位自己，以 Dijkstra 演算法找出最短路徑，並選擇路徑上最遠、且在一段短的步數窗口內與目前視野相似度超過門檻的節點作為路點。

## 結果

論文在七個測試迷宮中評估代理，成功的定義是在 5,000 步內抵達目標（Savinov et al., 2018, Table 1）。SPTM 在每個測試中都抵達目標，平均為 100%。最佳基線是不以目標為條件的 LSTM，平均為 33.9%。100 與 33.9 的比值約為 2.95，論文將其描述為 SPTM 的成功率高出三倍。

## 限制

- **離散動作。** 移動網路從七個固定動作中選擇，因此代理無法產生平滑的速度，這限制了它對動力學的反應。
- **事先探索。** 在導航之前，必須先由環境的一段走訪建立圖。
- **沒有度量資訊。** 圖只儲存連接關係，因此代理不知道目標有多遠，也無法依距離規劃。
- **受控環境。** 報告的實驗是在迷宮中進行的。在較大、會改變的戶外場景中的結果不在論文的評估範圍內。

## 相關連結

- [ViNG](ving.md) 延續這個想法。它以學習得到的時間距離函數取代檢索網路，並加入一個學習得到的位姿預測器，驅動控制器。
- [視覺教導與重播](visual-teach-and-repeat.md) 是經典的替代方法。它同樣儲存路線，但以里程計而非學習得到的檢索網路來追蹤路線。
- [世界模型](../../../theory/models/world-models/index.md) 涵蓋環境的預測模型，是儲存圖以外的另一種選擇。

## 開放問題

- 當環境在走訪與導航執行之間發生改變時，學習得到的檢索是否仍然可靠。
- 如何在不失去對不精確位置之穩健性的前提下，為圖加入度量資訊。

## 參考文獻

- Savinov, N., Dosovitskiy, A. & Koltun, V. (2018). *Semi-parametric Topological Memory for Navigation*. arXiv. https://arxiv.org/abs/1803.00653 — 介紹拓撲記憶、檢索網路與規劃方法，並包含上文引用的迷宮結果。
- Shah, D., Eysenbach, B., Kahn, G., Rhinehart, N. & Levine, S. (2021). *ViNG: Learning Open-World Navigation with Visual Goals*. ICRA 2021. https://doi.org/10.1109/ICRA48506.2021.9561936 — 以學習得到的時間距離與學習得到的控制器擴充拓撲圖。
- Furgale, P. & Barfoot, T. D. (2010). *Visual teach and repeat for long-range rover autonomy*. Journal of Field Robotics, 27(5), 534–560. https://doi.org/10.1002/rob.20342 — 經典的教導與重播系統，儲存路線並以里程計追蹤。
- Krajník, T., Majer, F., Halodová, L. & Vintr, T. (2017). *Navigation without localisation: reliable teach and repeat based on the convergence theorem*. arXiv. https://arxiv.org/abs/1711.05348 — 重播教導時的運動，並只用相機修正航向。
- Dall'Osto, D., Fischer, T. & Milford, M. (2020). *Fast and Robust Bio-inspired Teach and Repeat Navigation*. arXiv. https://arxiv.org/abs/2010.11326 — 一種充分利用里程計的非同步教導與重播方法。
