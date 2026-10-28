---
translation_reviewed: 2026-10-28
---

# 基於種群的訓練

基於種群的訓練（population-based training, PBT）同時訓練許多智能體，並讓它們互相學習。表現較好的成員會複製表現較差成員的權重與超參數，然後探索新的設定。結果是訓練過程中會改變的超參數時程，而不是一組固定的設定。在多智能體強化學習中，種群還能提供對手，因此這裡的方法也用於訓練競爭與混合型遊戲的智能體。

## 問題

整個訓練過程只用一組固定的超參數，通常並不是最佳選擇。前期有效的學習率與探索設定，後期可能有害。若以獨立的實驗搜尋設定，運算成本很高，而搜尋找到的最佳設定仍然是固定的。在競爭遊戲中還有另一個問題：只針對單一對手訓練的智能體，可能無法應付其他對手，因此訓練種群必須具有多樣性。

## 主要方法

- **[基於種群的訓練（PBT）](pbt/index.md)**（Jaderberg 等人，2017）以非同步方式執行一個種群。落後的工作者會複製表現較好工作者的權重與超參數，然後擾動複製來的超參數，形成超參數時程。
- **[奪旗智能體（FTW）](ftw/index.md)**（Jaderberg 等人，2019）訓練一個由獨立智能體組成的種群，讓它們在隨機生成的地圖上組隊、彼此對戰。每個智能體學習自己的內在獎勵，作者報告其在第一人稱遊戲 Quake III Arena 中達到人類水準。
- **與舊策略自我對弈**，如[總覽](../index.md)中描述的 OpenAI Five 訓練：大多數對局與最新策略對弈，其餘對局與舊策略對弈，使訓練不會過度擬合最新的策略。

## 比較

| 方法 | 種群的角色 | 時程 | 目標 |
|---|---|---|---|
| PBT | 複製並擾動成員 | 訓練中改變超參數 | 單智能體訓練、監督式與生成模型 |
| FTW | 隊友與對手 | 內在獎勵與策略 | 3D 遊戲中的團隊競爭 |
| 與舊策略自我對弈 | 過去的策略作為對手 | 對手取樣 | 競爭遊戲 |

## 關聯

- 種群是一種帶有梯度式內部迴圈的[演化計算](../../../../../theory/paradigms/evolutionary/index.md)形式。
- 競爭設定與棋類遊戲的[自我對弈](../../../../../applications/games/index.md)有關，例如 [AlphaZero](../../alphazero/index.md)。
- 超參數時程屬於訓練神經網路的[最佳化](../../../../../theory/optimization/index.md)方法。

## 應用

- **超參數調整**，適用於強化學習、監督式學習與生成模型。
- **競爭遊戲**，例如第一人稱團隊遊戲與即時戰略遊戲。

## 未解問題

- 需要多大的種群，以及如何為新的應用設定複製與探索的規則。
- 如何讓種群維持足夠的多樣性，避免收斂到單一策略。

## 參考文獻

### 奠基性論文

- Jaderberg 等人（2017），"Population based training of neural networks"，[arXiv:1711.09846](https://arxiv.org/abs/1711.09846)——PBT 論文，包含複製與探索步驟，以及在強化學習、翻譯與 GAN 上的實驗。
- Snoek, Larochelle & Adams（2012），"Practical Bayesian optimization of machine learning algorithms"，[arXiv:1206.2944](https://arxiv.org/abs/1206.2944)——超參數的貝氏最佳化，是 PBT 時程的搜尋式基準。
- Jaderberg 等人（2016），"Reinforcement learning with unsupervised auxiliary tasks"，[arXiv:1611.05397](https://arxiv.org/abs/1611.05397)——UNREAL，論文中 PBT 所調整的智能體之一。
- Jaderberg 等人（2019），"Human-level performance in 3D multiplayer games with population-based reinforcement learning"，*Science* 364, 859–865。https://doi.org/10.1126/science.aau6249——將基於種群的訓練應用於奪旗遊戲。
- Vinyals 等人（2019），"Grandmaster level in StarCraft II using multi-agent reinforcement learning"，*Nature* 575, 350–354。https://doi.org/10.1038/s41586-019-1724-z——多智能體訓練達到星海爭霸 II 的宗師級水準，是本頁比較的競爭情境之一。

### 綜述與教科書

- Busoniu, Babuska & De Schutter（2008），"A comprehensive survey of multiagent reinforcement learning"，*IEEE Transactions on Systems, Man, and Cybernetics, Part C* 38(2), 156–172。https://doi.org/10.1109/tsmcc.2007.913919——多智能體學習設定的綜述，包含種群所處理的競爭情境。
