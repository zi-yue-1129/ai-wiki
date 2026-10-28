---
status: complete
last_reviewed: 2026-10-28
---

# Global workspace (Dehaene & Naccache, 2001)

A piece of information becomes conscious when it is amplified and broadcast across a distributed network of neurons, which makes it available to many other processes at once.

## Overview

Most of what the brain does never reaches awareness. A driver can react to a hazard without noticing it, and a briefly flashed word can change a later response even when the reader reports seeing nothing. Dehaene and Naccache (2001) asked what separates information that enters awareness from information that stays unconscious. Their answer, the *global neuronal workspace* hypothesis, places consciousness in a process rather than in one brain area. Many specialised modules process information in parallel. Conscious access happens when the content of one module is made available to the rest of the brain.

The framework has become one of the two leading scientific theories of consciousness, and it is the main rival of [Integrated Information Theory](../integrated-information-theory/index.md).

## Key concepts

- **Specialised processors**: modules for perception, motor preparation, memory, evaluation and attention. They work in parallel and, on their own, produce no awareness.
- **Global workspace**: a set of neurons, spread across the cortex and heavily interconnected by long-range axons, that can share information between processors.
- **Mobilisation (ignition)**: a sudden, self-sustaining, brain-wide activation that puts a representation into the workspace. "Ignition" is the usual term in later work.
- **Conscious access**: the state in which content can be reported, remembered and used to guide deliberate action.
- **Masking**: a paradigm in which a brief stimulus is followed quickly by a second stimulus, so that the first is not reported. Researchers use it to compare seen and unseen stimuli.

## Problem

Processing without awareness is real, and it can be surprisingly complex. A stimulus that is too brief or too weak to report can still shift attention, prime a later word or influence a choice. A theory of consciousness therefore has to say where the boundary between seen and unseen falls, and why it falls there.

Dehaene and Naccache framed the problem with three empirical findings that a theory should explain. First, much processing happens without consciousness. Second, attention is a prerequisite for conscious perception. Third, some operations seem to require awareness: keeping information available over time, combining operations in new ways, and acting on spontaneous intentions.

## Core idea

The framework splits the brain into two computational spaces. The first contains many specialised modules that process their inputs quickly and in parallel. The second is the global workspace, a network of neurons with long-range connections, which the 2001 paper places most strongly in prefrontal cortex, anterior cingulate cortex and their connected areas.

A stimulus processed by a module alone stays unconscious. If the stimulus is strong or sustained enough, top-down attention amplifies its representation and mobilises workspace neurons into a self-sustaining, coherent state. This state is then available to perception, memory, evaluation and action at the same time. The authors identify this global availability with conscious access. They also note that the workspace has no fixed location: its boundaries shift as different circuits are recruited and released.

## Equation or algorithm

The 2001 framework is verbal rather than mathematical, so its core process is best written as numbered steps:

1. A stimulus activates its specialised processor. The processing runs in parallel with other modules and stays local when the stimulus is brief or weak.
2. If the representation is strong enough and attention amplifies it, it crosses a threshold and recruits workspace neurons with long-range connections.
3. The recruited neurons settle into a self-sustaining, coherent state that feeds back onto the processors.
4. While this state lasts, the content is available for report, memory, evaluation and action. Information below the threshold influences behaviour only through local processing.

A computational version of the idea appeared in Dehaene, Kerszberg and Changeux (1998). In their model of the Stroop task, workspace activity rose during the acquisition of a new task, during effortful execution, and after errors. This is the best-known simulation of the framework.

## Results

The 2001 paper is a review rather than a single experiment. It brings together evidence from masked and unmasked presentations. In these studies, some stimuli are processed well enough to change later behaviour, such as priming, without ever being reported. Other stimuli, once they cross the threshold, produce a sudden change that participants can report. The paper uses this contrast to argue for an all-or-none transition into conscious access. It also makes predictions about the timing and location of brain activity, which later experiments were designed to test.

A large recent test is the 2025 adversarial collaboration reported by the Cogitate Consortium (2025). It compared the workspace theory and Integrated Information Theory in 256 human participants, using functional MRI, magnetoencephalography and intracranial recordings. Information about conscious content was found in visual, ventrotemporal and inferior frontal cortex. The authors report that the results align with some predictions of the workspace theory but challenge key tenets of it. In particular, the data did not generally show the sustained ignition the theory predicted at stimulus offset.

## Limitations

