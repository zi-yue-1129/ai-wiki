---
status: complete
last_reviewed: 2026-10-28
---

# Sparse coding (Olshausen & Field, 1996)

Natural image patches can be written as sparse combinations of learned basis functions, and when the basis is learned from natural images, its functions resemble the receptive fields of simple cells in primary visual cortex.

## Overview

Neurons in the primary visual cortex (V1) of mammals respond to edges of a particular orientation at a particular place in the visual field. Olshausen and Field (1996) asked whether this structure follows from a simple efficiency principle: represent natural images using as few active units as possible. Their learning algorithm, applied to small patches of natural scenes, produced filters that look like V1 simple-cell receptive fields.

Sparse coding is therefore a normative account of early vision, meaning that it explains what the system should compute rather than how each neuron is wired. It belongs to the family of efficient-coding theories, and the same objective has since been used as a feature learner in machine learning.

## Key concepts

- **Basis function**: a pattern, such as a small localised wave, that can be added with other patterns to build an image patch.
- **Coefficient**: the amount by which each basis function contributes to a given patch. The coefficients change from one image to the next.
- **Sparseness**: the property that only a few coefficients are non-zero for any input. It is enforced with a penalty function $S$.
- **Overcomplete code**: a code with more basis functions than input dimensions. The 1997 follow-up paper focuses on this case.
- **Receptive field**: the region of the stimulus, and the pattern within it, to which a neuron responds.
- **Efficient coding**: representing sensory input so that the code is compact or its outputs are statistically independent.

## Problem

Why do neurons in V1 respond to oriented, localised edges at particular positions? The question concerns the statistics of natural images. Earlier attempts to train unsupervised learning algorithms on natural images had not produced a complete set of basis functions with all three properties of V1 simple cells: localised, oriented and bandpass.

## Core idea

A patch of an image is modelled as a weighted sum of basis functions, with each coefficient $a_i$ multiplying a basis function $\phi_i$. The basis functions are learned from unlabelled natural images. For each patch, the coefficients are chosen to balance two goals: reconstruct the patch accurately, and keep as few coefficients active as possible. The second goal is what the paper calls maximising sparseness, and it is the step that produces the localised, oriented filters.

## Equation or algorithm

The image model is

$$I(x, y) = \sum_i a_i\, \phi_i(x, y)$$

For each patch, the coefficients are chosen to minimise the energy

$$E = \frac{1}{2} \sum_{x,y} \Big( I(x, y) - \sum_i a_i\, \phi_i(x, y) \Big)^2 + \lambda \sum_i S\!\left(\frac{a_i}{\sigma}\right)$$

Here $\lambda$ sets the weight of the sparseness term, $\sigma$ is a scaling constant, and $S$ is a penalty that is large for big coefficients. The paper's main simulation uses $S(x) = \log(1 + x^2)$. The energy follows the paper's form, which adds a reconstruction term and a sparseness term; it is written here as a cost to minimise. The first term is the reconstruction error and the second is the sparseness cost.

The learning procedure alternates between two steps:

1. Take a 16 × 16 pixel patch from a natural image.
2. With the current basis fixed, adjust the coefficients $a_i$ so that the energy decreases. The paper gives the coefficients dynamics in which they change over time under this energy.
3. Adjust the basis functions $\phi_i$ so that the energy, averaged over many patches, decreases. Repeat over many patches until the basis stabilises.

## Results

With 16 × 16 pixel patches and a set of 192 basis functions, the vast majority of learned functions are well localised within their array. They are oriented and tuned to different spatial scales, and the abstract describes the whole set as a complete family of localised, oriented, bandpass receptive fields. The paper reports that the functions have an average spatial-frequency bandwidth of about 1.1 octaves and an average length-to-width aspect ratio of about 1.3. The authors also note that the learned code is more efficient for later processing because its outputs are more statistically independent.

## Limitations

The 1996 model is a linear generative model: it describes an image as a sum of basis functions and does not model complex cells, temporal dynamics or top-down influence. The sparseness penalty $S$ is chosen by the authors, not derived from neurons. The comparison with V1 is qualitative, based on the shape of the filters rather than on fitted neural responses. Sparse coding is one normative account among several, not a complete model of V1.

