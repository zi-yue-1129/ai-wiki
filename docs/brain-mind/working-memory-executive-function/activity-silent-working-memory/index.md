---
status: draft
last_reviewed: 2026-10-28
related:
- brain-mind/memory-learning
tags:
- working memory
- activity-silent
- persistent activity
- synaptic plasticity
aliases:
  - Activity-silent working memory
  - Synaptic theory of working memory
  - 活動靜默工作記憶
  - 突觸工作記憶理論
  - Mongillo 2008
  - Stokes 2015
---

# Activity-silent working memory (Mongillo et al., 2008; Stokes, 2015)

Activity-silent working memory is the idea that information can be held across a delay without neurons firing continuously. The memory is carried by transient changes in synaptic strength or other hidden states, and a brief reactivation can bring it back into spiking when needed. Mongillo, Barak and Tsodyks (2008) gave an explicit synaptic model, and Stokes (2015) reviews the evidence and sets out a dynamic coding framework.

This page is one method within [Working Memory and Executive Function](../index.md). The competing account, in which memory is kept by sustained firing, is summarised there.

## Overview

For a long time, working memory was assumed to be persistent. Neurons were thought to keep firing through a delay, and that firing was the memory. Recent work suggests that delay activity often waxes and wanes with the current task relevance of the items held, and that population-level activity keeps changing even while a memory is kept. Stokes (2015) asks how a stable memory can exist when the underlying activity is always moving.

Activity-silent accounts answer that the stable part of the memory need not be in spiking at all. It can be stored in synapses or other hidden states, so that spiking may fall silent during the delay.

## Problem

If memory depended only on ongoing spiking, maintaining it would be costly and fragile, and the spiking patterns would need to be stable throughout the delay. Two observations challenged this view. Persistent delay activity does not always accompany maintenance, and population activity is highly dynamic. The problem is to explain how information survives a delay in which the visible activity does not hold it steady.

## Core idea

Two linked ideas describe the account.

1. **Synaptic storage.** Mongillo et al. (2008) propose that working memory is sustained by calcium-mediated synaptic facilitation in the recurrent connections of neocortical networks. Residual calcium in presynaptic terminals acts as a buffer. Spiking loads, refreshes and reads out this buffer. Because calcium decays slowly, the refresh can be infrequent, which makes the mechanism metabolically efficient and robust.
2. **Dynamic hidden states.** Stokes (2015) argues that memory can be carried by transient activity states that change with task relevance, and that the framework explains how a stable memory coexists with changing activity. Wolff et al. (2017) support this with a perturbation pulse during the delay, which allowed item-specific memory to be detected in EEG.

## Equation or algorithm

No single equation summarises the framework, and the mechanism is written here as numbered steps for the synaptic version.

1. A brief burst of spiking in a population loads residual calcium into its recurrent synapses, which strengthens the connections within that population.
2. Between refreshes the calcium decays slowly, so the synaptic facilitation, and the memory it encodes, persists without sustained spiking.
3. A refresh, which can be a brief burst of spiking or a stimulus, reads out the memory and reloads the calcium.
4. Spontaneous background activity regulates how long the memory lasts and how stable it is.

The steps describe a simplified model. Other synaptic mechanisms are possible, and Stokes (2015) treats hidden states more broadly than any single one.

## Results

- **Synaptic model.** Mongillo et al. (2008) show that a synaptic memory can be sustained with a low refresh rate and that its duration can be controlled by background activity. They describe the mechanism as robust and metabolically efficient.
- **Pulse-based evidence.** Wolff et al. (2017) used EEG and a perturbation pulse during maintenance. A cue to forget one item erased its trace, while items that were only unattended stayed coded. The strength of this hidden-state coding predicted the accuracy and precision of memory-guided responses.

## Limitations

- **Indirect evidence.** Hidden states are inferred from decoding and perturbation, not seen directly. A pulse can reveal a memory, but it also changes the state being measured.
- **Persistent firing still occurs.** Sustained delay activity has been reported in many prefrontal studies (Curtis & D'Esposito, 2003). Activity-silent accounts probably describe some conditions better than others, and the boundary is not settled.
- **Model specificity.** The synaptic model is one specific mechanism, and the framework is a dynamic account rather than a single experiment.

## Connections

- **Persistent activity.** The sustained-firing view is represented by the network model of Compte et al. (2000) and the recordings of Funahashi et al. (1989), summarised in the [parent overview](../index.md).
- **Synaptic plasticity.** The calcium-based storage in Mongillo et al. (2008) depends on the same kind of synaptic change studied in [Long-term potentiation](../../memory-learning/long-term-potentiation/index.md). The link is conceptual: the timescales differ.
- **Gated maintenance.** [PBWM](../pbwm/index.md) describes maintenance as an active, gated store. Both accounts can apply to different parts of a task.
- **Neuroimaging.** Reading hidden states needs methods that do not depend on spiking, such as perturbation with EEG. See [Neuroimaging & Recording Methods](../../neuroimaging-methods/index.md).
- **AI.** A synaptic account of memory is an analogy to storage in changing weights, not a claim about how machine memory is implemented. The [Transformer](../../../theory/models/transformer/index.md) page describes one machine design.

## Applications

- **Experimental design.** Perturbation and decoding methods, such as the pulse design of Wolff et al. (2017), are used to read memory when ongoing activity does not show it.
- **Models of maintenance.** Synaptic models of working memory inspire network models in which memory is kept by connection strengths rather than by sustained firing (Mongillo et al., 2008).

## Open questions

- **Which mechanism holds the memory in a given task?** Synaptic storage, dynamic hidden states and persistent firing each have supporting evidence. The conditions that favour each are not clear.
- **How are hidden states reactivated?** Refreshing can be triggered by a stimulus, by attention or by spontaneous activity. The relative roles of these triggers are unresolved.
- **How does storage relate to capacity?** Whether activity-silent storage explains the capacity limits reported by Cowan (2001) and by Ma et al. (2014) is an open question.

## References

### Seminal papers

- Mongillo, G., Barak, O. & Tsodyks, M. (2008). Synaptic theory of working memory. *Science*. https://doi.org/10.1126/science.1150769 — Proposes that working memory is sustained by calcium-mediated synaptic facilitation, refreshed by spiking.
- Wolff, M. J., Jochim, J., Akyürek, E. G. & Stokes, M. G. (2017). Dynamic hidden states underlying working-memory-guided behavior. *Nature Neuroscience*. https://doi.org/10.1038/nn.4546 — Uses EEG and a perturbation pulse to detect item-specific memory during the delay; the strength of this signal predicts memory-guided behaviour.
- Compte, A. et al. (2000). Synaptic mechanisms and network dynamics underlying spatial working memory in a cortical network model. *Cerebral Cortex*. https://doi.org/10.1093/cercor/10.9.910 — The persistent-activity network model that activity-silent accounts are compared against.

### Surveys and reviews

- Stokes, M. G. (2015). 'Activity-silent' working memory in prefrontal cortex: a dynamic coding framework. *Trends in Cognitive Sciences*. https://doi.org/10.1016/j.tics.2015.05.004 — Reviews evidence that delay activity does not always accompany maintenance, and proposes the dynamic coding framework.
- Curtis, C. E. & D'Esposito, M. (2003). Persistent activity in the prefrontal cortex during working memory. *Trends in Cognitive Sciences*. https://doi.org/10.1016/S1364-6613(03)00197-9 — Reviews the evidence for persistent delay activity in prefrontal cortex, the view that activity-silent accounts revise.
