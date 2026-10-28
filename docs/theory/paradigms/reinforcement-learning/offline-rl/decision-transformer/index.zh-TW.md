---
translation_reviewed: 2026-10-28
---

# 決策 Transformer（Chen 等人，2021）

一種離線強化學習方法，把決策視為序列建模。在軌跡上訓練一個因果遮罩的 Transformer，測試時以期望回報為條件，使它生成朝向該回報的動作。它不學習價值函數。

## 問題

以價值為基礎的離線方法必須估計資料未涵蓋的動作價值，而策略梯度方法則需要許多同策略樣本。Chen 等人探討：支撐大型語言模型的序列建模工具，能否同時取代這兩者。想法是把強化學習抽象為序列問題：給定過去的狀態、動作與期望回報，預測下一個動作。

## 核心想法

每條軌跡被寫成一串 token，每個時間步貢獻三個項目：回報至終（return-to-go，即智能體希望獲得的未來獎勵總和）、狀態與動作。一個因果遮罩的 Transformer 被訓練來從前面的 token 預測每個動作，這就是在記錄軌跡上的監督式學習。測試時，智能體從一個高的期望回報開始，附加每個觀測到的狀態，並取樣下一個動作；接著依收到的獎勵更新回報至終。

由於期望回報扮演生成提示的角色，同一個訓練好的模型可以被要求達到不同的表現水準。此方法不需要貝爾曼備份，也不需要價值估計。

## 方程式或演算法

模型被訓練以最大化記錄動作在前面 token 條件下的似然：

\[
\mathcal{L} = -\mathbb{E}_{\tau \sim \mathcal{D}}\left[\sum_t \log \pi_\theta(a_t \mid \hat{R}_t, s_t, \hat{R}_{t-1}, \ldots, s_1)\right],
\]

其中 \(\hat{R}_t = \sum_{t' \ge t} r_{t'}\) 是記錄軌跡的回報至終。評估時，\(\hat{R}_1\) 設為期望回報，並隨每個觀測到的獎勵遞減回報至終。

## 結果

摘要指出，Decision Transformer「在 Atari、OpenAI Gym 與 Key-to-Door 任務上，達到或超過最先進的無模型離線 RL 基準」。論文在這些基準上與保守型與以價值為基礎的離線方法比較。

## 限制

- **以回報為條件。** 必須選擇期望回報。論文以資料集中最大回報的倍數來縮放回報至終，並指出還有更有原則的條件設定方式。
- **上下文長度。** Transformer 只看見固定窗口的過去 token，限制了它能使用的歷史長度。

## 關聯

- 上層主題：[離線強化學習](../index.md)。
- 它是以價值為基礎的離線方法（如 [CQL](../cql/index.md) 與 [IQL](../iql/index.md)）的序列模型替代方案。
- 序列模型的想法與 Transformer 架構相關，見 [Transformer 模型家族](../../../../models/transformer/index.md)；它也與[模仿學習](../../../imitation/index.md)相關，因為它以示範上的監督式預測來訓練。

## 應用

- **Atari 遊戲**，從記錄的遊玩中學習，如論文實驗所示。
- **控制任務**，從記錄軌跡學習，論文在 OpenAI Gym 上評估。

## 未解問題

- 如何把序列建模與價值學習結合，使模型能拼接軌跡片段。
- 如何為新任務選擇期望回報。

## 參考文獻

### 奠基性論文

- Chen 等人（2021），"Decision Transformer: Reinforcement learning via sequence modeling"，[arXiv:2106.01345](https://arxiv.org/abs/2106.01345)——Decision Transformer 論文，包含以回報為條件的序列模型，以及 Atari、Gym 與 Key-to-Door 結果。
- Kumar, Zhou, Tucker & Levine（2020），"Conservative Q-learning for offline reinforcement learning"，[arXiv:2006.04779](https://arxiv.org/abs/2006.04779)——以價值為基礎的離線方法，與序列建模比較。
- Kostrikov, Nair & Levine（2021），"Offline reinforcement learning with implicit Q-learning"，[arXiv:2110.06169](https://arxiv.org/abs/2110.06169)——避免查詢未見動作的以價值為基礎離線方法。
- Fu, Kumar, Nachum, Tucker & Levine（2020），"D4RL: Datasets for deep data-driven reinforcement learning"，[arXiv:2004.07219](https://arxiv.org/abs/2004.07219)——用於比較離線方法的離線基準套件。
- Fujimoto, Meger & Precup（2019），"Off-policy deep reinforcement learning without exploration"，[arXiv:1812.02900](https://arxiv.org/abs/1812.02900)——批次約束 Q 學習，作為離線基準。
