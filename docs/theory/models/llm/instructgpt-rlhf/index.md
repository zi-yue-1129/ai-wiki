---
status: draft
last_reviewed: 2026-10-28
aliases:
  - InstructGPT
  - RLHF
  - 人類回饋強化學習
---

# InstructGPT: reinforcement learning from human feedback (Ouyang et al., 2022)

Fine-tunes GPT-3 in three stages (supervised learning on labeller demonstrations, a reward model trained on labeller rankings, and reinforcement learning against that reward model). The result follows user instructions far better than a model over a hundred times larger that was trained on next-token prediction alone.

## Problem

A language model trained only to predict the next token is not trained to do what a user asks. Making the model larger does not by itself make it better at following instructions. Ouyang et al. ask whether human feedback can align GPT-3 with the intent of the users of an API, judged by labellers who compare its outputs.

## Core idea

The pipeline has three steps:

1. **Supervised fine-tuning.** Labellers write demonstrations of the desired behaviour for prompts from the API. GPT-3 is fine-tuned on them.
2. **Reward model.** Labellers rank several outputs (between K = 4 and K = 9) for each prompt. A reward model is trained to score the preferred output above the others.
3. **Policy optimisation.** The supervised model is tuned with PPO against the reward model. A penalty keeps the policy close to the supervised model, so that it does not drift into outputs the reward model has never seen.

The final models, which the paper calls InstructGPT, are trained with PPO plus pretraining gradients (PPO-ptx), to reduce the regressions discussed below.

## Equation or algorithm

The reward model is trained to minimise

\[
\text{loss}(\theta) = -\frac{1}{\binom{K}{2}}\, \mathbb{E}_{(x, y_w, y_l)} \left[\log \sigma\big(r_\theta(x, y_w) - r_\theta(x, y_l)\big)\right]
\]

where \(y_w\) is the preferred output of a pair from the ranking of \(K\) outputs, \(y_l\) the other output, and \(\binom{K}{2}\) the number of comparisons per prompt.

The PPO-ptx objective combines the reward with a KL penalty to the supervised model, and adds a pretraining term:

\[
\mathbb{E}\left[r_\theta(x, y) - \beta \log \frac{\pi^{\text{RL}}_\phi(y \mid x)}{\pi^{\text{SFT}}(y \mid x)}\right] + \gamma\, \mathbb{E}_{x \sim \mathcal{D}_{\text{pretrain}}}\left[\log \pi^{\text{RL}}_\phi(x)\right]
\]

Plain PPO sets \(\gamma = 0\). The data sizes are about 13k prompts for supervised fine-tuning, 33k for the reward model and 31k for PPO, and the labellers were about 40 contractors. The paper evaluates three sizes, 1.3B, 6B and 175B parameters, and the reward models are 6B.

## Results

- **Against GPT-3.** The abstract reports that outputs from the 1.3B InstructGPT model are preferred to outputs from the 175B GPT-3, with 100 times fewer parameters.
- **Preference rates.** The body reports that 175B InstructGPT outputs are preferred to GPT-3 outputs 85 ± 3% of the time, and to few-shot GPT-3 outputs 71 ± 4% of the time.

## Limitations

- **Alignment tax.** The paper says its procedure "comes at the cost of lower performance on certain tasks". Regressions appear on SQuAD, DROP, HellaSwag and the WMT 2015 French–English translation task.
- **Partial fix.** Mixing in pretraining gradients (PPO-ptx) greatly reduces these regressions without hurting labeller preference scores, but PPO-ptx still lags GPT-3 on DROP, SQuADv2 and translation.
- **Narrow preferences.** The reward reflects a small group of about 40 contractors and their judgements of the prompts they saw, not a general standard of helpfulness.
- **Proxy reward.** The policy is optimised against a learned model of preference, so it can exploit that model. This over-optimisation problem is discussed on the [reward modelling](../../../paradigms/reinforcement-learning/learning-from-human-feedback/reward-modelling/index.md) page.

## Connections

- Parent topic: [Large Language Models](../index.md)
- The reward model and its training are covered in [Reward modelling](../../../paradigms/reinforcement-learning/learning-from-human-feedback/reward-modelling/index.md), and the broader field in [Learning from Human Feedback](../../../paradigms/reinforcement-learning/learning-from-human-feedback/index.md).
- The policy update uses [Proximal Policy Optimisation](../../../paradigms/reinforcement-learning/proximal-policy-optimisation/index.md).
- A later method that fits the policy to preference pairs without a reward model is [Direct preference optimisation](../../../paradigms/reinforcement-learning/learning-from-human-feedback/dpo/index.md).
- Other method on this topic: [GPT-3 Few-Shot Learning](../gpt-3-few-shot/index.md), the base model that InstructGPT fine-tunes.
- Other method on this topic: [Compute-Optimal Training](../compute-optimal-training/index.md)

## Applications

- **Instruction following.** The models are evaluated on prompts sent to the OpenAI API, and on public NLP benchmarks to measure regressions.

## Open questions

- Whose preferences should count, and how well a small labeller group represents users.
- How much of the alignment tax can be removed without losing preference gains.
- How reward over-optimisation behaves as the policy becomes stronger than the reward model.

## References

### Seminal papers

- Brown, T. B., et al. (2020), *Language Models are Few-Shot Learners*, [arXiv:2005.14165](https://arxiv.org/abs/2005.14165) — The GPT-3 paper, the base model that InstructGPT fine-tunes.
- Ouyang, L., et al. (2022), *Training language models to follow instructions with human feedback*, [arXiv:2203.02155](https://arxiv.org/abs/2203.02155) — The InstructGPT paper, with the three-stage pipeline and the results above.
- Christiano, P., et al. (2017), "Deep reinforcement learning from human preferences", [arXiv:1706.03741](https://arxiv.org/abs/1706.03741) — The original method for learning a reward function from human comparisons.
- Stiennon, N., et al. (2020), "Learning to summarize from human feedback", NeurIPS 2020, [arXiv:2009.01325](https://arxiv.org/abs/2009.01325) — Applies the same pipeline to summarisation, with a reward model and PPO.
- Schulman, J., et al. (2017), "Proximal policy optimization algorithms", [arXiv:1707.06347](https://arxiv.org/abs/1707.06347) — The PPO algorithm used for the policy step.
- Rafailov, R., et al. (2023), "Direct preference optimization: your language model is secretly a reward model", NeurIPS 2023, [arXiv:2305.18290](https://arxiv.org/abs/2305.18290) — Fits the policy to preference pairs directly, without a separate reward model.
- Bradley, R. A. & Terry, M. E. (1952), "Rank analysis of incomplete block designs: I. The method of paired comparisons", *Biometrika* 39(3/4), 324. https://doi.org/10.2307/2334029 — The paired-comparison model that the reward model follows.

### Further learning

- Hugging Face. *LLM Course*. https://huggingface.co/learn/llm-course — Hands-on course on using, fine-tuning and building LLMs with the Hugging Face libraries.
- Karpathy, A. (2023). *[1hr Talk] Intro to Large Language Models*. YouTube. https://www.youtube.com/watch?v=zjkBMFhNj_g — A one-hour non-technical overview of how LLMs are trained, what they can do and where they fail.
