---
status: draft
last_reviewed: 2026-10-28
related:
  - society/human-ai-interaction
  - society/interpretability
  - brain-mind/psychology
tags:
  - automation bias
  - overreliance
  - human-AI interaction
  - skill erosion
aliases:
  - 自動化偏誤
  - 過度依賴
  - Automation bias
  - Overreliance
---

# Automation bias and overreliance

Automation bias is the tendency for people to rely on an automated aid's output too readily, so that they miss problems the aid does not flag and accept advice that is wrong. Overreliance is the broader term for the same pattern when the aid is an AI system, including language models. The effect is well documented in aviation and medicine, and it is now a central concern for people who use generative AI in their work.

## Overview

People using an automated aid face a trade-off. Checking the aid's output costs effort, and if the aid is usually right, checking can seem unnecessary. Over time, the habit of trusting the aid can outrun its reliability, so errors pass unnoticed. Automation bias describes the two kinds of error this produces: omission errors, where a person fails to act because the aid did not signal a problem, and commission errors, where a person acts on wrong advice from the aid. Overreliance is the same pattern seen at the level of an AI system's suggestions in ordinary work.

## Key concepts

- **Omission error**: failing to notice or respond to a problem because the automated aid did not flag it.
- **Commission error**: acting on the automated aid's incorrect advice despite other information.
- **Complacency**: reduced monitoring of an automated system when it has been reliable in the past.
- **Cognitive offloading**: delegating a mental task to an external tool, which can reduce the effort spent on the task itself.
- **Deskilling**: the loss of a skill through lack of practice, which can follow from long-term automation.

## How it works

Parasuraman and Manzey (2010) review the research on complacency and automation bias and integrate it with attention models. Their account is that people allocate attention between monitoring tasks and the automated system. When the system is reliable, monitoring becomes less frequent and less thorough, which lowers the chance of catching the system's occasional errors. The result depends on the reliability of the aid, the workload of the person, and how easily the errors can be checked.

Skitka, Mosier and Burdick (1999) tested this in a flight-simulation setting with an automated monitoring aid. They found that people made omission errors when the aid failed to flag a problem and commission errors when they followed a wrong recommendation, and that the errors were a measurable cost of relying on the aid rather than a matter of carelessness alone.

## Key methods

Experimental approaches differ in how they try to reduce the effect:

- **Explanations.** Bansal et al. (2021) study whether AI explanations help human-AI teams. They report that explanations often increased how readily people accepted AI recommendations, including incorrect ones, so that team performance gains were uneven across tasks.
- **Cost-benefit reasoning about checking.** Vasconcelos et al. (2023) argue and test that explanations reduce overreliance when the effort of checking them is low relative to the benefit of catching an error.
- **Cognitive forcing functions.** Buçinca, Malaya and Gajos (2021) introduce designs that delay or structure the AI's answer so that people think before accepting it. These reduced overreliance, but participants often rated them as less helpful, which shows a gap between what helps and what people want.

## Evidence from practice

The research in aviation and medicine predates generative AI, and its findings have been applied to AI decision support. Overreliance on language models has been studied in writing, coding and information-seeking tasks, where a plausible but wrong answer can be accepted without checking. Lee et al. (2025) surveyed knowledge workers and report that higher confidence in generative AI tools was associated with less reported critical thinking, while higher self-confidence in one's own skill was associated with more. The study is self-reported and cross-sectional, so it shows an association rather than a cause.

## Deskilling and cognitive offloading

Bainbridge (1983) described the "ironies of automation": automating a task removes the practice that keeps operators skilled, and the remaining manual tasks, such as handling rare failures, are the ones that need the most skill. The same argument is made for generative AI, where a worker who never drafts or checks a solution may lose the ability to do so. Evidence on this is still limited, and researchers distinguish between offloading that frees attention for better work and offloading that erodes skills people need.

## Connections

Automation bias is the behavioural side of the explanation problem in [Interpretability](../interpretability/index.md): explanations change what people trust, not only what they understand. It also links to the psychology of heuristics and biases in [Psychology](../../brain-mind/psychology/index.md), since the same mechanisms of attention and trust underlie these errors. The umbrella page [Human-AI interaction and trust](index.md) places automation bias next to companionship and AI literacy.

## Applications

- Clinical decision support, where a model's recommendation can change a diagnosis.
- Software development with coding assistants, where generated code can pass review without careful reading.
- Public-sector decisions that use automated scores.
- Education, where students may accept generated answers without learning the material.

## Open questions

- **Which designs reduce overreliance without reducing use of helpful advice?** The forcing functions that work also reduce how much people like the system.
- **Long-term effects.** Most studies are short; whether repeated use changes skill or trust over months is not well measured.
- **Generalisation across tasks.** Results from aviation and laboratory tasks may not carry over to open-ended generative tasks.

## References

### Seminal papers

- Skitka, L. J., Mosier, K. L. & Burdick, M. (1999). Does automation bias decision-making? *International Journal of Human-Computer Studies*, 51(5), 991–1006. https://doi.org/10.1006/ijhc.1999.0252 — Experimental study of omission and commission errors when people use an automated aid in a monitoring task.
- Bainbridge, L. (1983). Ironies of automation. *Automatica*, 19(6), 775–779. https://doi.org/10.1016/0005-1098(83)90046-8 — Argues that automating a process removes the practice needed for the human operator to handle failures.
- Bansal, G. et al. (2021). Does the Whole Exceed its Parts? The Effect of AI Explanations on Complementary Team Performance. *Proceedings of CHI 2021*. https://doi.org/10.1145/3411764.3445717 — Tests whether AI explanations improve human-AI team performance and finds effects that depend on the task.
- Buçinca, Z., Malaya, M. B. & Gajos, K. Z. (2021). To Trust or to Think: Cognitive Forcing Functions Can Reduce Overreliance on AI in AI-assisted Decision-making. *Proceedings of the ACM on Human-Computer Interaction*, 5(CSCW1). https://doi.org/10.1145/3449287 — Shows that forcing functions reduce overreliance and that participants prefer them less.
- Vasconcelos, H. et al. (2023). Explanations Can Reduce Overreliance on AI Systems During Decision-Making. *Proceedings of the ACM on Human-Computer Interaction*, 7(CSCW1). https://doi.org/10.1145/3579605 — Argues and tests that explanations reduce overreliance when checking them is cheap relative to the benefit.
- Lee, H.-P. et al. (2025). The Impact of Generative AI on Critical Thinking: Self-Reported Reductions in Cognitive Effort and Confidence. *Proceedings of CHI 2025*. https://doi.org/10.1145/3706598.3713778 — Survey associating confidence in generative AI with reported critical thinking.

### Surveys and textbooks

- Parasuraman, R. & Manzey, D. H. (2010). Complacency and Bias in Human Use of Automation: An Attentional Integration. *Human Factors*, 52(3), 381–410. https://doi.org/10.1177/0018720810376055 — Review of complacency and automation bias, integrating them into an account of attention allocation.

## Further learning

- [Transformer Circuits Thread](https://transformer-circuits.pub/) — background on how language models work, useful for judging when their output needs checking.
