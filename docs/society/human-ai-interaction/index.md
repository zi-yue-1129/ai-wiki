---
status: draft
last_reviewed: 2026-10-28
related:
  - society
  - society/interpretability
  - society/ethics
  - brain-mind/psychology
tags:
  - human-AI interaction
  - trust
  - overreliance
aliases:
  - 人機互動與信任
  - 人機互動
  - Human-AI interaction
  - Human-AI trust
---

# Human-AI interaction and trust

Human-AI interaction is the study of how people use, trust, over-trust and are changed by AI systems. Whether an AI system is accurate matters less than how the people who use it come to rely on it, understand it and adjust their own work around it. This section covers that relationship, from the cognitive mechanisms of trust to the design of explanations, the role of humans in the loop and the long-term effects on skills.

## Overview

A system can be correct most of the time and still be used badly. People may trust it too much and stop checking, trust it too little and ignore useful advice, or form a relationship with it that changes their behaviour in ways no one intended. Human-AI interaction brings together psychology, human-computer interaction and the social science of technology to explain these patterns and to design systems that support better use.

## Topics

| Page | Focus |
|---|---|
| [Automation bias and overreliance](automation-bias.md) | Omission and commission errors, the effect of explanations, cognitive forcing functions, deskilling |
| [AI companionship](ai-companionship.md) | Emotional attachment to conversational systems and its effects on wellbeing |
| [AI literacy and public understanding](ai-literacy.md) | What people need to know to judge AI output and to take part in governing it |

## Key concepts

- **Trust calibration**: the match between how much a person relies on a system and how reliable it actually is.
- **Overreliance**: relying on a system beyond its reliability, which can lead to errors that go unnoticed.
- **Explanation design**: how a system presents its reasons, and whether those reasons help people decide better.
- **Human-in-the-loop**: a design in which a person reviews, approves or can override an automated decision.
- **Deskilling**: loss of a skill through long-term reliance on a tool that performs it.

## How it works

People form expectations about a system from its interface, its fluency and its past performance. When those expectations match the system's reliability, reliance is appropriate. When they do not, errors follow. Explanations, confidence displays and the order in which information is presented all change those expectations, sometimes in ways that increase reliance without improving accuracy.

Human-in-the-loop designs assume a person can catch the system's mistakes. That assumption holds only when the person has the time, the information and the skill to check. Where these conditions are missing, a nominal human review can add little safety. The same concern applies to organisations that use AI-generated outputs as a basis for decisions.

## Connections

The explanation problem links to [Interpretability](../interpretability/index.md), where the methods that generate explanations are described. The fairness and accountability issues that arise when people rely on automated decisions are covered in [Ethics & Fairness](../ethics/index.md). The psychological mechanisms of attention and trust are in [Psychology](../../brain-mind/psychology/index.md).

## Applications

- Clinical decision support, where clinicians must decide when to follow a model's recommendation.
- Writing and coding tools, where drafts can be accepted without close reading.
- Public-sector scoring systems, where officials must justify decisions that rely on automated scores.
- Education, where AI tutors and assistants affect how students practise and learn.

## Open questions

- **Which design choices produce calibrated trust** across different users and tasks?
- **Long-term change.** How repeated use shapes skills, expectations and relationships over months and years.
- **Responsibility.** Who is accountable when a person accepts an AI recommendation that proves wrong.

## References

### Seminal papers

- Parasuraman, R. & Manzey, D. H. (2010). Complacency and Bias in Human Use of Automation: An Attentional Integration. *Human Factors*, 52(3), 381–410. https://doi.org/10.1177/0018720810376055 — Review of how complacency and bias shape the use of automated systems.
- Bansal, G. et al. (2021). Does the Whole Exceed its Parts? The Effect of AI Explanations on Complementary Team Performance. *Proceedings of CHI 2021*. https://doi.org/10.1145/3411764.3445717 — Tests whether explanations improve human-AI team performance.
- Vasconcelos, H. et al. (2023). Explanations Can Reduce Overreliance on AI Systems During Decision-Making. *Proceedings of the ACM on Human-Computer Interaction*, 7(CSCW1). https://doi.org/10.1145/3579605 — Shows that explanations reduce overreliance under a cost-benefit account of checking.
- Bainbridge, L. (1983). Ironies of automation. *Automatica*, 19(6), 775–779. https://doi.org/10.1016/0005-1098(83)90046-8 — Identifies how automation can leave operators less prepared for the failures they must handle.

### Surveys and textbooks

- Lee, H.-P. et al. (2025). The Impact of Generative AI on Critical Thinking: Self-Reported Reductions in Cognitive Effort and Confidence. *Proceedings of CHI 2025*. https://doi.org/10.1145/3706598.3713778 — Survey of knowledge workers on generative AI use and critical thinking.

## Further learning

- [Transformer Circuits Thread](https://transformer-circuits.pub/) — background on how language models work, which helps judge when their output needs checking.
