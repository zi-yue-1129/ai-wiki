---
status: draft
last_reviewed: 2026-10-28
related:
- theory/paradigms/meta-learning
- theory/optimization
- theory/paradigms/reinforcement-learning
tags:
- neuroscience
- learning
- neuromodulation
aliases:
  - 多巴胺之外的神經調節物質
  - 神經調節物質
  - Neuromodulation
  - Neuromodulators beyond dopamine
  - Acetylcholine
  - 乙醯膽鹼
  - Noradrenaline
  - Norepinephrine
  - 正腎上腺素
  - Serotonin
  - 血清素
  - ACh
  - NE
  - 5-HT
---

# Neuromodulators beyond Dopamine

Dopamine is the neuromodulator most often linked to AI, because its reward prediction error matches the learning signal of reinforcement learning. The brain has other neuromodulators. Acetylcholine, noradrenaline and serotonin each come from a small nucleus and project widely, and theories assign them roles in uncertainty, arousal and the speed of learning. These roles are a source of ideas for adaptive learning in AI.

This page covers those three systems. The dopamine signal is on [Dopamine Reward Prediction Error](../neuroscience/dopamine-reward-prediction-error/index.md), and the role of dopamine in choice is on [Decision Making, Dopamine & Reward](../decision-reward/index.md). The general idea of neuromodulation is introduced in [Neuroscience Basics](../neuroscience/index.md).

## Overview

A neurotransmitter such as glutamate carries a specific message from one neuron to the next. A neuromodulator is released diffusely and acts over longer periods, so it changes how strongly whole circuits respond and learn. It works less like a message and more like a setting.

This suggests a division of labour. Each system may report something about the state of the world, and the brain's learning then adjusts to that state. The main proposals are that acetylcholine signals expected uncertainty, noradrenaline signals sudden and unexpected change, serotonin sets how far ahead the brain looks, and arousal sets the balance between exploiting what is known and exploring.

## Key concepts

- **Neuromodulator**: a chemical that alters how neurons and circuits operate over a wide area.
- **Expected uncertainty**: uncertainty that is known to exist, for example because a cue is unreliable in a given context.
- **Unexpected uncertainty**: a sudden change that makes existing expectations unreliable.
- **Learning rate**: how much one new outcome changes an estimate. It is a meta-parameter of most learning algorithms, meaning a setting of the algorithm rather than a value learned from data.

## Key methods

- [Uncertainty-based neuromodulation (Yu & Dayan, 2005)](yu-dayan-2005/index.md): acetylcholine and noradrenaline signal two kinds of uncertainty, and both reduce reliance on top-down expectations.
- [Meta-learning with neuromodulation (Doya, 2002)](doya-2002/index.md): four neuromodulators correspond to the parts of a reinforcement-learning algorithm, one prediction error and three meta-parameters.

The two accounts differ in what they explain. Yu and Dayan ask how the brain should weigh its beliefs under uncertainty, and they link acetylcholine and noradrenaline mainly to attention. Doya asks how the learning algorithm's own settings are controlled, and he assigns each neuromodulator one component of it.

## Core ideas

**Uncertainty as a signal.** If a cue is known to be noisy, one surprising outcome should not change beliefs much. If the environment has just changed, beliefs should change quickly. Yu and Dayan argue that acetylcholine and noradrenaline encode these two cases.

**Arousal and the exploration trade-off.** The locus coeruleus, the main source of brain noradrenaline, is described as switching between a tonic mode that supports broad exploration and a phasic mode that supports focused exploitation (Aston-Jones & Cohen, 2005). In humans, pupil-linked arousal tracks the assessed instability of a noisy process and predicts how strongly new data change beliefs (Nassar et al., 2012).

**Neuromodulators as meta-parameters.** Doya (2002) maps dopamine onto the prediction error, serotonin onto the discount factor, noradrenaline onto the randomness of action selection, and acetylcholine onto the learning rate. The mapping is a hypothesis, but it gives each neuromodulator a precise computational job.

**The same idea in AI.** Adaptive optimisers such as Adam control the step size of each parameter from running estimates of the gradient (Kingma & Ba, 2015). Learned optimisers go further and learn the update rule itself. Andrychowicz et al. (2016) trained recurrent networks as optimisers that outperformed hand-designed ones on the tasks they were trained for.

## Connections

