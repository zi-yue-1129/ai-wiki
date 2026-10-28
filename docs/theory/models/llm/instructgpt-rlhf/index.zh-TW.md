---
translation_reviewed: 2026-10-28
---

# InstructGPT：從人類回饋中進行強化學習（Ouyang 等人，2022）

分三個階段微調 GPT-3：以標註者示範做監督式學習、以標註者排序訓練獎勵模型，再以該獎勵模型進行強化學習。結果是，它遵循使用者指令的能力遠勝於僅以下一詞預測訓練、規模大上百倍的模型。

## 問題

只被訓練去預測下一個詞的語言模型，並不是被訓練去依照使用者的要求做事。單純把模型做大，並不會自動讓它更會遵循指令。Ouyang 等人探討：人類回饋能否使 GPT-3 與 API 使用者的意圖對齊，並以標註者對其輸出的比較來衡量。

## 核心想法

流程分三步：

1. **監督式微調。**標註者為 API 來源的提示撰寫期望行為的示範，GPT-3 以此微調。
2. **獎勵模型。**標註者為每個提示排序數個輸出（K 介於 4 至 9 之間）。獎勵模型被訓練為給偏好的輸出比其他輸出更高的分數。
3. **策略最佳化。**以 PPO 針對獎勵模型調整監督模型。一個懲罰項使策略靠近監督模型，避免漂移到獎勵模型從未見過的輸出。

論文最終的模型稱為 InstructGPT，以 PPO 加上預訓練梯度（PPO-ptx）訓練，以減少下文所述的退步。

## 方程式或演算法

獎勵模型的訓練目標是最小化

\[
\text{loss}(\theta) = -\frac{1}{\binom{K}{2}}\, \mathbb{E}_{(x, y_w, y_l)} \left[\log \sigma\big(r_\theta(x, y_w) - r_\theta(x, y_l)\big)\right]
\]

其中 \(y_w\) 是 \(K\) 個輸出排序中偏好的那個，\(y_l\) 是另一個輸出，\(\binom{K}{2}\) 是每個提示的比較次數。

PPO-ptx 的目標把獎勵與對監督模型的 KL 懲罰結合，並加上預訓練項：

\[
\mathbb{E}\left[r_\theta(x, y) - \beta \log \frac{\pi^{\text{RL}}_\phi(y \mid x)}{\pi^{\text{SFT}}(y \mid x)}\right] + \gamma\, \mathbb{E}_{x \sim \mathcal{D}_{\text{pretrain}}}\left[\log \pi^{\text{RL}}_\phi(x)\right]
\]

單純的 PPO 令 \(\gamma = 0\)。資料規模約為監督式微調 13k 個提示、獎勵模型 33k 個、PPO 31k 個，標註者約 40 位承包商。論文評估 1.3B、6B 與 175B 三種參數規模，獎勵模型為 6B。

## 結果

- **與 GPT-3 比較。**摘要指出，1.3B 參數的 InstructGPT 輸出，勝過 175B 參數的 GPT-3 輸出，而參數量少了 100 倍。
- **偏好比例。**正文報告，175B 的 InstructGPT 輸出在 85 ± 3% 的情況下勝過 GPT-3 輸出，在 71 ± 4% 的情況下勝過少樣本的 GPT-3 輸出。

## 限制

- **對齊稅。**論文表示此程序「在某些任務上的表現較差」。在 SQuAD、DROP、HellaSwag 與 WMT 2015 法英翻譯任務上出現退步。
- **只是部分解決。**混入預訓練梯度（PPO-ptx）能大幅減少這些退步，且不損害標註者的偏好分數；但 PPO-ptx 在 DROP、SQuADv2 與翻譯上仍落後 GPT-3。
- **偏好範圍窄。**獎勵反映的是約 40 位承包商的判斷，以及他們所見提示的判斷，並非一般的有用性標準。
- **代理獎勵。**策略是針對學習得到的偏好模型最佳化，因此可能利用該模型的缺陷。此過度最佳化問題在[獎勵建模](../../../paradigms/reinforcement-learning/learning-from-human-feedback/reward-modelling/index.md)頁面中討論。

## 連結

- 母頁：[大型語言模型](../index.md)
- 獎勵模型及其訓練見[獎勵建模](../../../paradigms/reinforcement-learning/learning-from-human-feedback/reward-modelling/index.md)，更廣的領域見[從人類回饋學習](../../../paradigms/reinforcement-learning/learning-from-human-feedback/index.md)。
- 策略更新使用[近端策略最佳化](../../../paradigms/reinforcement-learning/proximal-policy-optimisation/index.md)。
- 後來一種不需要獎勵模型、直接以偏好對擬合策略的方法是[直接偏好最佳化](../../../paradigms/reinforcement-learning/learning-from-human-feedback/dpo/index.md)。
- 同一主題的另一方法：[GPT-3 少樣本學習](../gpt-3-few-shot/index.md)，即 InstructGPT 所微調的基礎模型。
- 同一主題的另一方法：[運算最佳化訓練](../compute-optimal-training/index.md)

## 應用

- **遵循指令。**模型以送往 OpenAI API 的提示評估，並在公開的 NLP 基準上衡量退步。

## 未解問題

- 哪些人的偏好應該被納入計算，以及小群標註者能多大程度代表使用者。
- 在不損失偏好提升的前提下，能去除多少對齊稅。
- 當策略比獎勵模型更強時，獎勵的過度最佳化會如何發展。

## 參考文獻

### 開創性論文

- Brown, T. B., et al. (2020), *Language Models are Few-Shot Learners*, [arXiv:2005.14165](https://arxiv.org/abs/2005.14165) — The GPT-3 paper, the base model that InstructGPT fine-tunes.
- Ouyang, L., et al. (2022), *Training language models to follow instructions with human feedback*, [arXiv:2203.02155](https://arxiv.org/abs/2203.02155) — The InstructGPT paper, with the three-stage pipeline and the results above.
- Christiano, P., et al. (2017), "Deep reinforcement learning from human preferences", [arXiv:1706.03741](https://arxiv.org/abs/1706.03741) — The original method for learning a reward function from human comparisons.
- Stiennon, N., et al. (2020), "Learning to summarize from human feedback", NeurIPS 2020, [arXiv:2009.01325](https://arxiv.org/abs/2009.01325) — Applies the same pipeline to summarisation, with a reward model and PPO.
- Schulman, J., et al. (2017), "Proximal policy optimization algorithms", [arXiv:1707.06347](https://arxiv.org/abs/1707.06347) — The PPO algorithm used for the policy step.
- Rafailov, R., et al. (2023), "Direct preference optimization: your language model is secretly a reward model", NeurIPS 2023, [arXiv:2305.18290](https://arxiv.org/abs/2305.18290) — Fits the policy to preference pairs directly, without a separate reward model.
- Bradley, R. A. & Terry, M. E. (1952), "Rank analysis of incomplete block designs: I. The method of paired comparisons", *Biometrika* 39(3/4), 324. https://doi.org/10.2307/2334029 — The paired-comparison model that the reward model follows.

### 延伸學習

- Hugging Face. *LLM Course*. https://huggingface.co/learn/llm-course — Hands-on course on using, fine-tuning and building LLMs with the Hugging Face libraries.
- Karpathy, A. (2023). *[1hr Talk] Intro to Large Language Models*. YouTube. https://www.youtube.com/watch?v=zjkBMFhNj_g — A one-hour non-technical overview of how LLMs are trained, what they can do and where they fail.
