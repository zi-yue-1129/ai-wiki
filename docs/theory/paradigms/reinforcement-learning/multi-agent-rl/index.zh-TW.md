---
translation_reviewed: 2026-10-28
---

# 多智能體強化學習

多個學習中的智能體在同一環境中行動，每個智能體的經驗都取決於其他智能體的行為。

## 概覽

單智能體強化學習假設環境是固定的。當其他智能體也在學習時，對每個智能體而言環境都會變得非平穩，因為其他智能體的策略在訓練中不斷改變。標準模型是馬可夫博弈（Markov game），它是馬可夫決策過程的推廣，具有聯合動作與每個智能體各自的獎勵函數。Busoniu、Babuska 與 De Schutter（2008）對此領域做了綜述，把任務分為合作、競爭與混合三類設定。

## 關鍵概念

- **非平穩性。**每個智能體的策略在訓練中都會改變，因此它所見的轉移動態也隨之改變。Lowe 等人（2017）指出，這正是經驗回放無法直接套用的原因。
- **集中式訓練、分散式執行。**訓練時智能體可以使用額外資訊，例如其他智能體的動作；測試時則只依自身觀測行動。
- **信用分配。**當一個團隊共享一個獎勵時，很難判斷哪個智能體的動作造成了該結果。
- **通訊。**當沒有事先設計通道時，智能體可以學會彼此傳送什麼，見[湧現式通訊](emergent-communication/index.md)。

## 訓練方式

- **獨立學習者**把其他智能體視為環境的一部分。實作簡單，但會受非平穩性所苦。
- **集中式評論家搭配分散式演員**，如 [MADDPG](maddpg/index.md)，讓每個智能體的價值函數能看到其他智能體的動作。
- **價值分解**，如 [QMIX](qmix/index.md)，學習每個智能體的價值，並把它們組合起來，使聯合的貪婪動作與團隊最佳動作一致。
- **共享參數的策略梯度**，如 [MAPPO](mappo/index.md)，對同質智能體使用同一個策略網路，並搭配集中式價值函數。

## 群體訓練與自我對弈

競爭與混合設定中，常常讓智能體對抗過去或對手的策略群體來訓練，見[基於種群的訓練](population-based-training/index.md)。在 OpenAI 等人（2019）中，Dota 2 團隊以自我對弈訓練：80% 的對局使用最新策略，20% 使用舊策略。OpenAI Five 在公開競技場中贏得超過 7,000 場對局中的 99.4%。Vinyals 等人（2019）報告，以多智能體強化學習在星海爭霸 II 中達到大師級表現。

## 應用

- **遊戲。**星海爭霸 II 與 Dota 2 是最有名的測試環境，如上述論文所示。
- **合作的模擬任務。**導航、通訊與獵食者–獵物任務，是集中式評論家方法的標準基準（Lowe 等人，2017）。

## 未解問題

- 隨著智能體數量增加，如何維持學習的穩定。
- 智能體如何在沒有人工設計通道的情況下學會溝通與合作。
- 當對手本身持續改變時，如何評估智能體。

## 連結

- 母頁：[強化學習](../index.md)
- 單智能體的基礎方法是[深度 Q 網路](../deep-q-networks/index.md)與[近端策略最佳化](../proximal-policy-optimisation/index.md)。

## 參考文獻

### 開創性論文

- Lowe et al. (2017), "Multi-agent actor-critic for mixed cooperative-competitive environments", [arXiv:1706.02275](https://arxiv.org/abs/1706.02275) — MADDPG, which introduces centralised critics with decentralised actors.
- Rashid et al. (2018), "QMIX: Monotonic value function factorisation for deep multi-agent reinforcement learning", *Proceedings of ICML 2018*, PMLR 80, [arXiv:1803.11485](https://arxiv.org/abs/1803.11485) — Value factorisation with a monotonic mixing network.
- Yu et al. (2022), "The surprising effectiveness of PPO in cooperative multi-agent games", NeurIPS 2022 Datasets and Benchmarks Track, [arXiv:2103.01955](https://arxiv.org/abs/2103.01955) — MAPPO, a strong PPO baseline for cooperative benchmarks.
- Vinyals et al. (2019), "Grandmaster level in StarCraft II using multi-agent reinforcement learning", *Nature* 575, 350–354. https://doi.org/10.1038/s41586-019-1724-z — Grandmaster-level StarCraft II play with multi-agent training.
- OpenAI et al. (2019), "Dota 2 with large scale deep reinforcement learning", [arXiv:1912.06680](https://arxiv.org/abs/1912.06680) — Self-play with PPO and an LSTM policy, beating the reigning world champions.

### 綜述與教科書

- Busoniu, Babuska & De Schutter (2008), "A comprehensive survey of multiagent reinforcement learning", *IEEE Transactions on Systems, Man, and Cybernetics, Part C* 38(2), 156–172. https://doi.org/10.1109/tsmcc.2007.913919 — Survey of multi-agent RL settings, learning approaches and open problems.
