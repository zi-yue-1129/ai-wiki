---
status: draft
last_reviewed: 2026-10-28
related:
  - engineering/rag
  - applications/search-and-information-retrieval
tags:
  - retrieval
  - large language models
aliases:
  - OpenScholar
  - 文獻綜整
  - 科學文獻檢索增強模型
---

# OpenScholar (Asai et al. 2024)

OpenScholar is a retrieval-augmented language model that answers questions about the scientific literature. It searches a datastore of 45 million open-access papers and writes long answers with citations. Akari Asai and colleagues reported it in 2024. It is the literature-review method on the parent page [AI for AI Research](../index.md).

## Overview

Synthesising the literature of a field is slow, and language models often invent references. The authors report that GPT-4o hallucinated citations 78 to 90% of the time in their experiments (Asai et al., 2024). Earlier systems had also tried to answer questions over papers. PaperQA (Lála et al., 2023) is an example, and the broader idea of grounding generated text in retrieved sources is known as [retrieval-augmented generation](../../../engineering/rag/index.md) (Lewis et al., 2020). Citation quality as a measurable property of generated text was studied by Gao et al. (2023).

OpenScholar's answers are built from retrieved passages, so every claim can point to a source the system actually found. This is a different problem from [search and information retrieval](../../search-and-information-retrieval/index.md) in general, because the output is a synthesis, not a ranked list of documents.

## Key concepts

- **Datastore**: the collection of 45 million open-access papers, indexed for search.
- **Retriever**: the component that finds candidate passages for a question.
- **Citation accuracy**: whether each cited passage supports the sentence it is attached to. [RAG](../../../engineering/rag/index.md) systems are often judged on this.
- **Self-feedback loop**: the model reviews its own draft and may retrieve more evidence before it revises the answer.
- **ScholarQABench**: the benchmark that the authors built to test literature search and synthesis.

## How it works

The system follows a retrieve, draft and revise cycle:

1. The question goes to the retriever, which returns candidate passages from the datastore.
2. The language model reads the passages and drafts an answer, attaching each claim to specific passages.
3. In the self-feedback step, the model critiques its draft and may retrieve further passages to strengthen weak claims.
4. The revised answer is returned with its citations.

The authors describe the retriever, datastore and feedback loop together as an inference loop. They also show that the same loop can improve an existing model: OpenScholar-GPT4o raised GPT-4o's correctness by 12% (Asai et al., 2024).

## Results

On ScholarQABench, which contains 2,967 expert-written queries and 208 long-form answers across computer science, physics, neuroscience and biomedicine, OpenScholar-8B outperforms GPT-4o by 5% and PaperQA2 by 7% in correctness. The authors note that OpenScholar-8B is a smaller, open model. Its citation accuracy is on par with that of human experts.

In human evaluation, experts preferred OpenScholar-8B responses over expert-written ones 51% of the time, and OpenScholar-GPT4o responses 70% of the time. The comparable figure for GPT-4o was 32%.

## Limitations

- **Open-access coverage.** The datastore holds only open-access papers, so paywalled work is missing from the synthesis. Readers should check whether the omitted work changes the picture.
- **Citation is not correctness.** A correct citation shows that a passage supports a sentence. It does not show that the cited study is sound, representative or current.
- **Benchmark fit.** The queries were written by experts for the benchmark. They may not match the questions a particular researcher asks.
- **Balance depends on the literature.** A synthesis reflects what has been published and indexed. Where fields have publication bias, the answer inherits it.

## Open questions

- Can systems like this weigh conflicting studies, rather than only citing them?
- How should the datastore be kept current as the literature grows?
- Does reliance on synthesised reviews reduce how often researchers read primary sources? Messeri and Crockett (2024) raise this concern about AI-assisted science in general.

## References

### Seminal papers

- Asai, A. et al. (2024). OpenScholar: Synthesizing Scientific Literature with Retrieval-augmented LMs. arXiv. https://arxiv.org/abs/2411.14199 — Retrieval-augmented model that writes citation-backed answers from 45 million open-access papers, with a new benchmark.
- Lewis, P. et al. (2020). Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. arXiv. https://arxiv.org/abs/2005.11401 — Introduces retrieval-augmented generation, which lets a generator draw on documents fetched by a retriever.

### Articles and documentation

- Gao, T. et al. (2023). Enabling Large Language Models to Generate Text with Citations. arXiv. https://arxiv.org/abs/2305.14627 — Studies how to make language-model outputs cite supporting evidence, and how to measure citation quality.
- Lála, J. et al. (2023). PaperQA: Retrieval-Augmented Generative Agent for Scientific Research. arXiv. https://arxiv.org/abs/2312.07559 — Agent that retrieves and assesses full-text scientific articles to answer questions with citations.
- Messeri, L. & Crockett, M. J. (2024). Artificial intelligence and illusions of understanding in scientific research. *Nature*. https://doi.org/10.1038/s41586-024-07146-0 — Commentary on how AI tools can give researchers an illusion of understanding, relevant to trusting synthesised literature.
