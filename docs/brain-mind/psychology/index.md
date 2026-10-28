---
related:
- applications/mental-health
- applications/social-science
- applications/education
- engineering/evaluation
aliases:
  - 心理學
  - 心理學與 AI
  - Psychology
---

# Psychology & AI

Psychology and AI influence each other in at least four ways: psychology **inspires** AI designs, provides **methods to evaluate** AI, uses AI as a **research tool**, and studies **how humans interact** with AI.

## Key methods

### Videotaped problem-solving test (Premack & Woodruff 1978)

- **Problem:** Can an animal infer another agent's goal from its behaviour, the core of theory of mind, or does it only respond to the visible action?
- **Core idea:** Show a chimpanzee short videos of a human actor struggling with problems, then ask it to choose between photographs of possible solutions. If it reliably picks the photograph that solves the actor's problem, the authors argue it understood the actor's goal and not only the action.
- **Equation or algorithm:**
  1. Show an adult chimpanzee a series of videotaped scenes of a human actor struggling with a problem.
  2. Present photographs of possible solutions, one of which solves the problem shown.
  3. Record which photograph the chimpanzee chooses on each trial.
  4. Infer goal attribution from consistent choice of the correct photograph.
- **Results:** The abstract reports the chimpanzee's consistent choice of the correct photographs. It gives no trial counts or statistics, so the numbers should be checked in the full paper.
- **Limitations:** The study rests on one adult chimpanzee. Whether the choices reflect attribution of goals rather than simpler explanations is still debated; the theory of mind section above covers the wider question.

### False-belief tests on language models (Kosinski 2023)

- **Problem:** Do large language models solve false-belief tasks, the standard test of theory of mind in children, and how does performance depend on model size?
- **Core idea:** Write scenarios in which a character's belief about an object or location differs from the facts, then ask what the character will think or do. Each task is written in eight scenario variants with 16 prompts in total, and a task counts as solved only if the model answers all 16 correctly.
- **Equation or algorithm:**
  1. Write a false-belief scenario: a protagonist holds a belief that the world has since contradicted.
  2. Ask a question that can only be answered correctly by tracking the protagonist's belief.
  3. Repeat across the eight variants, giving 16 prompts per task.
  4. Score each model, count a task as solved only when all 16 answers are correct, and compare models of different sizes and generations.
- **Results:** Eleven models were tested. The smaller and older models solved none of the tasks. GPT-3-davinci-003 and ChatGPT-3.5-turbo each solved about 20%, and ChatGPT-4 solved 75%, a level the author compares with six-year-old children in earlier studies.
- **Limitations:** Passing the test does not show that a model has mental states; the author treats the spontaneous emergence of theory of mind as a possibility the results suggest, not a finding. Later work has questioned how robust such results are to changes in wording (see the theory of mind section above).

## Dual-process theory

Kahneman's popularisation (*Thinking, Fast and Slow*, 2011) of a long research tradition (Evans, Stanovich, Sloman):

| | System 1 | System 2 |
|---|---|---|
| Speed | Fast | Slow |
| Effort | Automatic | Effortful |
| Capacity | Parallel, high | Serial, limited by working memory |
| Errors | Heuristic biases | Fewer, but costly |
| AI analogy | A single forward pass; pattern recognition | Chain-of-thought, search, tool use, "thinking" modes |

Reasoning models that "think longer" before answering are often described as adding System 2. The analogy is loose but productive; Bengio's 2019 "From System 1 deep learning to System 2 deep learning" talk popularised it in ML.

## Cognitive biases — in humans and in LLMs

| Bias | Human finding | LLM findings |
|---|---|---|
| Framing | Choices flip between gain and loss frames (Tversky & Kahneman, 1981) | Many LLMs show framing effects, sometimes stronger than humans |
| Anchoring | Arbitrary numbers bias estimates | LLM estimates shift with anchors in the prompt |
| Belief bias / content effects | Logic judged by believability of conclusions | LLMs show human-like content effects on reasoning (Dasgupta, Lampinen et al., 2022) |
| Order and recency effects | Primacy and recency in memory | Position bias ("lost in the middle") in long contexts |
| Conformity / social desirability | Agreeing with the group or authority | Sycophancy toward user opinions |
| Overconfidence | Calibration errors | Verbalised confidence often poorly calibrated |

Binz & Schulz (2023, *PNAS*) used classic cognitive-psychology tasks to study GPT-3 — the start of "**machine psychology**" (Hagendorff, 2023): treating models as participants in psychology experiments.

## Theory of mind

Theory of mind (ToM) is the capacity to attribute beliefs, desires and intentions to others.

