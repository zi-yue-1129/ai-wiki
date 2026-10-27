# Learning Paths

Pick the path that fits your background. Each stop links to a page on this site; each page ends with external courses and books.

## Path A: No background, want a broad understanding

1. [What is AI](../index.md) → [History of AI](../history/index.md)
2. [Machine Learning](../../foundations/machine-learning/index.md) (read the intuition, skip the equations)
3. [Deep Learning](../../foundations/deep-learning/index.md)
4. [Large Language Models](../../models/llm/index.md) → [Prompt Engineering](../../engineering/prompting/index.md)
5. Two [application areas](../../applications/index.md) you care about
6. [Safety & Alignment](../../society/safety-alignment/index.md), [Ethics & Fairness](../../society/ethics/index.md)

**Recommended outside resources:** Microsoft *AI for Beginners*; 3Blue1Brown's neural network videos.

## Path B: Software engineer → AI engineer

1. [Mathematics](../../foundations/math/index.md) (linear algebra, probability, optimisation are enough)
2. [Machine Learning](../../foundations/machine-learning/index.md) → [Deep Learning](../../foundations/deep-learning/index.md)
3. [Transformers](../../models/transformer/index.md) → [Large Language Models](../../models/llm/index.md)
4. [Frameworks & Tools](../../engineering/frameworks/index.md) → [Training & Fine-tuning](../../engineering/training/index.md)
5. [RAG](../../engineering/rag/index.md) → [AI Agents](../../models/agents/index.md)
6. [Evaluation](../../engineering/evaluation/index.md) → [MLOps & Deployment](../../engineering/mlops/index.md)

**Hands-on milestones:** train MNIST from scratch in PyTorch → train a small language model with nanoGPT → LoRA-fine-tune an open-weight LLM → build a tool-using RAG agent with its own evaluation set.

## Path C: Researcher (ML theory and frontier)

1. [Mathematics](../../foundations/math/index.md) including information theory and convex optimisation
2. [Probabilistic & Bayesian Methods](../../foundations/probabilistic/index.md)
3. Theory sections of [Deep Learning](../../foundations/deep-learning/index.md) (generalisation, double descent, scaling laws)
4. [Generative Models](../../models/generative/index.md) (diffusion, flow matching)
5. [Reinforcement Learning](../../foundations/paradigms/reinforcement-learning/index.md) → [World Models](../../models/world-models/index.md)
6. [Interpretability](../../society/interpretability/index.md) → [Safety & Alignment](../../society/safety-alignment/index.md)
7. [Landmark Papers](../../reference/papers/index.md)

## Path D: Neuroscience / psychology background → AI

1. [Machine Learning](../../foundations/machine-learning/index.md) and [Deep Learning](../../foundations/deep-learning/index.md): read neural networks as radically simplified neuron models
2. [Computational Neuroscience](../../brain-mind/computational-neuroscience/index.md): how your field gets formalised
3. [NeuroAI](../../brain-mind/neuroai/index.md): deep networks as brain models, brains as inspiration for AI
4. [Reinforcement Learning](../../foundations/paradigms/reinforcement-learning/index.md): dopamine and temporal-difference learning
5. [Spiking Networks & Neuromorphic Computing](../../brain-mind/snn-neuromorphic/index.md)
6. [Cognitive Architectures](../../brain-mind/cognitive-architectures/index.md), [Psychology & AI](../../brain-mind/psychology/index.md)
7. [Brain-Computer Interfaces](../../brain-mind/bci/index.md)

**Recommended outside resources:** Neuromatch Academy's *Computational Neuroscience* and *NeuroAI* courses (fully open).

## Path E: AI → brain and cognitive science

1. [Neuroscience Basics](../../brain-mind/neuroscience/index.md)
2. [Memory & Learning in the Brain](../../brain-mind/memory-learning/index.md)
3. [Cognitive Science](../../brain-mind/cognitive-science/index.md) → [Psychology & AI](../../brain-mind/psychology/index.md)
4. [NeuroAI](../../brain-mind/neuroai/index.md) → [Consciousness](../../brain-mind/consciousness/index.md)

## Path F: Domain professionals

1. [What is AI](../index.md) → [Large Language Models](../../models/llm/index.md) → [Prompt Engineering](../../engineering/prompting/index.md)
2. The [application page](../../applications/index.md) for your field
3. [RAG](../../engineering/rag/index.md) (connecting your organisation's knowledge to an LLM)
4. [Law, Policy & Governance](../../society/governance/index.md), [Ethics & Fairness](../../society/ethics/index.md)

## Self-check

- [ ] Explain overfitting, the bias–variance trade-off and cross-validation
- [ ] Derive backpropagation for a one-hidden-layer network by hand
- [ ] Explain what Q, K and V are in attention
- [ ] Distinguish pre-training, instruction tuning, and RLHF/DPO
- [ ] Name three similarities and three differences between brains and deep networks
- [ ] Explain the link between the TD error and dopamine neurons
- [ ] Design an evaluation set for a task and explain the contamination risk
- [ ] List the three main risks of deploying AI in your own field