The 1997 follow-up paper goes further. It argues that an overcomplete basis, with more functions than input dimensions, makes the input-output mapping depart from linearity, which may explain the weak non-linearities seen in cortical simple cells. That extension is outside the 1996 model.

## Key methods

A brief comparison of the approaches most often set beside sparse coding:

- **Principal component analysis (PCA)**: finds decorrelated components that minimise squared reconstruction error, without a sparseness constraint. The 1996 paper uses PCA as a comparison for its own learned basis.
- **Independent component analysis (ICA)**: learns a basis whose outputs are statistically independent, and it also learns filters from natural images. The difference from sparse coding lies in the objective, not in the data.
- **Sparse coding** (this page): a linear generative model with a sparseness penalty, which yields localised, oriented filters.
- **Sparse autoencoders**: neural-network versions that add a sparsity penalty to the hidden units. They apply the same idea within a learned encoder and decoder.

## Connections

- Parent topic: [Computational Neuroscience](../index.md)
- Companion method: [Hodgkin–Huxley Model](../hodgkin-huxley/index.md) describes the electrical behaviour of a single neuron. Sparse coding describes what a population of neurons should represent, so the two sit at different levels of description.
- [Receptive Fields (Hubel & Wiesel)](../../neuroscience/receptive-fields-hubel-wiesel/index.md) covers the receptive-field measurements that sparse coding is meant to explain.
- [Visual Perception](../../visual-perception/index.md) gives the wider background on how the visual system processes images.
- [Predictive Coding](../../predictive-coding/index.md) offers another normative account of early vision, based on prediction error rather than sparseness.
- Machine-learning side: [Unsupervised Learning](../../../theory/paradigms/unsupervised/index.md) covers learning features from unlabelled data.

## Applications

- **Models of V1.** The learned basis functions serve as a quantitative model of simple-cell receptive fields. The 1997 paper outlines further model predictions and possible experimental tests.
- **Feature learning.** The same objective, reconstructing inputs from a few active units, appears in sparse dictionary learning and sparse autoencoders, which learn features from unlabelled images and other data.
- **Testing efficient-coding ideas.** Because the model is simple and fully specified, it is a standard test case for asking whether a principle, here sparseness, really explains a cortical property.

## Open questions

- Do real simple cells implement this objective, or do they only resemble its output?
- How do overcomplete and non-linear codes fit recordings from cortex, and how much of the non-linearity do they account for?
- How can complex cells, temporal structure and feedback be added to the model without losing its clarity?
- How could a neuron implement the sparseness penalty and the learning rule with local signals?

## References

### Seminal papers

- Hubel, D. H. & Wiesel, T. N. (1962). Receptive fields, binocular interaction and functional architecture in the cat's visual cortex. *The Journal of Physiology*. https://doi.org/10.1113/jphysiol.1962.sp006837 — The original study of receptive fields in cat visual cortex, the empirical background that sparse-coding models try to explain.
- Olshausen, B. A. & Field, D. J. (1996). Emergence of simple-cell receptive field properties by learning a sparse code for natural images. *Nature*. https://doi.org/10.1038/381607a0 — Shows that a sparse code learned from natural images yields localised, oriented, bandpass filters like V1 simple-cell receptive fields.
- Olshausen, B. A. & Field, D. J. (1997). Sparse coding with an overcomplete basis set: A strategy employed by V1? *Vision Research*. https://doi.org/10.1016/S0042-6989(97)00169-7 — Extends the account to overcomplete codes, and discusses how they may explain the weak non-linearities of cortical simple cells.

### Surveys and textbooks

- Richards, B. A. et al. (2019). A deep learning framework for neuroscience. *Nature Neuroscience*. https://doi.org/10.1038/s41593-019-0520-2 — Argues for studying the brain through objective functions, learning rules and architectures, the framework in which sparse coding sits.
- Gerstner, W., Kistler, W. M., Naud, R. & Paninski, L. (2014). *Neuronal Dynamics*. Cambridge University Press. https://doi.org/10.1017/CBO9781107447615 — Textbook of neuron and network models, with a free online version at https://neuronaldynamics.epfl.ch/. Covers the neural modelling background for readers who want the biophysical side.
