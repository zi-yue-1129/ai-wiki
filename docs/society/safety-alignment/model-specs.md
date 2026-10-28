---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/llm/instructgpt-rlhf
tags:
  - alignment
  - policy
aliases:
  - Model specifications
  - Model spec
  - Instruction hierarchy
  - 模型規範
  - 指令層級
---

# Model specifications and behaviour policies

A model specification, or model spec, is a document that states how an AI system is intended to behave: what it should do by default, what it should refuse, how it should weigh instructions from different parties, and how conflicts are resolved. Developers publish these documents, or parts of them, so that outsiders can compare intended behaviour with observed behaviour. They are one of the most visible forms of principle-based alignment, alongside [Constitutional AI](constitutional-ai.md).

## Overview

A language model receives instructions from several sources at once: the developer who built the product, the business that deploys it, and the user who types into it. It also has its own defaults. A model spec defines which of these should win when they conflict. For example, a developer may restrict the model to a topic, but the user should still be told when a request is out of scope, and some protections for users may not be overridden by any developer.

This is a policy question as much as a technical one. Specifications make choices about what a model should and should not do, and those choices affect many users. Publishing the spec lets people contest the choices. Without a spec, behaviour can still be shaped, but the shaping is less visible.

## Key concepts

- **Instruction hierarchy**: a ranking of instruction sources, such as system, developer, user and tool outputs, that determines which instruction takes precedence.
- **Default behaviour**: what the model does when no instruction covers a situation.
- **Hard constraints**: behaviours that no instruction can change.
- **Auditing**: checking observed behaviour against the stated spec.

## How behaviour is specified

Specifications work at three levels. Some rules are stated as principles, such as respecting the user's autonomy or avoiding deception about the model's nature. Others are stated as examples of desired and undesired responses, which make intent concrete but can leave gaps. A third level is the training method, which determines how the spec is turned into behaviour.

Two training approaches tie the spec to the model directly. Wallace et al. (2024) train models to follow a strict instruction hierarchy, so that instructions from lower-priority sources such as tool outputs are not obeyed when they conflict with higher-priority instructions. They report that this improves robustness against prompt injection, while noting that it does not eliminate the problem. Guan et al. (2024) propose deliberative alignment, in which a model is trained to recall relevant parts of a safety specification and reason about them before responding. The model is given the text of the spec, so the behaviour follows from written rules rather than from examples alone.

Askell et al. (2021) describe an earlier step in the same direction. They use a general assistant, trained to be helpful, honest and harmless, as a testbed for alignment methods and argue that stated behavioural goals make it possible to measure progress.

## Auditing

A written spec makes auditing possible. Evaluators can write test prompts that target each stated rule and check whether the model complies. Disagreement between the spec and observed behaviour is evidence of a training gap, a specification gap, or both. Auditing faces the same difficulties as other evaluations: a finite set of tests cannot cover every situation, and a model that behaves well when tested may behave differently in deployment (see [dangerous-capability evaluations](dangerous-capability-evals.md)).

## Disagreements about who decides

Specifications raise questions that are not purely technical:

- **Authority.** The developer writes the spec, but the people affected by a model's behaviour did not. Some proposals call for public input or for competing specs that users can choose between.
- **Values.** A spec states which values take priority when they conflict, such as safety against user autonomy. Reasonable people weigh these differently, and the spec does not settle the question.
- **Transparency.** Publishing a spec helps outsiders check behaviour, but a spec can describe intent without describing the training data or procedures that realise it.
- **Local norms.** A single global spec may not match the legal or cultural expectations of every deployment.

These disagreements connect to the wider debate in [governance](../governance/index.md) and [ethics](../ethics/index.md).

## Connections

A spec resembles the codes of conduct that professional bodies publish, such as medical codes that set out duties to patients and limits on what a practitioner may do. The analogy suggests that stated norms, enforced through training and review, can shape behaviour in a predictable way, though a model is not a practitioner bound by professional sanctions. Models that follow an instruction hierarchy also raise the question of how a system distinguishes instructions from information, which is studied in [language models](../../theory/models/llm/index.md).

## Applications

- Public model specs used by developers to communicate intended behaviour to users, deployers and researchers.
- Instruction-hierarchy training to reduce prompt injection in agents that read untrusted content.
- Automated auditing of model behaviour against written rules.

## Open questions

- How complete can a spec be, and what should happen in cases it does not cover?
- Who should decide the priorities a spec encodes, and how can affected groups take part?
- Do training methods that reason over a written spec generalise to situations the spec did not anticipate?

## References

### Seminal papers

- Askell, A. et al. (2021). *A General Language Assistant as a Laboratory for Alignment*. arXiv:2112.00861. https://arxiv.org/abs/2112.00861 — Uses a helpful, honest and harmless assistant as a testbed for measuring progress on alignment.
- Wallace, E. et al. (2024). *The Instruction Hierarchy: Training LLMs to Prioritize Privileged Instructions*. arXiv:2404.13208. https://arxiv.org/abs/2404.13208 — Trains models to prioritise system and developer instructions over conflicting user or tool instructions, improving resistance to prompt injection.
- Guan, M. Y. et al. (2024). *Deliberative Alignment: Reasoning Enables Safer Language Models*. arXiv:2412.16339. https://arxiv.org/abs/2412.16339 — Trains models to reason over a written safety specification before responding.

### Surveys and textbooks

- Bai, Y. et al. (2022). *Constitutional AI: Harmlessness from AI Feedback*. arXiv:2212.08073. https://arxiv.org/abs/2212.08073 — Uses a written set of principles to guide training, the approach that stated specifications build on.

### Articles and documentation

- Anthropic, *Anthropic's Responsible Scaling Policy*. https://www.anthropic.com/responsible-scaling-policy — Developer policy that connects stated commitments to required safeguards, an example of a published behaviour and safety commitment.
