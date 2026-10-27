---
related:
- models/llm
- brain-mind/cognitive-science
- models/computer-vision
---

# Self-Supervised Learning

## Idea

Create a supervised-looking task **from unlabelled data itself** — hide part of the input and predict it, or make two views of the same thing agree. The model must learn useful representations to solve the pretext task. Self-supervision is what makes foundation models possible: there is no limit on the amount of "labelled" data when the data labels itself.

## Families

| Family | Pretext task | Examples |
|---|---|---|
| Autoregressive prediction | Predict the next token / pixel / audio sample | GPT, PixelCNN, WaveNet, audio LMs |
| Masked modelling | Reconstruct masked parts | BERT (text), MAE and BEiT (images), wav2vec 2.0 / HuBERT (speech), masked protein models (ESM) |
| Contrastive learning | Pull together views of the same item, push apart others (InfoNCE loss) | SimCLR, MoCo, CPC, CLIP (image–text) |
| Non-contrastive joint embedding | Agree across views without negatives, avoiding collapse via asymmetry or regularisation | BYOL, SimSiam, Barlow Twins, VICReg, DINO |
| Joint-embedding predictive architectures | Predict *representations* of hidden parts, not raw pixels | I-JEPA, V-JEPA |
| Denoising | Remove added noise | Denoising autoencoders, diffusion models |
| Pretext puzzles (early work) | Rotation prediction, jigsaw, colourisation | 2016–2018 vision papers |

### InfoNCE (contrastive) loss

For an anchor \(z_i\), positive \(z_i^+\), and negatives \(z_j\), with similarity \(s\) and temperature \(\tau\):

\[
L = -\log \frac{\exp(s(z_i, z_i^+)/\tau)}{\sum_j \exp(s(z_i, z_j)/\tau)}
\]

Minimising it maximises a lower bound on the mutual information between views.

## Why it works

- The pretext task forces the model to capture regularities (syntax, semantics, object shape, physics) that are also useful for downstream tasks.
- Scale: billions of examples are free.
- Augmentations encode **invariances** we want (crop, colour jitter → object identity matters, exact pixels don't).

## Risks

- **Representation collapse** in joint-embedding methods (everything maps to one point) — prevented by negatives, stop-gradient, variance/covariance regularisation.
- **Learned shortcuts** from augmentations or data artefacts.
- **Data quality and bias** are inherited wholesale from web-scale corpora.

## The brain as a self-supervised learner

- **Predictive coding / predictive processing** (Rao & Ballard, 1999; Friston): the cortex continuously predicts its sensory input and learns from prediction errors — essentially self-supervised learning. See [Cognitive Science](../../../brain-mind/cognitive-science/index.md).
- **Temporal contrast**: slowness / temporal-coherence principles (slow feature analysis) yield complex-cell-like and place-cell-like representations.
- **Self-supervised models match the ventral stream about as well as supervised ones** (Zhuang et al., 2021, *PNAS*), which matters because primates do not receive millions of labels.
- **Language**: next-word prediction models predict activity in human language areas (Schrimpf et al., 2021); the brain may predict upcoming words at multiple timescales (Caucheteux et al., 2023).

## Further reading

- Balestriero et al. (2023), "A Cookbook of Self-Supervised Learning"
- LeCun & Misra, "Self-supervised learning: the dark matter of intelligence" (Meta AI blog, 2021)
- Chen et al. (2020) SimCLR; He et al. (2022) MAE; Radford et al. (2021) CLIP
