---
related:
- brain-mind/memory-learning
- theory/models/llm
---

# Meta-Learning & Few-Shot Learning

## Idea

**Learning to learn**: train on a *distribution of tasks* so that a new task can be learned from very few examples. Few-shot learning is the most common goal: recognise a new class from 1–5 examples ("N-way K-shot").

## Families

| Family | Idea | Examples |
|---|---|---|
| Metric-based | Learn an embedding where a nearest-neighbour or prototype rule works | Siamese networks, Matching Networks, Prototypical Networks |
| Optimisation-based | Learn an initialisation (or optimiser) that adapts in a few gradient steps | MAML, Reptile, learned optimisers |
| Model-based / black-box | A sequence model ingests examples and outputs predictions | Memory-augmented networks, SNAIL, RL² |
| Bayesian / hierarchical | Learn a prior shared across tasks | Neural processes, hierarchical Bayes |
| In-context learning | A large pre-trained Transformer learns from examples in its prompt | GPT-3 and later LLMs |

**MAML** (Finn et al., 2017) finds parameters \(\theta\) such that one or a few gradient steps on a new task's small dataset give good performance:

\[
\min_\theta \sum_{\mathcal{T}} L_{\mathcal{T}}\big(\theta - \alpha \nabla_\theta L_{\mathcal{T}}(\theta)\big)
\]

## In-context learning as emergent meta-learning

Large language models, trained only on next-token prediction, can learn tasks from a few examples in the prompt. Research suggests Transformers can implement learning algorithms (such as gradient-descent-like updates for linear regression) inside their forward pass (Garg et al., 2022; von Oswald et al., 2023), and that data with "bursty", Zipfian structure promotes in-context learning (Chan et al., 2022). Pre-training on the internet is, in effect, meta-training on millions of implicit tasks.

## Related ideas

- **Hyperparameter optimisation and AutoML** — learning the learning configuration
- **Neural architecture search**
- **Learned optimisers** (VeLO)
- **Meta-reinforcement learning** — agents that adapt to new environments within an episode

## Brain and cognition

- **Harlow's learning sets (1949)**: monkeys solving many two-object discrimination problems got faster and faster at new ones — the original demonstration of learning to learn.
- **Prefrontal cortex as a meta-RL system** (Wang et al., 2018, *Nature Neuroscience*): slow dopamine-driven learning trains a recurrent prefrontal network that then implements its own fast learning algorithm in its activity dynamics.
- **One-shot human learning**: people learn new handwritten characters from one example; Bayesian program learning (Lake, Salakhutdinov & Tenenbaum, 2015) and the Omniglot benchmark were designed to capture this.
- **Inductive biases from evolution**: evolution is the outer loop and lifetime learning the inner loop — a meta-learning perspective on innate structure.
- **Hippocampus** supports rapid one-shot episodic learning; see [Memory & Learning](../../../brain-mind/memory-learning/index.md).

## Subtopics

- [Optimisation-based meta-learning](optimisation-based/index.md): MAML, Reptile and latent-space adaptation.
- [Metric-based few-shot learning](metric-based/index.md): matching and prototypical networks, relation networks.
- [Memory- and model-based meta-learning](memory-and-model-based/index.md): memory-augmented, attentive and hypernetwork learners.
- [Meta-learning theory](meta-learning-theory/index.md): why learning across tasks reduces the data needed per task.
- [Benchmarks and foundation models](benchmarks-and-foundation-models/index.md): few-shot benchmarks and in-context learning in large models.

## Further reading

- Hospedales et al. (2021), "Meta-Learning in Neural Networks: A Survey". https://arxiv.org/abs/2004.05439
- Finn et al. (2017), MAML. https://arxiv.org/abs/1703.03400
- Snell et al. (2017), Prototypical Networks. https://arxiv.org/abs/1703.05175
- Lake et al. (2017), "Building machines that learn and think like people", *Behavioral and Brain Sciences*. https://arxiv.org/abs/1604.00289
- Stanford CS330, *Deep Multi-Task and Meta Learning*. https://cs330.stanford.edu

## References

### Seminal papers

- Finn, Abbeel & Levine (2017), "Model-agnostic meta-learning for fast adaptation of deep networks", ICML, [arXiv:1703.03400](https://arxiv.org/abs/1703.03400) — MAML, the foundational gradient-based meta-learning method.
- Snell, Swersky & Zemel (2017), "Prototypical networks for few-shot learning", NeurIPS, [arXiv:1703.05175](https://arxiv.org/abs/1703.05175) — Classifies by distance to class prototypes computed from a few examples.
- Vinyals et al. (2016), "Matching networks for one shot learning", NeurIPS, [arXiv:1606.04080](https://arxiv.org/abs/1606.04080) — Introduces episodic training with attention over a labelled support set.
- Santoro et al. (2016), "Meta-learning with memory-augmented neural networks", ICML. https://proceedings.mlr.press/v48/santoro16.html — Uses an external memory to learn fast, one-shot adaptation.
- Baxter (2000), "A model of inductive bias learning", Journal of Artificial Intelligence Research. https://jair.org/index.php/jair/article/download/10253/24418 — Formal model of learning the inductive bias from a family of tasks.

### Surveys and textbooks

- Hospedales, Antoniou, Micaelli & Storkey (2021), "Meta-learning in neural networks: a survey", IEEE TPAMI, [arXiv:2004.05439](https://arxiv.org/abs/2004.05439) — Broad survey of meta-learning, covering all the families on this page.
