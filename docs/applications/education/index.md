---
related:
- brain-mind/psychology
- brain-mind/cognitive-architectures
- brain-mind/memory-learning
- theory/models/llm
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

- **Human tutoring** is highly effective — Bloom's "2 sigma problem" (1984) set the goal, though later meta-analyses find smaller but still large effects
- **Intelligent tutoring systems** produce moderate learning gains on average (VanLehn, 2011; Kulik & Fletcher, 2016)
- **LLM tutors**: a randomised trial in Nigeria found a GPT-4-based after-school tutoring programme produced substantial English-learning gains over six weeks (World Bank, 2024–2025); a Harvard physics course study found an AI tutor designed with pedagogical best practices outperformed active-learning classes on learning gains (Kestin et al., 2025, *Scientific Reports*)
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

## Resources

- UNESCO (2023), *Guidance for Generative AI in Education and Research*
- Holmes, Bialik & Fadel, *Artificial Intelligence in Education*
- Koedinger & Corbett, cognitive tutors research
- [EdArXiv](https://edarxiv.org/) for recent education research
