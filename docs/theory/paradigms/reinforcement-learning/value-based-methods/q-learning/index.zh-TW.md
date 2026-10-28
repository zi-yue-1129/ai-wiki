---
status: complete
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
aliases:
  - Q-learning
  - Q 學習
---

# Q 學習（Watkins 與 Dayan，1992）

一種離策略的時序差分方法：無需環境模型，即可從取樣的轉換中學習最佳動作價值。

## 問題

不知道轉移機率的智能體，需要僅憑經驗學會在每個狀態下哪個動作最好。動態規劃需要模型，蒙地卡羅方法則必須等待完整的回合結束。問題在於：如何從取樣經驗中學習最佳動作價值，並在每一步之後更新。

## 核心想法

維護一張動作價值表 \(Q(x, a)\)。每一步之後，若狀態為 \(x\)、動作為 \(a\)、獎勵為 \(r\)、下一狀態為 \(y\)，就把 \(Q(x, a)\) 朝 \(r + \gamma \max_b Q(y, b)\) 移動。目標在下一狀態取貪婪的最大值，而不論智能體接下來實際採取哪個動作。因此，即使智能體以另一個策略探索，學到的價值仍描述最佳策略。

## 方程式與演算法

Watkins 與 Dayan 以依該配對造訪次數而定的學習因子 \(\alpha_n\) 寫出更新式：

\[
Q_n(x,a) = (1 - \alpha_n)\, Q_{n-1}(x,a) + \alpha_n \left[ r_n + \gamma \max_b Q_{n-1}(y_n, b) \right]
\]

此式適用於在第 \(n\) 步被造訪的配對 \((x, a)\)，其他配對則不變。流程如下：

1. 為所有配對初始化 \(Q(s, a)\)。
2. 從狀態 \(s\) 開始一個回合。
3. 依探索規則從 \(s\) 選擇 \(a\)，例如依 \(Q\) 的 ε-貪婪策略。
4. 執行 \(a\)，觀察 \(r\) 與下一狀態 \(s'\)。
5. 更新 \(Q(s, a) \leftarrow Q(s, a) + \alpha \left[ r + \gamma \max_{b} Q(s', b) - Q(s, a) \right]\)。
6. 令 \(s \leftarrow s'\)，重複直到回合結束。

**收斂。** Watkins 與 Dayan 證明，若滿足以下條件，\(Q_n\) 以機率 1 收斂到 \(Q^*\)：每個狀態–動作配對都被無限次造訪；獎勵有界；每個配對的學習率滿足 \(0 \le \alpha_n < 1\)、\(\sum_n \alpha_n = \infty\) 且 \(\sum_n \alpha_n^2 < \infty\)；且 \(0 < \gamma < 1\)。Tsitsiklis（1994）以非同步隨機逼近證明了相同的收斂性。

## 結果

Watkins 與 Dayan 的貢獻是收斂定理，而非實證基準。它的實際影響來自函數逼近：深度 Q 網路以神經網路使用相同的最大值目標，並在許多 Atari 遊戲上達到人類水準（Mnih 等人，2015）。

## 限制

- **表格形式。** 為每個狀態–動作配對存一筆表格項目，對大型或連續的空間並不實際。
- **最大化偏差。** 對含雜訊估計取最大值，傾向於高估價值。Double DQN 論文報告，DQN 在測試的全部 49 款 Atari 遊戲中都有高估（van Hasselt 等人，2016）。
- **收斂條件。** 此保證需要每個配對被無限次造訪，並需要特定的學習率排程。這兩個假設在實務中都可能不成立；而使用函數逼近時，此保證不再成立。

## 關聯

- 上層主題：[基於價值的方法](../index.zh-TW.md)，以及更廣的[強化學習](../../index.zh-TW.md)概觀。
- 其深度版本是[深度 Q 網路](../../deep-q-networks/index.zh-TW.md)。高估的修正方法是 [Double DQN](../double-dqn/index.zh-TW.md)。
- 同策略的對應方法是 [SARSA](../sarsa/index.zh-TW.md)，它學習的是實際所遵循策略的價值。
- 更新中使用的時序差分誤差，是上層頁面中與多巴胺相關的訊號。

## 應用

- **教學與小型離散問題**，例如格子世界，其表格小到可以儲存。格子世界是表格方法常見的教學範例（Sutton 與 Barto，2018）。

## 未解問題

- 在函數逼近下的穩定離策略學習，此時收斂保證不再成立。
- 在雜訊下取得可靠的價值估計，同時避免高估偏差。

## 參考文獻

### 開創性論文

- Watkins 與 Dayan（1992），"Q-learning"，*Machine Learning* 8(3–4), 279–292。https://doi.org/10.1007/bf00992698 — 定義 Q 學習並證明其收斂到最佳動作價值的論文。
- Tsitsiklis（1994），"Asynchronous stochastic approximation and Q-learning"，*Machine Learning* 16(3), 185–202。https://doi.org/10.1007/bf00993306 — 以非同步隨機逼近證明 Q 學習的收斂性。
- Mnih 等人（2015），"Human-level control through deep reinforcement learning"，*Nature* 518, 529–533。https://doi.org/10.1038/nature14236 — Q 學習的深度版本，包含回放與目標網路。
- van Hasselt、Guez 與 Silver（2016），"Deep reinforcement learning with double Q-learning"，[arXiv:1509.06461](https://arxiv.org/abs/1509.06461)（2015 年提交至 arXiv）— 顯示 DQN 會高估動作價值，並降低此偏差。
- Mnih 等人（2013），"Playing Atari with deep reinforcement learning"，[arXiv:1312.5602](https://arxiv.org/abs/1312.5602) — 早期預印本，將以 Q 學習為基礎的網路應用於原始 Atari 畫面。

### 綜述與教科書

- Sutton, R. S. & Barto, A. G. *Reinforcement Learning: An Introduction*，第 2 版。MIT Press, 2018。http://incompleteideas.net/book/the-book-2nd.html — 在時序差分章節中介紹表格式 Q 學習及其收斂背景。
