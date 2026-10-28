---
status: draft
last_reviewed: 2026-10-28
tags:
  - transfer learning
  - sequence modelling
aliases:
  - T5
  - Text-to-Text Transfer Transformer
  - 文字到文字轉移 Transformer
---

# T5: text-to-text transfer with an encoder–decoder (Raffel et al., 2019)

T5 is an encoder–decoder Transformer that turns every language task into text in, text out, and is pre-trained by filling in dropped spans of text. It is the landmark encoder–decoder member of the [Transformer architecture families](../index.md).

## Overview

Transfer learning in NLP had used a different head, format and objective for each task. Raffel et al. (2019) proposed one interface for all of them: classification labels, translations and summaries are written as text strings and handled by the same model and loss. The paper used this framework for a systematic study of objectives, architectures and corpora.

They built the Colossal Clean Crawled Corpus (C4), about 750 GB of cleaned English web text, and trained models up to 11 billion parameters.

T5 sits in the [architecture families](../index.md) between the encoder-only [BERT](../bert/index.md) and the decoder-only [GPT-3](../../../llm/gpt-3-few-shot/index.md). BART (Lewis et al., 2019) is a close relative, trained by text reconstruction. The encoder–decoder design is also used for speech, as in Whisper (Radford et al., 2022); see [Speech models](../../../speech/index.md). The wider context is [Transformers & Attention](../../index.md).

## Key concepts

- **Text-to-text format.** An input begins with a task prefix, such as "translate English to German:", and the target is the answer as text. Classification labels are written as words, so the output format never changes.
- **Encoder–decoder.** A standard Transformer following Vaswani et al. (2017): a bidirectional encoder over the input and a causal decoder with cross-attention over the encoder's output.
- **Span corruption.** A denoising objective in which spans of input tokens are replaced by sentinel tokens, and the target is the sequence of dropped spans.
- **Sentinel token.** A special vocabulary item that marks where a span was removed.

## How it works

Pre-training proceeds as follows, in the form used by the final model:

1. Take a span of unlabelled text from C4 and choose about 15% of its tokens for corruption.
2. Group the chosen tokens into consecutive spans with an average length of three. Replace each span in the input with one unique sentinel token.
3. Build the target as the dropped spans, each preceded by its sentinel, followed by a final sentinel that marks the end.
4. Train with teacher forcing on the cross-entropy loss over the target.
5. For a downstream task, write the input and target as text with a task prefix, and fine-tune in the same format.

An example from the paper: the text "Thank you for inviting me to your party last week" can be corrupted so that the input reads "Thank you <X> me to your party <Y> week" and the target reads "<X> for inviting <Y> last <Z>", where the sentinels mark the spans and the final one ends the target.

Consecutive spans were chosen partly to reduce computational cost, as the paper notes.

## Results

The paper's controlled comparisons use models of matched computational cost. In its architecture and objective table, the encoder–decoder with the denoising objective had the highest GLUE average (83.28). The decoder-only language model with the same denoising objective scored 74.70, and the decoder-only language model with the standard causal objective scored 73.78, the lowest GLUE value in the table. A prefix language model, a decoder-only model that is bidirectional over its prefix, scored 81.82 with denoising.

In the span-length sweep, mean lengths of 2 to 5 scored about the same on GLUE (83.40 to 83.54, against 83.28 for independent tokens), and 10 scored 82.85. The final model uses a mean length of three.

The 11-billion-parameter model performed best of the sizes studied, and the abstract reports state-of-the-art results on many benchmarks.

## Limitations

- **Two stacks cost memory.** An encoder–decoder with *L* layers in each stack has about twice the parameters of a decoder-only model with *L* layers, at roughly the same compute.
- **Comparisons depend on scale.** Later work reported that decoder-only models with autoregressive pre-training generalised best to new tasks after purely unsupervised pre-training (Wang et al., 2022). The T5 comparisons were made at a particular scale and budget.

## Open questions

- Does the encoder–decoder advantage on understanding tasks survive at much larger scales?
- Can one model be trained with mixed objectives and used in different modes? UL2 (Tay et al., 2022) proposes a mixture of denoisers and reports gains over T5 and GPT-like models in several setups.

## References

### Seminal papers

- Raffel, C., et al. (2019). *Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer*. arXiv; JMLR 2020. https://arxiv.org/abs/1910.10683 — The original paper: text-to-text framework, C4 corpus and controlled comparisons.
- Vaswani, A., et al. (2017). *Attention Is All You Need*. NeurIPS. https://arxiv.org/abs/1706.03762 — The encoder–decoder Transformer that T5 uses as its base architecture.
- Devlin, J., et al. (2018). *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding*. arXiv; NAACL 2019. https://arxiv.org/abs/1810.04805 — The masked objective that span corruption adapts.
- Lewis, M., et al. (2019). *BART: Denoising Sequence-to-Sequence Pre-training for Natural Language Generation, Translation, and Comprehension*. arXiv; ACL 2020. https://arxiv.org/abs/1910.13461 — An encoder–decoder pre-trained to reconstruct corrupted text.
- Wang, T., et al. (2022). *What Language Model Architecture and Pretraining Objective Work Best for Zero-Shot Generalization?* arXiv. https://arxiv.org/abs/2204.05832 — Finds that decoder-only models with autoregressive pre-training generalise best zero-shot.

### Surveys and textbooks

- Tay, Y., et al. (2022). *UL2: Unifying Language Learning Paradigms*. arXiv; ICLR 2023. https://arxiv.org/abs/2205.05131 — Proposes a mixture of denoisers, reported to beat T5 and GPT-like models in several setups.

### Articles and documentation

- Radford, A., et al. (2022). *Robust Speech Recognition via Large-Scale Weak Supervision*. arXiv; ICML 2023. https://arxiv.org/abs/2212.04356 — Describes Whisper, a speech recognizer built on an encoder–decoder Transformer and trained on large-scale web audio transcripts.
