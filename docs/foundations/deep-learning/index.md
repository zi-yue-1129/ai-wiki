---
related:
- brain-mind/neuroai
- brain-mind/neuroscience
- models/transformer
- foundations/paradigms/self-supervised
---

# Deep Learning

## Intuition

Deep learning composes **many layers of differentiable functions** to learn useful **representations** directly from raw data (pixels, text, waveforms). Early layers learn edges or phonemes; deeper layers learn objects and meanings. This hierarchy bears a striking resemblance to the primate visual stream (V1 → V2 → V4 → IT); see [NeuroAI](../../brain-mind/neuroai/index.md).

## The artificial neuron

\[
y = \sigma\Big(\sum_i w_i x_i + b\Big)
\]

| Biological neuron | Artificial neuron |
|---|---|
| Dendrites receive input | Inputs \(x_i\) |
| Synaptic strength | Weights \(w_i\) |
| Soma integrates | Weighted sum |
| Fires an action potential above threshold | Nonlinear activation \(\sigma\) |
| Codes with spike rates and timing | Outputs a real number (spiking versions: [SNNs](../../brain-mind/snn-neuromorphic/index.md)) |

!!! warning "Limits of the analogy"
    Real dendrites perform nonlinear computation themselves; simulating a single cortical pyramidal neuron's input–output behaviour can require a 5–8-layer deep network (Beniaguev et al., 2021). The artificial neuron is an extreme abstraction.

### Activation functions

| Function | Formula | Notes |
|---|---|---|
| Sigmoid | \(1/(1+e^{-x})\) | Early default; saturates → vanishing gradients |
| Tanh | \(\tanh x\) | Zero-centred |
| ReLU | \(\max(0,x)\) | Simple and effective; CNN default |
| GELU / SiLU | \(x\Phi(x)\) / \(x\sigma(x)\) | Common in Transformers |
| SwiGLU | Gated variant | Common in modern LLMs |

## Training: backpropagation and gradient descent

1. **Forward pass**: compute predictions layer by layer.
2. **Loss**: compare with targets (cross-entropy, mean squared error).
3. **Backward pass**: apply the chain rule from output to input to get every parameter's gradient.
4. **Update**: an optimiser (SGD, AdamW) moves parameters against the gradient.

!!! question "Does the brain do backpropagation?"
    Exact backprop needs symmetric feedback weights and separate forward/backward phases — biologically implausible. Candidate alternatives: feedback alignment, predictive-coding networks, equilibrium propagation, dendritic error computation, burst-dependent plasticity, and the forward-forward algorithm. See [NeuroAI](../../brain-mind/neuroai/index.md).

## Architectures

| Architecture | Inductive bias | Typical use | See |
|---|---|---|---|
| Multi-layer perceptron | None in particular | Tabular data, inside Transformers | — |
| Convolutional network (CNN) | Locality, translation equivariance | Images, audio | [Computer Vision](../../models/computer-vision/index.md) |
| Recurrent network (RNN/LSTM/GRU) | Sequential order, recurrent state | Sequences, time series | [NLP](../../models/nlp/index.md) |
| Transformer | Global attention, permutation equivariance (+ positions) | Almost every modality | [Transformers](../../models/transformer/index.md) |
| State-space models (S4, Mamba) | Linear recurrence, efficient long sequences | Long sequences, audio, genomics | [Transformers](../../models/transformer/index.md) |
| Graph neural network | Graph structure, permutation invariance | Molecules, social networks | [GNNs](../../models/gnn/index.md) |
| Autoencoder / VAE | Bottleneck compression | Representation learning, generation | [Generative Models](../../models/generative/index.md) |
| Diffusion model | Iterative denoising | Images, video, molecules | [Generative Models](../../models/generative/index.md) |

## Tricks that make deep networks trainable

- **Initialisation**: Xavier/Glorot, He
- **Normalisation**: BatchNorm, LayerNorm, RMSNorm
- **Residual connections** (ResNet): gradients flow through hundreds of layers
- **Dropout**, weight decay, data augmentation
- **Optimisation**: AdamW, warmup + cosine decay, gradient clipping
- **Mixed precision**: BF16/FP16/FP8
- **Distributed training**: data, tensor and pipeline parallelism; ZeRO/FSDP

## Representation learning and self-supervision

Deep learning's real power is **learning representations**. The biggest shift of recent years is [self-supervised learning](../paradigms/self-supervised/index.md): creating training signals from unlabelled data — masked prediction (BERT, MAE), next-token prediction (GPT), contrastive learning (SimCLR, CLIP), joint-embedding prediction (JEPA).

This echoes **predictive processing** theories of the brain, in which the cortex continuously predicts its input and learns from prediction errors (see [Cognitive Science](../../brain-mind/cognitive-science/index.md)).

## Scaling laws

Kaplan et al. (2020) and Hoffmann et al. (2022, "Chinchilla") found that language-model loss falls as a **power law** in parameters, data and compute. Chinchilla suggested that for a fixed compute budget, parameters and training tokens should grow together (roughly 20 tokens per parameter). In practice, models are often trained far beyond that ratio to make inference cheaper.

Since 2024, **test-time compute scaling** — letting models think longer before answering (long chains of thought, search, sampling and voting) — has become a second reliable axis of improvement for reasoning.

## Open theoretical questions

- Why do over-parameterised networks generalise? (implicit regularisation, flat minima, neural tangent kernel)
- **Grokking**: sudden generalisation long after the training loss has converged
- **Emergent abilities**: genuine phase transitions or artefacts of discontinuous metrics? (Schaeffer et al., 2023)
- **Representational convergence**: do different models and modalities converge on similar representations of the world? (Huh et al., 2024, "Platonic representation hypothesis")

## Resources

- [Dive into Deep Learning](https://d2l.ai/) (CC BY-SA 4.0; strongly recommended)
- [Understanding Deep Learning](https://udlbook.github.io/udlbook/) (free PDF)
- Andrej Karpathy, *Neural Networks: Zero to Hero*
- Stanford CS231n (vision), CS224n (NLP)
- fast.ai, *Practical Deep Learning for Coders*
