---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/rnn
tags:
  - neuroscience
  - recurrent networks
aliases:
  - Funahashi et al. 1989
  - 延遲反應任務
  - Delayed response task
  - 持續活動
  - Persistent activity
---

# Persistent Activity in the Prefrontal Cortex (Funahashi et al. 1989)

Funahashi, Bruce and Goldman-Rakic (1989) recorded prefrontal neurons in monkeys performing a delayed-response task. Many neurons kept firing during the delay, and their firing depended on where the cue had been. This is the experimental basis of the persistent-activity account of working memory, which is one of the three methods compared on the parent page, [Working Memory and Executive Function](../index.md).

## Overview

Working memory must keep a cue available after it has disappeared. To find where that memory lives, Funahashi et al. recorded single neurons in the monkey dorsolateral prefrontal cortex, around the principal sulcus, while the cue was gone and the animal still had to remember it. The result was delay-period activity that was often specific to the direction of the cue, which made it a candidate for the memory itself.

## Key concepts

- **Delayed-response task**: the animal sees a brief cue, waits through a delay, and then responds to the remembered cue.
- **Delay-period activity**: firing that is sustained during the delay and differs from the baseline between trials.
- **Directional tuning**: a neuron responds strongly to cues in some directions and weakly or not at all to others.

## How it works

The paper's task is a sequence of steps.

1. The monkey fixates a central spot.
2. A peripheral cue is shown briefly (0.5 s) at one of eight locations, 45 degrees apart.
3. The cue is removed, and a delay of 1 to 6 s follows while the monkey keeps fixating.
4. The fixation target is switched off, and the monkey makes a saccade to the remembered location.
5. Each neuron is classified by whether its activity during the delay differs from its activity between trials, and by whether the difference depends on cue direction.

Persistent activity can be modelled with a firing-rate equation in which a recurrent network holds a pattern after its input stops:

$$\tau \dot{r}_i = -r_i + \phi\Big(\sum_j W_{ij} r_j + I_i\Big)$$

Here $r_i$ is the rate of neuron $i$, $W_{ij}$ are the recurrent weights, $I_i$ is the input and $\phi$ is a nonlinearity. Funahashi et al. did not fit their data to this equation. It is the standard way of expressing the idea that the delay activity is held by recurrence.

## Results

The results come from the paper's abstract. Of 288 neurons recorded in the principal sulcus region, 170 showed task-related activity in at least one phase of the task. Of these, 87 showed significant excitation or inhibition during the delay compared with the intertrial interval. Of the 87, 79 percent were directional, meaning that their delay activity occurred only for cues in a certain range of directions. The directional preference was maintained across delay intervals of 1 to 6 s. Among neurons with purely excitatory delay activity, 92 percent were directional. Among those with purely inhibitory delay activity, 62 percent were directional.

The evidence is correlational. It shows that the activity of these neurons during the delay carries information about the cue, and it does not show that the activity causes the memory to be held.

## Limitations

- **Correlation, not causation**: recording shows that delay activity follows the remembered cue. It does not by itself show that the activity is necessary for the memory.
- **A minority of neurons**: only 87 of 288 recorded neurons showed significant delay activity, so the account rests on a subset of cells.
- **Entangled with eye movements**: the task uses saccades to report the memory, so delay activity may partly reflect preparation for the response.
- **Single-neuron view**: single recordings cannot show whether persistent firing is generated within the prefrontal circuit or inherited from other areas.
- **Alternative accounts**: the paper does not address silent storage in synapses, the alternative in [Synaptic Theory of Working Memory](../mongillo-2008/index.md).

## Open questions

- **What does delay activity represent?** It may hold the remembered item, the plan for the response, or both. Separating these needs tasks that dissociate them.
- **How general is persistent activity?** The paper studied one task and one area. How far the pattern extends to other tasks and regions is a question that the parent page's open questions address.
- **How do circuits generate it?** Attractor networks reproduce the pattern in models, but whether the real circuits work that way is open.

## References

### Seminal papers

- Funahashi, S., Bruce, C. J. & Goldman-Rakic, P. S. (1989). Mnemonic coding of visual space in the monkey's dorsolateral prefrontal cortex. *Journal of Neurophysiology*. https://doi.org/10.1152/jn.1989.61.2.331 — Recordings from prefrontal neurons in an oculomotor delayed-response task, showing delay-period activity tied to the remembered cue direction.
- Miller, E. K. & Cohen, J. D. (2001). An Integrative Theory of Prefrontal Cortex Function. *Annual Review of Neuroscience*. https://doi.org/10.1146/annurev.neuro.24.1.167 — Proposes that the PFC actively maintains goal representations that bias activity in other areas.
- Cowan, N. (2001). The magical number 4 in short-term memory: A reconsideration of mental storage capacity. *Behavioral and Brain Sciences*. https://doi.org/10.1017/S0140525X01003922 — Reviews capacity-limit studies and argues for a limit of about three to five chunks.
- Mongillo, G., Barak, O. & Tsodyks, M. (2008). Synaptic Theory of Working Memory. *Science*. https://doi.org/10.1126/science.1150769 — Proposes that working memory is held by calcium-mediated synaptic facilitation, the alternative to persistent firing.

### Surveys and textbooks

- Diamond, A. (2013). Executive Functions. *Annual Review of Psychology*. https://doi.org/10.1146/annurev-psych-113011-143750 — Reviews the core executive functions, including working memory, and how they develop.
