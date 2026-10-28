---
status: complete
last_reviewed: 2026-10-28
related:
- brain-mind/neuroscience
- brain-mind/neuroai
tags:
- neuroscience
- attention
- computer-vision
aliases:
  - Itti et al. 1998
  - Saliency map
  - Saliency-based visual attention
---

# Saliency-Based Visual Attention (Itti, Koch & Niebur 1998)

Itti, Koch and Niebur (1998) built a model of bottom-up attention that selects locations in a scene from feature contrast alone. Colour, intensity and orientation are computed at several scales, centre-surround differences highlight regions that stand out, and the results are combined into a single saliency map. A winner-take-all stage picks the most salient location, and inhibition of return prevents the model from getting stuck on it. The model became the reference implementation for saliency-based attention in computer vision.

This page is part of [Attention in Brains and Machines](../index.md). The parent page gives the overview; this page covers the method and its evidence.

## The problem

Human observers move their eyes to a few locations in a scene, and those locations are often not chance. Some regions attract attention because they differ from their surroundings, even when the observer is not searching for them. The question was whether a simple, bottom-up computation could predict where attention goes in a natural image.

## The approach

The model is a bottom-up pipeline of image operations, with no learning from eye-movement data. It takes an image, computes feature maps, and combines them into a map of salience. It then selects locations in order of salience, suppressing each one after it has been attended.

The steps were:

1. Decompose the image into colour, intensity and orientation channels at several spatial scales.
2. Compute centre-surround differences within each channel, so that regions that differ from their surroundings give strong responses.
3. Normalise and combine the feature maps into a single saliency map.
4. Select the most salient location with a winner-take-all stage, then apply inhibition of return so that attention moves on.

Step 4 is what turns a static map into a sequence of fixations. Without inhibition of return, the model would keep returning to the same location.

## Results

The paper reports that the model's selections on synthetic and natural images qualitatively follow the regions that stand out, and that the sequence of selections resembles the order in which people look at such scenes. These results are qualitative in the summary used for this page. Check the full paper before quoting figures.

## Limitations

- The model is bottom-up only. It has no task goals, so it cannot explain search for a specific target.
- Salience is not the same as relevance. A salient region may be irrelevant to what the observer is doing.
- The features are hand-designed and the model does not learn them from data.

## Connections

- **Top-down account**: the goal-driven counterpart, in which selection is biased by task demands, is on [Biased Competition](../biased-competition/index.md).
- **Visual features**: the orientation and colour channels relate to the receptive-field work on [Perception and the Visual System](../../visual-perception/index.md).
- **Neuroscience background**: the cortical areas that compute contrast are summarised in [Neuroscience Basics](../../neuroscience/index.md).

## Open questions

- **Does salience capture human attention in complex scenes?** Simple feature models predict some fixations but not all, and the gap is studied with more detailed scene models.
- **How should bottom-up and top-down signals be combined?** The model keeps them separate, and a combined account is still an open problem.

## References

### Seminal papers

- Itti, L., Koch, C. & Niebur, E. (1998). A model of saliency-based visual attention for rapid scene analysis. *IEEE Transactions on Pattern Analysis and Machine Intelligence*. https://doi.org/10.1109/34.730558 — A saliency-map model of bottom-up attention built from centre-surround feature contrasts.
- Desimone, R. & Duncan, J. (1995). Neural mechanisms of selective visual attention. *Annual Review of Neuroscience*. https://doi.org/10.1146/annurev.ne.18.030195.001205 — The top-down biased-competition account that the saliency model complements.
- Mnih, V., Heess, N., Graves, A. & Kavukcuoglu, K. (2014). Recurrent Models of Visual Attention. *NeurIPS*. https://arxiv.org/abs/1406.6247 — A learned glimpse-selection model, a machine version of goal-directed selection.
- Bahdanau, D., Cho, K. & Bengio, Y. (2014). Neural Machine Translation by Jointly Learning to Align and Translate. arXiv preprint. https://arxiv.org/abs/1409.0473 — Introduces learned alignment, an early form of attention in neural networks.

### Surveys and reviews

- Corbetta, M. & Shulman, G. L. (2002). Control of goal-directed and stimulus-driven attention in the brain. *Nature Reviews Neuroscience*. https://doi.org/10.1038/nrn755 — The ventral network for stimulus-driven attention, which the saliency account models.
