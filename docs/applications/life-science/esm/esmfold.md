---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/transformer
aliases:
  - ESMFold
  - ESM Metagenomic Atlas
  - 單序列結構預測
---

# ESMFold (Lin et al., 2023)

ESMFold predicts a protein's three-dimensional structure from a single amino-acid sequence. It adds a folding head to [ESM-2](esm-2.md), so the language model's representations feed directly into a structure predictor. It needs no alignment of related sequences, which makes it the fast, sequence-only option in the [Life Sciences](../index.md) overview.

## Overview

Structure predictors such as [AlphaFold 2](../alphafold-2.md) search sequence databases to build a multiple sequence alignment before they predict. That search takes time and fails when a protein has few relatives. ESMFold takes one sequence as input and returns coordinates and confidence scores in one pass.

## Key concepts

- **Single-sequence prediction**: the input is one sequence, with no alignment.
- **Folding block**: a block that alternates between updating a sequence representation and a pairwise representation of residues.
- **Recycling**: the output is fed back into the blocks. The preprint uses three recycling steps.
- **Confidence**: the model outputs a predicted confidence for the structure along with the coordinates.
- **Atlas**: a database of predicted structures, built by running the model over a large set of sequences.

## Algorithm

1. Encode the sequence with [ESM-2](esm-2.md), which gives a representation for each residue.
2. Pass the representations through a stack of folding blocks. Each block updates the sequence representation and the pairwise representation.
3. Pass the output to an equivariant transformer structure module, which produces atomic coordinates.
4. Repeat the trunk and structure steps for three recycling steps, then output the structure and its predicted confidences.

The authors train the folding head with the same losses used for AlphaFold, so the training objective follows the AlphaFold line of work while the input and architecture differ.

## Results

- **Speed**: the preprint reports inference up to 60 times faster than the state of the art on the forward pass alone, with the claim that resolution and accuracy are maintained.
- **Atlas**: the authors fold more than 617 million sequences from the MGnify90 database. About 225 million of the predictions are high confidence.
- Accuracy numbers on benchmark test sets are reported in the paper and are not restated here.

## Limitations

- The speed and accuracy figures come from the preprint. The published *Science* version should be checked for the final numbers.
- Atlas entries are computational predictions. High confidence means the model is confident, not that the structure has been confirmed experimentally.
- Accuracy depends on how much the language model has learned about the protein. Proteins with few relatives in the training data are the hardest case (an inference, not a claim from the paper).

## Connections

- [ESM-2](esm-2.md): the language model that ESMFold is built on.
- [AlphaFold 2](../alphafold-2.md): the alignment-based predictor. ESMFold's authors describe their method as a simplification of current structure predictors, and it shares AlphaFold's training losses.
- [RFdiffusion](../rfdiffusion/index.md): a design tool that uses a structure predictor, RoseTTAFold, rather than a language model.
- Brain and mind: no direct connection. The method works on sequences and structures, not on neural data.

## Applications

- **Metagenomic structure atlas**: ESMFold made it possible to predict structures for many proteins from environmental sequences that have no experimental structures.
- **Rapid screening**: a fast single-sequence predictor suits settings where many sequences need a first structural estimate before a slower method or an experiment.

## Open questions

- How accurate single-sequence prediction is for proteins with few relatives, and for complexes of several chains.
- How to judge which atlas predictions are reliable enough for experimental follow-up.

## References

### Seminal papers

- Lin et al. (2023). Evolutionary-scale prediction of atomic-level protein structure with a language model. *Science*. https://doi.org/10.1126/science.ade2574 — The published version, introducing ESMFold and the ESM Metagenomic Atlas.
- Lin et al. (2022). Evolutionary-scale prediction of atomic level protein structure with a language model. *bioRxiv*. https://doi.org/10.1101/2022.07.20.500902 — The preprint behind the speed and atlas figures summarised on this page.
- Jumper et al. (2021). Highly accurate protein structure prediction with AlphaFold. *Nature*. https://doi.org/10.1038/s41586-021-03819-2 — AlphaFold 2, the alignment-based predictor ESMFold is compared with.
- Rives et al. (2021). Biological structure and function emerge from scaling unsupervised learning to 250 million protein sequences. *PNAS*. https://doi.org/10.1073/pnas.2016239118 — The earlier ESM work on language models trained on protein sequences.
- Vaswani et al. (2017). Attention Is All You Need. arXiv. https://arxiv.org/abs/1706.03762 — Introduces the transformer architecture behind the language model.