- **Reinforcement learning.** The learning rate, discount factor and softmax temperature are the meta-parameters that Doya relates to neuromodulators. See [Reinforcement Learning](../../theory/paradigms/reinforcement-learning/index.md) and its [exploration](../../theory/paradigms/reinforcement-learning/exploration/index.md) page.
- **Meta-learning.** Neuromodulation offers a biological view of learning to learn: the brain adjusts how it learns, not only what it has learned. See [Meta-Learning](../../theory/paradigms/meta-learning/index.md).
- **Predictive coding.** Both accounts treat uncertainty as a control on how much new evidence changes beliefs. See [Predictive Coding & Free Energy](../predictive-coding/index.md).
- **Attention.** Uncertainty signals shape attention. See [Attention in Brains & Machines](../attention-brain-machine/index.md).
- **Memory and model-based control.** Acetylcholine's proposed role in the speed of memory update connects to [Memory & Learning in the Brain](../memory-learning/index.md). Neuromodulators may also change how much an agent relies on a learned model, as covered on [Model-Based vs Model-Free Control](../decision-reward/model-based-vs-model-free/index.md).

## Applications

- **Adaptive learning rates in AI.** Adaptive optimisers such as [Adam](../../theory/optimization/adaptive/adam.md) perform the same functional job as Doya's acetylcholine mapping, although they are not neuromodulatory models.
- **Learning to learn.** Learned optimisers replace hand-designed update rules with trained ones, which is the engineering counterpart of the idea that learning rules can themselves be learned.
- **Human experiments.** Pupil diameter serves as a non-invasive readout of arousal and uncertainty in cognitive experiments, as in Nassar et al. (2012).

## Open questions

- **Which signal is which?** The split of acetylcholine and noradrenaline into expected and unexpected uncertainty has support, but the two signals overlap in many tasks.
- **Are the mappings causal?** Testing whether manipulating one neuromodulator changes exactly one parameter is hard, because the systems interact.
- **How do neuromodulators reach the learning rule?** The molecular and circuit routes that change learning rates are still being mapped.
- **Do artificial meta-learners resemble the brain?** The goal is shared, but it is unclear whether the brain implements anything like the learned update rules used in AI.

## References

### Seminal papers

- Yu, A. J. & Dayan, P. (2005). Uncertainty, Neuromodulation, and Attention. *Neuron*. https://doi.org/10.1016/j.neuron.2005.04.026 — Proposes that acetylcholine and noradrenaline signal expected and unexpected uncertainty. Covered on [Yu & Dayan 2005](yu-dayan-2005/index.md).
- Doya, K. (2002). Metalearning and neuromodulation. *Neural Networks*, 15(4–6), 495–506. https://doi.org/10.1016/s0893-6080(02)00044-8 — Proposes that four neuromodulators correspond to reinforcement-learning meta-parameters. Covered on [Doya 2002](doya-2002/index.md).
- Dayan, P. & Yu, A. J. (2006). Phasic norepinephrine: a neural interrupt signal for unexpected events. *Network: Computation in Neural Systems*, 17(4), 335–350. https://doi.org/10.1080/09548980601004024 — Proposes that phasic noradrenaline is a neural interrupt signal for unexpected events.
- Nassar, M. R., Rumsey, K. M., Wilson, R. C., Parikh, K., Heasly, B. & Gold, J. I. (2012). Rational regulation of learning dynamics by pupil-linked arousal systems. *Nature Neuroscience*, 15(7), 1040–1046. https://doi.org/10.1038/nn.3130 — Human experiments showing that pupil-linked arousal tracks assessed instability in a noisy process and predicts how strongly new data influence beliefs.
- Andrychowicz, M. et al. (2016). Learning to learn by gradient descent by gradient descent. *NeurIPS*. https://arxiv.org/abs/1606.04474 — Trains recurrent networks as optimisers that outperform hand-designed optimisers on the tasks they are trained on.
- Kingma, D. P. & Ba, J. (2015). Adam: A Method for Stochastic Optimization. *ICLR*. https://arxiv.org/abs/1412.6980 — Introduces Adam, which keeps running estimates of the first and second moments of the gradient.

### Surveys and textbooks

- Aston-Jones, G. & Cohen, J. D. (2005). An integrative theory of locus coeruleus-norepinephrine function: adaptive gain and optimal performance. *Annual Review of Neuroscience*. https://doi.org/10.1146/annurev.neuro.28.061604.135709 — Proposes that tonic noradrenaline activity supports exploration and phasic activity supports exploitation.
- Doya, K. (2008). Modulators of decision making. *Nature Neuroscience*, 11(4), 410–416. https://doi.org/10.1038/nn2077 — Review of neuromodulators and decision making.
- Hasselmo, M. E. (2006). The role of acetylcholine in learning and memory. *Current Opinion in Neurobiology*. https://doi.org/10.1016/j.conb.2006.09.002 — Reviews the evidence for acetylcholine's role in learning and memory.
- Sutton, R. S. & Barto, A. G. (2018). *Reinforcement Learning: An Introduction*, 2nd ed. MIT Press. http://incompleteideas.net/book/the-book-2nd.html — Standard introduction to reinforcement learning, the framework in which the discount factor, learning rate and softmax choice rule are used.
