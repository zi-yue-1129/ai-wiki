---
translation_reviewed: 2026-10-28
---

# 強化學習

## 直覺

代理人（agent）在環境中行動，得到**獎勵**，目標是學出能最大化**長期累積獎勵**的策略。沒有人告訴它正確答案，只能從試誤中學習。這和動物學習（操作制約）以及大腦的多巴胺系統有深刻的對應。

![強化學習動畫：代理人觀察環境、採取行動、收到獎勵並更新策略。](../../../assets/concept-animations/agent-environment.gif)

*代理人與環境互動的概念動畫（原創，CC BY-SA 4.0）。* 代理人接收觀察、選擇行動，再取得後續狀態的觀察與獎勵；網格路徑只是示例。**獎勵是行動後果的回饋，不是「正確動作」標籤**。實際的策略更新取決於演算法。

## 形式化：馬可夫決策過程（MDP）

MDP 由 \((S, A, P, R, \gamma)\) 組成：狀態、行動、轉移機率、獎勵函數、折扣因子。

- **策略** \(\pi(a\mid s)\)：在狀態 s 選行動 a 的機率
- **回報** \(G_t = \sum_{k=0}^\infty \gamma^k r_{t+k+1}\)
- **狀態價值** \(V^\pi(s) = \mathbb{E}_\pi[G_t\mid s_t=s]\)
- **行動價值** \(Q^\pi(s,a) = \mathbb{E}_\pi[G_t\mid s_t=s, a_t=a]\)

**貝爾曼方程**：

