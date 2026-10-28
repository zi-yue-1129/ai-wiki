---
status: draft
last_reviewed: 2026-10-28
related:
  - society/governance
tags:
  - alignment
  - evaluation
  - safety policy
aliases:
  - Dangerous capability evaluations
  - Frontier safety frameworks
  - 危險能力評估
  - 前沿安全框架
---

# Dangerous-capability evaluations and frontier safety frameworks

Dangerous-capability evaluations test whether an AI model has abilities that could enable serious harm, such as meaningful help with biological or chemical weapons, offensive cyber operations, or autonomous replication. Frontier safety frameworks are the policies that tie the results of those tests to commitments: which capability levels trigger which safeguards, and when a model may not be deployed. Together they are one of the main ways developers try to decide whether a model is safe to release.

## Overview

A general-purpose model can be used for many tasks, so a capability that is harmless in most hands may still matter for a small number of misuses. Evaluators therefore test for specific capabilities that would be serious if present, rather than only measuring average performance. Shevlane et al. (2023) argue that this kind of evaluation should become a standard part of responsible development, and they set out the categories of risk that such tests should cover.

Two structures have emerged. The first is an evaluation suite: a set of tasks, from question answering to multi-step agentic work, scored against thresholds. The second is a policy that connects scores to actions. Anthropic's Responsible Scaling Policy defines AI Safety Levels whose safeguards rise with capability, and Google DeepMind's Frontier Safety Framework names critical capability levels for domains such as cyber and autonomy. Other developers publish comparable frameworks under different names.

## Key concepts

- **Capability threshold**: a level of performance at which a model is treated as needing stronger safeguards, set in advance of testing.
- **Pre-deployment evaluation**: testing before release, usually by the developer and sometimes by an outside body.
- **Elicitation**: the effort used to bring out a model's capability, such as prompting, tools and fine-tuning. An evaluation that under-elicits underestimates risk.
- **Safeguard**: a measure, such as a refusal policy, a classifier or access control, that reduces a capability's usable risk.

## How it works

A typical cycle has four steps. Developers define risk domains and thresholds before a model is trained. They run evaluations on candidate models, including tests in which the model is given tools and a multi-step task. If a threshold is reached, the framework requires specific safeguards before deployment, and may require pausing development if the safeguards cannot be met. Results are documented in a model card or system card.

Phuong et al. (2024), working at Google DeepMind, describe evaluations for several dangerous capabilities, including persuasion, cyber-security tasks and self-proliferation, and report results for several frontier models on those tasks. Kinniment et al. (2023) evaluate language-model agents on realistic autonomous tasks, such as multi-step software and research work, to see how far models can complete tasks that would matter for autonomous replication. Biological risk is assessed with benchmarks such as WMDP, which Li et al. (2024) build to measure hazardous knowledge in biosecurity, cybersecurity and chemical security, and which they use to test unlearning methods.

## Key methods

Evaluation practice is still forming, so the landmark items are better described as approaches than as single algorithms:

- **Capability benchmarks** (Li et al., 2024; Phuong et al., 2024): fixed question sets or tasks scored against a threshold. They are easy to repeat but can be gamed and can go stale.
- **Agentic task evaluations** (Kinniment et al., 2023): models are given tools and open-ended tasks. They capture more of real capability but cost more and are harder to standardise.
- **Frontier safety frameworks** (Anthropic, 2024; Google DeepMind, 2024): policies that connect results to required safeguards and deployment decisions.
- **Third-party evaluation**: outside bodies run tests independently. Shevlane et al. (2023) make the case for this, since developers have an incentive to report favourable results.

## Limitations

- **Under-elicitation.** A test can miss a capability that a more determined user would find. Pre-deployment results are a lower bound.
- **Benchmark validity.** A test that measures knowledge may not measure whether a model can apply it, and a test that measures one task may not predict others.
- **Access.** Third-party evaluators often have less access to the model and its tools than the developer does.
- **Timing.** Evaluation happens before release, but capabilities can change after fine-tuning, deployment and new tools.
- **Self-assessment.** Frameworks written by developers depend on the developer's judgement of thresholds, which is why external review is often proposed.

## Connections

Risk evaluation has a long history in engineering and public health, where thresholds and independent testing are normal. Aircraft certification and drug trials are common analogies. These analogies are useful for the logic of thresholds and staged approval, though AI capabilities differ from physical products in that they can change after release. The question of what counts as a dangerous capability also depends on who is harmed and how, a topic linked to [governance](../governance/index.md). Methods for detecting dangerous knowledge or behaviour inside a model are part of [interpretability](../interpretability/index.md), and deceptive behaviour, which would make evaluations misleading, is discussed in [deceptive alignment](deceptive-alignment.md).
## Applications

- Pre-release evaluation and reporting in model cards and system cards.
- Government-led testing by national AI safety institutes, such as those in the UK and the US.
- Benchmarks such as WMDP that let researchers compare safeguards and unlearning methods.

## Open questions

- How should thresholds be set when the harms are uncertain and the benefits of a capability are also large?
- Can evaluations reliably detect capabilities that a model conceals, as discussed in [deceptive alignment](deceptive-alignment.md)?
- Who should be allowed to see the full results, and what should be published?

## References

### Seminal papers

- Shevlane, T. et al. (2023). *Model evaluation for extreme risks*. arXiv:2305.15324. https://arxiv.org/abs/2305.15324 — Argues that developers should evaluate models for dangerous capabilities and sets out the risk categories such tests should cover.
- Phuong, M. et al. (2024). *Evaluating Frontier Models for Dangerous Capabilities*. arXiv:2403.13793. https://arxiv.org/abs/2403.13793 — Reports evaluations of frontier models across several dangerous-capability domains.
- Kinniment, M. et al. (2023). *Evaluating Language-Model Agents on Realistic Autonomous Tasks*. arXiv:2312.11671. https://arxiv.org/abs/2312.11671 — Evaluates language-model agents on multi-step autonomous tasks relevant to autonomous replication.
- Li, N. et al. (2024). *The WMDP Benchmark: Measuring and Reducing Malicious Use With Unlearning*. arXiv:2403.03218. https://arxiv.org/abs/2403.03218 — A benchmark of hazardous knowledge in biosecurity, cybersecurity and chemical security, used to test unlearning.

### Articles and documentation

- Anthropic, *Anthropic's Responsible Scaling Policy*. https://www.anthropic.com/responsible-scaling-policy — The developer's policy defining AI Safety Levels and the safeguards required at each.
- Google DeepMind, *Introducing the Frontier Safety Framework*, 17 May 2024. https://deepmind.google/discover/blog/introducing-the-frontier-safety-framework/ — Describes critical capability levels and the procedure for responding when a model reaches them.
