---
translation_reviewed: 2026-10-28
---

# AlphaGo（Silver 等人，2016）

AlphaGo 結合深度策略網路、價值網路與蒙地卡羅樹搜尋，以職業水準下圍棋。它是[上層主題](../index.md)所描述的搜尋加自我對弈系統中的第一個，也是讓這種結合廣為人知的系統。

## 概述

圍棋長期以來是 AI 的挑戰，因為它的分支因子遠大於西洋棋，窮舉搜尋與人工撰寫的評估都不切實際。在 AlphaGo 之前，最好的圍棋程式使用[附 UCT 的 MCTS](../monte-carlo-tree-search/index.md)與人工設計的特徵，達到強業餘水準。AlphaGo 加入了兩個學習得到的網路：策略網路提出值得檢查的走法，價值網路估計一個局面誰佔優勢。搜尋再利用這兩個網路把模擬集中在重點上。

原論文先以人類專家棋譜訓練策略網路，再透過與自己過去版本對弈的強化學習加以改進。論文報告，整套系統擊敗了一位歐洲圍棋冠軍。之後的 AlphaGo Zero（Silver 等人，2017）則完全移除了人類棋譜，並在 [AlphaZero](../alphazero/index.md) 頁面中說明。

## 關鍵概念

- **策略網路**：對每個合法走法輸出機率，用來偏置搜尋要展開哪些分支。
- **價值網路**：輸出一個局面的勝率估計，取代了大部分推演的工作。
- **監督式預訓練**：先訓練策略預測人類專家的走法。
- **自我對弈精煉**：接著透過與自己過去版本對弈來改進策略。

## 運作方式

AlphaGo 從目前局面開始執行 MCTS。在每次模擬中，它利用搜尋統計量，並結合策略網路提供的先驗來選擇走法；葉節點的評估則以兩種方式進行：價值網路與快速的推演策略。兩個估計值混合成一個葉節點價值，再沿樹回傳。

訓練流程大致如下：

1. 以人類棋譜訓練策略網路 $p_\sigma$，使其預測專家走法。
2. 以自我對弈的局面與結果，訓練快速推演策略與價值網路 $v_\theta$。
3. 透過與自己過去版本對弈的強化學習，改進策略網路，得到 $p_\rho$。
4. 下棋時執行 MCTS：以策略先驗決定展開哪些子節點，並以混合後的葉節點價值決定哪一步較好。

葉節點評估會把價值網路與推演結果混合，混合權重由論文調整。

## 結果

Nature 論文報告，AlphaGo 戰勝了一位歐洲圍棋人類冠軍。這個結果是里程碑，因為多年來研究者普遍認為，圍棋在搜尋與評估方法之下還會遙不可及。確切的對局比分與其他比較，請見原論文，引用前應先在論文中核對。

## 限制

- **依賴人類資料**。最初的策略仰賴大量專家棋譜，因此方法僅適用於存在此類紀錄的領域。
- **搜尋負擔重**。每一步都需要大量網路評估，因此要達到強的水準需要相當的硬體。
- **兩個網路加上推演**。設計複雜，各個獨立訓練的元件必須一起調校。
- **領域狹窄**。系統是為圍棋設計的，輸入特徵也使用了圍棋專用的設計。

## 開放問題

若不從人類棋譜開始，系統能否同樣出色？AlphaGo Zero 對圍棋給出了肯定的答案，接下來的問題是設計中哪些部分能推廣到其他領域。另一個問題是，力量有多少來自搜尋、多少來自網路，後來的系統就是為了檢驗這點而設計的。

## 關聯

AlphaGo 連接了[深度 Q 網路](../../deep-q-networks/index.md)的價值基礎研究，以及[MCTS](../monte-carlo-tree-search/index.md)的搜尋研究。它的自我對弈精煉，與 [AlphaZero](../alphazero/index.md) 和 [MuZero](../muzero/index.md) 所用的自我對弈是同一個想法，其對局歷史則見[遊戲](../../../../../applications/games/index.md)頁面。

## 參考文獻

### 開創性論文

- Silver, D. 等人 (2016). *Mastering the game of Go with deep neural networks and tree search*. Nature. https://doi.org/10.1038/nature16961 — AlphaGo 原論文，結合策略與價值網路與蒙地卡羅樹搜尋。
- Silver, D. 等人 (2017). *Mastering the game of Go without human knowledge*. Nature. https://doi.org/10.1038/nature24270 — AlphaGo Zero，從隨機對弈開始、不使用人類棋譜、以自我對弈學習圍棋。
- Silver, D. 等人 (2018). *A general reinforcement learning algorithm that masters chess, shogi, and Go through self-play*. Science. https://doi.org/10.1126/science.aar6404 — AlphaZero，把 AlphaGo Zero 推廣到西洋棋與將棋。
- Kocsis, L. & Szepesvári, C. (2006). *Bandit Based Monte-Carlo Planning*. Lecture Notes in Computer Science. https://doi.org/10.1007/11871842_29 — AlphaGo 搜尋所延伸的 UCT 演算法。
- Coulom, R. (2007). *Efficient Selectivity and Backup Operators in Monte-Carlo Tree Search*. Lecture Notes in Computer Science. https://doi.org/10.1007/978-3-540-75538-8_7 — 圍棋程式中蒙地卡羅樹搜尋的選擇與回傳規則，是 AlphaGo 所建立的傳統。

### 綜述與教科書

- Browne, C. B. 等人 (2012). *A Survey of Monte Carlo Tree Search Methods*. IEEE Transactions on Computational Intelligence and AI in Games. https://doi.org/10.1109/TCIAIG.2012.2186810 — 綜述 AlphaGo 之前與之後的 MCTS 方法。
