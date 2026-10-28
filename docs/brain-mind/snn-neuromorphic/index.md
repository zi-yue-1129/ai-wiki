---
related:
- engineering/hardware
aliases:
  - SNN
  - 脈衝神經網路
  - 神經形態運算
  - Neuromorphic computing
---

# Spiking Neural Networks & Neuromorphic Computing

## Why spikes?

Biological neurons communicate with brief, discrete **spikes**. Spiking neural networks (SNNs) — sometimes called the "third generation" of neural networks (Maass, 1997) — model this explicitly. The appeal:

- **Energy efficiency**: computation happens only when spikes occur (event-driven), and spikes are binary
- **Temporal coding**: timing itself can carry information
- **Biological fidelity**: a bridge between neuroscience models and machine learning
- **Natural fit to event-based sensors** (dynamic vision sensors, silicon cochleas)

## Neuron models used in SNNs

| Model | Notes |
|---|---|
| Leaky integrate-and-fire (LIF) | The workhorse; see [Computational Neuroscience](../computational-neuroscience/index.md) |
| Adaptive LIF / ALIF | Adds spike-frequency adaptation; improves temporal tasks (Bellec et al., 2018) |
| Izhikevich | Rich firing patterns at low cost |
| Resonate-and-fire | Oscillatory dynamics |
| Hodgkin–Huxley | Too expensive for large SNNs; used for detailed modelling |

## Spike coding schemes

| Scheme | Information carried by |
|---|---|
| Rate coding | Number of spikes in a window |
| Time-to-first-spike / latency | When the first spike arrives |
| Phase coding | Spike timing relative to an oscillation |
| Population / rank-order coding | Which neurons spike, in what order |
| Delta / event coding | Changes in the input |

## Training SNNs

The spike is a step function, so its derivative is zero almost everywhere — backprop doesn't directly apply.

| Approach | Idea | Tools |
|---|---|---|
| ANN-to-SNN conversion | Train a normal network, map activations to firing rates | Good accuracy, but often needs many time steps |
| Surrogate gradients | Use a smooth stand-in derivative in the backward pass; backprop through time (Neftci, Mostafa & Zenke, 2019) | snnTorch, SpikingJelly, Norse, Lava-DL |
| Local / biologically plausible rules | STDP, three-factor rules, e-prop (Bellec et al., 2020) | Online learning on chip |
| Exact spike-time gradients | EventProp and related methods | Event-based training |
| Evolutionary / reservoir approaches | Liquid state machines | Few trained parameters |

### Spike-timing-dependent plasticity (STDP)

If a presynaptic spike precedes a postsynaptic spike by Δt > 0, the synapse strengthens; if it follows, it weakens — typically with an exponential window of tens of milliseconds (Bi & Poo, 1998). STDP alone performs unsupervised feature learning; combined with a reward signal (reward-modulated STDP) it supports reinforcement learning.

## Neuromorphic hardware

| Chip / system | Organisation | Notes |
|---|---|---|
| TrueNorth | IBM (2014) | 1 million neurons, ~70 mW |
| Loihi / Loihi 2 | Intel (2017 / 2021) | On-chip learning; Hala Point system (2024) with ~1.15 billion neurons |
| SpiNNaker / SpiNNaker 2 | University of Manchester / TU Dresden | Many ARM cores for real-time brain simulation |
| BrainScaleS | Heidelberg | Analogue, accelerated (faster than biological time) |
| Akida | BrainChip | Commercial edge AI |
| Speck / Xylo | SynSense | Ultra-low-power vision and audio |
| Tianjic | Tsinghua University | Hybrid ANN/SNN chip (Nature, 2019) |
| Darwin series | Zhejiang University | Large-scale neuromorphic systems |

Related: **in-memory computing** with memristors and phase-change memory, which stores weights where computation happens — like synapses.

## Where SNNs shine (and don't)

