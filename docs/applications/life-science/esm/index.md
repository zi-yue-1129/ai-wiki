---
status: draft
last_reviewed: 2026-10-28
aliases:
  - ESM-2
  - ESMFold
  - ESM Metagenomic Atlas
---

# ESM-2 and ESMFold (Lin et al., 2023)

ESM-2 is a transformer language model trained on protein sequences. ESMFold adds a structure head, so the same model predicts a protein's three-dimensional structure directly from its sequence. It is the sequence-based model in the [Life Sciences](../index.md) overview.

## Problem

Gene sequencing has revealed far more protein sequences than structures are known for, and predicting structure for them needs much faster methods. The preprint argues that inferring structure directly from the primary sequence, with a language model, could give an order-of-magnitude speed-up at high resolution.

## Core idea

A language model trained on millions of sequences learns evolutionary patterns. When the model is scaled up, the preprint reports, it encodes enough information to predict structure at atomic resolution. The largest model has up to 15 billion parameters.

## Equation or algorithm

ESM-2 is a [transformer](../../../theory/models/transformer/attention-is-all-you-need/index.md) encoder trained on protein sequences with a masked-token objective: parts of a sequence are hidden and predicted from their context (Lin et al., 2023). ESMFold reads the model's internal representations and outputs three-dimensional coordinates:

1. Encode the amino-acid sequence with the language model.
2. Predict the three-dimensional structure from the internal representations.
3. Apply the same procedure across a database to build a structure atlas.

## Results

From the preprint abstract:

- Structure prediction up to 60 times faster than the state of the art, "while maintaining resolution and accuracy".
- The ESM Metagenomic Atlas contains more than 617 million predicted structures. Over 225 million of them are high-confidence predictions, including millions with structures that are novel compared with experimentally determined ones.

## Limitations

- These results come from the preprint. The published Science version should be consulted for final numbers.
- Atlas entries are computational predictions. The abstract describes them as high-confidence predictions, not experimentally confirmed structures.
- The model learns from evolutionary patterns in sequences, so it may have less information for proteins with few known relatives (an inference, not a claim from the paper).

## Connections

- [RFdiffusion](../rfdiffusion/index.md): a design tool that builds on a structure predictor, RoseTTAFold, rather than on a language model.
- [Transformer](../../../theory/models/transformer/attention-is-all-you-need/index.md): the architecture behind ESM-2.

## References

### Seminal papers

- Lin et al. (2023). Evolutionary-scale prediction of atomic-level protein structure with a language model. *Science*. https://doi.org/10.1126/science.ade2574 — The published version, introducing ESM-2 and ESMFold.
- Lin et al. (2022). Evolutionary-scale prediction of atomic level protein structure with a language model. *bioRxiv*. https://doi.org/10.1101/2022.07.20.500902 — The preprint whose abstract the results section summarises.
- Rives et al. (2021). Biological structure and function emerge from scaling unsupervised learning to 250 million protein sequences. *PNAS*. https://doi.org/10.1073/pnas.2016239118 — The earlier ESM work, showing that structure-related information emerges from language-model training on sequences.
- Jumper et al. (2021). Highly accurate protein structure prediction with AlphaFold. *Nature*. https://doi.org/10.1038/s41586-021-03819-2 — AlphaFold 2, the reference structure predictor.
- Vaswani et al. (2017). Attention Is All You Need. arXiv. https://arxiv.org/abs/1706.03762 — The transformer architecture.
