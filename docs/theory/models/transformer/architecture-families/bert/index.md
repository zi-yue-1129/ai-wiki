---
status: draft
last_reviewed: 2026-10-28
tags:
  - self-supervised learning
  - transfer learning
aliases:
  - BERT
  - Bidirectional Encoder Representations from Transformers
  - 雙向編碼器表示
---

# BERT: bidirectional encoder pre-training (Devlin et al., 2018)

BERT is an encoder-only Transformer pre-trained to recover masked words from both their left and right context, and then fine-tuned with one added output layer. It is the landmark encoder-only member of the [Transformer architecture families](../index.md).

## Overview

Before BERT, pre-trained language models were either feature-based or left-to-right. ELMo (Peters et al., 2018) ran two separate left-to-right and right-to-left LSTMs and used their outputs as extra features. OpenAI GPT fine-tuned an entire left-to-right Transformer. BERT's authors argued that the left-to-right constraint is harmful for token-level tasks such as question answering, where the answer depends on context from both sides.

BERT keeps the bidirectional self-attention of the encoder and pre-trains it with a masked objective instead of next-token prediction. The same network is then fine-tuned on each downstream task.

BERT is one member of the [architecture families](../index.md) discussed on the parent page, alongside the decoder-only [GPT-3](../../../llm/gpt-3-few-shot/index.md) and the encoder–decoder [T5](../t5/index.md). The masked objective is a special case of [masked prediction](../../../../paradigms/self-supervised/masked-prediction/index.md), and [DistilBERT](../../../../model-compression/knowledge-distillation/response-based/distilbert/index.md) shrinks it. The wider context is [Transformers & Attention](../../index.md).

## Key concepts

- **WordPiece tokens.** Text is split into sub-word units. A special `[CLS]` token starts each input, and `[SEP]` separates two sentences packed into one sequence.
- **Masked language model (MLM).** The objective that hides some tokens and asks the model to recover them.
- **Next-sentence prediction (NSP).** A binary task on sentence pairs: is sentence B the sentence that follows A in the corpus, or a random one?
- **Fine-tuning.** Adding one output layer to the pre-trained network and training all parameters on labelled data.

## How it works

The pre-training procedure, as described by Devlin et al. (2018):

1. Build each training example from two text spans, A and B. Half the time B is the true next sentence; half the time it is a random one.
2. Choose 15% of the token positions at random. Replace 80% of them with `[MASK]`, 10% with a random token, and leave 10% unchanged.
3. Pass the sequence through the bidirectional Transformer. Use the hidden vectors at the chosen positions for the MLM loss, and the `[CLS]` vector for the NSP loss.
4. Minimise the sum of the two losses:

$$
\mathcal{L} = \mathcal{L}_{\text{MLM}} + \mathcal{L}_{\text{NSP}}
$$

5. For fine-tuning, add one output layer (on `[CLS]` for sentence tasks, or on each token for tagging and question answering) and train all weights.

The two model sizes in the paper are BERT-Base, with 12 layers, hidden size 768, 12 attention heads and 110 million parameters, and BERT-Large, with 24 layers, hidden size 1024, 16 heads and 340 million parameters.

## Results

The paper's headline results come from BERT-Large. In the abstract, BERT pushes the GLUE score to 80.5%, MultiNLI accuracy to 86.7%, SQuAD v1.1 test F1 to 93.2 and SQuAD v2.0 test F1 to 83.1, each a clear gain over the earlier state of the art.

The ablation on the development sets (Table 5 of the paper, BERT-Base) isolates the two choices. Changing the objective from bidirectional MLM to a left-to-right language model without NSP lowers MRPC accuracy from 86.7 to 77.5 and SQuAD F1 from 88.5 to 77.8. Dropping NSP alone lowers SQuAD F1 from 88.5 to 87.9, and MNLI accuracy from 84.4 to 83.9.

## Limitations

- **Train–test mismatch.** The `[MASK]` token never appears at fine-tuning time. The 10% random and 10% unchanged replacements reduce, but do not remove, this gap.
- **Less signal per token.** Only about 15% of positions give a training signal in each example, which makes pre-training costly. Later work examined this directly: ELECTRA (Clark et al., 2020) trains a discriminator to detect replaced tokens, and reports better sample efficiency.
- **Not a generator.** A bidirectional encoder does not produce text left to right, so it is not used for open-ended generation.
- **Undertrained recipe.** RoBERTa (Liu et al., 2019) re-examined BERT's pre-training choices, including its training budget, and reported that BERT was significantly undertrained.

## Open questions

- Is masked prediction the best objective for understanding text, or does a discriminative objective do better per unit of compute?
- How much does NSP contribute? In the ablation above, removing it lowered the score on every dev task measured, by much more on QNLI than on MRPC or SST-2, and later replication studies re-examined the whole pre-training recipe (Liu et al., 2019).
- How far do masked-word models resemble human language processing? Caucheteux and King (2022) show correlation, not shared mechanism.

## References

### Seminal papers

- Devlin, J., et al. (2018). *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding*. arXiv; NAACL 2019. https://arxiv.org/abs/1810.04805 — The original paper, introducing the masked language model, next-sentence prediction and fine-tuning recipe.
- Peters, M. E., et al. (2018). *Deep contextualized word representations*. arXiv; NAACL 2018. https://arxiv.org/abs/1802.05365 — ELMo, the feature-based bidirectional language model that BERT's authors contrast with their approach.
- Vaswani, A., et al. (2017). *Attention Is All You Need*. NeurIPS. https://arxiv.org/abs/1706.03762 — The Transformer encoder that BERT stacks and trains bidirectionally.

### Surveys and textbooks

- Liu, Y., et al. (2019). *RoBERTa: A Robustly Optimized BERT Pretraining Approach*. arXiv. https://arxiv.org/abs/1907.11692 — A replication study of BERT pre-training that measures the effect of hyperparameters and data size.

### Articles and documentation

- Clark, K., et al. (2020). *ELECTRA: Pre-training Text Encoders as Discriminators Rather Than Generators*. arXiv; ICLR 2020. https://arxiv.org/abs/2003.10555 — An alternative to masked modelling that trains a discriminator to detect replaced tokens, and is more sample-efficient.
- Caucheteux, C. & King, J.-R. (2022). Brains and algorithms partially converge in natural language processing. *Communications Biology*. https://doi.org/10.1038/s42003-022-03036-1 — Compares deep language models, including masked-word models, with brain responses and finds that predictive ability drives the similarity.
