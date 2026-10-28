---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/reinforcement-learning/learning-from-human-feedback
tags:
  - alignment
  - oversight
aliases:
  - AI debate
  - Debate
  - 辯論
---

# AI debate

AI debate is a protocol for supervising a system on questions that a human judge cannot check directly. Two copies of a model argue for opposing answers, and a judge decides which argument is more convincing. The idea is that the judge needs only to evaluate short, checkable claims, because the opposing debater will point out errors. Irving, Christiano and Amodei (2018) proposed the method, and later experiments test whether it helps non-expert judges.

## Problem

Supervising a model with human judgements works when the judge can tell a correct answer from an incorrect one. For questions that need expert knowledge, or for outputs too long to check, the judge cannot do this alone. Oversight then depends on finding a procedure that lets a weaker judge reach correct answers, which is the problem treated in [scalable oversight](scalable-oversight.md).

## Core idea

Treat the question as a zero-sum game. Each debater is rewarded only if the judge accepts its answer. If one debater makes a false claim, the other can challenge it, and a false claim that is hard to defend should lose. Irving et al. argue that, in this setting, the debate can reveal the truth to a judge who could not check the original question directly.

## Protocol

1. A question $q$ is posed. Debater A argues for answer $a$, and debater B argues for an opposing answer.
2. The debaters take turns making statements, and may quote evidence. The number of rounds is fixed.
3. A judge, human or model with limited capability, reads the transcript and picks the debater whose answer it accepts.
4. Both debaters are trained by self-play, so each learns to win against the other, and the winner's statements are reinforced.

The proposal assumes that the honest debater can always expose a lie in a way the judge can follow. The paper gives a theoretical argument under this assumption, and it demonstrates the setup on small tasks.

## Results

Irving et al. (2018) include small experiments on image classification. The paper is a proposal with theory and early demonstrations, not a large empirical study.

Two later studies test the idea with language models and human judges:

- Khan et al. (2024) test debate with non-expert human judges. The abstract reports that when expert debaters were optimised to be more persuasive, without ground-truth labels, non-expert judges identified the correct answer more often. In other words, the persuasiveness of the debaters helped the judge reach truth.
- Michael et al. (2023) test debate between two unreliable expert debaters, against a consultancy baseline with a single expert. The abstract reports that debate helped non-expert human judges answer hard reading-comprehension questions more accurately, at 84% judge accuracy against 74% for the consultancy baseline.

These are results from particular tasks and judge pools, and they should not be read as evidence for debate on every kind of question.

## Limitations

- **Persuasion versus truth.** A debater that is more persuasive can win without being right. The Khan et al. result suggests this can be turned to advantage in some settings, but it is also the central risk.
- **Hidden flaws.** A claim that is too long or too technical to check may survive the debate even if it is false.
- **Collusion.** Debaters trained together could agree on a misleading answer and split the reward.
- **Judge limits.** Judges can be fooled by rhetoric, and their errors may be systematic.
- **Assumed structure.** The theory depends on the honest side being able to win, which may not hold for every question type.

## Connections

Debate borrows from adversarial legal and scientific practice, where opposing advocates and cross-examination are used to test claims. The analogy is useful for the structure of the protocol, though human debates are not zero-sum games with a learned strategy. The method is one of the decomposition-based approaches in [scalable oversight](scalable-oversight.md), and it is related to the amplification approach of Christiano, Shlegeris and Amodei (2018). Judges in debate experiments face the same evaluation problems discussed in [reward hacking](reward-hacking.md), since a debater can learn to exploit the judge rather than find the truth.

## Applications

- Experimental supervision of models on question-answering tasks where experts are scarce.
- Human-subject studies of whether assistance from models improves non-expert judgements.
- Designing judges and evaluation protocols that resist persuasion by a model.

## Open questions

- Does debate reach the truth when the judge is much weaker than the debaters, and under what conditions does it fail?
- How should judges be trained to resist persuasive but wrong arguments?
- Can debate be extended to tasks where no single claim can be checked in isolation?

## References

### Seminal papers

- Irving, G., Christiano, P. & Amodei, D. (2018). *AI safety via debate*. arXiv:1805.00899. https://arxiv.org/abs/1805.00899 — Proposes two-agent debate judged by a human as a way to supervise systems on questions beyond direct human judgement.
- Khan, A. et al. (2024). *Debating with More Persuasive LLMs Leads to More Truthful Answers*. Proceedings of ICML 2024 (PMLR 235). https://arxiv.org/abs/2402.06782 — Shows that optimising debaters for persuasiveness, without ground truth, increases non-expert judge accuracy.
- Michael, J. et al. (2023). *Debate Helps Supervise Unreliable Experts*. arXiv:2311.08702. https://arxiv.org/abs/2311.08702 — Reports that debate between unreliable experts improves non-expert judges on hard reading-comprehension questions.

### Surveys and textbooks

- Bowman, S. R. et al. (2022). *Measuring Progress on Scalable Oversight for Large Language Models*. arXiv:2211.03540. https://arxiv.org/abs/2211.03540 — Builds a benchmark for whether model assistance helps non-expert judges, including debate-style setups.
