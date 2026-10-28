---
status: complete
last_reviewed: 2026-10-28
related:
  - engineering/evaluation
  - theory/evaluation/protocols/methods/llm-as-judge.md
tags:
  - evaluation
  - protocols
  - llm-as-judge
aliases:
  - Length-controlled AlpacaEval
  - AlpacaEval-LC
  - 長度控制 AlpacaEval
---

# Length-Controlled AlpacaEval

!!! info "Part of LLM as Judge"
    This method page belongs to [LLM as Judge](llm-as-judge.md). It explains the length correction in detail; the parent page compares the judging methods.

AlpacaEval is an automatic benchmark in which a strong model judges whether a model's answer beats a baseline's answer on a set of instructions. Dubois et al. (2024) showed that its raw win rate rewards longer answers, and they proposed a regression that estimates the win rate that would be seen if both answers had the same length.

## Problem

An automatic judge is cheap and agrees fairly well with human preferences, but it prefers longer answers. A model can then raise its score by writing more rather than by answering better, and the leaderboard may rank verbosity. The question was whether an automatic benchmark can be debiased for length without a new human study.

## Core idea

Fit a model of the judge's preference that separates three effects: the difference in quality between the two models, a term for the normalised difference in length, and a term for the instruction. Then predict the preference with the length term set to zero. The average of these predictions over the instructions is the length-controlled win rate.

## Procedure

The authors fit a logistic model to the judge's preferences. The model has three parts: a quality difference between the two models, a length term that scales a tanh of the normalised length difference, and an instruction-specific term. The length-controlled win rate removes the length term:

$$\text{winrate}^{\text{LC}}(m, b) = 100 \cdot \mathbb{E}_x\left[\sigma\left(\theta_m - \theta_b + (\psi_m - \psi_b)\gamma_x\right)\right]$$

Here $m$ is the model being scored, $b$ is the baseline, $\sigma$ is the logistic function, and $\gamma_x$ is an instruction term estimated first in a joint regression. Training uses cross-entropy loss, five-fold cross-validation and L2 regularisation. The length coefficient is lightly regularised so that a model cannot exploit truncation to game the regression.

## Results

- **Agreement with Chatbot Arena.** The Spearman correlation between the leaderboard and Chatbot Arena rose from 0.94 for AlpacaEval to 0.98 for the length-controlled version, on 38 models (Figure 1 and Section 4.2). The authors report a bootstrap p-value of 0.07 against the original, so the improvement is suggestive rather than conclusive.
- **Length gaming.** Varying the verbosity instruction in the prompt moved the raw win rate of gpt4_1106_preview from 22.9% to 64.3%. Its length-controlled rate ranged from 41.9% to 51.6% (Section 4.1). The paper notes qualitatively that weaker models, such as claude-2.1, can gain a lot from being asked to be verbose.
- **Stability across prompts.** The normalised standard deviation of the win rate across prompt variants fell from about 25% to about 10% (Section 4.1). Table 1 lists 26% to 10%.
- **Truncation attack.** The win rate for truncated outputs rose from 3.7 on AlpacaEval 2.0 to 25.9 on AlpacaEval-LC without regularisation, and fell to 12.2 with it (Section 4.3). Table 1 reports the gain with regularisation as 8.5 points.

## Limitations

- The authors test the debiasing method on AlpacaEval. The results here do not show that it transfers to other benchmarks.
- The method answers a counterfactual question, namely how the two models would compare at equal length. Length can be part of a good answer, so this is a modelling choice, not a fact about users.
- The method does not address the other known biases of LLM judges, such as position and self-preference. See [MT-Bench](mt-bench.md) for those.
- The reference model and the auto-annotator are fixed to a GPT-4 Turbo variant, so that judge's own biases carry into the result.

## Connections

- The judge's position and self-preference biases, and the agreement study that documents them, are covered on [MT-Bench](mt-bench.md).
- The arena that the length-controlled score is correlated with, and the ranking methods used to turn votes into scores, are on [Elo Rating and Arenas](elo-rating.md).
- The wider protocol, with its rubric and reporting advice, is on [LLM as Judge](llm-as-judge.md).

## Open questions

- Does length control hold for long-form writing, multi-turn dialogue and non-English answers?
- Should an automatic benchmark also control for formatting, such as lists and headings, which judges may also favour?

## References

### Seminal papers

- Dubois, Y., Galambosi, B., Liang, P. & Hashimoto, T. B. (2024). *Length-Controlled AlpacaEval: A Simple Way to Debias Automatic Evaluators*. arXiv. https://arxiv.org/abs/2404.04475 — Proposes the length-controlled win rate and reports its correlation with Chatbot Arena.
- Zheng, L. et al. (2023). *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena*. NeurIPS Datasets and Benchmarks Track. https://arxiv.org/abs/2306.05685 — Documents verbosity and other biases of LLM judges, and the agreement of GPT-4 with human raters.
- Chiang, W.-L. et al. (2024). *Chatbot Arena: An Open Platform for Evaluating LLMs by Human Preference*. arXiv. https://arxiv.org/abs/2403.04132 — The human-preference arena against which the length-controlled benchmark is correlated.
- Wang, P. et al. (2023). *Large Language Models are not Fair Evaluators*. arXiv. https://arxiv.org/abs/2305.17926 — Shows that candidate order changes an LLM evaluator's verdict, a bias that the length correction does not remove.
- Liu, Y. et al. (2023). *G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment*. arXiv. https://arxiv.org/abs/2303.16634 — Another judging method that uses chain-of-thought and form filling, for comparison with raw automatic scoring.
