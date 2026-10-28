---
status: draft
last_reviewed: 2026-10-28
related:
- theory/model-compression
- theory/model-compression/pruning
- theory/model-compression/quantisation
tags:
- model compression
- pruning
- quantisation
- Huffman coding
- embedded inference
aliases:
  - Deep Compression
  - Han et al. 2016
  - 深度壓縮
---

# Deep Compression

Deep Compression is a three-stage pipeline that combines pruning, codebook quantisation and Huffman coding to shrink a trained network's storage. Han, Mao and Dally (2016) introduced it for embedded deployment, where a single technique did not reduce a network to the size the hardware could hold. It is a clear example of [composition](../index.md): each stage removes a different kind of redundancy, and the stages are applied in sequence. The stages themselves are covered on the [pruning](../pruning/index.md) and [quantisation](../quantisation/index.md) pages.

## Problem

A trained network can be too large to store on an embedded device, and the usual single technique, such as pruning alone or quantisation alone, does not reach the required size without unacceptable loss of accuracy. Storage is the constraint here, so the target is the number of bits needed to represent the network rather than its speed.

## Core idea

Apply three stages in order. First, prune connections whose weights are small, then retrain the remaining weights to recover accuracy. Second, cluster the surviving weights into a small number of shared values, a codebook, and store each weight as an index into that codebook. Third, entropy-code the indices with Huffman coding, so that frequent indices use fewer bits. Each stage removes a different kind of redundancy: the zeros, the number of distinct values, and the unequal frequency of the remaining values.

## Equation or algorithm

The pruning stage keeps a weight \(w\) when its magnitude exceeds a threshold, \(|w| > t\), and sets the rest to zero. Retraining then updates only the surviving connections.

The quantisation stage clusters the surviving weights into \(k\) centroids, usually with k-means. Each weight is replaced by the index \(c_i\) of its nearest centroid, so a layer with \(n\) weights needs \(n \log_2 k\) bits for its indices plus a small table of centroids. The centroids are then fine-tuned with the gradient averaged over the weights that share each one.

The final stage applies Huffman coding to the indices. Its expected code length is close to the entropy of the index distribution, which is lower than \(\log_2 k\) when some centroids are used much more often than others.

## Results

Han et al. (2016) report that the pipeline reduces the storage requirement of neural networks by 35 to 49 times without affecting their accuracy. In their setting the reduction is in stored size rather than in run-time speed, and the figures apply to the networks and datasets they studied.

## Limitations

The gains are mainly in storage. Sparse and codebook-based models need special hardware or software to run faster, and dense accelerators may see little speed-up from the zeros. The pipeline also needs retraining after each pruning and quantisation step, which is expensive for very large models, and its later stages are less useful once the model is already compact.

## Open issues and related variants

- **Speed versus size.** A smaller file does not imply a faster model. Whether the zeros and shared values are exploited at run time depends on the hardware the model is deployed on, as the [overview](../index.md) explains.
- **Post-training versions.** Retraining is the costly part for large models. Later one-shot methods, such as those in the [one-shot LLM pruning](../pruning/one-shot-llm-pruning/index.md) family, avoid most of it.
- **Related:** the codebook step is a form of vector quantisation, which Gong et al. (2014) applied to the dense layers of CNNs.

## Connections

Deep Compression links the two largest families of the [model compression](../index.md) overview, [pruning](../pruning/index.md) and [quantisation](../quantisation/index.md). Its storage format is most relevant to [on-device and edge AI](../../../engineering/on-device-edge/index.md), where model size limits deployment.

## References

### Seminal papers

- Han, S., Mao, H., Dally, W. J. (2016). *Deep Compression: Compressing Deep Neural Networks with Pruning, Trained Quantization and Huffman Coding*. ICLR. https://arxiv.org/abs/1510.00149 — Combines pruning, codebook quantisation and Huffman coding, reporting 35 to 49 times storage reduction without affecting accuracy.
- Han, S., et al. (2015). *Learning both Weights and Connections for Efficient Neural Networks*. arXiv:1506.02626. https://arxiv.org/abs/1506.02626 — Prunes connections and retrains the survivors, shrinking AlexNet and VGG-16 without loss of accuracy.
- Gong, Y., et al. (2014). *Compressing Deep Convolutional Networks using Vector Quantization*. arXiv:1412.6115. https://arxiv.org/abs/1412.6115 — Reports a clear gain of vector quantisation over matrix factorisation for compressing the most storage-demanding dense layers of CNNs.

### Surveys and textbooks

- Hoefler, T., et al. (2021). *Sparsity in Deep Learning: Pruning and Growth for Efficient Inference and Training in Neural Networks*. arXiv:2102.00554. https://arxiv.org/abs/2102.00554 — A broad survey of sparsity methods across training and inference.

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Gale, T., Elsen, E., Hooker, S. (2019). *The State of Sparsity in Deep Neural Networks*. arXiv:1902.09574. https://arxiv.org/abs/1902.09574 — Reports that simple magnitude pruning achieves comparable or better results than complex sparsity techniques, which perform inconsistently.
