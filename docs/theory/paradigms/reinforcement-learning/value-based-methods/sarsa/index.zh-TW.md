---
translation_reviewed: 2026-10-28
---

# SARSA（同策略時序差分控制）

一種同策略的時序差分方法，把每個動作價值朝「獎勵加上智能體實際下一步所選動作的價值」移動。

## 問題

Q 學習學習的是貪婪策略的價值，即使智能體實際的行為與之不同。若智能體必須持續探索，並且在學習過程中為錯誤付出代價，它可能更需要反映自身所遵循之探索策略的價值。SARSA 學習的正是這個探索策略的價值。

## 核心想法

在狀態 \(s\) 執行 \(a\)、得到 \(r\) 並到達 \(s'\) 之後，以同一探索策略在 \(s'\) 選擇 \(a'\)。接著把 \(Q(s, a)\) 朝 \(r + \gamma Q(s', a')\) 移動。名稱來自每次更新使用的五個量 \((s, a, r, s', a')\)。由於目標使用的是實際會執行的動作，學到的價值就是行為策略的價值。

## 方程式或演算法

\[
Q(s_t, a_t) \leftarrow Q(s_t, a_t) + \alpha \left[ r_{t+1} + \gamma Q(s_{t+1}, a_{t+1}) - Q(s_t, a_t) \right]
\]

流程如下：

1. 初始化所有組合的 \(Q(s, a)\)。
2. 從狀態 \(s\) 開始一個回合，並以基於 \(Q\) 的 ε-貪婪從 \(s\) 選擇 \(a\)。
3. 執行 \(a\)，觀察 \(r\) 與下一狀態 \(s'\)。
4. 以 ε-貪婪從 \(s'\) 選擇 \(a'\)。
5. 依上式更新 \(Q(s, a)\)。
6. 令 \(s \leftarrow s'\)、\(a \leftarrow a'\)，重複直到回合結束。

與 Q 學習的唯一差別在第 4 步：Q 學習在目標中使用 \(\max_b Q(s', b)\)，而非 \(Q(s', a')\)。

## 結果

SARSA 沒有單一的代表性基準。Rummery 與 Niranjan（1994）研究了這類更新的線上連接式版本。在模擬的機器人導航任務中，他們報告線上更新比回溯回放更不受訓練參數選擇的影響。

## 限制

- **價值取決於探索。**學到的價值屬於 ε-貪婪策略，因此只有在探索逐漸減少後，才能恢復貪婪策略。
- **排程很重要。**收斂結果要求仔細選擇探索率與步長，並非對每種排程都成立。
- **表格形式。**與 Q 學習相同，大型或連續的空間無法使用表格。深度擴充使用相同的同策略目標搭配神經網路。

## 連結

- 母頁：[值函數方法](../index.md)，以及更大範圍的[強化學習](../../index.md)總覽。
- 離策略的對應方法：[Q 學習](../q-learning/index.md)。
- 同策略的想法也出現在策略梯度方法中。[近端策略最佳化](../../proximal-policy-optimisation/index.md)同樣從目前策略收集的資料中學習，而[策略梯度與演員–評論家](../../policy-gradient-and-actor-critic/index.md)總覽涵蓋使用時序差分目標的評論家。

## 應用

- **代價高的錯誤下的線上控制。**智能體必須邊行動邊學習，其價值包含了自身探索的代價，這正是線上研究所針對的情境（Rummery 與 Niranjan，1994）。

## 未解問題

- 如何選擇探索排程，使學習既安全又快速。
- 同策略時序差分目標在大規模神經網路下的行為。

## 參考文獻

### 開創性論文

- Rummery & Niranjan (1994), "On-line Q-learning using connectionist systems", Technical Report CUED/F-INFENG/TR 166, Cambridge University Engineering Department. https://mi.eng.cam.ac.uk/reports/abstracts/rummery_tr166.html — Early study of on-line connectionist temporal-difference control, with the robustness result cited above.
- Watkins & Dayan (1992), "Q-learning", *Machine Learning* 8(3–4), 279–292. https://doi.org/10.1007/bf00992698 — The off-policy counterpart, with its convergence theorem.
- Mnih et al. (2015), "Human-level control through deep reinforcement learning", *Nature* 518, 529–533. https://doi.org/10.1038/nature14236 — The deep off-policy value learner, a contrast to SARSA's on-policy target.
- Schulman et al. (2017), "Proximal policy optimization algorithms", arXiv:1707.06347 — A deep on-policy method that also learns from data gathered by the current policy.

### 綜述與教科書

- Sutton, R. S. & Barto, A. G. *Reinforcement Learning: An Introduction*, 2nd ed. MIT Press, 2018. http://incompleteideas.net/book/the-book-2nd.html — Presents SARSA as on-policy temporal-difference control in its temporal-difference chapter.
