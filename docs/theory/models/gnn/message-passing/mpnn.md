---
related:
  - theory/models/gnn
  - theory/models/gnn/message-passing
  - theory/models/gnn/message-passing/gcn
tags:
  - graph neural networks
  - message passing
  - quantum chemistry
aliases:
  - MPNN
  - Message passing neural networks
  - Neural message passing for quantum chemistry
  - 訊息傳遞神經網路
last_reviewed: 2026-11-01
---

# MPNN: Neural Message Passing for Quantum Chemistry

A message-passing neural network (MPNN) is a graph model written as three learned functions: a message function, a vertex update and a readout. Gilmer et al. (2017) proposed this framework and applied it to predicting properties of small molecules. The paper shows that several earlier graph models fit the same template, and it tests the template on the QM9 benchmark. The general family is described on the [Message Passing](index.md) page. This page covers the framework itself and the molecular results.

## Overview

Most graph models of 2017 used a fixed neighbourhood operation, such as a normalised average or a gated update. Gilmer et al. asked whether one general description could cover all of them, and whether the choice of message and update functions could be tuned for a particular task. The answer is a single template with learned parts, and a set of experiments that compare the choices.

## Problem

The paper asks how to build a network that respects the symmetries of a molecule and predicts its quantum-mechanical properties. The benchmark is QM9, about 134,000 small organic molecules with 13 targets each. Every target approximates a result from density functional theory (DFT), which is accurate but expensive to compute. The paper measures success against the error of DFT, and against chemical accuracy, the error level it uses as the target for each property.

## Core idea

Each node \(v\) holds a hidden state \(h_v\), and each edge \(vw\) carries a feature vector \(e_{vw}\). For \(T\) steps, every node collects messages from its neighbours, and then updates its own state. After the last step, a readout function maps the set of node states to one prediction. The readout must not depend on the order of the nodes.

## Algorithm

The forward pass is

\[
m_v^{t+1} = \sum_{w \in \mathcal{N}(v)} M_t\big(h_v^t, h_w^t, e_{vw}\big), \qquad h_v^{t+1} = U_t\big(h_v^t, m_v^{t+1}\big), \qquad \hat y = R\big(\{h_v^T : v \in G\}\big)
\]

where \(M_t\) is the message function, \(U_t\) the vertex update and \(R\) the readout. Section 5 of the paper compares several choices.

- **Matrix multiplication**, as in gated graph neural networks (GG-NN): the message is a matrix for each edge type times the neighbour's state.
- **Edge network**: a small network maps the edge feature vector to a matrix \(A(e_{vw})\), and the message is \(A(e_{vw})\,h_w\). This is the best-performing message function in the paper.
- **Pair message**: a function of both endpoints and the edge, \(f(h_w, h_v, e_{vw})\).
- **Readouts**: the GG-NN readout, and Set2Set (Vinyals et al., 2015), which uses attention over the node set and is order-invariant.

## Results

Table 2 reports the error ratio for each target, which is the mean absolute error divided by the chemical accuracy target. A value below 1 means the model reached chemical accuracy on that target. The table below shows part of the paper's Table 2. Full results include the other baselines.

| Target | Chemical accuracy | GG-NN | enn-s2s | enn-s2s-ens5 |
|---|---|---|---|---|
| mu | 0.1 | 1.22 | 0.30 | 0.20 |
| alpha | 0.1 | 1.55 | 0.92 | 0.68 |
| HOMO | 0.043 | 1.17 | 0.99 | 0.74 |
| gap | 0.043 | 1.70 | 1.60 | 1.23 |
| U0 | 0.043 | 0.83 | 0.45 | 0.33 |
| ZPVE | 0.0012 | 2.52 | 1.27 | 1.10 |
| Omega | 10.0 | 0.53 | 0.19 | 0.15 |
| **Average** | | 1.36 | 0.68 | 0.52 |

Here enn-s2s is the single edge-network model with Set2Set readout, and enn-s2s-ens5 is an ensemble of five. The single model is within chemical accuracy on 11 of 13 targets, failing on gap and ZPVE. The ensemble is within chemical accuracy on the same 11 targets. The paper's other baselines have average error ratios of 1.35 for HDAD and 2.59 for graph convolution (GC).

The paper also tests models that do not use spatial information. With partial charges as input, the Set2Set model has an average error ratio of 2.57 and reaches chemical accuracy on 5 of 13 targets. The authors note that partial charges are themselves DFT outputs, so this setting is not available in a practical application.

## Limitations

- **Larger molecules.** The authors say that future work "should focus on datasets with larger molecules or more accurate ground truth labels." With spatial information, the distribution of pairwise distances shifts as the molecule grows, and the fully connected graph grows with the number of atoms.
- **Generalisation to larger graphs.** Section 9 names this as an important direction. The authors suggest attention over incoming messages as one possibility.
- **Towers.** Splitting the hidden state into towers did not combine well with the edge network in the paper's experiments. The authors say the towers variant "will be needed to scale to much larger graphs."
- **Label source.** The chemical accuracy is measured against DFT-derived labels, not experimental measurements.

## Connections

- The template covers the normalised convolution of [GCN](gcn/index.md), the attention of [GAT](gat/index.md), the sum aggregation of [GIN](gin/index.md) and the sampling of [GraphSAGE](graphsage/index.md).
- The family-level view of the template and its expressivity limits is on the [Message Passing](index.md) page, and the wider model family is on the [Graph Neural Networks](../index.md) page.
- Spatial models for molecules such as SchNet (Schütt et al., 2017) use continuous-filter convolutions on the same kind of data, and are a natural comparison.

## Open issues

- How should messages be formed when atoms are far apart, without the cost of a fully connected graph?
- Does the edge-network message generalise from QM9 to larger molecules and to other properties?
- How much of the accuracy comes from the readout, and how much from the message function?

## References

### Seminal papers

- Gilmer, J., Schoenholz, S. S., Riley, P. F., Vinyals, O. & Dahl, G. E. (2017). Neural Message Passing for Quantum Chemistry. ICML, PMLR 70, pp. 1263–1272. [arXiv:1704.01212](https://arxiv.org/abs/1704.01212) — Defines the message, update and readout framework and reports results on QM9.
- Li, Y., Tarlow, D., Brockschmidt, M. & Zemel, R. (2015). Gated Graph Sequence Neural Networks. [arXiv:1511.05493](https://arxiv.org/abs/1511.05493) — The GG-NN model, whose matrix-multiplication message is one of the variants the paper compares.
- Kipf, T. N. & Welling, M. (2016). Semi-Supervised Classification with Graph Convolutional Networks. [arXiv:1609.02907](https://arxiv.org/abs/1609.02907) — The normalised neighbour averaging that the framework generalises.
- Vinyals, O., Bengio, S. & Kudlur, M. (2015). Order Matters: Sequence to Sequence for Sets. [arXiv:1511.06391](https://arxiv.org/abs/1511.06391) — Introduces Set2Set, the order-invariant readout used in the best model.
- Schütt, K. T. et al. (2017). SchNet: A Continuous-filter Convolutional Neural Network for Modeling Quantum Interactions. [arXiv:1706.08566](https://arxiv.org/abs/1706.08566) — A spatial model for molecules, which the paper's spatial-information experiments relate to.

### Surveys and textbooks

(none checked for this page)

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Ramakrishnan, R. et al. (2014). Quantum Chemistry Structures and Properties of 134 Kilo Molecules. Scientific Data, 1. [DOI 10.1038/sdata.2014.22](https://doi.org/10.1038/sdata.2014.22) — The QM9 dataset with its 13 targets, used as the benchmark in the paper.
