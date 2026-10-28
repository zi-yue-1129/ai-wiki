---
status: draft
last_reviewed: 2026-10-28
related:
- brain-mind/neuroai
- theory/models/cnn
tags:
- neuroscience
- perception
aliases:
  - Yamins 2014
  - 效能最佳化的階層模型
  - Performance-optimised hierarchical models
---

# Performance-Optimised Networks Predict IT Cortex (Yamins et al. 2014)

Yamins et al. (2014) asked whether neural networks that are good at recognising objects also explain the responses of neurons in higher visual cortex. The answer they reported was yes, and that the match came from performance rather than from fitting the networks to neural data. The paper is a landmark of [NeuroAI](../../neuroai/index.md), and it set the pattern that later benchmark work followed.

This page is part of [Perception and the Visual System](../index.md). The parent page gives the overview; this page covers the method and its evidence.

## The problem

Object recognition in primates depends on the inferior temporal (IT) cortex, the highest area of the ventral visual stream. Its responses are hard to explain with simple models. A convolutional network trained for categorisation is one candidate, but a network that happens to categorise well might not share the brain's computations. The question was whether task performance alone selects the networks that match IT.

## The approach

The authors defined a large family of hierarchical convolutional networks that differed in depth, filter sizes and connectivity. They trained each network on an object-recognition task and scored its performance. Then they tested how well each model predicted neural responses.

The steps were:

1. Define a family of hierarchical networks, varying depth, filter sizes and connectivity.
2. Train each network on an object-recognition task and score its performance.
3. Select the networks with high recognition performance. The selected model matches human performance on several recognition tests.
4. Fit a linear regression from each model layer to recorded IT and V4 responses on held-out natural images, and measure how well the model predicts each recording site.

The key feature is that the selection step never uses neural data. Only the final regression does.

## Results

The abstract reports three findings:

- Within the family, categorisation performance was strongly correlated with how well a network predicted IT responses.
- The selected network, which matched human performance on several recognition tasks, predicted IT spiking responses to natural images at both single-site and population levels.
- Its intermediate layers predicted responses in V4, the area before IT.

The abstract gives no numerical correlation values or explained-variance figures, so this page does not quote any.

## Limitations

- The comparison uses a limited set of images and recorded sites. A good linear fit does not show that the model uses the same computation as the brain.
- Predictive success on held-out images does not establish that the model generalises to other stimuli, species or tasks.
- Later benchmark work compares many more models against neural data. Whether this predictive power transfers across stimuli and species remains an open question.

## Connections

- **Method family**: the same logic, selecting models by task performance and then testing them on neural data, underlies later vision benchmarks. See [CNN](../../../theory/models/cnn/index.md) for the architecture family.
- **Shape bias**: a related question about what these networks learn is covered in [Shape Bias in CNNs (Geirhos et al. 2019)](../geirhos-2019/index.md).
- **Neuroscience background**: the cortical hierarchy and receptive fields the paper relies on are in [Neuroscience Basics](../../neuroscience/index.md).

## Open questions

- **How far does the match extend?** The paper tested visual categories and a limited set of sites. Whether the match holds for other sensory systems and tasks is open.
- **Is performance the right selector?** Selecting by performance worked here, but other selection criteria might identify different models.

## References

### Seminal papers

- Yamins, D. L. K., Hong, H., Cadieu, C. F., Solomon, E. A., Seibert, D. & DiCarlo, J. J. (2014). Performance-optimized hierarchical models predict neural responses in higher visual cortex. *PNAS*. https://doi.org/10.1073/pnas.1403112111 — Shows that object-recognition performance predicts how well networks explain IT responses.
- Krizhevsky, A., Sutskever, I. & Hinton, G. E. (2012). ImageNet Classification with Deep Convolutional Neural Networks. *NeurIPS*. https://papers.nips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html — The AlexNet paper, the kind of network the 2014 study examined.
- Hubel, D. H. & Wiesel, T. N. (1962). Receptive fields, binocular interaction and functional architecture in the cat's visual cortex. *The Journal of Physiology*. https://doi.org/10.1113/jphysiol.1962.sp006837 — The receptive-field work behind the hierarchy the models imitate. (Reference reused from the Neuroscience Basics page; not re-checked for this page.)

### Surveys and reviews

- Lindsay, G. W. (2021). Convolutional Neural Networks as a Model of the Visual System: Past, Present, and Future. *Journal of Cognitive Neuroscience*. https://doi.org/10.1162/jocn_a_01544 — A review of how CNNs have been used as models of the visual system, and what they explain and miss.
- Kriegeskorte, N. (2015). Deep neural networks: a new framework for modelling biological vision and brain information processing. bioRxiv preprint. https://doi.org/10.1101/029876 — Argues for deep networks as candidate models of brain information processing, and discusses how such models should be evaluated.
