---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/nlp
  - theory/models/speech
tags:
  - sequence modelling
  - supervised learning
  - uncertainty
aliases:
  - 條件隨機場
  - CRF
  - Conditional random field
  - Linear-chain CRF
---

# Conditional Random Field

A conditional random field (CRF) is an undirected graphical model that defines the probability of a label sequence given an observed input. It was a leading method for labelling sequences in natural language processing before neural networks took over, and it is one of the methods covered in [Probabilistic Graphical Models](../index.md).

## Overview

Sequence labelling assigns a label to each position in an input, as in part-of-speech tagging, shallow parsing and named-entity recognition. A [hidden Markov model](../hidden-markov-model/index.md) solves this by modelling how labels produce words, which is a generative task. A CRF models the labels directly given the words. The inputs are conditioned on, not generated, so the model can use overlapping and non-independent features of the input, such as capitalisation, suffixes and neighbouring words, without modelling their distribution.

Sha and Pereira (2003) showed that a CRF trained on the CoNLL-2000 chunking data matched the best reported results of the time. In the linear-chain case the dependency structure is the same as an HMM's, but the training objective is discriminative.

## Key concepts

- **Linear-chain CRF**: an undirected chain over the label sequence \(y_1,\dots,y_T\), with each label connected to the input \(x\) and to its neighbours.
- **Feature function** \(f_k(y_{t-1}, y_t, x, t)\): a real-valued function of adjacent labels, the input and the position. Features can overlap and depend on the whole input.
- **Weight** \(\lambda_k\): the learned importance of a feature.
- **Partition function** \(Z(x)\): the sum over all label sequences, computed with the forward algorithm.

## How it works

The conditional distribution of a label sequence is

\[
p(y \mid x) = \frac{1}{Z(x)}\exp\Big(\sum_{t}\sum_{k}\lambda_k\, f_k(y_{t-1}, y_t, x, t)\Big),
\]

where \(Z(x)\) is the same expression summed over all label sequences \(y'\). Training maximises the conditional log-likelihood of the labelled data. The gradient for each weight is the difference between the feature count observed in the data and its expectation under the model:

\[
\frac{\partial \ell}{\partial \lambda_k} = \sum_{i}\sum_{t} f_k\big(y^{(i)}_{t-1}, y^{(i)}_t, x^{(i)}, t\big) - \sum_{i}\mathbb{E}_{p(y\mid x^{(i)})}\Big[\sum_{t} f_k(y_{t-1}, y_t, x^{(i)}, t)\Big].
\]

The expectation is computed with forward and backward passes over the chain, which is the same cost as one HMM pass. The procedure is:

1. Define the feature functions from the input and label sets.
2. Run forward and backward passes to compute \(Z(x)\) and the expected feature counts.
3. Update the weights with a gradient-based optimiser, usually L-BFGS or conjugate gradient.
4. For prediction, use the Viterbi algorithm to find the most probable label sequence.

## Results

Sha and Pereira (2003) evaluate on noun-phrase chunking in the CoNLL-2000 shared task, with a feature set of about 3.8 million features. Their CRF reaches an F score of 94.38%. This is close to the SVM combination of Kudo and Matsumoto (94.39%) and above a maximum-entropy Markov model (93.70%).[^1] The difference between the CRF and the SVM is not statistically significant under their test, and the difference between the CRF and the MEMM is. On a smaller feature set, L-BFGS reached the target training objective in 84 minutes, against 130 minutes for preconditioned conjugate gradient.

Later neural systems keep the CRF layer. Ma and Hovy (2016) combine a character-level CNN, a bidirectional LSTM and a CRF, and report 97.55% accuracy on Penn Treebank part-of-speech tagging and 91.21 F1 on CoNLL 2003 named-entity recognition. Huang et al. (2015) report accuracy that is state of the art or close to it on part-of-speech, chunking and named-entity data, using past and future inputs.

## Limitations

- **Local structure.** The linear chain models dependencies only between neighbouring labels. Longer-range label dependencies need more complex graphs, which make inference harder.
- **Feature engineering.** Classic CRFs depend on large, hand-designed feature sets. The shallow-parsing system used about 3.8 million features.
- **Training cost.** Each gradient step needs forward and backward passes over every training sequence.
- **No input model.** A CRF cannot say how likely an input is, so it cannot generate data or flag unusual inputs.

## Open questions

- Does a CRF layer still add value on top of large pretrained encoders, or does the encoder learn the label dependencies on its own?
- How far can label structure be extended beyond chains, for example to trees or graphs, without making inference intractable?

[^1]: The F scores are those in Table 2 of Sha and Pereira (2003), and the significance tests are those in their Table 4.

## References

### Seminal papers

- Sha, F. & Pereira, F. (2003). Shallow Parsing with Conditional Random Fields. *NAACL-HLT*. https://aclanthology.org/N03-1028/ — Shows that a CRF matches the best reported noun-phrase chunking results on the CoNLL-2000 task, and that it is more accurate than an MEMM.

### Surveys and textbooks

- Sutton, C. & McCallum, A. (2010). *An Introduction to Conditional Random Fields*. arXiv. https://arxiv.org/abs/1011.4088 — Tutorial on CRFs for structured prediction, including inference and parameter estimation, written for readers without a background in graphical models.

### Articles and documentation

- Ma, X. & Hovy, E. (2016). *End-to-end Sequence Labeling via Bi-directional LSTM-CNNs-CRF*. arXiv. https://arxiv.org/abs/1603.01354 — Combines character and word representations, a bidirectional LSTM and a CRF layer, with results on part-of-speech tagging and named-entity recognition.
- Huang, Z., Xu, W. & Yu, K. (2015). *Bidirectional LSTM-CRF Models for Sequence Tagging*. arXiv. https://arxiv.org/abs/1508.01991 — Compares LSTM, bidirectional LSTM and CRF-output models for sequence tagging, and finds that the bidirectional LSTM-CRF depends less on word embeddings.
- Collins, M. (2002). Discriminative Training Methods for Hidden Markov Models: Theory and Experiments with Perceptron Algorithms. *EMNLP 2002*. https://aclanthology.org/W02-1001/ — A discriminative alternative to maximum-entropy and CRF training for tagging, with experiments on tagging and chunking.
