---
status: draft
last_reviewed: 2026-10-28
aliases:
  - 認知強制功能
  - 認知強制
  - Cognitive forcing functions
  - Need for cognition
---

# Cognitive Forcing Functions (Buçinca et al., 2021)

!!! info "Part of Human-AI Interaction and Trust"
    This method page belongs to [Human-AI Interaction and Trust](../index.md). It explains the experiment in detail; the parent page compares it with the other landmark work.

Buçinca, Malaya and Gajos (2021) test whether interface designs that make people think before they accept an AI suggestion reduce overreliance. In an experiment with 199 participants, the designs they call cognitive forcing reduced overreliance compared with simple explainable-AI designs. However, participants rated these designs least favourably, and the benefit was larger for people who are more motivated to think effortfully.

## Overview

The paper starts from a puzzle. People using AI decision support often accept its suggestions even when they are wrong, and adding explanations does not appear to reduce this. The authors argue that people rarely analyse each recommendation and explanation one by one. Instead they build general heuristics about when to follow the AI. Their remedy is to change the interface so that the heuristic is interrupted, and the person has to engage with the explanation before deciding.

The work draws on dual-process theory, which separates fast, automatic judgement from slower, analytical reasoning. It also builds on earlier research on medical decision-making, which the authors use to shape the interventions. The [psychology](../../../brain-mind/psychology/index.md) overview covers the dual-process frame in more detail, and the [human-AI interaction](../index.md) overview places this experiment among the other landmark methods.

## Key concepts

- **Overreliance**: accepting an AI recommendation that is wrong. The paper measures it as the share of wrong recommendations that participants accept.
- **Dual-process theory**: the distinction between quick, heuristic judgement and slower, deliberate analysis. Overreliance is treated as a case where the quick route is used when the slow route is needed.
- **Cognitive forcing**: an interface intervention that compels a person to engage more thoughtfully with the AI's output, rather than accepting it by default.
- **Need for Cognition**: an individual difference, the stable motivation to engage in effortful thinking. The authors use it to check whether an intervention helps some people more than others.

## How it works

The experiment compares several conditions in a decision-making task with AI support. The steps can be read as a procedure.

1. **Present a decision task.** Participants make decisions for a series of cases, with an AI recommendation that is sometimes wrong.
2. **Vary the presentation.** Three cognitive forcing designs change how the recommendation and its explanation are shown, so that the person has to engage with them before accepting. The abstract describes them as interventions designed to compel more thoughtful engagement with the explanations. The paper defines no single equation for them.
3. **Compare with baselines.** The same tasks are run with two simple explainable-AI designs and with a no-AI baseline.
4. **Record two kinds of outcome.** The first is overreliance, measured by how often wrong recommendations are accepted. The second is participants' subjective rating of each design.
5. **Audit for unequal benefit.** Participants are grouped by Need for Cognition, to see whether the designs help people in each group equally.

There is no benchmark dataset and no algorithm. The method is an experimental design, and its value lies in comparing designs under the same conditions.

## Results

The abstract reports the main findings in qualitative terms, with one number, the sample size of 199 participants.

- Cognitive forcing **significantly reduced overreliance** compared with the simple explainable-AI approaches.
- There was a **trade-off**: the designs that reduced overreliance the most received the least favourable subjective ratings.
- The interventions **benefited participants with higher Need for Cognition more**, which the authors read as evidence that cognitive motivation moderates how well explainable AI works.

The page does not add figures beyond those in the abstract. The full paper contains the detailed comparisons, and they should be checked there before any effect size is quoted.

## Limitations

- **One experiment.** The result comes from a single study with a fixed set of tasks and a fixed AI. It does not show how the designs perform in long-term, real workflows.
- **Acceptance is part of the outcome.** A design that people dislike may be abandoned in practice, so reduced overreliance on paper may not persist. The trade-off in ratings is therefore central, not a side note.
- **Unequal benefit.** If the designs help people who already engage deliberately more than those who do not, they may widen differences between users instead of closing them.
- **Narrow interventions.** The three designs are specific to the experiment. The principle may generalise, but the particular designs may not.

## Open questions

- Can a design keep the reduction in overreliance while getting better ratings from users?
- Should cognitive forcing be the default for high-stakes decision support, or should it be offered only when the stakes or the uncertainty call for it?
- Do people learn to rely on the AI more carefully over time, or does the benefit fade once the forcing step becomes routine?

## References

### Seminal papers

- Buçinca, Z., Malaya, M. B. & Gajos, K. Z. (2021). To Trust or to Think: Cognitive Forcing Functions Can Reduce Overreliance on AI in AI-assisted Decision-making. *CSCW 2021*. https://arxiv.org/abs/2102.09692 — The experiment itself: three cognitive forcing designs compared with explainable-AI and no-AI conditions, with N=199 participants.
- Lee, J. D. & See, K. A. (2004). Trust in Automation: Designing for Appropriate Reliance. *Human Factors*. https://doi.org/10.1518/hfes.46.1.50_30392 — The framework of calibrated trust that the cognitive forcing work extends to AI decision support.

### Surveys and textbooks

- Vasconcelos, H. et al. (2023). Explanations Can Reduce Overreliance on AI Systems During Decision-Making. arXiv:2212.06823. https://arxiv.org/abs/2212.06823 — Studies when explanations reduce overreliance on AI and when they do not, in decision-making experiments.
- Green, B. & Chen, Y. (2019). The Principles and Limits of Algorithm-in-the-Loop Decision Making. *Proceedings of the ACM on Human-Computer Interaction*. https://doi.org/10.1145/3359152 — Reviews why people often cannot tell when an algorithm is accurate, and what that means for algorithm-in-the-loop decisions.

### Articles and documentation

- Wang, D. et al. (2019). Designing Theory-Driven User-Centric Explainable AI. *CHI '19*. https://doi.org/10.1145/3290605.3300831 — Ties the design of explanations to cognitive theories of human reasoning and tests the resulting design with users.
- Amershi, S. et al. (2019). Guidelines for Human-AI Interaction. *CHI '19*. https://doi.org/10.1145/3290605.3300233 — Design guidelines for AI products that cover how a system should present its outputs and explanations to users.
- Lai, V. & Tan, C. (2018). On Human Predictions with Explanations and Predictions of Machine Learning Models: A Case Study on Deception Detection. arXiv:1811.07901. https://arxiv.org/abs/1811.07901 — Compares human decisions with and without model predictions and explanations on a deception-detection task.
