---
status: draft
last_reviewed: 2026-10-28
tags:
- neuroscience
- episodic memory
aliases:
  - 目標記憶再活化
  - Targeted Memory Reactivation
  - Rasch et al 2007
---

# Targeted Memory Reactivation (Rasch et al., 2007)

Rasch and colleagues tested whether reactivating a memory during sleep causes it to be consolidated. Participants learned a task in the presence of an odour, and the odour was presented again during sleep. Re-exposure during slow-wave sleep improved retention of hippocampus-dependent declarative memories. The same cue had no such effect during REM sleep or wakefulness, or when the odour had been absent during learning. The method is one of the two in [Sleep, Replay and Memory Consolidation](../index.md).

## Overview

Many studies show that sleep helps memory, but the benefit alone does not show that reactivation of a memory during sleep causes it to be consolidated. The problem is to find a way to reactivate one specific memory during sleep, without waking the sleeper, and then see whether that reactivation changes later retention.

Rasch et al. (2007) addressed this with a context cue. An odour that was present while a memory was formed becomes part of the memory's context. Presenting the same odour during sleep is therefore a targeted way to reactivate that memory. The design includes several control conditions, so that a benefit can be linked to the particular combination of cue, sleep stage and memory type.

## Key concepts

- **Targeted memory reactivation (TMR)**: presenting, during sleep, a cue that was paired with a memory during learning, so that the memory is reactivated.
- **Context cue**: a stimulus present during learning, here an odour, that becomes associated with the memory.
- **Declarative and procedural memory**: declarative memories are facts and events that can be stated, and they depend on the hippocampus. Procedural memories are skills, and in the study they did not depend on the hippocampus.
- **Slow-wave sleep and REM sleep**: the two sleep stages compared in the study. REM sleep serves as a comparison stage, since the cue had no benefit there.

## How it works

The experiment can be read as a numbered procedure:

1. **Learning.** Participants learn a memory task while an odour is presented as a context.
2. **Cueing.** During sleep, the same odour is presented again during slow-wave sleep. Control conditions present the odour during REM sleep, during wakefulness, or during slow-wave sleep when the odour had been omitted at learning.
3. **Test.** Retention is tested after sleep for a declarative task and for a procedural task, which the hippocampus does not depend on.
4. **Imaging.** Functional MRI records hippocampal activity while the odour is re-presented during slow-wave sleep.

The logic is conjunctive. If reactivation drives consolidation, the benefit should appear only when the cue was tied to the learning, arrived during slow-wave sleep, and concerned a hippocampus-dependent memory. The abstract reports that the benefit failed under each control, and that the procedural memory did not benefit.

## Results

The main result is qualitative: re-exposure to the learning odour during slow-wave sleep improved retention of the declarative memory, and did not improve the procedural memory. Re-exposure during REM sleep or wakefulness had no such effect, and neither did re-exposure when the odour had been omitted during learning. The imaging showed significant hippocampal activation in response to the odour during slow-wave sleep. The abstract gives no numerical effect sizes, so this page quotes none.

## Limitations

- The odour is a proxy for reactivation. A cue can also change arousal or attention during sleep, and the controls reduce but do not remove that concern.
- The imaging result is correlational. Hippocampal activation shows that the hippocampus responds to the cue, but not how the response relates to the memory.
- The study tests one cue modality and two memory types. It does not show which memories a cue can strengthen, or how well the effect generalises to other tasks.

## Open questions

- **Does cueing select memories or only reactivate them?** It is not clear whether a cue strengthens the memories it reactivates most strongly, or whether it selects among them.
- **Is the effect a reactivation effect?** Cueing could also work through sleep arousal. Separating these explanations is a central test.
- **How does cueing relate to replay in ripples?** The recordings of Wilson and McNaughton (1994) were of unprompted replay. Whether a cue reaches the same ripple-based replay is open.
- **What is the AI analogue?** Selective replay is a common idea in deep RL, where it is studied as prioritised or targeted sampling of stored transitions. See [Experience Replay](../../../theory/paradigms/reinforcement-learning/experience-replay/index.md).

## References

### Seminal papers

- Rasch, B., Büchel, C., Gais, S. & Born, J. (2007). Odor Cues During Slow-Wave Sleep Prompt Declarative Memory Consolidation. *Science*. https://doi.org/10.1126/science.1138581 — Shows that re-presenting a learning odour during slow-wave sleep improves retention of declarative memories, with controls for sleep stage and cue.
- Wilson, M. A. & McNaughton, B. L. (1994). Reactivation of Hippocampal Ensemble Memories During Sleep. *Science*. https://doi.org/10.1126/science.8036517 — Records place-cell ensembles during spatial tasks and in sleep, and shows that waking co-firing patterns recur in later sleep.

### Surveys and textbooks

- Rasch, B. & Born, J. (2013). About Sleep's Role in Memory. *Physiological Reviews*. https://doi.org/10.1152/physrev.00032.2012 — Reviews how slow-wave sleep reactivation drives consolidation, and how REM sleep may stabilise memories.
- Diekelmann, S. & Born, J. (2010). The memory function of sleep. *Nature Reviews Neuroscience*. https://doi.org/10.1038/nrn2762 — Reviews the evidence that sleep contributes to memory processing, and how different sleep stages do so.
- Walker, M. P. & Stickgold, R. (2004). Sleep-Dependent Learning and Memory Consolidation. *Neuron*. https://doi.org/10.1016/j.neuron.2004.08.031 — Reviews how sleep after learning supports memory consolidation in humans.
