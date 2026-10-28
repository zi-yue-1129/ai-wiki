---
status: complete
last_reviewed: 2026-10-28
---

# Long-term potentiation (Bliss & Lømo, 1973)

A brief burst of high-frequency stimulation strengthens a synapse for hours, which made long-term potentiation (LTP) the leading candidate for a cellular mechanism of memory.

## Overview

Learning must change something in the brain, and the most plausible place to look is the synapse, the junction where one neuron passes a signal to another. Hebbian ideas hold that connections between co-active neurons are strengthened, and such ideas needed a physiological test. Bliss and Lømo (1973) provided a clear demonstration that a synapse can change in a way that lasts far longer than the stimulus that produced it. The change is now called long-term potentiation (LTP).

LTP is one of the best-studied mechanisms in neuroscience. It is not a complete theory of memory, but many memory models build on it, and it links the behaviour of neurons to the storage of experience. It sits between the [patient evidence for memory systems](../medial-temporal-lesions/index.md) and the [systems-level theory of how memories are organised](../complementary-learning-systems/index.md).

## Key concepts

- **Synapse**: the junction through which one neuron influences another. Its strength determines how much a presynaptic signal changes the postsynaptic cell.
- **Perforant path**: the fibre bundle that carries signals from the entorhinal cortex to the dentate gyrus of the hippocampus.
- **Dentate gyrus**: a hippocampal region, whose granule cells receive the perforant path.
- **Population response**: the combined response of many neurons, recorded with an electrode. It has two parts in these experiments: an excitatory postsynaptic potential (EPSP), which reflects the depolarisation of the cells, and a population spike, which reflects their discharge.
- **Potentiation**: a lasting increase in the response to the same input. Its opposite, long-term depression (LTD), is a lasting decrease.

## Problem

Is there a lasting physical change at synapses that could store memories? Two questions were open. First, can a synapse change in a way that lasts for hours, rather than milliseconds or seconds? Second, does the change depend on how the synapse is used, so that it could store specific information? Bliss and Lømo addressed the first question directly.

## Core idea

Bliss and Lømo stimulated the perforant path of anaesthetised rabbits and recorded the response in the dentate gyrus. They delivered brief trains of stimuli at high frequency and then tested the response with single pulses at low frequency. After the trains, the response to the test pulses stayed enhanced for a long time. The stimulus was brief, but the synaptic change far outlasted it. This was the first report of a lasting synaptic change of this kind.

## Equation or algorithm

The experimental protocol can be written as numbered steps, using the conditions in the 1973 paper:

1. Anaesthetise the rabbit and place extracellular electrodes in the dentate area. Record the population response to single pulses delivered to the perforant path, which serve as baseline test responses.
2. Deliver a conditioning train at high frequency: 10 to 20 stimuli per second for 10 to 15 seconds, or 100 stimuli per second for 3 to 4 seconds.
3. Continue testing with single pulses at low frequency, and track the EPSP amplitude, the population spike amplitude and the spike latency over time.
4. Compare the responses with the baseline. Potentiation is the lasting increase relative to that baseline.

No equation is needed to describe the basic result, but later work expresses LTP as a change in synaptic weight $w$ that depends on the timing and frequency of pre- and postsynaptic activity. The 1973 paper is descriptive: it measures responses and their change, not a formal model.

## Results

In 15 of the 18 rabbits, the population response to single perforant-path volleys was potentiated for periods ranging from 30 minutes to 10 hours after one or more conditioning trains. Both kinds of train produced long-term potentiation. The conditioning trains at 10 to 20 per second produced a large potentiation of the population spike, while the 100 per second train suppressed the spike during stimulation. Three parameters were analysed: the EPSP amplitude, the spike amplitude and the spike latency. A reduction in latency was the commonest sign of potentiation, seen in 57% of all experiments. The authors concluded that two independent mechanisms contribute to the lasting potentiation: an increase in the efficiency of transmission at the synapses, and an increase in the excitability of the granule cell population.

Later work showed that the best-characterised form of LTP depends on NMDA receptors. Bliss and Collingridge (1993) describe these receptors as giving the synapse Hebbian properties, because they convert electrical activity at the postsynaptic membrane into chemical signals that trigger lasting changes on both sides of the synapse. Morris et al. (1986) reported that an NMDA receptor antagonist, AP5, blocked LTP and selectively impaired learning, which linked the synaptic mechanism to behaviour.

## Limitations

The 1973 experiments were done in anaesthetised animals, with extracellular recordings of population responses, not of single synapses. The link to learning was an inference. The paper showed that potentiation can last hours, but it did not show that the potentiated synapses store any particular memory. Lynch (2004) makes this point explicitly: it is not yet clear whether the changes that maintain LTP also underlie memory consolidation.

