---
related:
- brain-mind/computational-neuroscience
- brain-mind/bci
aliases:
  - 神經科學
  - 腦科學
---

# Neuroscience Basics

## A sense of scale

| Item | Approximate number |
|---|---|
| Neurons in the human brain | ~86 billion |
| Neurons in cerebral cortex | ~16 billion |
| Neurons in cerebellum | ~69 billion |
| Synapses | ~10¹⁴–10¹⁵ |
| Glial cells | Roughly as many as neurons |
| Power | ~20 W |
| Mass | ~1.4 kg (≈2% of body weight, ≈20% of energy use) |

For comparison: frontier LLMs have hundreds of billions to trillions of parameters. If each synapse counted as one parameter, the brain would still be hundreds of times larger — and each synapse is a complex biochemical machine, not a single number.

## The neuron

```mermaid
flowchart LR
  D[Dendrites<br/>receive input] --> S[Soma<br/>integrates]
  S --> AH[Axon hillock<br/>decides to fire]
  AH --> AX[Axon<br/>conducts action potential]
  AX --> T[Terminals<br/>release neurotransmitter]
  T -.synapse.-> D2[Next neuron's dendrites]
```

- **Resting potential** ≈ −70 mV
- **Action potential**: when the membrane crosses threshold (≈ −55 mV), sodium rushes in and potassium flows out, producing an all-or-none ~1 ms spike
- **Coding**: information can be carried by firing rate, precise spike timing, or population activity
- **Cell types**: excitatory pyramidal cells (~80% of cortical neurons) and many inhibitory interneuron classes (PV, SST, VIP, …)
- **Dendrites compute**: active dendritic spikes let a single neuron perform nonlinear operations such as XOR (Gidon et al., 2020)

## Synapses and neurotransmitters

