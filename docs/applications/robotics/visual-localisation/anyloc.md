---
status: complete
last_reviewed: 2026-10-28
related:
  - applications/robotics/visual-localisation
tags:
  - robotics
  - place recognition
  - foundation model
aliases:
  - AnyLoc
  - 通用視覺地點辨識
---

# AnyLoc

AnyLoc, introduced by Keetha, Mishra, Karhade, Jatavallabhula, Scherer, Krishna and Garg (2023), is a place recognition method built from a frozen self-supervised foundation model. It takes intermediate DINOv2 features, aggregates them into one descriptor per image without training an encoder, and retrieves matching places from a database. The paper's claim is that one general descriptor works across very different environments. The parent subtopic is [Visual Localisation](index.md).

## Overview

AnyLoc has no encoder training step. A frozen DINOv2 backbone produces dense local features, and an unsupervised clustering-based aggregation pools them into one vector per image. Retrieval is then a nearest-neighbour search. The contribution is a choice of features, the layer they come from, and how they are aggregated, rather than a new network.

## Problem

Place recognition methods are usually trained on one kind of scene, such as city streets, and their accuracy drops in other settings. Training a new encoder for every environment is costly, and a robot may not have the labelled data to do so. The paper asks whether a general foundation model can serve as one encoder across domains, and which layer and aggregation give the best results.

## Core idea

Use the features of a frozen self-supervised model, taken from a deep intermediate layer, and aggregate them without labels. The aggregation turns a rich set of local features into a compact descriptor. The authors also group the database by environment type, so that each group gets its own vocabulary for the aggregation.

## How it works

1. Pass the image through a frozen DINOv2 backbone and keep the features of one chosen layer and facet. The paper uses the value facet of the largest ViT-G/14 model, at layer 31.
2. Assign each local feature to the nearest cluster centre $c_k$ of a vocabulary of $K$ centres. The centres come from k-means over the database features, so no labels are used.
3. Aggregate with VLAD, which sums the residuals of the features assigned to each centre:

$$
v_k = \sum_{x_i \in \text{cluster } k} \left(x_i - c_k\right), \qquad d = \left[v_1, \dots, v_K\right]
$$

   The concatenated vector $d$ is normalised and stored with the place it came from.
4. For a query image, compute its descriptor and retrieve the stored descriptors with the smallest distance.

The vocabulary is built per domain. The authors project global DINOv2 descriptors with PCA and separate the database into domains such as urban, indoor, aerial, subterranean, degraded and underwater. The paper's VLAD configuration uses 32 clusters.

## Results

The paper evaluates recall at one (R@1) across many benchmarks. Some of the numbers that bear on the claim:

| Dataset | AnyLoc-VLAD-DINOv2 | MixVPR | CosPlace | NetVLAD |
|---|---|---|---|---|
| Baidu Mall (indoor) | 75.2 | 64.4 | 41.6 | 53.1 |
| Gardens Point | 95.5 | 91.5 | 74.0 | 58.5 |
| Hawkins (unstructured) | 65.2 | 25.4 | 31.4 | 34.8 |

The paper also reports that intermediate-to-deep layers give the best results, and that the gain from the larger backbone is uneven: on Urban, ViT-G improves recall from 82.6 to 92.3 over ViT-B, but on Underwater it is slightly lower. The abstract summarises the advantage as performance up to four times higher than existing methods in some settings. Those figures depend on the benchmark, so the table above should be read with the paper's full results in hand.

## Limitations

- Retrieval does not estimate geometry, so a match still needs verification before a robot relies on it.
- The per-domain vocabulary assumes that the domain of the data can be identified, which the paper does with a PCA-based procedure over the database.
- The best results use the largest backbone, and the gains from scaling are not uniform across domains.
- The evaluation is retrieval recall. Closed-loop robot performance is outside the paper's scope.

## Connections

- [Visual Localisation](index.md) places AnyLoc next to the trained alternative, EigenPlaces.
- [DINOv2](../../../theory/paradigms/self-supervised/non-contrastive-methods/dinov2.md) describes the frozen backbone that AnyLoc uses.
- [EigenPlaces](eigenplaces.md) represents the approach of training for viewpoint robustness.

## Open questions

- Whether the aggregation can be made cheap enough for real-time use on small platforms without losing accuracy.
- How much of the gain survives when the domain of a new environment is not one of the groups the vocabulary was built for.

## References

- Keetha, N., Mishra, A., Karhade, J., Jatavallabhula, K. M., Scherer, S., Krishna, M. & Garg, S. (2023). *AnyLoc: Towards Universal Visual Place Recognition*. arXiv:2308.00688. https://arxiv.org/abs/2308.00688 — The source of the frozen-feature method, the domain-specific vocabularies and the benchmark tables quoted above.
- Oquab, M., Darcet, T., Moutakanni, T., et al. (2023). *DINOv2: Learning Robust Visual Features without Supervision*. arXiv:2304.07193. https://arxiv.org/abs/2304.07193 — The self-supervised backbone whose features AnyLoc uses without finetuning.
- Berton, G., Trivigno, G., Caputo, B., & Masone, C. (2023). *EigenPlaces: Training Viewpoint Robust Models for Visual Place Recognition*. ICCV 2023. https://openaccess.thecvf.com/content/ICCV2023/papers/Berton_EigenPlaces_Training_Viewpoint_Robust_Models_for_Visual_Place_Recognition_ICCV_2023_paper.pdf — The trained alternative for viewpoint robustness, used for comparison.
- Zaffar, M., Garg, S., Milford, M., et al. (2021). *VPR-Bench: An open-source visual place recognition evaluation framework with quantifiable viewpoint and appearance change*. International Journal of Computer Vision (2021). https://doi.org/10.1007/s11263-021-01469-5 — The benchmark that separates viewpoint and appearance change, relevant to how AnyLoc's robustness should be read.
- Silwal, S., Yadav, K., Wu, T., et al. (2024). *What do we learn from a large-scale study of pre-trained visual representations in sim and real environments?* arXiv:2310.02219. https://arxiv.org/abs/2310.02219 — Evidence that pretrained visual encoders transfer from simulation to a real robot, the setting in which frozen features matter most.
