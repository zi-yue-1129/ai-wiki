---
translation_reviewed: 2026-10-28
---

# 直接偏好最佳化（Rafailov 等人，2023）

以分類損失把語言模型擬合到偏好對上，因此不需要獨立的獎勵模型，也不需要強化學習迴圈。

## 問題

從人類回饋進行強化學習，首先要以比較資料訓練獎勵模型，然後以策略梯度方法針對它進行最佳化。這比直接把模型擬合到比較資料上更複雜，也更難調整。Rafailov 等人探討：是否能直接在偏好資料上求解具 KL 約束的獎勵最大化目標。

## 核心想法

具 KL 約束的目標有已知的最佳策略。給定參考策略 \(\pi_{\text{ref}}\)、係數 \(\beta\) 與獎勵 \(r\)，最佳解為 \(\pi_r(y \mid x) \propto \pi_{\text{ref}}(y \mid x)\exp(r(x, y)/\beta)\)。移項後，獎勵可以用策略表示：\(r(x, y) = \beta \log(\pi_r(y \mid x)/\pi_{\text{ref}}(y \mid x)) + \beta \log Z(x)\)。把它代入 Bradley–Terry 偏好模型後，配分項會消去，獎勵模型也就不再需要。剩下的只是策略與參考模型的損失。

## 方程式或演算法

對偏好三元組 \((x, y_w, y_l)\) 的 DPO 損失為

\[
\mathcal{L}_{\text{DPO}}(\pi_\theta; \pi_{\text{ref}}) = -\mathbb{E}_{(x, y_w, y_l)} \left[\log \sigma\left(\beta \log \frac{\pi_\theta(y_w \mid x)}{\pi_{\text{ref}}(y_w \mid x)} - \beta \log \frac{\pi_\theta(y_l \mid x)}{\pi_{\text{ref}}(y_l \mid x)}\right)\right]
\]

其中 \(y_w\) 是偏好的完成，\(y_l\) 是不被偏好的完成，\(\beta\) 控制 KL 約束的強度。流程如下：

1. 取一批含有偏好與非偏好完成的提示。
2. 計算每個完成在策略與凍結的參考模型下的對數機率。
3. 對上述損失做一步梯度更新。
4. 重複直到策略收斂。訓練時不需要從策略取樣。

## 結果

論文在數項任務上與基於 PPO 的人類回饋強化學習比較：

- **情感控制。**DPO「產生的效率前緣遠優於其他方法，在保持低 KL 的同時達到最高獎勵」，並在控制生成文字的情感上超越基於 PPO 的人類回饋強化學習。
- **摘要。**在溫度 0.0 時，DPO 對參考摘要的勝率約為 61%；PPO 在其最佳取樣溫度下為 57%。作者指出，他們沒有有意義地調整 \(\beta\)，因此這些結果可能低估了 DPO。
- **人類評估。**溫度 0.25 的 DPO 樣本，有 58% 的情況被偏好於溫度 0 的 PPO 樣本。
- **對話。**論文報告，在 Anthropic HH 資料集上，DPO 是唯一計算效率高、且能改進偏好完成的方法。

## 限制

- **規模。**模型只評估到 6B 參數，論文把將 DPO 擴展到更大模型列為未來工作。
- **泛化。**論文提問：與從明確獎勵函數學習相比，DPO 策略如何在分布之外泛化，這個問題仍未解決。
- **過度最佳化。**論文提問：獎勵過度最佳化在直接偏好最佳化的設定中如何出現，此問題也未解決。
- **自動判斷。**GPT-4 計算的勝率取決於提示，因此評估本身也有疑慮。

## 連結

- 母頁：[從人類回饋學習](../index.md)，以及更大範圍的[強化學習](../../index.md)總覽。
- DPO 去掉了[獎勵建模](../reward-modelling/index.md)中明確的獎勵模型，但使用相同的 Bradley–Terry 比較模型。
- 它取代了 [InstructGPT](../../../../models/llm/instructgpt-rlhf/index.md) 的策略最佳化步驟，後者使用[近端策略最佳化](../../proximal-policy-optimisation/index.md)。

## 應用

- **語言模型的偏好微調。**論文以偏好資料微調摘要與對話模型。
- **可控生成。**將生成文字的情感導向較受偏好的輸出。

## 未解問題

- 不含明確獎勵模型訓練出的策略，其泛化能力是否與含獎勵模型者相當。
- 在更大規模下，如何為最佳效果調整 \(\beta\) 與參考模型。

## 參考文獻

### 開創性論文

- Rafailov et al. (2023), "Direct preference optimization: your language model is secretly a reward model", NeurIPS 2023, [arXiv:2305.18290](https://arxiv.org/abs/2305.18290) — The DPO paper, with the loss, the closed-form derivation and the results above.
- Ouyang et al. (2022), "Training language models to follow instructions with human feedback", [arXiv:2203.02155](https://arxiv.org/abs/2203.02155) — InstructGPT, the RLHF pipeline that DPO simplifies.
- Christiano et al. (2017), "Deep reinforcement learning from human preferences", [arXiv:1706.03741](https://arxiv.org/abs/1706.03741) — Learns reward functions from human comparisons, the basis of the reward model that DPO avoids.
- Stiennon et al. (2020), "Learning to summarize from human feedback", NeurIPS 2020, [arXiv:2009.01325](https://arxiv.org/abs/2009.01325) — Summarisation with a reward model and PPO, one of the baselines DPO is compared against.
- Bradley & Terry (1952), "Rank analysis of incomplete block designs: I. The method of paired comparisons", *Biometrika* 39(3/4), 324. https://doi.org/10.2307/2334029 — The paired-comparison model used to derive the DPO loss.
