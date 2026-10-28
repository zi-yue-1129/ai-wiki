---
translation_reviewed: 2026-10-28
related:
  - applications/robotics/navigation
tags:
  - robotics
  - navigation
  - teach and repeat
  - visual odometry
aliases:
  - Visual teach and repeat
  - VT&R
  - 視覺教學與重播
---

# 視覺教學與重播

視覺教學與重播（VT&R）是一族方法：機器人先在人工操控下沿著一條路線行駛，並記下所見的內容；之後它自行沿同一條路線行駛，方法是把目前的相機畫面與儲存的畫面做比對。Furgale 與 Barfoot（2010）給出這個方法的典型拓撲式形式。上層子主題是[以視覺目標導航](index.md)。

## 概述

儲存的路線是一串局部子地圖或關鍵影格，彼此以相對變換相連。機器人對這條鏈上鄰近的部分做定位，並轉向以跟隨教過的路徑。由於誤差是相對於儲存的路線測量的，此方法不需要 GPS 或全域地圖座標系。

## 問題

路線可能很長，而教學行駛與重播之間，環境會改變。機器人必須準確地跟隨教過的路徑、避免位置估計漂移，並能應付光照與外觀的變化。拓撲式地圖的作法，是在不需要全域一致度量地圖的前提下，把局部誤差維持在小範圍內。

## 核心想法

以教學資料做相對定位，並用有正負號的誤差來轉向。Furgale 與 Barfoot 對重疊的子地圖做定位，並以路徑追蹤控制器依橫向與航向誤差來控制機器人。Krajník 與同事則採取較簡單的路線。在他們 2017 年的形式中，機器人依行駛距離重播教學時記錄的速度，只用相機來修正航向。其摘要報告，所得誤差在整條路線上不會發散。

## 方程式或演算法

核心量是機器人相對於教過路徑的橫向偏移與航向誤差，兩者都以儲存的資料測量。接著由控制器減少這些誤差。論文給出確切的控制律，本頁不重現。

重播的變體流程如下：

1. 教學時，記錄沿路線的影像與運動。
2. 重播時，依行駛距離重播記錄的速度。
3. 以影像估計航向修正量，並套用到重播的運動上。

Krajník 2010 的只用方位方法，儲存地點與其方位的地圖，並在由里程計定義的段落端點之間移動。Dall'Osto 等人（2020）描述一種以里程計為基礎的非同步教學與重播形式。

## 結果

論文報告的是實地測試，具體數字在重用前應先在原始文獻中核對。Furgale 與 Barfoot 報告了漫遊車上的長距離實地測試。Krajník 等人（2017）在其摘要中報告，重播學到的速度並以相機修正航向，可使誤差不再發散。Rozsypálek 等人（2023）報告了在環境變化下長期重播的結果，這正是其多維粒子濾波器的主要應用情境。

## 限制

- 里程計的漂移隨距離增長，因此系統依賴可靠的距離估計來決定何時轉彎。
- 急轉彎或缺乏紋理的區域，影像特徵可能遺失，這也是為何重播運動曲線常與視覺並用。
- 單次行走只儲存一種外觀。要跨光照與季節長期使用，需要能容忍變化的濾波或配準，這正是 Rozsypálek 等人（2023）的重點。

## 變體

- **拓撲式子地圖教學與重播**（Furgale 與 Barfoot，2010）：局部子地圖以相對變換相連，並以度量誤差做路徑追蹤。
- **只用方位的教學與重播**（Krajník 等人，2010）：方位地圖，段落端點由里程計定義。
- **以視覺航向修正的重播**（Krajník 等人，2017）：依距離重播教過的速度，並由相機修正航向。
- **以里程計為基礎的非同步教學與重播**（Dall'Osto 等人，2020）：以里程計為基礎的非同步形式。
- **長期重播的多維粒子濾波器**（Rozsypálek 等人，2023）：在變化條件下進行濾波。

## 相關主題

- [以視覺目標導航](index.md) 把視覺教學與重播和學習的影像目標導航放在一起比較。
- [SPTM](sptm.md) 是學習式的拓撲替代方案，以網路取代里程計追蹤器。
- [ViNG](ving.md) 學習距離與位姿，這些量在視覺教學與重播中原本由里程計計算。

## 開放問題

- 在教學與重播之間發生的環境變化（超出小幅外觀改變的範圍），教學與重播應如何處理。
- 學習的影像配準在超長路線上，能否達到幾何定位的精度。

## 參考文獻

- Furgale, P., & Barfoot, T. D. (2010). *Visual teach and repeat for long-range rover autonomy*. Journal of Field Robotics, 27(5), 534–560. https://doi.org/10.1002/rob.20342 — 典型的拓撲式視覺教學與重播系統，以里程計與子地圖為基礎。
- Krajník, T., Faigl, J., Vonásek, V., Košnar, K., Kulich, M., & Přeučil, L. (2010). *Simple yet stable bearing-only navigation*. Journal of Field Robotics, 27(5), 511–533. https://doi.org/10.1002/rob.20354 — 只用方位的地圖與重播，段落端點由里程計定義。
- Krajník, T., Majer, F., Halodová, L., & Vintr, T. (2017). *Navigation without localisation: reliable teach and repeat based on the convergence theorem*. arXiv. https://arxiv.org/abs/1711.05348 — 重播學到的速度，並以相機修正航向。
- Dall'Osto, D., Fischer, T., & Milford, M. (2020). *Fast and Robust Bio-inspired Teach and Repeat Navigation*. arXiv. https://arxiv.org/abs/2010.11326 — 以里程計驅動的非同步教學與重播形式。
- Rozsypálek, Z., Rouček, T., Vintr, T., & Krajník, T. (2023). *Multidimensional Particle Filter for Long-Term Visual Teach and Repeat in Changing Environments*. IEEE Robotics and Automation Letters, 8(4), 1951–1958. https://doi.org/10.1109/LRA.2023.3244418 — 用於變化環境中長期重播的濾波器。
