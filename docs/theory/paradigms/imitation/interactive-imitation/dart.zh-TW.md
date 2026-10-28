---
translation_reviewed: 2026-10-28
tags:
  - imitation learning
  - noise injection
  - robustness
aliases:
  - DART
  - 噪聲注入模仿學習
---

# DART（Noise Injection for Robust Imitation Learning）

DART 是一種模仿學習方法，讓專家示範中包含恢復行為。在記錄示範時，它對專家執行的動作注入雜訊，使資料涵蓋學習者可能漂移到的狀態。它不需要專家標註學習者自己的執行過程，這點與 [DAgger](dagger.md) 不同。

## 問題

[行為克隆](../behavioural-cloning/index.md)只從專家造訪過的狀態學習。學習者一旦出錯，就會進入沒有訓練資料的狀態，誤差隨之累積。DAgger 透過線上查詢專家來解決，但這往往成本高或不安全。DART 探討：能否在離線示範中就建立同樣的覆蓋範圍。

## 核心想法

收集示範時，對專家執行的動作加入雜訊，但記錄的標籤是專家未加雜訊的乾淨動作。學習者因此能看到專家如何從被擾動的狀態恢復。雜訊的大小依據目前策略的誤差來調整，使被擾動的狀態接近學習者之後會造訪的狀態。

## 演算法

1. 以乾淨示範的行為克隆得到初始策略。
2. 重複示範過程，在執行動作上加入雜訊，雜訊大小由目前策略的誤差決定。
3. 記錄被擾動的狀態，並配對專家未加雜訊的動作。
4. 在合併後的資料集上訓練策略。

示範收集完成後，此流程不需要線上查詢專家。

## 結果

Laskey 等人（2017）報告，在 MuJoCo 模擬任務中，DART 的計算時間最多可比 DAgger 減少三倍，而在 Humanoid 任務上專家的獎勵只下降約 5%。在實體抓取任務上，論文報告平均比行為克隆高出 62%。這些是作者報告的結果，重用前應先查證原論文。

## 限制

- **雜訊調整。** 雜訊大小必須小心選擇。雜訊太小不會產生恢復資料，太大則會讓資料遠離學習者實際造訪的狀態。
- **專家品質。** 專家必須能從被擾動的狀態恢復，但人類專家不一定做得到。
- **覆蓋範圍。** DART 涵蓋的是專家軌跡附近的狀態。從遠離軌跡的狀態恢復，並不能保證。

## 與其他主題的連結

DART 是 [DAgger](dagger.md) 的對應方法：兩者都處理共變量偏移，DAgger 透過在學習者的狀態上查詢專家，DART 則讓示範本身涵蓋這些狀態。兩者都屬於[互動式模仿](index.md)。注入擾動的想法在更廣泛的行為克隆穩健性研究中也會用到，見[行為克隆](../behavioural-cloning/index.md)。

## 應用

機器人操作中，以遙控操作收集並加入受控雜訊的示範；駕駛或導航中，以擾動控制收集恢復示範。

## 開放問題

如何自動設定雜訊排程，以及帶雜訊的示範能涵蓋多遠的狀態，才能覆蓋學習者只有在多次出錯後才會到達的狀態。

## 參考文獻

### 奠基性論文

- Laskey, M.、Lee, J.、Fox, R.、Dragan, A. 與 Goldberg, K.（2017）. *DART: Noise Injection for Robust Imitation Learning*. arXiv:1703.09327. https://arxiv.org/abs/1703.09327 — 提出 DART，透過對示範注入雜訊來取得恢復行為，不需要線上查詢專家。
- Ross, S.、Gordon, G. J. 與 Bagnell, J. A.（2011）. *A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning*. AISTATS 2011, PMLR 15:627–635. https://proceedings.mlr.press/v15/ross11a.html — DAgger，是 DART 的線上替代方案，兩者在論文中被比較。
- Ross, S. 與 Bagnell, J. A.（2010）. *Efficient Reductions for Imitation Learning*. AISTATS 2010, PMLR 9:661–668. https://proceedings.mlr.press/v9/ross10a.html — 分析 DART 與 DAgger 都要解決的複合誤差。

### 文章與預印本

- Kelly, M. 等人（2018）. *HG-DAgger: Interactive Imitation Learning with Human Experts*. arXiv:1810.02890. https://arxiv.org/abs/1810.02890 — 討論人類專家接管學習策略時的行為，與雜訊方法的專家品質限制相關。
- Wen, C. 等人（2020）. *Fighting Copycat Agents in Behavioral Cloning from Observation Histories*. arXiv:2010.14876. https://arxiv.org/abs/2010.14876 — 說明克隆策略可能複製前一個動作，這種失誤光靠示範覆蓋並不能解決。