**Good fits**: always-on sensing (keyword spotting, gesture recognition, anomaly detection), event-camera vision, robotics with tight power budgets, brain-computer interfaces and implants, predictive maintenance on vibration signals, real-time brain simulation.

**Challenges**: accuracy gap to ANNs on large benchmarks has narrowed but persists in places; training is slower; tooling and hardware are fragmented; energy gains depend heavily on spike sparsity and the hardware actually used — benchmark carefully. Spiking versions of Transformers and LLMs (e.g. Spikformer, SpikeGPT) are active research.

## Event-based sensors

**Dynamic vision sensors** (event cameras) output per-pixel brightness changes asynchronously with microsecond latency and high dynamic range — inspired by the retina. Natural partners for SNNs in drones, robotics and high-speed tracking.

## Key methods

Each method has its own page. The overview and comparison here are brief.

### Surrogate gradients (Neftci, Mostafa & Zenke, 2019)

- **Overview:** Spiking networks are trained with backpropagation by replacing the threshold's derivative with a smooth surrogate.
- **Comparison:** The practical route to deep-style training of spiking networks. E-prop below is a local, more biologically plausible alternative.
- **Full write-up:** [Surrogate Gradients](surrogate-gradients/index.md)

### Online learning with local updates: e-prop (Bellec et al., 2020)

- **Overview:** Learning uses local eligibility traces and a learning signal, instead of backpropagation through time.
- **Comparison:** Trades some gradient accuracy for locality and online updates. Surrogate gradients above use backpropagation through time.
- **Full write-up:** [Online Learning with Local Updates (e-prop)](eprop/index.md)

## Resources

- Eshraghian et al. (2023), "Training Spiking Neural Networks Using Lessons From Deep Learning", *Proceedings of the IEEE*, with the [snnTorch](https://snntorch.readthedocs.io/) tutorials
- Roy, Jaiswal & Panda (2019), "Towards spike-based machine intelligence with neuromorphic computing", *Nature*
- Schuman et al. (2022), "Opportunities for neuromorphic computing algorithms and applications", *Nature Computational Science*
- Gerstner et al., *Neuronal Dynamics* (free online)
- [Open Neuromorphic](https://open-neuromorphic.org/) community
- Frameworks: [snnTorch](https://github.com/jeshraghian/snntorch), [SpikingJelly](https://github.com/fangwei123456/spikingjelly), [Norse](https://github.com/norse/norse), [Lava](https://github.com/lava-nc/lava), [Brian2](https://briansimulator.org/)

## References

### Seminal papers

- Neftci, E. O., Mostafa, H. & Zenke, F. (2019). Surrogate Gradient Learning in Spiking Neural Networks. *IEEE Signal Processing Magazine*. https://doi.org/10.1109/MSP.2019.2931595 — Introduces surrogate gradients, which let spiking networks be trained with backpropagation through time.
- Bellec, G., et al. (2020). A solution to the learning dilemma for recurrent networks of spiking neurons. *Nature Communications*. https://doi.org/10.1038/s41467-020-17236-y — The e-prop learning rule, an online approximation to backpropagation through time for spiking networks.

### Surveys and textbooks

- Eshraghian, J. K., et al. (2023). Training Spiking Neural Networks Using Lessons From Deep Learning. *Proceedings of the IEEE*. https://doi.org/10.1109/JPROC.2023.3308088 — A tutorial on training spiking networks with deep-learning tools, with the snnTorch examples.
- Roy, K., Jaiswal, A. & Panda, P. (2019). Towards spike-based machine intelligence with neuromorphic computing. *Nature*. https://doi.org/10.1038/s41586-019-1677-2 — A review of spike-based computation and neuromorphic hardware.
- Gerstner, W., Kistler, W. M., Naud, R. & Paninski, L. (2014). *Neuronal Dynamics*. Cambridge University Press. https://neuronaldynamics.epfl.ch/ — Free online textbook on spiking neuron models and networks.
