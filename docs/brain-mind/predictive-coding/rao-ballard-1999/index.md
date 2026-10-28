---
status: complete
last_reviewed: 2026-10-28
related:
- brain-mind/neuroai
- brain-mind/visual-perception
tags:
- neuroscience
- learning
aliases:
  - Rao & Ballard 1999
  - Predictive coding in visual cortex
  - Extra-classical receptive-field effects
---

# Predictive Coding in Visual Cortex (Rao & Ballard 1999)

Rao and Ballard (1999) proposed that feedback connections from higher visual areas carry predictions of lower-level activity, and that feedforward connections carry the residual errors. In their hierarchical network, trained on natural image patches, the feature detectors resembled simple cells, and the error-carrying units showed extra-classical receptive-field effects such as endstopping. The paper gave the first explicit computational account of why cortical responses depend on context outside the classical receptive field.

This page is part of [Predictive Coding and the Free-Energy Principle](../index.md). The parent page gives the overview; this page covers the method and its evidence.

## The problem

Neurons in primary visual cortex respond to a small region of the visual field, their classical receptive field. Their responses are also modulated by stimuli outside that region, and this modulation is called an extra-classical effect. The question was what these effects are for, and why the feedback connections that carry them exist.

## The approach

The authors built a hierarchical network in which each level holds an estimate of its input and sends a prediction to the level below. The prediction error at each level, the difference between that level's input and its prediction, is passed upward. The network learns its weights from natural image patches, so that the predictions reduce the error over time.

The steps were:

1. Build a hierarchical network where each level holds an estimate of the input and sends a prediction to the level below.
2. Compute the residual error at each level, the difference between the level's input and its prediction.
3. Send the errors upward, and update each level's estimate so that its prediction reduces the error.
4. Train the connection weights on natural image patches, so that the network learns a set of features.

The key assumption is that the error units and the prediction units are separate populations, so that the model makes a testable claim about which neurons should show which effects.

## Results

The abstract reports that the trained network developed simple-cell-like receptive fields, and that a subset of the error-carrying units showed endstopping and other extra-classical effects. These results are qualitative. The abstract does not give a numerical measure of fit to recorded neurons, so this page does not quote one.

## Limitations

- The model is a proof of principle. It is not a fit to recorded neurons, and the match to particular response properties is qualitative.
- The paper attributes the surround effects to cortico-cortical feedback. Testing that claim needed later experiments.
- The network uses a linear generative model and simple update rules, which simplify the cortex considerably.

## Connections

- **Learning rule**: a later account that approximates backpropagation with local plasticity in a predictive coding network is on [Whittington and Bogacz 2017](../whittington-bogacz-2017/index.md).
- **Review**: the case that predictive processing is a repeated cortical computation, by Keller and Mrsic-Flogel (2018), is cited on the [parent page](../index.md).
- **Visual hierarchy**: the ventral stream and receptive-field background this model builds on is on [Perception and the Visual System](../../visual-perception/index.md).
- **NeuroAI**: using predictive objectives and networks as models of cortex is covered on [NeuroAI](../../neuroai/index.md).

## Open questions

- **Are the error and prediction units separate populations?** The model assumes this, and the evidence for distinct cell types is still being gathered.
- **How much of the surround effect comes from feedback?** Feedback and local circuit mechanisms are both candidates, and separating them needs targeted experiments.

## References

### Seminal papers

- Rao, R. P. N. & Ballard, D. H. (1999). Predictive coding in the visual cortex: a functional interpretation of some extra-classical receptive-field effects. *Nature Neuroscience*. https://pubmed.ncbi.nlm.nih.gov/10195184/ — Proposes that feedback carries predictions and feedforward connections carry errors, and that a hierarchical network trained on natural images reproduces several surround effects.
- Whittington, J. C. R. & Bogacz, R. (2017). An Approximation of the Error Backpropagation Algorithm in a Predictive Coding Network with Local Hebbian Synaptic Plasticity. *Neural Computation*. https://pmc.ncbi.nlm.nih.gov/articles/PMC5467749/ — Shows that predictive coding with local plasticity can approximate backpropagation under suitable parameters.
- Hubel, D. H. & Wiesel, T. N. (1962). Receptive fields, binocular interaction and functional architecture in the cat's visual cortex. *The Journal of Physiology*. https://pubmed.ncbi.nlm.nih.gov/14449617/ — The receptive-field work that defines the classical receptive field the paper builds on.

### Surveys and reviews

- Keller, G. B. & Mrsic-Flogel, T. D. (2018). Predictive Processing: A Canonical Cortical Computation. *Neuron*. https://pmc.ncbi.nlm.nih.gov/articles/PMC6400266 — A review arguing that predictive processing is a repeated circuit-level computation across cortex, and discussing how it could be tested.
- Friston, K. (2010). The free-energy principle: a unified brain theory? *Nature Reviews Neuroscience*. https://pubmed.ncbi.nlm.nih.gov/20068583/ — Proposes that brains minimise prediction error, a unifying framework for perception, action and learning.
