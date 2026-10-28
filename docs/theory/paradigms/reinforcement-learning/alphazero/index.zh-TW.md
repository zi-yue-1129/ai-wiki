---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
  - applications/games
tags:
  - reinforcement learning
  - search
  - self-play
aliases:
  - AlphaZero
  - 阿爾法零
---

# AlphaZero（Silver 等人，2018）

AlphaZero 是同一套演算法，它只靠自我對弈，從隨機對弈開始、僅依各遊戲的規則，學會西洋棋、將棋與圍棋。它在每種遊戲中都達到超人水準，並擊敗了專為各遊戲設計的最先進程式。它移除了 [AlphaGo](../alphago/index.md) 方法中的人類棋譜與遊戲專用知識，使方法得以簡化。

## 問題

AlphaZero 之前，強大的棋類程式各自針對一種遊戲設計，使用開局庫、手工評估函數與遊戲專用的搜尋技巧。這篇論文探討的問題是：單一學習演算法，在沒有這些知識的情況下，能否在多種遊戲中達到頂尖水準。

## 關鍵概念

- **單一網路**：一個網路接收局面，同時輸出走法分布（策略）與價值。
- **搭配搜尋的自我對弈**：落點由網路引導的 MCTS 選出，搜尋結果成為訓練目標。
- **白板學習（tabula rasa）**：從隨機對弈開始，只使用規則，不用人類資料。

## 核心想法

網路提出走法並評估局面。由這些輸出引導的蒙地卡羅樹搜尋，所選的走法比網路直接輸出的更強。接著訓練網路去預測搜尋的選擇與最終的對局結果。反覆進行這個迴圈，網路與搜尋會一起進步。

## 演算法

1. 以隨機權重初始化網路。
2. **自我對弈。** 每一手都執行由網路引導的 MCTS，記錄各走法的造訪次數分布 \(\pi\)；對局結束時記錄結果 \(z\)。
3. **訓練。** 從最近的自我對弈棋局取樣局面，更新網路以降低下方的綜合損失。
4. 重複步驟 2 與 3，對弈時一律使用最新的網路。

```latex
\mathcal{L} = (z - v)^2 - \pi^\top \log p + c\,\lVert \theta \rVert^2
```

其中 \(p\) 與 \(v\) 分別是網路對某局面輸出的走法機率與價值，\(c\) 控制權重正則化的強度。

## 結果

《Science》摘要指出，AlphaZero 在其訓練的每種遊戲中都擊敗了最先進的程式。同一工作的 arXiv 預印本報告指出，AlphaZero 在訓練 24 小時內達到超人水準，並且在每種情況下都擊敗了世界冠軍級程式。比分與逐項比較見論文，這裡不再重述。

## 限制

- 此方法需要遊戲的精確模擬器，因此只適用於規則已知、沒有隱藏資訊的遊戲。
- 訓練耗用大量運算，而 24 小時的時間說明對應的是論文所用的硬體。
- 論文只評估三種棋類遊戲，其他遊戲的結果並未在論文中呈現。

## 相關連結

- [AlphaGo](../alphago/index.md)：較早、專為圍棋設計、使用人類棋譜的系統。
- [MuZero](../model-based-rl/muzero/index.md)：把同一套搜尋加網路的設計，延伸到規則不交給規劃器的遊戲。
- [強化學習](../index.md)：從獎勵中學習的更廣泛方法家族。
- 腦與心智：論文未模擬神經活動。它的自我對弈迴圈是無人類教師、從經驗中學習的計算範例。

## 應用

- 遊戲研究：在完全資訊棋類遊戲中，搭配搜尋的自我對弈的通用範本。

## 開放問題

- 此方法能延伸到什麼程度，例如不完全資訊遊戲，或沒有模擬器的問題。
- 學到的策略在多大程度上取決於自我對弈所投入的運算量。

## 參考文獻

### 開創性論文

- Silver, D. et al. (2018). A general reinforcement learning algorithm that masters chess, shogi, and Go through self-play. *Science*. https://doi.org/10.1126/science.aar6404 — AlphaZero，介紹單一演算法的方法。
- Silver, D. et al. (2017). Mastering the game of Go without human knowledge. *Nature* 550, 354–359. https://doi.org/10.1038/nature24270 — AlphaGo Zero，只針對圍棋、從隨機對弈學習的前身。
- Silver, D. et al. (2016). Mastering the game of Go with deep neural networks and tree search. *Nature* 529. https://doi.org/10.1038/nature16961 — AlphaGo，使用人類棋譜。
- Silver, D. et al. (2017). Mastering Chess and Shogi by Self-Play with a General Reinforcement Learning Algorithm. arXiv. https://arxiv.org/abs/1712.01815 — AlphaZero 工作的預印本，含 24 小時訓練結果與與世界冠軍程式的比較。

### 綜述與教科書

- Browne, C. et al. (2012). A Survey of Monte Carlo Tree Search Methods. *IEEE Transactions on Computational Intelligence and AI in Games*. https://doi.org/10.1109/TCIAIG.2012.2186810 — AlphaZero 用於規劃的樹搜尋方法綜述。
- Sutton, R. S. & Barto, A. G. *Reinforcement Learning: An Introduction*, 2nd ed. MIT Press, 2018. http://incompleteideas.net/book/the-book-2nd.html — 涵蓋自我對弈學習背後之價值與策略方法的教科書。
