---
translation_reviewed: 2026-10-28
---

# 由人類比較建立獎勵模型（Christiano 等人，2017）

從人類對輸出的成對比較中學習獎勵函數，使強化學習策略能針對人類偏好最佳化，而不必依賴人工撰寫的獎勵。

## 問題

對許多任務而言，獎勵函數很難寫出來，例如讓模擬機器人做出後空翻。人們比較容易判斷兩種行為哪一種較好，而不是給它打一個數字。Christiano 等人探討：由這類比較擬合出的獎勵預測器，能否像真正的獎勵一樣有效地驅動強化學習。

## 核心想法

獎勵模型 \(r_\theta\) 為每個觀測與動作打分。人類偏好某一片段 \(\sigma_1\) 勝過另一片段 \(\sigma_2\) 的機率，以兩者預測獎勵總和之差的邏輯函數建模，即 Bradley–Terry 模型。獎勵網路透過最大化人類標籤的似然來擬合，因此學到的分數會讓偏好的片段排名較高。Stiennon 等人（2020）把同一想法應用到文字上：獎勵模型為摘要打分，策略以 PPO 針對它調整，並對偏離監督模型的程度加以懲罰。

## 方程式或演算法

對兩個片段，偏好機率是其預測獎勵總和的 softmax（Christiano 等人，式 1）。獎勵模型以交叉熵對照人類標籤進行訓練。流程如下：

1. 從目前策略取樣成對的行為。
2. 請人判斷每一對中哪一個較好。
3. 以交叉熵損失擬合獎勵模型。
4. 以強化學習針對學到的獎勵最佳化策略。
5. 持續從改進後的策略取樣新的成對行為並重複，使人類標籤涵蓋策略現在產生的行為。

在文字設定中，策略還會因偏離監督模型的 KL 散度而受到懲罰，使其保持在獎勵模型見過的輸出附近（Stiennon 等人，2020）。

## 結果

- **Atari。**Christiano 等人在七款遊戲上使用 5,500 次比較。他們報告，在這些環境中，此方法比使用真正獎勵的強化學習表現更吃力，不過在部分遊戲上可以相當或超越。
- **MuJoCo。**使用 700 筆標籤，此方法在全部八個任務上幾乎與使用真正獎勵的強化學習相當。使用 1,400 筆標籤時，表現略優於給予真正獎勵的情況。
- **新行為。**模擬的 Hopper 在 900 次查詢、不到一小時內學會後空翻。
- **摘要。**Stiennon 等人在 TL;DR 資料集上收集了 64,832 組摘要比較。其 1.3B 人類回饋模型對參考摘要的原始偏好為 61%，而規模大十倍的監督模型為 43%。

## 限制

- **過度最佳化。**策略針對獎勵模型最佳化得越多，人類真正的偏好相對於預測就越低；論文報告，獎勵模型最終會與人類偏好呈負相關。
- **標註成本。**每一筆比較都需要一個人，因此標籤數量限制了能學到的內容。
- **覆蓋範圍。**獎勵模型只在被比較過的行為上較準確，這也是為何要從改進後的策略收集新比較。

## 連結

- 母頁：[從人類回饋學習](../index.md)，以及更大範圍的[強化學習](../../index.md)總覽。
- 策略步驟通常使用[近端策略最佳化](../../proximal-policy-optimisation/index.md)。
- 語言模型版本是 [InstructGPT](../../../../models/llm/instructgpt-rlhf/index.md) 的第二步。
- [直接偏好最佳化](../dpo/index.md)略去明確的獎勵模型，直接以相同的比較擬合策略。

## 應用

- **機器人與模擬控制。**如 MuJoCo 實驗所示，從比較中學習後空翻與行走等行為。
- **語言模型對齊。**以人類偏好標籤訓練摘要與指令遵循模型（Stiennon 等人，2020；Ouyang 等人，2022）。

## 未解問題

- 如何偵測並防止學到的獎勵被過度最佳化。
- 如何減少所需的人類比較數量。
- 獎勵模型在其訓練行為之外的泛化程度如何。

## 參考文獻

### 開創性論文

- Christiano et al. (2017), "Deep reinforcement learning from human preferences", arXiv:1706.03741 — Learns a reward predictor from human comparisons and trains reinforcement learning on it, with the Atari and MuJoCo results above.
- Stiennon et al. (2020), "Learning to summarize from human feedback", NeurIPS 2020, arXiv:2009.01325 — Applies reward modelling and PPO to summarisation, and reports the over-optimisation result.
- Ouyang et al. (2022), "Training language models to follow instructions with human feedback", arXiv:2203.02155 — InstructGPT, which uses a reward model trained on labeller rankings.
- Bradley & Terry (1952), "Rank analysis of incomplete block designs: I. The method of paired comparisons", *Biometrika* 39(3/4), 324. https://doi.org/10.2307/2334029 — The paired-comparison model behind the preference probability.
- Schulman et al. (2017), "Proximal policy optimization algorithms", arXiv:1707.06347 — The policy-optimisation step used against the learned reward.
