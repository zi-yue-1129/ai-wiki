---
related:
- brain-mind/consciousness
- brain-mind/memory-learning
---

# Cognitive Architectures

A **cognitive architecture** is a theory of the fixed structures of the mind — memories, processing modules, control — implemented as software that can run cognitive tasks. It aims at a "unified theory of cognition" (Newell, 1990) rather than a model of a single task.

## Classic architectures

| Architecture | Origin | Key ideas |
|---|---|---|
| **Soar** | Laird, Newell & Rosenbloom (1983–) | Problem spaces; production rules; impasses trigger subgoaling; chunking learns new rules; later added RL, episodic and semantic memory |
| **ACT-R** | Anderson (1990s–) | Modules (visual, motor, declarative, goal, imaginal) communicate via buffers; production rules; declarative memory with activation based on recency and frequency; module timings mapped to brain regions and validated with fMRI |
| **EPIC** | Kieras & Meyer | Detailed perceptual-motor processing; multitasking |
| **CLARION** | Sun | Explicit (symbolic) and implicit (subsymbolic) levels interact |
| **LIDA** | Franklin | Implements global workspace theory |
| **Sigma** | Rosenbloom | Graphical-model-based unification |
| **Spaun** | Eliasmith (2012) | 2.5-million spiking-neuron brain model performing eight tasks; built with the Neural Engineering Framework |
| **OpenCog / Hyperon** | Goertzel | AGI-oriented hybrid architecture |
| **Common Model of Cognition** | Laird, Lebiere & Rosenbloom (2017) | Community consensus on shared components across Soar, ACT-R and Sigma |

### ACT-R memory equation

The activation of a declarative chunk \(i\) reflects how often and how recently it was used:

\[
A_i = \ln \sum_{j=1}^{n} t_j^{-d} + \text{context} + \text{noise}
\]

where \(t_j\) is time since the j-th use and \(d \approx 0.5\). This reproduces power-law forgetting and practice effects — and is the basis of some adaptive tutoring systems.

## Global workspace theory

Baars (1988) proposed that many specialised unconscious processors compete for access to a limited-capacity **global workspace**; whatever wins is broadcast to all processors and becomes conscious. Dehaene's **global neuronal workspace** gives it a neural form (prefrontal–parietal "ignition"). It has inspired AI proposals for shared workspaces between modules (Goyal et al., 2022; VanRullen & Kanai, 2021) and is one lens for asking whether LLM agents could have consciousness-relevant properties (see [Consciousness](../consciousness/index.md)).

## Other architecture-level theories

- **Society of Mind** (Minsky, 1986): mind as many simple agents
- **Subsumption architecture** (Brooks, 1986): layered reactive behaviours without central representation — behaviour-based robotics
- **Thousand Brains theory** (Hawkins): many cortical columns each learn models of objects and vote
- **Hierarchical temporal memory** (Numenta)
- **LeCun's autonomous machine intelligence** proposal (2022): perception, world model, cost, actor, short-term memory and a configurator module

## LLM agents as cognitive architectures

LLM agents implicitly re-create cognitive architectures — see [AI Agents](../../theory/models/agents/index.md).

| Classic component | LLM-agent version |
|---|---|
| Working memory / buffers | Context window, scratchpad |
| Declarative memory | Retrieval over documents, vector stores |
| Episodic memory | Logged trajectories, reflections (Generative Agents' memory stream) |
| Procedural memory / productions | Tools, code, skill libraries (Voyager), system prompts |
| Decision cycle | Plan → act → observe loops (ReAct) |
| Learning (chunking) | Saving successful procedures as reusable skills |
| Metacognition | Self-critique, confidence estimation |

**CoALA** (Sumers, Yao, Narasimhan & Griffiths, 2023) formalises this mapping. A practical lesson from decades of architecture research: explicit memory management, control structures and learning mechanisms matter as much as the core reasoning engine.

## Why architectures still matter

- **Integration**: real intelligence combines perception, memory, reasoning and action in one system
- **Constraints from human data**: reaction times, error patterns and learning curves test whether a design is human-like
- **Applications**: intelligent tutoring (Carnegie Learning's cognitive tutors grew out of ACT-R), human-performance modelling in aviation and defence, user modelling in HCI
- **Interpretability**: explicit modules and traces are easier to inspect than monolithic networks

## Resources

- Newell, *Unified Theories of Cognition* (1990)
- Anderson, *How Can the Human Mind Occur in the Physical Universe?* (2007)
- Laird, *The Soar Cognitive Architecture* (2012)
- Kotseruba & Tsotsos (2020), "40 years of cognitive architectures: core cognitive abilities and practical applications", *Artificial Intelligence Review*
- [ACT-R website](http://act-r.psy.cmu.edu/), [Soar website](https://soar.eecs.umich.edu/)
- Eliasmith, *How to Build a Brain* (Spaun)
