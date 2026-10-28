---
translation_reviewed: 2026-10-28
aliases:
  - 端到端駕駛
  - End-to-end driving
---

# 從像素到方向盤的端到端學習（Bojarski 等人，2016）

Bojarski 等人（NVIDIA）訓練了一個卷積網路，把一支前方相機的原始像素直接映射為方向盤指令。網路從人類駕駛的錄影中學習，不需要手工設計的感知或規劃模組。本主題屬於[自動駕駛與運輸](../index.md)。

## 問題

自動駕駛系統通常由感知、規劃與控制等模組分別手工設計。問題在於：能否只用人類駕駛作為監督，讓單一網路學會從原始相機像素到轉向的整個映射？

## 核心想法

卷積網路接收一支前方相機的影像，輸出方向盤指令。因為它以人類駕駛的錄影訓練，場景與轉向之間的對應是學出來的，而不是寫死的。論文主張，這種極簡的監督已足以讓系統在多種情境下行駛。

## 程序

1. 記錄前方相機的影像，以及人類駕駛當時的轉向角度。
2. 訓練卷積網路，從每張影像預測轉向指令。
3. 在車上執行訓練好的網路，依即時相機畫面決定轉向。

## 結果

摘要指出，系統能在有或沒有車道線的一般道路、高速公路、停車場與未鋪裝道路上行駛，並報告以每秒 30 幀運作。摘要沒有給出安全性或錯誤率，這些需要查閱全文。

## 限制

- 摘要沒有說明網路為何選擇某個轉向指令，因此難以檢驗。
- 從人類駕駛學習，也意味著系統可能複製人類的錯誤。
- 網路只是從單一相機視角的一個映射。路線指令、試錯學習與模擬測試都由下方列出的後續研究處理。

## 連結

- 同樣的端到端思路也應用於機器人操作，見[用於抓取的手眼協調學習](../../robotics/hand-eye-grasping/index.md)。
- 從人類示範模仿，見[模仿學習](../../../theory/paradigms/imitation/index.md)。

## 參考文獻

### 開創性論文

- Bojarski, M. et al. (2016). End to End Learning for Self-Driving Cars. arXiv. https://arxiv.org/abs/1604.07316 — 卷積網路把一支前方相機的像素映射為轉向指令，以人類駕駛資料訓練。
- Codevilla, F. et al. (2018). End-to-end Driving via Conditional Imitation Learning. arXiv. https://arxiv.org/abs/1710.02410 — 以高層指令（例如路口要轉向哪一邊）條件化模仿學習的駕駛策略。
- Kendall, A. et al. (2018). Learning to Drive in a Day. arXiv. https://arxiv.org/abs/1807.00412 — 以深度強化學習做車道跟隨，在真實車輛上從單眼相機、數個回合內學會。
- Bansal, M., Krizhevsky, A. & Ogale, A. (2018). ChauffeurNet: Learning to Drive by Imitating the Best and Synthesizing the Worst. arXiv. https://arxiv.org/abs/1812.03079 — 以合成的擾動與碰撞懲罰強化模仿學習，使駕駛更穩健。

### 文章與文件

- Dosovitskiy, A. et al. (2017). CARLA: An Open Urban Driving Simulator. arXiv. https://arxiv.org/abs/1711.03938 — 開源的城市模擬器，提供城市佈局、車輛與可設定的感測器，用於訓練與測試駕駛系統。
