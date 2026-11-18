---
status: draft
tags:
  - multimodal
  - contrastive learning
  - zero-shot learning
  - embeddings
aliases:
  - CLIP
  - Contrastive Language–Image Pre-training
  - 對比語言—影像預訓練
  - 零樣本分類
---

# CLIP

CLIP (Contrastive Language–Image Pre-training) learns an image encoder and a text encoder whose outputs share one embedding space. Trained on 400 million web image–text pairs, it can perform downstream classification without task-specific labelled fine-tuning by comparing images with class descriptions. Here zero-shot describes the adaptation protocol, not a guarantee that web pre-training contained no overlapping images. The method is the modality-alignment member of the family on the parent page, [Embeddings and Representation Learning](index.md).

## Problem

Image classifiers trained on fixed label sets, such as ImageNet, learn only the categories in their training labels, and new categories require new labelled data. Radford et al. (2021) asked whether a model could learn visual concepts from the natural-language text that already accompanies images on the web, and then transfer to new tasks by describing the task in words.

## Core idea

For a batch of `N` image–text pairs, CLIP must identify which of the `N × N` possible pairings actually occurred. The image and text embeddings are normalised, and the contrastive loss favours the paired captions/images over other batch entries. Other entries act as negatives, even though some may also be semantically compatible. The objective is applied in both directions, from image to text and from text to image, which makes the loss symmetric.

Because the loss compares a pair against every other pair in the batch, the negatives come for free: no separate negative set is needed. The similarities are multiplied by a learned inverse temperature. Section 2.5 reports an initial temperature of 0.07 and a cap of 100 on the multiplicative logit scale during training.

## Equation and algorithm

The paper gives its pseudocode for the core step. With row-normalised image and text embedding matrices \(I_e,T_e\in\mathbb R^{N\times d}\), the logits are

\[
S=I_eT_e^\top\exp(t)=I_eT_e^\top/\tau,\qquad t=\log(1/\tau).
\]

Thus \(t\) is the learned **log inverse-temperature**, or logit scale. The symmetric loss is \(L=(L_{I\to T}+L_{T\to I})/2\). The image-to-text term classifies each image over the texts in its batch, and the text-to-image term does the reverse.

Zero-shot classification proceeds in three steps. The names of the classes are passed through the text encoder to give one embedding per class. Each image embedding is compared with these class embeddings by cosine similarity, scaled by the inverse temperature and normalised with a softmax. The class with the highest probability is the prediction. The default prompt template, "A photo of a {label}", adds about 1.3 percentage points of accuracy on ImageNet in the paper. Ensembling 80 context prompts adds about 3.5 further percentage points (Section 3.1.4).

## Results

The paper reports zero-shot top-1 accuracy on ImageNet. Its **ViT-L/14@336px** model reaches **76.2%**, compared with 11.5% for the earlier Visual N-Grams method ([Table 1 and Section 2.5](https://arxiv.org/abs/2103.00020)). The authors describe this as matching the original supervised ResNet-50; it is not a comparison against the best later ImageNet systems. The authors also report that prompt engineering and ensembling together raise ImageNet accuracy by almost five points. The training set is the paper's own 400-million-pair dataset, called WIT (WebImageText).

## Limitations

- **Behind supervised baselines.** Zero-shot CLIP is competitive with a simple supervised baseline on many datasets but is not state of the art overall. The authors estimate that roughly a thousand-fold increase in compute would be needed to reach the 2021 ImageNet state of the art by extrapolating their observed scaling trend; this is an estimate, not a demonstrated result.
- **Specialised and abstract tasks.** Fine-grained performance varies: Flowers102 and FGVCAircraft trail the paper's linear classifier on ResNet-50 features, while Stanford Cars and Food101 outperform that baseline (Section 3.1.5). Abstract tasks such as counting and new tasks such as nearest-car distance estimation can be near chance; this does not mean all fine-grained classification is near chance.
- **Out-of-distribution data.** It reaches only about 88% on handwritten MNIST digits, which a logistic regression on raw pixels outperforms.
- **Closed set.** It chooses among the concepts it is given and cannot generate new outputs, unlike a captioning model.
- **Social bias.** Training on unfiltered web pairs leads to learned social biases.
- **Evaluation caveats.** Validation sets were queried repeatedly during development, and the evaluation suite was co-adapted with CLIP's development.

## References

### Seminal papers

- Radford, A., Kim, J. W., Hallacy, C., Ramesh, A., Goh, G., Agarwal, S., Sastry, G., Askell, A., Mishkin, P., Clark, J., Krueger, G. & Sutskever, I. (2021). *Learning Transferable Visual Models From Natural Language Supervision*. arXiv. https://arxiv.org/abs/2103.00020 — Defines the contrastive pre-training objective, the WIT dataset and the zero-shot ImageNet results on this page.
- Oord, A. van den, Li, Y. & Vinyals, O. (2018). *Representation Learning with Contrastive Predictive Coding*. arXiv. https://arxiv.org/abs/1807.03748 — Introduces contrastive predictive coding, a probabilistic contrastive loss that uses negative samples to make learning tractable.

### Surveys and textbooks

- Bengio, Y., Courville, A. & Vincent, P. (2012). *Representation Learning: A Review and New Perspectives*. arXiv. https://arxiv.org/abs/1206.5538 — Background on learned representations and their transfer to new tasks.

### Articles and documentation

- Khosla, P. et al. (2020). *Supervised Contrastive Learning*. arXiv. https://arxiv.org/abs/2004.11362 — Uses class labels in a batch contrastive loss, showing how the pull-and-push objective generalises beyond pairs.
- Wang, T. & Isola, P. (2020). *Understanding Contrastive Representation Learning through Alignment and Uniformity on the Hypersphere*. arXiv. https://arxiv.org/abs/2005.10242 — Explains the alignment and uniformity properties that a normalised contrastive embedding such as CLIP's should have.
