---
status: draft
last_reviewed: 2026-10-28
tags:
  - deep learning
  - supervised learning
aliases:
  - 感知器
  - 感知機
  - Perceptron
  - 明斯基與派普特批判
  - Minsky–Papert critique
  - Perceptrons
---

# Perceptron and the Minsky–Papert Critique

The perceptron is a network of trainable threshold units that Frank Rosenblatt introduced in 1958 as a model of learning in the brain. In 1969 Marvin Minsky and Seymour Papert analysed what a single layer of such units cannot compute, and their analysis is often read as ending neural-network research for about a decade. It is the main neural landmark of the [symbolic era](../index.md).

## Overview

Rosenblatt's perceptron learned from examples. Given a pattern and its label, it produced an output and, if the output was wrong, adjusted its numerical weights. Rosenblatt presented it as a theory of brain organisation, at a time when most AI research used symbols and rules.

The critique came from within AI, from leading symbolic researchers, and showed that a single-layer perceptron has fixed limits. Later historians have argued that the reception of the book, and the long decline of neural research that followed, reflected the growing institutional strength of symbolic AI as much as the mathematics (Olazaran, 1996).

## Key concepts

- **Threshold unit**: a unit that computes a weighted sum of its inputs plus a bias and outputs 1 if the sum is positive, and 0 otherwise.
- **Linear separability**: two sets of points are linearly separable if a straight line (or hyperplane) puts one set on one side and the other on the other. A single threshold unit classifies only such sets.
- **Error-correction learning**: the weights change only when the unit is wrong, in the direction that reduces the error on the current example.
- **Single layer**: a network with no hidden layer, the architecture the critique analysed.

## How it works

For inputs $\mathbf{x}$, weights $\mathbf{w}$ and bias $b$, the unit output is

$$
\hat{y} = \mathbf{1}\left[\mathbf{w}^\top \mathbf{x} + b > 0\right].
$$

Training follows a simple loop over labelled examples $(\mathbf{x}, y)$ with $y \in \{0, 1\}$:

1. Start with weights and bias set to zero or to small values.
2. For each example, compute $\hat{y}$ with the current weights.
3. If $\hat{y} \neq y$, update $\mathbf{w} \leftarrow \mathbf{w} + \eta\,(y - \hat{y})\,\mathbf{x}$ and $b \leftarrow b + \eta\,(y - \hat{y})$, where $\eta$ is a learning rate.
4. Repeat passes over the data until no example is misclassified or a maximum number of passes is reached.

The perceptron convergence theorem, a standard result for linear classifiers, says that if the data are linearly separable this procedure makes only finitely many mistakes and ends with a separating line. If the data are not separable, it never settles.

The Minsky–Papert argument concerns what the model can represent at all. The exclusive-or function, which outputs 1 when exactly one of two inputs is 1, is not linearly separable, so no single-layer unit computes it, and adding units to the same layer does not help. Solving such problems needs a hidden layer and a way to train it.

## Results

Rosenblatt's 1958 paper reports experiments in which the network learned to classify simple visual patterns from examples rather than from hand-written rules. The evidence is qualitative.

Minsky and Papert's evidence is mathematical. They prove limits on what single-layer perceptrons can compute, with exclusive-or as the simplest example. Block's 1962 review had earlier analysed the perceptron for a physics audience, including its learning behaviour and limits.

## Limitations

- **Linear limits.** A single layer separates only linearly separable classes, a precise limit that more training cannot remove.
- **No practical rule for hidden layers.** No widely used rule for training hidden units existed in the 1960s, so the limit could not be overcome in practice.
- **Over-reading.** The critique is often summarised as proof that neural networks cannot work. The mathematics concerns one architecture (Olazaran, 1996).

## Open questions

- Why was a limit on one architecture read as a limit on the whole approach? The historical debate is still active.
- How much did the single-layer result delay learning rules for multi-layer networks? Rumelhart, Hinton and Williams's 1986 paper on backpropagation is usually taken as the turning point.
- Does error-correction learning describe any part of how the brain learns?

## Connections

The perceptron builds on McCulloch and Pitts's 1943 model of neurons as threshold logic units, and it is the ancestor of the multi-layer [neural networks](../../../../theory/deep-learning/index.md) now in standard use. For the biological side, see [receptive fields](../../../../brain-mind/neuroscience/receptive-fields-hubel-wiesel/index.md) and [NeuroAI](../../../../brain-mind/neuroai/index.md).

## References

### Seminal papers

- Rosenblatt, F. (1958). The perceptron: A probabilistic model for information storage and organization in the brain. *Psychological Review*. https://doi.org/10.1037/h0042519 — Introduces the perceptron, a trainable network of threshold units proposed as a model of how the brain stores and organises information.
- McCulloch, W. S. & Pitts, W. (1943). A logical calculus of the ideas immanent in nervous activity. *The Bulletin of Mathematical Biophysics*. https://doi.org/10.1007/BF02478259 — Models neurons as threshold logic units, the model that the perceptron builds on.
- Minsky, M. & Papert, S. (2017). *Perceptrons*. MIT Press. https://doi.org/10.7551/mitpress/11301.001.0001 — Reissue of the 1988 expanded edition of the 1969 analysis of what perceptrons can compute, the source of the critique discussed here.
- Rumelhart, D. E., Hinton, G. E. & Williams, R. J. (1986). Learning representations by back-propagating errors. *Nature*. https://doi.org/10.1038/323533a0 — Describes training networks with hidden layers by propagating errors backwards, the method that answered the single-layer limitation.

### Surveys and textbooks

- Block, H. D. (1962). The perceptron: A model for brain functioning. I. *Reviews of Modern Physics*. https://doi.org/10.1103/RevModPhys.34.123 — Reviews the perceptron as a model of brain function for a physics audience and analyses its learning behaviour and limits.

### Articles and documentation

- Olazaran, M. (1996). A sociological study of the official history of the perceptrons controversy. *Social Studies of Science*. https://doi.org/10.1177/030631296026003005 — Examines how the 1969 critique came to be read as the end of neural-network research, and argues that institutional factors shaped that reading.
