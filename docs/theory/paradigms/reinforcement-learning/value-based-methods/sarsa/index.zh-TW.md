---
status: complete
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
aliases:
  - SARSA
  - 同策略時序差分控制
---

# SARSA（同策略時序差分控制）

一種同策略的時序差分方法：每個動作價值都朝「即時獎勵加上智能體實際接下來所採取動作的價值」移動。

## 問題

Q 學習學到的是貪婪策略的價值，即使智能體的實際行為與之不同。若智能體必須持續探索，並在學習過程中為錯誤付出代價，它可能需要反映其實際遵循策略的價值。SARSA 學習的正是這個探索策略的價值。

## 核心想法

在 \(s\) 中採取 \(a\)、得到 \(r\) 並到達 \(s'\) 後，依同一個探索策略在 \(s'\) 中選擇 \(a'\)。接著把 \(Q(s, a)\) 朝 \(r + \gamma Q(s', a')\) 移動。名稱來自每次更新所用的五個量 \((s, a, r, s', a')\)。由於目標使用的是實際將被執行的動作，學到的價值就是行為策略的價值。

## 方程式與演算法

\[
Q(s_t, a_t) \leftarrow Q(s_t, a_t) + \alpha \left[ r_{t+1} + \gamma Q(s_{t+1}, a_{t+1}) - Q(s_t, a_t) \right]
\]

流程如下：

1. 為所有配對初始化 \(Q(s, a)\)。
2. 從狀態 \(s\) 開始一個回合，依 \(Q\) 的 ε-貪婪策略從 \(s\) 選擇 \(a\)。
3. 執行 \(a\)，觀察 \(r\) 與下一狀態 \(s'\)。
4. 依同一策略從 \(s'\) 選擇 \(a'\)。
5. 以上式更新 \(Q(s, a)\)。
6. 令 \(s \leftarrow s'\)、\(a \leftarrow a'\)，然後重複直到回合結束。

與 Q 學習的唯一差別在第 4 步：Q 學習以 \(\max_b Q(s', b)\) 取代 \(Q(s', a')\)。

## 結果

SARSA 沒有單一的代表性基準。Rummery 與 Niranjan（1994）研究了具有線上更新的連接主義 Q 學習變體。他們的報告提出了與 SARSA 密切相關的更新規則 MCQ-L；在一個必須在障礙物間抵達目標的模擬移動機器人上，他們發現線上學習對訓練參數的選擇比倒序回放（backward replay）更不敏感。

## 限制

- **價值取決於探索。** 學到的價值屬於 ε-貪婪策略，因此只有在探索逐漸減少後，才能恢復貪婪策略。
- **排程很重要。** 收斂結果要求仔細選擇探索率與步長，並非對每種排程都成立。
- **表格形式。** 與 Q 學習相同，表格對大型或連續空間並不實際。深度擴充使用相同的同策略目標搭配神經網路。

## 關聯

- 上層主題：[基於價值的方法](../index.zh-TW.md)，以及更廣的[強化學習](../../index.zh-TW.md)概觀。
- 離策略的對應方法：[Q 學習](../q-learning/index.zh-TW.md)。
- 同策略的想法在策略梯度方法中再次出現。[近端策略最佳化](../../proximal-policy-optimisation/index.zh-TW.md)同樣從當前策略收集的資料中學習，而[策略梯度與演員–評論家](../../policy-gradient-and-actor-critic/index.zh-TW.md)概觀則涵蓋使用時序差分目標的評論家。

## 應用

- **線上控制。** 智能體必須在行動的同時學習，且探索有代價。Rummery 與 Niranjan（1994）以一台模擬移動機器人與有限的感測回饋研究此設定。

## 未解問題

- 如何選擇既安全又快速的探索排程。
- 同策略時序差分目標與大規模神經網路結合時的行為。

## 參考文獻

### 開創性論文

- Rummery 與 Niranjan（1994），Technical Report CUED/F-INFENG/TR 166，Cambridge University Engineering Department。https://mi.eng.cam.ac.uk/reports/abstracts/rummery_tr166.html — 早期研究線上連接主義時序差分控制，上文引用的穩健性結果即來自此報告。本次查核未確認報告的完整標題。
- Watkins 與 Dayan（1992），"Q-learning"，*Machine Learning* 8(3–4), 279–292。https://doi.org/10.1007/bf00992698 — 離策略的對應方法，附其收斂定理。
- Mnih 等人（2015），"Human-level control through deep reinforcement learning"，*Nature* 518, 529–533。https://doi.org/10.1038/nature14236 — 深度離策略價值學習器，與 SARSA 的同策略目標形成對照。
- Schulman 等人（2017），"Proximal policy optimization algorithms"，[arXiv:1707.06347](https://arxiv.org/abs/1707.06347) — 同樣從當前策略收集資料學習的深度同策略方法。

### 綜述與教科書

- Sutton, R. S. & Barto, A. G. *Reinforcement Learning: An Introduction*，第 2 版。MIT Press, 2018。http://incompleteideas.net/book/the-book-2nd.html — 在時序差分章節中將 SARSA 介紹為同策略時序差分控制。
