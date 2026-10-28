---
related:
- brain-mind/neuroai
- brain-mind/snn-neuromorphic
aliases:
  - 計算神經科學
  - 理論神經科學
  - Theoretical neuroscience
---

# Computational Neuroscience

Understanding **how the nervous system computes** with mathematical models, simulation and data analysis.

## Marr's three levels

David Marr's *Vision* (1982) proposed three levels for understanding any information-processing system — still a shared framework for AI and neuroscience:

| Level | Question | Example (edge detection) | AI counterpart |
|---|---|---|---|
| Computational | What problem is solved, and why? | Find places where image intensity changes sharply | Objective / loss |
| Algorithmic / representational | What representations and algorithms? | Laplacian-of-Gaussian filtering, zero crossings | Architecture, learning rule |
| Implementational | How is it physically realised? | Retinal ganglion cells, V1 simple cells | GPUs, neuromorphic chips |

Richards et al. (2019, *Nature Neuroscience*), "A deep learning framework for neuroscience", propose studying the brain via **objective functions, learning rules and architectures** — a framing borrowed directly from deep learning.

## Neuron models

| Model | Complexity | Description |
|---|---|---|
| McCulloch–Pitts | Minimal | Binary threshold unit |
| Rate model | Simple | Output is firing rate; like an artificial neuron |
| Leaky integrate-and-fire (LIF) | Simple | Integrates input with leak; spikes and resets at threshold — basis of SNNs |
| Izhikevich | Moderate | Two variables reproduce many firing patterns |
| Hodgkin–Huxley | High | Ion-channel dynamics of the action potential (Nobel Prize 1963) |
| Multi-compartment | Very high | Detailed dendritic morphology |

LIF dynamics:

![Animated leaky integrate-and-fire neuron: discrete input spikes integrate into membrane voltage, trigger threshold crossing and reset, producing output spikes.](../../assets/concept-animations/lif-neuron.gif)

*Leaky integrate-and-fire (LIF) illustration (original schematic, CC BY-SA 4.0).* Input events increment the membrane voltage, which leaks down between events. When it reaches the threshold the neuron emits a spike and the voltage resets. This simplified discrete-time simulation illustrates the mechanism; it is not a biological recording.


\[
\tau_m \frac{dV}{dt} = -(V - V_{rest}) + R\,I(t), \quad V \geq V_{th} \Rightarrow \text{spike}, \; V \leftarrow V_{reset}
\]

## Neural coding and decoding

- **Encoding**: stimulus → response. Tuning curves, receptive fields, linear–nonlinear–Poisson (LNP) models, generalised linear models (GLMs); increasingly, deep networks as encoding models
- **Decoding**: response → stimulus or intention. Linear and Bayesian decoders, deep networks; the core of [BCIs](../bci/index.md)
- **Population coding**: information is distributed across many neurons
- **Efficient and sparse coding**: Olshausen & Field (1996) learned a sparse code for natural images and obtained V1-simple-cell-like receptive fields — a classic case of unsupervised learning explaining neural properties

## Network dynamics

- **Attractor networks**: Hopfield networks (memory), continuous attractors (head-direction cells, working memory)
- **Excitation–inhibition balance**
- **Reservoir computing** (echo-state networks, liquid-state machines)
- **Neural manifolds and low-dimensional dynamics**: high-dimensional activity often lies on low-dimensional manifolds; training RNNs on cognitive tasks and reverse-engineering their dynamics generates hypotheses about prefrontal cortex (Mante et al., 2013; Sussillo & Barak, 2013)
- **Criticality hypothesis**: the brain may operate near the edge between order and chaos

## Learning rules

| Rule | Description |
|---|---|
| Hebbian | Co-active synapses strengthen: \(\Delta w \propto x_{pre}\,x_{post}\) |
| Oja's rule | Normalised Hebbian learning; extracts the first principal component |
| BCM | Plasticity with a sliding threshold |
| STDP | Pre-before-post spikes strengthen; post-before-pre weaken |
| Three-factor rules | Hebbian term × a third modulatory signal (e.g. dopamine), linking local plasticity to reward |

## Normative models

Derive what the brain *should* do by optimising an objective, then compare with data: efficient coding, Bayesian observers, optimal control, reinforcement learning, resource rationality.

## Key methods

Each method has its own page. The overview and comparison here are brief.

### Hodgkin–Huxley model (Hodgkin & Huxley, 1952)

- **Overview:** A conductance-based model of the neuron's membrane voltage, built from ion channels and gating variables.
- **Comparison:** The most detailed biophysical neuron model. Simpler spiking models such as Izhikevich's trade biophysical detail for speed.
- **Full write-up:** [Hodgkin–Huxley Model](hodgkin-huxley/index.md)

### Sparse coding (Olshausen & Field, 1996)

- **Overview:** Natural image patches are described as sparse combinations of learned basis functions.
- **Comparison:** The same idea reappears in the early layers of deep vision networks, so it links this page to the neuroAI page.
- **Full write-up:** [Sparse Coding](sparse-coding/index.md)

## Tools and data

- Simulators: [NEURON](https://neuron.yale.edu/), [NEST](https://www.nest-simulator.org/), [Brian2](https://briansimulator.org/)
- Analysis: [MNE-Python](https://mne.tools/) (EEG/MEG), [Nilearn](https://nilearn.github.io/) (fMRI), [SpikeInterface](https://spikeinterface.readthedocs.io/)
- Data standards and archives: [NWB](https://www.nwb.org/), [DANDI Archive](https://dandiarchive.org/), [OpenNeuro](https://openneuro.org/), Allen Brain Atlas and Allen Brain Observatory

## Resources

- Dayan & Abbott, *Theoretical Neuroscience*
- Gerstner et al., *Neuronal Dynamics* ([full text online](https://neuronaldynamics.epfl.ch/))
- [Neuromatch Academy Computational Neuroscience](https://compneuro.neuromatch.io/) (CC BY 4.0; strongly recommended)
- Marr, *Vision*
- Artem Kirsanov's YouTube channel (visual computational-neuroscience explainers)

## References

### Seminal papers

- Hodgkin, A. L. & Huxley, A. F. (1952). A quantitative description of membrane current and its application to conduction and excitation in nerve. *The Journal of Physiology*. https://doi.org/10.1113/jphysiol.1952.sp004764 — Derives the four-variable conductance model of the action potential, the basis of most biophysical neuron models.
- Izhikevich, E. M. (2003). Simple model of spiking neurons. *IEEE Transactions on Neural Networks*. https://doi.org/10.1109/TNN.2003.820440 — A two-variable model that reproduces many cortical firing patterns at low computational cost.
- Olshausen, B. A. & Field, D. J. (1996). Emergence of simple-cell receptive field properties by learning a sparse code for natural images. *Nature*. https://doi.org/10.1038/381607a0 — Shows that a sparse code for natural images yields oriented, localised filters like V1 simple cells.
- Richards, B. A. et al. (2019). A deep learning framework for neuroscience. *Nature Neuroscience*. https://doi.org/10.1038/s41593-019-0520-2 — Argues for studying the brain through objective functions, learning rules and architectures.

### Surveys and textbooks

- Gerstner, W., Kistler, W. M., Naud, R. & Paninski, L. (2014). *Neuronal Dynamics*. Cambridge University Press. https://neuronaldynamics.epfl.ch/ — Free online textbook, from single neuron models to networks and learning rules.
