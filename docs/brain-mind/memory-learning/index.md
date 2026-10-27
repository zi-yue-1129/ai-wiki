# Memory & Learning in the Brain

## Kinds of memory

```mermaid
flowchart TB
  M[Memory] --> STM[Short-term / working memory]
  M --> LTM[Long-term memory]
  LTM --> DEC[Declarative / explicit]
  LTM --> NONDEC[Non-declarative / implicit]
  DEC --> EP[Episodic: events — hippocampus]
  DEC --> SEM[Semantic: facts — neocortex]
  NONDEC --> PROC[Procedural: skills — basal ganglia, cerebellum]
  NONDEC --> PRIME[Priming — cortex]
  NONDEC --> COND[Conditioning — amygdala, cerebellum]
```

| Memory system | Brain basis | AI counterpart |
|---|---|---|
| Working memory | Prefrontal and parietal persistent activity; limited capacity (~4 chunks, Cowan 2001) | Context window, recurrent state |
| Episodic | Hippocampus, binding "what–where–when" | Episodic buffers, retrieval-augmented memory, conversation logs |
| Semantic | Distributed neocortex, anterior temporal lobe hub | Model weights, knowledge graphs |
| Procedural | Basal ganglia, cerebellum, motor cortex | Policies, tool/skill libraries |

## Patient H.M.

After bilateral removal of medial temporal lobes in 1953 to treat epilepsy, Henry Molaison could no longer form new episodic memories, yet he could learn new motor skills (mirror drawing) without remembering practising. Brenda Milner's studies established that memory has multiple systems and that the hippocampus is essential for forming declarative memories.

## Synaptic plasticity

- **Long-term potentiation (LTP)** (Bliss & Lømo, 1973) and **long-term depression (LTD)**: persistent strengthening or weakening of synapses
- **NMDA receptors** act as coincidence detectors — they open only when presynaptic glutamate arrives *and* the postsynaptic neuron is depolarised — a molecular Hebbian rule
- **Early vs late LTP**: protein synthesis is needed for lasting changes; **synaptic tagging and capture** explains how weak and strong events interact
- **Structural plasticity**: dendritic spines grow and retract; some persist for months
- **Homeostatic plasticity** (synaptic scaling) keeps activity in range — akin to normalisation layers
- **Engram cells**: memories can be reactivated by optogenetically stimulating the neurons active during learning (Tonegawa lab; Liu et al., 2012)

## Consolidation and replay

- **Systems consolidation**: memories initially depend on the hippocampus and gradually become cortical
- **Sharp-wave ripples**: during rest and slow-wave sleep, hippocampal place cells **replay** recent experiences in compressed time, sometimes in reverse and sometimes as novel trajectories (Wilson & McNaughton, 1994; Foster & Wilson, 2006)
- Disrupting ripples impairs learning; enhancing them can improve it
- **Sleep**: slow oscillations, spindles and ripples coordinate hippocampal–cortical dialogue; the synaptic-homeostasis hypothesis proposes sleep downscales synapses

### Complementary learning systems (CLS)

McClelland, McNaughton & O'Reilly (1995) explained *why* two systems exist:

- The **hippocampus** learns quickly with sparse, pattern-separated codes, storing individual episodes without interference
- The **neocortex** learns slowly with overlapping, distributed codes, extracting statistical structure
- Fast learning in the cortex would cause **catastrophic interference**; instead, the hippocampus **interleaves** replay of old and new memories to train the cortex

This is the conceptual root of **experience replay** in deep RL and of replay-based [continual learning](../../foundations/paradigms/continual/index.md). Kumaran, Hassabis & McClelland (2016) updated the theory for the deep-learning era.

## Forgetting is a feature

- Ebbinghaus's forgetting curve (1885): rapid early loss, then levelling off
- **Spacing effect** and **testing effect**: distributed practice and retrieval practice greatly improve retention — the basis of spaced-repetition software (Anki, SuperMemo), which uses models of memory decay
- Forgetting may aid generalisation and avoid overfitting to outdated information (Richards & Frankland, 2017, "The persistence and transience of memory")
- **Reconsolidation**: retrieved memories become labile and can be updated — memory is reconstructive, not a recording (Bartlett; Loftus's misinformation studies)

## Pattern separation and completion

- **Dentate gyrus** performs pattern separation (making similar inputs distinct)
- **CA3** recurrent collaterals perform pattern completion (retrieving a whole memory from a cue) — a Hopfield-like **autoassociative memory**
- Modern Hopfield networks connect this to Transformer attention (see [Transformers](../../models/transformer/index.md))

## Memory in AI systems: design lessons

| Brain lesson | AI design |
|---|---|
| Separate fast episodic and slow semantic stores | RAG / external memory + model weights |
| Replay prevents interference | Replay buffers, rehearsal in continual learning |
| Consolidate what matters | Summarise and distil agent memories; prioritised replay |
| Retrieval is cue-dependent and reconstructive | Retrieval quality depends on query formulation; generated "memories" can be wrong |
| Forgetting is useful | Memory decay, recency weighting, pruning stale knowledge |
| Working memory is limited and actively maintained | Context management, scratchpads, task decomposition |

## Resources

- Squire & Kandel, *Memory: From Mind to Molecules*
- Eichenbaum, *The Cognitive Neuroscience of Memory*
- McClelland, McNaughton & O'Reilly (1995), *Psychological Review*
- Kumaran, Hassabis & McClelland (2016), "What learning systems do intelligent agents need?", *Trends in Cognitive Sciences*
- Buzsáki, *The Brain from Inside Out*
