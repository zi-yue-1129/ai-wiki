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
  - Goldstein 2022
  - Shared computational principles
  - Contextual embeddings and next-word prediction
---

# Shared Computational Principles for Language (Goldstein et al. 2022)

Goldstein et al. (2022) asked whether an autoregressive language model and the human brain share computational principles during real listening, or whether the similarity appears only in the final predictions. They recorded electrocorticography (ECoG) while people listened to a podcast, and compared the neural signals with GPT-2 on three properties: prediction before a word is heard, surprise after it is heard, and contextual embeddings for each word. The match was strongest for the contextual embeddings, and it improved as the context grew.

This page is part of [Language in the Brain](../index.md). The parent page gives the overview; this page covers the method and its evidence.

## The problem

Language models predict the next word, and so does the listener. The open question was whether the brain's prediction and the model's prediction line up word by word during natural speech, and whether the internal representations match as well. Earlier studies compared models with brains mostly on sentences or on the final outputs, so the temporal structure of the match was not clear.

## The approach

Nine participants listened to a 30-minute podcast while ECoG was recorded from electrodes placed for clinical reasons. For each word, the authors compared three things with GPT-2: the human predictability of the word, a surprise signal after the word was heard, and the contextual embedding of the word. They also used GloVe, a static word embedding, as a baseline.

The steps were:

1. Collect word-level predictions from human participants, and compare them with GPT-2's predictions for the same words.
2. Measure how well each electrode's signal encodes GPT-2 embeddings and GloVe embeddings.
3. Test whether neural activity before word onset predicts the upcoming word, and whether post-onset activity tracks surprise.
4. Decode word identity from neural signals, and compare the decoding performance across embedding types.

Step 2 is the comparison that separates contextual embeddings from static ones. Electrodes that encode GPT-2 can be compared with those that encode GloVe, site by site.

## Results

Human predictability and GPT-2 predictions correlated at r = 0.79. The match improved as the context grew, from r = 0.46 at two words to about 0.79 at roughly 100 words.

GPT-2 contextual embeddings were encoded at 208 left-hemisphere electrodes and 34 right-hemisphere electrodes. Of the left-hemisphere sites, 71 were not found with GloVe. Decoding word identity with GPT-2 embeddings gave a mean ROC-AUC of 0.74, against 0.68 for GloVe. For unpredicted words, post-onset activity peaked around 400 ms after onset.

## Limitations

- The study has nine participants, so the generality across individuals is limited.
- ECoG is recorded only where clinical needs place electrodes. This constrains which regions can be studied.
- The authors argue for a biologically plausible framework. The results do not show that the brain implements a transformer.

## Connections

- **Method family**: the comparison of brain responses with transformer models is also on [Schrimpf et al. 2021](../schrimpf-2021/index.md), which uses fMRI and ECoG on sentences rather than a continuous podcast.
- **Model families**: the autoregressive model used here is on [Large Language Models](../../../theory/models/llm/index.md), and the transformer architecture is on [Transformer](../../../theory/models/transformer/index.md).
- **Static embeddings**: GloVe, the baseline in the study, is a static word embedding, described in [Pennington et al. 2014](https://aclanthology.org/D14-1162/).
- **Earlier framework**: the streams the regions are read against are in [Hickok and Poeppel 2007](../hickok-poeppel-2007/index.md).

## Open questions

- **Does the match hold for other people and other languages?** Nine participants and one podcast leave the generality open.
- **Is the similarity mechanistic?** Matching representations and predictions is evidence of shared structure, not of shared computation.

## References

### Seminal papers

- Goldstein, A., Zada, Z., Buchnik, E., Schain, M., Price, A., et al. (2022). Shared computational principles for language processing in humans and deep language models. *Nature Neuroscience*. https://doi.org/10.1038/s41593-022-01026-4 — Compares human ECoG responses with GPT-2 on prediction, surprise and contextual embeddings during a podcast.
- Schrimpf, M., Blank, I. A., Tuckute, G., Kauf, C., Hosseini, E. A., Kanwisher, N., Tenenbaum, J. B. & Fedorenko, E. (2021). The neural architecture of language: Integrative modeling converges on predictive processing. *PNAS*. https://doi.org/10.1073/pnas.2105646118 — Shows that the best transformer models predict nearly all explainable variance in neural responses to sentences.
- Pennington, J., Socher, R. & Manning, C. D. (2014). GloVe: Global Vectors for Word Representation. *EMNLP*. https://aclanthology.org/D14-1162/ — The static word embedding used as the baseline in the study.
- Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, Ł. & Polosukhin, I. (2017). Attention Is All You Need. *NeurIPS*. https://arxiv.org/abs/1706.03762 — Introduces the transformer architecture behind the contextual embeddings.

### Articles and primary research

- Caucheteux, C. & King, J.-R. (2022). Brains and algorithms partially converge in natural language processing. *Communications Biology*. https://doi.org/10.1038/s42003-022-03036-1 — Compares language-model representations with brain recordings, and reports partial convergence between the two.
- Hickok, G. & Poeppel, D. (2007). The cortical organization of speech processing. *Nature Reviews Neuroscience*. https://doi.org/10.1038/nrn2113 — The dual-stream model that frames the cortical regions studied.
