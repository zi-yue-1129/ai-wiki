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

## 學習資源

- Yannakakis & Togelius，*Artificial Intelligence and Games*（可免費下載 PDF）
- [OpenSpiel](https://github.com/google-deepmind/open_spiel)、[PettingZoo](https://pettingzoo.farama.org/)
- Silver et al. (2016, 2018)，AlphaGo 與 AlphaZero 論文
