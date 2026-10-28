---
status: complete
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
  - applications/games
tags:
  - reinforcement learning
  - model-based
  - planning
aliases:
  - MuZero
---

# MuZero（Schrittwieser 等人，2020）

MuZero 以學習得到的模型取代遊戲規則進行規劃。它學習的模型只預測規劃所需的量：獎勵、策略與價值。在圍棋、西洋棋與將棋上，它達到了與被給予規則的 [AlphaZero](../../alphazero/index.md) 相當的超人水準；在 57 款 Atari 遊戲上，它也創下新的最先進成績。

## 問題

以模型進行規劃，需要模型在關鍵之處夠準確。若要學習預測每一個未來觀測（例如遊戲畫面的每個像素），模型容量會花在不影響決策的細節上。這篇論文探討的問題是：能否學到只預測規劃所需量的模型，並且在遊戲規則對它未知的情況下仍能規劃得很好。

## 關鍵概念

- **潛在狀態**：模型所維護的遊戲內部表徵，它不需要重現觀測。
- **預測目標**：模型在每一步只預測獎勵、走法策略與價值，其他一概不預測。
- **規劃**：蒙地卡羅樹搜尋在學習得到的模型內執行，搜尋的是想像出的潛在狀態。

## 核心想法

三個學習得到的函數協同運作。表徵函數把觀測轉為起始的潛在狀態。動態函數接收潛在狀態與一個動作，回傳下一個潛在狀態與獎勵。預測函數回傳潛在狀態的策略與價值。搜尋在這些函數所定義的潛在狀態上進行，而網路的訓練目標是讓其預測的獎勵、策略與價值，與搜尋及真實遊戲所產生的結果相符。

## 演算法

1. **表徵。** 將近期的觀測編碼為潛在狀態 \(s^0\)。
2. **展開。** 對每個規劃中的動作 \(a^k\)，以動態函數計算 \(s^k, r^k\)，以預測函數計算 \(p^k, v^k\)。
3. **搜尋。** 在這些潛在狀態上執行 MCTS 以選擇動作。儲存造訪次數分布形式的策略，以及搜尋得到的價值。
4. **訓練。** 端到端更新三個函數，使展開步驟上預測的獎勵、策略與價值，與真實獎勵、搜尋策略與對局結果一致。

## 結果

論文在 Atari 上比較 MuZero 與無模型及有模型的基線，並在棋類遊戲上與 AlphaZero 比較。以下數字皆取自論文的表格。

- **棋類遊戲**：MuZero 達到與 AlphaZero 相當的超人水準，而 AlphaZero 是在給定遊戲規則下訓練的。在圍棋上，MuZero 每個搜尋樹節點使用的運算量較少，表現略勝 AlphaZero。
- **Atari，大量資料設定**：MuZero 的中位數正規化分數為 2041.1%，平均為 4999.2%，高於 R2D2 的中位數 1920.6% 與平均 4024.9%。
- **Atari，每遊戲 2 億影格**：Reanalyze 變體的中位數為 731.1%。同一設定下，論文將其與 IMPALA（中位數 191.8%）、Rainbow（231.1%）與 LASER（431%）比較。

完整表格請見論文。

## 限制

- 學習得到的模型不會直接與真實遊戲核對。模型的錯誤可能誤導搜尋，這也是訓練目標使用真實獎勵與結果的原因。
- 對局時的搜尋成本高昂，訓練也耗用大量運算。
- 潛在狀態無法解釋為遊戲狀態，因此很難檢視模型的規劃過程。

## 相關連結

- [AlphaZero](../../alphazero/index.md)：MuZero 把它的搜尋與網路設計延伸到規則未知的遊戲。
- [基於模型的強化學習](../index.md)：MuZero 所屬的家族，還包括 Dyna 與世界模型。
- 腦與心智：在學習得到的模型中模擬未來以進行規劃，是目標導向行為的一種計算解釋。神經科學面向見[計算神經科學](../../../../../brain-mind/computational-neuroscience/index.md)。

## 應用

- 不給規則的遊戲：此方法僅從經驗出發，即可玩 Atari 與棋類遊戲。
- 模型式研究：論文是以只為決策相關量學習模型進行規劃的參考點。

## 開放問題

- 學習得到的模型對很少造訪的狀態出錯時，如何仍能規劃得好。
- 如何減少對局時搜尋所需的運算。

## 參考文獻

### 開創性論文

- Schrittwieser, J. et al. (2020). Mastering Atari, Go, chess and shogi by planning with a learned model. *Nature* 588, 604–609. https://doi.org/10.1038/s41586-020-03051-4 — MuZero，以預測獎勵、策略與價值之學習模型進行規劃。
- Silver, D. et al. (2018). A general reinforcement learning algorithm that masters chess, shogi, and Go through self-play. *Science*. https://doi.org/10.1126/science.aar6404 — AlphaZero，MuZero 在棋類遊戲上所比較的基準。
- Silver, D. et al. (2016). Mastering the game of Go with deep neural networks and tree search. *Nature* 529. https://doi.org/10.1038/nature16961 — AlphaGo，開啟這一系列工作的圍棋專用系統。
- Ha, D. & Schmidhuber, J. (2018). World Models. arXiv. https://arxiv.org/abs/1803.10122 — 學習潛在世界模型，並在其中訓練控制器。

### 綜述與教科書

- Sutton, R. S. & Barto, A. G. *Reinforcement Learning: An Introduction*, 2nd ed. MIT Press, 2018. http://incompleteideas.net/book/the-book-2nd.html — 涵蓋 MuZero 所建立之基於模型規劃方法的教科書。
