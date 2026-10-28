---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/nlp
  - theory/models/transformer
  - brain-mind/attention-brain-machine
aliases:
  - 語言學與機器翻譯
  - Machine translation
  - Linguistics
---

# Linguistics and Machine Translation

AI now does most of the work of translating text between languages, and it is increasingly used to study language itself. This page covers how AI is used in translation and linguistic research. The underlying language models are described in [Natural Language Processing](../../theory/models/nlp/index.md).

## Landscape

| Area | Examples |
|---|---|
| Text translation | Commercial and open neural machine translation for documents, websites and chat |
| Speech translation | Spoken input translated to text or speech, used in travel and meetings |
| Corpus linguistics | Large annotated corpora and automatic tagging of grammar and meaning |
| Low-resource languages | Translation and documentation for languages with little written data |
| Literary and specialist translation | Drafting tools used by translators, with human review |
| Language learning | Automatic feedback on grammar, pronunciation and vocabulary |

## From rules to neural models

Machine translation began with hand-written rules, then moved to statistical models that learned phrase correspondences from parallel text. The standard reference for that period is Koehn's textbook (see References). Since about 2014, neural models have replaced most of the statistical pipeline.

## Key methods

Three landmark ideas shaped neural translation. Each links to the page that explains it.

- [Attention for alignment (Bahdanau et al. 2014)](../../theory/models/transformer/bahdanau-attention/index.md): the decoder learns to look back at the source words most relevant to each output word.
- [Transformer (Vaswani et al. 2017)](../../theory/models/transformer/attention-is-all-you-need/index.md): attention alone replaces recurrence, which made training faster and is the basis of current systems.
- Subword units: splitting rare words into smaller pieces, so the vocabulary does not have to list every word (Sennrich et al. 2015, see References).

## Low-resource languages

Most of the world's languages have little parallel text, so systems trained on web data serve them poorly. The NLLB project (2022) built a system covering 200 languages, with new datasets gathered by interviewing native speakers. Its authors report large gains over earlier systems, but the quality gap between high-resource and low-resource languages remains, and a single benchmark cannot show how a system works for every community.

## Evaluation

- Automatic scores such as BLEU compare system output with reference translations. They correlate only roughly with human judgement, and they can mislead when references are few.
- Human evaluation is the standard for publication, but it is slow and costly.
- Safety checks, such as toxicity benchmarks, are now part of major multilingual evaluations.

## Risks

- **Errors in high-stakes text.** A mistranslated medical instruction or legal clause can cause real harm, so professional review is still needed.
- **Bias and stereotyping** carried over from training data, for example gendered pronouns in occupations.
- **Language endangerment.** Automatic tools may spread a dominant language's norms and reduce incentives to document minority languages.

## Connections

- Attention in translation was named by analogy to selective attention in the brain. The analogy is loose; see [Attention in Brains & Machines](../../brain-mind/attention-brain-machine/index.md).
- Language models used for translation are covered in [Natural Language Processing](../../theory/models/nlp/index.md).

## Open questions

- How well do translation systems handle languages with no written standard, dialects and code-switching?
- How should translation quality be measured when there is no single correct answer?
- Can machine-assisted translation improve the work of human translators, without lowering pay or quality?

## References

### Seminal papers

- Bahdanau, D., Cho, K. & Bengio, Y. (2014). Neural Machine Translation by Jointly Learning to Align and Translate. arXiv. https://arxiv.org/abs/1409.0473 — Introduces learned soft alignment between source and target words, so the model no longer compresses a sentence into one fixed vector.
- Vaswani, A. et al. (2017). Attention Is All You Need. NeurIPS. https://arxiv.org/abs/1706.03762 — Introduces the Transformer, which uses attention alone and improves translation quality while training faster.
- Sennrich, R., Haddow, B. & Birch, A. (2015). Neural Machine Translation of Rare Words with Subword Units. arXiv. https://arxiv.org/abs/1508.07909 — Splits rare words into subword units, so neural systems can translate words they have not seen before.
- NLLB Team (2022). No Language Left Behind: Scaling Human-Centered Machine Translation. arXiv. https://arxiv.org/abs/2207.04672 — A translation system for 200 languages, built with new datasets and an open evaluation across more than 40,000 language pairs.

### Surveys and textbooks

- Koehn, P. (2009). *Statistical Machine Translation*. Cambridge University Press. https://www.cambridge.org/core/books/statistical-machine-translation/94EADF9F680558E13BE759997553CDE5 — A textbook on statistical machine translation, covering word-based, phrase-based and tree-based models, and evaluation.
