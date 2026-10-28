---
status: draft
last_reviewed: 2026-10-28
---

# Complementary learning systems (McClelland, McNaughton & O'Reilly, 1995)

A fast hippocampal store and a slow neocortical learner, linked by replay.

## Problem

Why does the brain need both a hippocampus and a neocortex, and why does fast learning in one network erase earlier learning?

## Core idea

The hippocampus stores new items quickly with sparse codes, while the neocortex learns slowly with overlapping codes. Replay of stored patterns interleaves old and new items during cortical training.

## Equation or algorithm

In connectionist simulations, a fast learner stores new items, and an interleaved training schedule of old and new items trains the slow learner.

## Results

Sequential training erased earlier items (catastrophic interference), while interleaved training avoided it.

## Limitations

The theory is conceptual and rests on simulations. Kumaran et al. (2016) revisit it in light of deep learning and replay.

## Connections

- Parent topic: [Memory & Learning in the Brain](../index.md)
- Other method on this topic: [Medial Temporal Lobe Lesions](../medial-temporal-lesions/index.md)
- Other method on this topic: [Long-Term Potentiation](../long-term-potentiation/index.md)

## References

### Seminal papers

- Scoville, W. B. & Milner, B. (1957). Loss of recent memory after bilateral hippocampal lesions. *Journal of Neurology, Neurosurgery & Psychiatry*. https://doi.org/10.1136/jnnp.20.1.11 — Reports the patients with bilateral medial temporal lobe lesions, including H.M., that established the role of these structures in new memories.
- Bliss, T. V. P. & Lømo, T. (1973). Long-lasting potentiation of synaptic transmission in the dentate area of the anaesthetized rabbit following stimulation of the perforant path. *The Journal of Physiology*. https://doi.org/10.1113/jphysiol.1973.sp010273 — The first report of long-lasting potentiation, the synaptic change that many memory models build on.
- McClelland, J. L., McNaughton, B. L. & O'Reilly, R. C. (1995). Why there are complementary learning systems in the hippocampus and neocortex: Insights from the successes and failures of connectionist models of learning and memory. *Psychological Review*. https://doi.org/10.1037/0033-295X.102.3.419 — The original complementary learning systems theory, with simulations of interference and interleaved learning.

### Surveys and textbooks

- Kumaran, D., Hassabis, D. & McClelland, J. L. (2016). What learning systems do intelligent agents need? Complementary learning systems theory updated. *Trends in Cognitive Sciences*. https://doi.org/10.1016/j.tics.2016.05.004 — Revisits the theory in light of deep learning, replay and the roles of the two systems.
- Richards, B. A. & Frankland, P. W. (2017). The persistence and transience of memory. *Neuron*. https://doi.org/10.1016/j.neuron.2017.04.037 — Argues that forgetting supports generalisation, and that memory should be seen as a balance of persistence and transience.