| Substance | Main roles |
|---|---|
| Glutamate | Main excitatory transmitter; learning and memory (NMDA, AMPA receptors) |
| GABA | Main inhibitory transmitter |
| Dopamine | Reward-prediction error, motivation, movement (Parkinson's disease) |
| Serotonin | Mood, patience, sleep |
| Norepinephrine | Arousal, attention, explore/exploit |
| Acetylcholine | Attention, learning, muscle control |

**Neuromodulators** (dopamine, serotonin, norepinephrine, acetylcholine) do not simply relay messages; they reconfigure how whole circuits operate and learn. Doya (2002) proposed they correspond to RL meta-parameters: TD error, discount factor, exploration temperature and learning rate respectively — a classic computational theory of neuromodulation.

## Major brain regions

| Region | Function | AI counterpart |
|---|---|---|
| Occipital visual cortex (V1–V4, IT) | Visual processing hierarchy | CNNs, ViTs |
| Temporal lobe | Hearing, language comprehension, object recognition, memory | Speech and language models |
| Parietal lobe | Space, attention, sensory integration | Multimodal integration |
| Frontal / prefrontal cortex | Planning, working memory, decision making, executive control | Planner / controller of an agent |
| Motor cortex | Movement planning and execution | Robot control |
| Hippocampus | Episodic memory, navigation, replay | Experience replay, memory-augmented networks, retrieval |
| Basal ganglia (striatum etc.) | Action selection, habits, reinforcement learning | Actor–critic |
| Cerebellum | Coordination, prediction, timing | Supervised learning, forward models |
| Thalamus | Sensory relay, attentional gating | Routing and gating |
| Amygdala | Emotion, fear learning | Value assessment |
| Language network (left fronto-temporal) | Language comprehension and production | LLMs |

### Cortical organisation

- Six layers with repeating **cortical columns** (Mountcastle) — the basis of the hypothesis that cortex runs a common algorithm (Hawkins' "thousand brains" theory builds on this)
- Massive **feedback** connections: top-down connections rival or outnumber feedforward ones — something most feedforward deep networks lack
- **Sparse activity**: few neurons are active at any moment, saving energy

## Methods

| Method | Spatial resolution | Temporal resolution | Invasive? |
|---|---|---|---|
| fMRI | mm | seconds | No |
| EEG | cm | ms | No |
| MEG | sub-cm | ms | No |
| fNIRS | cm | seconds | No |
| ECoG | mm | ms | Requires surgery |
| Single-unit recording / Neuropixels probes | Single cells | Sub-ms | Yes |
| Calcium imaging | Single cells | Tens of ms | Yes (animals) |
| Optogenetics | Genetically targeted cell types | ms | Yes (animals) — lets you *control*, not just observe |
| Electron-microscopy connectomics | nm | — | Post-mortem tissue |

**AI is now a core tool of neuroscience**: automated segmentation for connectomes, DeepLabCut for pose tracking, Kilosort for spike sorting, decoding images from fMRI, and foundation models trained on large neural datasets to predict activity across animals and stimuli.

## Brain vs computer

| Aspect | Brain | Digital computer / GPU |
|---|---|---|
| Unit speed | Slow (ms) | Fast (ns) |
| Parallelism | Massive | High |
| Memory and compute | Co-located (synapses) | Separated (von Neumann bottleneck) |
| Signals | Analogue + spikes, noisy | Digital, precise |
| Energy | ~20 W | Frontier training runs use data centres drawing tens of MW |
| Learning | Continual, local, few-shot | Mostly offline batches with global backprop |
| Fault tolerance | High | Low |

## Key methods

### Single-neuron recording in visual cortex (Hubel & Wiesel, 1962)

- **Problem:** how the visual cortex builds representations of edges and shapes from light falling on the retina.
- **Core idea:** record single neurons in the visual cortex of anaesthetised cats while presenting spots and bars of light at different positions and orientations. Neurons were sorted into simple cells, with separate on and off subregions that respond to edges at a preferred orientation, and complex cells, which respond to such an edge anywhere in a larger region.
- **Algorithm:**
    1. Present a stimulus at a given position and orientation.
    2. Record the spikes of the neuron.
    3. Map the receptive field from the responses.
    4. Classify the cell by its response pattern.
- **Results:** complex cells appear to pool the outputs of simple cells, a hierarchy that inspired hierarchical convolutional vision models.
- **Limitations:** the experiments used anaesthetised cats, and the hierarchy is a model that later work found more varied than the two cell types suggest.

### Dopamine reward prediction error (Schultz, Dayan & Montague, 1997)

- **Problem:** what do midbrain dopamine neurons signal while an animal learns about rewards?
- **Core idea:** dopamine neurons respond to unexpected rewards, and as learning proceeds the response moves to the earliest predictive cue. The pattern matches a temporal-difference error, the difference between the reward received and the reward predicted.
- **Equation:** in modern notation, \(\delta_t = r_t + \gamma V(s_{t+1}) - V(s_t)\).

- **Results:** in monkeys, dopamine firing rose to unexpected rewards, shifted to the predictive cue after learning, and dipped when an expected reward was omitted.
- **Limitations:** recordings came from a limited number of monkeys and tasks. Later work debated whether dopamine signals only prediction error or also salience and other information.

## Resources

- Kandel et al., *Principles of Neural Science*
- Bear, Connors & Paradiso, *Neuroscience: Exploring the Brain*
- Purves et al., *Neuroscience*
- [Neuromatch Academy](https://compneuro.neuromatch.io/) (computational)
- Crash Course *Psychology* and *Neuroscience* videos

## References

### Seminal papers

- Hubel, D. H. & Wiesel, T. N. (1962). Receptive fields, binocular interaction and functional architecture in the cat's visual cortex. *The Journal of Physiology*. https://doi.org/10.1113/jphysiol.1962.sp006837 — Discovers orientation-selective simple and complex cells, the biological inspiration for hierarchical vision models.
- Schultz, W., Dayan, P. & Montague, P. R. (1997). A Neural Substrate of Prediction and Reward. *Science*. https://doi.org/10.1126/science.275.5306.1593 — Shows that dopamine neurons signal reward prediction errors, linking reinforcement learning to the brain.
- Friston, K. (2010). The free-energy principle: a unified brain theory? *Nature Reviews Neuroscience*. https://doi.org/10.1038/nrn2787 — Proposes that brains minimise prediction error, a unifying framework for perception, action and learning.
- Yamins, D. L. K., et al. (2014). Performance-optimized hierarchical models predict neural responses in higher visual cortex. *PNAS*. https://doi.org/10.1073/pnas.1403112111 — Shows that deep networks trained for object recognition predict neural responses in higher visual cortex.

### Surveys and textbooks

- Neuroscience Online: An Electronic Textbook for the Neurosciences. Department of Neurobiology and Anatomy, UTHealth McGovern Medical School. https://nba.uth.tmc.edu/neuroscience/ — A free, open-access electronic textbook for the neurosciences.
