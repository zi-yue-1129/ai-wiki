---
related:
- theory/models/llm
- brain-mind/snn-neuromorphic
---

# Other Learning Paradigms

Shorter entries for paradigms that do not fit neatly elsewhere.

## Multi-task learning

Train one model on several related tasks at once with shared representations. Benefits: data efficiency, regularisation, better generalisation. Risks: **negative transfer** and conflicting gradients (addressed by gradient surgery such as PCGrad, uncertainty-based loss weighting). Instruction-tuned LLMs are extreme multi-task learners.

## Curriculum learning

Present examples **from easy to hard** (Bengio et al., 2009), as in human education. Variants: self-paced learning (the model chooses), teacher–student curricula, automatic curricula in RL (environments that get harder as the agent improves), and data-mixing schedules in LLM pre-training (higher-quality data near the end). Effect sizes vary; it helps most when the task is hard to learn from scratch.

**Psychology link:** scaffolding and Vygotsky's *zone of proximal development*; "desirable difficulties" (Bjork) show that some difficulty during learning improves retention.

## Multiple-instance learning (MIL)

Labels are attached to **bags** of instances, not to instances. A bag is positive if at least one instance is positive. Used for whole-slide pathology, drug activity (a molecule is active if any conformation binds), and weakly labelled video.

## Positive–unlabelled (PU) learning

Only some positive examples are labelled; everything else is unlabelled (a mix of positives and negatives). Examples: known disease genes vs all other genes; a user's clicked items vs everything unseen.

## Zero-shot, few-shot and in-context learning

- **Zero-shot**: handle classes or tasks never seen in training, via side information (attributes, text descriptions, CLIP-style embeddings) or instructions to an LLM.
- **Few-shot**: see [Meta-Learning](../meta-learning/index.md).
- **In-context learning**: an LLM learns from examples in its prompt without weight updates.

## Contrastive and metric learning

Learn an embedding space where similar items are close: Siamese networks, triplet loss, ArcFace for face recognition, sentence embeddings. Underlies retrieval, deduplication and [RAG](../../../engineering/rag/index.md). See also [Self-Supervised Learning](../self-supervised/index.md).

## Ensemble learning

Combine many models: bagging (random forests), boosting (gradient boosting), stacking, deep ensembles. Often the easiest way to gain accuracy and calibrated uncertainty. The "wisdom of crowds" is the social-science analogue.

## Knowledge distillation

A small **student** model learns to match a large **teacher**'s soft outputs (Hinton, Vinyals & Dean, 2015). Widely used to deploy LLMs and vision models cheaply; reasoning models are often distilled into smaller ones.

## Learning from human feedback and preferences

Learn from comparisons ("A is better than B") rather than labels or numeric rewards: RLHF, DPO, preference-based RL. See [Large Language Models](../../models/llm/index.md) and [Safety & Alignment](../../../society/safety-alignment/index.md).

## Causal and invariant learning

Learn relationships that stay stable across environments rather than spurious correlations: invariant risk minimisation (IRM), causal representation learning. See [Probabilistic & Bayesian Methods](../../probabilistic/index.md).

## Evolutionary and developmental learning

Optimise by population-based search rather than gradients. See [Evolutionary & Swarm Intelligence](../../evolutionary/index.md). Developmental robotics studies how robots can learn through staged, child-like development.

## Hebbian and local learning rules

Learning without global backpropagated error — Hebbian, STDP, predictive-coding networks, forward-forward. Important for [neuromorphic hardware](../../../brain-mind/snn-neuromorphic/index.md) and for theories of [how the brain learns](../../../brain-mind/neuroai/index.md).

## Test-time training and test-time compute

- **Test-time training/adaptation**: update the model on each test input via a self-supervised loss.
- **Test-time compute scaling**: spend more inference computation (long chains of thought, search, voting) instead of more training — a defining trend of 2024–2026 reasoning models.
