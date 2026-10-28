---
status: complete
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
---

# 群組相對策略最佳化（Shao 等人，2024）

一種類 PPO 的語言模型策略梯度方法。它不使用學習得到的評論家，而是在同一題目的一組取樣答案內標準化獎勵，以計算優勢。

## 問題

語言模型的 PPO 需要一個獨立的價值模型，增加訓練時的記憶體與計算成本。Shao 等人在 DeepSeekMath 的工作中提出 GRPO，探討基線能否直接來自同一提示下多個取樣輸出的獎勵，而不需要評論家。

## 核心想法

對每個問題 \(q\)，策略取樣一組 \(G\) 個輸出 \(\{o_i\}\)，每個輸出獲得一個獎勵 \(r_i\)。優勢是組內標準化後的獎勵 \(\hat{A}_i = (r_i - \text{mean}(\mathbf{r})) / \text{std}(\mathbf{r})\)，同一輸出的每個詞元都套用相同的值。組內平均扮演的是評論家原本需要學習的基線角色。更新保留 PPO 的截斷機率比，並加上一項對參考策略的 KL 懲罰，使策略不會偏離太遠。

## 方程式與演算法

GRPO 的目標是：在組內與每個輸出的詞元上取平均，對加權後的截斷與未截斷比率項取較小者（權重為標準化優勢），再減去 \(\beta\) 乘以對參考策略的 KL 散度。KL 項直接加入損失，而不是加入獎勵。論文在 DeepSeekMath-RL 的設定中，使用不偏的 KL 估計器，係數 \(\beta = 0.04\)，並且每個問題取樣 64 個輸出。流程如下：

1. 對批次中的每個問題，從舊策略取樣 \(G\) 個輸出。
2. 以獎勵為每個輸出打分，例如最終答案是否正確。
3. 在組內標準化獎勵，得到優勢 \(\hat{A}_i\)。
4. 以截斷目標與 KL 懲罰更新策略，進行一或多步梯度更新。
5. 將舊策略設為更新後的策略，然後重複。

論文也描述了結果監督（outcome supervision）與過程監督（process supervision）兩種版本。結果版本如上，每個輸出只得到一個獎勵。

## 結果

論文報告一個 7B 模型經 GRPO 訓練後的結果，即 DeepSeekMath-RL，並與其起點 DeepSeekMath-Instruct 7B 比較，兩者都使用思維鏈提示：

- **GSM8K：** 指令微調模型為 82.9%，GRPO 之後為 88.2%。
- **MATH：** 指令微調模型為 46.8%，GRPO 之後為 51.7%。

這些是一次數學推理訓練的提升，並非跨任務的通用比較。

## 限制

- **依賴獎勵。** 優勢的品質受限於獎勵訊號。在語言任務中，獎勵通常是可驗證的答案，或是學習得到的模型。
- **組內取樣的成本。** 即使去除了評論家，每個問題取樣 64 個輸出仍需要生成時間。
- **證據範圍窄。** 報告的提升來自單一模型家族上的數學推理基準，論文並未證明此方法適用於開放式任務。

## 關聯

- 上層主題：[策略梯度與演員–評論家](../index.md)，以及更廣的[強化學習](../../index.zh-TW.md)概觀。
- GRPO 是 [PPO](../../proximal-policy-optimisation/index.zh-TW.md) 去除評論家的變體，保留了其截斷目標。
- 它繼承了 REINFORCE 以回報為權重的 log 機率的想法，見 [REINFORCE](../reinforce/index.zh-TW.md) 頁面。
- 其訓練訊號與[從人類回饋學習](../../learning-from-human-feedback/index.md)頁面中的人類回饋獎勵模型相關。

## 應用

- **數學推理。** 以 GRPO 訓練的 DeepSeekMath-RL 模型在 GSM8K 與 MATH 上有所提升（Shao 等人，2024）。
- **語言模型對齊。** 同一策略梯度家族也用於以偏好為基礎的微調，如 InstructGPT（Ouyang 等人，2022）。

## 未解問題

- 當組內獎勵有雜訊或答案為開放式時，組內標準化的優勢是否仍然可靠。
- 如何選擇組的大小，它是在計算成本與變異降低之間的取捨。

## 參考文獻

### 開創性論文

- Shao 等人（2024），"DeepSeekMath: Pushing the limits of mathematical reasoning in open language models"，[arXiv:2402.03300](https://arxiv.org/abs/2402.03300) — 提出 GRPO、組相對基線，以及上述 GSM8K 與 MATH 結果。
- Schulman 等人（2017），"Proximal policy optimization algorithms"，[arXiv:1707.06347](https://arxiv.org/abs/1707.06347) — GRPO 保留的截斷目標。
- Schulman 等人（2015），"Trust region policy optimization"，*Proceedings of ICML 2015*，[arXiv:1502.05477](https://arxiv.org/abs/1502.05477) — 限制策略變動的信賴域概念。
- Ouyang 等人（2022），"Training language models to follow instructions with human feedback"，[arXiv:2203.02155](https://arxiv.org/abs/2203.02155) — 以學習得到的獎勵模型對語言模型進行策略梯度微調。
- Mnih 等人（2016），"Asynchronous methods for deep reinforcement learning"，[arXiv:1602.01783](https://arxiv.org/abs/1602.01783) — 以優勢為基礎的演員–評論家更新，即 GRPO 所修改的方法家族。

### 綜述與教科書

- Sutton, R. S. & Barto, A. G. *Reinforcement Learning: An Introduction*，第 2 版。MIT Press, 2018。http://incompleteideas.net/book/the-book-2nd.html — 策略梯度與基線的背景知識。
