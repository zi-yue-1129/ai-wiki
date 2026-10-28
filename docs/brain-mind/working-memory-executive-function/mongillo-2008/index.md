---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/rnn
tags:
  - neuroscience
  - recurrent networks
aliases:
  - Mongillo et al. 2008
  - Synaptic theory of working memory
  - 活動靜默記憶
  - 突觸工作記憶
  - Activity-silent memory
  - Short-term synaptic facilitation
---

# Synaptic Theory of Working Memory (Mongillo et al. 2008)

Mongillo, Barak and Tsodyks (2008) proposed that working memory is held not by sustained spiking but by short-term changes in synaptic strength, driven by residual calcium in the presynaptic terminals. In this account neurons can be quiet during a delay while the memory persists. This is the activity-silent alternative to persistent activity, one of the three methods compared on the parent page, [Working Memory and Executive Function](../index.md).

## Overview

The usual assumption, as the paper states it, is that enhanced spiking in the form of persistent reverberation for several seconds is the neural correlate of working memory. Mongillo et al. argued that the memory could instead be carried by the synapses of a recurrent cortical network. Their argument has two parts. The synaptic mechanism can keep a memory for the length of a delay, and it does so at a low metabolic cost, because the memory needs to be refreshed only occasionally. The paper is a theoretical proposal, and its abstract reports no new data.

The long-term counterpart, synaptic plasticity, is covered in [Long-Term Potentiation](../../memory-learning/long-term-potentiation/index.md).

## Key concepts

- **Synaptic facilitation**: a short-term increase in synaptic efficacy after presynaptic spikes, which decays over time.
- **Residual calcium**: calcium that remains in a presynaptic terminal after a spike. In this account it acts as a buffer that spikes load, refresh and read out.
- **Refresh**: a brief burst of spikes that reloads the synaptic trace before it decays.

## How it works

The synaptic trace can be described with the facilitation model of Tsodyks, Pawelzik and Markram (1998). Each synapse has a utilisation variable $u$ that rises with every presynaptic spike $t_k$ and relaxes back to a baseline $U$:

$$\frac{du}{dt} = \frac{U - u}{\tau_F} + U(1-u)\sum_k \delta(t - t_k)$$

The efficacy of the synapse is proportional to $u$, so a spike sequence leaves a trace that lasts for longer than the spikes themselves. Mongillo et al. use a closely related calcium-based variant, in which residual calcium plays the role of $u$. The memory cycle has four steps.

1. **Encoding**: a cue drives a subset of excitatory neurons to fire, which loads the recurrent synapses between them with facilitation.
2. **Silent delay**: spiking stops or becomes sparse during the delay, while the facilitation decays slowly because its time constant is long.
3. **Refresh**: occasional bursts of spikes, either spontaneous or driven by the network, reload the traces and stabilise the memory.
4. **Readout**: a probe stimulus makes the facilitated synapses boost the cells that encode the cued item, so the memory is read out.

## Results

The paper's evidence is the behaviour of the proposed mechanism, analysed theoretically and in network models. The abstract reports three claims. The synaptic mechanism can hold a memory over a delay while the neurons are largely quiet. It is metabolically efficient and robust, because the long time constant of calcium kinetics allows a low refresh rate. The duration and stability of the memory can be regulated by spontaneous activity. The abstract does not give benchmark figures, so none are quoted here.

## Limitations

- **Theory-first**: the claims depend on parameters such as the facilitation time constant and the baseline utilisation.
- **Hard to observe**: a silent memory is difficult to distinguish from low-rate firing with standard recording methods, so the claim of silence has to be tested with methods that can detect synaptic traces.
- **Refresh is assumed**: the source of the refresh bursts is part of the model rather than something the theory explains in full.
- **Capacity**: the paper concentrates on duration and stability. How the mechanism accounts for the capacity limit of about three to five items (Cowan, 2001) is a separate question.

## Open questions

- **Which mechanism dominates where?** Silent and persistent storage may coexist, and their relative roles may depend on the brain area and the task.
- **Can synaptic traces be measured directly during a delay?** A direct test would separate the two accounts more cleanly than delay activity alone.
- **How does the silent trace respond to distractors?** Gating, as in [O'Reilly & Frank 2006](../oreilly-frank-2006/index.md), needs a mechanism to protect a trace from new input, and the synaptic account does not yet specify one.

## References

### Seminal papers

- Mongillo, G., Barak, O. & Tsodyks, M. (2008). Synaptic Theory of Working Memory. *Science*. https://doi.org/10.1126/science.1150769 — Proposes that working memory is held by calcium-mediated synaptic facilitation in recurrent connections, with neurons able to stay quiet.
- Tsodyks, M., Pawelzik, K. & Markram, H. (1998). Neural Networks with Dynamic Synapses. *Neural Computation*. https://doi.org/10.1162/089976698300017502 — A phenomenological model of synapses that depress or facilitate, driven by presynaptic spike trains, used here for the facilitation equation.
- Funahashi, S., Bruce, C. J. & Goldman-Rakic, P. S. (1989). Mnemonic coding of visual space in the monkey's dorsolateral prefrontal cortex. *Journal of Neurophysiology*. https://doi.org/10.1152/jn.1989.61.2.331 — Recordings of delay-period firing in prefrontal neurons, the persistent-activity account that this method is set against.
- Miller, E. K. & Cohen, J. D. (2001). An Integrative Theory of Prefrontal Cortex Function. *Annual Review of Neuroscience*. https://doi.org/10.1146/annurev.neuro.24.1.167 — Proposes that the PFC maintains goal representations that bias activity in other areas, a theory that either storage mechanism could support.
- Cowan, N. (2001). The magical number 4 in short-term memory: A reconsideration of mental storage capacity. *Behavioral and Brain Sciences*. https://doi.org/10.1017/S0140525X01003922 — Reviews capacity-limit studies and argues for a limit of about three to five chunks.
