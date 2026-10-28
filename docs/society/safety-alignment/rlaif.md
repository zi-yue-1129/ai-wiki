---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/reinforcement-learning/learning-from-human-feedback
tags:
  - alignment
  - AI feedback
aliases:
  - RLAIF
  - Reinforcement learning from AI feedback
  - 基於 AI 回饋的強化學習
---

# Reinforcement learning from AI feedback (RLAIF)

Reinforcement learning from AI feedback (RLAIF) replaces the human preference labels used in RLHF with labels produced by a language model. The learning procedure stays the same: a reward model is trained on preference pairs, and a policy is optimised against it with reinforcement learning. Lee et al. (2024) study this substitution directly and report that AI labels can train a policy about as well as human labels on the tasks they test.

## Problem

RLHF needs many human comparisons of model responses. Each comparison takes time and money, and raters disagree with one another. The question is whether a capable language model can give preference labels that are good enough to train a reward model, so that the human effort can be reduced or moved to a smaller set of checks.

## Core idea

Use an off-the-shelf language model as the labeller. For each prompt and pair of responses, ask the labeller which response is better, and use its probability for each answer as a soft label. Train the reward model on these labels, then run reinforcement learning as in RLHF. The method is a change in the source of labels, not in the reinforcement learning step, which is why it can be compared directly with RLHF.

## Equation or algorithm

1. Sample a prompt $x$ and two responses $y_1, y_2$ from the current policy.
2. Ask the labeller model which response is better, and read off the probability $p$ that it prefers $y_1$.
3. Train a reward model $r_\phi$ on the soft labels with the standard Bradley–Terry loss,

$$
\mathcal{L}(\phi) = -\mathbb{E}\left[p \log \sigma\big(r_\phi(x, y_1) - r_\phi(x, y_2)\big) + (1 - p)\log \sigma\big(r_\phi(x, y_2) - r_\phi(x, y_1)\big)\right]
$$

4. Optimise the policy against $r_\phi$ with reinforcement learning, usually with a penalty that keeps the policy close to the starting model.

Lee et al. (2024) also describe a direct variant, d-RLAIF, which skips step 3. The labeller scores responses during reinforcement learning, so no separate reward model is trained.

## Results

Lee et al. (2024) compare RLAIF and RLHF on summarisation and on helpful and harmless dialogue. The abstract reports that RLAIF performs about as well as RLHF on these tasks. It also reports that RLAIF can beat a supervised fine-tuned baseline even when the labeller is the same size as the policy, or is the policy's own starting checkpoint. The abstract states that d-RLAIF outperforms standard RLAIF. These are results from the authors' own evaluation protocols, and the numbers are in the paper, not repeated here.

## Limitations

- **Labeller bias.** The labeller's preferences become the training target. If it favours particular styles or positions, the reward model learns those preferences too.
- **Self-preference.** A model that labels its own outputs, or outputs close to its own, may prefer them for reasons unrelated to quality.
- **Labeller ceiling.** The policy is trained toward what the labeller can judge. On tasks the labeller cannot evaluate well, the signal is weak, which is the central difficulty of [scalable oversight](scalable-oversight.md).
- **Narrow evidence.** The reported comparisons cover a few tasks. Results on coding, long-horizon agents or open-ended research are not established by these experiments.
- **Reward hacking.** The reward model is still a proxy, and over-optimising it can reduce true quality, as described in [reward hacking](reward-hacking.md).

## Connections

RLAIF is the label-source part of [Constitutional AI](constitutional-ai.md), which adds written principles and critique-and-revision. Compared with the human-feedback framework in [learning from human feedback](../../theory/paradigms/reinforcement-learning/learning-from-human-feedback/index.md), RLAIF keeps the same objective and changes only who gives the comparison. The idea of judging by a rule instead of by direct experience has a human analogue in how people apply written standards, but the analogy is loose.

## Applications

- Reducing the cost of preference data when building chat and summarisation models.
- Generating preference data for tasks where human experts are scarce, with spot-checks by humans.
- Comparing labeller models to choose one whose judgements agree with human raters on a held-out set.

## Open questions

- How well do AI labels track human preferences when the task requires expert knowledge?
- Does d-RLAIF's gain over standard RLAIF persist with stronger labellers and longer training?
- What checks are enough to detect systematic labeller bias before it is baked into a policy?

## References

### Seminal papers

- Lee, H. et al. (2024). *RLAIF vs. RLHF: Scaling Reinforcement Learning from Human Feedback with AI Feedback*. Proceedings of ICML 2024 (PMLR 235). https://arxiv.org/abs/2309.00267 — Compares AI-labelled and human-labelled preferences for training policies on summarisation and dialogue.
- Bai, Y. et al. (2022). *Constitutional AI: Harmlessness from AI Feedback*. arXiv:2212.08073. https://arxiv.org/abs/2212.08073 — Introduces training from AI preference labels guided by written principles.
- Christiano, P. et al. (2017). *Deep Reinforcement Learning from Human Preferences*. arXiv:1706.03741. https://arxiv.org/abs/1706.03741 — Learns a reward model from human comparisons, the human-label baseline that RLAIF replaces.

### Surveys and textbooks

- Casper, S., Davies, X. & Shi, C. (2023). *Open Problems and Fundamental Limitations of Reinforcement Learning from Human Feedback*. arXiv:2307.15217. https://arxiv.org/abs/2307.15217 — Surveys open problems in preference-based training, many of which apply to AI-generated labels.
- Ouyang, L. et al. (2022). *Training language models to follow instructions with human feedback*. arXiv:2203.02155. https://arxiv.org/abs/2203.02155 — Applies reward-model RLHF to make a language model follow user instructions.
- Rafailov, R. et al. (2023). *Direct Preference Optimization: Your Language Model is Secretly a Reward Model*. arXiv:2305.18290. https://arxiv.org/abs/2305.18290 — Fits a policy directly to preference pairs, with no explicit reward model.
