---
status: draft
last_reviewed: 2026-10-28
related:
- brain-mind/memory-learning
- brain-mind/cognitive-architectures
- theory/models/rnn/gated-cells
tags:
- working memory
- executive function
- prefrontal cortex
- gating
aliases:
  - 工作記憶與執行功能
  - 工作記憶
  - 執行功能
  - Working Memory
  - Executive Function
  - Executive Control
  - Prefrontal Cortex
  - PFC
---

# Working memory and executive function

Working memory is the ability to hold a small amount of information in mind for a few seconds and use it, such as a phone number being dialled or the start of a sentence being read. Executive function is the set of control processes that decide what enters that store, what is kept, when it is updated, and how behaviour follows from it. Both depend heavily on the prefrontal cortex (PFC), and both have clear parallels in AI, where the context window and gated recurrent networks play similar roles.


## Overview

Working memory is a limited, temporary store. Baddeley and Hitch (1974) proposed a multi-component model in which a central executive directs attention and coordinates storage systems for verbal and visual-spatial information. Executive functions form a broader family of controls: selecting goals, switching between tasks, filtering distractions and holding rules in mind. The two are hard to separate in practice, because holding something in mind serves control, and control decides what is held.

Miller and Cohen (2001) proposed that the prefrontal cortex does executive work by actively maintaining patterns of activity that represent goals and the means to reach them. These patterns bias processing in other brain areas, so that activity flows along the mappings between inputs, internal states and outputs that a task requires.

## Key concepts

- **Working memory**: information kept available for a short time while it is used.
- **Executive function**: control over what is attended, stored, updated, switched or suppressed.
- **Persistent activity**: sustained firing of neurons during a delay. Funahashi, Bruce and Goldman-Rakic (1989) recorded it in monkey prefrontal cortex during a spatial memory task.
- **Activity-silent memory**: information held in transient changes that do not need ongoing spiking.
- **Gating**: a mechanism that opens or closes access to a memory store, so that only relevant input updates it.
- **Capacity limit**: the amount that can be held at once. Cowan (2001) reviewed evidence for a limit of about three to five chunks, centred on about four.

## Core ideas

**Keeping and deciding are separate problems.** A system that keeps everything is not selective, and one that updates constantly forgets what it needs. Gating is the common solution proposed: the system learns when to write to memory and when to protect what is already there.

**Two mechanisms for keeping information.** Early network models explained persistent activity as a stable pattern of firing sustained by recurrent connections (Compte et al., 2000). More recent work finds that delay activity does not always accompany maintenance, which suggests that memory can also be carried by synaptic or other hidden states (Stokes, 2015). The two views are not yet resolved.

**Learned gates for control.** In one influential model, the basal ganglia learn when the prefrontal cortex should update its contents, using a dopamine-like learning signal. Control is then something the system learns, rather than an unexplained internal controller.

**Capacity as slots or resources.** Slot-based accounts treat working memory as a few discrete items. Resource accounts treat it as a shared pool of precision that can be divided among items. Bays and Husain (2008) showed that visual memory is not fixed by the number of objects, but is shared out flexibly and biased by attention, which favours the resource view.

## Key methods

- [Prefrontal basal ganglia working memory (PBWM)](pbwm/index.md): a model in which the basal ganglia learn when the prefrontal cortex updates its contents, so that executive control is learned.
- [Activity-silent working memory](activity-silent-working-memory/index.md): an account in which memories are held in transient synaptic states, so that spiking can fall silent during the delay.

## Connections

- **Memory.** Long-term storage in the hippocampus and cortex is covered in [Memory & Learning in the Brain](../memory-learning/index.md) and [Complementary learning systems](../memory-learning/complementary-learning-systems/index.md).
- **Basal ganglia and reward.** PBWM relies on the same kind of learning signal as the [dopamine reward prediction error](../neuroscience/dopamine-reward-prediction-error/index.md). The wider role of dopamine in choice is on [Decision Making, Dopamine & Reward](../decision-reward/index.md).
- **Attention.** Selecting relevant information is shared with [Attention in Brains & Machines](../attention-brain-machine/index.md).
- **Cognitive architectures.** Several architectures treat working memory and control as separate modules; see [Cognitive Architectures](../cognitive-architectures/index.md).
- **AI: context windows.** A transformer's context window is the set of tokens it can attend to at once ([Transformer](../../theory/models/transformer/index.md)). Unlike a working memory store, the window does not decide by itself what to keep. What persists beyond it depends on the surrounding system, which is why many systems add external memory.
- **AI: gated recurrent networks.** The LSTM's input, forget and output gates learn when to write to, keep and read from a memory cell ([LSTM](../../theory/models/rnn/gated-cells/lstm/index.md)). This resembles PBWM's gating in function. The resemblance is functional only; the two systems do not share an implementation.
- **AI: executive control.** Planning and control in artificial agents are discussed in [AI Agents](../../theory/models/agents/index.md) and [Reasoning](../../theory/models/reasoning/index.md).

## Applications

