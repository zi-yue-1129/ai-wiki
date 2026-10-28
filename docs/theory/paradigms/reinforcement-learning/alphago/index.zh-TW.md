---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
  - applications/games
tags:
  - reinforcement learning
  - search
  - games
aliases:
  - AlphaGo
  - 阿爾法圍棋
---

# AlphaGo（Silver 等人，2016）

AlphaGo 是一套圍棋系統，結合深度神經網路與蒙地卡羅樹搜尋。2015 年 10 月，它擊敗歐洲圍棋冠軍樊麾，2016 年的《Nature》論文報告了這些結果。這是電腦程式首次在不讓子的對局中擊敗職業圍棋選手，而這在過去被認為是以搜尋為基礎的程式難以達到的目標。

## 問題

圍棋的合法局面數量遠多於西洋棋，而且很難僅憑計算子力或地盤來判斷局面的價值。早期程式依賴手工設計的評估函數，面對職業棋士時相當弱。這篇論文探討的問題是：學習得到的局面評估與落子選擇，加上搜尋，能否縮小這個差距。

## 關鍵概念

- **策略網路**：給定一個局面，輸出每個合法落點的機率。它提出值得考慮的著手。
- **價值網路**：給定一個局面，估計輪到的一方獲勝的機率。它不需要把棋下到底就能判斷局面。
- **蒙地卡羅樹搜尋（MCTS）**：從目前局面模擬對局以建立搜尋樹，由策略引導，並以價值網路評估。
- **自我對弈**：網路透過與自己較早的版本對弈而進步。

## 核心想法

策略網路縮小搜尋要考慮的落點範圍，價值網路則以一次學習得到的局面判斷，取代大量的隨機對局推演。搜尋再從綜合的證據中選出最佳著手。兩個網路缺一不可：策略讓搜尋聚焦，價值讓搜尋不必把每條變化都下到終局。

## 演算法

1. **監督式策略。** 以專家人類棋譜的資料庫訓練策略網路，預測落點。
2. **強化學習策略。** 透過自我對弈改進該策略：讓目前的網路與一批較早的版本對弈，並依結果更新。
3. **價值網路。** 以從自我對弈棋局取樣的局面訓練價值網路，目標為最終的對局結果。
4. **搜尋。** 每一手都執行 MCTS。每次模擬依一個平衡價值估計與策略先驗的規則選擇分支，展開新局面，以價值網路評估，再把結果回傳至搜尋樹。

論文中的選擇規則形式如下：

```latex
a_t = \arg\max_a \left( Q(s_t, a) + u(s_t, a) \right), \qquad u(s, a) \propto \frac{P(s, a)}{1 + N(s, a)}
```

其中 \(Q\) 是經過該分支之模擬的平均價值，\(P\) 是策略先驗，\(N\) 是造訪次數。

## 結果

- 論文報告了與歐洲圍棋冠軍樊麾的對局，AlphaGo 獲勝。
- 論文將其實力與當時其他圍棋程式比較，後者明顯較弱。

具體比分見論文，這裡不再重述。

## 限制

- 訓練使用了專家人類棋譜，因此系統的起點依賴人類資料。之後的 [AlphaZero](../alphazero/index.md) 在其所涵蓋的遊戲中移除了這項依賴。
- 此方法需要遊戲的精確模擬器。圍棋有，但許多實際問題沒有。
- 實力來自大量的運算，包括訓練與對局時的搜尋。

## 相關連結

- [AlphaZero](../alphazero/index.md)：不使用人類棋譜、只靠自我對弈學習的後繼系統。
- [MuZero](../model-based-rl/muzero/index.md)：以學習得到的模型取代遊戲規則進行規劃的後繼系統。
- [強化學習](../index.md)：更廣泛的方法家族，包括其大腦章節中關於多巴胺的獎勵預測理論。
- 腦與心智：一項對圍棋棋手的研究指出，AlphaGo 之後棋手的決策有所改變，新手法增加（Shin et al., 2023）。參見[遊戲](../../../../applications/games/index.md)頁面。

## 應用

- 遊戲研究：此方法是在棋類遊戲中結合學習式評估與搜尋的參考點。
- 人類專業知識：Shin et al. (2023) 的研究以圍棋為場景，衡量強大的電腦對手如何改變人類的決策。

## 開放問題

- 結果中有多少來自搜尋、多少來自學習得到的網路，兩者在不同運算預算下如何取捨。
- 同樣的組合能否用於具隱藏資訊的遊戲，因為在那裡無法直接使用模擬器。

## 參考文獻

### 開創性論文

- Silver, D. et al. (2016). Mastering the game of Go with deep neural networks and tree search. *Nature* 529. https://doi.org/10.1038/nature16961 — AlphaGo，結合策略與價值網路及蒙地卡羅樹搜尋。
- Silver, D. et al. (2017). Mastering the game of Go without human knowledge. *Nature* 550, 354–359. https://doi.org/10.1038/nature24270 — AlphaGo Zero，從隨機對弈開始學習圍棋，不使用人類棋譜。
- Silver, D. et al. (2018). A general reinforcement learning algorithm that masters chess, shogi, and Go through self-play. *Science*. https://doi.org/10.1126/science.aar6404 — AlphaZero，把同一套自我對弈方法應用於三種棋類。
- Shin, M. et al. (2023). Superhuman artificial intelligence can improve human decision-making by increasing novelty. *PNAS*. https://doi.org/10.1073/pnas.2214840120 — 比較 AlphaGo 出現前後圍棋棋手的著手，發現更具新意的著手與更好的決策品質。

### 綜述與教科書

- Browne, C. et al. (2012). A Survey of Monte Carlo Tree Search Methods. *IEEE Transactions on Computational Intelligence and AI in Games*. https://doi.org/10.1109/TCIAIG.2012.2186810 — 蒙地卡羅樹搜尋方法及其應用（包括圍棋）的綜述。
- Sutton, R. S. & Barto, A. G. *Reinforcement Learning: An Introduction*, 2nd ed. MIT Press, 2018. http://incompleteideas.net/book/the-book-2nd.html — 涵蓋 AlphaGo 與搜尋結合之價值與策略方法的教科書。
