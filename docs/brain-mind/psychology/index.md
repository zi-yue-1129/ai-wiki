---
related:
- applications/mental-health
- applications/social-science
- applications/education
- engineering/evaluation
---

# Psychology & AI

Psychology and AI influence each other in at least four ways: psychology **inspires** AI designs, provides **methods to evaluate** AI, uses AI as a **research tool**, and studies **how humans interact** with AI.

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
