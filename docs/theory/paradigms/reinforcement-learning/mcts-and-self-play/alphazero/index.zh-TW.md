---
translation_reviewed: 2026-10-28
---

# AlphaZero（Silver 等人，2017）

AlphaZero 是一套單一的自我對弈演算法，僅憑規則、使用一個神經網路與[蒙地卡羅樹搜尋](../monte-carlo-tree-search/index.md)，即可學會西洋棋、將棋與圍棋。它以移除人類棋譜與圍棋專用設計的方式推廣了 [AlphaGo](../alphago/index.md)，是[上層主題](../index.md)中搜尋加自我對弈方法的參考設計。

## 概述

AlphaGo 需要人類專家棋譜來啟動策略網路，並依賴為圍棋設計的特徵。AlphaZero 的問題是：同一套程序能否從零開始學會多種遊戲，只需知道規則。作者對西洋棋、將棋與圍棋的回答都是肯定的。arXiv 摘要報告，AlphaZero 從隨機下棋開始，除了遊戲規則之外不給予任何領域知識，在 24 小時內便在這些遊戲中達到超人水準，並在每一種遊戲中明確擊敗了一個世界冠軍級的程式。

這個演算法後來發表於 Science（Silver 等人，2018）。它的關鍵簡化是把 AlphaGo 的策略網路與價值網路合併為一個有兩個輸出的網路，並且只用自己產生的對局資料來訓練它。

## 關鍵概念

- **單一網路**：輸入棋盤，輸出每個走法的機率（策略 $\mathbf{p}$），以及對結果的純量估計（價值 $v$）。
- **搜尋導向的目標**：搜尋的走法次數構成策略目標，通常比網路的原始輸出更銳利。
- **結果目標**：每一局自我對弈的最終結果，從該局面行棋方的觀點看，構成價值目標。
- **PUCT 選擇**：UCT 規則的一種變體，以網路的先驗 $P(s,a)$ 取代均勻的偏置項。

## 運作方式

每一局自我對弈的產生方式如下。在每個局面，MCTS 執行固定次數的模擬，並以網路提供先驗與葉節點價值。搜尋會回傳每個走法的造訪次數，再依此抽樣選出一步。每次模擬的選擇規則為

$$
a^\ast = \arg\max_a \left( Q(s,a) + c_{\text{puct}}\, P(s,a)\, \frac{\sqrt{\sum_b N(s,b)}}{1 + N(s,a)} \right),
$$

而網路的訓練目標是讓其價值輸出預測對局結果 $z$，讓其策略輸出預測搜尋分布 $\boldsymbol{\pi}$。損失函數的形式為

$$
\ell = (z - v)^2 - \boldsymbol{\pi}^\top \log \mathbf{p} + c\,\lVert\theta\rVert^2.
$$

訓練迴圈如下：

1. 以隨機權重初始化網路。
2. 與自己下一局，每一步都以目前的網路執行 MCTS。
3. 儲存每個局面、其搜尋分布 $\boldsymbol{\pi}$，以及最終結果 $z$。
4. 從近期的對局中抽樣局面，對損失函數做一次梯度更新。
5. 重複。更新後的網路引導下一局，搜尋也隨之改進。

由於產生對局的網路正是正在被訓練的網路，訓練資料的難度會隨學習者一起上升，資料與網路因此一起改進。

## 結果

根據 arXiv 摘要（Silver 等人，2017），AlphaZero 從隨機下棋學會了西洋棋與將棋，也學會了圍棋，並在 24 小時內在每一種遊戲中達到超人水準，在各種遊戲中都擊敗了世界冠軍級的程式。論文的比較對象是針對各遊戲所建構的強力程式，確切比分請見原論文。

## 限制

- **完全資訊**。這個方法是為確定性、雙人、零和且局面完全可見的遊戲設計的。
- **需要已知規則**。搜尋需要精確的模擬器，因此方法無法直接轉移到規則未知的任務。
- **運算需求**。自我對弈需要極大量的搜尋與訓練運算，限制了能重現結果的人數。

## 開放問題

這個方法能否推廣到不完全資訊的遊戲（例如撲克），或推廣到具有連續動作與未知動態的任務？[MuZero](../muzero/index.md)以學習模型回答了後者，前者在這一系列方法中仍未解決。另一個問題是如何把自我對弈用於語言模型，因為語言模型沒有明確的勝者。[Feng 等人（2023）](https://arxiv.org/abs/2309.17179)把 AlphaZero 的搜尋用於語言模型的解碼，但獎勵訊號遠不如遊戲那樣乾淨。

## 關聯

AlphaZero 建立在專家迭代（Anthony 等人，2017）之上，後者同樣在樹搜尋與模仿搜尋結果的學習策略之間交替進行；它也建立在 [AlphaGo](../alphago/index.md) 及其 Zero 變體之上。它的訓練使用與[價值基礎方法](../../value-based-methods/index.md)和[策略梯度方法](../../policy-gradient-and-actor-critic/index.md)相同的價值與策略學習。其後繼者 [MuZero](../muzero/index.md) 則不再需要規則。

## 參考文獻

### 開創性論文

- Silver, D. 等人 (2018). *A general reinforcement learning algorithm that masters chess, shogi, and Go through self-play*. Science. https://doi.org/10.1126/science.aar6404 — 經同儕審查的 AlphaZero 論文，單一套自我對弈加搜尋演算法僅憑規則即可學會三種棋類。
- Silver, D. 等人 (2017). *Mastering Chess and Shogi by Self-Play with a General Reinforcement Learning Algorithm*. arXiv:1712.01815. https://arxiv.org/abs/1712.01815 — AlphaZero 的預印本，包含單一網路設計與訓練結果的描述。
- Silver, D. 等人 (2017). *Mastering the game of Go without human knowledge*. Nature. https://doi.org/10.1038/nature24270 — AlphaGo Zero，移除人類棋譜的圍棋前身。
- Anthony, T., Tian, Z. & Barber, D. (2017). *Thinking Fast and Slow with Deep Learning and Tree Search*. arXiv:1705.08439. https://arxiv.org/abs/1705.08439 — 專家迭代，即 AlphaZero 所建立於其上的樹搜尋與策略學習循環。

### 文章與文件

- Feng, X. 等人 (2023). *Alphazero-like Tree-Search can Guide Large Language Model Decoding and Training*. arXiv:2309.17179. https://arxiv.org/abs/2309.17179 — 把類似 AlphaZero 的樹搜尋，以學得的價值函數應用於語言模型的解碼與訓練。
