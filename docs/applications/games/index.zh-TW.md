# 遊戲

遊戲是 AI 最愛的實驗室：規則清楚、結果可量測，而且模擬經驗幾乎無限。

## 遊戲 AI 的里程碑

| 年份 | 遊戲 | 系統 | 技術 |
|---|---|---|---|
| 1952–59 | 西洋跳棋 | Samuel | 早期機器學習 |
| 1992 | 西洋雙陸棋 | TD-Gammon | TD 學習加神經網路 |
| 1994–2007 | 西洋跳棋 | Chinook | 搜尋；2007 年西洋跳棋被完全解出 |
| 1997 | 西洋棋 | Deep Blue | 大規模搜尋加人工設計的評估函數 |
| 2015 | Atari 遊戲 | DQN | 以像素為輸入的深度強化學習 |
| 2016 | 圍棋 | AlphaGo | 策略與價值網路加 MCTS |
| 2017 | 西洋棋、將棋、圍棋 | AlphaZero | 從零開始的自我對弈 |
| 2017–2019 | 一對一與六人德州撲克 | Libratus、Pluribus | 反事實遺憾最小化，處理不完全資訊 |
| 2019 | Dota 2 | OpenAI Five | 大規模 PPO 自我對弈 |
| 2019 | 星海爭霸 II | AlphaStar | 聯賽式訓練，結合模仿與強化學習 |
| 2020 | Atari、圍棋、西洋棋（不給規則） | MuZero | 學習出的模型加規劃 |
| 2022 | 外交（Diplomacy） | Cicero | 語言模型加策略規劃，與人類談判 |
| 2022 | Stratego | DeepNash | 不完全資訊下的無模型強化學習 |
| 2022 | Gran Turismo | GT Sophy | 強化學習賽車，兼顧運動家精神 |
| 2023 起 | Minecraft 與開放世界 | Voyager、VPT、DreamerV3 | LLM 代理人、影片預訓練、世界模型 |

## 遊戲開發中的 AI

- 程序化內容生成：關卡、地形、任務
- 生成式素材：貼圖、3D 模型、語音、音樂
- NPC 行為：行為樹與效用 AI（仍是主流），以及由 LLM 驅動的對話角色
- 測試：自動化試玩代理人、錯誤偵測
- 玩家建模：配對、難度調整、流失預測、反作弊
- 渲染：類似 DLSS 的神經網路升頻與影格生成

## AI 原生與模擬型遊戲

- 能互動式生成畫面的神經遊戲引擎（GameNGen 在 2024 年於擴散模型中執行 DOOM；類似 Genie 的世界模型）
- 由 LLM 驅動的互動式小說與社會模擬（Generative Agents）

## 遊戲為何對 AI 研究重要

- 規劃、不完全資訊、多代理人合作與競爭、長時程任務的基準
- 賽局理論：納許均衡、自我對弈的收斂性
- 想法的遷移：AlphaZero 式的搜尋 → AlphaFold 的反覆精煉思路、AlphaTensor、AlphaDev（排序演算法）

## 透過遊戲研究人類認知

- 對西洋棋專家的研究（de Groot；Chase 與 Simon 的組塊理論）塑造了專家記憶的理論
- AlphaGo 之後，職業圍棋棋士的下法改變了：決策品質提升，新手法增加（Shin et al., 2023, *PNAS*）
- 多臂老虎機（bandit）與兩步任務等遊戲，是認知科學與計算精神醫學的標準工具

## 關鍵方法

下列三種方法涵蓋上文多數里程碑。每一項都連結到解釋該方法的頁面。

- [深度 Q 網路](../../theory/paradigms/reinforcement-learning/deep-q-networks/index.md)：從原始像素做深度價值學習，即 2015 年 Atari 成果所用的方法（Mnih et al., 2015）。
- [近端策略最佳化](../../theory/paradigms/reinforcement-learning/proximal-policy-optimisation/index.md)：一種裁剪的策略梯度更新，用於 OpenAI Five 等大規模自我對弈系統（Schulman et al., 2017；OpenAI et al., 2019）。
- [基於模型的強化學習](../../theory/paradigms/reinforcement-learning/model-based-rl/index.md)：以遊戲的學習模型進行規劃。MuZero 在不給定規則的情況下做到這點（Schrittwieser et al., 2020）。

## 參考文獻

### 開創性論文

