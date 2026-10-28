---
status: draft
last_reviewed: 2026-10-28
tags:
  - sequence modelling
  - uncertainty
aliases:
  - 統計自然語言處理
  - statistical NLP
  - 統計機器翻譯
  - statistical machine translation
  - 隱馬可夫模型
  - hidden Markov model
  - 語料庫
  - corpus
  - 詞性標註
---

# Statistical Language Processing (1976–1993)

Statistical language processing replaced hand-written grammars and rules with probabilistic models estimated from data. It began with speech recognition in the 1970s. In the early 1990s the same approach reached machine translation and part-of-speech tagging, helped by large annotated text corpora such as the Penn Treebank.

## Overview

By the 1970s speech recognition was the clearest case where rules alone failed. An acoustic signal is ambiguous, and the word sequences that could match it are far too many to list by hand. Frederick Jelinek and his colleagues at IBM framed recognition as a statistical decision: given the sound, find the word sequence that is most probable under a model of the language and a model of how words sound (Jelinek, 1976). This shift from rules to estimated probabilities is what the field later called the statistical turn.

During the 1980s and early 1990s the same way of thinking spread. Translation between French and English was modelled with probabilities learned from sentence pairs in parallel text (Brown et al., 1990, 1993). Part-of-speech tagging was handled by hidden Markov models trained on tagged text (Kupiec, 1992).

## Key concepts

- **Corpus**: a large collection of text or speech, often annotated by people, used to estimate a model's parameters and to test it.
- **Hidden Markov model (HMM)**: a model in which a sequence of hidden states, such as part-of-speech tags, generates the observed words. It has probabilities for moving between states and for each word given a state.
- **Source-channel model**: a way of recovering the most likely original text from an observed output, by combining a language model with a model of how the original becomes the output.
- **Parameter estimation**: fitting a model's probabilities from data, by counting or by iterative methods such as EM.

## How it works

Speech recognition and translation share a decision rule. Given an observation $x$, choose the source sentence $w$ that maximises

$$
\hat{w} = \arg\max_{w}\; P(w)\, P(x \mid w).
$$

The first factor is a language model, which favours fluent word sequences. The second is a channel model: in speech it describes the acoustic signal, and in translation it is a probabilistic translation model learned from aligned sentences.

For tagging, the most probable tag sequence $t_i$ for words $w_i$ maximises

$$
\hat{t} = \arg\max_{t}\; \prod_i P(w_i \mid t_i)\, P(t_i \mid t_{i-1}).
$$

Each factor is estimated by counting in a tagged corpus. Decoding uses dynamic programming, the Viterbi procedure, so the best tag sequence is found without enumerating every possibility. Kupiec (1992) studied how to make such a tagger robust, including for words that rarely appear in training.

## Results

The results of the period are measured against annotated data. Tagging accuracy, for example, is measured against hand-tagged text (Kupiec, 1992). The 1990 and 1993 translation papers use parallel French and English text. The Penn Treebank (Marcus et al., 1993) gave the field a shared, hand-annotated English corpus, which made results comparable across groups.

## Limitations

- **Dependence on data.** Probabilities are only as good as the corpus. Rare events are poorly estimated, and a model trained on one kind of text can perform badly on another.
- **Costly annotation.** Tagged corpora take human effort and cover a language only partly.
- **Less interpretable.** A table of probabilities can predict well without showing why a sentence is grammatical. The statistical turn traded explicit rules for coverage, a trade-off the [MYCIN](../mycin/index.md) page also discusses.

## Connections

Statistical language processing is the immediate ancestor of today's language models. Its probabilistic framing carried into [language models](../../../../theory/models/nlp/index.md) and later [large language models](../../../../theory/models/llm/index.md), which estimate token probabilities from much larger corpora. Hidden Markov models belong to the wider family of [graphical models](../../../../theory/probabilistic/graphical-models/index.md).

The approach also meets the brain-and-mind question. Infants can find word-like units in continuous speech from the statistics of the syllables before they know what the words mean, a finding that the [statistical learning](../../../../brain-mind/developmental-cognition/statistical-learning/index.md) page discusses.

## Applications

- **Speech recognition** in dictation and telephone systems, one of the earliest and most widespread applications.
- **Machine translation**, where probabilistic translation models trained on parallel text became the basis of later statistical systems.

## Open questions

- How much of the structure of language can be learned from statistics over text alone? The answer divides linguists and computational researchers.
- Do probabilistic models describe how people understand language, or only how well machines process it?

## References

### Seminal papers

- Jelinek, F. (1976). Continuous speech recognition by statistical methods. *Proceedings of the IEEE*. https://doi.org/10.1109/PROC.1976.10159 — Frames continuous speech recognition as statistical decoding with probabilistic models estimated from data.
- Brown, P. F. et al. (1990). A statistical approach to machine translation. *Computational Linguistics*. https://aclanthology.org/J90-2002/ — Applies statistical translation models, learned from parallel French and English text, to machine translation.
- Brown, P. F., Della Pietra, S. A., Della Pietra, V. J. & Mercer, R. L. (1993). The mathematics of statistical machine translation: Parameter estimation. *Computational Linguistics*. https://aclanthology.org/J93-2003/ — Sets out the IBM translation models and the estimation methods used to fit them to parallel text.

### Articles and documentation

- Kupiec, J. (1992). Robust part-of-speech tagging using a hidden Markov model. *Computer Speech & Language*. https://doi.org/10.1016/0885-2308(92)90019-Z — Applies a hidden Markov model to part-of-speech tagging and studies how to make the tagger robust in practice.
- Marcus, M., Santorini, B. & Marcinkiewicz, M. A. (1993). Building a large annotated corpus of English: The Penn Treebank. *Computational Linguistics*. https://aclanthology.org/J93-2004/ — Describes the Penn Treebank, a large hand-annotated English corpus that became a standard training and test resource.

### Surveys and textbooks

- Nilsson, N. J. (2009). *The Quest for Artificial Intelligence*. Cambridge University Press. https://doi.org/10.1017/CBO9780511819346 — A history of AI that places the shift to statistical methods in the wider story of the field.
