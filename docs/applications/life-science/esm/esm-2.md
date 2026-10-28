---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/transformer
aliases:
  - ESM-2
  - ESM2
  - 蛋白質語言模型
---

# ESM-2 (Lin et al., 2023)

ESM-2 is a transformer language model trained only on protein sequences. Its internal representations carry information about protein structure, which is why the same model can be extended to predict structure. It is the sequence model behind [ESMFold](esmfold.md), and the family overview is on the [ESM-2 and ESMFold](index.md) page.

## Overview

A protein is a chain of amino acids, and its sequence is far easier to obtain than its three-dimensional structure. ESM-2 applies the language-modelling approach to these sequences: it learns statistical patterns across the sequences of many proteins, the way a language model learns from text.

## Problem

Sequencing has revealed far more protein sequences than structures are known for. A model that could extract structural information from sequence alone would be much faster than experimental methods, and would not need the sequence databases that alignment-based predictors search.

## Key concepts

- **Protein language model**: a model trained on amino-acid sequences, where each residue plays the role of a word.
- **Masked language modelling**: parts of a sequence are hidden, and the model predicts them from the rest. Earlier ESM models were trained this way (Rives et al., 2021).
- **Embedding**: the vector the model produces for each residue. Downstream models read these vectors.
- **Scale**: the preprint trains models from 8 million up to 15 billion parameters.

## Core idea

A language model trained on many sequences learns evolutionary patterns. The preprint reports that, as the model is scaled up, its representations contain enough information to predict structure at atomic resolution. The structure predictor built on top of it is [ESMFold](esmfold.md).

## Algorithm

Training follows the masked-token objective:

1. Sample a protein sequence from the training data.
2. Hide a fraction of its residues.
3. Predict the hidden residues from the surrounding sequence, using a transformer encoder whose self-attention lets every residue attend to every other.
4. Update the parameters to reduce the prediction error on the hidden residues.

The training loss is the cross-entropy over the hidden positions \(M\):

```latex
\mathcal{L} = -\sum_{i \in M} \log p_\theta(x_i \mid x_{\setminus M})
```

## Results

The preprint reports that scaling the model up gives representations good enough to predict structure at atomic resolution. The figures for each model size are in the paper and are not restated here. The published version in *Science* should be used for final numbers.

## Limitations

- The results described here come from the preprint. The *Science* version supersedes its figures.
- The model learns from patterns in sequence databases. Proteins with few known relatives probably give less information to work from (an inference, not a claim from the paper).
- Good embeddings do not by themselves give a reliable three-dimensional shape. Structure is produced by the head on top, and that head has its own limits (see [ESMFold](esmfold.md)).

## Connections

- [ESMFold](esmfold.md): the structure predictor built on this model.
- [Transformer](../../../theory/models/transformer/attention-is-all-you-need/index.md): the architecture ESM-2 uses, with self-attention over residues instead of words.
- [AlphaFold 2](../alphafold-2.md): the alignment-based structure predictor that the family is usually compared with.
- Brain and mind: no direct connection. The model learns from sequence statistics and does not model neural activity.

## Applications

- **Structure prediction**: the ESM Metagenomic Atlas, built with ESMFold on top of ESM-2, is the main large-scale use (see [ESMFold](esmfold.md)).
- **Protein representations**: earlier ESM work reported that simple models trained on these representations can predict structural contacts and other protein properties (Rives et al., 2021).

## Open questions

- How much of the learned structure is general, and how much comes from close relatives in the training data.
- Whether further scaling keeps improving the results, and at what compute cost.

## References

### Seminal papers

- Lin et al. (2023). Evolutionary-scale prediction of atomic-level protein structure with a language model. *Science*. https://doi.org/10.1126/science.ade2574 — The published version, introducing ESM-2 and ESMFold.
- Lin et al. (2022). Evolutionary-scale prediction of atomic level protein structure with a language model. *bioRxiv*. https://doi.org/10.1101/2022.07.20.500902 — The preprint behind the figures summarised on this page.
- Rives et al. (2021). Biological structure and function emerge from scaling unsupervised learning to 250 million protein sequences. *PNAS*. https://doi.org/10.1073/pnas.2016239118 — The earlier ESM work, which showed that structure-related information emerges from language-model training on sequences.
- Jumper et al. (2021). Highly accurate protein structure prediction with AlphaFold. *Nature*. https://doi.org/10.1038/s41586-021-03819-2 — AlphaFold 2, the alignment-based structure predictor used for comparison.
- Vaswani et al. (2017). Attention Is All You Need. arXiv. https://arxiv.org/abs/1706.03762 — Introduces the transformer architecture that ESM-2 is built on.