- Samuel, A. L. (1959). Some Studies in Machine Learning Using the Game of Checkers. *IBM Journal of Research and Development*. https://doi.org/10.1147/rd.33.0210 — 早期的西洋跳棋程式，透過對弈學習改進其評估函數。
- Tesauro, G. (1995). Temporal difference learning and TD-Gammon. *Communications of the ACM*. https://doi.org/10.1145/203330.203343 — 以時序差分學習加神經網路訓練的西洋雙陸棋程式。
- Chase, W. G. & Simon, H. A. (1973). Perception in chess. *Cognitive Psychology*. https://doi.org/10.1016/0010-0285(73)90004-2 — 經典研究，說明西洋棋專家如何透過組塊記住棋盤局面。
- Campbell, M., Hoane, A. J. & Hsu, F.-h. (2002). Deep Blue. *Artificial Intelligence*. https://doi.org/10.1016/s0004-3702(01)00129-1 — 說明 1997 年擊敗世界冠軍之西洋棋系統的設計。
- Mnih, V. et al. (2015). Human-level control through deep reinforcement learning. *Nature*. https://doi.org/10.1038/nature14236 — 從像素學習的深度 Q 學習，跨多款 Atari 遊戲。
- Silver, D. et al. (2016). Mastering the game of Go with deep neural networks and tree search. *Nature*. https://doi.org/10.1038/nature16961 — AlphaGo，結合策略與價值網路及蒙地卡羅樹搜尋。
- Silver, D. et al. (2018). A general reinforcement learning algorithm that masters chess, shogi, and Go through self-play. *Science*. https://doi.org/10.1126/science.aar6404 — AlphaZero，僅給定規則，透過自我對弈學會西洋棋、將棋與圍棋。
- Schrittwieser, J. et al. (2020). Mastering Atari, Go, chess and shogi by planning with a learned model. *Nature*. https://doi.org/10.1038/s41586-020-03051-4 — MuZero，在不給定規則的情況下，以學習到的模型進行規劃。
- Schulman, J. et al. (2017). Proximal Policy Optimization Algorithms. arXiv. https://arxiv.org/abs/1707.06347 — 裁剪目標的策略梯度演算法，即 PPO。
- OpenAI et al. (2019). Dota 2 with Large Scale Deep Reinforcement Learning. arXiv. https://arxiv.org/abs/1912.06680 — OpenAI Five，以 PPO 在 Dota 2 中進行大規模自我對弈。
- Vinyals, O. et al. (2019). Grandmaster level in StarCraft II using multi-agent reinforcement learning. *Nature*. https://doi.org/10.1038/s41586-019-1724-z — AlphaStar，透過與一群代理人的聯盟對戰訓練。
- Brown, N. & Sandholm, T. (2019). Superhuman AI for multiplayer poker. *Science*. https://doi.org/10.1126/science.aay2400 — Pluribus，可進行六人無限注德州撲克。
- Perolat, J. et al. (2022). Mastering the game of Stratego with model-free multiagent reinforcement learning. *Science*. https://doi.org/10.1126/science.add4679 — DeepNash，在不完全資訊遊戲中使用無模型的強化學習。
- Wurman, P. R. et al. (2022). Outracing champion Gran Turismo drivers with deep reinforcement learning. *Nature*. https://doi.org/10.1038/s41586-021-04357-7 — GT Sophy，與頂尖人類車手競速的強化學習系統。
- Meta Fundamental AI Research Diplomacy Team (FAIR) et al. (2022). Human-level play in the game of *Diplomacy* by combining language models with strategic reasoning. *Science*. https://doi.org/10.1126/science.ade9097 — Cicero，結合語言模型與策略規劃進行談判。
- Park, J. S. et al. (2023). Generative Agents: Interactive Simulacra of Human Behavior. arXiv. https://arxiv.org/abs/2304.03442 — 在模擬小鎮中會規劃與記憶的 LLM 代理人。
- Shin, M. et al. (2023). Superhuman artificial intelligence can improve human decision-making by increasing novelty. *PNAS*. https://doi.org/10.1073/pnas.2214840120 — 比較 AlphaGo 出現前後圍棋棋手的著手，發現決策更具新意且更好。

### 綜述與教科書

- Yannakakis, G. N. & Togelius, J. (2018). *Artificial Intelligence and Games*. Springer. https://doi.org/10.1007/978-3-319-63519-4 — 關於遊戲中的 AI 對弈、內容生成與玩家建模的教科書。

## 延伸學習

- [OpenSpiel](https://github.com/google-deepmind/open_spiel) — 遊戲與多代理人學習研究的開源框架。
- [PettingZoo](https://pettingzoo.farama.org/) — 多代理人強化學習的標準 API 與環境。
