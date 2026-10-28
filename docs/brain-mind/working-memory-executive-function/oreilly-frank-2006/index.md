---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/rnn/gated-cells
  - theory/paradigms/reinforcement-learning
tags:
  - neuroscience
  - recurrent networks
  - planning
aliases:
  - O'Reilly and Frank 2006
  - PBWM
  - Prefrontal basal ganglia working memory
  - 門控工作記憶
  - Gated working memory
  - Actor-critic gating
---

# Learned Gating of Working Memory (O'Reilly & Frank 2006)

O'Reilly and Frank (2006) presented a model, called PBWM (prefrontal cortex and basal ganglia working memory), in which a basal ganglia actor-critic learns when the prefrontal cortex should update its working-memory contents and when it should keep them. Executive control is thus learned rather than fixed in advance. This is the gating method compared on the parent page, [Working Memory and Executive Function](../index.md).

## Overview

Holding information is not enough. A useful store must also decide when new input should enter it. A store that updates on every input loses its goal when a distractor arrives, and a store that never updates cannot respond to a change in the task. The gating problem is to choose the update decision correctly at each moment.

O'Reilly and Frank framed executive function as this decision. Earlier models often left executive control as a homunculus, a hidden controller that is assumed rather than explained. Their model replaces it with learning mechanisms in subcortical structures.

## Key concepts

- **Working-memory store**: a set of prefrontal representations that are kept online for use in later steps.
- **Gate**: a decision, made at each time step, to update the store with the current input or to keep its contents.
- **Actor-critic**: a learning architecture in which an actor chooses actions and a critic learns to evaluate them, so that the critic's signal trains the actor.
- **Credit assignment**: working out which earlier decisions led to a later outcome. The model addresses both its temporal and its structural forms.
- **1-2-AX task**: a sequential working-memory benchmark, named in the paper's abstract, that requires an earlier cue to be held across several steps.

## How it works

The model has four components.

1. **Representation**: the prefrontal network holds representations of the current task context and of past inputs.
2. **Actor**: the basal ganglia select, at each step, whether the store is updated with the current input or left unchanged.
3. **Critic**: a second learner, part of the subcortical system that the abstract groups with the basal ganglia, learns which prefrontal representations are task relevant.
4. **Training**: the critic's learning signal trains the actor to gate correctly, and it also shapes the representations so that they are useful for the task.

The gating itself can be written in a simplified general form. If $g_t \in [0,1]$ is the gate, $\tilde{h}_t$ is the candidate new content and $h_{t-1}$ is the previous store, then

$$h_t = g_t \odot \tilde{h}_t + (1 - g_t) \odot h_{t-1}$$

When $g_t$ is near 1 the store is overwritten, and when it is near 0 the store is protected. This is the same pattern as the update of the LSTM's cell state, which multiplies the old state by a forget gate and adds gated new content. The equation is a notational device for this page and not the paper's exact formulation.

## Results

The paper's main evidence is simulation on working-memory tasks. On the 1-2-AX task and other benchmarks, the abstract reports that the model compares favourably with standard backpropagation-based temporal learning. The abstract gives no numbers, so none are quoted here.

## Limitations

- **Interpretation of anatomy**: the mapping of the actor onto the basal ganglia and of the critic onto midbrain and amygdala is an interpretation of the model's architecture, not a measured correspondence.
- **Small benchmarks**: the tasks are controlled and sequential. Performance on the benchmark does not show that the mechanism would scale to natural tasks such as language.
- **Biological learning rule**: the paper claims that its mechanism solves the temporal and structural credit assignment problems. Whether cortico-basal ganglia circuits implement a rule of that kind has not been established.

## Open questions

- **Is the learning rule biological?** Testing whether gating signals in the basal ganglia behave as the actor-critic predicts is an empirical question.
- **Does gating transfer to natural sequences?** Language and planning tasks have longer and less regular structure than the benchmark, and it is unclear whether the same gate learns them.
- **How does gating relate to attention?** Gating controls what enters the store, while attention controls what is read from it. Models that combine the two are an open area, relevant to [Attention in Brains & Machines](../../attention-brain-machine/index.md).

## References

### Seminal papers

- O'Reilly, R. C. & Frank, M. J. (2006). Making Working Memory Work: A Computational Model of Learning in the Prefrontal Cortex and Basal Ganglia. *Neural Computation*. https://doi.org/10.1162/089976606775093909 — A model in which a basal ganglia actor-critic learns the gating of prefrontal working memory, tested on sequential benchmark tasks.
- Miller, E. K. & Cohen, J. D. (2001). An Integrative Theory of Prefrontal Cortex Function. *Annual Review of Neuroscience*. https://doi.org/10.1146/annurev.neuro.24.1.167 — Proposes that the PFC maintains goal representations that bias processing elsewhere, the executive role that the gate is meant to implement.
- Hochreiter, S. & Schmidhuber, J. (1997). Long Short-Term Memory. *Neural Computation*. https://doi.org/10.1162/neco.1997.9.8.1735 — Introduces the LSTM, whose multiplicative gates learn to open and close access to the stored state.
- Graves, A., Wayne, G. & Danihelka, I. (2014). Neural Turing Machines. arXiv. https://arxiv.org/abs/1410.5401 — Couples a neural network to an external memory that it reads and writes through attention, trainable end to end.

### Articles and documentation

- Chung, J. et al. (2014). Empirical Evaluation of Gated Recurrent Neural Networks on Sequence Modeling. arXiv. https://arxiv.org/abs/1412.3555 — Compares LSTM and GRU units on polyphonic music and speech modelling, finding both better than plain tanh units.
