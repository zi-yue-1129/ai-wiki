---
translation_reviewed: 2026-10-28
related:
  - applications/robotics/navigation
  - theory/paradigms/imitation
tags:
  - robotics
  - navigation
  - topological graph
aliases:
  - ViNG
  - Visual Navigation Graph
  - 視覺目標導航圖
---

# ViNG：學習以視覺目標進行開放世界導航

ViNG 由 Shah、Eysenbach、Kahn、Rhinehart 與 Levine（ICRA 2021）提出，是一個以學習為基礎、在實體移動機器人上抵達目標影像的系統。它結合學習得到的距離估計，以及由先前蒐集的觀測所建立的拓撲圖，因此部署時可以更換目標而無需重新訓練。所屬的子主題是 [以視覺目標導航](index.md)。

## 概述

學習得到的導航策略很難改變方向。傳統規劃器可以給予新的目標，但為某一目的地訓練的策略若要前往別處，就必須重新訓練。ViNG 讓學習的部分保持精簡：它學習兩個觀測之間相距多遠，以及如何朝附近的觀測移動；另外用過去觀測組成的圖來決定通往目標影像的路線。作者報告，此系統能在真實的戶外環境中運作，並能抵達超過 40 公尺遠的目標，而論文中沒有任何基線做到這一點（Shah et al., 2021）。

## 問題

要導航到以影像指定的目標，系統必須回答兩個問題：環境中哪些地點相連，以及如何從一個地點移動到下一個。度量建圖以幾何回答這兩個問題，但在沒有結構的環境中很脆弱。然而，單一的端到端策略在測試時很難改變方向。

## 核心想法

以學習得到的距離函數為觀測圖加權，並讓圖搜尋選出路線。接著由學習得到的位姿預測器與傳統控制器，驅動機器人前往該路線上的下一個路點。論文的消融實驗檢驗了三個設計選擇：以路點而非直接動作作為輸出、修剪容易通行的邊，以及只用正例配對訓練。

## 方程式或演算法

系統有三個組成部分：

1. **時間距離函數。** 輸入兩個觀測，每個觀測是兩張 160 × 120 像素影格堆疊而成，估計它們之間的時間步數。以 MobileNet 編碼器接三個全連接層，輸出 50 個區間上的分布，以交叉熵訓練。
2. **相對位姿預測器。** 使用相同的編碼器設計，從里程計推導出的位姿迴歸水平與垂直方向的相對路點偏移，以 L2 損失訓練。
3. **控制器。** 比例-微分控制器使用預測的偏移，驅動機器人朝向目前的路點。它輸出連續的線速度與角速度，本身不是學習得到的。

圖由離線觀測建立，節點是影像，沒有幾何座標。邊以距離函數加權。估計可通行程度低於稀疏門檻的邊會被丟棄。測試時，目前的影像與目標影像被加入圖中，並連接到最容易通行的鄰近節點，接著以加權的 Dijkstra 搜尋找出最短路徑。機器人則朝路徑上的下一個節點移動。

## 結果

在真實世界的試驗中，作者報告最困難任務的成功率為 86%。ViNG 是論文中唯一能抵達超過 40 公尺遠目標的方法。這些試驗的基線見論文的圖 3（Shah et al., 2021）。

消融實驗在 50 公尺的目標距離下報告（Table II）。時間差分變體的路點方法得分為 0.87，基本的路點方法為 0.81。以離散輸出的路點方法得分為 0.70。直接預測動作得分為 0.40，其離散版本得分為 0.45。移除圖修剪則降至 0.52，只用正例配對訓練得分為 0.43。

在四個新的戶外場地（兵營、工業區、公園與高草區）上，經微調的 ViNG 得分為 0.96、0.84、0.82 與 0.79。在相同場地上，經微調的 SPTM 得分為 0.74、0.68、0.71 與 0.56。

## 限制

- 規劃器在靜態的離線觀測資料集上運作，作者將此列為方法的限制。
- 尚不能處理光線與動態物體等非平穩變化。作者把穩健的表示列為未來工作。
- 論文中的控制器是人工設計的。學習的部分不涵蓋控制，因此控制器的行為並非從同一份資料學得。

## 相關連結

- [SPTM](sptm.md) 是 ViNG 所延續的記憶方法。ViNG 以學習得到的距離函數取代其檢索網路。
- [GNM](gnm.md) 與 [ViNT](vint.md) 是較晚的學習策略，以影像輸入預測未來的運動，目標以影像給定。
- [視覺教導與重播](visual-teach-and-repeat.md) 是經典的路線跟隨方法，不需要學習得到的距離。

## 開放問題

- 圖能否在機器人探索時線上擴充，而不是只由離線資料建立。
- 當蒐集與部署之間的光線和外觀改變時，如何讓距離估計保持可靠。

## 參考文獻

- Shah, D., Eysenbach, B., Kahn, G., Rhinehart, N. & Levine, S. (2021). *ViNG: Learning Open-World Navigation with Visual Goals*. ICRA 2021. https://doi.org/10.1109/ICRA48506.2021.9561936；預印本 https://arxiv.org/abs/2012.09812 — 距離函數、圖方法、消融實驗與真實世界結果的來源。
- Savinov, N., Dosovitskiy, A. & Koltun, V. (2018). *Semi-parametric Topological Memory for Navigation*. arXiv. https://arxiv.org/abs/1803.00653 — ViNG 所延續的拓撲記憶，也是真實世界試驗中比較的基線。
- Shah, D., Sridhar, A., Bhorkar, A., Hirose, N. & Levine, S. (2022). *GNM: A General Navigation Model to Drive Any Robot*. arXiv. https://arxiv.org/abs/2210.03370 — 較晚的模型，以跨機器人共享的策略與路點輸出為主。
- Shah, D., Sridhar, A., Dashora, N., Stachowicz, K., Black, K., Hirose, N. & Levine, S. (2023). *ViNT: A Foundation Model for Visual Navigation*. arXiv. https://arxiv.org/abs/2306.14846 — 以圖進行子目標選擇的 Transformer 後繼模型。
- Furgale, P. & Barfoot, T. D. (2010). *Visual teach and repeat for long-range rover autonomy*. Journal of Field Robotics, 27(5), 534–560. https://doi.org/10.1002/rob.20342 — 基於圖的學習方法所推廣的經典路線跟隨方法。
