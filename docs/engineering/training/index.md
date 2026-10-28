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

The number formats behind the Precision row, and how gradient checkpointing trades recomputation for activation memory, are covered in [Mixed-precision training and gradient checkpointing](mixed-precision-and-checkpointing.md). The attention kernel that dominates much of long-context training memory and time, and the fused kernels around it, are covered in [FlashAttention and fused kernels](flash-attention.md).

## Fine-tuning methods

| Method | What changes | Memory | When |
|---|---|---|---|
| Full fine-tuning | All weights | Highest | Enough data and compute; major behaviour change |
| LoRA (Hu et al., 2021) | Low-rank update \(W + BA\) on chosen matrices | Low | Default for most adaptation |
| QLoRA (Dettmers et al., 2023) | LoRA on a 4-bit quantised base model | Very low | Fine-tune large models on one GPU |
| DoRA, other LoRA variants | Decompose magnitude/direction, etc. | Low | Sometimes better quality |
| Adapters, prefix/prompt tuning | Small inserted modules or learned prompts | Very low | Many tasks on one base |
| Continued pre-training | All weights on domain text | High | New domain or language |

For LoRA, QLoRA, DoRA, adapters and prefix and prompt tuning in detail, see [LoRA, QLoRA and parameter-efficient fine-tuning](peft-lora.md).

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

The derivation of DPO and its successors (IPO, KTO, ORPO, SimPO), with online versus offline data, is in [Preference optimisation: DPO and its successors](preference-optimisation.md).

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

## Resources

- Hugging Face [TRL](https://huggingface.co/docs/trl), [PEFT](https://huggingface.co/docs/peft)
- Stanford CS336
- *The Ultra-Scale Playbook* (Hugging Face, 2025) on distributed training
- Lambert, *RLHF Book* (free online)
- Unsloth and Axolotl documentation for practical fine-tuning

## References

Seminal works for this overview, drawn from the sub-pages linked above, where each is discussed in detail.

- Hu, E. J. et al. (2021). *LoRA: Low-Rank Adaptation of Large Language Models*. arXiv:2106.09685. https://arxiv.org/abs/2106.09685 — Introduces the frozen-weight low-rank update used throughout this page.
- Dettmers, T. et al. (2023). *QLoRA: Efficient Finetuning of Quantized LLMs*. arXiv:2305.14314. https://arxiv.org/abs/2305.14314 — Trains LoRA adapters on a 4-bit frozen base model.
- Bradley, R. A. & Terry, M. E. (1952). *Rank Analysis of Incomplete Block Designs: I. The Method of Paired Comparisons*. Biometrika. https://doi.org/10.2307/2334029 — Introduces the paired-comparison model behind the preference loss.
- Rafailov, R. et al. (2023). *Direct Preference Optimization: Your Language Model is Secretly a Reward Model*. arXiv. https://arxiv.org/abs/2305.18290 — Derives the DPO loss from the RLHF objective, dropping the reward model.
- Micikevicius, P. et al. (2017). *Mixed Precision Training*. arXiv:1710.03740. https://arxiv.org/abs/1710.03740 — Introduces FP32 master weights and loss scaling for half-precision training.
- Kalamkar, D. et al. (2019). *A Study of BFLOAT16 for Deep Learning Training*. arXiv:1905.12322. https://arxiv.org/abs/1905.12322 — Shows BF16 training matches FP32 results across several domains.
- Dao, T. et al. (2022). *FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness*. NeurIPS 2022. https://arxiv.org/abs/2205.14135 — Introduces tiled exact attention that reduces reads and writes between GPU high-bandwidth memory and on-chip SRAM.
- Dao, T. (2023). *FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning*. ICLR 2024. https://arxiv.org/abs/2307.08691 — Improves work partitioning across thread blocks and warps, so attention reaches a larger share of peak FLOPs/s.
