---
status: draft
last_reviewed: 2026-10-28
related:
- theory/paradigms/reinforcement-learning
- brain-mind/neuroscience
tags:
- reinforcement learning
- decision making
aliases:
  - 有模型與無模型控制
  - 模型基礎與模型自由
  - Model-Based vs Model-Free
  - Model-Free Reinforcement Learning
---

# Model-Based vs Model-Free Control

Model-based and model-free control are two ways an agent can choose actions from experience. A model-free controller learns how good each action is, directly from past rewards. A model-based controller learns how the world works, and plans with that model. The distinction comes from reinforcement learning, and neuroscience has used it to ask which of the two the brain relies on, and when.

This page is part of [Decision Making, Dopamine & Reward](../index.md). The parent page gives the overview; this page covers the distinction and the arbitration proposal of Daw, Niv and Dayan (2005).

## Overview

Consider choosing between two routes to work after a road closure. A model-free habit says "last time I went left and it was fine, so go left". A model-based plan says "the closure is on the left, so go right", using knowledge of the road network. The habit is cheap and quick; the plan adapts immediately to changes but costs more computation and time.

## Key concepts

- **Model-free value**: an estimate of how good an action is, learned from the reward that followed it. Updates use the reward prediction error, the difference between reward received and reward expected.
- **Model-based value**: an estimate obtained by planning over a learned model of transitions (what leads to what) and rewards (what each outcome is worth).
- **Flexibility**: model-based control updates at once when the environment changes, because the model is changed and the plan follows. Model-free control has to relearn the values through experience.
- **Cost**: model-free control is cheap at decision time; model-based control costs computation at each choice.
- **Arbitration**: the rule that decides which controller's choice is used when they disagree.

## Arbitration by uncertainty

Daw, Niv and Dayan (2005) start from the observation that the brain appears to have more than one controller for choosing behaviour, including one linked to prefrontal cortex and one to dorsolateral striatum. Their question is which should win when they disagree.

Their answer uses reinforcement learning theory. The two systems trade off computational simplicity against flexible, statistically efficient use of experience. The proposal is a Bayesian arbitration rule based on uncertainty: at each moment, the controller whose estimate is more reliable takes over. The authors argue that this rule accounts for a range of experimental findings about which system dominates in which situation.

In outline, the arbitration works as follows:

1. Keep a model-free estimate of action values, learned from reward prediction errors.
2. Keep a model-based estimate, obtained by planning over a learned model.
3. Estimate the uncertainty of each controller from its recent accuracy.
4. Let the controller with lower uncertainty control the choice.

The paper's exact formulation of the uncertainty and the arbitration is more detailed than this outline, and the abstract summary used here does not state its equations.

## Results

The abstract reports that the uncertainty-based rule explains a range of experimental findings about the dominance of the two systems, and it does so qualitatively. It gives no numerical fits, so the page does not quote any.

## Limitations

- The proposal is a theory of arbitration, and the evidence it explains comes from a limited set of experimental paradigms.
- How the two controllers map onto specific brain regions is an open question; the abstract does not settle it.
- The two systems may interact in ways a simple switch does not capture, for example one training the other, and the arbitration view does not exclude that.

## Connections

- **Reward prediction error**: the model-free controller is updated by the same prediction error that dopamine neurons signal. See [Neuroscience Basics](../../neuroscience/index.md), where the dopamine key method is described.
- **Diffusion decision model**: a different question, about how evidence accumulates into a choice. See [Diffusion Decision Model](../diffusion-model/index.md).
- **Reinforcement learning**: the same distinction is central to AI agents, which combine learned values with planning. See [Reinforcement Learning](../../../theory/paradigms/reinforcement-learning/index.md).

## Applications

- **Computational psychiatry**: fitting models that weight model-based and model-free control to behaviour, to study conditions such as addiction and compulsion. These are research tools, not clinical diagnoses.
- **AI agents**: many systems combine a learned value function, the model-free part, with search or planning over a learned model, the model-based part, and the choice of how to combine them is a practical design question.

## Open questions

- **Do the systems compete or cooperate?** Arbitration treats them as competitors, while training one from the other suggests cooperation.
- **What signal drives arbitration?** Uncertainty is one candidate; the brain may use other signals, such as cost or time pressure.
- **How do the systems map onto the brain?** The prefrontal and striatal correspondence is a useful starting point but needs direct tests.

## References

### Seminal papers

- Daw, N. D., Niv, Y. & Dayan, P. (2005). Uncertainty-based competition between prefrontal and dorsolateral striatal systems for behavioral control. *Nature Neuroscience*. https://doi.org/10.1038/NN1560 — Proposes uncertainty-based arbitration between model-based and model-free controllers.
- Schultz, W., Dayan, P. & Montague, P. R. (1997). A Neural Substrate of Prediction and Reward. *Science*. https://doi.org/10.1126/science.275.5306.1593 — Shows that dopamine neurons signal reward prediction errors, the learning signal that model-free control uses.

### Surveys and reviews

- Gold, J. I. & Shadlen, M. N. (2007). The neural basis of decision making. *Annual Review of Neuroscience*. https://doi.org/10.1146/annurev.neuro.29.051605.113038 — Background on how neurons accumulate evidence toward a decision, cited here for the neural framing of choice in general.
- Dayan, P. & Daw, N. D. (2008). Decision theory, reinforcement learning, and the brain. *Cognitive, Affective, & Behavioral Neuroscience*. https://doi.org/10.3758/CABN.8.4.429 — Reviews how decision theory and reinforcement learning models relate to choice in the brain, including the two controllers.
- Sutton, R. S. & Barto, A. G. (2018). *Reinforcement Learning: An Introduction*, 2nd ed. MIT Press. http://incompleteideas.net/book/the-book-2nd.html — The standard textbook on model-free value learning and planning with models.
