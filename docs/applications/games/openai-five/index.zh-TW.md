---
status: draft
last_reviewed: 2026-10-28
aliases:
  - OpenAI Five
  - Dota 2 AI
---

# OpenAI Five（OpenAI et al., 2019）

OpenAI Five 是由五個神經網路代理人組成的隊伍，透過自我對弈學會玩 Dota 2。2019 年，它在三戰兩勝的比賽中擊敗了在位的世界冠軍。它是[遊戲](../index.md)里程碑中的 Dota 2 項目。

## 問題

Dota 2 是五對五的團隊遊戲，具有長時間跨度、因戰爭迷霧而不完全的資訊，以及大型連續的動作空間。問題在於：在這樣的遊戲中，自我對弈的強化學習能否達到超人水準，而且規模遠超過先前的遊戲系統。

## 核心想法

每位英雄由一個帶 LSTM 記憶的策略網路控制。網路讀取經過處理的遊戲畫面，輸出動作。代理人透過與自己的副本對弈而學習，約 20% 的對局與較舊版本的策略對戰。獎賞會以對方隊伍的獎賞做對稱化處理，因此代理人學的是獲勝，而不是最大化個人得分。

## 方程式或演算法

訓練使用近端策略最佳化（PPO），這是一種裁剪的策略梯度方法（[Schulman et al., 2017](#參考文獻)）。訓練流程是分散式的：

1. 執行 Dota 2 引擎的模擬機（CPU）把觀測送給前向推論 GPU，由後者選擇動作。
2. 經驗存入緩衝區，最佳化 GPU 以 PPO 在一百萬到三百萬個時間步的大批次上更新參數，尖峰時使用多達 1,536 張 GPU。
3. 更新後的參數會被發布，之後的模擬使用最新版本。

## 結果

本頁的數據來自論文。論文描述的是一次連續的訓練：從 2018 年 6 月到 2019 年 4 月，實際時間約十個月，訓練 180 天，模型參數超過 1.5 億。

- 2019 年 4 月，OpenAI Five 在三戰兩勝的比賽中擊敗了在位世界冠軍 OG。
- 2019 年 4 月 18 日至 21 日，對公眾開放的競技場中，OpenAI Five 在 7,257 場對戰（對手為 3,193 支隊伍）中取得 99.4% 的勝率。有 29 支隊伍在 42 場比賽中擊敗它。論文指出，許多人類玩家會放棄落後的比賽，因此這個數字並不完全精確。

## 限制

- 代理人玩的是受限版本的遊戲：它只支援 117 位英雄中的 17 位，而且不能使用讓單一玩家同時控制多個單位的道具。
- 在競技場中獲勝，並不代表它對遊戲有廣泛的理解。競技場的目的是測試創意或分佈外的打法能否利用這個系統，而且確實有隊伍擊敗了它。
- 訓練使用約 770 PFlop/s-days 的運算量，很少有團隊能夠重現。

## 關聯

- [近端策略最佳化](../../../theory/paradigms/reinforcement-learning/proximal-policy-optimisation/index.md)：訓練所用的演算法。
- [強化學習](../../../theory/paradigms/reinforcement-learning/index.md)：從獎賞中學習的整體方法家族。

## 參考文獻

### 開創性論文

- OpenAI et al. (2019). Dota 2 with Large Scale Deep Reinforcement Learning. arXiv. https://arxiv.org/abs/1912.06680 — 描述 OpenAI Five、其訓練系統、結果與限制。
- Schulman et al. (2017). Proximal Policy Optimization Algorithms. arXiv. https://arxiv.org/abs/1707.06347 — 用於訓練代理人的 PPO 演算法。
- Silver et al. (2016). Mastering the game of Go with deep neural networks and tree search. *Nature*. https://doi.org/10.1038/nature16961 — AlphaGo，論文拿來比較規模的早期自我對弈系統。
- Vinyals et al. (2019). Grandmaster level in StarCraft II using multi-agent reinforcement learning. *Nature*. https://doi.org/10.1038/s41586-019-1724-z — 同期的多代理人遊戲系統，以聯盟式自我對弈訓練。

### 綜述與教科書

- Yannakakis & Togelius (2018). *Artificial Intelligence and Games*. Springer. https://doi.org/10.1007/978-3-319-63519-4 — 遊戲 AI 的教科書，包含自我對弈與多代理人方法。
