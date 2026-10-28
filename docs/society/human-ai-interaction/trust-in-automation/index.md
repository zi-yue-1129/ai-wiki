---
status: draft
last_reviewed: 2026-10-28
aliases:
  - 適當依賴
  - 自動化中的信任
  - Trust in automation
  - Appropriate reliance
---

# Trust in Automation (Lee & See, 2004)

!!! info "Part of Human-AI Interaction and Trust"
    This method page belongs to [Human-AI Interaction and Trust](../index.md). It explains the framework in detail; the parent page compares it with the other landmark work.

Lee and See's 2004 framework defines appropriate reliance as trust that matches what an automated system can actually do. It names the properties of trust that a designer has to make visible, so that people can rely on a system when it is reliable and doubt it when it is not.

## Overview

The paper was written for automation in work settings, such as process control and vehicles, where a human operator supervises a machine. Its question is practical. If trust is what decides whether an operator uses an automated aid, how should the aid be designed so that the operator's trust follows its real capability? The authors answer by treating trust as an attitude with measurable properties, and by linking those properties to design choices.

The paper is the basis for much of the later thinking on [human-AI interaction](../index.md). It predates modern AI systems, so its examples are industrial, but its distinction between too little and too much trust still organises the field.

## Key concepts

- **Trust**: the attitude that an agent will help achieve an individual's goals in a situation marked by uncertainty and vulnerability.
- **Calibration**: how closely the level of trust matches the system's actual reliability. Trust that is too high leads to misuse; trust that is too low leads to disuse.
- **Resolution**: how finely trust tracks the system's performance across different conditions. A person whose trust rises and falls with the system's real performance has good resolution.
- **Specificity**: whether trust is attached to the particular functions of a system that work, rather than to the whole system at once.
- **Bases of trust**: the authors group what people judge a system by into its performance (what it does), its process (how it works, and whether that is appropriate for the situation) and its purpose (the designer's intent in building it).

## How it works

The framework can be read as a sequence of steps.

1. **The operator forms trust** from the system's observed performance, from information about its process, and from its stated purpose.
2. **Trust guides reliance.** The operator decides whether to rely on the system for a task, to control it manually, or to rely on it only partly.
3. **Reliance produces outcomes.** Some outcomes show whether the operator's trust was calibrated, for example when the system fails in a case the operator had trusted.
4. **Design aims at calibration.** The designer should show performance, process and purpose in a form the operator can use, so that trust moves with the system's real reliability rather than with its appearance.

The paper gives no equation. Its model is conceptual, and it is best read as a checklist of what a design must communicate.

## Results

The paper is a review and synthesis of empirical work on trust in automated systems, not a benchmark study. Its main contribution is the conceptual model and the design guidance that follows from it. It reports no accuracy figures of its own, and the page does not add any. Later studies of reliance on automation have used the calibration and resolution vocabulary to measure how well operators' trust matches a system's reliability.

## Limitations

- **Conceptual rather than quantitative.** The framework names what to measure, but it does not say how to measure calibration when a system's reliability is unknown or changes between tasks.
- **Industrial setting.** Its examples come from supervisory control. Generative AI differs in ways the framework does not cover: outputs are open-ended, errors are not always binary, and the system's reliability may not be stated at all.
- **Trust is partly self-reported.** Many studies that follow the framework rely on questionnaires, and self-reported trust does not always match behaviour. Hoff and Bashir (2014) review the empirical trust literature, which relies on such measures.
- **Explanation of process can cut both ways.** Showing how a system works can help people judge when to trust it, but it can also raise confidence that is not justified.

## Open questions

- How should a designer report the reliability of an open-ended system, where there is no single accuracy figure?
- Do disclosures about process and purpose improve calibration, or do they mainly increase confidence?
- How does trust recalibrate across repeated use, and how quickly does it recover after a visible failure?

## References

### Seminal papers

- Lee, J. D. & See, K. A. (2004). Trust in Automation: Designing for Appropriate Reliance. *Human Factors*. https://doi.org/10.1518/hfes.46.1.50_30392 — The framework itself: defines trust in automation, its calibration, resolution and specificity, and the design guidance for appropriate reliance.
- Parasuraman, R. & Riley, V. (1997). Humans and Automation: Use, Misuse, Disuse, Abuse. *Human Factors*. https://doi.org/10.1518/001872097778543886 — Gives the four named patterns of use of automation, which correspond to calibrated and miscalibrated trust.
- Parasuraman, R., Sheridan, T. B. & Wickens, C. D. (2000). A model for types and levels of human interaction with automation. *IEEE Transactions on Systems, Man, and Cybernetics*. https://doi.org/10.1109/3468.844354 — Proposes a model of the levels of automation across the stages of information processing, which shapes how much control the operator keeps.

### Surveys and textbooks

- Hoff, K. A. & Bashir, M. (2014). Trust in Automation: Integrating Empirical Evidence on Factors That Influence Trust. *Human Factors*. https://doi.org/10.1177/0018720814547570 — Reviews the operator, situational and learned factors that shape trust, and how the trust studies measured them.

### Articles and documentation

- Dietvorst, B. J., Simmons, J. P. & Massey, C. (2015). Algorithm aversion: People erroneously avoid algorithms after seeing them err. *Journal of Experimental Psychology: General*. https://doi.org/10.1037/xge0000033 — Shows the opposite failure of calibration: people drop an algorithm after one visible error, even when it is the better forecaster.
- Skitka, L. J., Mosier, K. L. & Burdick, M. (1999). Does automation bias decision-making? *International Journal of Human-Computer Studies*. https://doi.org/10.1006/ijhc.1999.0252 — Experimental evidence that people over-rely on automated aids, which is the miscalibrated-trust case the framework describes.