The paper also did not examine the molecular basis. Later work tied the best-characterised form of LTP to NMDA receptors, as Bliss and Collingridge (1993) summarise. Malenka and Bear (2004), whose title speaks of an "embarrassment of riches", discuss how many forms of potentiation and depression exist, which makes it harder to say which form matters for memory.

## Key methods

Three landmark alternatives explain how synapses change or how such changes relate to memory:

- [Patients with medial temporal lobe lesions (Scoville & Milner, 1957)](../medial-temporal-lesions/index.md): behavioural evidence that the hippocampal system is needed for new memories. It does not show a synaptic mechanism, which LTP research supplies.
- [Complementary learning systems (McClelland et al., 1995)](../complementary-learning-systems/index.md): a systems-level theory of how fast and slow learning interact, which needs a plasticity mechanism such as LTP to implement its fast store.
- Spike-timing-dependent plasticity (Dan & Poo, 2004): a rule in which the relative timing of pre- and postsynaptic spikes decides whether a synapse strengthens or weakens. It is a refinement of the Hebbian idea that LTP tested.

## Connections

- Parent topic: [Memory & Learning in the Brain](../index.md)
- Other method on this topic: [Medial Temporal Lobe Lesions](../medial-temporal-lesions/index.md)
- Other method on this topic: [Complementary Learning Systems](../complementary-learning-systems/index.md)
- Spiking models: LTP-like rules are used in spiking neural networks. See [SNNs & Neuromorphic Computing](../../snn-neuromorphic/index.md).

## Applications

- **Hebbian learning in models.** Many artificial models of learning use rules that resemble LTP: a connection strengthens when the cells on either side are active together. See the parent page for the Hebbian term.
- **Neuromorphic hardware.** Spiking hardware implements timing-based plasticity rules, which are closer to the synaptic mechanisms studied since Bliss and Lømo's work. See [SNNs & Neuromorphic Computing](../../snn-neuromorphic/index.md).
- **Drug and disease research.** Because LTP depends on NMDA receptors, drugs and disease states that alter these receptors are studied for their effects on learning. Morris et al. (1986) is the classic example of this approach.

## Open questions

- Does LTP cause memory, or does it accompany processes that store memory? Lynch (2004) notes that it is not yet clear whether the changes that maintain LTP also underlie memory consolidation.
- Which molecular changes maintain LTP over days and months, and how do these relate to memory consolidation? Lynch (2004) lists this as unresolved.
- How much of the LTP seen in slices and anaesthetised animals occurs during natural behaviour?
- Which form of plasticity, LTP, LTD, or timing-based rules, best explains how specific memories are stored?

## References

### Seminal papers

- Bliss, T. V. P. & Lømo, T. (1973). Long-lasting potentiation of synaptic transmission in the dentate area of the anaesthetized rabbit following stimulation of the perforant path. *The Journal of Physiology*. https://doi.org/10.1113/jphysiol.1973.sp010273 — The first report of long-lasting potentiation in the dentate gyrus of anaesthetised rabbits, lasting from 30 minutes to 10 hours.
- Morris, R. G. et al. (1986). Selective impairment of learning and blockade of long-term potentiation by an N-methyl-D-aspartate receptor antagonist, AP5. *Nature*. https://doi.org/10.1038/319774a0 — Links the NMDA receptor to LTP, reporting that the antagonist AP5 blocked LTP and impaired learning.
- Bliss, T. V. P. & Collingridge, G. L. (1993). A synaptic model of memory: long-term potentiation in the hippocampus. *Nature*. https://doi.org/10.1038/361031a0 — Review that presents LTP as a model of memory storage, with its NMDA-receptor dependence and Hebbian properties.

### Surveys and textbooks

- Lynch, M. A. (2004). Long-term potentiation and memory. *Physiological Reviews*. https://doi.org/10.1152/physrev.00014.2003 — Review of how LTP relates to learning and memory, especially spatial learning, and of the open question of whether LTP maintenance and memory consolidation share mechanisms.
- Malenka, R. C. & Bear, M. F. (2004). LTP and LTD: an embarrassment of riches. *Neuron*. https://doi.org/10.1016/j.neuron.2004.09.012 — Review of the many forms and mechanisms of synaptic potentiation and depression, and why this diversity matters for memory.
- Dan, Y. & Poo, M.-M. (2004). Spike timing-dependent plasticity of neural circuits. *Neuron*. https://doi.org/10.1016/j.neuron.2004.09.007 — Review of spike-timing-dependent plasticity, a timing rule that refines the Hebbian idea behind LTP.