- Human development: false-belief understanding emerges around age 4 in explicit tasks (Wimmer & Perner, 1983; Sally–Anne test)
- LLMs: large models pass many textbook false-belief tasks (Kosinski, 2023), but small perturbations can break performance (Ullman, 2023); broad batteries show mixed, model-dependent results (Strachan et al., 2024, *Nature Human Behaviour*)
- Debate: genuine mental-state reasoning or pattern matching on narrative regularities? Behavioural tests alone may not settle it

## Personality, emotion and motivation

- Personality questionnaires (Big Five) can be administered to LLMs; scores depend strongly on prompts, raising validity questions for "AI personality"
- **Affective computing** (Picard, 1997): recognising and simulating emotion; facial-expression-based emotion recognition is scientifically contested (Barrett et al., 2019) and restricted under the EU AI Act in workplaces and schools
- **Intrinsic motivation** and curiosity inspire RL exploration bonuses

## LLMs as models of human cognition

- **Simulating participants**: LLMs reproduce many classic experimental effects ("silicon samples", Argyle et al., 2023), but with reduced variance and biases toward WEIRD populations — useful for piloting, not replacing, human studies
- **Foundation models of cognition**: Centaur (Binz et al., 2025, *Nature*) fine-tuned an LLM on 10+ million choices from 160 psychology experiments (Psych-101) to predict human behaviour across many tasks; its claims as a "unified model of cognition" are debated
- **Language and thought**: LLMs as test cases for theories of language acquisition and the relation between language and reasoning

## AI as a tool for psychological science

- Automated coding of open-ended responses, speech and video
- Large-scale text analysis of social media for well-being and mental-health indicators
- Adaptive testing and item generation
- Computational modelling and model fitting
- Experiment design and literature synthesis assistance
- See [Mental Health](../../applications/mental-health/index.md) and [Social Sciences](../../applications/social-science/index.md)

## Human factors: how people interact with AI

| Phenomenon | Description |
|---|---|
| Automation bias | Over-relying on automated advice, even when wrong |
| Algorithm aversion | Rejecting algorithms after seeing them err (Dietvorst et al., 2015) |
| Anthropomorphism / ELIZA effect | Attributing understanding and feelings to chatbots |
| Calibrated trust | Trust should match actual reliability; explanations do not always help |
| Cognitive offloading | Relying on AI can reduce effortful processing and learning |
| Parasocial relationships | Emotional bonds with companion chatbots, with benefits and risks |
| Persuasion | LLM messages can be as persuasive as human ones on some topics |

## Resources

- Kahneman, *Thinking, Fast and Slow*
- Binz & Schulz (2023), "Using cognitive psychology to understand GPT-3", *PNAS*
- Hagendorff (2023), "Machine Psychology"
- Frank (2023), "Baby steps in evaluating the capacities of large language models", *Nature Reviews Psychology*
- Shiffrin & Mitchell (2023), "Probing the psychology of AI models", *PNAS*

## References

### Seminal papers

- Tversky, A. & Kahneman, D. (1974). Judgment under Uncertainty: Heuristics and Biases. *Science*. https://doi.org/10.1126/science.185.4157.1124 — Documents heuristics such as availability and representativeness that shape human judgement under uncertainty.
- Miller, G. A. (1956). The magical number seven, plus or minus two: Some limits on our capacity for processing information. *Psychological Review*. https://doi.org/10.1037/h0043158 — The classic account of working-memory capacity and how chunking expands it.
- Anderson, J. R., et al. (2004). An Integrated Theory of the Mind. *Psychological Review*. https://doi.org/10.1037/0033-295X.111.4.1036 — ACT-R, a cognitive architecture that models memory, goals and learning within one system.
- Lake, B. M., et al. (2017). Building machines that learn and think like people. *Behavioral and Brain Sciences*. https://doi.org/10.1017/S0140525X16001837 — Target article arguing that human-like learning needs intuitive physics, intuitive psychology and compositional models, with commentaries.
- Clark, A. (2013). Whatever next? Predictive brains, situated agents, and the future of cognitive science. *Behavioral and Brain Sciences*. https://doi.org/10.1017/S0140525X12000477 — A review of predictive processing as a unifying framework for perception, action and cognition.
- Premack, D. & Woodruff, G. (1978). Does the chimpanzee have a theory of mind? *Behavioral and Brain Sciences*. https://doi.org/10.1017/S0140525X00076512 — Introduces the term "theory of mind" and a videotape test of whether a chimpanzee attributes goals to a human actor.
- Kosinski, M. (2023). Evaluating Large Language Models in Theory of Mind Tasks. arXiv. https://arxiv.org/abs/2302.02083 — Tests eleven language models on false-belief tasks; ChatGPT-4 solves about 75% of them.
