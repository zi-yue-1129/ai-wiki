---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
tags:
- reinforcement learning
- memory
- sleep
aliases:
  - Experience Replay
  - Replay Buffer
  - 經驗回放
  - 經驗重播
  - 回放緩衝區
  - DQN Replay
---

# 經驗回放（Lin, 1992；Mnih 等人, 2015）

經驗回放把代理人過去的轉移儲存在緩衝區中，並在之後的學習更新中重複使用。它是標準的工程工具，也是本章中與海馬迴重播最接近的對應概念。

本頁是[睡眠、重播與記憶鞏固](../index.zh-TW.md)的一部分，比較此方法與海馬迴重播。演算法本身、各種變體及其取捨，見[經驗回放的理論頁](../../../theory/paradigms/reinforcement-learning/experience-replay/index.zh-TW.md)，此處不重複。

## 概述

若學習者只依發生順序使用每個新轉移一次，它看到的資料會高度相關，因為連續的步驟彼此相似。把轉移儲存在緩衝區中，並從中抽樣，能讓同一個經驗支持多次更新，也能把不同時間的樣本混合在一起。

## 問題

本章要問的是，大腦是否以類似方式重複利用近期經驗。海馬迴重播會在休息與睡眠期間重新活化近期序列，有時是反向的（見[海馬迴重播](../hippocampal-replay/index.zh-TW.md)）。

## 核心想法

每個轉移都以狀態、行動、獎勵與下一狀態的元組儲存。Lin（1992）把經驗回放列為加速強化學習的三種延伸之一（另兩者為規劃用的行動模型學習與教學），並在動態、非確定性的環境中評估。Mnih 等人（2015）在深度 Q 網路中保留近期經驗的重播記憶，並從中隨機抽樣。隨機抽樣能打破連續步驟之間的相關性。

大腦與演算法的比較在於結構。兩者都以不同於經驗發生時的順序，重複利用近期經驗。海馬迴重播在時間上是壓縮的，並與網路事件相連（見[尖波漣波](../sharp-wave-ripples/index.zh-TW.md)），而人工緩衝區則是以隨機方式抽樣的一般儲存。兩者的相似處在於原理，而非機制。

## 方程式或演算法

概括來說，代理人儲存每個轉移，從緩衝區抽取一個小批次，並依抽樣到的轉移更新其價值估計。精確的更新規則，見[經驗回放的理論頁](../../../theory/paradigms/reinforcement-learning/experience-replay/index.zh-TW.md)與[深度 Q 網路頁](../../../theory/paradigms/reinforcement-learning/deep-q-networks/index.zh-TW.md)。

## 結果

- Lin（1992）以動態、非確定性的環境對三種延伸進行實證評估。經驗回放是其中之一。
- Mnih 等人（2015）報告，使用回放的深度 Q 網路在一組遊戲上達到人類水準的控制。

深度 Q 網路的結果，是把回放與代理人的其他組成部分合併後的表現，因此無法單獨分離出回放的貢獻。

## 限制

- **記憶體成本。** 儲存原始畫面，尤其是影像，成本高昂，因此緩衝區大小會成為設計上的限制。
- **均勻抽樣會平均分配更新。** 代理人已能良好預測的轉移，與罕見或出乎意料的轉移，得到的更新次數相同。優先方法會改變這一點，理論頁有說明。
- **離策略偏差。** 儲存的轉移來自較舊的策略，因此由它們所做的更新，與依當前策略所做的更新不同。
- **證據範圍窄。** 深度 Q 網路的結果來自同一類遊戲。推廣到其他領域，需要另外的證據。
- **大腦類比僅具啟發性。** 與海馬迴重播的相似，是一個比較的起點，而非大腦使用此演算法的證據。

## 關聯

- **大腦。** [海馬迴重播](../hippocampal-replay/index.zh-TW.md)所述的海馬迴重播會重複使用近期序列，而逆向重播把結果連回先前的行動（Mattar 與 Daw, 2018）。記憶系統的說明見[互補學習系統](../../memory-learning/complementary-learning-systems/index.zh-TW.md)。
- **強化學習。** 演算法見[深度 Q 網路](../../../theory/paradigms/reinforcement-learning/deep-q-networks/index.zh-TW.md)，一般框架見[強化學習](../../../theory/paradigms/reinforcement-learning/index.zh-TW.md)。
- **持續學習。** 以重播舊資料來防止遺忘，使用的是同樣的緩衝區概念，見[持續學習中的重播與記憶](../../../theory/paradigms/continual/replay-and-memory/index.md)。

## 應用

- **遊戲與控制代理人。** 深度 Q 網路風格的代理人，使用重播緩衝區從儲存的經驗中學習。
- **持續學習。** 將舊資料與新資料交錯重新排練，是對抗災難性遺忘的常用基準。

## 未解問題

- **反轉重播的順序，對深度網路有幫助嗎？** 逆向重播是受大腦啟發的想法，其對大型網路的效益尚未確立。
- **效用規則能否推廣？** Mattar 與 Daw（2018）的效用解釋，是選擇哪些經驗進行重播的候選規則。它是否對深度網路有幫助，仍是開放問題。

## 參考文獻

### 奠基性論文

- Lin, L.-J. (1992). Self-improving reactive agents based on reinforcement learning, planning and teaching. *Machine Learning* 8, 293–321. https://doi.org/10.1007/BF00992699 — 把經驗回放列為加速強化學習的三種延伸之一（另兩者為規劃用的行動模型學習與教學），並在動態、非確定性的環境中評估。
- Mnih, V. 等人（2015）。Human-level control through deep reinforcement learning. *Nature* 518, 529–533. https://doi.org/10.1038/nature14236 — 深度 Q 網路，從近期經驗的重播記憶中隨機抽樣進行學習。
- Foster, D. J. & Wilson, M. A. (2006). Reverse replay of behavioural sequences in hippocampal place cells during the awake state. *Nature* 440, 680–683. https://doi.org/10.1038/nature04587 — 生物學上的對應：清醒大鼠跑動後休息期間，位置細胞序列的逆向重播。
- Mattar, M. G. & Daw, N. D. (2018). Prioritized memory access explains planning and hippocampal replay. *Nature Neuroscience* 21, 1609–1617. https://doi.org/10.1038/s41593-018-0232-z — 提出重播依效用排序的假說（效用指更新所帶來的額外獎勵），並重現向前與逆向重播。

### 綜述與教科書

- Wittkuhn, L. 等人（2021）。Replay in minds and machines. *Neuroscience & Biobehavioral Reviews* 129, 367–388. https://doi.org/10.1016/j.neubiorev.2021.08.002 — 回顧大腦與機器學習中的重播，並比較兩個領域。
