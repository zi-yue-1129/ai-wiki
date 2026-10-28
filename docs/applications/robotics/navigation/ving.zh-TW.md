---
translation_reviewed: 2026-10-28
tags:
  - robotics
  - navigation
  - temporal distance
aliases:
  - ViNG
  - Visual navigation with visual goals
  - 以視覺目標導航
---

# ViNG

ViNG 由 Shah、Eysenbach、Kahn、Rhinehart 與 Levine（2021）提出，它學習如何朝向目標影像導航，所用的是離線收集影像組成的圖。兩個學習得到的輸出頭負責主要工作：一個預測兩張影像之間的時間距離，用來在圖上規劃；另一個預測到附近路標的相對位姿，由控制器跟隨。上層子主題是[以視覺目標導航](index.md)。

## 概述

ViNG 從離線行駛資料建立拓撲圖，節點是影像，時間距離短的地方才連邊。時間距離頭估計兩張影像之間相隔幾步，用來判斷哪些邊是合理的。路徑規劃完成後，位姿頭預測到下一個路標的相對位移，比例微分控制器再帶動機器人朝該路標前進。

## 問題

較早的拓撲系統必須從離散方向中決定下一步，當目標很遠或圖很稀疏時表現不佳。論文探討：學習得到的時間距離能否在圖上規劃，以及對控制而言，回歸連續的路標是否優於選擇離散指令。

## 核心想法

把規劃與控制分開。規劃使用學習得到的時間距離，在圖上選出一條路徑。控制則使用回歸頭，輸出到下一個路標的相對位姿。圖的修剪會移除時間距離模型認為太長的邊，使規劃保持可靠。

## 運作方式

1. 收集離線行駛資料，建立以影像為節點、以相鄰影格為邊的圖。
2. 以影像對訓練時間距離頭，分類兩者相隔的步數，負樣本取自較遠的影格。
3. 訓練位姿頭，從目前影像與路標影像預測路標的相對位置。
4. 執行時，在修剪後的圖上找到通往目標影像的最短路徑，並以位姿頭與比例微分控制器跟隨。

## 結果

論文報告了在戶外小型輪式機器人上的真實機器人實驗，圖由約四十小時的離線資料建立。作者報告，回歸到路標的相對位姿優於在離散方向中做選擇，且圖的修剪對成功率很重要。確切的成功率取決於目標的距離，應在論文表格中核對。

## 限制

- 建立圖需要涵蓋環境的大型離線資料集，而且圖不會自行適應新區域。
- 時間距離是在訓練分布上學得的，外觀改變很大時可能不準確。
- 控制器是簡單的比例微分追蹤器，因此結果依賴機器人動力學與資料中的相近。

## 相關主題

- [SPTM](sptm.md) 提出 ViNG 所延伸的拓撲記憶，其輸出是離散動作。
- [GNM](gnm.md) 與 [ViNT](vint.md) 把同樣的想法延伸到多台機器人與更大的訓練集。
- [以視覺目標導航](index.md) 比較這些方法的輸出空間。

## 開放問題

- 如何在不從頭重新訓練時間距離模型的情況下，把新環境加入圖中。
- 時間距離能否跨建築物、天氣與季節泛化。

## 參考文獻

- Shah, D., Eysenbach, B., Kahn, G., Rhinehart, N., & Levine, S. (2021). *ViNG: Learning open-world navigation with visual goals*. ICRA 2021. https://doi.org/10.1109/ICRA48506.2021.9561936 — 時間距離與相對位姿兩個頭的來源。
- Savinov, N., Dosovitskiy, A., & Koltun, V. (2018). *Semi-parametric topological memory for navigation*. ICLR 2018. arXiv:1803.00653. https://arxiv.org/abs/1803.00653 — ViNG 所延伸的拓撲記憶。
- Shah, D., Sridhar, A., Bhorkar, A., Hirose, N., & Levine, S. (2023). *GNM: A general navigation model to drive any robot*. ICRA 2023. arXiv:2210.03370. https://arxiv.org/abs/2210.03370 — 在多台機器人上訓練的共用模型，並比較輸出空間。
- Shah, D., Sridhar, A., Dashora, N., Stachowicz, K., Black, K., Hirose, N., & Levine, S. (2023). *ViNT: A foundation model for visual navigation*. CoRL 2023. arXiv:2306.14846. https://arxiv.org/abs/2306.14846 — 預測時間距離與路標的較大型後繼方法。
- Codevilla, F., Santana, E., López, A. M., & Gaidon, A. (2019). *Exploring the limitations of behavior cloning for autonomous driving*. ICCV 2019. arXiv:1904.08980. https://arxiv.org/abs/1904.08980 — 記錄行為克隆的失敗模式，與學習導航相關。
