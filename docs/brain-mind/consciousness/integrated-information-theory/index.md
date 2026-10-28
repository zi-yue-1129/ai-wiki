---
status: complete
last_reviewed: 2026-10-28
---

# Integrated information theory (Tononi, 2004)

Integrated information theory identifies consciousness with a system's capacity to integrate information, measured by a quantity called Φ (phi).

## Overview

Consciousness is hard to study because we can only observe it directly in ourselves, and we infer it in others from behaviour and brain activity. Tononi (2004) took a different route. Instead of asking which brain processes correlate with experience, he asked what experience must be like in order to be what it is, and then asked what kind of physical system could have those properties. The resulting theory says that consciousness is the capacity of a system to integrate information. It makes claims about which systems are conscious, how much, and of what kind.

The theory is one of the two leading scientific accounts of consciousness, alongside the [Global Workspace](../global-workspace/index.md) theory, and the two have been tested against each other experimentally.

## Key concepts

- **Phenomenological axioms**: properties that every experience has. Tononi and Koch (2015) list five: intrinsic existence, composition, information, integration and exclusion.
- **Postulates**: the properties a physical system must have to support experience, derived from the axioms.
- **Integrated information (Φ)**: the amount of causally effective information that a system generates above and beyond its parts, measured across the weakest link of a partition.
- **Complex**: a subset of elements with Φ greater than zero that is not part of a larger subset with higher Φ. The complex is the unit of consciousness.
- **Minimum information partition (MIP)**: the way of cutting a system that changes its causal structure the least. Φ is measured across this cut.

## Problem

Why is the cerebral cortex conscious while the cerebellum, which has more neurons, is not? Why is consciousness present in wakefulness and reduced in dreamless sleep? And how could we judge whether a patient with severe brain damage, a newborn or a machine is conscious when we cannot ask them? Correlates of consciousness, such as activity in a particular network, do not answer these questions on their own, because they say nothing about why the correlate matters. Tononi argued that a theory is needed that says what experience is and which physical systems can have it.

## Core idea

The argument starts from experience itself. Tononi (2004) emphasised two properties that every conscious experience shares. The first is differentiation: the very large number of distinct experiences a system can have. The second is integration: each experience is unified, and it cannot be split into independent parts.

From these properties the theory asks what a physical system must be like to have them. Its answer is that the system must have a causal structure in which its elements are informative about one another and cannot be broken into independent subsystems without losing information. The degree of this unity is Φ. The quality of an experience is then given by the pattern of informational relations among the elements, and the quantity by Φ. Later versions of the theory replaced these ideas with more formal definitions, but the central claim has stayed the same.

## Equation or algorithm

The formal definition of Φ in IIT 3.0 (Oizumi, Albantakis & Tononi, 2014) can be written in simplified form. Let $S$ be a set of elements in a given state, $\mathcal{C}(S)$ be its constellation of concepts (the cause-effect structure of the whole), and $\mathcal{C}(S^{P})$ be the constellation of the same elements after a partition $P$ has cut the causal connections between the parts. Then

$$
P^{*} = \arg\min_{P} \; D\big(\mathcal{C}(S),\, \mathcal{C}(S^{P})\big), \qquad \Phi(S) = D\big(\mathcal{C}(S),\, \mathcal{C}(S^{P^{*}})\big),
$$

where $D$ is the extended earth mover's distance between constellations. The partition $P^{*}$ is the minimum information partition: it changes the constellation the least. Φ is the difference that remains after this cut. This follows the description in Oizumi et al. (2014), where the partition is evaluated in both directions between a subset and its complement. The notation here is a simplification, and the paper gives the full definitions.

The full theory can be read as a procedure:

1. State the phenomenological axioms of experience, as Tononi and Koch (2015) do.
2. Derive postulates about the physical mechanisms that would satisfy them.
3. For a candidate system in a given state, compute its constellation of concepts.
4. Consider every partition, find the minimum information partition, and measure Φ across it.
5. Call a subset a complex if its Φ is positive and no larger subset that contains it has higher Φ. Only complexes count as conscious.

## Results

The 2004 article is theoretical. It reports no new experiments. It argues that the theory accounts for several neurobiological observations: why consciousness is linked to certain neural systems, such as the thalamocortical system, and not to others, such as the cerebellum; why consciousness is reduced in dreamless sleep and during generalised seizures; and why neural interactions that support consciousness need time to work. Later work applies the theory to measurement. Casali et al. (2013) introduced a theory-derived index based on the complexity of the brain's response to a stimulus, and reported that the index measures the level of consciousness in awake, sleeping, anaesthetised and brain-damaged subjects.

A major test is the 2025 adversarial collaboration reported by the Cogitate Consortium. Its key IIT result was that the data showed no sustained synchronisation within the posterior cortex. The authors report that this contradicts the claim that the connectivity of the network specifies consciousness, which is a core prediction of the theory.

## Limitations

Φ is very hard to compute for realistic systems. A definition based on the minimum over partitions requires considering every way of cutting the system, and the number of ways grows very fast with the number of elements. This makes it hard to apply the theory to the human brain, let alone to other systems.

