---
translation_reviewed: 2026-10-28
---

# QMIX（Rashid 等人，2018）

QMIX 是一種用於合作式[多代理人強化學習](../index.md)的價值基礎方法。它為團隊中的每個代理人學出一個價值，再把這些價值組合成整個團隊的聯合價值，並加上一項限制，使每個代理人自己的貪婪選擇與最佳聯合動作保持一致。團隊以聯合價值進行訓練，執行時則只根據各自的個別價值行動。

## 概述

在合作式團隊中，每個代理人共享同一份獎勵。最自然的量是聯合動作價值 $Q_{\text{tot}}(\boldsymbol{\tau}, \mathbf{a})$，但聯合動作空間隨代理人數量呈指數成長，而去中心化的團隊需要每個代理人只靠自己能算出的量來選擇動作。價值分解提供了一條路。Sunehag 等人（2017）提出 VDN，把每個代理人的價值相加。加法很簡單，但限制了能表示的聯合價值。QMIX 保留分解的架構，但把加法換成可學習的非線性混合，並要求混合在每個代理人的價值上具有單調性，以確保去中心化執行的正確性。這個方法把[深度 Q 網路](../../deep-q-networks/index.md)延伸到多代理人情境。

## 關鍵概念

- **個別效用** $Q_a(\tau_a, a_a)$：代理人 $a$ 根據自己局部的觀測與動作歷史，為自己的動作所指定的價值。
- **混合網路**：把個別效用組合成 $Q_{\text{tot}}$。它只在訓練時使用。
- **超網路**：讀取全域狀態並輸出混合網路權重的小型網路，使混合可以依賴單一代理人看不到的資訊。
- **單調性**：當某個代理人的價值上升時，聯合價值不會下降。這使每個代理人都能依自己的價值貪婪地行動。

## 運作方式

QMIX 把聯合價值分解為

$$
Q_{\text{tot}}(\boldsymbol{\tau}, \mathbf{a}; \theta) = f_{\text{mix}}\big(Q_1(\tau_1, a_1), \dots, Q_n(\tau_n, a_n); s\big), \qquad \frac{\partial Q_{\text{tot}}}{\partial Q_a} \ge 0 \;\; \text{對每個代理人 } a \text{ 皆成立},
$$

其中 $s$ 是全域狀態。單調性條件意味著聯合貪婪動作等於每個代理人貪婪動作的組合，這正是去中心化執行得以成立的一致性。在論文的架構中，混合權重透過對超網路輸出取絕對值而保持非負，這是單調性的充分條件；偏置項則不受限制。

訓練使用深度 Q 學習中常見的聯合價值損失，並搭配目標網路與經驗回放：

$$
L(\theta) = \mathbb{E}\Big[\big(r + \gamma \max_{\mathbf{a}'} Q_{\text{tot}}^{-}(\boldsymbol{\tau}', \mathbf{a}'; \theta^{-}) - Q_{\text{tot}}(\boldsymbol{\tau}, \mathbf{a}; \theta)\big)^2\Big]。
$$

演算法的步驟如下：

1. 每個代理人的效用網路根據自己的觀測歷史計算 $Q_a$。
2. 超網路讀取全域狀態，產生混合權重。
3. 混合網路把各個效用組合成 $Q_{\text{tot}}$。
4. 在一批儲存的轉移上最小化損失，並定期更新目標網路。
5. 執行時，每個代理人取自己 $Q_a$ 的最大值。不使用混合網路。

## 結果

論文的主要證據來自星海爭霸多代理人挑戰（StarCraft Multi-Agent Challenge，SMAC），這是一組微操情境，要求一支單位團隊擊敗內建的對手。論文報告，QMIX 在這些地圖上的表現優於 VDN 與策略梯度方法 COMA，而差距最大的是最需要協調的情境。確切的勝率請見論文。

## 限制

- **表示能力受限。** 單調性限制了能表示的聯合價值。Son 等人（2019）指出，有些可分解的任務無法以此方式表示，並提出 QTRAN 來填補這個缺口。
- **僅適用共享獎勵。** QMIX 假設團隊共享獎勵。競爭或混合動機的情境需要其他方法，例如 [MADDPG](../maddpg/index.md)。
- **訓練時需要全域狀態。** 超網路使用全域狀態，因此訓練時必須能取得它。
- **離散動作。** 這種以價值為基礎的設計無法直接處理連續動作空間。

## 開放問題

非單調的、表示能力更強的分解，能否泛化得更好，還是只能擬合訓練用的團隊？Papoudakis 等人（2020）在共同任務上比較了各類價值分解方法，使我們能追問混合網路在實務上究竟增加了多少效益。另一個問題是，QMIX 式的價值分解如何與 Yu 等人（2021）研究的 PPO 變體等同策略方法結合。

## 參考文獻

### 開創性論文

- Rashid, T. 等人 (2018). *QMIX: Monotonic Value Function Factorisation for Deep Multi-Agent Reinforcement Learning*. arXiv:1803.11485. https://arxiv.org/abs/1803.11485 — QMIX 論文，以全域狀態為條件的單調網路混合各個代理人的價值。
- Sunehag, P. 等人 (2017). *Value-Decomposition Networks For Cooperative Multi-Agent Learning*. arXiv:1706.05296. https://arxiv.org/abs/1706.05296 — VDN，把團隊價值分解為各代理人價值的總和，並指出懶惰代理人問題。
- Son, K. 等人 (2019). *QTRAN: Learning to Factorize with Transformation for Cooperative Multi-Agent Reinforcement Learning*. arXiv:1905.05408. https://arxiv.org/abs/1905.05408 — 指出 VDN 與 QMIX 只能涵蓋部分可分解的任務，並提出避開其結構限制的分解方法。
- Foerster, J. 等人 (2017). *Counterfactual Multi-Agent Policy Gradients*. arXiv:1705.08926. https://arxiv.org/abs/1705.08926 — COMA，以中心化評論家搭配去中心化的演員，在此作為 SMAC 上的比較方法。

### 文章與文件

- Yu, C. 等人 (2021). *The Surprising Effectiveness of PPO in Cooperative, Multi-Agent Games*. arXiv:2103.01955. https://arxiv.org/abs/2103.01955 — 顯示基於 PPO 的多代理人方法在合作式基準上表現強勁，包括星海爭霸任務。
- Papoudakis, G. 等人 (2020). *Benchmarking Multi-Agent Deep Reinforcement Learning Algorithms in Cooperative Tasks*. arXiv:2006.07869. https://arxiv.org/abs/2006.07869 — 在共同的合作式任務上比較獨立學習、中心化策略梯度，以及包括 QMIX 在內的價值分解方法。
