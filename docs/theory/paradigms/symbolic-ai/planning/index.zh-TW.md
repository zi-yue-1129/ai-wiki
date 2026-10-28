---
translation_reviewed: 2026-10-28
---

# 自動規劃

自動規劃是找出一串動作，使智能體從初始狀態到達目標狀態的任務。規劃器以動作的描述為基礎，包括各動作的前置條件與效果。本頁是[符號 AI、搜尋與規劃](../index.md)的一部分。

## 概述

規劃問題指定初始狀態、目標，以及一組動作模式。每個動作只有在其前置條件成立時才能套用，並透過效果改變狀態。規劃器在狀態空間或部分計畫的空間中搜尋，找出通往目標的路徑。古典規劃假設世界完全已知且具確定性，後來也擴展到不確定與階層式的情境。

古典規劃的標準建模語言是 PDDL（Planning Domain Definition Language），它源自 STRIPS 表示法。以下兩種方法各有專頁。

## 關鍵概念

- **狀態**：某一時刻成立的事實集合。在古典規劃中，狀態是基底原子的集合。
- **動作模式**：具前置條件、新增效果與刪除效果的模板。
- **計畫**：一串動作，能把初始狀態轉換為滿足目標的狀態。
- **啟發式**：對仍需多少動作的估計。好的啟發式（常由鬆弛問題導出）使搜尋變得實用（Bonet 與 Geffner，2001）。

## 運作方式

多數規劃器採用搜尋。前向規劃器從初始狀態出發，展開前置條件成立的動作，並以啟發式引導搜尋。後向規劃器則從目標出發，透過動作進行回推。以圖為基礎的規劃器先建立一個緊湊的分層結構，再從中抽出計畫。表示法與搜尋策略的選擇，大致決定規劃器的效能。

## 主要方法

- [STRIPS](strips.md)：以前置條件、新增表與刪除表表示動作的原始表示法，也是 PDDL 的基礎。
- [GraphPlan](graphplan.md)：建立分層的規劃圖，並帶有互斥資訊，然後從後向前在圖上搜尋計畫。

文獻中其他的規劃方法包括把規劃視為啟發式搜尋（Bonet 與 Geffner，2001），以及把任務分解為子任務的階層任務網路規劃。這些方法在此僅作摘要，沒有各自的頁面。

## 不確定下的規劃

當動作具隨機性或觀測不完整時，規劃就成為決策問題。馬可夫決策過程（MDP）描述完全可觀測的隨機情境，部分可觀測 MDP（POMDP）則處理隱藏狀態。Kaelbling 等人（1998）給出了規劃與行動中 POMDP 的標準表述。[強化學習](../../reinforcement-learning/index.md)範式則以學習而非既定模型來處理同類問題。

## 與其他頁面的連結

- [搜尋演算法](../search/index.md)提供多數規劃器所用的搜尋方法，例如搭配規劃啟發式的 A\*。
- [機率方法](../../probabilistic/index.md)涵蓋不確定下規劃所需的不確定性模型。
- [強化學習](../../reinforcement-learning/index.md)以學得的價值或策略解決序列決策問題。

## 應用

- **物流**：在固定規則下排程配送與運輸。
- **太空任務與機器人**：自主太空船與機器人，自行選擇動作順序（Kaelbling 等人，1998）。
- **製造與工作流程**：產生符合資源與順序限制的製程計畫。

## 開放問題

- 與領域無關的規劃器仍需要領域相關的協助才能擴展。從範例學習有用的啟發式或控制知識，是活躍的研究方向。
- 把規劃模型與學得的感知和語言模型結合，並檢驗所得計畫的正確性，仍然困難。
- 階層式與不確定的規劃比古典規劃困難，通用而有效率的方法仍然有限。

## 參考文獻

### 奠基性論文

- Fikes, R. E. & Nilsson, N. J. (1971). STRIPS: A new approach to the application of theorem proving to problem solving. *Artificial Intelligence* 2(3–4), 189–208. https://doi.org/10.1016/0004-3702(71)90010-5 — 提出 STRIPS 動作表示法及建立於其上的規劃器。
- Blum, A. L. & Furst, M. L. (1997). Fast planning through planning graph analysis. *Artificial Intelligence* 90(1–2), 281–300. https://doi.org/10.1016/S0004-3702(96)00047-1 — 提出 GraphPlan，一種基於規劃圖的方法，在基準問題上明顯快於早期規劃器。
- Bonet, B. & Geffner, H. (2001). Planning as heuristic search. *Artificial Intelligence* 129(1–2), 5–33. https://doi.org/10.1016/S0004-3702(01)00108-4 — 把古典規劃視為啟發式搜尋，並研究由鬆弛問題導出的啟發式。
- Kaelbling, L. P., Littman, M. L. & Cassandra, A. R. (1998). Planning and acting in partially observable stochastic domains. *Artificial Intelligence* 101(1–2), 99–134. https://doi.org/10.1016/S0004-3702(98)00023-X — 以 POMDP 描述部分可觀測下的規劃與行動。

### 綜述與教科書

- Helmert, M. (2006). The Fast Downward planning system. *Journal of Artificial Intelligence Research* 26, 191–246. https://doi.org/10.1613/jair.1705 — 一套廣為使用、建立於啟發式搜尋之上的古典規劃器。
- Russell, S. & Norvig, P. *Artificial Intelligence: A Modern Approach*, 4th ed. Pearson. http://aima.cs.berkeley.edu/ — 教科書對古典規劃、規劃圖與不確定下規劃的說明。
