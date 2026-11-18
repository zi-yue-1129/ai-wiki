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
| LoRA (Hu et al., 2021) | Low-rank update \(W + BA\) on chosen matrices | Low | Parameter-efficient adaptation; compare with full fine-tuning when feasible |
| [QLoRA](../../theory/model-compression/low-rank-and-efficient-architectures/lora/qlora.md) (Dettmers et al., 2023) | LoRA on a 4-bit quantised base model | Very low | Memory-constrained adaptation; verify the actual GPU requirement |
| [DoRA](../../theory/model-compression/low-rank-and-efficient-architectures/lora/dora.md), other LoRA variants | Decompose magnitude/direction, etc. | Low | Sometimes better quality |
| [Adapters](../../theory/paradigms/transfer/fine-tuning-and-adaptation/adapters.md), [prefix](../../theory/paradigms/transfer/fine-tuning-and-adaptation/prefix-tuning.md) and [prompt tuning](../../theory/paradigms/transfer/fine-tuning-and-adaptation/prompt-tuning.md) | Small inserted modules or learned prompts | Very low | Many tasks on one base |
| Continued pre-training | All weights on domain text | High | New domain or language |

The memory labels are qualitative, not GPU-capacity guarantees. LoRA reduces trainable parameters, gradients and optimiser state; the base weights and intermediate activations still occupy memory. QLoRA additionally quantises the frozen base weights, not the entire training computation.[^lora][^qlora][^memory]

## Post-training for LLMs

1. **Supervised fine-tuning (SFT)** on instruction–response pairs (quality > quantity)
2. **Preference optimisation**:
    - RLHF with a reward model and PPO
    - **DPO** (Rafailov et al., 2023) and variants (IPO, KTO, ORPO, SimPO)
    - RLAIF / Constitutional AI
3. **Reinforcement learning with verifiable rewards** (GRPO and related) for reasoning, math and code
4. **Safety training** and refusal calibration
5. **Distillation** from a stronger teacher

DPO objective, given preferred \(y_w\) and dispreferred \(y_l\):[^dpo]

\[
L = -\log \sigma\!\left(\beta \log\frac{\pi_\theta(y_w\mid x)}{\pi_{ref}(y_w\mid x)} - \beta \log\frac{\pi_\theta(y_l\mid x)}{\pi_{ref}(y_l\mid x)}\right)
\]

## Practical workflow for a LoRA fine-tune

Treat this as an experiment checklist, not a universal hyperparameter recipe. Dataset size, LoRA rank, learning rate and training duration must be selected for the model and task.

1. **Define the comparison first.** Specify the target behaviour and failure cases. Establish a prompting or retrieval-augmented generation (RAG) baseline. Separate training data, a validation set for choosing settings, and a held-out test set for the final comparison; repeated tuning on the test set leaks information.[^splits] See [Evaluation](../evaluation/index.md) for metrics and split design.
2. **Inspect the training examples.** Check data provenance, coverage and duplicates. Render examples through the intended tokenizer and chat template, then inspect token lengths and training labels. Decide whether the loss should cover the full sequence, completions, or assistant turns. In TRL, assistant-only loss requires a compatible template that supplies the assistant-token mask.[^sft]
3. **Choose adapter targets deliberately.** Verify the actual layer names and trainable-parameter count. PEFT's `target_modules="all-linear"` is an option for QLoRA-style coverage; it is not a requirement for every LoRA task. Tune rank, scaling, learning rate and training duration on validation results rather than copying a fixed rank or epoch count.[^peft][^splits]
4. **Run a short memory and correctness check.** Use representative sequence lengths, including long examples. Exercise a forward pass, backward pass, optimiser update and evaluation before committing to a long run. Record peak memory and throughput for the actual configuration; fitting the weights alone is insufficient.[^memory]
5. **Evaluate behaviour as well as loss.** Compare generated outputs with the baseline under the same decoding settings. Track target-task quality, important language or task slices, and general-skill and safety regressions. SFT loss measures token prediction, so it does not replace these behavioural checks.[^sft][^instructgpt] Select the checkpoint with validation data, then report the held-out test result.[^splits]
6. **Package a reproducible result.** Record the base-model revision, tokenizer/template, dataset splits, library versions, random seed, precision and adapter settings. Keep the adapter checkpoint; if merging or changing inference precision, repeat evaluation on the artifact that will actually be served. PEFT supports separate adapter loading as well as merging into the base model.[^peft]

