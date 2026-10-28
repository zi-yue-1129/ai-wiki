---
related:
- theory/models/llm
- theory/paradigms/transfer
- theory/deep-learning
- engineering/hardware
---

# Training & Fine-tuning

## Pre-training at scale

| Ingredient | Notes |
|---|---|
| Compute | Measured in FLOPs; frontier runs exceed 10²⁵–10²⁶ FLOPs |
| Parallelism | Data, tensor, pipeline, sequence/context and expert parallelism; ZeRO/FSDP sharding |
| Precision | BF16 standard; FP8 training increasingly common |
| Stability | Learning-rate warmup, gradient clipping, careful initialisation, QK-norm, loss-spike monitoring |
| Data mixture | Web, code, math, multilingual, synthetic; curricula and annealing on high-quality data |
| Checkpointing | Frequent, sharded, with fault tolerance for thousands of accelerators |

Rough compute estimate for dense Transformers: **training FLOPs ≈ 6 × parameters × tokens**.

## Fine-tuning methods

| Method | What changes | Memory | When |
|---|---|---|---|
| Full fine-tuning | All weights | Highest | Enough data and compute; major behaviour change |
| LoRA (Hu et al., 2021) | Low-rank update \(W + BA\) on chosen matrices | Low | Default for most adaptation |
| [QLoRA](../../theory/model-compression/low-rank-and-efficient-architectures/lora/qlora.md) (Dettmers et al., 2023) | LoRA on a 4-bit quantised base model | Very low | Fine-tune large models on one GPU |
| [DoRA](../../theory/model-compression/low-rank-and-efficient-architectures/lora/dora.md), other LoRA variants | Decompose magnitude/direction, etc. | Low | Sometimes better quality |
| [Adapters](../../theory/paradigms/transfer/fine-tuning-and-adaptation/adapters.md), [prefix](../../theory/paradigms/transfer/fine-tuning-and-adaptation/prefix-tuning.md) and [prompt tuning](../../theory/paradigms/transfer/fine-tuning-and-adaptation/prompt-tuning.md) | Small inserted modules or learned prompts | Very low | Many tasks on one base |
| Continued pre-training | All weights on domain text | High | New domain or language |

## Post-training for LLMs

1. **Supervised fine-tuning (SFT)** on instruction–response pairs (quality > quantity)
2. **Preference optimisation**:
    - RLHF with a reward model and PPO
    - **DPO** (Rafailov et al., 2023) and variants (IPO, KTO, ORPO, SimPO)
    - RLAIF / Constitutional AI
3. **Reinforcement learning with verifiable rewards** (GRPO and related) for reasoning, math and code
4. **Safety training** and refusal calibration
5. **Distillation** from a stronger teacher

DPO objective, given preferred \(y_w\) and dispreferred \(y_l\):

\[
L = -\log \sigma\!\left(\beta \log\frac{\pi_\theta(y_w\mid x)}{\pi_{ref}(y_w\mid x)} - \beta \log\frac{\pi_\theta(y_l\mid x)}{\pi_{ref}(y_l\mid x)}\right)
\]

## Practical recipe for a LoRA fine-tune

1. Define the target behaviour and build an **evaluation set first**
2. Try prompting and RAG; fine-tune only if they fall short
3. Collect a few hundred to a few thousand high-quality examples in the chat format of the base model
4. Start with LoRA rank 8–64 on attention and MLP projections, learning rate ~1e-4 to 2e-4, 1–3 epochs
5. Watch validation loss and task evals; check for **catastrophic forgetting** of general skills and safety behaviour
6. Merge or serve adapters; document data and settings in a model card

## Other techniques

- **Knowledge distillation** (teacher → student)
- **Model merging** (task arithmetic, TIES, SLERP)
- **Quantisation-aware training**
- **Curriculum and data mixing** schedules
- **Hyperparameter search**: random search, Bayesian optimisation, population-based training

## References

- Micikevicius, P., et al. (2017). *Mixed Precision Training*. arXiv:1710.03740. https://arxiv.org/abs/1710.03740 — Shows that 16-bit training reduces memory use by nearly two times across architectures, with master weights and loss scaling.
- Shoeybi, M., et al. (2019). *Megatron-LM: Training Multi-Billion Parameter Language Models Using Model Parallelism*. arXiv:1909.08053. https://arxiv.org/abs/1909.08053 — Shows intra-layer model parallelism training an 8.3 billion parameter transformer on 512 GPUs at 76% scaling efficiency.
- Rajbhandari, S., et al. (2019). *ZeRO: Memory Optimizations Toward Training Trillion Parameter Models*. arXiv:1910.02054. https://arxiv.org/abs/1910.02054 — Eliminates memory redundancy in data- and model-parallel training while keeping communication volume low.
- Houlsby, N., et al. (2019). *Parameter-Efficient Transfer Learning for NLP*. arXiv:1902.00751. https://arxiv.org/abs/1902.00751 — Introduces adapters that reach a mean GLUE score 0.4 points below full fine-tuning while adding 3.6% parameters per task.
- Dettmers, T., et al. (2023). *QLoRA: Efficient Finetuning of Quantized LLMs*. arXiv:2305.14314. https://arxiv.org/abs/2305.14314 — Fine-tunes LoRA adapters on a 4-bit frozen base, making a 65-billion-parameter model trainable on one 48 GB GPU.
- Hu, E. J. et al. (2021). *LoRA: Low-Rank Adaptation of Large Language Models*. arXiv:2106.09685. https://arxiv.org/abs/2106.09685 — Freezes the pretrained weights and trains low-rank update matrices, the method behind the LoRA recipe on this page.
- Ouyang, L. et al. (2022). *Training language models to follow instructions with human feedback*. NeurIPS 2022. https://arxiv.org/abs/2203.02155 — InstructGPT: supervised fine-tuning on demonstrations, then reinforcement learning against a reward model; the template for post-training.
- Hoffmann, J. et al. (2022). *Training Compute-Optimal Large Language Models*. arXiv:2203.15556. https://arxiv.org/abs/2203.15556 — Chinchilla: shows that model size and training tokens should grow together for a fixed compute budget.
- Kaplan, J. et al. (2020). *Scaling Laws for Neural Language Models*. arXiv:2001.08361. https://arxiv.org/abs/2001.08361 — Power-law relations between loss, parameters, data and compute that motivate large-scale pre-training.
- Rafailov, R. et al. (2023). *Direct Preference Optimization: Your Language Model is Secretly a Reward Model*. NeurIPS 2023. https://arxiv.org/abs/2305.18290 — Fits the policy to preference pairs directly, without a separate reward model or an RL loop.

## Further learning

- [Hugging Face TRL](https://huggingface.co/docs/trl) and [PEFT](https://huggingface.co/docs/peft) — libraries that implement the fine-tuning and adapter methods described above.
- Stanford CS336
- *The Ultra-Scale Playbook* (Hugging Face, 2025) on distributed training
- Lambert, *RLHF Book* (free online)
- Unsloth and Axolotl documentation for practical fine-tuning
