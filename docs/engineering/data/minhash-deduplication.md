---
tags:
- engineering
- data
aliases:
- MinHash 去重
---

# MinHash Deduplication

MinHash deduplication finds near-duplicate documents in a corpus too large to compare pairwise. It represents each document as a compact signature whose agreement rate estimates how much two documents overlap, then uses locality-sensitive hashing to find the likely pairs without checking every pair. It is the standard tool for removing repeated web text before language-model pre-training.

## Overview

Exact deduplication, which hashes whole documents, misses the common case where a page is copied with a changed header, a different date or a few edited words. Those near-copies still teach a model the same text many times. Comparing every pair of documents is quadratic, which is impossible for billions of documents. MinHash turns the comparison into a short signature and a hash lookup, so the cost grows roughly with the corpus size.

## Key concepts

- **Shingles**: the set of overlapping word or character n-grams in a document. Two documents are compared by the overlap of their shingle sets.
- **Jaccard similarity**: the size of the intersection of two shingle sets divided by the size of their union. A value near 1 means near-duplicates.
- **MinHash signature**: for each of many hash functions, keep the smallest hash value over a document's shingles. The fraction of positions where two signatures agree is an unbiased estimate of Jaccard similarity.
- **Locality-sensitive hashing (LSH)**: split each signature into bands and hash each band. Documents that share a band land in the same bucket and become candidate pairs. The number of bands and rows sets the similarity threshold at which pairs are likely to be found.

## How it works

Each document is shingled, reduced to a signature, and bucketed by LSH. Candidate pairs are then checked more precisely and one document of each duplicate cluster is kept.

```mermaid
flowchart LR
  D[Documents] --> S[Shingles]
  S --> M[MinHash signatures]
  M --> B[LSH bands and buckets]
  B --> C[Candidate pairs]
  C --> V[Verify similarity above threshold]
  V --> K[Keep one document per cluster]
```

## Key methods

The method is MinHash signatures combined with LSH banding, followed by a similarity threshold and a cluster-level choice of which copy to keep. Broder (1997) introduced the resemblance measure based on min-wise hashing of shingles. Lee et al. (2022) showed that removing near-duplicates from training corpora changes how language models reproduce their training data, which made the method a standard step in pre-training pipelines.

## Results

Lee et al. (2022) report that removing near-duplicates reduces how often models regenerate training sequences verbatim, and that duplicated text in the training data is common in standard corpora. Later large-corpus pipelines, such as DataComp-LM, list deduplication among the curation choices they compare, so its effect is measured together with filtering and mixing rather than alone.

## Limitations

- **Threshold choice**: a high threshold keeps near-copies; a low one removes legitimate repeated text such as licence headers, boilerplate and quotations.
- **Scope**: deduplication across a whole corpus, across splits, or within a single source gives different results, and the right choice depends on the goal.
- **Semantic copies are missed**: paraphrases and translations have low shingle overlap, so MinHash does not remove them.
- **Cost at scale**: signatures and buckets must be computed and stored for every document, which requires distributed processing.

## Open questions

- Does removing near-duplicates help more than it hurts when a corpus is trained for several epochs?
- How should deduplication be combined with data mixing, so that rare high-quality sources are not removed along with web copies?
- When is semantic deduplication worth its extra cost over MinHash?

## References

### Seminal papers

- Broder, A. Z. (1997). *On the resemblance and containment of documents*. https://www.cs.princeton.edu/courses/archive/spring13/cos598C/broder97resemblance.pdf — Introduces resemblance between documents, estimated from min-wise hashes of their shingles.

### Related work

- Lee, K. et al. (2021). *Deduplicating Training Data Makes Language Models Better*. arXiv:2107.06499. https://arxiv.org/abs/2107.06499 — Shows that near-duplicates in pre-training corpora increase verbatim regeneration of training text and that removing them helps.
- Li, J. et al. (2024). *DataComp-LM: In search of the next generation of training sets for language models*. arXiv:2406.11794. https://arxiv.org/abs/2406.11794 — A benchmark for data curation in which deduplication is one of the strategies compared with filtering and mixing.
- Soldaini, L. et al. (2024). *Dolma: an Open Corpus of Three Trillion Tokens for Language Model Pretraining Research*. arXiv:2402.00159. https://arxiv.org/abs/2402.00159 — An open corpus of three trillion tokens for pre-training research, built with a documented curation pipeline.
- Penedo, G. et al. (2024). *The FineWeb Datasets: Decanting the Web for the Finest Text Data at Scale*. arXiv:2406.17557. https://arxiv.org/abs/2406.17557 — A large web-text corpus and the filtering pipeline that produces it.
