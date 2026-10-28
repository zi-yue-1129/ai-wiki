---
translation_reviewed: 2026-10-28
tags:
  - robotics
  - navigation
  - topological memory
aliases:
  - SPTM
  - Semi-parametric topological memory
  - 半參數拓撲記憶
---

# 半參數拓撲記憶（SPTM）

SPTM 由 Savinov、Dosovitskiy 與 Koltun（2018）提出，它以一張儲存影像的圖來導航。學習得到的網路根據目前影像與圖上下一個路標影像，選出下一個動作。此方法在環境的一段短影片上訓練，不需要度量地圖。上層子主題是[以視覺目標導航](index.md)。

## 概述

SPTM 由三部分組成：以拓撲圖組織的影像記憶、把目前畫面定位到圖上的檢索步驟，以及輸出離散動作的行進網路。圖由單次行走建立，每個節點是一個影格。名稱的意思是：記憶以影像的形式非參數地儲存，而定位與行進則是學習得到的。

## 問題

從影像進行目標導向的導航，需要知道機器人在地圖上的位置，並選出能把它帶向目標的動作。早期的拓撲方法必須對每一幀從頭定位，在重複性高的環境中並不可靠，而且依賴人工設計的動作規則。論文探討：能否以自監督方式在儲存的影片上訓練行進模型，同時取代這兩者。

## 核心想法

從圖上選一個在機器人前方、且有高把握可達的路標。接著訓練行進網路，預測能把代理人從目前畫面帶向該路標畫面的動作。路標由可達性估計選出，因此前瞻的距離會依機器人有把握能走多遠而調整。

## 運作方式

1. 從環境的影片建立圖，把時間上相近的影格相連。
2. 把目前的觀測定位到圖上。先在上一個位置附近搜尋，只有失敗時才做全域搜尋。
3. 在有限的圖步數範圍內，選出可達性預測超過門檻、且最遠的路標。
4. 把目前影像與路標影像輸入行進網路，執行預測出的離散動作。

## 結果

作者報告，在使用約五分鐘影片的迷宮實驗中，SPTM 的成功率約為最佳基線的三倍。消融實驗顯示，時間上一致的定位優於逐幀獨立定位。實驗在以 DOOM 引擎建構的迷宮模擬中進行，因此原論文並未顯示真實機器人上的表現。

## 限制

- 動作空間是離散的，機器人只能以固定步幅轉向或前進。後續的方法顯示，連續輸出能更好地處理急轉彎。
- 定位取決於圖是否充分涵蓋環境，外觀相似的地點可能混淆檢索步驟。
- 原論文的評估是在模擬中進行，因此該論文沒有顯示真實機器人的行為。

## 相關主題

- [以視覺目標導航](index.md) 把 SPTM 放在後來的學習方法之中做比較。
- [ViNG](ving.md) 保留拓撲圖，但學習的是時間距離與連續的相對位姿。
- [視覺教學與重播](visual-teach-and-repeat.md) 是解決同一路線跟隨問題的經典方法。
- [Meng 等人（2020）](https://arxiv.org/abs/1909.12329) 透過回歸路標，把局部控制擴展到大型拓撲地圖。

## 開放問題

- 在長走廊與開放空間並存的真實環境中，如何選擇可達性門檻與前瞻視窗。
- 離散動作的策略能否在急轉彎時表現良好，同時保留其簡單性。

## 參考文獻

- Savinov, N., Dosovitskiy, A., & Koltun, V. (2018). *Semi-parametric topological memory for navigation*. ICLR 2018. arXiv:1803.00653. https://arxiv.org/abs/1803.00653 — 原始方法與其消融實驗。
- Meng, X., Ratliff, N., Xiang, Y., & Fox, D. (2020). *Scaling local control to large-scale topological navigation*. ICRA 2020. arXiv:1909.12329. https://arxiv.org/abs/1909.12329 — 比較拓撲地圖上直接控制回歸與路標回歸。
- Shah, D., Eysenbach, B., Kahn, G., Rhinehart, N., & Levine, S. (2021). *ViNG: Learning open-world navigation with visual goals*. ICRA 2021. https://doi.org/10.1109/ICRA48506.2021.9561936 — 學習時間距離與連續相對位姿的後繼方法。
- Shah, D., Sridhar, A., Dashora, N., Stachowicz, K., Black, K., Hirose, N., & Levine, S. (2023). *ViNT: A foundation model for visual navigation*. CoRL 2023. arXiv:2306.14846. https://arxiv.org/abs/2306.14846 — 保留拓撲圖的大規模後繼方法。
- Hirose, N., Xia, F., Martín-Martín, R., Sadeghian, A., & Savarese, S. (2019). *Deep visual MPC-policy learning for navigation*. IEEE Robotics and Automation Letters, 4(4), 3184–3191. arXiv:1903.02749. https://arxiv.org/abs/1903.02749 — 以影像子目標為對象的學習導航策略。
