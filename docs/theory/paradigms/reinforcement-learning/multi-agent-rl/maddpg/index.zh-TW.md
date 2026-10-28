---
translation_reviewed: 2026-10-28
---

# 多智能體深度確定性策略梯度（Lowe 等人，2017）

一種集中式評論家的方法：訓練時，每個智能體的評論家能看到所有智能體的觀測與動作；執行時，每個演員只使用自身的觀測。

## 問題

獨立學習者所面對的環境是非平穩的，因為其他智能體不斷改變。經驗回放也因同樣的原因變得不可靠。Lowe 等人探討：在混合的合作與競爭設定中，若訓練時能使用測試時無法取得的額外資訊，智能體是否能學會協調的行為。

## 核心想法

論文採用集中式訓練、分散式執行。每個智能體 \(i\) 有一個演員 \(\mu_i\)，把其局部觀測 \(o_i\) 映射為動作；還有一個評論家 \(Q_i\)，其輸入為狀態資訊 \(x\) 與所有智能體的動作。最簡單的情況是 \(x = (o_1, \ldots, o_N)\)。由於評論家知道其他智能體的動作，從它的角度看，環境是平穩的，即使其他策略仍在改變。演員透過自身的評論家，以確定性策略梯度訓練，如同 [DDPG](../../policy-gradient-and-actor-critic/ddpg/index.md)。

論文還提出兩項擴充。策略集成為每個智能體訓練 \(K\) 個子策略，並在每個回合隨機選一個。策略推論則在其他智能體的策略未知時，從觀測中學習它們的近似模型。

## 方程式或演算法

對智能體 \(i\)，演員的更新是透過集中式評論家的確定性策略梯度：

\[
\nabla_{\theta_i} J(\mu_i) = \mathbb{E}_{x, \mathcal{D}}\left[\nabla_{\theta_i}\mu_i(o_i)\, \nabla_{a_i} Q_i^{\mu}(x, a_1, \ldots, a_N)\big|_{a_i = \mu_i(o_i)}\right]
\]

評論家以由目標演員建立的時序差分目標訓練，與 DDPG 相同。流程如下：

1. 讓目前的演員各依自身觀測行動，並儲存聯合轉移。
2. 從回放緩衝區取樣一批聯合轉移。
3. 以其集中式目標更新每個評論家 \(Q_i\)。
4. 以透過評論家的梯度更新每個演員 \(\mu_i\)。
5. 緩慢更新目標網路，然後重複。

## 結果

論文在六個多智能體環境上評估：合作通訊、合作導航、保持距離、物理欺騙、獵食者–獵物，以及隱蔽通訊。論文報告：「在所有情況下，當直接與 DDPG 對抗時，MADDPG 都更勝一籌」。在合作通訊中，使用 MADDPG 的智能體有 84.0% 的回合能抵達目標，而 DDPG 為 32.0%。作者也報告，使用策略集成的智能體比只有單一策略的更強。

## 限制

- **集中式資訊。**訓練需要其他智能體的動作與觀測，這在某些部署情境中可能無法取得。
- **擴展性。**評論家的輸入隨智能體數量增加，聯合動作空間也隨之增長。
- **推論的策略。**若其他策略無法觀測，近似策略推論會帶來額外誤差。
- **連續動作。**此方法繼承了 DDPG 的連續動作設定，其確定性演員需要探索雜訊。

## 連結

- 母頁：[多智能體強化學習](../index.md)，以及更大範圍的[強化學習](../../index.md)總覽。
- 每個智能體的演員與評論家建立在 [DDPG](../../policy-gradient-and-actor-critic/ddpg/index.md) 之上。
- 離散動作的價值方法替代方案是 [QMIX](../qmix/index.md)，共享參數的 PPO 替代方案是 [MAPPO](../mappo/index.md)。

## 應用

- **合作的模擬任務。**論文用來檢驗協調能力的導航與通訊任務。
- **混合設定。**獵食者–獵物與保持距離等任務，團隊與對手同時學習。

## 未解問題

- 如何把集中式評論家擴展到大量智能體。
- 當其他智能體的策略無法觀測時，如何可靠地推論它們的策略。

## 參考文獻

### 開創性論文

- Lowe et al. (2017), "Multi-agent actor-critic for mixed cooperative-competitive environments", [arXiv:1706.02275](https://arxiv.org/abs/1706.02275) — The MADDPG paper, with the centralised critic, the ensemble extension and the results above.
- Lillicrap et al. (2016), "Continuous control with deep reinforcement learning", ICLR, [arXiv:1509.02971](https://arxiv.org/abs/1509.02971) — DDPG, the single-agent method that each MADDPG agent uses.
- Rashid et al. (2018), "QMIX: Monotonic value function factorisation for deep multi-agent reinforcement learning", *Proceedings of ICML 2018*, PMLR 80, [arXiv:1803.11485](https://arxiv.org/abs/1803.11485) — A value-based alternative for cooperative teams.
- Yu et al. (2022), "The surprising effectiveness of PPO in cooperative multi-agent games", NeurIPS 2022 Datasets and Benchmarks Track, [arXiv:2103.01955](https://arxiv.org/abs/2103.01955) — A strong on-policy baseline with a centralised value function.
- Busoniu, Babuska & De Schutter (2008), "A comprehensive survey of multiagent reinforcement learning", *IEEE Transactions on Systems, Man, and Cybernetics, Part C* 38(2), 156–172. https://doi.org/10.1109/tsmcc.2007.913919 — Survey of multi-agent learning settings and their difficulties.
