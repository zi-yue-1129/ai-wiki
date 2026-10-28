---
translation_reviewed: 2026-10-28
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

典型的學習系統把儲存的影像組成一張圖，在空間或時間上接近的影格之間連邊。要前往目標時，它在圖上找一條路徑，把下一張影像當作子目標，並輸出一個讓機器人朝該影像移動的動作。執行這件事的網路，可以預測速度、相對路標，或動作的分布。較早的系統從一小組離散指令中選擇，較新的則回歸連續運動。

視覺教學與重播不學習策略，而是用里程計追蹤教過的路線，並用影像修正航向。學習方法則以網路取代追蹤器，並用圖來決定下一步往哪裡去。

## 關鍵方法

每個方法都有自己的頁面。此處的概述與比較只是簡短的整理。

| 方法 | 策略的輸出 | 記憶 | 改變的部分 |
|---|---|---|---|
| [視覺教學與重播](visual-teach-and-repeat.md)（經典） | 以度量或里程計誤差做路徑追蹤 | 教過路線的影像 | 以有正負號的方位或橫向誤差轉向，而不是靠影像相似度 |
| [SPTM](sptm.md)（Savinov 等人，2018） | 由一對影像得到的離散動作 | 影格組成的拓撲圖 | 學習的定位與離散的行進分類器 |
| [ViNG](ving.md)（Shah 等人，2021） | 到路標的相對位姿 | 由離線資料建立的圖 | 用時間距離規劃，用位姿回歸控制 |
| [GNM](gnm.md)（Shah 等人，2023） | 正規化後的路標 | 跨機器人共用的模型 | 在急轉彎上，路標輸出優於速度輸出 |
| [ViNT](vint.md)（Shah 等人，2023） | 未來路標與時間距離 | 用 Dijkstra 選子目標的圖 | Transformer 基礎模型，只需少量資料即可適應 |
| [NoMaD](nomad.md)（Sridhar 等人，2023） | 從擴散模型取樣的動作序列 | 目標遮罩，因此同一策略也能探索 | 保留多種模式，例如路口的左轉與右轉 |

表格顯示一個趨勢：在同一任務上，回歸連續運動的系統通常勝過從離散指令中選擇的系統。Hirose 等人（2019）以另一種形式說明同樣的道理：在即時執行時，透過學習到的世界模型為候選動作打分，遠不如訓練一個策略去模仿被打分的行為。用學習到的預測模型做規劃，見[世界模型](../../../theory/models/world-models/index.md)子主題。

## 相關主題

- [機器人](../index.md) 把導航放在本站其他機器人任務之中。
- [行為克隆](../../../theory/paradigms/imitation/behavioural-cloning/index.md) 是大多數學習導航策略的訓練設定。
- [世界模型](../../../theory/models/world-models/index.md) 涵蓋其中一些方法用來規劃的預測模型。

## 開放問題

- 像 GNM 與 ViNT 那樣跨機器人共用一個模型，能否轉移到動力學差異很大的平台，例如空中與足式機器人。
- 只由一次行走建立的圖，在環境改變時表現如何，這正是經典視覺教學與重播所面對的情境。

## 參考文獻

- Furgale, P., & Barfoot, T. D. (2010). *Visual teach and repeat for long-range rover autonomy*. Journal of Field Robotics, 27(5), 534–560. https://doi.org/10.1002/rob.20342 — 典型的拓撲式教學與重播系統。
- Savinov, N., Dosovitskiy, A., & Koltun, V. (2018). *Semi-parametric topological memory for navigation*. ICLR 2018. arXiv:1803.00653. https://arxiv.org/abs/1803.00653 — 提出拓撲影像記憶與學習的移動網路。
- Shah, D., Eysenbach, B., Kahn, G., Rhinehart, N., & Levine, S. (2021). *ViNG: Learning open-world navigation with visual goals*. ICRA 2021. https://doi.org/10.1109/ICRA48506.2021.9561936 — 學習時間距離與相對位姿，用於以影像為目標的導航。
- Shah, D., Sridhar, A., Bhorkar, A., Hirose, N., & Levine, S. (2023). *GNM: A general navigation model to drive any robot*. ICRA 2023. arXiv:2210.03370. https://arxiv.org/abs/2210.03370 — 在多台機器人上訓練一個導航模型，並比較輸出空間。
- Shah, D., Sridhar, A., Dashora, N., Stachowicz, K., Black, K., Hirose, N., & Levine, S. (2023). *ViNT: A foundation model for visual navigation*. CoRL 2023. arXiv:2306.14846. https://arxiv.org/abs/2306.14846 — 以拓撲圖為輔的 Transformer 導航策略。
- Sridhar, A., Shah, D., Glossop, C., & Levine, S. (2023). *NoMaD: Goal masked diffusion policies for navigation and exploration*. arXiv:2310.07896. https://arxiv.org/abs/2310.07896 — 以目標遮罩擴散策略做以目標為條件的導航與探索。
- Hirose, N., Xia, F., Martín-Martín, R., Sadeghian, A., & Savarese, S. (2019). *Deep visual MPC-policy learning for navigation*. IEEE Robotics and Automation Letters, 4(4), 3184–3191. arXiv:1903.02749. https://arxiv.org/abs/1903.02749 — 比較對預測未來打分與把打分結果蒸餾成策略。
