---
translation_reviewed: 2026-10-28
---

# MuZero（Schrittwieser 等人，2020）

MuZero 在自己學得的模型中，以[蒙地卡羅樹搜尋](../monte-carlo-tree-search/index.md)進行規劃，而不是在由規則給定的模擬器中。它保留了 [AlphaZero](../alphazero/index.md) 的搜尋與自我對弈循環，同時不再需要知道環境如何運作，因此同一套方法既能下棋，也能玩 Atari 遊戲。

## 概述

AlphaZero 的搜尋需要精確的模擬器：它必須能回答「走了這一步之後會發生什麼」。棋類遊戲的規則提供了這樣的模擬器，但對大多數其他問題而言，包括以像素為輸入的電子遊戲，並沒有可用的模擬器。基於模型的規劃在這類視覺複雜的領域中一直表現不佳。MuZero 的問題是：代理人能否學到一個足夠精確、可用於規劃的模型，而且不必對整個觀測進行建模。論文提出的答案是一個只預測規劃所需內容的模型：獎勵、策略與價值。

arXiv 摘要報告，MuZero 在 57 款 Atari 遊戲（視覺豐富的遊戲環境的標準基準）上達到新的最佳水準。摘要還報告，在圍棋、西洋棋與將棋上，MuZero 在不知道遊戲規則的情況下，與得知規則的 AlphaZero 達到相當的超人水準。

## 關鍵概念

- **表徵函數**：把最近的觀測映射到內部狀態 $s^0$。這個狀態是學得的，不需要能重建觀測。
- **動態函數**：輸入一個內部狀態與一個動作，預測獎勵與下一個內部狀態。
- **預測函數**：把內部狀態映射到策略與價值，即 AlphaZero 網路的兩個輸出。
- **潛在空間規劃**：MCTS 在內部狀態上運行，每一步模擬都呼叫一次動態函數。

## 運作方式

對於觀測序列 $o_1,\dots,o_t$ 與規劃的動作序列 $a^1,\dots,a^K$，三個學得的函數為

$$
s^0 = h_\theta(o_1,\dots,o_t), \qquad r^k, s^k = g_\theta(s^{k-1}, a^k), \qquad \mathbf{p}^k, v^k = f_\theta(s^k).
$$

MCTS 把這些函數當作模擬器使用。每個模擬步驟先呼叫 $g_\theta$ 預測獎勵，再以 $f_\theta$ 取得新內部狀態上的策略與價值，之後套用一般的選擇與回傳規則。搜尋過程中內部狀態不會與真實觀測核對，因此模型必須被訓練得對規劃有用。

訓練時，模型從觀測到的起點展開數步，並讓其預測與真實經驗的目標相符：觀測到的獎勵、由儲存的搜尋結果自舉而來的價值，以及由造訪次數得到的搜尋策略。演算法流程如下：

1. 以模型中的 MCTS 進行數局遊戲，儲存觀測、動作、獎勵、搜尋策略與搜尋價值。
2. 隨機抽取一段已儲存的遊戲片段。
3. 從該片段的第一個觀測出發，依實際採取的動作把模型展開 $K$ 步。
4. 建立目標：觀測到的獎勵、$n$ 步價值目標，以及搜尋策略。
5. 以梯度下降同時更新三個網路，最小化展開各步的獎勵、價值與策略誤差之和。

## 結果

arXiv 摘要（Schrittwieser 等人，2020）陳述了兩項結果。在 57 款 Atari 遊戲（論文用來測試視覺複雜領域的環境）上，MuZero 達到新的最佳水準。在圍棋、西洋棋與將棋上，MuZero 在不知道規則的情況下，與 AlphaZero 的超人表現相當。

## 限制

- **模型只為規劃用途而學**。學得的狀態是為了預測獎勵、價值與策略而訓練，並不忠實地表示環境。對規劃有用的模型，對於預測或解釋等其他用途未必有用。
- **誤差會累積**。與任何基於學得模型的規劃器一樣，學得動態中的錯誤會在長時間搜尋的各步中累積。
- **測試領域**。主要證據來自獎勵明確、動態確定的遊戲。論文並未展示在有雜訊的真實世界環境中的表現。

## 開放問題

如何讓學得的模型在對規劃關鍵的地方更精確，同時又不必在完整觀測上訓練？只預測獎勵與價值的模型，在實務上能否被檢查或修正？而這套方法能否擴展到隨機或部分可觀測的環境，在那裡單一的搜尋路徑可能無法涵蓋不確定性？

## 關聯

MuZero 是[基於模型的強化學習](../../model-based-rl/index.md)最清楚的例子，與其他學習世界模型的代理人並列，例如 Dreamer（見[基於模型的強化學習](../../model-based-rl/index.md)頁面），以及 Ha 與 Schmidhuber（2018）的[世界模型](../../../../models/world-models/index.md)。它的規劃步驟與 [AlphaZero](../alphazero/index.md) 的搜尋相同，較早的棋類結果則見[上層主題](../index.md)。

## 參考文獻

### 開創性論文

- Schrittwieser, J. 等人 (2020). *Mastering Atari, Go, chess and shogi by planning with a learned model*. Nature. https://doi.org/10.1038/s41586-020-03051-4 — MuZero 論文，在預測獎勵、策略與價值的學得模型中以搜尋進行規劃。
- Silver, D. 等人 (2018). *A general reinforcement learning algorithm that masters chess, shogi, and Go through self-play*. Science. https://doi.org/10.1126/science.aar6404 — AlphaZero，MuZero 所推廣的、以規則為基礎的搜尋方法。
- Silver, D. 等人 (2016). *Mastering the game of Go with deep neural networks and tree search*. Nature. https://doi.org/10.1038/nature16961 — AlphaGo，首個在這種規模上結合學習網路與樹搜尋的系統。
- Ha, D. & Schmidhuber, J. (2018). *World Models*. arXiv:1803.10122. https://arxiv.org/abs/1803.10122 — 學習環境的壓縮模型，並完全在其想像的展開中訓練控制器。

### 文章與文件

- Hafner, D. 等人 (2023). *Mastering Diverse Domains through World Models*. arXiv:2301.04104. https://arxiv.org/abs/2301.04104 — DreamerV3，單一的世界模型代理人，學習潛在模型並在其中規劃，適用於多種領域。
