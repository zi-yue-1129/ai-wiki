---
translation_reviewed: 2026-10-28
---

# 保守 Q 學習（Kumar 等人，2020）

一種離線強化學習方法，學習刻意保持悲觀的 Q 函數。它加入一個懲罰，降低資料集未涵蓋的動作的價值，使學到的策略價值成為其真實價值的下界。

## 問題

在離線強化學習中，智能體只能從其他策略收集的固定資料集學習。標準的離策略方法會從下一個動作的價值進行自舉（bootstrap），而該動作可能完全不在資料集中。這類動作學到的 Q 值沒有任何資料加以修正，因此可能被高估。策略會追逐這些高估的值，表現因此崩潰。Kumar 等人直接處理這種分布偏移。

## 核心想法

CQL 在標準的貝爾曼誤差之外加入一個正則項：一方面把策略取樣的動作的 Q 值壓低，另一方面把資料集中動作的 Q 值推高。結果是一個對分布外動作給出比分布內動作更低價值的 Q 函數，使策略保持接近資料。作者證明，策略在學到的 Q 函數下的期望值，是其真實價值的下界，而且這個界可用於具有改進保證的策略學習程序。

這個正則項很容易加到既有的深度 Q 學習或演員–評論家實作中，這也是此方法廣泛被使用的原因之一。

## 方程式或演算法

Q 函數的更新最小化貝爾曼誤差加上保守懲罰，形式如下：

\[
\min_Q \; \alpha\, \mathbb{E}_{s \sim \mathcal{D}}\left[\log \sum_a \exp Q(s,a) - \mathbb{E}_{a \sim \hat{\pi}_\beta(a\mid s)}[Q(s,a)]\right] + \tfrac{1}{2}\mathbb{E}_{(s,a,s') \sim \mathcal{D}}\left[(Q(s,a) - \hat{\mathcal{B}}^\pi Q(s,a))^2\right] ,
\]

其中 \(\alpha\) 控制懲罰的強度，\(\hat{\pi}_\beta\) 是由資料估計的行為策略，\(\hat{\mathcal{B}}^\pi\) 是目前策略的貝爾曼運算子。第一項降低資料不偏好之動作的價值，第二項使 Q 函數與資料保持一致。

## 結果

論文在離散與連續動作的離線基準上報告結果，並指出 CQL「學到一個保守的 Q 函數，使策略在此 Q 函數下的期望值成為其真實價值的下界」。實驗與離策略方法比較；後者在離線資料上可能因高估問題而失敗。

## 限制

- **悲觀。** 保守估計可能低估好的動作，因此表現可能低於資料所能支持的程度。
- **超參數敏感。** 懲罰權重 \(\alpha\) 需要調整，其最佳值取決於資料集。
- **覆蓋範圍。** 當資料涵蓋的有用動作很少時，下界也很低，改進空間有限。

## 關聯

- 上層主題：[離線強化學習](../index.md)。
- CQL 建立在[深度 Q 網路](../../deep-q-networks/index.md)的價值學習之上，並與 [SAC](../../policy-gradient-and-actor-critic/sac/index.md) 等演員–評論家方法相關。
- 它處理與批次約束方法（BCQ，Fujimoto 等人，2019）相同的問題，後者將動作限制在與資料相似的範圍內。
- [隱式 Q 學習](../iql/index.md)完全避免查詢未見過的動作，[決策 Transformer](../decision-transformer/index.md)則完全避免價值學習。

## 應用

- **機器人學**，從記錄資料學習，因為新的探索成本很高。

## 未解問題

- 如何在沒有線上評估的情況下選擇懲罰權重。
- 如何在保持悲觀的同時，超越資料所能支持的表現。

## 參考文獻

### 奠基性論文

- Kumar, Zhou, Tucker & Levine（2020），"Conservative Q-learning for offline reinforcement learning"，[arXiv:2006.04779](https://arxiv.org/abs/2006.04779)——CQL 論文，包含保守懲罰、下界結果與離線實驗。
- Fujimoto, Meger & Precup（2019），"Off-policy deep reinforcement learning without exploration"，[arXiv:1812.02900](https://arxiv.org/abs/1812.02900)——批次約束 Q 學習，將策略限制在與資料相似的動作上。
- Fu, Kumar, Nachum, Tucker & Levine（2020），"D4RL: Datasets for deep data-driven reinforcement learning"，[arXiv:2004.07219](https://arxiv.org/abs/2004.07219)——標準的離線資料集與基準，用於比較離線方法。
- Kostrikov, Nair & Levine（2021），"Offline reinforcement learning with implicit Q-learning"，[arXiv:2110.06169](https://arxiv.org/abs/2110.06169)——另一種離線方法，從不評估資料集之外的動作。
- Chen 等人（2021），"Decision Transformer: Reinforcement learning via sequence modeling"，[arXiv:2106.01345](https://arxiv.org/abs/2106.01345)——將強化學習視為序列建模的離線方法，用於比較。
