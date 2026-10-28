---
translation_reviewed: 2026-10-28
tags:
  - robotics
  - navigation
  - foundation model
  - transformer
aliases:
  - ViNT
  - Visual Navigation Transformer
  - 視覺導航 Transformer
---

# ViNT：視覺導航的基礎模型

ViNT 由 Shah、Sridhar、Dashora、Stachowicz、Black、Hirose 與 Levine（2023）提出，是一個在大量機器人導航資料集混合體上訓練的視覺導航 Transformer 策略。它根據過去的影格與目標影像，預測時間距離與一小段未來路標。一張儲存影像的拓撲圖提供子目標，之後策略可以用少量資料微調到新任務。上層子主題是[以視覺目標導航](index.md)。

## 概述

ViNT 有兩個部分。預訓練的 Transformer 把一小段影格歷史與目標一起編碼，兩個輸出頭分別產生時間距離估計與未來路標。執行時，在儲存影像的圖上搜尋路徑，把路徑上的下一個節點當作子目標，策略輸出的路標再由滾動視窗控制器跟隨。

## 問題

較早的導航策略只在一台機器人或一個環境上訓練，每換一個場景都需要大量新資料。論文探討：大規模且多樣的訓練資料，加上 Transformer 架構，能否得到一個只需少量額外資料就能轉移到新機器人與新任務的單一模型。

## 核心想法

同時擴大資料與模型，並預測對規劃與控制都有用的輸出。時間距離頭為圖上的規劃提供訊號，路標頭則提供控制訊號。模型在混合多台機器人的資料上訓練，論文認為這是廣泛泛化所必需的。

## 運作方式

1. 在來自不同機器人的導航資料集混合體上訓練 Transformer，預測時間距離與未來路標。
2. 為目標環境建立影像的拓撲圖，並在圖上搜尋通往目標的路徑。
3. 以路徑上的下一個節點作為子目標，用目前的影格歷史執行策略。
4. 以比例微分控制器跟隨預測的路標，並隨新影格到來重新規劃。
5. 適應新任務時，以少量任務資料微調。

## 結果

論文報告，模型以超過一百小時的資料訓練，約有三千一百萬參數；在作者的真實世界測試中，可在數百公尺到超過一公里的路線上導航。論文報告，以一到兩小時的資料適應新任務，成功率有明顯提升。隨機子目標選擇的消融顯示，以圖為基礎的子目標確實重要。確切數字應在論文表格中核對。

## 限制

- 模型很大，在小型車載電腦上執行需要不是每個平台都有的加速器。
- 只由一次行走建立的拓撲圖本質上近似一條鏈，子目標的選擇因此有限。
- 新任務的成功率取決於適應資料的數量與品質，論文只報告其自身設定的結果。

## 相關主題

- [GNM](gnm.md) 是前身，提出共用模型與正規化路標輸出。
- [NoMaD](nomad.md) 是後來的變體，使用擴散策略與目標遮罩。
- [ViNG](ving.md) 提供 ViNT 所用的時間距離與圖上規劃。

## 開放問題

- 單一基礎模型能涵蓋多大範圍、外觀與佈局差異很大的環境。
- 新任務所需的適應資料，能否透過在無標註影片上的自監督預訓練進一步減少。

## 參考文獻

- Shah, D., Sridhar, A., Dashora, N., Stachowicz, K., Black, K., Hirose, N., & Levine, S. (2023). *ViNT: A foundation model for visual navigation*. CoRL 2023. arXiv:2306.14846. https://arxiv.org/abs/2306.14846 — Transformer 策略、圖規劃與適應結果的來源。
- Shah, D., Sridhar, A., Bhorkar, A., Hirose, N., & Levine, S. (2023). *GNM: A general navigation model to drive any robot*. ICRA 2023. arXiv:2210.03370. https://arxiv.org/abs/2210.03370 — ViNT 所建立於其上的共用模型與輸出空間比較。
- Shah, D., Eysenbach, B., Kahn, G., Rhinehart, N., & Levine, S. (2021). *ViNG: Learning open-world navigation with visual goals*. ICRA 2021. https://doi.org/10.1109/ICRA48506.2021.9561936 — 時間距離與圖規劃的做法。
- Savinov, N., Dosovitskiy, A., & Koltun, V. (2018). *Semi-parametric topological memory for navigation*. ICLR 2018. arXiv:1803.00653. https://arxiv.org/abs/1803.00653 — 用於子目標選擇的拓撲記憶。
- Sridhar, A., Shah, D., Glossop, C., & Levine, S. (2023). *NoMaD: Goal masked diffusion policies for navigation and exploration*. arXiv:2310.07896. https://arxiv.org/abs/2310.07896 — 同一系列較後的策略。