- **Gated memory in neural networks.** The LSTM (Hochreiter & Schmidhuber, 1997) uses multiplicative gates to protect a memory cell across long time lags, and it is widely used in sequence modelling.
- **Interpreting executive-control experiments.** Miller and Cohen (2001) review neurophysiological, neuroimaging and computational studies that support the view of the PFC as a source of control. That framing guides how studies of task switching and rule use are interpreted.
- **Testing memory maintenance.** Wolff et al. (2017) used a brief EEG perturbation pulse to detect item-specific memory during the delay.

## Open questions

- **How is information kept?** Persistent spiking, synaptic states and a mixture of the two all have some support. How much each contributes in a given task is debated (Stokes, 2015; Ma et al., 2014).
- **What sets capacity?** Slot-based and resource-based accounts still compete, and the answer may depend on the task (Cowan, 2001; Bays & Husain, 2008).
- **How is gating learned?** PBWM proposes a learned, dopamine-based gate, but its mapping onto identified circuits is still under test.
- **Do AI and brain gates share principles?** The functional analogy is clear. Whether it reflects a shared computational principle is an open question.

## References

### Seminal papers

- Baddeley, A. D. & Hitch, G. (1974). Working memory. In *Psychology of Learning and Motivation*, pp. 47–89. Academic Press. https://doi.org/10.1016/S0079-7421(08)60452-1 — Proposes the multi-component model of working memory, with a central executive.
- Funahashi, S., Bruce, C. J. & Goldman-Rakic, P. S. (1989). Mnemonic coding of visual space in the monkey's dorsolateral prefrontal cortex. *Journal of Neurophysiology*. https://doi.org/10.1152/jn.1989.61.2.331 — Records prefrontal neurons active during a memory delay in a spatial task.
- Compte, A. et al. (2000). Synaptic mechanisms and network dynamics underlying spatial working memory in a cortical network model. *Cerebral Cortex*. https://doi.org/10.1093/cercor/10.9.910 — Network model of spatial working memory based on persistent activity.
- Cowan, N. (2001). The magical number 4 in short-term memory: A reconsideration of mental storage capacity. *Behavioral and Brain Sciences*. https://doi.org/10.1017/S0140525X01003922 — Reviews evidence that the capacity limit is about three to five chunks.
- Bays, P. M. & Husain, M. (2008). Dynamic shifts of limited working memory resources in human vision. *Science*. https://doi.org/10.1126/science.1158023 — Shows that visual memory is a limited resource shared dynamically between items.
- Hochreiter, S. & Schmidhuber, J. (1997). Long short-term memory. *Neural Computation*. https://doi.org/10.1162/neco.1997.9.8.1735 — Introduces the LSTM, whose multiplicative gates control access to a memory cell.
- Miller, E. K. & Cohen, J. D. (2001). An integrative theory of prefrontal cortex function. *Annual Review of Neuroscience*. https://doi.org/10.1146/annurev.neuro.24.1.167 — Proposes that the prefrontal cortex maintains goal representations that bias other brain areas.
- O'Reilly, R. C. & Frank, M. J. (2006). Making working memory work: a computational model of learning in the prefrontal cortex and basal ganglia. *Neural Computation*. https://doi.org/10.1162/089976606775093909 — Introduces PBWM, a model in which basal ganglia gate prefrontal updating.
- Mongillo, G., Barak, O. & Tsodyks, M. (2008). Synaptic theory of working memory. *Science*. https://doi.org/10.1126/science.1150769 — Proposes that working memory is sustained by calcium-mediated synaptic facilitation.

### Surveys and reviews

- Stokes, M. G. (2015). 'Activity-silent' working memory in prefrontal cortex: a dynamic coding framework. *Trends in Cognitive Sciences*. https://doi.org/10.1016/j.tics.2015.05.004 — Reviews evidence that memory can be held without persistent spiking, and proposes a dynamic coding framework.
- Curtis, C. E. & D'Esposito, M. (2003). Persistent activity in the prefrontal cortex during working memory. *Trends in Cognitive Sciences*. https://doi.org/10.1016/S1364-6613(03)00197-9 — Reviews the evidence for persistent delay activity in prefrontal cortex.
- Ma, W. J., Husain, M. & Bays, P. M. (2014). Changing concepts of working memory. *Nature Neuroscience*. https://doi.org/10.1038/nn.3655 — Reviews how models of working memory capacity and maintenance have changed.
- Miller, E. K., Lundqvist, M. & Bastos, A. M. (2018). Working memory 2.0. *Neuron*. https://doi.org/10.1016/j.neuron.2018.09.023 — Reviews recent neural accounts of working memory across brain areas.
- Jonides, J., Lewis, R. L., Nee, D. E., Lustig, C. A., Berman, M. G. & Moore, K. S. (2008). The mind and brain of short-term memory. *Annual Review of Psychology*. https://doi.org/10.1146/annurev.psych.59.103006.093615 — Reviews behavioural and neuroimaging evidence on short-term memory.
- Wolff, M. J., Jochim, J., Akyürek, E. G. & Stokes, M. G. (2017). Dynamic hidden states underlying working-memory-guided behavior. *Nature Neuroscience*. https://doi.org/10.1038/nn.4546 — Uses EEG and a perturbation pulse to detect item-specific memory during the delay; the strength of this signal predicts memory-guided behaviour.