### Memory controls and their trade-offs

| Control | What to check |
|---|---|
| LoRA / QLoRA | Fewer trainable parameters do not remove base-weight or activation memory; 4-bit base weights alone do not determine peak training memory.[^lora][^qlora][^memory] |
| Sequence length | Inspect the token-length distribution before setting a limit. Truncation can discard the answer or other important supervision.[^trl-memory] |
| Smaller microbatches + gradient accumulation | Accumulate gradients over several small forward/backward batches before updating weights. This supports a larger effective batch without holding all its activations at once; it is not a throughput improvement over a large batch that already fits.[^accumulation] |
| Activation checkpointing | Recompute some intermediate activations during backpropagation instead of storing them all; this trades extra computation for memory.[^checkpointing] |

Check the documentation for the library version used in the run. Supported templates, packing strategies, quantisation backends and merge paths can differ across models and releases.

## Other techniques

- **Knowledge distillation** (teacher → student)
- **Model merging** (task arithmetic, TIES, SLERP)
- **Quantisation-aware training**
- **Curriculum and data mixing** schedules
- **Hyperparameter search**: random search, Bayesian optimisation, population-based training

[^lora]: Hu et al. (2021), in References.
[^qlora]: Dettmers et al. (2023), in References.
[^dpo]: Rafailov et al. (2023), in References.
[^instructgpt]: Ouyang et al. (2022), in References.
[^splits]: scikit-learn, *Cross-validation: evaluating estimator performance*, in References.
[^peft]: Hugging Face PEFT, *LoRA*, in References.
[^sft]: Hugging Face TRL, *SFT Trainer*, in References.
[^memory]: Hugging Face Transformers, *GPU memory usage*, in References.
[^trl-memory]: Hugging Face TRL, *Reducing Memory Usage*, in References.
[^accumulation]: Hugging Face Transformers, *Gradient accumulation*, in References.
[^checkpointing]: Hugging Face Transformers, *Gradient checkpointing*, in References.

## References

### Seminal papers

