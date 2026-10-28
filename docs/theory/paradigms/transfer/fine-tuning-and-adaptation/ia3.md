---
status: draft
last_reviewed: 2026-10-28
related:
- theory/paradigms/transfer/fine-tuning-and-adaptation/index.md
- theory/paradigms/transfer/fine-tuning-and-adaptation/adapters.md
- theory/model-compression/low-rank-and-efficient-architectures/lora/index.md
tags:
- transfer learning
- fine-tuning
- parameter-efficient fine-tuning
- in-context learning
aliases:
  - IA3
  - "(IA)³"
  - 激活縮放微調
---

# (IA)³ Fine-Tuning

(IA)³ is a parameter-efficient fine-tuning method that adapts a frozen language model by rescaling its internal activations with learned vectors. Liu et al. (2022) argue that parameter-efficient fine-tuning is both more accurate and far cheaper than few-shot in-context learning, which must process all the examples again for every prediction. They combine the method with a training recipe, T-Few, that reaches super-human performance on the RAFT benchmark. It sits within [fine-tuning and adaptation](index.md) as a method that adds very few parameters and leaves the model's structure unchanged.

## Problem

In-context learning adapts a model by putting a few labelled examples in its input, without any weight updates. This is convenient, but it has substantial computational, memory and storage costs, because every example is processed again for every prediction. Full fine-tuning is accurate but needs a full copy of the model per task. A method is needed that is cheap to train and store, and that competes with both.

## Key concepts

- **Activation scaling:** multiplying an activation element-wise by a learned vector. The vectors start at ones, so the model's behaviour is unchanged at initialisation.
- **Where it scales:** the keys and values in self-attention and encoder-decoder attention, and the intermediate activations of the feed-forward networks, in every Transformer block.
- **Frozen model:** the pre-trained weights stay fixed, and only the scaling vectors are trained.

## How it works

For each task, the scaling vectors are trained on the task's labelled examples while the model's weights stay fixed. At inference, the activations are multiplied by these vectors. Because the change is an element-wise scaling, it adds little computation, and a task is stored as a small set of vectors.

T-Few is the recipe built around the method. It uses the T0 model as the backbone, pre-trains the (IA)³ vectors on T0's multitask mixture, and sums three losses: standard language modelling, unlikelihood, and length-normalised. In the paper's ablation, length normalisation raises accuracy from 60.7% to 62.7%, and adding the unlikelihood loss brings it to 63.3%.

## Results

The paper says (IA)³ updates up to 10,000 times fewer parameters than full fine-tuning, and its table lists about 540K added parameters for T0-3B. On RAFT, a benchmark of unseen tasks, T-Few reaches 75.8% against a human baseline of 73.5%, which the paper calls super-human performance for the first time, and it outperforms the previous state of the art by 6% absolute. The next-best entry in its table, PET, scores 69.6%. The authors state that the code used in the experiments is public.

## Limitations

- **Classification only.** The authors say all their experiments are on classification tasks, and they leave generative tasks such as summarisation and question answering to future work.
- **FLOPs as a proxy.** The cost comparison uses FLOPs, which are hardware-independent, so it does not measure real latency or power use.
- **Copied baselines.** The GPT-3 numbers were copied from Brown et al. rather than re-run.
- **Recipe effects.** The reported RAFT results are for T-Few as a whole, which combines the method with pre-training and extra losses, so the effect of the scaling alone needs its own ablation.

## Open questions

- **Generative tasks.** Whether the same gains hold for generation, which the paper leaves to future work, is an open question.
- **Versus low-rank updates.** How activation scaling compares with [LoRA](../../../../theory/model-compression/low-rank-and-efficient-architectures/lora/index.md) in accuracy and inference cost on the same tasks is an open practical question.

## Connections

(IA)³ is a parameter-efficient method alongside [adapters](adapters.md), which add small layers, and [LoRA](../../../../theory/model-compression/low-rank-and-efficient-architectures/lora/index.md), which adds low-rank updates. The comparison with in-context learning matters for [training and fine-tuning](../../../../engineering/training/index.md) practice, where few-shot prompting is the usual alternative.

## References

### Seminal papers

- Liu, H., et al. (2022). *Few-Shot Parameter-Efficient Fine-Tuning is Better and Cheaper than In-Context Learning*. arXiv:2205.05638. https://arxiv.org/abs/2205.05638 — Introduces (IA)³ and the T-Few recipe, and shows that parameter-efficient fine-tuning beats few-shot in-context learning on accuracy and cost.
- Houlsby, N., et al. (2019). *Parameter-Efficient Transfer Learning for NLP*. arXiv:1902.00751. https://arxiv.org/abs/1902.00751 — Introduces adapters, the layer-adding parameter-efficient method in the same family.
- Hu, E. J., et al. (2021). *LoRA: Low-Rank Adaptation of Large Language Models*. arXiv:2106.09685. https://arxiv.org/abs/2106.09685 — Learns low-rank updates on frozen weights, another parameter-efficient method that adds no inference latency once merged.
- Li, X. L., Liang, P. (2021). *Prefix-Tuning: Optimizing Continuous Prompts for Generation*. arXiv:2101.00190. https://arxiv.org/abs/2101.00190 — Trains a continuous prefix with the language model frozen, a prompt-based route to the same goal.
- Lester, B., Al-Rfou, R., Constant, N. (2021). *The Power of Scale for Parameter-Efficient Prompt Tuning*. arXiv:2104.08691. https://arxiv.org/abs/2104.08691 — Learns soft prompts on a frozen model and shows the approach matches model tuning as models grow.
