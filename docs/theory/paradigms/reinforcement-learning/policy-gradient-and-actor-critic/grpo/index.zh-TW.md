---
translation_reviewed: 2026-10-28
---

# 群組相對策略最佳化（Shao 等人，2024）

一種類 PPO 的語言模型策略梯度方法，不使用學習得到的評論家，而是在同一題目的一組取樣答案內標準化獎勵，以計算優勢。

## 問題

語言模型的 PPO 需要一個獨立的價值模型，這會增加訓練的記憶體與計算成本。Shao 等人在 DeepSeekMath 的研究中提出 GRPO，探討基線能否改由同一提示下多個取樣輸出的獎勵提供，而不需要評論家。

## 核心想法

對每個問題 \(q\)，策略取樣一組 \(G\) 個輸出 \(\{o_i\}\)，每個輸出得到獎勵 \(r_i\)。優勢是組內標準化的獎勵 \(\hat{A}_i = (r_i - \text{mean}(\mathbf{r})) / \text{std}(\mathbf{r})\)，同一個值套用於該輸出的每個 token。組內平均扮演評論家原本會學習的基線角色。更新保留 PPO 的截斷機率比，並加上一個與參考策略之間的 KL 懲罰，使策略不會偏離太遠。

## 方程式或演算法

GRPO 目標在組內各輸出的各 token 上取平均，對每一項取截斷比率與未截斷比率的較小者，以標準化優勢加權，再減去 \(\beta\) 乘以與參考策略的 KL 散度。KL 項直接加在損失上，而非加在獎勵上。論文在 DeepSeekMath-RL 的設定中使用無偏的 KL 估計器，係數 \(\beta = 0.04\)，每個問題取樣 64 個輸出。流程如下：

1. 對批次中的每個問題，從舊策略取樣 \(G\) 個輸出。
2. 以獎勵為每個輸出評分，例如最終答案是否正確。
3. 在組內標準化獎勵，得到優勢 \(\hat{A}_i\)。
4. 以截斷目標與 KL 懲罰更新策略，進行一或多次梯度步。
5. 將舊策略設為更新後的策略，然後重複。

論文也描述了結果監督與過程監督兩種版本。結果監督版本如上，每個輸出只得到一個獎勵。

## 結果

論文報告一個以 GRPO 訓練的 7B 模型 DeepSeekMath-RL，與其指令微調的起點 DeepSeekMath-Instruct 7B 相比，使用思維鏈提示：

- **GSM8K：**指令模型為 82.9%，GRPO 之後為 88.2%。
- **MATH：**指令模型為 46.8%，GRPO 之後為 51.7%。

這些是一次數學推理訓練的提升，並不是跨任務的通用比較。

## 限制

- **依賴獎勵。**優勢的品質取決於獎勵訊號；在語言任務中，獎勵常是可驗證的答案或學習得到的模型。
- **組取樣成本。**每個問題取樣 64 個輸出，即使去掉了評論家，生成時間仍然可觀。
- **證據範圍窄。**報告的提升來自單一模型系列的數學推理基準，論文並未證明此方法適用於開放式任務。

## 連結

- 母頁：[策略梯度與演員–評論家](../index.md)，以及更大範圍的[強化學習](../../index.md)總覽。
- GRPO 是 [PPO](../../proximal-policy-optimisation/index.md) 去掉評論家的變體，保留其截斷目標。
- 它繼承了 [REINFORCE](../reinforce/index.md) 以回報加權對數機率的想法。
- 其訓練訊號與[從人類回饋學習](../../learning-from-human-feedback/index.md)頁面中的人類回饋獎勵模型相關。

## 應用

- **數學推理。**以 GRPO 訓練的 DeepSeekMath-RL 模型在 GSM8K 與 MATH 上有所提升（Shao 等人，2024）。
- **語言模型對齊。**同一類策略梯度方法用於偏好式微調，如 InstructGPT（Ouyang 等人，2022）。

## 未解問題

- 當組內獎勵有雜訊或答案為開放式時，組標準化的優勢是否仍然成立。
- 如何選擇組大小，它在計算成本與變異數降低之間取捨。

## 參考文獻

### 開創性論文

- Shao et al. (2024), "DeepSeekMath: Pushing the limits of mathematical reasoning in open language models", [arXiv:2402.03300](https://arxiv.org/abs/2402.03300) — Introduces GRPO, the group-relative baseline, and the GSM8K and MATH results above.
- Schulman et al. (2017), "Proximal policy optimization algorithms", [arXiv:1707.06347](https://arxiv.org/abs/1707.06347) — The clipped objective that GRPO keeps.
- Schulman et al. (2015), "Trust region policy optimization", *Proceedings of ICML 2015*, [arXiv:1502.05477](https://arxiv.org/abs/1502.05477) — The trust-region idea behind the constraint on policy change.
- Ouyang et al. (2022), "Training language models to follow instructions with human feedback", [arXiv:2203.02155](https://arxiv.org/abs/2203.02155) — Policy-gradient fine-tuning of language models with a learned reward model.
- Mnih et al. (2016), "Asynchronous methods for deep reinforcement learning", [arXiv:1602.01783](https://arxiv.org/abs/1602.01783) — Advantage-based actor-critic updates, the family GRPO modifies.

### 綜述與教科書

- Sutton, R. S. & Barto, A. G. *Reinforcement Learning: An Introduction*, 2nd ed. MIT Press, 2018. http://incompleteideas.net/book/the-book-2nd.html — Background on policy gradients and baselines.
