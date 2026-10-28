---
status: draft
last_reviewed: 2026-10-28
tags:
- neuroscience
- episodic memory
aliases:
  - 海馬迴重播
  - Wilson and McNaughton 1994
  - Hippocampal Replay
---

# Hippocampal Replay (Wilson & McNaughton, 1994)

Wilson and McNaughton recorded many hippocampal place cells in rats during spatial behaviour and again during the sleep that followed. Cells that had fired together while the rat occupied particular places fired together more often in the later sleep. The paper is an early direct demonstration that waking experience is re-expressed in the hippocampus during sleep. It is one method behind [Sleep, Replay and Memory Consolidation](../index.md).

## Overview

Place cells are hippocampal neurons that fire when an animal is in a particular location. Because an animal visits many locations, its experience is represented by an ensemble of place cells, each active in its own part of the environment. Theories of memory consolidation proposed that recent experience is reactivated during sleep. Wilson and McNaughton tested this by recording ensembles during slow-wave sleep, before and after behaviour.

The result connects to the wider account in [Complementary Learning Systems](../../memory-learning/complementary-learning-systems/index.md). In that theory, the hippocampus stores recent episodes quickly, and the neocortex is trained slowly by replaying those episodes. The 1994 paper is the physiological observation that replay of this kind occurs during sleep.

## Key concepts

- **Place cell**: a hippocampal neuron whose firing is tied to a location in the environment.
- **Ensemble**: a set of neurons recorded at the same time and analysed together, rather than one at a time.
- **Co-firing**: the tendency of two cells to fire within the same short window. The paper compares co-firing across sleep sessions.
- **Replay**: the re-expression of a waking firing pattern during rest or sleep.
- **Slow-wave sleep**: the non-REM stage in which the sleep episodes in the study were recorded.

## How it works

The study can be read as a numbered procedure:

1. Record large ensembles of hippocampal place cells in rats during spatial behavioural tasks.
2. Record in slow-wave sleep before the tasks, and again in slow-wave sleep after them, in the same animals.
3. For each pair of cells, measure how often the two fire together in each sleep episode.
4. Compare pairs whose place fields overlapped during behaviour with pairs whose fields did not, and compare sleep after behaviour with sleep before it.

In notation, let $C^{\text{pre}}_{ij}$ and $C^{\text{post}}_{ij}$ be the co-firing of cells $i$ and $j$ in sleep before and after the task. The claim is that $C^{\text{post}}_{ij} > C^{\text{pre}}_{ij}$ on average for pairs that shared spatial firing during behaviour, and not for pairs that did not. The paper suggests that this increase may reflect synaptic modification during waking experience.

## Results

The main evidence is the pre-task and post-task sleep comparison from ensembles recorded in three rats. The increase in co-firing was specific to cells that fired together during the task. Cells that were inactive during behaviour, or that had non-overlapping spatial firing, did not show it. The effect declined gradually over each post-task sleep session. The abstract reports no numerical benchmark, so this page quotes none.

## Limitations

- The study used three animals, and the design is correlational. It shows that waking patterns recur in sleep. It does not show that the recurrence stores the memory.
- Co-firing is a summary of pairs. It does not capture the order in which cells fired, which later work examined (Foster & Wilson, 2006; Diba & Buzsáki, 2007).
- Replay was studied in rodents, and the link between replay and memory was inferred. Later work used ripple disruption and cueing to test the causal question, summarised in Buzsáki (2015) and in [Targeted Memory Reactivation](../targeted-memory-reactivation/index.md).
- Sleep replay was also found in visual cortex together with the hippocampus (Ji & Wilson, 2006), which the 1994 recordings did not address.

## Open questions

- **Which features of the waking pattern are replayed?** Frequency, reward and novelty may all play a part. Mattar and Daw (2018) argue that prioritised memory access, tied to planning, can explain the replay pattern.
- **Does replay track the content of memory?** Replayed sequences are compressed in time, and the mapping from replayed pattern to stored content is still under study.
- **How do forward and reverse replay differ?** Diba and Buzsáki (2007) report both forward and reverse sequences during ripples, and their functional roles are not yet settled.

## References

### Seminal papers

- Wilson, M. A. & McNaughton, B. L. (1994). Reactivation of Hippocampal Ensemble Memories During Sleep. *Science*. https://doi.org/10.1126/science.8036517 — Records place-cell ensembles during spatial tasks and in sleep, and shows that waking co-firing patterns recur in later sleep.
- Foster, D. J. & Wilson, M. A. (2006). Reverse replay of behavioural sequences in hippocampal place cells during the awake state. *Nature*. https://doi.org/10.1038/nature04587 — Reports that place-cell sequences from running are replayed in reverse order during the awake state, extending replay beyond sleep.
- Diba, K. & Buzsáki, G. (2007). Forward and reverse hippocampal place-cell sequences during ripples. *Nature Neuroscience*. https://doi.org/10.1038/nn1961 — Reports that place-cell sequences replayed during sharp-wave ripples run both forward and in reverse.
- Ji, D. & Wilson, M. A. (2006). Coordinated memory replay in the visual cortex and hippocampus during sleep. *Nature Neuroscience*. https://doi.org/10.1038/nn1825 — Reports that replay during sleep is coordinated between visual cortex and hippocampus.
- Mattar, M. G. & Daw, N. D. (2018). Prioritized memory access explains planning and hippocampal replay. *Nature Neuroscience*. https://doi.org/10.1038/s41593-018-0232-z — Proposes that prioritised memory access, linked to planning, can explain the pattern of hippocampal replay.

### Surveys and textbooks

- Buzsáki, G. (2015). Hippocampal sharp wave-ripple: A cognitive biomarker for episodic memory and planning. *Hippocampus*. https://doi.org/10.1002/hipo.22488 — Reviews sharp-wave ripples as the setting for compressed replay, and the evidence that disrupting them impairs memory.
- Diekelmann, S. & Born, J. (2010). The memory function of sleep. *Nature Reviews Neuroscience*. https://doi.org/10.1038/nrn2762 — Reviews the evidence that sleep contributes to memory processing, and how different sleep stages do so.
