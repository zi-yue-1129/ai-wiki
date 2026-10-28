---
status: draft
last_reviewed: 2026-10-28
aliases:
  - ESM-2
  - ESMFold
  - ESM Metagenomic Atlas
---

# ESM-2 and ESMFold (Lin et al., 2023)

ESM-2 and ESMFold are a protein language model and a structure predictor built on it. ESM-2 learns from protein sequences alone, and ESMFold adds a folding head that turns its representations into three-dimensional coordinates. They are the sequence-based models in the [Life Sciences](../index.md) overview, and each has its own page.

## Overview

Sequences of proteins are far easier to obtain than their structures. The ESM approach learns from the sequences themselves, with no structures used as training labels for the language model. ESMFold then predicts structure from one sequence, without the alignment step used by [AlphaFold 2](../alphafold-2.md).

## Key methods

Two methods make up this family. Each links to its own page.

- [ESM-2](esm-2.md): a transformer language model trained on protein sequences with a masked-token objective. It predicts no coordinates on its own.
- [ESMFold](esmfold.md): a structure predictor built on ESM-2. It takes one sequence and returns coordinates and confidences, and the preprint reports much faster inference than alignment-based predictors.

## Connections

- [AlphaFold 2](../alphafold-2.md): the alignment-based structure predictor that this family is usually compared with.
- [Transformer](../../../theory/models/transformer/attention-is-all-you-need/index.md): the architecture both models use.
- [RFdiffusion](../rfdiffusion/index.md): a design tool that builds on a structure predictor rather than a language model.

## Applications

The main large-scale use is the ESM Metagenomic Atlas, a database of predicted structures for proteins from metagenomic sequences. See [ESMFold](esmfold.md) for details.

## References

### Seminal papers

- Lin et al. (2023). Evolutionary-scale prediction of atomic-level protein structure with a language model. *Science*. https://doi.org/10.1126/science.ade2574 — The published version, introducing ESM-2 and ESMFold.
- Lin et al. (2022). Evolutionary-scale prediction of atomic level protein structure with a language model. *bioRxiv*. https://doi.org/10.1101/2022.07.20.500902 — The preprint whose abstract the figures summarise.
- Rives et al. (2021). Biological structure and function emerge from scaling unsupervised learning to 250 million protein sequences. *PNAS*. https://doi.org/10.1073/pnas.2016239118 — The earlier ESM work, showing that structure-related information emerges from language-model training on sequences.
- Jumper et al. (2021). Highly accurate protein structure prediction with AlphaFold. *Nature*. https://doi.org/10.1038/s41586-021-03819-2 — AlphaFold 2, the reference structure predictor.
- Vaswani et al. (2017). Attention Is All You Need. arXiv. https://arxiv.org/abs/1706.03762 — Introduces the transformer architecture that ESM-2 is built on.
