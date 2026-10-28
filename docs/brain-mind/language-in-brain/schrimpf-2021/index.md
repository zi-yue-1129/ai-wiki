---
status: complete
last_reviewed: 2026-10-28
related:
- brain-mind/neuroai
- theory/models/llm
- theory/models/transformer
tags:
- neuroscience
- language
aliases:
  - Schrimpf 2021
  - Neural architecture of language
  - Integrative modeling of language
---

# Language Models Predict Brain Responses to Sentences (Schrimpf et al. 2021)

Schrimpf et al. (2021) asked which computational features of a language model explain human brain responses to sentences. They scored many transformer models on how well their internal representations predicted neural responses, and found that the best models explained nearly all the explainable variance. The brain fit tracked next-word prediction accuracy more closely than performance on other language tasks, which the authors read as support for predictive processing.

This page is part of [Language in the Brain](../index.md). The parent page gives the overview; this page covers the method and its evidence.

## The problem

Language models and human listeners both handle sentences, but a model that performs well on language tasks might not process sentences in the same way as the brain. The question was which properties of a model, if any, predict how well its representations match neural responses, and whether those properties are the ones that make it good at predicting words.

## The approach

The authors presented the same sentences to human participants and to a set of transformer language models. Neural responses were recorded with functional MRI and with electrocorticography (ECoG), and each model's internal activations were extracted for the same sentences.

The steps were:

1. Present the same sentences to human participants and to a set of transformer language models.
2. Record brain responses with fMRI and ECoG, and extract each model's internal activations.
3. Fit a regression from model activations to the brain responses, and measure how much of the explainable variance it accounts for.
4. Relate each model's brain fit to its next-word prediction accuracy and to its scores on other language tasks.

Step 4 is the key comparison. It separates the property that tracks the brain from the many properties a model may have.

## Results

The most powerful models predicted nearly 100% of the explainable variance in neural responses to sentences, across datasets and across both imaging modalities. Brain fit and behavioural fit correlated strongly with next-word prediction accuracy. They did not track performance on other language tasks, which the authors take as evidence for predictive processing.

## Limitations

- The explainable variance depends on the noise ceiling of each dataset, so the figure is relative to that ceiling rather than an absolute measure of fit.
- The result shows a correlation between prediction and brain fit. It does not show that the brain implements the same mechanism.
- Model architecture also affected the fit. The authors treat this as a separate factor, which means prediction accuracy is not the only thing that matters.

## Connections

- **Method family**: the comparison of brain responses with language models is also the subject of [Goldstein et al. 2022](../goldstein-2022/index.md), which uses a different recording method and asks a more temporal question.
- **Language network**: the regions these responses come from are the language network, and the paper relies on the localiser in [Fedorenko et al. 2010](https://pmc.ncbi.nlm.nih.gov/articles/PMC2934923).
- **Model families**: the transformer architecture used in the comparison is on [Transformer](../../../theory/models/transformer/index.md), and the language-model family is on [Large Language Models](../../../theory/models/llm/index.md).
- **Earlier framework**: the cortical streams the paper's regions are read against are in [Hickok and Poeppel 2007](../hickok-poeppel-2007/index.md).

## Open questions

- **Does prediction explain the fit, or only correlate with it?** The correlation with next-word accuracy is strong, but a causal link would need an intervention on the model.
- **Does the result generalise beyond these datasets?** The noise ceilings and recording sites are specific to the studies, so cross-study comparisons need care.

## References

### Seminal papers

- Schrimpf, M., Blank, I. A., Tuckute, G., Kauf, C., Hosseini, E. A., Kanwisher, N., Tenenbaum, J. B. & Fedorenko, E. (2021). The neural architecture of language: Integrative modeling converges on predictive processing. *PNAS*. https://doi.org/10.1073/pnas.2105646118 — Shows that the best transformer models predict nearly all explainable variance in neural responses to sentences.
- Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, Ł. & Polosukhin, I. (2017). Attention Is All You Need. *NeurIPS*. https://arxiv.org/abs/1706.03762 — Introduces the transformer architecture used by the models compared in the study.
- Hickok, G. & Poeppel, D. (2007). The cortical organization of speech processing. *Nature Reviews Neuroscience*. https://doi.org/10.1038/nrn2113 — The dual-stream model that gives the cortical framing for the regions studied.
- Fedorenko, E., Hsieh, P.-J., Nieto-Castañón, A., Whitfield-Gabrieli, S. & Kanwisher, N. (2010). New method for fMRI investigations of language: defining ROIs functionally in individual subjects. *Journal of Neurophysiology*. https://pmc.ncbi.nlm.nih.gov/articles/PMC2934923 — The individual-level localiser that defines the language network used in the study.

### Articles and primary research

- Goldstein, A., Zada, Z., Buchnik, E., Schain, M., Price, A., et al. (2022). Shared computational principles for language processing in humans and deep language models. *Nature Neuroscience*. https://doi.org/10.1038/s41593-022-01026-4 — Compares human ECoG responses with GPT-2 on prediction, surprise and contextual embeddings during a podcast.
- Caucheteux, C. & King, J.-R. (2022). Brains and algorithms partially converge in natural language processing. *Communications Biology*. https://doi.org/10.1038/s42003-022-03036-1 — Compares language-model representations with brain recordings, and reports partial convergence between the two.