The framework explains which information is available, reportable and usable. It does not, by itself, explain why this availability is accompanied by subjective experience. The authors treat global availability as what experience is. Critics argue that this is a hypothesis rather than a demonstration, and that the explanatory gap remains, which is the "hard problem" discussed on the [parent page](../index.md).

The evidence comes mostly from laboratory tasks with simple stimuli and reports. Many paradigms require the participant to say what they saw, which makes it hard to separate awareness from the act of reporting. No-report paradigms were developed to address this, but they are not yet decisive. The framework makes predictions that can be tested, and the 2025 adversarial collaboration reported that some of them were challenged by the data. The debate about the theory is therefore more open than the 2001 text suggests.

## Key methods

Four landmark alternatives explain conscious access or experience in different ways:

- [Integrated Information Theory (Tononi, 2004)](../integrated-information-theory/index.md): consciousness is a property of integrated causal structure, not of broadcast, so the two theories disagree on what makes a system conscious.
- Recurrent processing theory: consciousness depends on feedback within sensory cortex, and it does not need a late, global broadcast.
- Higher-order theories: a state is conscious when the system represents it with a further, higher-order state.
- [Predictive processing](../../predictive-coding/index.md): perception and awareness arise from a brain that continually predicts its inputs and corrects its predictions.

## Connections

- Parent topic: [Consciousness & Philosophy of Mind](../index.md)
- Other method on this topic: [Integrated Information Theory](../integrated-information-theory/index.md)
- Attention: the 2001 framework treats top-down attention as the amplifier that gives a representation access. See [Attention & Brain-Machine Interfaces](../../attention-brain-machine/index.md).
- Memory: a workspace that holds content for report also gives memory systems something to store. See [Memory & Learning in the Brain](../../memory-learning/index.md).

## Applications

- **Experimental design.** Masking, no-report and adversarial collaboration are used to test whether conscious contents follow the workspace predictions. The 2025 Cogitate study is an example.
- **Assessing artificial systems.** Butlin et al. (2023) derive "indicator properties" from five theories, including global workspace, and assess current AI systems against them. Their conclusion is that none of the systems they evaluated appears to be conscious, but that there is no clear technical barrier to building systems with these indicators.

## Open questions

- Is an all-or-none, sustained ignition necessary for conscious access, or does it appear only when the task requires a report? The 2025 results make this question sharper but do not settle it.
- Where, anatomically, is the workspace? The debate between prefrontal and posterior accounts is still open.
- Can any functional account explain why global availability feels like something?
- If a machine implements the same workspace architecture, would it be conscious? Indicator-based assessments say there is no obvious technical barrier, but whether the indicators are sufficient is debated.

## References

### Seminal papers

- Dehaene, S. & Naccache, L. (2001). Towards a cognitive neuroscience of consciousness: basic evidence and a workspace framework. *Cognition*. https://doi.org/10.1016/S0010-0277(00)00123-2 — The workspace framework itself, including the three empirical findings it aims to explain and its testable predictions.
- Dehaene, S., Kerszberg, M. & Changeux, J.-P. (1998). A neuronal model of a global workspace in effortful cognitive tasks. *Proceedings of the National Academy of Sciences*. https://doi.org/10.1073/pnas.95.24.14529 — A computer model of the workspace, in which workspace activity rises during learning, effortful execution and errors in the Stroop task.

### Surveys and textbooks

- Dehaene, S. & Changeux, J.-P. (2011). Experimental and theoretical approaches to conscious processing. *Neuron*. https://doi.org/10.1016/j.neuron.2011.03.018 — Review of how the workspace model is linked to experimental work on conscious and unconscious processing.
- Mashour, G. A. et al. (2020). Conscious processing and the global neuronal workspace hypothesis. *Neuron*. https://doi.org/10.1016/j.neuron.2020.01.026 — Review of the global neuronal workspace hypothesis and of the experimental evidence that bears on it.
- Cogitate Consortium et al. (2025). Adversarial testing of global neuronal workspace and integrated information theories of consciousness. *Nature*. https://doi.org/10.1038/s41586-025-08888-1 — A preregistered test of workspace and integrated-information predictions with 256 participants and three recording methods.

### Articles and documentation

- Butlin, P., Long, R., Elmoznino, E. et al. (2023). Consciousness in artificial intelligence: insights from the science of consciousness. arXiv. https://arxiv.org/abs/2308.08708 — Derives indicator properties from five theories, including the global workspace, and assesses current AI systems against them.
