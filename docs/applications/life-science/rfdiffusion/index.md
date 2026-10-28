---
status: draft
last_reviewed: 2026-10-28
aliases:
  - RFdiffusion
  - RoseTTAFold Diffusion
---

# RFdiffusion (Watson et al., 2023)

RFdiffusion designs new protein backbones with a diffusion model. It is built by fine-tuning the RoseTTAFold structure-prediction network to denoise protein structures, which lets it generate proteins from simple specifications. It is the design tool in the [Life Sciences](../index.md) overview.

## Problem

Deep-learning design methods existed, but the preprint notes that a general framework covering binder design, symmetric architectures and enzyme scaffolding had not been described. Diffusion models had succeeded for images and language but less well for proteins, probably because backbone geometry and the link between sequence and structure are complex (Watson et al., 2022).

## Core idea

Start from a random set of backbone coordinates and denoise it step by step into a plausible backbone, in the way image diffusion models turn noise into pictures. The denoiser is RoseTTAFold, a network trained to predict protein structures, so it already encodes protein geometry. Conditioning on a design specification steers the result toward a chosen shape or function.

## Equation or algorithm

RFdiffusion follows the [denoising diffusion](../../../theory/paradigms/unsupervised/density-and-generative-models/diffusion/ddpm.md) framework (Ho et al., 2020). A forward process adds noise to real structures, and a learned reverse process removes it. Generation runs the reverse process from noise, conditioned on the design task:

1. Sample a random backbone.
2. Denoise it over many steps with the fine-tuned RoseTTAFold network.
3. Test the resulting designs experimentally.

## Results

The preprint reports strong performance on unconditional and topology-constrained monomer design, protein binder design, symmetric oligomer design, enzyme active-site scaffolding and symmetric motif scaffolding. It reports experimental characterisation of hundreds of new designs.

## Limitations

- The results here come from the preprint abstract. The published version should be consulted for final figures and success rates for each task.
- The model proposes designs, and experiments decide which ones work. Design quality is not guaranteed.
- The design model is built on RoseTTAFold, so its strengths and gaps in structure prediction carry over (an inference, not a claim from the paper).

## Connections

- [ESM-2 and ESMFold](../esm/index.md): sequence-based protein language models that predict structure from a single sequence.
- [Denoising diffusion](../../../theory/paradigms/unsupervised/density-and-generative-models/diffusion/ddpm.md): the general framework the method builds on.

## References

### Seminal papers

- Watson et al. (2023). De novo design of protein structure and function with RFdiffusion. *Nature*. https://doi.org/10.1038/s41586-023-06415-8 — The published RFdiffusion paper, which introduces the method.
- Watson et al. (2022). Broadly applicable and accurate protein design by integrating structure prediction networks and diffusion generative models. *bioRxiv*. https://doi.org/10.1101/2022.12.09.519842 — The preprint whose abstract the results section summarises.
- Baek et al. (2021). Accurate prediction of protein structures and interactions using a three-track neural network. *Science*. https://doi.org/10.1126/science.abj8754 — RoseTTAFold, the structure-prediction network that RFdiffusion fine-tunes.
- Jumper et al. (2021). Highly accurate protein structure prediction with AlphaFold. *Nature*. https://doi.org/10.1038/s41586-021-03819-2 — AlphaFold 2, the structure predictor that RoseTTAFold is usually compared with.
- Ho et al. (2020). Denoising Diffusion Probabilistic Models. arXiv. https://arxiv.org/abs/2006.11239 — The diffusion framework the method builds on.