- Micikevicius, P., et al. (2017). *Mixed Precision Training*. arXiv:1710.03740. https://arxiv.org/abs/1710.03740 — Shows that 16-bit training reduces memory use by nearly two times across architectures, with master weights and loss scaling.
- Shoeybi, M., et al. (2019). *Megatron-LM: Training Multi-Billion Parameter Language Models Using Model Parallelism*. arXiv:1909.08053. https://arxiv.org/abs/1909.08053 — Shows intra-layer model parallelism training an 8.3 billion parameter transformer on 512 GPUs at 76% scaling efficiency.
- Rajbhandari, S., et al. (2019). *ZeRO: Memory Optimizations Toward Training Trillion Parameter Models*. arXiv:1910.02054. https://arxiv.org/abs/1910.02054 — Eliminates memory redundancy in data- and model-parallel training while keeping communication volume low.
- Houlsby, N., et al. (2019). *Parameter-Efficient Transfer Learning for NLP*. arXiv:1902.00751. https://arxiv.org/abs/1902.00751 — Introduces adapters that reach a mean GLUE score 0.4 points below full fine-tuning while adding 3.6% parameters per task.
- Dettmers, T., et al. (2023). *QLoRA: Efficient Finetuning of Quantized LLMs*. arXiv:2305.14314. https://arxiv.org/abs/2305.14314 — Fine-tunes LoRA adapters on a 4-bit frozen base, making a 65-billion-parameter model trainable on one 48 GB GPU.
- Hu, E. J. et al. (2021). *LoRA: Low-Rank Adaptation of Large Language Models*. arXiv:2106.09685. https://arxiv.org/abs/2106.09685 — Freezes the pretrained weights and trains low-rank update matrices, the method behind the LoRA workflow on this page.
- Ouyang, L. et al. (2022). *Training language models to follow instructions with human feedback*. NeurIPS 2022. https://arxiv.org/abs/2203.02155 — InstructGPT: supervised fine-tuning on demonstrations, then reinforcement learning against a reward model; the template for post-training.
- Hoffmann, J. et al. (2022). *Training Compute-Optimal Large Language Models*. arXiv:2203.15556. https://arxiv.org/abs/2203.15556 — Chinchilla: shows that model size and training tokens should grow together for a fixed compute budget.
- Kaplan, J. et al. (2020). *Scaling Laws for Neural Language Models*. arXiv:2001.08361. https://arxiv.org/abs/2001.08361 — Power-law relations between loss, parameters, data and compute that motivate large-scale pre-training.
- Rafailov, R. et al. (2023). *Direct Preference Optimization: Your Language Model is Secretly a Reward Model*. NeurIPS 2023. https://arxiv.org/abs/2305.18290 — Fits the policy to preference pairs directly, without a separate reward model or an RL loop.

### Books and courses

- Lambert, N. *Reinforcement Learning from Human Feedback*. https://rlhfbook.com/ — Free online book covering instruction tuning, reward modelling, direct alignment and evaluation.
- Hugging Face. *The Ultra-Scale Playbook: Training LLMs on GPU Clusters*. https://huggingface.co/spaces/nanotron/ultrascale-playbook — Open book on distributed training, parallelism and memory/communication trade-offs, with code and benchmarks.
- Hashimoto, T. & Liang, P. *CS336: Language Modeling from Scratch*. Stanford, Spring 2025. https://cs336.stanford.edu/spring2025/ — Archived course with assignments on tokenization, training systems, scaling, data and alignment.

### Official documentation

- Hugging Face PEFT. *LoRA*. https://huggingface.co/docs/peft/developer_guides/lora — Explains target modules, rank and scaling configuration, adapter loading and merging.
- Hugging Face TRL. *SFT Trainer*. https://huggingface.co/docs/trl/sft_trainer — Documents dataset formats, chat templates, loss masking and adapter training.
- Hugging Face TRL. *Reducing Memory Usage*. https://huggingface.co/docs/trl/reducing_memory_usage — Explains sequence-length selection, truncation and packing trade-offs for supported trainers.
- Hugging Face Transformers. *GPU memory usage*. https://huggingface.co/docs/transformers/model_memory_anatomy — Separates weights, optimiser state, gradients, activations and temporary tensors in training memory.
- Hugging Face Transformers. *Gradient accumulation*. https://huggingface.co/docs/transformers/grad_accumulation — Explains effective batches, accumulation steps and token-aware loss normalisation.
- Hugging Face Transformers. *Gradient checkpointing*. https://huggingface.co/docs/transformers/grad_checkpointing — Explains recomputation of activations and the memory-versus-compute trade-off.
- scikit-learn. *Cross-validation: evaluating estimator performance*. https://scikit-learn.org/stable/modules/cross_validation.html — Distinguishes training, validation and testing, including the risk of tuning on test data.

## Further learning

- [Hugging Face TRL](https://huggingface.co/docs/trl) and [PEFT](https://huggingface.co/docs/peft) — library entry points for post-training and parameter-efficient adaptation.
- [Unsloth documentation](https://unsloth.ai/docs) — practical setup and model-specific training guides; check the requirements for the selected model.
- [Axolotl documentation](https://docs.axolotl.ai/) — configuration-driven fine-tuning, dataset formats and supported-model guides.
