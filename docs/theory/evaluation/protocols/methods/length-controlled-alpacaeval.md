---
status: draft
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
- **Length gaming.** For the model gpt4_1106_preview, the raw win rate ranged from 22.9% under a concise prompt to 64.3% under a verbose prompt. The length-controlled rate ranged from 41.9% to 51.6% (Figure 3 and Table 1). For claude-2.1, the raw rate ranged from 9.2% to 24.4%, and the length-controlled rate from 18.2% to 30.3%.
- **Stability across prompts.** The normalised standard deviation of the win rate across prompt variants fell from about 25% to about 10% (Section 4.1). Table 1 lists 26% to 10%.
- **Truncation attack.** The win rate for truncated GPT-4 outputs rose from 3.7 to 25.9 without regularisation and to 12.2 with it (Section 4.3). The paper's Table 1 lists a gain of 8.5 for the same attack, so readers should check the table alongside the text.

The paper does not report how much longer the winning answers are, only the average output length of each model.

## Limitations

- The authors tested the debiasing method only on AlpacaEval, which uses relatively simple English instructions and one judge prompt.
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
