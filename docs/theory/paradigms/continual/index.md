---
related:
- brain-mind/memory-learning
- engineering/mlops
---

# Continual Learning

## Idea

Learn from a **sequence of tasks or a non-stationary stream** while keeping what was learned before. Also called lifelong or incremental learning. Standard neural networks suffer **catastrophic forgetting** (McCloskey & Cohen, 1989): training on task B overwrites the weights that solved task A.

## The stability–plasticity dilemma

A learner must be **plastic** enough to acquire new knowledge yet **stable** enough not to lose old knowledge. Brains manage this remarkably well; artificial networks do not by default.

## Scenarios

| Scenario | At test time the model must… |
|---|---|
| Task-incremental | Solve each task, with the task identity given |
| Domain-incremental | Solve the same task under changing input distributions |
| Class-incremental | Distinguish all classes seen so far, without task identity (hardest) |

(van de Ven, Tuytelaars & Tolias, 2022)

## Method families

| Family | Idea | Examples |
|---|---|---|
| Regularisation | Penalise changes to weights important for old tasks | EWC (Kirkpatrick et al., 2017), Synaptic Intelligence, MAS |
| Replay (rehearsal) | Mix stored or generated old examples with new data | Experience replay, iCaRL, generative replay, dark experience replay |
| Parameter isolation / architectural | Dedicate different parameters to different tasks | Progressive networks, PackNet, adapters/LoRA per task |
| Knowledge distillation | Keep new model's outputs close to old model's | LwF (Learning without Forgetting) |
| Pre-trained models + prompts | Freeze a strong backbone; learn small prompts or heads | L2P, CODA-Prompt |

**Elastic Weight Consolidation** adds a quadratic penalty weighted by the Fisher information \(F_i\):

\[
L(\theta) = L_B(\theta) + \sum_i \frac{\lambda}{2} F_i\,(\theta_i - \theta^*_{A,i})^2
\]

— explicitly inspired by synaptic consolidation in the brain.

## Continual learning for LLMs

- Continued pre-training on new domains or fresher data, mixed with replay of general data to avoid forgetting
- Knowledge editing (ROME, MEMIT) for targeted fact updates — brittle at scale
- Retrieval and external memory as a way to "learn" without changing weights
- Fine-tuning can erode safety behaviour or general skills — a practical form of forgetting

## How the brain avoids catastrophic forgetting

- **Complementary learning systems** (McClelland, McNaughton & O'Reilly, 1995): the hippocampus learns fast and sparsely; the neocortex learns slowly and is trained by **interleaved replay** of hippocampal memories, especially during sleep. This is the theoretical origin of experience replay.
- **Synaptic consolidation**: dendritic spines formed during learning can persist for months; selectively stabilised synapses resemble EWC's protected weights.
- **Sparse, context-dependent coding** reduces interference (like parameter isolation); neuromodulators gate when plasticity is allowed.
- **Metaplasticity**: synapses change how plastic they are based on history (Benna & Fusi's cascade models).

See [Memory & Learning in the Brain](../../../brain-mind/memory-learning/index.md).

## Subtopics

- [Regularisation-based methods](regularisation-based/index.md): EWC, synaptic intelligence and learning without forgetting.
- [Replay and memory](replay-and-memory/index.md): exemplar replay, gradient episodic memory and generative replay.
- [Architecture-based methods](architecture-based/index.md): progressive networks, PackNet and expandable networks.
- [Evaluation and scenarios](evaluation-and-scenarios/index.md): task-, domain- and class-incremental settings and forgetting metrics.
- [Neuroscience and continual learning](neuroscience-and-continual-learning/index.md): complementary learning systems and synaptic consolidation.

## Further reading

- Parisi et al. (2019), "Continual lifelong learning with neural networks: A review". https://arxiv.org/abs/1802.07569
- Kudithipudi et al. (2022), "Biological underpinnings for lifelong learning machines", *Nature Machine Intelligence*. https://www.nature.com/articles/s42256-022-00452-0
- Wang et al. (2024), "A Comprehensive Survey of Continual Learning", *IEEE TPAMI*. https://arxiv.org/abs/2302.00487
- [Avalanche](https://avalanche.continualai.org/) library (ContinualAI)

## References

### Seminal papers

- Kirkpatrick et al. (2017), "Overcoming catastrophic forgetting in neural networks", PNAS, [arXiv:1612.00796](https://arxiv.org/abs/1612.00796) — EWC, the influential penalty-based method for protecting old knowledge.
- Li & Hoiem (2016), "Learning without forgetting", ECCV, [arXiv:1606.09282](https://arxiv.org/abs/1606.09282) — Distils earlier outputs to keep old behaviour without storing old data.
- Rebuffi et al. (2017), "iCaRL: incremental classifier and representation learning", CVPR, [arXiv:1611.07725](https://arxiv.org/abs/1611.07725) — Exemplar replay with distillation for class-incremental learning.
- Rusu et al. (2016), "Progressive neural networks", [arXiv:1606.04671](https://arxiv.org/abs/1606.04671) — Adds a frozen-plus-new column per task, which avoids forgetting by design.
- Van de Ven & Tolias (2019), "Three scenarios for continual learning", [arXiv:1904.07734](https://arxiv.org/abs/1904.07734) — Defines the scenarios that most continual learning work is evaluated under.

### Surveys and textbooks

- De Lange et al. (2021), "A continual learning survey: defying forgetting in classification tasks", IEEE TPAMI, [arXiv:1909.08383](https://arxiv.org/abs/1909.08383) — Survey and comparison of the main families of methods under one protocol.
- Parisi, Kemker, Part, Kanan & Wermter (2019), "Continual lifelong learning with neural networks: a review", Neural Networks, [arXiv:1802.07569](https://arxiv.org/abs/1802.07569) — Review that links continual learning to biological learning.
