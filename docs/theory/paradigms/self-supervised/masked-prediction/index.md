---
tags:
  - self-supervised learning
  - masked modelling
  - pre-training
---

# Masked Prediction

Masked prediction hides part of an input and trains a model to reconstruct the hidden part from the rest. BERT made this the standard pre-training recipe for language, and masked autoencoders brought it to images.

## Overview

Choose a subset of the input tokens or patches, replace them with a mask or drop them, and predict the missing content from the visible context. The loss is usually cross-entropy over a vocabulary for discrete tokens, and mean squared error for continuous pixels or features. No labels are needed, since the target is part of the input.

## Methods

- **BERT** masks about 15% of word-piece tokens and predicts them with a bidirectional transformer, and it also predicts whether two sentences follow each other (a second objective the follow-up work tested and often dropped).
- **Masked autoencoders (MAE)** mask a large fraction of image patches, often about 75%, encode only the visible patches, and decode the full image. The high masking ratio makes the task non-trivial.
- **Speech models** such as wav2vec 2.0 and HuBERT mask spans of audio and predict discrete targets derived from clustering.
- **Protein and molecule models** mask residues or atoms and predict them, learning sequence and structural regularities.

## Why the masking ratio matters

If too little of the input is hidden, the task can be solved by copying nearby information. If too much is hidden, there is not enough context. MAE's high ratio works for images because pixels are highly redundant, whereas text is information-dense and needs a lower ratio.

## Connections

Masked prediction generalises the [denoising autoencoder](../../unsupervised/autoencoders-and-representations/index.md), where the corruption is noise rather than deletion. The large language model objective is next-token prediction, a related autoregressive form, see [Large Language Models](../../../models/llm/index.md). Masked image models are also covered under [computer vision](../../../models/computer-vision/index.md).

## Applications

Pre-training language models for classification, search and question answering, pre-training vision encoders for medical imaging, speech recognition with little labelled audio, and protein representation learning for structure and function prediction.

## Open questions

Masked objectives learn features that are good for prediction but may not be best for linear probing or retrieval. Whether masking should be random, semantic or adaptive is debated, and scaling masked models to video and multimodal data is still being explored.

## References

### Seminal papers

- Devlin, Chang, Lee & Toutanova (2019), "BERT: pre-training of deep bidirectional transformers for language understanding", NAACL, arXiv:1810.04805 — Masked language modelling with a bidirectional transformer, the start of modern language pre-training.
- He, Chen, Xie, Li, Dollár & Girshick (2022), "Masked autoencoders are scalable vision learners", CVPR, arXiv:2111.06377 — Masks most image patches and reconstructs them with an asymmetric encoder–decoder.
- Hinton & Salakhutdinov (2006), "Reducing the dimensionality of data with neural networks", *Science* 313. https://doi.org/10.1126/science.1127647 — Layer-wise pre-training by reconstruction, an early form of the same idea.
- Vincent, Larochelle, Bengio & Manzagol (2008), "Extracting and composing robust features with denoising autoencoders", ICML. https://doi.org/10.1145/1390156.1390294 — The denoising objective that masked prediction generalises.

### Surveys and textbooks

- Bengio, Courville & Vincent (2013), "Representation learning: a review and new perspectives", *IEEE TPAMI* 35(8), arXiv:1206.5538 — Survey of learned representations, the background for pre-training objectives.

### Lectures and videos

(none checked for this page)

### Articles and documentation

(none beyond the entries above)

## Further reading

- Devlin et al., *google-research/bert*, GitHub repository. https://github.com/google-research/bert — The original TensorFlow code and pre-trained models for BERT; the repository is archived and read-only.
