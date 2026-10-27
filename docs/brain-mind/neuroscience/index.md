---
related:
- brain-mind/computational-neuroscience
- brain-mind/bci
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

## Resources

- Kandel et al., *Principles of Neural Science*
- Bear, Connors & Paradiso, *Neuroscience: Exploring the Brain*
- Purves et al., *Neuroscience*
- [Neuromatch Academy](https://compneuro.neuromatch.io/) (computational)
- Crash Course *Psychology* and *Neuroscience* videos
