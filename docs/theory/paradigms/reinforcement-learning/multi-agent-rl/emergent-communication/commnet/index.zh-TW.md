---
translation_reviewed: 2026-10-28
---

# CommNet（Sukhbaatar 等人，2016）

一種完全合作的模型：智能體透過共享的廣播通道傳送連續向量進行通訊，通道與策略以反向傳播共同學習。

## 問題

許多合作任務中，智能體只能看到環境的一部分。在多數早期研究中，通訊協定是由設計者決定的。Sukhbaatar 等人探討：智能體能否學會該傳送什麼，而學到的通訊是否能讓它們表現得比不通訊的智能體更好。

## 核心想法

模型把全部 \(J\) 個智能體視為一個大型前饋控制器的組成部分。每個智能體佔用其中一部分單元，各層之間的連接結構即是廣播通道。在每一步，智能體 \(j\) 由其輸入產生隱藏狀態 \(h_j\)。接著，每個智能體接收其他智能體所傳送向量的總和，並由自身狀態與該總和計算下一個隱藏狀態。由於通道是連續的，整個系統可以用一般的反向傳播訓練，也能與標準的單智能體強化學習或監督式學習結合。

模型簡單、適用範圍廣，能用於許多環境部分可見的任務。它也允許在執行時改變智能體的數量，作者指出這對於移動車輛之間的通訊等應用很重要。

## 方程式或演算法

若智能體 \(j\) 傳送由其隱藏狀態導出的向量 \(c_j\)，則智能體 \(i\) 在下一層的輸入為

\[
\text{input}_i = \sum_{j \ne i} c_j ,
\]

也就是每個智能體的通訊向量是其他智能體傳送內容的總和。每個智能體的策略再由合併後的隱藏狀態產生，所有智能體共享同一獎勵。

## 結果

論文在數個合作任務上評估 CommNet，包括拉桿任務、車輛必須不相撞地通過的交通路口任務，以及戰鬥任務。摘要報告，智能體「學會彼此通訊，表現優於不通訊的智能體與基準」。在某些情況下，學到的語言可以被解讀，揭示解決任務的簡單策略。

## 限制

- **假設完全合作。** 每個智能體都接收相同的獎勵，因此模型不處理競爭情境。
- **以總和通訊。** 對傳送內容加總，等於把所有其他智能體一視同仁，因此模型難以專注於特定的智能體。
- **可解釋性。** 部分學到的訊息可以被解讀，但這取決於任務。

## 關聯

- DIAL（見 [RIAL 與 DIAL](../rial-dial/index.md)）同樣端到端地學習通訊，但在執行時使用離散訊息。
- [MADDPG](../../maddpg/index.md) 不使用學到的通道來協調智能體。它的集中式評論家在訓練時看到其他智能體的動作，而不是訊息。
- CommNet 是[總覽](../index.md)所涵蓋的湧現式通訊方法之一。

## 應用

- **交通控制。** 車輛就路口狀況互相通訊，如交通路口任務所示。
- **多機器人協調**，每個機器人只有局部視野，必須分享資訊。

## 未解問題

- 如何處理大量或數量變動的智能體之間的通訊。
- 如何讓學到的訊息更容易解讀。

## 參考文獻

### 奠基性論文

- Sukhbaatar, Szlam & Fergus（2016），"Learning multiagent communication with backpropagation"，*Advances in Neural Information Processing Systems 29 (NIPS 2016)*，[arXiv:1605.07736](https://arxiv.org/abs/1605.07736)——CommNet 論文，包含廣播通道、反向傳播訓練，以及交通路口與戰鬥任務。
- Foerster 等人（2016），"Learning to communicate with deep multi-agent reinforcement learning"，[arXiv:1605.06676](https://arxiv.org/abs/1605.06676)——RIAL 與 DIAL，用於比較離散與可微分的學習訊息。
- Lazaridou, Peysakhovich & Baroni（2017），"Multi-agent cooperation and the emergence of (natural) language"，[arXiv:1612.07182](https://arxiv.org/abs/1612.07182)——研究參照遊戲中湧現的符號，以及如何與人類語言建立關聯。
- Lowe 等人（2017），"Multi-agent actor-critic for mixed cooperative-competitive environments"，[arXiv:1706.02275](https://arxiv.org/abs/1706.02275)——集中式評論家，用於與以通訊為基礎的協調方式比較。

### 綜述與教科書

- Busoniu, Babuska & De Schutter（2008），"A comprehensive survey of multiagent reinforcement learning"，*IEEE Transactions on Systems, Man, and Cybernetics, Part C* 38(2), 156–172。https://doi.org/10.1109/tsmcc.2007.913919——多智能體學習設定的綜述，包含作為協調工具的通訊。
