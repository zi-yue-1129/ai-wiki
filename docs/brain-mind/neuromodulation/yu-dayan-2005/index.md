---
status: draft
last_reviewed: 2026-10-28
related:
- theory/machine-learning/uncertainty-and-calibration
tags:
- neuroscience
- uncertainty
- attention
aliases:
  - Yu and Dayan 2005
  - Expected and unexpected uncertainty
  - 預期與非預期不確定性
  - 不確定性、神經調節與注意力
---

# Uncertainty, Neuromodulation and Attention (Yu and Dayan, 2005)

Yu and Dayan proposed that acetylcholine signals expected uncertainty, the known unreliability of cues, while noradrenaline signals unexpected uncertainty, a sudden change that breaks prior predictions. Both modulate how attention and learning are allocated. The paper is one of the three method accounts in [Neuromodulation Beyond Dopamine](../index.md).

## Overview

A learner rarely knows the world for certain. There are two different reasons for that. Sometimes the environment is noisy but stable: a cue predicts an outcome only some of the time, and the learner knows this from experience. The uncertainty is expected, and the right response is to rely on the cue's average reliability. At other times the environment changes: the cue that used to predict the outcome suddenly stops working. The uncertainty is unexpected, and the right response is to abandon old beliefs and learn faster.

Yu and Dayan argued that the brain tracks these two situations with different neuromodulators. The paper is theoretical. It combines a Bayesian model of learning under these uncertainties with neurophysiological evidence about the two systems, and it treats their effects on attention as a consequence of the same computation.

## Key concepts

- **Expected uncertainty**: uncertainty that is known to be present in a context, such as the usual unreliability of a cue. It is a property of the learned environment.
- **Unexpected uncertainty**: a surprising change in the environment that signals the learned model may no longer apply. It is evidence that the environment has moved, not that it is noisy.
- **Acetylcholine**: a neuromodulator released from the basal forebrain. In this account it signals expected uncertainty.
- **Noradrenaline**: a neuromodulator released from the locus coeruleus. In this account it signals unexpected uncertainty.
- **Attention as allocation**: the proposal that attention is the way the brain assigns weight to cues whose predictive value is uncertain or has recently changed.

## How it works

The account can be read as an algorithm in which learning and attention depend on two estimates. The first is how reliable each cue is in the current context. The second is how likely it is that the context itself has just changed. The paper frames this as Bayesian inference over the hidden state of the world. This page gives a simplified reading in our own notation, which is not the paper's equation:

1. Maintain an estimate of how strongly each cue predicts the outcome, together with the estimate's uncertainty.
2. Estimate the expected uncertainty from the known reliability of the cues in the current context.
3. Estimate the unexpected uncertainty from how surprising the most recent outcome was, in relation to the predictions.
4. Increase the learning rate for a cue when unexpected uncertainty is high, so that changed contingencies are picked up quickly.
5. Increase the attention given to a cue when either kind of uncertainty is high, so that informative cues are sampled more.

In this reading, expected uncertainty acts mainly on the weight given to cues, and unexpected uncertainty acts mainly on how fast beliefs are revised. The two signals therefore have different effects on learning, even though both affect attention.

## Results

The paper is a theoretical and modelling contribution. Its evidence comes from two sources: a review of physiological findings on acetylcholine and noradrenaline, and simulations of a Bayesian learning model in cue-based tasks. The paper argues that the model's behaviour is consistent with the qualitative patterns of attention and learning seen in those tasks. This page quotes no numbers from it, and readers should consult the paper's own figures for the details.

## Limitations

- **The distinction is clearer in models than in data.** Expected and unexpected uncertainty can change together in an experiment, so separating them from recordings is hard.
- **The model is simple.** The cue-based task used to illustrate the idea captures only part of real attention and learning.
- **The mapping to two neuromodulators is a hypothesis.** Other neuromodulators and cortical circuits may also represent uncertainty.
- **The account does not give a single mechanism for attention.** It describes what the neuromodulators do to the allocation of attention, but the attentional circuit itself is left open.

## Open questions

- **How are the two signals measured?** A clean test would manipulate expected and unexpected uncertainty separately and record both neuromodulatory systems at once.
- **How do the two systems interact?** Acetylcholine and noradrenaline are both active in many tasks, so their combined effect may be more than the sum of the two.
- **Does the account extend to continuous environments?** Most of the theory concerns discrete cues. Whether the same logic applies to smoothly changing signals is less clear.
- **How does this relate to memory?** Acetylcholine is also discussed as a regulator of encoding and retrieval. Hasselmo (2006) reviews those roles, and the link to the uncertainty account is not yet settled.

## References

### Seminal papers

- Yu, A. J. & Dayan, P. (2005). Uncertainty, neuromodulation, and attention. *Neuron*. https://doi.org/10.1016/j.neuron.2005.04.026 — The paper itself. It proposes that acetylcholine and noradrenaline signal expected and unexpected uncertainty and shape attention.
- Aston-Jones, G. & Cohen, J. D. (2005). An integrative theory of locus coeruleus-norepinephrine function: adaptive gain and optimal performance. *Annual Review of Neuroscience*. https://doi.org/10.1146/annurev.neuro.28.061604.135709 — Proposes the phasic and tonic modes of the locus coeruleus, which underlie the noradrenaline side of this account.
- Schweighofer, N. & Doya, K. (2003). Meta-learning in Reinforcement Learning. *Neural Networks*. https://doi.org/10.1016/S0893-6080(02)00228-9 — Studies how the learning meta-parameters of a reinforcement learner can be adapted during learning, a related computational view.

### Surveys and textbooks

- Hasselmo, M. E. (2006). The role of acetylcholine in learning and memory. *Current Opinion in Neurobiology*. https://doi.org/10.1016/j.conb.2006.09.002 — Reviews acetylcholine's proposed effects on encoding and retrieval in the hippocampus and cortex.
- Bouret, S. & Sara, S. J. (2005). Network reset: a simplified overarching theory of locus coeruleus noradrenaline function. *Trends in Neurosciences*. https://doi.org/10.1016/j.tins.2005.09.002 — Proposes that bursts of locus coeruleus activity reset cortical networks after salient events.
- Doya, K. (2008). Modulators of decision making. *Nature Neuroscience*. https://doi.org/10.1038/nn2077 — Reviews how neuromodulators shape decisions and relates them to reinforcement-learning parameters.
- Sara, S. J. (2009). The locus coeruleus and noradrenergic modulation of cognition. *Nature Reviews Neuroscience*. https://doi.org/10.1038/nrn2573 — Reviews how the locus coeruleus and noradrenaline influence attention, memory and cognitive control.
