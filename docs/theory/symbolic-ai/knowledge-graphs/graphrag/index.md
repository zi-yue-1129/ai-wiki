---
status: draft
last_reviewed: 2026-10-28
tags:
  - retrieval
  - large language models
aliases:
  - GraphRAG
  - Graph RAG
  - 圖式檢索增強生成
  - Query-focused summarization
  - 查詢導向摘要
---

# GraphRAG

GraphRAG is a retrieval-augmented generation method. A large language model (LLM) builds an entity graph from a document collection, groups the graph into communities and writes a summary for each community. To answer a question, the system summarises these summaries. Edge and colleagues introduced it in 2024 for questions about a whole corpus rather than one passage. It is one of the two landmark methods in the [knowledge graphs overview](../index.md).

## Overview

[Retrieval-augmented generation](../../../../engineering/rag/index.md) (RAG) retrieves passages relevant to a question and gives them to a language model.[^1] It works well when a few passages answer the question. It fails on global questions, such as "What are the main themes in the dataset?", because the top retrieved chunks cover only a small part of the corpus. The paper treats these as query-focused summarisation (QFS). Earlier QFS methods do not scale to the volume of text that RAG systems index. GraphRAG combines a graph index, which scales, with summarisation, which covers the corpus.[^2]

## Key concepts

- **Entity graph**: nodes are entities, edges are relationships, and claims extracted by an LLM are attached to them.
- **Community**: a group of closely related graph elements, found by community detection. The method uses the Leiden algorithm.[^3]
- **Community summary**: an LLM-written summary of a community. Higher-level summaries reuse lower-level ones when the source text does not fit the context window.
- **Global and local questions**: global questions concern the whole corpus; local questions concern a specific entity or passage.
- **Token budget**: the number of tokens that fit in the model's context window, which limits how many summaries can be combined.

## How it works

Indexing and querying both use LLM calls.

1. **Chunk.** The corpus is split into chunks. The experiments used 600-token chunks with 100-token overlaps.[^2]
2. **Extract.** An LLM reads each chunk and extracts entities, relationships and claims, which are merged into one graph.
3. **Partition.** Leiden community detection divides the graph into communities at several levels.
4. **Summarise.** An LLM writes a summary of each community, from the lowest level upward. If a community's element summaries fit the token limit, they are summarised together; otherwise sub-community summaries replace their members.[^2]
5. **Answer.** For a query, each community summary at the chosen level produces a partial answer with a helpfulness score (map step). The highest-scoring partial answers are added to a context window until the token limit is reached, and an LLM summarises them into the final answer (reduce step).

## Results

The evaluation used two corpora: podcast transcripts of 1,669 chunks, about one million tokens, and news articles of 3,197 chunks, about 1.7 million tokens. For each corpus, 125 LLM-generated global questions were compared head to head by an LLM judge on comprehensiveness, diversity, empowerment and directness.[^2]

Global GraphRAG approaches beat vector RAG on comprehensiveness and diversity. Comprehensiveness win rates were 72–83% on the podcast transcripts and 72–80% on the news articles. Diversity win rates were 75–82% and 62–71%.[^2] Vector RAG gave the most direct answers, which the authors used as a validity check.

The cheapest variant, root-level community summaries, won 72% of comprehensiveness and 62% of diversity comparisons against vector RAG. It used more than 97% fewer context tokens than map-reduce summarisation of the source text.[^2] Indexing the podcast corpus took 281 minutes on a virtual machine.[^2]

## Limitations

- **Narrow evaluation.** The paper covers two corpora, and the authors say generalisation to other domains needs more work.[^2]
- **LLM judges.** Comparisons rest on LLM judgements. The authors note that fabrication rates were not measured, and that such a comparison would strengthen the analysis.[^2]
- **Trade-offs.** The authors find that directness runs against comprehensiveness and diversity, so GraphRAG is suited to sensemaking questions rather than precise lookups.[^2]
- **Indexing cost.** Every chunk and community passes through an LLM, which makes indexing slow and expensive for large corpora.

## Open questions

- How sensitive are answers to the extraction prompts? Errors in the graph reach every summary built on it.
- How should the index be updated when documents change, without rebuilding every summary?
- How does GraphRAG compare with other graph-based and tree-based methods, such as RAPTOR, which also summarises bottom-up?[^4]

[^1]: Lewis et al. (2020), listed above.
[^2]: Edge et al. (2024), listed above. Figures and procedure are as the paper reports them from its experiments.
[^3]: Traag et al. (2018), listed above.
[^4]: Sarthi et al. (2024) and Peng et al. (2024), listed above.

## References

### Seminal papers

- Edge, D. et al. (2024). From Local to Global: A Graph RAG Approach to Query-Focused Summarization. arXiv. https://arxiv.org/abs/2404.16130 — Builds an LLM-derived entity graph with community summaries to answer global questions over large document collections.
- Lewis, P. et al. (2020). Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. arXiv. https://arxiv.org/abs/2005.11401 — Introduces RAG, pairing a pretrained generator with a retriever over an explicit, non-parametric memory.
- Traag, V., Waltman, L. & van Eck, N. J. (2018). From Louvain to Leiden: guaranteeing well-connected communities. arXiv. https://arxiv.org/abs/1810.08473 — Shows that the Louvain method can produce badly connected communities, the problem the Leiden algorithm addresses.
- Sarthi, P. et al. (2024). RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval. arXiv. https://arxiv.org/abs/2401.18059 — Recursively clusters and summarises text chunks into a tree that is retrieved at several levels of abstraction.

### Surveys and textbooks

- Gao, Y. et al. (2023). Retrieval-Augmented Generation for Large Language Models: A Survey. arXiv. https://arxiv.org/abs/2312.10997 — Surveys RAG for LLMs, including how it addresses hallucination and outdated knowledge.
- Peng, B. et al. (2024). Graph Retrieval-Augmented Generation: A Survey. arXiv. https://arxiv.org/abs/2408.08921 — Surveys graph-based RAG, including how GraphRAG uses structure among entities.
