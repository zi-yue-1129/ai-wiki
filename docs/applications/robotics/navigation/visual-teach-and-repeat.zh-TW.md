---
translation_reviewed: 2026-10-28
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

儲存的路線是一串局部子地圖或關鍵影格，彼此以相對變換相連。機器人對最近的子地圖做定位，並以控制器追蹤路徑，控制器使用目前畫面的橫向與航向誤差。由於誤差是相對於儲存的地圖測量的，此方法不需要 GPS 或全域座標系。

## 問題

路線可能很長，而教學行駛與重播之間，環境會改變。機器人必須準確地跟隨教過的路徑、避免位置估計漂移，並能應付光照與外觀的變化。這些需求促成了拓撲式地圖：它能把局部誤差維持在小範圍內，而不需要全域一致的度量地圖。

## 核心想法

以教學資料做相對定位，並用有正負號的誤差來轉向。Furgale 與 Barfoot 對重疊的子地圖做定位，並以路徑追蹤控制器依度量的橫向與航向誤差來控制機器人。Krajník 與同事則採取較簡單的路線：依行駛距離重播教過的速度，並只用影像來修正航向。

## 運作方式

1. 教學時，沿路線記錄影像與相對運動，建立局部子地圖或關鍵影格鏈。
2. 重播時，以特徵比對估計機器人相對於最近儲存子地圖的位置。
3. 計算橫向與航向誤差，並轉向以減少誤差。
4. 在重播的變體中，依距離追蹤教過的運動曲線，並以影像估計的航向做修正。

## 結果

Furgale 與 Barfoot 報告了在漫遊車上的長距離實地測試，多次自主重播的總里程達數公里，且不使用 GPS。Krajník 等人（2010）報告，僅以方位的導航在超過一公里的路線上，平均位置誤差低於 0.3 公尺。Krajník 等人（2018）報告，只靠視覺修正航向無法跟隨急轉彎，因為特徵會離開視野；而重播教過的運動加上視覺修正，則能收斂到路徑上。數字在重用前應先在論文中核對。

## 限制

- 里程計的漂移隨距離增長，因此系統依賴可靠的距離估計來決定何時轉彎。
- 急轉彎或缺乏紋理的區域，影像特徵可能遺失，這也是為何重播運動曲線常與視覺並用。
- 單次行走只儲存一種外觀。要跨光照與季節長期使用，需要多次行走的資料或學習的影像配準，如 Rozsypálek 等人（2023）所示。

## 相關主題

- [以視覺目標導航](index.md) 把視覺教學與重播和學習的影像目標導航放在一起比較。
- [SPTM](sptm.md) 是學習式的拓撲替代方案，以網路取代里程計追蹤器。
- [機器人](../index.md) 涵蓋此局部定位與控制步驟背後更廣的估計與控制問題。

## 開放問題

- 在教學與重播之間發生的環境變化（超出小幅外觀改變的範圍），教學與重播應如何處理。
- 學習的影像配準在超長路線上，能否達到幾何定位的精度。

## 參考文獻

- Furgale, P., & Barfoot, T. D. (2010). *Visual teach and repeat for long-range rover autonomy*. Journal of Field Robotics, 27(5), 534–560. https://doi.org/10.1002/rob.20342 — 典型的拓撲式視覺教學與重播系統。
- Krajník, T., Faigl, J., Vonásek, V., Košnar, K., Kulich, M., & Přeučil, L. (2010). *Simple yet stable bearing-only navigation*. Journal of Field Robotics, 27(5), 511–533. https://doi.org/10.1002/rob.20354 — 只用方位的地圖與重播，並在里程計的段落端點轉彎。
- Krajník, T., Majer, F., Halodová, L., & Vintr, T. (2018). *Navigation without localisation: Reliable teach and repeat based on the convergence theorem*. IROS 2018. arXiv:1711.05348. https://arxiv.org/abs/1711.05348 — 重播教過的運動曲線，並以視覺修正。
- Dall'Osto, D., Fischer, T., & Milford, M. (2021). *Fast and robust bio-inspired teach and repeat navigation*. IROS 2021. arXiv:2010.11326. https://arxiv.org/abs/2010.11326 — 以里程計驅動的教學與重播，並分別做方向與沿路徑的修正。
- Rozsypálek, Z., Rouček, T., Vintr, T., & Krajník, T. (2023). *Multidimensional particle filter for long-term visual teach and repeat in changing environments*. IEEE Robotics and Automation Letters, 8, 1951–1958. https://doi.org/10.1109/LRA.2023.3244418 — 在環境改變下，對距離、橫向偏移與航向做聯合濾波。
