---
translation_reviewed: 2026-10-28
---

# RIAL 與 DIAL（Foerster 等人，2016）

兩種讓一組智能體端到端學習通訊協定的方法。RIAL 以深度 Q 學習訓練訊息；DIAL 則在訓練時讓誤差梯度直接穿過通訊通道。

## 問題

智能體只能看到部分狀態，必須分享資訊才能完成共同任務。論文研究的任務受通訊謎題與多智能體視覺啟發，每個智能體只看到輸入的一部分。協定不是事先給定的：智能體必須學會傳送什麼，以及如何理解收到的內容，而唯一的回饋是團隊的共享獎勵。

## 核心想法

每個智能體有一個網路，同時輸出兩樣東西：一個環境動作，以及一則給其他智能體的訊息。訊息在下一個時間步傳給其他智能體。兩種方法的差別在於如何處理訊息通道。

- **RIAL**（reinforced inter-agent learning）把每個訊息符號當成一個動作。每個智能體對環境動作與訊息的組合學習 Q 函數，並使用循環網路處理部分可觀測性。訊息與動作一樣，由同一個強化訊號學習。
- **DIAL**（differentiable inter-agent learning）讓通道可微分。在集中式學習期間，接收者的損失會透過訊息反向傳播給傳送者。一個離散化與正則化單元（discretise/regularise unit）在訓練時以雜訊正則化訊息，並在去中心化執行時將其離散化。由於梯度能在智能體之間傳遞，DIAL 的訊息獲得的學習訊號比 RIAL 更直接。

論文採用集中式學習、去中心化執行。參數可以在智能體之間共享，作者發現這對這些任務的學習有幫助。

## 方程式或演算法

對於 RIAL，每個智能體 \(a\) 對其聯合輸出 \(u = (u^{env}, m)\)（一個環境動作與一則訊息）保有一個 Q 函數，並以常見的時間差分目標學習：

\[
Q_a(h_t, u_t) \leftarrow r_t + \gamma \max_{u'} Q_a(h_{t+1}, u') ,
\]

其中 \(h_t\) 是該智能體的循環隱藏狀態。對於 DIAL，訓練時訊息 \(m\) 以 \(\mathrm{DRU}(m) = \mathrm{Logistic}(\mathcal{N}(m, \sigma))\) 正則化，使梯度能從接收者穿過通道回到傳送者。

## 結果

在三個智能體的 switch riddle 中，四種變體（RIAL 與 DIAL，各自有與沒有參數共享）都能在 5,000 個回合內學到最佳策略，且都勝過沒有通訊的基準。DIAL 搭配參數共享，達到最佳表現的速度明顯快於 RIAL。在四個智能體的情況下，沒有參數共享的 RIAL 無法勝過沒有通訊的基準，作者因此認為參數共享對學習通訊可能至關重要。在多步驟與色彩數字 MNIST 任務中，DIAL 明顯優於其他方法，而參數共享是達到最佳協定的必要條件。

## 限制

- **集中式學習。** DIAL 需要在訓練時讓梯度在智能體之間流動，因此需要共享的訓練流程。
- **獨立學習容易失敗。** 沒有參數共享時，RIAL 可能根本學不到共享協定，四個智能體的 switch riddle 即是例子。
- **可解釋性。** 學到的符號不保證具有人類可讀的意義。

## 關聯

- RIAL 為每個智能體使用[深度 Q 網路](../../../deep-q-networks/index.md)的深度 Q 學習方法。
- DIAL 的可微分通訊通道，是 [CommNet](../commnet/index.md) 所用平均隱藏狀態的另一種選擇。
- 通訊的研究見湧現式通訊的[總覽](../index.md)。

## 應用

- **觀察受限下的協調**，每個智能體只知道部分狀態。
- **多智能體視覺**，每個智能體看到場景的不同視角。

## 未解問題

- 如何學習能轉移到新夥伴身上的通訊。
- 如何在沒有人類監督下，讓學到的訊息具有共享意義。

## 參考文獻

### 奠基性論文

- Foerster 等人（2016），"Learning to communicate with deep multi-agent reinforcement learning"，[arXiv:1605.06676](https://arxiv.org/abs/1605.06676)——RIAL 與 DIAL 的論文，包含 switch riddle 與上文所述的離散化與正則化單元。
- Mnih 等人（2015），"Human-level control through deep reinforcement learning"，*Nature* 518, 529–533。https://doi.org/10.1038/nature14236——RIAL 為每個智能體使用的深度 Q 學習方法。
- Sukhbaatar, Szlam & Fergus（2016），"Learning multiagent communication with backpropagation"，[arXiv:1605.07736](https://arxiv.org/abs/1605.07736)——CommNet，是 DIAL 離散通道的連續替代方案。
- Lazaridou, Peysakhovich & Baroni（2017），"Multi-agent cooperation and the emergence of (natural) language"，[arXiv:1612.07182](https://arxiv.org/abs/1612.07182)——研究參照遊戲中湧現的符號，以及如何與人類語言建立關聯。

### 綜述與教科書

- Busoniu, Babuska & De Schutter（2008），"A comprehensive survey of multiagent reinforcement learning"，*IEEE Transactions on Systems, Man, and Cybernetics, Part C* 38(2), 156–172。https://doi.org/10.1109/tsmcc.2007.913919——多智能體學習設定與通訊所要解決的協調問題的綜述。
