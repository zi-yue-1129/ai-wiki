---
tags:
- engineering
- data
---

# TinyStories

TinyStories is a synthetic dataset of short children's stories, generated with a restricted vocabulary and simple structure, and used to train very small language models. It showed that coherent, fluent language can emerge at small scale when the training data is controlled.

## Overview

Language models were assumed to need enormous size before they produced coherent text. TinyStories tested whether the simplicity and consistency of the training data matter as much as scale. The authors generated many stories that a young child could understand, specifying the words, themes and story structure in the prompt. Small models trained on this data wrote grammatical, consistent stories, which larger models trained on general web text had not reliably matched at that size.

## Key concepts

- **Restricted vocabulary**: the generation prompts limit the words used, so the training text is simple but internally consistent.
- **Story structure**: stories follow a simple plot pattern, which makes it easy for a small model to learn coherent sequences.
- **Controlled generation**: generation is steered by a list of features, such as vocabulary, theme and length, so the dataset covers the space the authors chose.

## How it works

A large language model writes stories from prompts that specify the required words and the story's features. The stories are collected into a corpus, which is used to train a small transformer with standard next-token prediction. The trained models are then evaluated by how fluent, consistent and grammatical their generated stories are.

```mermaid
flowchart LR
  P[Prompt: vocabulary, theme, features] --> G[Large model writes stories]
  G --> D[Story corpus]
  D --> T[Train small model]
  T --> E[Judge fluency and consistency]
```

## Key methods

The method is the controlled data-generation pipeline. The study's main evidence comes from comparing small models trained on this corpus against the expectation that small models produce only incoherent text.

## Results

The paper reports that models with only a few million to tens of millions of parameters produce fluent, consistent stories when trained on this dataset. Evaluations rely in part on language-model judges and sampled outputs, so the paper's own description of the evaluation should be read carefully.

## Limitations

- **Narrow domain**: the stories are simple and the vocabulary is restricted, so the results do not show general knowledge or reasoning.
- **Generator dependence**: the quality of the corpus depends on the large model that wrote it.
- **Evaluation**: judging fluency at small scale depends on the metrics and judges chosen.

## Open questions

- Which features of the data drive coherence: vocabulary, structure, or consistency across a story?
- Can the same controlled approach yield useful small models for domains beyond children's stories?

## References

### Seminal papers

- Eldan, R. & Li, Y. (2023). *TinyStories: How Small Can Language Models Be and Still Speak Coherent English?* https://arxiv.org/abs/2305.07759 — Generates a controlled dataset of simple stories and shows that very small models can produce coherent English when trained on it.

### Related work

- Gunasekar, S. et al. (2023). *Textbooks Are All You Need*. https://arxiv.org/abs/2306.11644 — Applies the same idea of choosing training data for quality, but for code and textbook-style material.
- Wang, Y. et al. (2023). *Self-Instruct: Aligning Language Models with Self-Generated Instructions*. https://arxiv.org/abs/2212.10560 — Uses generated data for instruction tuning, a different target from the story-writing corpus here.
- Liu, Z. et al. (2024). *Best Practices and Lessons Learned on Synthetic Data*. https://arxiv.org/abs/2404.07503 — Discusses how generation controls and evaluation affect what a synthetic corpus teaches a model.
- Shumailov, I. et al. (2024). *AI models collapse when trained on recursively generated data*. Nature, 631. https://doi.org/10.1038/s41586-024-07566-y — Notes the diversity risk that controlled generation can reduce or increase when models train on model-written text.
