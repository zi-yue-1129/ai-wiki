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

### Hodgkin–Huxley model (Hodgkin & Huxley, 1952)

- **Problem:** how the action potential arises from ion movements across the membrane of the squid giant axon.
- **Core idea:** the membrane is a capacitor in parallel with voltage-gated sodium and potassium conductances and a leak. Three gating variables (m, h, n) each relax toward a voltage-dependent value, and they control the conductances.
- **Equations** (modern sign convention):

\[
C\frac{dV}{dt} = I - g_{Na}\,m^3 h\,(V - E_{Na}) - g_K\,n^4\,(V - E_K) - g_L\,(V - E_L)
\]

\[
\frac{dx}{dt} = \alpha_x(V)\,(1 - x) - \beta_x(V)\,x, \qquad x \in \{m, h, n\}
\]

- **Results:** the simulated action potential matches the shape of recordings from the squid axon, and the model reproduces how the spike propagates along the axon.
- **Limitations:** fitted to one preparation at one temperature, with no dendritic structure. Four coupled equations per compartment are costly for large networks, which is why the simpler leaky integrate-and-fire and Izhikevich models in the table above are so common.

### Sparse coding (Olshausen & Field, 1996)

- **Problem:** why neurons in primary visual cortex (V1) respond to oriented edges at particular positions.
- **Core idea:** a natural image patch is described as a weighted sum of a few basis functions with sparse coefficients. The basis functions are learned from unlabelled images.
- **Equation:** for each patch, find coefficients \(a_i\) and basis functions \(\phi_i\) that minimise

\[
E = \Big\| I - \sum_i a_i \phi_i \Big\|^2 + \lambda \sum_i S(a_i)
\]

  where \(S\) is a sparseness penalty that favours few active coefficients.
- **Results:** the learned basis functions are localised, oriented and band-pass, resembling the simple-cell receptive fields of V1.
- **Limitations:** a linear generative model that leaves out complex cells, temporal dynamics and top-down influences. Sparse coding is one normative account among several, not a full model of V1.

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
