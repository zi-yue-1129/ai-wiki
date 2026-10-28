---
related:
- brain-mind/cognitive-science
- theory/models/speech
---

# Natural Language Processing

## Timeline

| Period | Approach | Examples |
|---|---|---|
| 1950s–1980s | Rules and grammars | Chomskyan grammar, ELIZA, SHRDLU |
| 1990s–2000s | Statistical NLP | n-grams, HMMs, CRFs, statistical MT |
| 2013–2017 | Word vectors + neural nets | word2vec, GloVe, LSTMs, seq2seq with attention |
| 2018–2020 | Pre-train + fine-tune | ELMo, BERT, GPT-2, T5 |
| 2020– | LLMs + prompting | See [Large Language Models](../llm/index.md) |

## Word vectors

"You shall know a word by the company it keeps" (the distributional hypothesis, Firth 1957). word2vec vectors famously support analogies:

\[
\vec{\text{king}} - \vec{\text{man}} + \vec{\text{woman}} \approx \vec{\text{queen}}
\]

Static embeddings give each word one vector regardless of sense; contextual models like BERT fixed that.

## Classic tasks

| Task | Description | Today |
|---|---|---|
| Tokenisation, POS tagging, parsing | Basic analysis | Less central in the LLM era; still used in pipelines and linguistics |
| Named-entity recognition | Find people, places, organisations | Fine-tuned encoders or LLM extraction |
| Sentiment analysis | Polarity, emotion | Small fine-tuned models remain practical |
| Text classification | Topic, intent | Embeddings + classifier, or LLM |
| Machine translation | Across languages | NMT → LLMs |
| Summarisation | Extractive / abstractive | Mostly LLMs |
| Question answering | Reading comprehension, open-domain | RAG + LLM |
| Information extraction | Relations, events | LLMs with structured output |
| Semantic similarity and retrieval | Sentence embeddings | Sentence-BERT, embedding models, rerankers |
| Dialogue | Task-oriented, open-domain | LLMs |

## Multilingual and low-resource NLP

- Most of the world's ~7,000 languages have little digital text; performance drops sharply for them
- Tokenisers can make some scripts several times more expensive per word
- Approaches: multilingual pre-training, cross-lingual transfer, community data efforts (Masakhane for African languages, Aya), speech-first approaches for unwritten languages
- Chinese-specific issues: word segmentation, Traditional vs Simplified script conversion ([OpenCC](https://github.com/BYVoid/OpenCC)), regional vocabulary differences

## Linguistics and psycholinguistics

- **Chomsky vs statistical learning**: is language an innate universal grammar or learnable from data? LLMs reopened the debate (Piantadosi, 2023, argues LLMs undermine Chomsky's arguments; Chomsky and others disagree)
- **Surprisal theory**: human reading times scale with a word's negative log-probability (Hale, 2001; Levy, 2008); LLM surprisal is an excellent predictor of reading times
- **The N400** ERP component to semantically unexpected words correlates with language-model surprisal
- **Probing**: do LLMs encode syntax trees and semantic roles? (Hewitt & Manning, 2019, structural probes)
- See [Cognitive Science](../../../brain-mind/cognitive-science/index.md)

## Resources

- Jurafsky & Martin, *Speech and Language Processing*, 3rd ed. draft (free online)
- Stanford CS224n
- Hugging Face LLM Course
- [d2l: NLP chapters](https://d2l.ai/chapter_natural-language-processing-pretraining/index.html)

## References

### Seminal papers

- Mikolov, T., et al. (2013). *Efficient Estimation of Word Representations in Vector Space*. arXiv. https://arxiv.org/abs/1301.3781 — word2vec, which learns dense word vectors whose geometry captures meaning and analogy.
- Sutskever, I., Vinyals, O. & Le, Q. V. (2014). *Sequence to Sequence Learning with Neural Networks*. NeurIPS. https://arxiv.org/abs/1409.3215 — An encoder–decoder LSTM that translates whole sentences end to end, the basis of neural machine translation.
- Devlin, J., et al. (2018). *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding*. arXiv. https://arxiv.org/abs/1810.04805 — Masked-language-model pretraining that became the standard starting point for fine-tuned NLP systems.

### Surveys and textbooks

- Jurafsky, D. & Martin, J. H. *Speech and Language Processing*, 3rd ed. (draft). https://web.stanford.edu/~jurafsky/slp3/ — The standard NLP textbook, from text processing to large language models; the authors publish a free online draft.

### Lectures and videos

- Yang, D. & Choi, Y. *CS224N: Natural Language Processing with Deep Learning*. Stanford University. https://web.stanford.edu/class/cs224n/ — A Stanford course on neural NLP, from word vectors to large language models, with PyTorch assignments.

### Articles and documentation

- Mikolov, T., Sutskever, I., Chen, K., Corrado, G. & Dean, J. (2013). *Distributed Representations of Words and Phrases and their Compositionality*. NeurIPS. arXiv:1310.4546. https://arxiv.org/abs/1310.4546 — Introduces skip-gram training with negative sampling, an efficient way to learn word embeddings.
