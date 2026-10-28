---
related:
- engineering/vector-databases
- engineering/hardware
tags:
- engineering
- retrieval
- vector search
- quantisation
aliases:
- IVF-PQ
- FAISS IVF-PQ
---

# IVF-PQ in FAISS

IVF-PQ combines an inverted file index with product quantisation. It stores compressed vectors, so that very large collections fit in GPU or server memory, and it scans only a few cells per query. The method is implemented in the FAISS library, described by Johnson, Douze and Jégou (2017).

## Overview

Full-precision vectors take a lot of memory, and scanning them takes time proportional to the collection size. IVF-PQ reduces both. The inverted file splits the collection into cells, so a query looks at only the nearest few. Product quantisation shrinks each stored vector to a short code, and distances are estimated from that code with lookup tables.

## Key concepts

- **Coarse quantiser**: a set of centroids, typically learned with k-means, that assigns each vector to a cell.
- **Inverted file (IVF)**: a list of vectors for each cell. A query probes a fixed number of cells, which is the main speed setting.
- **Product quantisation (PQ)**: the vector is split into sub-vectors, and each is replaced by the index of its nearest centroid from a small codebook.
- **Residual encoding**: the vector is encoded relative to its cell centroid, so the codes describe the local offset rather than the whole vector.

## How it works

```mermaid
flowchart LR
  X[Query vector] --> C[Coarse quantiser picks nearest cells]
  C --> P[Scan only the probed cells]
  P --> L[Estimate distances with PQ lookup tables]
  L --> R[Re-rank top candidates with exact distances]
```

## Key ideas

- **Problem:** storing and scanning full-precision vectors for billions of items exceeds the memory and time of a single GPU or server.
- **Core idea:** split the collection into $n_{\text{list}}$ cells with a coarse quantiser (inverted file, IVF), so a query only scans the few cells nearest to it. Inside each cell, compress each vector with product quantisation (PQ): split it into $m$ sub-vectors and store the index of the nearest centroid for each, using one byte per sub-vector.
- **Equation or algorithm:** distance to a compressed vector is approximated as $\lVert q - x \rVert^2 \approx \sum_{j=1}^{m} \lVert q_j - c_{j}(x_j) \rVert^2$, where $c_j(x_j)$ is the centroid stored for sub-vector $j$. Precomputed lookup tables make each term a table read.
- **Results:** the paper reports billion-scale similarity search on GPUs, with the trade-off between memory, speed and recall controlled by $m$ and the number of probed cells.
- **Limitations:** PQ error limits recall, so systems often re-rank the top candidates with exact distances. Training the quantiser needs representative data.

## Trade-offs

- **Memory against recall**: fewer bytes per vector and fewer probed cells save memory and time, but each lowers recall.
- **Training cost**: the coarse quantiser and codebooks must be trained on data that represents the collection, and retraining is needed when the distribution shifts.
- **Updates**: new vectors can be added to existing cells, but a large change in content calls for retraining.

## Open questions

- How often should the quantiser be retrained as the data distribution drifts, and how can that be detected?
- How much recall is lost on rare queries that fall between cells?

## References

- Johnson, J., Douze, M. & Jégou, H. (2017). *Billion-scale similarity search with GPUs*. arXiv:1702.08734. https://arxiv.org/abs/1702.08734 — Describes FAISS and billion-scale GPU search with inverted files and product quantisation.
- Malkov, Y. A. & Yashunin, D. A. (2016). *Efficient and Robust Approximate Nearest Neighbor Search Using Hierarchical Navigable Small World Graphs*. arXiv:1603.09320. https://arxiv.org/abs/1603.09320 — Presents the graph-based alternative to inverted-file indexes.
- Guo, R. et al. (2019). *Accelerating Large-Scale Inference with Anisotropic Vector Quantization*. arXiv:1908.10396. https://arxiv.org/abs/1908.10396 — Proposes a quantisation loss that refines the product-quantisation codes used in IVF-style indexes.
- Aumüller, M., Bernhardsson, E. & Faithfull, A. (2018). *ANN-Benchmarks: A Benchmarking Tool for Approximate Nearest Neighbor Algorithms*. arXiv:1807.05614. https://arxiv.org/abs/1807.05614 — Compares the recall and speed of quantised and graph-based indexes on common datasets.
- Thakur, N. et al. (2021). *BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models*. NeurIPS 2021 Datasets and Benchmarks. https://arxiv.org/abs/2104.08663 — Evaluates retrievers across 18 datasets, where the index's recall directly affects the final quality.
