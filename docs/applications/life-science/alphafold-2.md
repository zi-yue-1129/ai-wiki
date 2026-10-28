---
status: complete
last_reviewed: 2026-10-28
related:
  - theory/models/transformer
tags:
  - protein structure
aliases:
  - AlphaFold2
  - AF2
  - 蛋白質結構預測
---

# AlphaFold 2 (Jumper et al., 2021)

AlphaFold 2 is a neural network that predicts the three-dimensional structure of a protein from its amino-acid sequence. In the 2020 CASP14 assessment its predictions were competitive with experimental structures in most cases, which made it the reference point for the protein structure work in [Life Sciences & Drug Discovery](index.md).

## Overview

A protein is a chain of amino acids that folds into a specific shape, and the shape largely determines what the protein does. Determining that shape by experiment takes months to years for a single protein. The 2021 paper notes that experimental work has determined the structures of around 100,000 unique proteins, a small fraction of the billions of known protein sequences.

## Problem

Predicting a protein's structure from its sequence alone, the structure prediction part of the protein folding problem, had been an open research problem for more than 50 years. Earlier methods fell well short of atomic accuracy, especially when no homologous structure was available to copy from.

## Core idea

AlphaFold 2 is, in the paper's words, "the first computational method that can regularly predict protein structures with atomic accuracy even in cases in which no similar structure is known." The paper describes a neural network that uses multiple sequence alignments as input and incorporates physical and biological knowledge about protein structure into its design.

## Key concepts

- **Multiple sequence alignment (MSA)**: a set of evolutionarily related sequences lined up position by position. The paper names MSAs as a core input.
- **Template**: the structure of a known protein related to the target. The released model_1 configuration can use up to four.
- **Pair representation**: a table holding the network's estimate of the relationship between every pair of residues. It is updated alongside the MSA representation.
- **Recycling**: the network's output is fed back in as input and processed again. The released model_1 configuration runs three recycling iterations.
- **pLDDT**: a per-residue confidence score from 0 to 100. The released code computes it as a probability-weighted average of bin centres, multiplied by 100, and labels scores as disordered (0–50), low (50–70), medium (70–90) or high (90–100).

## Algorithm

The released implementation runs these steps for model_1:

1. **Build inputs.** Assemble an MSA for the input sequence from sequence databases, and optionally gather templates from known structures. Turn them into the MSA and pair representations.
2. **Evoformer stack.** Pass the representations through 48 Evoformer blocks. Each block updates both representations. Row-wise attention over the MSA is biased by the pair representation, so evolutionary information and residue-pair information inform each other.
3. **Structure module.** Eight layers turn the final representations into 3D atom positions.
4. **Recycle.** The predicted positions and representations feed back into steps 2 and 3. The model_1 configuration sets three recycling iterations.
5. **Score.** A predicted-LDDT head outputs a pLDDT score for each residue.

## Results

At CASP14, the blind structure prediction assessment, the paper reports "accuracy competitive with experimental structures in a majority of cases and greatly outperforming other methods." Per-target scores are in the paper's results section and are not restated here.

The AlphaFold Protein Structure Database, built on AlphaFold v2.0, first contained more than 360,000 predicted structures across 21 model-organism proteomes. Its authors planned to cover most of more than 100 million representative sequences.

## Limitations

- **Single chains first.** The main model was built for single chains. The released code ships separate AlphaFold-Multimer weights for complexes, and AlphaFold 3 later extended the approach to complexes with nucleic acids, small molecules and ions.
- **Confidence is part of the output.** Residues with low pLDDT, such as those in the disordered bands, should not be read as a fixed shape.
- **Training cutoff.** The original training data ended on 2018-04-30. The v2.3.0 technical note moves the cutoff to 2021-09-30 for the newer weights, so structures added after the cutoff were not part of the original training.

## Connections

- **Attention**: the Evoformer uses attention, the same mechanism as the [transformer](../../theory/models/transformer/index.md) in language models. Its attention runs over residues and sequence positions rather than words.
- **Brain and mind**: no direct connection. The method works from evolutionary sequence data and does not model neural activity.
- **Drug discovery**: for how structure predictions are used in drug discovery, see the [Life Sciences](index.md) page.

## Applications

- **Structural biology**: the public AlphaFold Protein Structure Database gives researchers predicted structures for whole proteomes, with per-residue and pairwise confidence estimates.
- **Regulatory context**: the US FDA's January 2025 draft guidance on AI to support regulatory decisions for drugs and biological products covers AI that generates information for decisions about a drug's safety, effectiveness or quality. It proposes a risk-based framework for judging whether a model is credible for a specific context of use. The FDA page limits the guidance to regulatory decision-making and does not mention AI used in drug discovery research. A structure prediction used only in early research therefore sits outside its stated scope. A prediction used to support a regulatory decision falls within it.

## Open questions

- **Complexes and ligands**: AlphaFold 3 extends the approach to complexes that include nucleic acids, small molecules, ions and modified residues. How far accuracy carries over to these cases remains an active question.
- **Beyond one shape**: a predicted structure is a single conformation. How to represent the range of shapes a protein takes is still open.

## References

### Seminal papers

- Jumper, J. et al., *Highly accurate protein structure prediction with AlphaFold*, Nature 596, 583–589 (2021). https://doi.org/10.1038/s41586-021-03819-2 — The AlphaFold 2 paper: the problem, the CASP14 validation and the method.
- Senior, A. W. et al., *Improved protein structure prediction using potentials from deep learning*, Nature 577, 706–710 (2020). https://doi.org/10.1038/s41586-019-1923-7 — The earlier AlphaFold system, which predicted structure from deep-learning potentials.

### Surveys and textbooks

- Abramson, J. et al., *Accurate structure prediction of biomolecular interactions with AlphaFold 3*, Nature 630, 493–500 (2024). https://doi.org/10.1038/s41586-024-07487-w — The successor model, which extends the approach to complexes with nucleic acids, small molecules and ions.

### Articles and documentation

- Varadi, M. et al., *AlphaFold Protein Structure Database: massively expanding the structural coverage of protein-sequence space with high-accuracy models*, Nucleic Acids Research 50, D439–D444 (2022). https://doi.org/10.1093/nar/gkab1061 — The public database built on AlphaFold v2.0, with its first release and planned expansion.
- Google DeepMind, *AlphaFold* source code, `alphafold/model/config.py`, `alphafold/model/modules.py` and `alphafold/common/confidence.py`. https://github.com/google-deepmind/alphafold — The released implementation. The model_1 configuration sets the Evoformer depth, the structure module depth and the recycling count, and the confidence module defines pLDDT.
- Google DeepMind, *AlphaFold v2.3.0 technical note*. https://github.com/google-deepmind/alphafold/blob/main/docs/technical_note_v2.3.0.md — Release notes for the newer weights, including the training cutoff and the AlphaFold-Multimer models.
- US Food and Drug Administration, *Considerations for the Use of Artificial Intelligence to Support Regulatory Decision-Making for Drug and Biological Products*, draft guidance (January 2025). https://www.fda.gov/regulatory-information/search-fda-guidance-documents/considerations-use-artificial-intelligence-support-regulatory-decision-making-drug-and-biological — The scope of the draft guidance and its risk-based credibility framework.

## Further learning

- [AlphaFold Protein Structure Database](https://alphafold.ebi.ac.uk/) — Search and download predicted structures, with per-residue confidence for each one.