The theory's most striking claims concern systems other than brains. Tononi and Koch (2015) argue that, according to the theory, digital computers would experience next to nothing even if they behaved like humans or simulated the human brain. The claim follows from the axioms and postulates, so it depends on accepting them, and many researchers do not.

The formal definition has also changed between versions. Albantakis et al. (2023) present IIT 4.0, which introduces a new measure of intrinsic information and a more explicit treatment of causal relations. Because of these changes, results obtained under one version of the formalism may not transfer directly to another.

Finally, the empirical tests have challenged predictions of the theory. The 2025 Cogitate results did not support all of the theory's predictions, and this shows the framework is testable but not yet confirmed.

## Key methods

Three landmark alternatives explain consciousness differently from integrated information:

- [Global Workspace (Dehaene & Naccache, 2001)](../global-workspace/index.md): consciousness is the global broadcast of a representation to many processes, so it depends on access and not on the intrinsic structure of the system.
- Higher-order theories: a state is conscious when the system represents it with a higher-order state, so the account rests on meta-representation.
- [Predictive processing](../../predictive-coding/index.md): consciousness is tied to a brain that predicts and corrects its inputs, so it is explained by the function of prediction.

## Connections

- Parent topic: [Consciousness & Philosophy of Mind](../index.md)
- Other method on this topic: [Global Workspace](../global-workspace/index.md)
- Measurement: the perturbational complexity index in Casali et al. (2013) connects the theory to clinical assessment of consciousness in patients with brain damage. See [Consciousness & Philosophy of Mind](../index.md) for the wider debate on measuring awareness.
- Complexity and information: the theory's use of causal structure relies on the idea that information can be measured in a system. For the general concept, see [Computational Neuroscience](../../computational-neuroscience/index.md).

## Applications

- **Clinical assessment.** Casali et al. (2013) describe an index that quantifies the complexity of the brain's response to a stimulus. The authors report that it measures the level of consciousness across awake, sleeping, anaesthetised and brain-damaged subjects.
- **Assessing machines.** Tononi and Koch (2015) state that, according to IIT, digital computers would experience next to nothing, even if they reproduced human behaviour or ran faithful brain simulations. This implication is one reason the theory is discussed in debates about machine consciousness.
- **Testing theories.** The 2025 Cogitate collaboration was designed to make the theory's predictions testable against data, and it is a model for how competing theories of consciousness might be compared.

## Open questions

- Is Φ the right measure? The formal definition has already changed between versions, so it is fair to ask which version, if any, should be tested.
- Can Φ be computed for systems that are large enough to matter, or do we need approximations, and how good are they?
- Does the theory's account of experience extend to systems that are not brains? The implication for digital computers depends on the axioms that many researchers do not accept.
- How should the empirical failures of predictions in the 2025 study be interpreted? Does this count against the theory or against particular versions of it?

## References

### Seminal papers

- Tononi, G. (2004). An information integration theory of consciousness. *BMC Neuroscience*. https://doi.org/10.1186/1471-2202-5-42 — The original statement of the theory, which derives the quantity Φ from the properties of experience and applies it to neurobiological observations.
- Oizumi, M., Albantakis, L. & Tononi, G. (2014). From the phenomenology to the mechanisms of consciousness: Integrated Information Theory 3.0. *PLoS Computational Biology*. https://doi.org/10.1371/journal.pcbi.1003588 — Gives the formal definition of Φ in IIT 3.0, using a distance between constellations and the minimum information partition.
- Casali, A. G. et al. (2013). A theoretically based index of consciousness independent of sensory processing and behavior. *Science Translational Medicine*. https://doi.org/10.1126/scitranslmed.3006294 — Introduces a clinical index derived from IIT that measures the complexity of brain responses to stimulation, across awake, sleeping, anaesthetised and brain-damaged subjects.

### Surveys and textbooks

- Tononi, G. & Koch, C. (2015). Consciousness: here, there and everywhere? *Philosophical Transactions of the Royal Society B*. https://doi.org/10.1098/rstb.2014.0167 — A survey of the theory's five axioms, its postulates and its predictions, including for graded consciousness and digital computers.
- Tononi, G. et al. (2016). Integrated information theory: from consciousness to its physical substrate. *Nature Reviews Neuroscience*. https://doi.org/10.1038/nrn.2016.44 — Review of the theory and its account of the physical substrate of consciousness.
- Albantakis, L. et al. (2023). Integrated information theory (IIT) 4.0: formulating the properties of phenomenal existence in physical terms. *PLoS Computational Biology*. https://doi.org/10.1371/journal.pcbi.1011465 — The current formulation of the theory, with a new measure of intrinsic information and an explicit treatment of causal relations.
- Cogitate Consortium et al. (2025). Adversarial testing of global neuronal workspace and integrated information theories of consciousness. *Nature*. https://doi.org/10.1038/s41586-025-08888-1 — A preregistered comparison of IIT and the global workspace with 256 participants, showing where the theory's predictions held and where they failed.
