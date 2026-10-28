---
related:
  - engineering/vector-databases
  - engineering/rag
  - theory/models/transformer
aliases:
  - 搜尋引擎
  - 資訊檢索
---

# Search and Information Retrieval

Search engines decide which few items out of billions a person sees first. Machine learning now runs most stages of that decision, and generative models have added a new kind of search product that writes an answer instead of returning links.

## Landscape

| Area | Methods | Notes |
|---|---|---|
| Query understanding | Spelling correction, query classification, query rewriting with language models | Short, ambiguous queries are the norm |
| Candidate retrieval | Inverted indexes with BM25; dense retrieval with bi-encoders; approximate nearest-neighbour search | Must return candidates in milliseconds |
| Ranking | Learning to rank with gradient-boosted trees; neural cross-encoders (BERT-style re-rankers) | Usually applied to the top few hundred candidates |
| Personalisation and ads ranking | Click-through-rate models, user embeddings | Shares machinery with recommendation |
| Generative search and answer engines | Retrieval-augmented generation with inline citations | Citation accuracy is the main failure mode |
| Evaluation | Human relevance judgements, NDCG, online A/B tests | Click logs are biased by position |

## How a modern search stack fits together

A typical system runs in stages. A cheap retriever (a sparse index, a dense vector index, or both) selects a few hundred candidates. A learned ranker then reorders them, often in two passes, the second with a more expensive neural model. Finally, a post-processing layer removes duplicates, applies policy rules and, in answer engines, asks a language model to summarise the top documents with citations.

## Why it is hard

- **Biased feedback**: users click what they are shown, so raw click logs mix relevance with position. Joachims (2002) showed how clickthrough data can train a ranker, and the bias problem has been central since.
- **Latency budgets**: a neural model that is accurate but slow must run on fewer candidates.
- **Long-tail queries**: most queries are rare, so models trained on logs see little of them.
- **Freshness**: indexes must absorb new documents without a full rebuild.

## Key methods

Four methods explain most of the current stack. Each links to the page that explains it.

- [Dense Passage Retrieval](../../engineering/vector-databases/dense-passage-retrieval.md): separate encoders map queries and passages into one vector space, so retrieval becomes nearest-neighbour search.
- [ColBERT](../../engineering/vector-databases/colbert.md): keeps one vector per token and scores query and passage with late interaction, trading storage for accuracy.
- [HNSW](../../engineering/vector-databases/hnsw.md): a graph index that makes approximate nearest-neighbour search fast enough for candidate retrieval.
- [Retrieval-Augmented Generation](../../engineering/rag/index.md): feeds retrieved documents to a generator, the basis of answer engines.

Neural re-rankers are usually [Transformers](../../theory/models/transformer/index.md) fine-tuned on query-passage pairs (Nogueira & Cho, 2019).

## Connections

- The building blocks (vector stores, RAG pipelines) are covered in [Vector Databases and Semantic Search](../../engineering/vector-databases/index.md) and [Retrieval-Augmented Generation](../../engineering/rag/index.md). This page is about ranking at web scale and the products built on it.
- Exploration in ranking, where a system must show new items to learn about them, is a bandit problem. See [Contextual Bandits](../../theory/paradigms/online/contextual-bandits/index.md).
- Human memory works partly as retrieval from cues, a parallel that the [Memory & Learning](../../brain-mind/memory-learning/index.md) chapter examines.

## Applications

- Web search and answer engines
- Enterprise and document search, including legal discovery (see [Law](../law/index.md))
- E-commerce product ranking
- Advertising and feed ranking, which share ranking models with search

## Risks and limits

- **Unsupported answers**: Liu et al. (2023) found that many sentences in generative search responses were not fully supported by the sources they cited.
- **Feedback loops**: a ranker trained on its own past clicks can narrow what people see.
- **Gaming**: search-engine optimisation and AI-generated content target the ranking signals directly.
- **Publisher and traffic effects**: answer engines can reduce the clicks that sources depend on.

## Open questions

- How to evaluate answer engines beyond click metrics, given that users often read the answer and never visit a source.
- How to attribute and compensate sources whose content feeds a generated answer.

## References

### Seminal papers

- Joachims, T. (2002). Optimizing search engines using clickthrough data. *Proceedings of the 8th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining*. https://doi.org/10.1145/775047.775067 — Shows how clickthrough logs can train a ranking function as implicit relevance feedback.
- Karpukhin, V. et al. (2020). Dense Passage Retrieval for Open-Domain Question Answering. *EMNLP*. https://arxiv.org/abs/2004.04906 — Trains separate question and passage encoders so that retrieval reduces to nearest-neighbour search over dense vectors.
- Khattab, O. & Zaharia, M. (2020). ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT. *SIGIR*. https://arxiv.org/abs/2004.12832 — Scores query and passage token by token, balancing the accuracy of cross-encoders with the speed of bi-encoders.
- Nogueira, R. & Cho, K. (2019). Passage Re-ranking with BERT. arXiv. https://arxiv.org/abs/1901.04085 — Applies BERT as a re-ranker over retrieved passages and reports large gains on passage retrieval benchmarks.
- Lewis, P. et al. (2020). Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. *NeurIPS*. https://arxiv.org/abs/2005.11401 — Combines a retriever with a sequence generator so that answers can draw on retrieved documents.

### Surveys and textbooks

- Liu, T.-Y. (2009). Learning to Rank for Information Retrieval. *Foundations and Trends in Information Retrieval*. https://doi.org/10.1561/1500000016 — Survey of pointwise, pairwise and listwise approaches to learning ranking functions.
- Robertson, S. & Zaragoza, H. (2009). The Probabilistic Relevance Framework: BM25 and Beyond. *Foundations and Trends in Information Retrieval*. https://doi.org/10.1561/1500000019 — Explains the BM25 family of sparse retrieval scoring functions that most search engines still use for candidate generation.
- Johnson, J., Douze, M. & Jégou, H. (2021). Billion-Scale Similarity Search with GPUs. *IEEE Transactions on Big Data*. https://doi.org/10.1109/TBDATA.2019.2921572 — Describes the FAISS library for searching very large sets of dense vectors on GPUs.

### Articles and documentation

- Liu, N. F. et al. (2023). Evaluating Verifiability in Generative Search Engines. arXiv. https://arxiv.org/abs/2304.09848 — Measures whether the citations given by generative search engines actually support the sentences they are attached to.
