---
status: draft
last_reviewed: 2026-10-28
tags:
  - language
  - sequence modelling
aliases:
  - 聯合意圖偵測與槽位填充
  - Joint intent detection and slot filling
  - Joint NLU
  - Liu and Lane 2016
---

# Joint intent detection and slot filling (Liu and Lane 2016)

Liu and Lane (2016) proposed an attention-based recurrent network that classifies the intent of an utterance and tags its slots in one model, rather than in two separate stages. It is a landmark method of the understanding stage of [customer service and conversational systems](../index.md).

## Overview

A task-oriented system must turn a request such as "book a flight from Taipei to Tokyo on Friday" into two outputs. The intent is a flight booking. The slot values are origin Taipei, destination Tokyo and date Friday. Early systems trained a classifier for the intent and a sequence tagger for the slots separately, so the two models shared no features.

Liu and Lane built on attention-based encoder-decoder networks, which had shown strong results in machine translation and speech recognition. They noted that slot filling differs from those tasks because the alignment between words and labels is explicit. The model uses that alignment and is trained on both tasks at once.

## Key concepts

- **Intent detection**: assigning one label to a whole utterance, a sentence classification problem.
- **Slot filling**: assigning a label to every word, usually in the BIO scheme. B marks the start of a slot value, I its continuation and O a word outside any slot.
- **Alignment**: the correspondence between input words and output labels. In slot filling it is one-to-one.
- **Joint training**: one network trained on the combined loss of both tasks, so that features learned for one task help the other.

## How it works

Let $h_1, \dots, h_T$ be the hidden states of a recurrent encoder that reads the words $x_1, \dots, x_T$. For each slot position $t$, the model scores every input position and normalises the scores into weights:

$$
\alpha_{t,i} = \frac{\exp(e_{t,i})}{\sum_{j=1}^{T} \exp(e_{t,j})}, \qquad c_t = \sum_{i=1}^{T} \alpha_{t,i}\, h_i
$$

The context vector $c_t$, combined with the decoder state, predicts the slot tag $s_t$. The intent is predicted from a sentence-level context. Training minimises the sum of the two cross-entropy losses:

$$
\mathcal{L} = -\log p(y_{\text{intent}} \mid x) \;-\; \sum_{t=1}^{T} \log p(s_t \mid x)
$$

The procedure is:

1. Encode the words into hidden states with a recurrent network.
2. For each word position, compute attention weights over the encoder states and build the context vector.
3. Predict the BIO slot tag from the context and the decoder state, and predict the intent from a sentence-level representation.
4. Add the intent loss and the slot loss, and update all parameters by gradient descent.
5. At inference, take the most probable intent and tags, then read the slot values from the tagged spans.

## Results

The paper evaluates on the ATIS benchmark, a corpus of airline travel requests. Its independently trained task models reached state-of-the-art intent error rate and slot F1 at the time. Joint training improved on them further. The abstract reports a 0.56 point absolute reduction in intent error (23.8 percent relative) and a 0.23 point absolute gain in slot F1.[^1]

These results come from one domain with a small label set, so they show that sharing the two tasks helps on that benchmark, not on a live workload.

## Limitations

- **Narrow benchmark.** ATIS covers one domain with a small, fixed set of intents. Gains may not carry over to banking, telecoms or retail, where intents are more numerous and change often.
- **Annotation cost.** Slot filling needs word-level labels, which are expensive to produce for each new domain.
- **Closed label set.** The model predicts only labels it was trained on. A new kind of request needs new data and retraining, and an unseen request is forced into a wrong label.
- **Single turn.** The model reads one utterance. Carrying slot values across turns is the job of dialogue state tracking, which this method does not provide.
- **Upstream errors.** Speech-recognition errors in the input still reach the model.

## Open questions

- **Gains with pretraining.** Later work replaced the recurrent encoder with pretrained transformers. Whether joint training still adds value once every model is pretrained needs direct comparison.
- **Label efficiency.** Pretrained sentence encoders reduce the labelled examples needed for new intents (Casanueva et al., 2020). How far this reaches for slot labels is less clear.
- **Replacing the tagger.** A generative language model can write intents and slot values as text, which removes the fixed label set but may cost the checkability of typed outputs. See the [SimpleTOD](../simpletod/index.md) page.

[^1]: Liu and Lane (2016), abstract: the joint model gives a 0.56% absolute (23.8% relative) error reduction on intent detection and a 0.23% absolute gain in slot filling over the independent task models, on ATIS. https://arxiv.org/abs/1609.01454

## References

### Seminal papers

- Liu, B. & Lane, I. (2016). Attention-Based Recurrent Neural Network Models for Joint Intent Detection and Slot Filling. https://arxiv.org/abs/1609.01454 — The paper that introduces the attention-based joint model and shows that joint training improves intent and slot accuracy on ATIS.
- Chen, Q., Zhuo, Z. & Wang, W. (2019). BERT for Joint Intent Classification and Slot Filling. https://arxiv.org/abs/1902.10909 — Applies pretrained BERT to the joint task and reports significant gains in intent accuracy and slot F1.
- Devlin, J., Chang, M.-W., Lee, K. & Toutanova, K. (2018). BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding. https://arxiv.org/abs/1810.04805 — Introduces BERT, the pretrained transformer that later joint models fine-tune.
- Casanueva, I. et al. (2020). Efficient Intent Detection with Dual Sentence Encoders. https://arxiv.org/abs/2003.04807 — Intent detectors built on pretrained sentence encoders that work with few labelled examples per intent.

### Surveys and textbooks

- Weld, H. et al. (2021). A survey of joint intent detection and slot-filling models in natural language understanding. https://arxiv.org/abs/2101.08091 — Survey tracing joint intent and slot models from recurrent networks to BERT-based models.
