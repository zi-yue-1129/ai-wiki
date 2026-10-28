---
related:
- brain-mind/psychology
- brain-mind/cognitive-architectures
- brain-mind/memory-learning
- theory/models/llm
aliases:
  - 教育
  - 教學
---

# Education

## Landscape

| Area | Examples |
|---|---|
| Intelligent tutoring systems (ITS) | Cognitive Tutor / MATHia (grew out of ACT-R), ASSISTments, AutoTutor |
| LLM tutors | Khanmigo, chatbot "study modes" that guide rather than give answers |
| Adaptive practice | Knowledge tracing, spaced repetition (Duolingo, Anki) |
| Assessment | Automated essay scoring, short-answer grading, feedback on code |
| Teacher support | Lesson planning, differentiated materials, grading assistance |
| Accessibility | Speech-to-text, text-to-speech, translation, simplification |
| Learning analytics | Early warning for dropout, engagement dashboards |

## Evidence

- **Human tutoring** is highly effective. Bloom's "2 sigma problem" (1984) set the goal of matching one-to-one tutoring with group instruction (Bloom, 1984)
- **Intelligent tutoring systems** produce moderate learning gains on average (VanLehn, 2011; Kulik & Fletcher, 2016)
- **LLM tutors**: a randomised trial in a physics course found an AI tutor designed with pedagogical best practices produced larger learning gains than active-learning classes (Kestin et al., 2025)
- **Unstructured LLM use can hurt**: high-school students with unrestricted GPT-4 access did better on practice but worse on exams once access was removed, while a tutor-style version mitigated the harm (Bastani et al., 2025, *PNAS*)

## Methods

- **Knowledge tracing**: Bayesian knowledge tracing (an HMM over mastery), deep knowledge tracing (RNNs/Transformers)
- **Item response theory** for adaptive testing
- **Spaced repetition** schedulers model forgetting curves (FSRS, SuperMemo) — see [Memory & Learning](../../brain-mind/memory-learning/index.md)
- **Pedagogical prompting and fine-tuning**: Socratic questioning, withholding answers, checking understanding (e.g. LearnLM)

## Learning science lessons for AI tools

| Principle | Implication |
|---|---|
| Retrieval practice, spacing, interleaving | Quiz and space, don't just explain |
| Desirable difficulties | Productive struggle beats instant answers |
| Cognitive load theory | Chunk information, worked examples for novices |
| Metacognition | Prompt learners to explain and self-assess |
| Feedback timing and specificity | Immediate, targeted feedback on errors |
| Motivation and belonging | Human relationships remain central |

## Risks

- **Academic integrity**: AI-text detectors are unreliable and biased against non-native writers (Liang et al., 2023); redesign assessments instead
- **Cognitive offloading** and de-skilling
- **Hallucinated content** in explanations
- **Privacy** of children's data (FERPA, COPPA, GDPR)
- **Equity**: unequal access to devices, connectivity and premium tools
- **Bias** in automated scoring

## Key methods

Two methods are most relevant here. Each links to the page that explains it.

- [Transformer](../../theory/models/transformer/attention-is-all-you-need/index.md): sequence models used for deep knowledge tracing, which predict a learner's next answer from their history (Vaswani et al., 2017).
- [InstructGPT and RLHF](../../theory/models/llm/instructgpt-rlhf/index.md): the training recipe behind LLM tutors, which can be tuned to guide rather than give answers (Ouyang et al., 2022).

## References

### Seminal papers

- Bloom (1984). The 2 Sigma Problem: The Search for Methods of Group Instruction as Effective as One-to-One Tutoring. *Educational Researcher*. https://doi.org/10.3102/0013189X013006004 — Sets the benchmark that one-to-one tutoring outperforms group instruction.
- Kestin et al. (2025). AI tutoring outperforms in-class active learning: an RCT introducing a novel research-based design in an authentic educational setting. *Scientific Reports*. https://doi.org/10.1038/s41598-025-97652-6 — Randomised trial of an AI tutor against in-class active learning in a physics course.
- Bastani et al. (2025). Generative AI without guardrails can harm learning: Evidence from high school mathematics. *PNAS*. https://doi.org/10.1073/pnas.2422633122 — Unrestricted GPT-4 access hurt exam scores, and a tutor-style version reduced the harm.
- Liang et al. (2023). GPT detectors are biased against non-native English writers. *Patterns*. https://doi.org/10.1016/j.patter.2023.100779 — Shows AI-text detectors flag non-native English writing as machine-generated.
- Vaswani, A. et al. (2017). *Attention Is All You Need*. NeurIPS. https://arxiv.org/abs/1706.03762 — Introduces the Transformer, built on multi-head self-attention.
- Ouyang, L. et al. (2022). Training language models to follow instructions with human feedback. NeurIPS. https://arxiv.org/abs/2203.02155 — InstructGPT, instruction tuning from human preference feedback.

### Surveys and textbooks

- VanLehn (2011). The Relative Effectiveness of Human Tutoring, Intelligent Tutoring Systems, and Other Tutoring Systems. *Educational Psychologist*. https://doi.org/10.1080/00461520.2011.611369 — Compares human tutoring, intelligent tutoring systems and other tutoring systems.
- Kulik & Fletcher (2016). Effectiveness of Intelligent Tutoring Systems. *Review of Educational Research*. https://doi.org/10.3102/0034654315581420 — Meta-analysis of the learning gains from intelligent tutoring systems.
