---
related:
- society/philosophy
- society/ethics
aliases:
  - 意識
  - 心靈哲學
  - Consciousness
---

# Consciousness & Philosophy of Mind

## The questions

- **Easy problems** (Chalmers, 1995): explaining functions such as discrimination, report, attention and integration — hard in practice but standard science
- **Hard problem**: why is there *something it is like* to have these functions at all (phenomenal experience, qualia)?
- For AI: can a machine be conscious? How would we know? Would it matter morally?

## Positions in philosophy of mind

| Position | Claim | Implication for AI |
|---|---|---|
| Dualism | Mind is non-physical | Machines likely can't be conscious |
| Physicalism / identity theory | Mental states are brain states | Depends on whether the right physical states can be built |
| Functionalism | Mental states are defined by functional roles | A machine with the right organisation could be conscious (substrate independence) |
| Biological naturalism (Searle) | Consciousness depends on specific biological causal powers | Computation alone is insufficient |
| Illusionism (Frankish, Dennett) | Phenomenal consciousness as usually conceived is an illusion | The question shifts to functional self-models |
| Panpsychism | Consciousness is a fundamental feature of matter | Unclear; perhaps everything has some |

## Classic thought experiments

- **Turing test** (1950): behaviour as the criterion for thinking
- **Chinese room** (Searle, 1980): following rules to manipulate Chinese symbols produces correct answers without understanding — syntax is not sufficient for semantics. Replies: systems reply, robot reply (grounding), brain-simulator reply
- **Symbol grounding problem** (Harnad, 1990): how do symbols get meaning? Central to debates about text-only LLMs
- **Philosophical zombies**: beings behaviourally identical to us without experience
- **Mary's room** (Jackson): does knowing all physical facts about colour give you the experience of red?
- **Nagel's bat** (1974): "What is it like to be a bat?"

## Scientific theories of consciousness

| Theory | Core idea | Key proponents |
|---|---|---|
| Global workspace (GWT/GNW) | Conscious content is globally broadcast across specialised modules | Baars; Dehaene, Changeux |
| Integrated information theory (IIT) | Consciousness = integrated information (Φ) of a system's causal structure | Tononi, Koch |
| Higher-order theories (HOT) | A state is conscious when represented by a higher-order state | Rosenthal, Lau |
| Recurrent processing theory | Recurrent (feedback) processing in sensory cortex suffices | Lamme |
| Predictive processing / beast machine | Consciousness grounded in predictive regulation of the body | Seth, Clark |
| Attention schema theory | The brain models its own attention, and that model is our sense of awareness | Graziano |

**Adversarial collaborations**: the Templeton-funded collaboration testing GNW against IIT reported mixed results for both (Cogitate Consortium, 2025, *Nature*), and controversy followed when over 100 researchers labelled IIT "pseudoscience" in an open letter (2023), which others strongly disputed.

**Neural correlates of consciousness (NCC)**: posterior "hot zone" vs prefrontal involvement remains debated; methods include binocular rivalry, masking, no-report paradigms and the perturbational complexity index (TMS-EEG) used to assess consciousness in unresponsive patients.

## Key methods

### Integrated information theory (Tononi, 2004)

- **Problem:** what makes some physical systems conscious and others not, when we cannot ask them directly?
- **Core idea:** start from the properties every experience has (for example, that it exists, is unified, is specific and cannot be split into independent parts). Then ask what a physical system must be like to have those properties. The proposed quantity is integrated information, written Φ, which measures how much a system's causal structure is more than the sum of its parts.
- **Method:** a theoretical framework, not an experiment. The 2004 article states the framework in words, and later versions give formal definitions of Φ.
- **Results:** the article argues that the theory accounts for basic features of experience. It reports no experimental result of its own.
- **Limitations:** Φ is very hard to compute for realistic systems. The theory's claims about non-brain systems follow from its axioms and are contested; see the adversarial collaboration above.

### Global workspace (Dehaene & Naccache, 2001)

- **Problem:** what distinguishes information that reaches awareness from information that is processed without it?
- **Core idea:** a stimulus becomes conscious when it is amplified and broadcast across a network of distributed neurons, a global workspace. The broadcast makes the content available for report, memory and action. Unconscious processing stays local to specialised modules.
- **Method:** a review of experimental evidence, including paradigms that separate seen from unseen stimuli, used to argue that conscious access is an all-or-none transition.
- **Results:** the review argues that the evidence fits a model in which conscious access is an all-or-none, globally broadcast state.
- **Limitations:** the framework describes access to information, which is not the same as phenomenal experience. The evidence comes from laboratory tasks, and rival theories such as recurrent processing make different predictions, as the table above shows.

## Could AI be conscious?

Butlin, Long et al. (2023), "Consciousness in Artificial Intelligence: Insights from the Science of Consciousness", derived **indicator properties** from major theories (e.g. recurrent processing, global workspace, higher-order monitoring, agency and embodiment) and assessed current systems. Their conclusion: no current AI system was a strong candidate, but there were no obvious technical barriers to building systems that satisfy many indicators.

Considerations:

- LLM self-reports are unreliable evidence: models are trained on human text describing experiences
- Architecture matters for many theories (recurrence, global broadcast, self-models), not only behaviour
- IIT implies standard digital computers have very low Φ regardless of the software they run
- Biological-naturalist views deny machine consciousness outright

## Moral status and model welfare

If AI systems could have experiences or interests, they might deserve moral consideration. Long, Sebo et al. (2024), "Taking AI Welfare Seriously", argued companies should prepare for this possibility. Some AI developers have begun research programmes on model welfare (for example, Anthropic announced one in 2025). Others warn that attributing consciousness prematurely could mislead users and distract from human harms. This remains deeply uncertain.

## Resources

- Chalmers, *The Conscious Mind*; and "Could a Large Language Model be Conscious?" (2023)
- Dehaene, *Consciousness and the Brain*
- Seth, *Being You*
- Koch, *The Feeling of Life Itself*
- [Stanford Encyclopedia of Philosophy: Consciousness](https://plato.stanford.edu/entries/consciousness/), [The Chinese Room Argument](https://plato.stanford.edu/entries/chinese-room/)
- Butlin, Long et al. (2023), arXiv:2308.08708

## References

### Seminal papers

- Nagel, T. (1974). What Is It Like to Be a Bat? *The Philosophical Review*. https://doi.org/10.2307/2183914 — The classic argument that subjective experience cannot be fully captured by objective description.
- Dehaene, S. & Naccache, L. (2001). Towards a cognitive neuroscience of consciousness: basic evidence and a workspace framework. *Cognition*. https://doi.org/10.1016/S0010-0277(00)00123-2 — The global-workspace account of conscious access, with the experimental evidence behind it.
- Tononi, G. (2004). An information integration theory of consciousness. *BMC Neuroscience*. https://doi.org/10.1186/1471-2202-5-42 — Integrated Information Theory, which links consciousness to a system's integrated information.
- Friston, K. (2010). The free-energy principle: a unified brain theory? *Nature Reviews Neuroscience*. https://doi.org/10.1038/nrn2787 — Proposes that brains minimise prediction error, a unifying framework for perception, action and learning.
- Clark, A. (2013). Whatever next? Predictive brains, situated agents, and the future of cognitive science. *Behavioral and Brain Sciences*. https://doi.org/10.1017/S0140525X12000477 — A review of predictive processing as a unifying framework for perception, action and cognition.
