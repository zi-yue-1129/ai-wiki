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
  - MT-Bench
  - 多輪對話評估基準
---

# MT-Bench

!!! info "Part of LLM as Judge"
    This method page belongs to [LLM as Judge](llm-as-judge.md). It explains the MT-Bench judging study in detail; the parent page compares the judging methods.

MT-Bench is a set of 80 multi-turn questions, and the study that introduced it showed that a strong language model can judge answers to those questions about as consistently as human experts do. The same study documented the biases that such judges show, and it used pairwise comparison with swapped answer order.

## Problem

Open-ended answers, such as a reply in a conversation, have no single correct string to match. Human grading is accurate but slow and expensive, and automatic overlap metrics do not track whether an answer is helpful. The question was whether a language model could act as a cheap and consistent grader of such answers, and what kinds of error it would make.

## Core idea

Use a strong model as the judge, with a fixed prompt and a fixed set of questions. The questions fall into eight categories of ten each: writing, roleplay, extraction, reasoning, math, coding, STEM knowledge and humanities and social-science knowledge. Each question has a second turn that tests follow-up behaviour. Answers are compared in pairs with the order swapped, and a verdict counts only when it holds in both orders. Otherwise the comparison is recorded as a tie.

## Procedure

1. For each question, generate an answer from each model under comparison.
2. Show the judge the question and two answers, labelled A and B, and ask for a verdict.
3. Repeat the comparison with the two answers in the reverse order.
4. Count a win only when both orders favour the same answer. Otherwise count a tie.
5. Aggregate the verdicts across questions into a ranking, for example with the methods in [Elo rating and arenas](elo-rating.md).

## Results

Agreement is reported against expert human raters (Zheng et al., 2023, Table 5(a), first turn):

| Comparison | Including ties | Excluding ties |
|---|---|---|
| GPT-4 against human experts | 66% | 85% |
| Human experts against one another | 63% | 81% |

The second-turn comparison (Table 5(b)) gives the same 66% and 85% for GPT-4 against humans. On Chatbot Arena votes, GPT-4 agreed with human voters 64% of the time including ties and 87% excluding ties (Table 6).

Position consistency is the rate at which a judge gives the same verdict in both orders. With the default prompt it was 65.0% for GPT-4 and 46.2% for GPT-3.5 (Table 2). The authors report these mitigations, each tested on small sets, so the figures are indicative only:

- A few-shot judge raised GPT-4's consistency from 65.0% to 77.5%, at about four times the API cost.
- Chain-of-thought prompting and reference-guided grading reduced the failure rate on a math test of 20 comparisons (Table 4) from 14 of 20 to 6 of 20 and 3 of 20.
- A fine-tuned Vicuna-13B judge reached 65.0% consistency, against a zero-shot baseline of 15.0% in Table 15 (the appendix text gives 16.2%), and 56.8% agreement with humans including ties.

## Known biases

- **Position.** A judge's verdict can change when the order of the two answers changes, as the consistency figures above show. Swapping the order and counting only consistent verdicts is the protocol the paper adopts.
- **Verbosity.** In a "repetitive list" test on 23 answers, the judge failed 91.3% of the time for Claude-v1, 91.3% for GPT-3.5 and 8.7% for GPT-4.
- **Self-enhancement.** GPT-4 favoured its own answers with a 10% higher win rate, and Claude-v1 with a 25% higher win rate. The authors say the data cannot establish this bias conclusively.
- **Reference answers.** On the math test in Table 4, the default prompt failed 14 of 20 times, against 3 of 20 with a reference answer.

## Limitations

- The question set has 80 questions, so the agreement figures carry sampling uncertainty.
- The results describe the judges tested in 2023. Hosted judge models change over time, so any new result needs its own agreement check.

## Connections

- The general protocol, and the other judging methods, are on the [LLM as Judge](llm-as-judge.md) page.
- Length bias in an automatic judge, and the correction used by AlpacaEval, is on [Length-Controlled AlpacaEval](length-controlled-alpacaeval.md).
- Ranking many models from pairwise verdicts is covered in [Elo Rating and Arenas](elo-rating.md).
- Judges are a form of model-based evaluation that also appears in the application-level guidance in [Evaluation & Benchmarks](../../../../engineering/evaluation/index.md).

## Open questions

- How much agreement with human raters carries over to other languages, domains and task types?
- Can judges be trained to reduce position and verbosity bias without a large increase in cost?
- How should a judge be scored when a human panel itself disagrees about which answer is better?

## References

### Seminal papers

- Zheng, L. et al. (2023). *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena*. NeurIPS Datasets and Benchmarks Track. https://arxiv.org/abs/2306.05685 — Introduces MT-Bench and the pairwise judging protocol, and reports agreement with humans and the main judge biases.
- Chiang, W.-L. et al. (2024). *Chatbot Arena: An Open Platform for Evaluating LLMs by Human Preference*. arXiv. https://arxiv.org/abs/2403.04132 — Describes the crowdsourced pairwise arena whose votes the MT-Bench judge is compared against.
- Wang, P. et al. (2023). *Large Language Models are not Fair Evaluators*. arXiv. https://arxiv.org/abs/2305.17926 — Shows that the order of candidate answers can change which answer an LLM evaluator prefers.
- Liu, Y. et al. (2023). *G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment*. arXiv. https://arxiv.org/abs/2303.16634 — Uses chain-of-thought steps and form filling for LLM scoring; reports a Spearman correlation of 0.514 with humans on summarisation.
- Dubois, Y. et al. (2024). *Length-Controlled AlpacaEval: A Simple Way to Debias Automatic Evaluators*. arXiv. https://arxiv.org/abs/2404.04475 — Shows that an automatic judge rewards longer answers and proposes a length-controlled win rate.
