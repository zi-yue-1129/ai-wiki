---
related:
- brain-mind/snn-neuromorphic
- brain-mind/memory-learning
- models/computer-vision
---

# NeuroAI

**NeuroAI** is the two-way exchange between neuroscience and AI: using brains to inspire better AI, and using AI models to understand brains. Zador et al. (2023, *Nature Communications*), "Catalyzing next-generation AI through NeuroAI", argued for an "embodied Turing test" — AI that matches animals' sensorimotor competence — as the field's grand challenge.

## Direction 1: deep networks as models of the brain

### The task-optimised modelling paradigm

1. Train a network to perform a task animals perform (object recognition, word prediction, navigation).
2. Record neural responses to the same stimuli.
3. Fit a linear mapping from model features to neural responses; measure how well held-out responses are predicted.
4. Compare architectures, objectives and training data.

| System | Key findings |
|---|---|
| Ventral visual stream | Performance-optimised CNNs predict V4 and IT responses better than earlier models; layer depth tracks cortical hierarchy (Yamins et al., 2014; Khaligh-Razavi & Kriegeskorte, 2014) |
| Auditory cortex | Speech/music-trained networks predict auditory cortex with a cortex-like hierarchy (Kell et al., 2018) |
| Language network | Next-word-prediction LLMs predict fMRI/ECoG responses in the language network; better next-word prediction → better brain prediction (Schrimpf et al., 2021) |
| Motor cortex | RNNs trained to produce reaching movements show rotational dynamics like monkey motor cortex (Sussillo et al., 2015) |
| Hippocampal–entorhinal system | Networks trained on path integration develop grid-like units (Banino et al., 2018; Cueva & Wei, 2018) — with caveats about how much the result depends on design choices (Schaeffer et al., 2022) |
| Dopamine | TD learning and distributional RL explain dopamine responses |

**Benchmarks**: [Brain-Score](https://www.brain-score.org/) ranks models by similarity to primate vision and human language data; the Algonauts challenges and the Natural Scenes Dataset (NSD) provide large-scale fMRI benchmarks.

**Methods for comparing representations**: linear encoding models, representational similarity analysis (RSA), centred kernel alignment (CKA), Procrustes / shape metrics.

### Caveats

- **Predictivity is not mechanism**: many different models predict neural data similarly well; high scores can come from generic features.
- **Behavioural mismatches**: networks are vulnerable to adversarial examples and rely on texture more than humans (Bowers et al., 2023, "Deep problems with neural network models of human vision").
- **Biological implausibility**: backprop, weight sharing, and massive labelled data have no obvious biological counterpart — partly addressed by [self-supervised](../../foundations/paradigms/self-supervised/index.md) models that match the ventral stream about as well as supervised ones (Zhuang et al., 2021).

## Direction 2: the brain as inspiration for AI

| Brain principle | AI idea |
|---|---|
| Hierarchical receptive fields | CNNs |
| Dopamine prediction errors, animal learning | Reinforcement learning |
| Hippocampal replay | Experience replay (DQN), generative replay |
| Complementary learning systems | Continual-learning methods; retrieval-augmented models |
| Synaptic consolidation | Elastic weight consolidation |
| Attention and gating | Attention mechanisms, mixture-of-experts routing (loose analogy) |
| Spikes and event-driven processing | Spiking neural networks, neuromorphic chips |
| Dendritic computation | Dendritic neuron models, active-dendrite networks for multitask learning |
| Neuromodulation | Meta-learning of learning rates, context-dependent gating |
| Predictive coding | Self-supervised predictive objectives, JEPA |
| Grid cells and cognitive maps | Structured representations for navigation and abstract reasoning |
| Sparse, energy-efficient coding | Sparsity, activation sparsity, MoE |
| Innate structure from evolution | Inductive biases, meta-learning, "genomic bottleneck" models |

Hassabis et al. (2017, *Neuron*), "Neuroscience-inspired artificial intelligence", is the classic review.

## The credit-assignment problem: how does the brain learn?

Deep learning relies on **backpropagation**, which needs:

1. Symmetric feedback weights (the "weight transport" problem)
2. Separate forward and backward phases
3. Precise error signals delivered to each synapse

None is obviously available in the brain. Proposed biologically plausible alternatives:

| Proposal | Idea |
|---|---|
| Feedback alignment (Lillicrap et al., 2016) | Random fixed feedback weights still allow learning |
| Predictive-coding networks | Local prediction errors approximate backprop gradients (Whittington & Bogacz, 2017) |
| Equilibrium propagation (Scellier & Bengio, 2017) | Contrast two equilibrium states of an energy-based network |
| Dendritic error computation | Errors encoded in apical dendrites of pyramidal cells (Sacramento et al., 2018) |
| Burst-dependent plasticity | Bursts versus single spikes multiplex signals and errors (Payeur et al., 2021) |
| Forward-forward (Hinton, 2022) | Two forward passes, positive and negative data, local objectives |
| Three-factor rules / node perturbation | Reward-modulated local plasticity |

Lillicrap et al. (2020, *Nature Reviews Neuroscience*), "Backpropagation and the brain", argue the brain may approximate backprop-like gradients via feedback-driven activity differences.

## Big differences that remain

| Brain | Current AI |
|---|---|
| ~20 W | Kilowatts to megawatts |
| Learns continually without catastrophic forgetting | Mostly static after training |
| Few-shot learning from little data | Enormous data requirements |
| Embodied, multisensory, social from birth | Mostly disembodied |
| Recurrent, with massive feedback | Mostly feedforward per token |
| Robust to noise and adversarial perturbations | Brittle in specific ways |
| Intrinsic motivation, homeostasis, emotion | Externally specified objectives |

## Where to go next

- [Spiking Networks & Neuromorphic Computing](../snn-neuromorphic/index.md)
- [Memory & Learning in the Brain](../memory-learning/index.md)
- [Brain-Computer Interfaces](../bci/index.md)

## Resources

- [Neuromatch NeuroAI course](https://neuroai.neuromatch.io/) (CC BY 4.0)
- Hassabis et al. (2017), "Neuroscience-Inspired Artificial Intelligence", *Neuron*
- Richards et al. (2019), "A deep learning framework for neuroscience", *Nature Neuroscience*
- Yamins & DiCarlo (2016), "Using goal-driven deep learning models to understand sensory cortex", *Nature Neuroscience*
- Lindsay, *Models of the Mind* (accessible book)
- Doerig et al. (2023), "The neuroconnectionist research programme", *Nature Reviews Neuroscience*
