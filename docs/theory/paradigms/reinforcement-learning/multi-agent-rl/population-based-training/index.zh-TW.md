---
translation_reviewed: 2026-10-28
---

# 基於族群的訓練（Jaderberg 等人，2017）

基於族群的訓練（population-based training，PBT）並行訓練許多代理人。較弱的成員會定期複製較強成員的權重與超參數，然後對複製來的超參數加以擾動。這個方法最初是為調整神經網路的超參數而設計，之後成為多代理人訓練的基礎，應用於雷神之鎚 III 的團隊代理人與 AlphaStar 等遊戲系統；後者以代理人聯盟作為對手。它是[多代理人強化學習](../index.md)概述的一部分。

## 概述

一般的超參數調整是執行許多各自獨立的訓練工作並保留最好的結果，因此大部分運算都花在最終被丟棄的執行上。Jaderberg 等人（2017）則在一個固定的運算預算內，同時最佳化一個族群中的模型與它們的超參數，得到的是一組隨時間變化的設定排程，而不是整個訓練過程只用一組固定設定。

在多代理人情境中，族群還提供對手。只對抗一個固定對手的學習者，可能會得出只能打敗那個對手、卻輸給其他對手的策略。多元的族群，讓成員彼此對弈，是一種附有過去策略記憶的[自我對弈](../../mcts-and-self-play/index.md)。

## 關鍵概念

- **族群**：$N$ 個代理人，各自擁有權重、超參數與表現紀錄。
- **利用（exploit）**：表現較弱的成員以表現較強成員的權重與超參數取代自己的。
- **探索（explore）**：複製之後，超參數會被隨機擾動，使族群持續搜尋。
- **聯盟（league）**：AlphaStar 中具有多種角色的族群。主要代理人對抗整個聯盟，而利用者則尋找其他成員的弱點。
- **虛擬自我對弈（fictitious self-play）**：對抗過去對手的混合，而不只是最新的對手（Heinrich & Silver, 2016）；聯盟的對手抽樣正是建立在這個想法之上。

## 運作方式

PBT 是一種演算法，而不是單一公式。其循環如下：

1. 以隨機權重與隨機超參數初始化 $N$ 個工作者。
2. 讓所有工作者並行訓練固定的步數，並記錄每個工作者的適應度，例如平均回報或勝率。
3. 對於位於底部分位的每個工作者，複製來自頂部分位某個工作者的權重與超參數。
4. 擾動複製來的超參數，例如把每個超參數乘以一個隨機因子。
5. 重複步驟 2 至 4，直到預算用盡，並保留最佳的成員。

在多代理人遊戲中，族群的適應度是相對於族群本身來衡量的。AlphaStar 的聯盟把角色分開。主要代理人對抗聯盟成員的混合，並偏向它們目前會輸的對手。主要利用者以擊敗主要代理人為目標，聯盟利用者則針對聯盟中各成員的弱點。過去的快照留在聯盟中，使舊策略不會被遺忘。

OpenAI Five 與此密切相關，但其已發表的說明以大規模自我對弈為核心，並在數月內持續訓練（Berner 等人，2019）。

## 結果

PBT 論文報告了在固定預算內，於包括強化學習在內的深度學習任務上找到的超參數排程；比較的數字請見論文。Jaderberg 等人（2019）報告，經族群訓練的團隊在雷神之鎚 III 奪旗中，能與人類玩家競爭並取得成功。Vinyals 等人（2019）報告 AlphaStar 在星海爭霸 II 中達到大師級水準，而 Berner 等人（2019）報告 OpenAI Five 於 2019 年擊敗了 Dota 2 的世界冠軍。

## 限制

- **運算成本。** 族群與聯盟需要大量並行的遊戲。能夠重現最大規模結果的團隊很少。
- **啟發式搜尋。** 利用與探索的規則合理，但沒有一般性的保證能找到好的排程。
- **非傳遞性的強弱。** 類似石頭剪刀布的循環，使單一適應度數值可能誤導排名。聯盟處理了這個問題，但也增加了複雜度。
- **有限的遷移。** 已報告的成功集中在有明確勝負條件與模擬器的遊戲中。它們能否遷移到實體或開放式的多代理人問題，尚未得到證明。

## 開放問題

什麼樣的族群結構最能防止循環？當強弱不具傳遞性時，應如何衡量進展？Lanctot 等人（2017）把族群訓練與賽局理論的最佳回應連結起來。利用與探索也類似[演化搜尋](../../../evolutionary/index.md)，但這個類比能延伸到學習得來的策略多遠，仍不清楚。

## 參考文獻

### 開創性論文

- Jaderberg, M. 等人 (2017). *Population Based Training of Neural Networks*. arXiv:1711.09846. https://arxiv.org/abs/1711.09846 — 提出 PBT，在固定運算預算內聯合最佳化一個網路族群及其超參數。
- Jaderberg, M. 等人 (2019). *Human-level performance in 3D multiplayer games with population-based reinforcement learning*. Science. https://doi.org/10.1126/science.aau6249 — 透過一個族群訓練雷神之鎚 III 奪旗的團隊代理人，這些代理人曾與人類玩家競爭。
- Vinyals, O. 等人 (2019). *Grandmaster level in StarCraft II using multi-agent reinforcement learning*. Nature. https://doi.org/10.1038/s41586-019-1724-z — AlphaStar，以主要代理人與利用者組成的聯盟訓練而成。
- Heinrich, J. & Silver, D. (2016). *Deep Reinforcement Learning from Self-Play in Imperfect-Information Games*. arXiv:1603.01121. https://arxiv.org/abs/1603.01121 — 神經虛擬自我對弈，對抗過去對手的混合來學習，並在不完全資訊博弈中逼近均衡。

### 綜述與教科書

- Hernandez-Leal, P., Kartal, B. & Taylor, M. E. (2018). *A Survey and Critique of Multiagent Deep Reinforcement Learning*. arXiv:1810.05587. https://arxiv.org/abs/1810.05587 — 回顧深度多代理人方法，包括遊戲中使用的族群與自我對弈方法。

### 文章與文件

- Berner, C. 等人 (2019). *Dota 2 with Large Scale Deep Reinforcement Learning*. arXiv:1912.06680. https://arxiv.org/abs/1912.06680 — OpenAI Five 系統，以大規模自我對弈與歷時數月的持續訓練完成。
- Baker, B. 等人 (2019). *Emergent Tool Use From Multi-Agent Autocurricula*. arXiv:1909.07528. https://arxiv.org/abs/1909.07528 — 顯示族群內部的競爭會產生一連串新策略，形成自生成的課程。
- Lanctot, M. 等人 (2017). *A Unified Game-Theoretic Approach to Multiagent Reinforcement Learning*. arXiv:1711.00832. https://arxiv.org/abs/1711.00832 — 提出針對策略混合的近似最佳回應，是多代理人訓練的族群層次觀點。
