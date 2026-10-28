---
translation_reviewed: 2026-10-28
---

# For The Win（Jaderberg 等人，2019）

一個由獨立強化學習智能體組成的種群，被訓練來在 Quake III Arena 中進行團隊奪旗遊戲。智能體只從像素與遊戲分數學習，論文報告它們作為隊友與對手時都達到人類水準。

## 問題

先前的智能體已能在單智能體遊戲與回合制雙人遊戲中達到人類水準，但真實世界中有許多獨立學習並行動的智能體，它們既合作也競爭。Jaderberg 等人研究一個三維第一人稱團隊遊戲，智能體必須學會與沒見過的隊友合作，並擊敗沒見過的對手。獎勵很稀疏，因為只有在一場比賽結束時才會得到勝利的獎勵。

## 核心想法

此方法採用兩層最佳化流程：

- **內層。**種群中的每個智能體以強化學習從自身的內部獎勵學習策略。內部獎勵補足了勝利時稀疏的獎勵，而智能體的策略會在數個時間尺度上選擇動作。
- **外層。**一個智能體種群在數千場並行比賽中同時訓練，智能體在隨機生成的地圖上與隊友合作、也與對手競爭。外層是基於種群的訓練，會調整智能體的內部獎勵與超參數。

地圖是程序生成的，包含室內與室外，一場比賽中奪旗次數最多的隊伍在五分鐘後獲勝。由於種群中的智能體各不相同，訓練比賽讓每個智能體接觸到各式各樣的隊友與對手。

## 方程式或演算法

論文沒有把此方法簡化為單一方程式。每個智能體以強化學習訓練，其獎勵結合了遊戲中稀疏的勝利訊號，以及學到的內在獎勵。外層的基於種群訓練會在訓練過程中調整所有智能體的內在獎勵與超參數。

## 結果

論文以錦標賽式的情境檢驗訓練後的智能體。摘要指出，智能體「作為隊友與對手時，勝率都超過強大的人類玩家」，並且「遠強於現有的最先進智能體」。論文所稱的「強大」人類是其 40 名參與者中前 20%，摘要並未給出對抗這些人類的數值勝率。技能以取自西洋棋的 Elo 分數線上估計。智能體訓練了二十億步，約 45 萬場比賽。學到的表徵編碼了各式各樣的遊戲知識，論文以線性探測衡量。論文描述的行為包括導航、跟隨與防守，其中跟隨在訓練中途被捨棄。

## 限制

- **運算成本。** 在數千場比賽中訓練一個大型種群，需要大量的平行運算。
- **特定環境。** 結果來自一款遊戲與一組地圖，論文並未顯示其在其他設定中的普遍性。

## 關聯

- FTW 的外層迴圈使用[基於種群的訓練](../pbt/index.md)，它是[基於種群的訓練](../index.md)總覽中的主要例子。
- 它的隊友與對手設定，是[多智能體強化學習總覽](../../index.md)中的混合情境。
- 其他競爭遊戲請見[遊戲應用](../../../../../../applications/games/index.md)頁面。

## 應用

- **電子遊戲。** 團隊型第一人稱遊戲與其他競爭性三維環境。
- **不確定性下的訓練**，智能體必須與從未見過的夥伴合作。

## 未解問題

- 如何降低訓練成本，使類似的結果需要更少的比賽。
- 如何檢驗跨遊戲與跨地圖的普遍性，而不只是單一遊戲。

## 參考文獻

### 奠基性論文

- Jaderberg et al. (2019), "Human-level performance in 3D multiplayer games with population-based reinforcement learning", *Science* 364, 859–865. https://discovery.ucl.ac.uk/id/eprint/10076318 — FTW 論文，包含兩層最佳化、奪旗環境與人類錦標賽結果。連結為作者機構的典藏紀錄。
- Jaderberg et al. (2018), "Human-level performance in first-person multiplayer games with population-based deep reinforcement learning", [arXiv:1807.01281](https://arxiv.org/abs/1807.01281) — FTW 論文的預印本，方法與結果相同。
- Jaderberg et al. (2017), "Population based training of neural networks", [arXiv:1711.09846](https://arxiv.org/abs/1711.09846) — FTW 外層所用的 PBT 方法。
- Lowe et al. (2017), "Multi-agent actor-critic for mixed cooperative-competitive environments", [arXiv:1706.02275](https://arxiv.org/abs/1706.02275) — 混合合作與競爭設定下的集中式評論家，即 FTW 以種群研究的設定。

### 綜述與教科書

- Busoniu, Babuska & De Schutter (2008), "A comprehensive survey of multiagent reinforcement learning", *IEEE Transactions on Systems, Man, and Cybernetics, Part C* 38(2), 156–172. https://doi.org/10.1109/TSMCC.2007.913919 — 多智能體學習情境的綜述，包含 FTW 所結合的競爭與合作情形。
