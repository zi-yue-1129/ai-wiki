---
status: draft
last_reviewed: 2026-10-28
related:
- brain-mind/neuroscience
- brain-mind/neuroai
tags:
- neuroscience
- attention
aliases:
  - Desimone & Duncan 1995
  - Biased competition
  - Biased Competition Model
---

# Biased Competition (Desimone & Duncan 1995)

Desimone and Duncan (1995) proposed that stimuli in the same receptive field compete for representation in visual cortex, and that attention resolves the competition by biasing it toward the attended stimulus. The idea explains why responses to a pair of stimuli look like a weighted average when both are present, and how a top-down signal can change that average. It is a review that brings together neurophysiological evidence, and it became the standard account of attention in visual cortex.

This page is part of [Attention in Brains and Machines](../index.md). The parent page gives the overview; this page covers the method and its evidence.

## The problem

Neurons in extrastriate visual cortex have large receptive fields, so more than one object can fall inside them at once. When two stimuli are present, a neuron's response is not simply the sum of the responses to each alone. The question was how the brain decides which stimulus drives the response, and how attention changes that decision.

## The approach

The paper is a review of neurophysiological evidence rather than a single experiment. It collects recordings from visual areas in which a monkey attends to one of two stimuli, and it compares the responses with and without attention. It then proposes a single mechanism that accounts for the pattern across areas.

The steps of the proposed account are:

1. Stimuli within a receptive field compete for the neuron's limited response.
2. Without attention, the response to a pair of stimuli is pulled toward a combination of the two.
3. A top-down signal from higher areas biases the competition toward the stimulus that matches the current goal.
4. The biased response is passed on, so the attended stimulus is represented more strongly across the hierarchy.

Step 3 is what distinguishes attention from the bottom-up signal. The bias can be set by location, by a feature such as colour, or by a learned target.

## Results

The review reports that, when two stimuli are in a receptive field, the response to the pair is reduced relative to the attended stimulus alone, and that attention moves the response toward the attended stimulus. The effect is found across several visual areas. The paper summarises these findings qualitatively. Check the full text before quoting specific values.

## Limitations

- The account is a framework for the visual system and does not specify the circuit that implements the bias.
- Biased competition explains selection among stimuli in the receptive field. It says less about how attention is allocated across the visual field.
- The evidence comes mostly from primate visual cortex. Its generality to humans and to other sensory systems is a separate question.

## Connections

- **Saliency account**: the bottom-up route to selection, which works through feature contrast rather than top-down bias, is on [Itti, Koch and Niebur 1998](../saliency-map/index.md).
- **Attention models in machines**: the transformer attention weighting that resembles the top-down bias is on [Transformer](../../../theory/models/transformer/index.md).
- **Neuroscience background**: the receptive fields and cortical areas that compete are in [Neuroscience Basics](../../neuroscience/index.md).
- **Perception**: how attention changes responses along the ventral stream is on [Perception and the Visual System](../../visual-perception/index.md).

## Open questions

- **What sets the top-down bias?** The review names a source, but the mechanism that selects the goal signal and sends it to the right neurons is still under study.
- **Does competition happen early or late?** The timing of competition across areas is debated.

## References

### Seminal papers

- Desimone, R. & Duncan, J. (1995). Neural mechanisms of selective visual attention. *Annual Review of Neuroscience*. https://doi.org/10.1146/annurev.ne.18.030195.001205 — Proposes biased competition, in which top-down signals resolve competition between stimuli in the same receptive field.
- Itti, L., Koch, C. & Niebur, E. (1998). A model of saliency-based visual attention for rapid scene analysis. *IEEE Transactions on Pattern Analysis and Machine Intelligence*. https://doi.org/10.1109/34.730558 — The bottom-up counterpart to biased competition, based on feature contrast.
- Mnih, V., Heess, N., et al. (2014). Recurrent Models of Visual Attention. *NeurIPS*. https://arxiv.org/abs/1406.6247 — A learned, top-down glimpse-selection model, a machine version of goal-directed selection.

### Surveys and reviews

- Corbetta, M. & Shulman, G. L. (2002). Control of goal-directed and stimulus-driven attention in the brain. *Nature Reviews Neuroscience*. https://doi.org/10.1038/nrn755 — The dorsal and ventral attention networks that supply the top-down and bottom-up signals.

### Articles and primary research

- Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, Ł. & Polosukhin, I. (2017). Attention Is All You Need. *NeurIPS*. https://arxiv.org/abs/1706.03762 — The transformer attention weighting, the machine analogue of the top-down bias.
