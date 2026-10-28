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

(IA)³ is a parameter-efficient fine-tuning method that adapts a frozen language model by multiplying its internal activations by learned vectors. The paper introducing it, by Liu et al. (2022), argues that parameter-efficient fine-tuning is both more accurate and far cheaper than few-shot in-context learning, which must process all the examples again for every prediction. It is one of the methods in [fine-tuning and adaptation](index.md) that add very few parameters and leave the model's structure unchanged.

## Problem

In-context learning adapts a model by putting a few labelled examples in its input, without any weight updates. This is convenient, but it has substantial computational, memory and storage costs, because every example is processed again for every prediction. Full fine-tuning is accurate but needs a full copy of the model per task. A method is needed that is cheap to train and store, and that competes with both.

## Key concepts

- **Activation scaling:** multiplying a layer's activations element-wise by a learned vector. Each vector has the size of the activation it scales, so the added parameters are few.
- **Frozen model:** the pre-trained weights stay fixed, and only the scaling vectors are trained.
- **In-context learning:** adaptation by examples in the input, the baseline the paper compares against.

## How it works

For each task, a small set of scaling vectors is trained on the task's labelled examples while the model's weights stay fixed. At inference, the activations are scaled by these vectors. Because the change is a per-element scaling, it adds very little computation, and it can be stored as a small set of vectors per task.

## Results

The abstract reports that parameter-efficient fine-tuning gives better accuracy and much lower computational cost than few-shot in-context learning. The paper also proposes T-Few, a recipe built on the T0 model that can be applied to new tasks without task-specific tuning. Applied to the RAFT benchmark of unseen tasks, T-Few is reported to reach super-human performance for the first time and to outperform the previous state of the art by 6 points. The authors state that all code used in the experiments is public.

## Limitations

- **Task family.** The headline results are for T-Few, which is built on the T0 model, so they describe that setting and carry over to other model families only with new checks.
- **Compared with full tuning.** The abstract does not state a direct comparison with full fine-tuning, so the paper alone does not establish how far (IA)³ falls short of it.
- **Recipe dependence.** The reported results are for T-Few as a whole, so the effect of the activation scaling alone needs its own ablation.

## Open questions

- **Where to scale.** Which activations to scale, and whether one set of vectors works across tasks, are design choices the paper leaves open for further study.
- **Versus low-rank updates.** How activation scaling compares with [LoRA](../../../../theory/model-compression/low-rank-and-efficient-architectures/lora/index.md) in accuracy and inference cost on the same tasks is an open practical question.

## Connections

(IA)³ is a parameter-efficient method alongside [adapters](adapters.md), which add small layers, and [LoRA](../../../../theory/model-compression/low-rank-and-efficient-architectures/lora/index.md), which adds low-rank updates. The comparison with in-context learning is the reason the paper matters for [training and fine-tuning](../../../../engineering/training/index.md) practice, where few-shot prompting is the usual alternative.

## References

### Seminal papers

- Liu, H., et al. (2022). *Few-Shot Parameter-Efficient Fine-Tuning is Better and Cheaper than In-Context Learning*. arXiv:2205.05638. https://arxiv.org/abs/2205.05638 — Introduces (IA)³ and shows that parameter-efficient fine-tuning beats few-shot in-context learning on accuracy and cost.
- Houlsby, N., et al. (2019). *Parameter-Efficient Transfer Learning for NLP*. arXiv:1902.00751. https://arxiv.org/abs/1902.00751 — Introduces adapters, the layer-adding parameter-efficient method in the same family.
- Hu, E. J., et al. (2021). *LoRA: Low-Rank Adaptation of Large Language Models*. arXiv:2106.09685. https://arxiv.org/abs/2106.09685 — Learns low-rank updates on frozen weights, another parameter-efficient method that adds no inference latency once merged.
- Li, X. L., Liang, P. (2021). *Prefix-Tuning: Optimizing Continuous Prompts for Generation*. arXiv:2101.00190. https://arxiv.org/abs/2101.00190 — Trains a continuous prefix with the language model frozen, a prompt-based route to the same goal.
- Lester, B., Al-Rfou, R., Constant, N. (2021). *The Power of Scale for Parameter-Efficient Prompt Tuning*. arXiv:2104.08691. https://arxiv.org/abs/2104.08691 — Learns soft prompts on a frozen model and shows the approach matches model tuning as models grow.
