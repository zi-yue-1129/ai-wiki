---
related:
- brain-mind/psychology
- brain-mind/consciousness
- society/philosophy
aliases:
  - 認知科學
  - 認知心理學
  - Cognitive science
---

# Cognitive Science

Cognitive science studies the mind as an information-processing system, combining psychology, neuroscience, linguistics, philosophy, anthropology and AI.

## Major frameworks

| Framework | Core claim | Era |
|---|---|---|
| Behaviourism | Study only observable behaviour (Watson, Skinner) | 1910s–1950s |
| Cognitivism / computationalism | The mind manipulates symbolic representations (Newell & Simon, Fodor) | 1950s– |
| Connectionism | Cognition emerges from networks of simple units (Rumelhart & McClelland, PDP) | 1980s– |
| Bayesian cognitive science | Cognition approximates probabilistic inference (Tenenbaum, Griffiths, Chater) | 2000s– |
| Embodied, embedded, enactive, extended (4E) | Cognition depends on body, environment and action (Varela, Clark) | 1990s– |
| Predictive processing | The brain is a hierarchical prediction machine (Friston, Clark, Hohwy) | 2000s– |

## Perception

- **Perception is inference**: the retinal image underdetermines the world; the brain combines it with priors (Helmholtz's "unconscious inference")
- **Gestalt principles**: proximity, similarity, closure, good continuation
- **Two visual streams**: ventral "what" and dorsal "where/how" pathways (Ungerleider & Mishkin; Goodale & Milner)
- **Illusions** reveal the brain's assumptions; some deep networks share them, others reveal different ones

## Attention

- Selective attention: filter theories (Broadbent), feature-integration theory (Treisman)
- Bottom-up salience vs top-down goals
- Limited capacity; **inattentional blindness** (the "invisible gorilla")
- Neural mechanisms: gain modulation, biased competition (Desimone & Duncan), oscillatory synchrony
- Transformer attention borrows the word but is a different mechanism — a learned, content-based weighting with no capacity limit beyond compute

## Language

- **Competence vs performance** (Chomsky); poverty-of-the-stimulus arguments for innate grammar
- **Usage-based and statistical learning** views (Tomasello; Saffran)
- Processing: incremental, predictive, sensitive to surprisal; ERP components N400 (semantics) and P600 (syntax)
- **The language network** (Fedorenko) is selective for language and dissociable from reasoning, math and social cognition — relevant to interpreting LLM abilities
- LLMs have revived debates about learnability, compositionality and meaning; see [NLP](../../theory/models/nlp/index.md) and [LLMs](../../theory/models/llm/index.md)

## Concepts and categories

- Classical (definitional) → prototype (Rosch) → exemplar → theory-theory views
- **Embodied / grounded concepts**: understanding "kick" engages motor regions (Barsalou; Pulvermüller)
- **Conceptual metaphor** (Lakoff & Johnson): abstract thought built on bodily experience
- **Compositionality and systematicity** (Fodor & Pylyshyn, 1988) — a long-running challenge to neural networks; recent meta-learning work shows networks can acquire human-like systematic generalisation (Lake & Baroni, 2023, *Nature*)

## Reasoning and decision making

- Deductive, inductive and abductive reasoning; mental models (Johnson-Laird)
- Heuristics and biases (Kahneman & Tversky); bounded rationality (Simon); ecological rationality (Gigerenzer)
- **Dual-process theories** — see [Psychology & AI](../psychology/index.md)
- **Analogy** as the core of cognition (Hofstadter; Gentner's structure mapping)
- **Causal reasoning** in children and adults (Gopnik; Sloman)

## Predictive processing and the free-energy principle

**Predictive coding** (Rao & Ballard, 1999): each cortical level predicts the activity of the level below; only **prediction errors** propagate upward. Learning minimises prediction error.

**Free-energy principle** (Friston): self-organising systems minimise variational free energy, an upper bound on surprise. Under this view:

- **Perception** updates beliefs to explain sensory input (variational inference)
- **Action** changes the world to make input match predictions (**active inference**)
- **Attention** is precision-weighting of prediction errors

Connections to AI: variational autoencoders optimise the same free-energy (ELBO) objective; self-supervised predictive learning resembles predictive coding; active inference is an alternative to reward-maximising RL. Critics argue the free-energy principle is so general it is hard to falsify; supporters see it as a unifying framework.

## Development

- **Piaget's stages** — influential though revised
- **Core knowledge** (Spelke): infants have early systems for objects, agents, number, space
- **Child as scientist** (Gopnik): children learn by experimenting, like Bayesian learners
- **Social learning** and joint attention (Tomasello)
- AI lessons: curriculum, intrinsic motivation, the role of embodiment and social interaction; "Can we build a machine that learns like a child?" (Turing already suggested it in 1950)

## Building machines that think like people

Lake, Ullman, Tenenbaum & Gershman (2017), "Building machines that learn and think like people", argued AI should incorporate:

1. **Intuitive physics and intuitive psychology** ("start-up software")
2. **Compositionality**
3. **Learning-to-learn**
4. **Causal models** rather than pattern recognition alone

These remain an influential checklist for evaluating modern models.

## Key methods

### Heuristics and biases (Tversky & Kahneman, 1974)

- **Problem:** how do people judge probabilities and frequencies when they cannot compute the exact answer?
- **Core idea:** judgement under uncertainty relies on a few heuristics, namely representativeness, availability, and anchoring and adjustment. Each is often useful, and each leads to systematic errors.
- **Method:** illustrative problems and experiments, in which participants' judgements are compared with the answers that probability theory gives.
- **Results:** judgements deviate in predictable directions from the normative answers. Examples include ignoring base rates when a description seems typical of a category, and estimates that are pulled toward an arbitrary starting value.
- **Limitations:** the heuristics are described in words rather than as a formal model, so the paper does not say exactly when each one applies. Later work has argued that many heuristics are adaptive, not merely biased.

### Building machines that learn and think like people (Lake et al., 2017)

- **Problem:** why do deep networks need far more data than people do, and how do they differ from people in what they learn and how?
- **Core idea:** three ingredients are proposed: causal models of the world, learning grounded in intuitive theories of physics and psychology, and compositionality with learning-to-learn for fast generalisation to new tasks.
- **Method:** a target article with open commentaries, which argues for the three ingredients. Its evidence is a review of existing models and experiments, with a model that learns handwritten characters from a single example as a worked case.
- **Results:** the article is a position paper and does not report a new benchmark result.
- **Limitations:** the commentaries disagree about how much built-in structure machines need. Progress in large models since 2017 has changed how much of the argument still applies.

## Resources

- Bermúdez, *Cognitive Science: An Introduction to the Science of the Mind*
- Thagard, *Mind: Introduction to Cognitive Science*
- [Stanford Encyclopedia of Philosophy: Cognitive Science](https://plato.stanford.edu/entries/cognitive-science/)
- Clark, *Surfing Uncertainty* (predictive processing)
- Griffiths, Chater & Tenenbaum, *Bayesian Models of Cognition*
- MIT 9.66 *Computational Cognitive Science* (OCW)

## References

### Seminal papers

- Miller, G. A. (1956). The magical number seven, plus or minus two: Some limits on our capacity for processing information. *Psychological Review*. https://doi.org/10.1037/h0043158 — The classic account of working-memory capacity and how chunking expands it.
- Anderson, J. R., et al. (2004). An Integrated Theory of the Mind. *Psychological Review*. https://doi.org/10.1037/0033-295X.111.4.1036 — ACT-R, a cognitive architecture that models memory, goals and learning within one system.
- Lake, B. M., et al. (2017). Building machines that learn and think like people. *Behavioral and Brain Sciences*. https://doi.org/10.1017/S0140525X16001837 — Target article arguing that human-like learning needs intuitive physics, intuitive psychology and compositional models, with commentaries.
- Clark, A. (2013). Whatever next? Predictive brains, situated agents, and the future of cognitive science. *Behavioral and Brain Sciences*. https://doi.org/10.1017/S0140525X12000477 — A review of predictive processing as a unifying framework for perception, action and cognition.
- Tversky, A. & Kahneman, D. (1974). Judgment under Uncertainty: Heuristics and Biases. *Science*. https://doi.org/10.1126/science.185.4157.1124 — Documents heuristics such as availability and representativeness that shape human judgement under uncertainty.
