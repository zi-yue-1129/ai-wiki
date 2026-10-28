---
translation_reviewed: 2026-10-28
related:
  - applications/robotics
  - theory/models/world-models
  - theory/paradigms/imitation
tags:
  - robotics
  - navigation
  - visual navigation
  - image goals
aliases:
  - Visual navigation
  - Image-goal navigation
  - 視覺導航
---

# 以視覺目標導航

機器人可以用幾種方式被告知要去哪裡：地圖上的座標、語言指令，或展示一張目的地的影像。本子主題處理最後一種情況，也就是只靠相機影像（目標或路上的路標）來指定目的地。這裡交會兩條路線。視覺教學與重播是經典版本，機器人先走一遍路線，之後再重播。以影像為目標的學習導航則把這個想法推廣：用影像的拓撲記憶，加上在大量機器人行駛資料上訓練的策略。

## 概述

典型的學習系統把儲存的影像組成一張圖，在空間或時間上接近的影格之間連邊。要前往目標時，它在圖上找一條路徑，把下一張影像當作子目標，並輸出一個讓機器人朝該影像移動的動作。依方法不同，策略可以預測離散動作、相對路標、速度，或動作序列的分布。

視覺教學與重播完全不用學習的策略。它以里程計或重播的運動曲線追蹤教過的路線，並用影像修正航向。學習方法則以網路取代追蹤器，並用圖來決定下一步往哪裡去。

## 關鍵方法

每個方法都有自己的頁面。此處的概述與比較只是簡短的整理。

| 方法 | 策略的輸出 | 記憶 | 改變的部分 |
|---|---|---|---|
| [視覺教學與重播](visual-teach-and-repeat.md)（經典） | 以橫向與航向誤差做路徑追蹤 | 教過的路線，以局部子地圖或關鍵影格儲存 | 以相對於儲存路線的有正負號誤差轉向，沒有學習的策略 |
| [SPTM](sptm.md)（Savinov 等人，2018） | 七個離散動作之一 | 影格組成的拓撲圖，含視覺捷徑 | 學習的檢索網路做定位，以及離散的移動網路 |
| [ViNG](ving.md)（Shah 等人，2021） | 到路標的相對位姿，搭配人工設計的控制器 | 由離線觀測建立的圖，以學習得到的時間距離加權 | 學習的距離用於圖搜尋，以及學習的位姿預測器 |
| [GNM](gnm.md)（Shah 等人，2022） | 正規化後的路標 | 跨機器人與資料集共用的一個模型 | 論文中與速度輸出做比較的路標輸出 |
| [ViNT](vint.md)（Shah 等人，2023） | 五個未來路標與時間距離 | 擴散模型提出的子目標，以類 A* 方法搜尋 | 約 3,100 萬參數的 Transformer，只需少量資料即可適應 |
| [NoMaD](nomad.md)（Sridhar 等人，2023） | 從擴散模型取樣的動作序列 | 目標遮罩，因此同一模型在沒有目標時也能探索 | 同一策略同時支援以目標為條件的導航與無方向探索 |

各列的差異在於策略輸出什麼，而有比較輸出空間的論文報告了以下結果。在 ViNG 中，在 50 公尺的目標距離下，預測路標得分 0.81，離散動作得分 0.70（Shah 等人，2021，Table II）。在 GNM 中，LoCoBot 在簡單與中等設定下，正規化路標得分 1.00 與 0.95，速度輸出則為 0.73 與 0.54（Shah 等人，2022，Table V）。這些比較只在各自的論文內部、針對不同任務進行，因此不應被讀成單一排名。

Hirose 等人（2019）採取另一條路線。他們的模型 PoliNet 是一個視覺的模型預測控制策略。它以視覺軌跡與目前的視野為輸入，輸出規劃時域內的速度指令，並在執行時避開訓練時未見過的物體。其摘要以建圖與定位為對照來描述問題，而較新的方法則避開了這兩者。用學習得到的預測模型做規劃的一般概念，見[世界模型](../../../theory/models/world-models/index.md)子主題。

## 相關主題

- [機器人](../index.md) 把導航放在本站其他機器人任務之中。
- [行為克隆](../../../theory/paradigms/imitation/behavioural-cloning/index.md) 是大多數學習導航策略的訓練設定。
- [世界模型](../../../theory/models/world-models/index.md) 涵蓋其中一些方法用來規劃的預測模型。

## 開放問題

- 像 GNM 與 ViNT 那樣跨機器人共用一個模型，能否轉移到動力學差異很大的平台，例如空中與足式機器人。
- 只由一次行走建立的圖，在環境改變時表現如何，這正是經典視覺教學與重播所面對的情境。

## 參考文獻

- Furgale, P., & Barfoot, T. D. (2010). *Visual teach and repeat for long-range rover autonomy*. Journal of Field Robotics, 27(5), 534–560. https://doi.org/10.1002/rob.20342 — 典型的拓撲式視覺教學與重播系統，以里程計與子地圖為基礎。
- Savinov, N., Dosovitskiy, A., & Koltun, V. (2018). *Semi-parametric Topological Memory for Navigation*. arXiv. https://arxiv.org/abs/1803.00653 — 提出拓撲影像記憶與學習的移動網路。
- Shah, D., Eysenbach, B., Kahn, G., Rhinehart, N., & Levine, S. (2021). *ViNG: Learning Open-World Navigation with Visual Goals*. ICRA 2021. https://doi.org/10.1109/ICRA48506.2021.9561936 — 學習時間距離與相對位姿，用於以影像為目標的導航。
- Shah, D., Sridhar, A., Bhorkar, A., Hirose, N., & Levine, S. (2022). *GNM: A General Navigation Model to Drive Any Robot*. arXiv. https://arxiv.org/abs/2210.03370 — 在多台機器人上訓練一個導航模型，並比較輸出空間。
- Shah, D., Sridhar, A., Dashora, N., Stachowicz, K., Black, K., Hirose, N., & Levine, S. (2023). *ViNT: A Foundation Model for Visual Navigation*. arXiv. https://arxiv.org/abs/2306.14846 — 用於視覺導航的 Transformer 基礎模型，搭配擴散子目標提案。
- Sridhar, A., Shah, D., Glossop, C., & Levine, S. (2023). *NoMaD: Goal Masked Diffusion Policies for Navigation and Exploration*. arXiv. https://arxiv.org/abs/2310.07896 — 以目標遮罩擴散策略做以目標為條件的導航與探索。
- Hirose, N., Xia, F., Martín-Martín, R., Sadeghian, A., & Savarese, S. (2019). *Deep Visual MPC-Policy Learning for Navigation*. IEEE Robotics and Automation Letters, 4(4), 3184–3191. https://doi.org/10.1109/LRA.2019.2925731 — 視覺模型預測策略（PoliNet），跟隨視覺軌跡並避開未見過的障礙物。
