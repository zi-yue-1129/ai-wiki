---
status: draft
last_reviewed: 2026-10-28
aliases:
  - RFdiffusion
  - RoseTTAFold Diffusion
---

# RFdiffusion (Watson et al., 2023)

RFdiffusion designs new protein backbones with a diffusion model. It is built by fine-tuning the RoseTTAFold structure-prediction network to denoise protein structures, which lets it generate proteins from simple specifications. It is the design tool in the [Life Sciences](../index.md) overview.

## Overview

Most computational structure tools predict the shape of an existing sequence. Design runs the other way: the goal is a new backbone, and then a sequence that folds into it. Diffusion models had succeeded for images and language, but for proteins the same success had been harder to reach, partly because backbone geometry and the link between sequence and structure are complex (Watson et al., 2022).

## Problem

Deep-learning design methods existed before RFdiffusion, but the preprint argues that a single generative framework covering binder design, symmetric assemblies and enzyme scaffolding had not been described. It asks whether a diffusion model built on a structure-prediction network could handle all of these tasks.

## Key concepts

- **Backbone**: the chain of protein backbone atoms, the skeleton of the fold. RFdiffusion generates this skeleton.
- **Denoising**: a learned reverse process that turns random coordinates into a plausible structure in many small steps.
- **Conditioning**: a specification, such as a target fold, a binding surface or a symmetry, that steers generation.
- **Symmetric oligomer**: several identical chains arranged with a point-group symmetry, such as a trimer or an icosahedral shell.

## Core idea

Start from a random set of backbone coordinates and denoise it step by step into a plausible backbone, in the way image diffusion models turn noise into pictures. The denoiser is RoseTTAFold, a network trained to predict protein structures, so it already encodes protein geometry. The preprint fine-tunes it as a generative model with minimal architectural changes, and conditioning on a design specification steers the result toward a chosen shape or function.

## Algorithm

RFdiffusion follows the [denoising diffusion](../../../theory/paradigms/unsupervised/density-and-generative-models/diffusion/ddpm.md) framework (Ho et al., 2020). A forward process adds noise to real structures, and a learned reverse process removes it. Generation runs the reverse process from noise, conditioned on the design task:

1. Sample a random backbone.
2. Denoise it over many steps with the fine-tuned RoseTTAFold network, conditioned on the task.
3. Select designs for experimental testing. The preprint selected 608 designs for characterisation.

## Results

The results below come from the 2022 preprint. The published 2023 *Nature* version should be consulted for final figures.

- **Benchmark**: on a 25-problem benchmark, the preprint reports that RFdiffusion solved 23 problems, against 15 for Hallucination and 12 for RFjoint inpainting.
- **Tasks**: the preprint reports unconditional and topology-constrained monomer design, protein binder design conditioned on interface residues, symmetric oligomers with chosen point-group symmetry, enzyme active-site scaffolding and symmetric motif scaffolding.
- **Experiments**: 608 designs were selected for experimental characterisation. In one set of tested designs, the preprint reports that 55 of 95 showed some detectable binding at 10 μM.

## Limitations

- The model proposes designs, and experiments decide which ones work. Design quality is not guaranteed.
- Success rates vary by task. Among the symmetric icosahedral designs the preprint validated, only one was confirmed by negative-stain electron microscopy to form the intended assembly.
- The design model is built on RoseTTAFold, so its strengths and gaps in structure prediction carry over (an inference, not a claim from the paper).
- The results are for designs in silico and in a laboratory. Whether a designed protein works in a cell or a body is a further question.

## Connections

- [ESM-2 and ESMFold](../esm/index.md): sequence-based protein language models that predict structure from a single sequence. They are prediction tools, where RFdiffusion is a design tool.
- [Denoising diffusion](../../../theory/paradigms/unsupervised/density-and-generative-models/diffusion/ddpm.md): the general framework the method builds on.
- [AlphaFold 2](../alphafold-2.md): the structure predictor whose line of work RoseTTAFold belongs to.
- Brain and mind: no direct connection. The method works on protein geometry, not on neural data.

## Applications

- **Binder design**: generating proteins that bind a chosen target surface, for research tools and therapeutic candidates.
- **Enzyme scaffolding**: placing an enzyme's active site on a new backbone.
- **Symmetric assemblies**: designing self-assembling cages and rings from identical subunits.

## Open questions

- How often designs that look good in silico work after experimental testing, and how that rate changes with the task.
- Whether generating large, complex assemblies with many chains can be done reliably.
- How to add sequence design and function to the backbone generation in one step.

## References

### Seminal papers

- Watson et al. (2023). De novo design of protein structure and function with RFdiffusion. *Nature*. https://doi.org/10.1038/s41586-023-06415-8 — The published RFdiffusion paper, which introduces the method.
- Watson et al. (2022). Broadly applicable and accurate protein design by integrating structure prediction networks and diffusion generative models. *bioRxiv*. https://doi.org/10.1101/2022.12.09.519842 — The preprint whose benchmark and experimental figures are summarised above.
- Baek et al. (2021). Accurate prediction of protein structures and interactions using a three-track neural network. *Science*. https://doi.org/10.1126/science.abj8754 — RoseTTAFold, the structure-prediction network that RFdiffusion fine-tunes.
- Jumper et al. (2021). Highly accurate protein structure prediction with AlphaFold. *Nature*. https://doi.org/10.1038/s41586-021-03819-2 — AlphaFold 2, the structure predictor that RoseTTAFold is usually compared with.
- Ho et al. (2020). Denoising Diffusion Probabilistic Models. arXiv. https://arxiv.org/abs/2006.11239 — The diffusion framework the method builds on.
