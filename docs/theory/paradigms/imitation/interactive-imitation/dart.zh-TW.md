---
translation_reviewed: 2026-10-28
related:
  - theory/paradigms/imitation/behavioural-cloning
  - theory/paradigms/imitation/interactive-imitation/dagger.md
  - theory/paradigms/imitation/interactive-imitation
tags:
  - imitation learning
  - noise injection
  - robustness
aliases:
  - DART
  - 噪聲注入模仿學習
---

# DART（Noise Injection for Robust Imitation Learning）

DART 是一種模仿學習方法，讓專家示範中包含恢復行為。在收集示範時，它對實際執行的控制量加入雜訊，但記錄的標籤是專家未加雜訊的乾淨動作。因此資料涵蓋學習者可能漂移到的狀態，而且不需要線上專家去標註學習者自己的執行過程，這點與 [DAgger](dagger.md) 不同。此方法出自 Laskey、Lee、Fox、Dragan 與 Goldberg（2017），發表於第一屆機器人學習會議（CoRL 2017）。

## 概述

[行為克隆](../behavioural-cloning/index.md)只從專家造訪過的狀態學習。學習者一旦出錯，就會進入沒有訓練資料的狀態，誤差隨之累積。DAgger 透過在學習者自己的狀態上查詢專家來解決，但對人類而言往往成本高或不安全。DART 探討：能否把同樣的覆蓋範圍建立在示範之中，使專家只在前期需要參與。

## 核心概念

- **實際執行與記錄的動作**：機器人執行的是專家動作加上雜訊，而訓練標籤是專家的乾淨動作。學習者因此能看到專家在一個它自己不會到達的狀態上如何回應。
- **恢復資料**：被擾動的狀態與其乾淨標籤，展示了在出錯後如何回到專家的路徑。
- **雜訊大小**：依據目前學到的策略的誤差來設定，使被擾動的狀態接近學習者之後會造訪的狀態。論文的雜訊為高斯分布，其共變異數會縮放到預期的誤差水準 \(\alpha\)。

## 運作方式

令 \(\pi^*\) 為專家，\(x_t\) 為第 \(t\) 步的狀態。收集示範時，實際執行的控制量抽樣自

\[
u_t \sim \mathcal N\big(\pi^*(x_t), \Sigma\big),
\]

而記錄的訓練配對為 \((x_t, \pi^*(x_t))\)，標籤是乾淨的專家動作。共變異數 \(\Sigma\) 由目前學到的策略在其所到達的狀態上偏離專家的程度來估計，再縮放使其大小與最終策略的預期誤差 \(\alpha\) 相符。流程如下：

1. 以乾淨示範學習初始策略。
2. 以上述帶雜訊的執行控制收集示範，並依目前策略的偏離程度設定 \(\Sigma\)。
3. 記錄被擾動的狀態，並配對專家的乾淨動作。
4. 在合併後的資料上訓練策略，並隨策略改善更新雜訊大小。

示範收集完成後，不需要進一步查詢專家。

## 關鍵方法

### DART: Noise Injection for Robust Imitation Learning（Laskey 等人，2017）

- **問題：** 行為克隆在學習者偏離示範時會失敗，而 DAgger 的線上專家查詢成本高。論文探討能否離線收集恢復行為。
- **核心想法：** 在示範時擾動專家，以乾淨的專家動作為被擾動狀態加上標籤，並把擾動調整到學到的策略的誤差。
- **公式或演算法：** 執行控制 \(u_t\sim\mathcal N(\pi^*(x_t),\Sigma)\)，以 \(\pi^*(x_t)\) 為標籤，其中 \(\Sigma\) 由目前策略的偏離程度估計，並縮放到預期誤差 \(\alpha\)。此流程重複進行，雜訊在各輪之間更新。
- **結果：** 在 MuJoCo 模擬任務中，於高維的 Humanoid 任務上，DART 的計算時間約為 DAgger 的三分之一（摘要寫作「最多三倍快」）。訓練期間，專家的累積獎勵只下降 5%，而 DAgger 的策略獲得的累積獎勵比專家少約 80%。論文指出，DART 在各個領域都與 DAgger 持平。在實體實驗中，人類專家示範後，Toyota HSR 機器人在雜亂環境中抓取物體。DART 的成功率為 79%，行為克隆為 49%；摘要報告相較行為克隆平均提升 62%。
- **限制：** 雜訊大小必須調整。實驗只涵蓋一組 MuJoCo 任務與一個實體任務。專家必須能從被擾動的狀態恢復，而人類專家未必做得好。以雜訊獲得的覆蓋集中在專家軌跡附近，因此從遠離軌跡的狀態恢復並無保證。

## 關聯

DART 是 [DAgger](dagger.md) 的對應方法：兩者都處理共變量偏移，DAgger 透過在學習者的狀態上查詢專家，DART 則讓示範本身涵蓋這些狀態。兩者都屬於[互動式模仿](index.md)。注入雜訊是讓[行為克隆](../behavioural-cloning/index.md)更具穩健性的一種方式。DART 並不處理因果混淆，也就是學習者依賴了並非專家動作原因的特徵，見[因果混淆](../behavioural-cloning/causal-confusion.md)。

## 應用

機器人操作中，以遙控操作收集並加入受控雜訊的示範；駕駛或導航中，以擾動控制收集恢復示範。

## 開放問題

- 如何自動設定雜訊排程，而不是依賴人工選定的誤差水準 \(\alpha\)。
- 帶雜訊的示範能涵蓋多遠的狀態，才能覆蓋學習者只有在多次出錯後才會到達的狀態。
- 當人類專家的恢復動作並不完美時，此方法的效果如何。

## 參考文獻

### 奠基性論文

- Laskey, M.、Lee, J.、Fox, R.、Dragan, A. 與 Goldberg, K.（2017）. DART: Noise Injection for Robust Imitation Learning. CoRL 2017（第一屆機器人學習會議）. [arXiv:1703.09327](https://arxiv.org/abs/1703.09327) — 提出 DART，透過對示範注入雜訊來取得恢復行為，不需要線上查詢專家。
- Ross, S.、Gordon, G. J. 與 Bagnell, J. A.（2011）. A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning. AISTATS 2011, PMLR 15. [arXiv:1011.0686](https://arxiv.org/abs/1011.0686) — DAgger，是 DART 的線上替代方案，兩者在論文中被比較。
- Ross, S. 與 Bagnell, J. A.（2010）. Efficient Reductions for Imitation Learning. AISTATS 2010, PMLR 9. https://proceedings.mlr.press/v9/ross10a.html — 分析 DART 與 DAgger 都要解決的複合誤差。

### 綜述與教科書

- Osa, T. 等人（2018）. An Algorithmic Perspective on Imitation Learning. Foundations and Trends in Robotics. [arXiv:1811.06711](https://arxiv.org/abs/1811.06711) — 綜述，將基於雜訊的方法與線上互動方法放在模仿學習的脈絡中。

### 文章與預印本

- Kelly, M.、Sidrane, C.、Driggs-Campbell, K. 與 Kochenderfer, M. J.（2019）. HG-DAgger: Interactive Imitation Learning with Human Experts. ICRA 2019. [arXiv:1810.02890](https://arxiv.org/abs/1810.02890) — DAgger 的人類把關變體，與「互動式人類專家能提供多少」這個問題相關，可與離線的雜訊收集方式比較。