\[
Q^*(s,a) = \mathbb{E}\big[r + \gamma \max_{a'} Q^*(s',a')\big]
\]

## 核心演算法家族

| 家族 | 代表演算法 | 想法 |
|---|---|---|
| 動態規劃 | 價值迭代、策略迭代 | 已知環境模型時直接解貝爾曼方程 |
| 蒙地卡羅 | MC 控制 | 跑完整回合再用實際回報更新 |
| 時序差分（TD） | TD(0)、SARSA、Q-learning | 用「下一步估計」自舉更新 |
| 深度價值方法 | DQN、Double DQN、Rainbow | 用神經網路近似 Q |
| 策略梯度 | REINFORCE | 直接對策略參數做梯度上升 |
| Actor-Critic | A2C/A3C、PPO、SAC、TD3 | 策略（actor）＋價值估計（critic） |
| 模型式 RL | Dyna、MuZero、Dreamer | 學環境模型，在模型中規劃或想像 |
| 離線 RL | CQL、IQL、Decision Transformer | 只用既有資料學習，不與環境互動 |
| 多代理人 RL | MADDPG、QMIX、自我對弈 | 多個代理人互動 |

**TD 誤差**是關鍵量：

\[
\delta_t = r_{t+1} + \gamma V(s_{t+1}) - V(s_t)
\]

## 強化學習與大腦

### 多巴胺＝獎勵預測誤差

Schultz、Dayan 與 Montague（1997）發現：中腦多巴胺神經元的放電模式和 TD 誤差 \(\delta\) 幾乎一致——

- 意外得到獎勵 → 多巴胺爆發（\(\delta > 0\)）
- 學會預測後，獎勵本身不再引起反應，反應轉移到**預測線索**上
- 預期的獎勵沒來 → 多巴胺低於基線（\(\delta < 0\)）

這是計算理論與神經科學最成功的交會之一。後續的**分布式強化學習**（Distributional RL）也在多巴胺神經元中找到對應：不同神經元似乎編碼不同樂觀程度的預測（Dabney et al., 2020, *Nature*）。

### 其他對應

| RL 概念 | 大腦／心理學對應 |
|---|---|
| 無模型（model-free） | 習慣性行為，背外側紋狀體 |
| 模型式（model-based） | 目標導向行為，前額葉與背內側紋狀體 |
| Actor-Critic | 背側紋狀體（actor）與腹側紋狀體（critic）假說 |
| 經驗回放 | 海馬迴在睡眠與休息時的序列重播（replay） |
| 探索—利用權衡 | 正腎上腺素系統、前額葉；人類決策研究 |
| 好奇心／內在動機 | 新奇性驅動的探索、資訊尋求 |
| 折扣因子 | 延遲折扣、衝動性研究 |
| 繼承表徵（successor representation） | 海馬迴位置細胞的預測性地圖（Stachenfeld et al., 2017） |

心理學背景：Thorndike 效果律、Skinner 操作制約、Rescorla-Wagner 模型（1972，本身就是預測誤差學習規則）。

## 關鍵方法

每個方法各有專頁，此處的概述與比較從簡。

### 深度 Q 網路（Mnih 等人，2015）

- **概述：** 卷積網路從原始畫面近似動作價值函數，並以經驗回放與目標網路穩定訓練。
- **比較：** 價值基礎的路線。價值基礎方法頁涵蓋整個家族；下方的 PPO 則走策略基礎的路線。
- **完整內容：** [深度 Q 網路](deep-q-networks/index.md)

### 近端策略最佳化（Schulman 等人，2017）

- **概述：** 一種策略梯度方法，裁剪新舊策略的機率比，使每次更新都保持在舊策略附近。
- **比較：** 策略基礎的路線，比信任區域方法簡單。它是同策略的，與離線強化學習頁形成對比。
- **完整內容：** [近端策略最佳化](proximal-policy-optimisation/index.md)

### AlphaGo 與 AlphaZero（Silver 等人，2016、2018）

- **概況：** 以學習得到的網路進行搜尋。AlphaGo 結合策略網路與價值網路及蒙地卡羅樹搜尋，並以人類棋譜起步。AlphaZero 僅靠自我對弈學習，只依各遊戲的規則。
- **比較：** 以搜尋為基礎的對弈路線。兩者都列於圍棋與棋類遊戲的里程碑中，而 [MuZero](model-based-rl/muzero/index.md) 把同一套搜尋延伸到規則不交給規劃器的遊戲。
- **完整內容：** [AlphaGo](alphago/index.md)、[AlphaZero](alphazero/index.md)

## 里程碑

- **TD-Gammon**（1992）
- **DQN**（2013/2015）：從像素學會玩 Atari
- **[AlphaGo](alphago/index.md) / [AlphaZero](alphazero/index.md) / [MuZero](model-based-rl/muzero/index.md)**（2016–2019）：自我對弈＋蒙地卡羅樹搜尋
- **OpenAI Five、AlphaStar**（2019）：Dota 2、星海爭霸 II
- **RLHF**（2017 起，2022 ChatGPT 普及）：用人類偏好訓練獎勵模型再以 PPO 微調 LLM
- **推理模型的 RL**（2024–2025）：以可驗證獎勵（數學答案、程式測試）訓練長思維鏈，例如 DeepSeek-R1 使用的 GRPO
- **機器人**：模擬到真實（sim-to-real）、四足與人形機器人行走

## 實務挑戰

- 樣本效率低
- 獎勵設計困難，容易出現**獎勵駭客**（reward hacking）：代理人找到獲得高分但違背設計者本意的捷徑（見 [AI 安全](../../../society/safety-alignment/index.md)）
- 探索困難（稀疏獎勵）
- 訓練不穩定、對超參數敏感
- 模擬與真實的差距

## 學習資源

- Sutton & Barto《Reinforcement Learning: An Introduction》第二版（免費 PDF）
- David Silver UCL RL 課程
- OpenAI [Spinning Up](https://spinningup.openai.com/)（MIT）
- Hugging Face Deep RL Course
- [Gymnasium](https://gymnasium.farama.org/)、[Stable-Baselines3](https://stable-baselines3.readthedocs.io/)
- Niv (2009) "Reinforcement learning in the brain"（神經科學觀點綜述）

## 參考文獻

### 開創性論文

- Mnih et al. (2015), "Human-level control through deep reinforcement learning", *Nature* 518. https://doi.org/10.1038/nature14236 — DQN 論文，開啟了大規模深度強化學習的起點。
- Silver et al. (2016), "Mastering the game of Go with deep neural networks and tree search", *Nature* 529. https://research.google/pubs/mastering-the-game-of-go-with-deep-neural-networks-and-tree-search/ — AlphaGo，結合學習得到的網路與搜尋。
- Christiano et al. (2017), "Deep reinforcement learning from human preferences", NeurIPS, [arXiv:1706.03741](https://arxiv.org/abs/1706.03741) — 從人類的成對比較中學習獎勵函數，是 RLHF 的基礎。
- Schulman et al. (2017), "Proximal policy optimization algorithms", [arXiv:1707.06347](https://arxiv.org/abs/1707.06347) — PPO，實務上最常用的策略梯度方法。

### 綜述與教科書

- Sutton, R. S. & Barto, A. G. *Reinforcement Learning: An Introduction*, 2nd ed. MIT Press, 2018. http://incompleteideas.net/book/the-book-2nd.html — 標準強化學習教科書，提供免費線上草稿，涵蓋上方表格中的演算法家族。
- Levine, S., Kumar, A., Tucker, G. & Fu, J. (2020), "Offline reinforcement learning: tutorial, review, and perspectives on open problems", [arXiv:2005.01643](https://arxiv.org/abs/2005.01643) — 從固定資料集學習的教學與綜述。
