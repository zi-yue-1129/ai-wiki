---
status: draft
last_reviewed: 2026-10-28
---

# InstructGPT: reinforcement learning from human feedback (Ouyang et al., 2022)

Fine-tunes GPT-3 in three stages: supervised learning on demonstrations, a reward model, and reinforcement learning against that reward model.

## Problem

A larger model is not automatically better at following user intent. It can still be untruthful, toxic or unhelpful.

## Core idea

Fine-tune GPT-3 in three stages: supervised learning on human demonstrations, a reward model trained on rankings of model outputs, and reinforcement learning against that reward.

## Equation or algorithm


  1. Collect labeller demonstrations and fine-tune with supervised learning.
  2. Collect rankings of model outputs and train a reward model on them.
  3. Optimise the policy with reinforcement learning (PPO) against the reward model.

## Results

Human raters preferred outputs from the 1.3-billion-parameter InstructGPT over those from the 175-billion-parameter GPT-3. The models were more truthful and produced less toxic output, with minimal regressions on public NLP datasets.

## Limitations

The authors note that InstructGPT still makes simple mistakes. The reward reflects the preferences of a small group of labellers, not a universal standard.

## Connections

- Parent topic: [Large Language Models](../index.md)
- Other method on this topic: [GPT-3 Few-Shot Learning](../gpt-3-few-shot/index.md)
- Other method on this topic: [Compute-Optimal Training](../compute-optimal-training/index.md)

## References

### Seminal papers

- Brown, T. B., et al. (2020). *Language Models are Few-Shot Learners*. arXiv. https://arxiv.org/abs/2005.14165 — The GPT-3 paper, showing that very large models can learn new tasks from a few examples given in the prompt.
- Kaplan, J., et al. (2020). *Scaling Laws for Neural Language Models*. arXiv. https://arxiv.org/abs/2001.08361 — Shows how loss falls predictably as model size, data and compute increase.
- Hoffmann, J., et al. (2022). *Training Compute-Optimal Large Language Models*. arXiv. https://arxiv.org/abs/2203.15556 — The Chinchilla study, arguing that model size and training tokens should grow together for a fixed compute budget.
- Ouyang, L., et al. (2022). *Training language models to follow instructions with human feedback*. arXiv. https://arxiv.org/abs/2203.02155 — InstructGPT, which combines supervised fine-tuning with reinforcement learning from human preferences.
- Wei, J., et al. (2022). *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models*. arXiv. https://arxiv.org/abs/2201.11903 — Shows that prompting models to write intermediate reasoning steps improves multi-step problem solving.

### Surveys and textbooks

- Zhao, W. X., et al. (2023). *A Survey of Large Language Models*. arXiv. https://arxiv.org/abs/2303.18223 — A broad survey of pre-training, adaptation and evaluation of LLMs, with a timeline of models.

### Lectures and videos


### Articles and documentation


## Further learning

- Hugging Face. *LLM Course*. https://huggingface.co/learn/llm-course — Hands-on course on using, fine-tuning and building LLMs with the Hugging Face libraries.
- Karpathy, A. (2023). *[1hr Talk] Intro to Large Language Models*. YouTube. https://www.youtube.com/watch?v=zjkBMFhNj_g — A one-hour non-technical overview of how LLMs are trained, what they can do and where they fail.
