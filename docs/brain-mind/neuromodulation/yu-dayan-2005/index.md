---
status: draft
last_reviewed: 2026-10-28
related:
- brain-mind/attention-brain-machine
tags:
- neuroscience
- attention
- uncertainty
aliases:
  - Yu & Dayan 2005
  - Uncertainty, neuromodulation, and attention
  - 基於不確定性的神經調節
  - Expected and unexpected uncertainty
  - 預期不確定性與非預期不確定性
---

# Uncertainty-based neuromodulation (Yu & Dayan, 2005)

Yu and Dayan propose that two neuromodulators answer two different questions about uncertainty. Acetylcholine signals that a predictive cue is known to be unreliable. Noradrenaline signals that the environment has changed in a way that makes old expectations invalid. Both reduce how much the brain relies on top-down expectations.

This page is part of [Neuromodulators beyond Dopamine](../index.md), which compares this account with the others in the chapter.

## Overview

Imagine a light that usually predicts a reward but is wrong one time in five. Learning what that light means should be slow and careful. Now suppose the rules change without warning. The light that was reliable a moment ago now means nothing, and the brain should update quickly. Both cases involve uncertainty, but they call for opposite responses. Yu and Dayan argue that the brain separates them and assigns each to a neuromodulator.

## Key concepts

- **Cue validity**: how reliably a cue predicts the outcome it is linked to.
- **Expected uncertainty**: uncertainty from known noise in the cue-outcome relationship within a context.
- **Unexpected uncertainty**: uncertainty from a change of context that the agent did not anticipate.
- **Top-down expectation**: a prediction that guides perception, as opposed to bottom-up sensory input.

## Problem

Acetylcholine and noradrenaline both affect attention and learning, and their effects are hard to separate in experiments. Without a model, cholinergic and noradrenergic effects look like a general change in arousal. The question is what computational variable each one reports.

## Core idea

The authors treat perception as Bayesian inference: the brain combines prior expectations with sensory evidence to estimate what is happening. Two kinds of uncertainty need different responses. Expected uncertainty is the residual uncertainty when a cue is known to be imperfect within a context, and the paper proposes that acetylcholine signals it. Unexpected uncertainty arises when the environment changes in a way the current model does not anticipate. The paper proposes that noradrenaline signals it, and that noradrenaline boosts learning after a change.

Both signals reduce the weight given to top-down expectations relative to bottom-up input. The two also interact. Acetylcholine sets the threshold at which noradrenaline-driven detection of a context change is triggered, which is an antagonistic interaction. The two also cooperate in predicting the next target on each trial.

## Equation or algorithm

The paper builds a probabilistic model of cue validity and context change. This page does not reproduce its equations. In general terms, the agent keeps a belief about whether a cue is valid and whether the context has changed, and each new observation updates that belief. High expected uncertainty widens the belief about a noisy cue, so one outcome moves it only a little. High unexpected uncertainty signals a probable change, so new outcomes count for more.

## Results

The paper does not present a new large dataset. It compares its model with existing experiments, mainly cueing tasks and maze learning.

- In cueing tasks, the validity effect, the advantage of valid over invalid cues, changes with cholinergic manipulation. The model reproduces this as a change in expected uncertainty.
- In maze learning, boosting noradrenaline speeds the detection of a cue shift. The model links this to unexpected uncertainty.
- In simulated tracking runs, the model's acetylcholine and noradrenaline signals follow the true cue validity and context changes.

The paper also proposes an extended cueing task in which both cue identity and cue validity change, as a test of the theory.

## Limitations

- **Qualitative comparison.** The model is compared with pharmacological results from a few tasks, and the agreement is qualitative.
- **Model constructs.** Expected and unexpected uncertainty cannot be recorded directly, so each signal's link to its neuromodulator is inferred from behaviour and drugs.
- **Scope of the claim.** The authors warn that the results do not mean more noradrenaline makes animals learn faster in general. The claim concerns learning after a change in context.
- **Later measurements.** Pupil-linked arousal studies (Nassar et al., 2012) support a role for noradrenaline in updating beliefs, but they measure a proxy and do not separate expected from unexpected uncertainty in the same way.

## Connections

- **Predictive coding.** Uncertainty weighting of prediction errors is central to [Predictive Coding & Free Energy](../../predictive-coding/index.md). This account describes one way neuromodulators could set that weighting.
- **Attention.** The paper treats uncertainty as a driver of attention. See [Attention in Brains & Machines](../../attention-brain-machine/index.md).
- **Doya's account.** [Meta-learning with neuromodulation (Doya, 2002)](../doya-2002/index.md) assigns acetylcholine to the learning rate and noradrenaline to action randomness. The two accounts make different assignments and are best read together.
- **Exploration.** Uncertainty-driven exploration is covered on the [exploration](../../../theory/paradigms/reinforcement-learning/exploration/index.md) page of the reinforcement-learning chapter.

## Applications

- **Pupil-based readouts.** Human studies use pupil size to measure arousal and the variables that drive learning rate. Nassar et al. (2012) is an example that links the arousal account to behaviour.
- **Uncertainty-aware learning in AI.** Methods that increase learning after a detected change, or that scale updates by estimated uncertainty, share the functional logic of the model. They are engineering choices, not implementations of the paper's account.

## Open questions

- **Are the two signals separable?** The model assumes that acetylcholine and noradrenaline carry different uncertainty signals, and experiments that manipulate both have given mixed results.
- **How is unexpected uncertainty detected?** The model assumes a change-detection process that signals noradrenaline, and the circuit that performs this detection is not yet mapped.
- **Does the model generalise?** Most tests use cueing and maze tasks, so its reach into richer, natural environments is unclear.

## References

### Seminal papers

- Yu, A. J. & Dayan, P. (2005). Uncertainty, Neuromodulation, and Attention. *Neuron*, 46(4), 681–692. https://doi.org/10.1016/j.neuron.2005.04.026 — The original paper. Proposes acetylcholine as a signal of expected uncertainty and noradrenaline as a signal of unexpected uncertainty, and models their effects on attention and learning.
- Dayan, P. & Yu, A. J. (2006). Phasic norepinephrine: a neural interrupt signal for unexpected events. *Network: Computation in Neural Systems*, 17(4). https://doi.org/10.1080/09548980601004024 — Develops the noradrenaline part of the account, treating phasic noradrenaline as an interrupt signal for unexpected events.
- Nassar, M. R., Rumsey, K. M., Wilson, R. C., Parikh, K., Heasly, B. & Gold, J. I. (2012). Rational regulation of learning dynamics by pupil-linked arousal systems. *Nature Neuroscience*. https://doi.org/10.1038/nn.3130 — Human experiments showing that pupil measures track change-point probability and predict learning rate.

### Surveys and reviews

- Aston-Jones, G. & Cohen, J. D. (2005). An integrative theory of locus coeruleus-norepinephrine function: adaptive gain and optimal performance. *Annual Review of Neuroscience*. https://doi.org/10.1146/annurev.neuro.28.061604.135709 — Reviews the noradrenaline system the model relies on, with its tonic and phasic modes.
- Hasselmo, M. E. (2006). The role of acetylcholine in learning and memory. *Current Opinion in Neurobiology*. https://doi.org/10.1016/j.conb.2006.09.002 — Reviews acetylcholine's role in learning and memory, relevant to the acetylcholine part of the account.
