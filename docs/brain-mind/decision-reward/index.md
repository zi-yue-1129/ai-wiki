---
status: draft
last_reviewed: 2026-10-28
related:
- brain-mind/neuroscience
- brain-mind/cognitive-science
- brain-mind/psychology
- brain-mind/predictive-coding
tags:
- neuroscience
- decision making
- reinforcement learning
aliases:
  - 決策與獎勵
  - 多巴胺與獎勵
  - Decision Making
  - Dopamine and Reward
---

# Decision Making, Dopamine and Reward

Deciding is the point where perception and value meet action. The brain must weigh evidence, estimate what each option is likely to bring, and commit to one. Reinforcement learning, the main AI framework for choosing actions, was shaped by this neuroscience, and the two fields now test each other's models.

## Overview

A decision has two parts. The first is evidence: how much information supports each option, which is often noisy and accumulates over time. The second is value: how much each option is worth, which is learned from past outcomes. Neuroscience has studied both, and the most productive models link them through a shared learning signal, dopamine. [Cognitive Science](../cognitive-science/index.md) covers the psychology of reasoning and choice; this page focuses on the neural and computational mechanisms.

## Key concepts

- **Evidence accumulation**: the process of summing noisy sensory evidence over time until it reaches a threshold, at which point the choice is made.
- **Speed-accuracy trade-off**: waiting longer for evidence improves accuracy but delays the decision. Models describe this trade-off with a decision boundary.
- **Value**: the expected reward of an option, estimated from experience.
- **Model-free and model-based control**: model-free methods cache the value of actions from past rewards, which is cheap but slow to adapt. Model-based methods plan with a model of the environment, which is flexible but costly.
- **Reward prediction error**: the difference between the reward received and the reward expected. Dopamine neurons signal this quantity, as summarised in [Neuroscience Basics](../neuroscience/index.md).

## How it works

Two broad mechanisms explain most of the data. In perceptual decisions, evidence accumulates toward a bound, and the sensory and parietal cortex carry the running total. In value-based decisions, the basal ganglia learn which actions lead to reward, and dopamine updates those values. Many models combine the two, using accumulated evidence for quick perceptual choices and learned values for choices made from experience.

```mermaid
flowchart LR
  E[Sensory evidence] --> A[Accumulate noisy<br/>evidence over time]
  A --> B{Reached<br/>bound?}
  B -- no --> A
  B -- yes --> C[Choice]
  R[Reward] --> P[Reward prediction<br/>error, dopamine]
  P --> V[Update action values<br/>basal ganglia]
  V -. biases .-> A
```

The loop in the diagram is a common shape for these theories. Learned values bias the starting point or drift of accumulation, so experience changes how quickly and accurately people decide.

## Key methods

Each method has its own page. This table is only a comparison.

| Method | Question it answers | Page |
|---|---|---|
| Diffusion decision model (Ratcliff & McKoon, 2008) | Which process changes when difficulty or instructions change: information quality, caution, or bias? | [Diffusion Decision Model](diffusion-model/index.md) |
| Model-based vs model-free arbitration (Daw, Niv & Dayan, 2005) | When the two controllers disagree, which one should control choice? | [Model-Based vs Model-Free Control](model-based-vs-model-free/index.md) |

The dopamine reward prediction error (Schultz, Dayan & Montague, 1997), the third landmark, is covered on [Neuroscience Basics](../neuroscience/index.md) and is not repeated here.

## Connections

- **Neuroscience**: the basal ganglia, the dopamine reward prediction error and neuromodulation are in [Neuroscience Basics](../neuroscience/index.md).
- **Cognitive science**: reasoning and decision making, including the dual-process view, are in [Cognitive Science](../cognitive-science/index.md).
- **Psychology**: cognitive biases and the human side of choice, including how people respond to AI advice, are in [Psychology & AI](../psychology/index.md).
- **Predictive coding**: active inference treats choice as inference over preferred outcomes, a different route to decisions from value learning. See [Predictive Coding & Free Energy](../predictive-coding/index.md).
- **Reinforcement learning in AI**: the reward prediction error is the core update of temporal-difference learning, the basis of much AI research on agents. See [Reinforcement Learning](../../theory/paradigms/reinforcement-learning/index.md).

## Applications

- **Computational psychiatry**: models of learning and choice are fitted to behaviour to study conditions such as addiction and depression. These are research tools, not clinical diagnoses.
- **Human-AI decision support**: understanding how people accumulate evidence and weigh AI advice helps design interfaces that avoid over-reliance. See [Psychology & AI](../psychology/index.md).
- **AI agents**: reinforcement learning methods that learn values from reward, and planning methods that use a model, are the AI counterparts of the two controllers.

## Open questions

- **Do model-free and model-based systems really compete?** Arbitration accounts fit many results, but the systems may interact in other ways, such as one training the other.
- **How does dopamine relate to value, salience and action?** The prediction error account is strong, but dopamine may also signal motivation or novelty, and the debate continues.
- **Are drift-diffusion parameters neural quantities?** Fitted parameters are useful summaries, but mapping them onto specific neurons is still under test.
- **How well do AI agents mirror these controllers?** Current agents combine learned values and planning, but whether the trade-off works the same way is unclear.

## References

### Seminal papers

- Ratcliff, R. & McKoon, G. (2008). The Diffusion Decision Model: Theory and Data for Two-Choice Decision Tasks. *Neural Computation*. https://doi.org/10.1162/neco.2008.12-06-420 — Reviews the diffusion model and shows how its parameters separate the effects of difficulty, speed-accuracy instructions and bias.
- Daw, N. D., Niv, Y. & Dayan, P. (2005). Uncertainty-based competition between prefrontal and dorsolateral striatal systems for behavioral control. *Nature Neuroscience*. https://doi.org/10.1038/NN1560 — Proposes uncertainty-based arbitration between model-based and model-free controllers.
- Schultz, W., Dayan, P. & Montague, P. R. (1997). A Neural Substrate of Prediction and Reward. *Science*. https://doi.org/10.1126/science.275.5306.1593 — Shows that dopamine neurons signal reward prediction errors, linking reinforcement learning to the brain.

### Surveys and reviews

- Gold, J. I. & Shadlen, M. N. (2007). The neural basis of decision making. *Annual Review of Neuroscience*. https://doi.org/10.1146/annurev.neuro.29.051605.113038 — A review of how neurons accumulate evidence toward a decision, the framework behind the diffusion models.
- Dayan, P. & Daw, N. D. (2008). Decision theory, reinforcement learning, and the brain. *Cognitive, Affective, & Behavioral Neuroscience*. https://doi.org/10.3758/CABN.8.4.429 — Reviews how decision theory and reinforcement learning models relate to choice in the brain.
- Sutton, R. S. & Barto, A. G. (2018). *Reinforcement Learning: An Introduction*, 2nd ed. MIT Press. http://incompleteideas.net/book/the-book-2nd.html — The standard textbook on value learning, temporal-difference methods and planning with models.
