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

Parasuraman and Manzey (2010) review the research on complacency and bias in human use of automation and integrate it into an attentional account, as their title states. On this view, the question is how people allocate attention between monitoring and the automated system. When the system is reliable, monitoring becomes less frequent and less thorough, which lowers the chance of catching the system's occasional errors. The result depends on the reliability of the aid, the workload of the person, and how easily the errors can be checked.

Skitka, Mosier and Burdick (1999) study whether automated decision aids bias people's decisions, in a paper titled "Does automation bias decision-making?"

## Key methods

Experimental approaches differ in how they try to reduce the effect:

- **Explanations.** Bansal et al. (2021) test whether AI explanations improve complementary team performance, where the team does better than the human or the AI working alone.
- **Cost-benefit reasoning about checking.** Vasconcelos et al. (2023) report that overreliance does not generally fall when an AI gives explanations, and argue with a cost-benefit framework that people strategically choose whether to engage with an explanation. In some scenarios explanations do reduce overreliance.
- **Cognitive forcing functions.** Buçinca, Malaya and Gajos (2021) design three cognitive forcing interventions that compel people to engage more thoughtfully with AI explanations. In an experiment with 199 participants, they compare these with two explainable-AI designs and a no-AI baseline.

## Evidence from practice

The research in aviation and medicine predates generative AI, and its findings have been applied to AI decision support. Overreliance on language models is an active research area, where a plausible but wrong answer can be accepted without checking. Lee et al. (2025) report, from a survey, self-reported reductions in cognitive effort and confidence when people use generative AI. Self-report measures what people say about their own thinking, not how their performance changes.

## Deskilling and cognitive offloading

Bainbridge (1983) discusses the "ironies of automation" in automated systems. Whether generative AI produces a similar loss of skill is an open question, and this page does not treat it as established.

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

- Skitka, L. J., Mosier, K. L. & Burdick, M. (1999). Does automation bias decision-making? *International Journal of Human-Computer Studies*, 51(5), 991–1006. https://doi.org/10.1006/ijhc.1999.0252 — Study of whether automated decision aids bias people's decisions, as its title asks.
- Bainbridge, L. (1983). Ironies of automation. *Automatica*, 19(6), 775–779. https://doi.org/10.1016/0005-1098(83)90046-8 — Discusses the ironies of automation, as its title states.
- Bansal, G. et al. (2021). Does the Whole Exceed its Parts? The Effect of AI Explanations on Complementary Team Performance. *Proceedings of CHI 2021*. https://doi.org/10.1145/3411764.3445717 — Finds that explanations do not raise complementary team performance, though they increase acceptance of the AI's recommendation.
- Buçinca, Z., Malaya, M. B. & Gajos, K. Z. (2021). To Trust or to Think: Cognitive Forcing Functions Can Reduce Overreliance on AI in AI-assisted Decision-making. *Proceedings of the ACM on Human-Computer Interaction*, 5(CSCW1). https://doi.org/10.1145/3449287 — Designs three cognitive forcing interventions and compares them with explanation-only designs and a no-AI baseline.
- Vasconcelos, H. et al. (2023). Explanations Can Reduce Overreliance on AI Systems During Decision-Making. *Proceedings of the ACM on Human-Computer Interaction*, 7(CSCW1). https://doi.org/10.1145/3579605 — Argues, with a cost-benefit framework, that explanations can reduce overreliance in some scenarios.
- Lee, H.-P. et al. (2025). The Impact of Generative AI on Critical Thinking: Self-Reported Reductions in Cognitive Effort and Confidence Effects From a Survey of Knowledge Workers. *Proceedings of CHI 2025*. https://doi.org/10.1145/3706598.3713778 — Survey of knowledge workers on self-reported reductions in cognitive effort and confidence with generative AI.

### Surveys and textbooks

- Parasuraman, R. & Manzey, D. H. (2010). Complacency and Bias in Human Use of Automation: An Attentional Integration. *Human Factors*, 52(3), 381–410. https://doi.org/10.1177/0018720810376055 — Review of complacency and automation bias, integrating them into an account of attention allocation.

## Further learning

- [Transformer Circuits Thread](https://transformer-circuits.pub/) — background on how language models work, useful for judging when their output needs checking.
