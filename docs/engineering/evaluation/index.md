---
related:
- foundations/machine-learning
- brain-mind/psychology
- society/safety-alignment
- applications/software
---

# Evaluation & Benchmarks

"You can't improve what you don't measure" — and with AI, it's easy to measure the wrong thing.

## Major benchmarks (as reference points)

| Area | Benchmarks | Status |
|---|---|---|
| General knowledge | MMLU, MMLU-Pro | MMLU saturated |
| Hard expert questions | GPQA Diamond, Humanity's Last Exam | Rapid progress |
| Math | GSM8K (saturated), MATH, AIME, FrontierMath | Reasoning models made large gains |
| Code | HumanEval (saturated), SWE-bench Verified, LiveCodeBench | See [Software Development](../../applications/software/index.md) |
| Reasoning / abstraction | ARC-AGI-1/2 | Designed to resist memorisation |
| Agents | GAIA, WebArena, OSWorld, τ-bench, Terminal-Bench | Long-horizon autonomy |
| Long context | Needle-in-a-haystack, RULER, LongBench | Retrieval ≠ reasoning over long inputs |
| Multimodal | MMMU, MathVista, Video-MME | |
| Chinese / Traditional Chinese | C-Eval, CMMLU, TMMLU+ | |
| Human preference | LMArena (Chatbot Arena) Elo ratings | Style can influence votes |
| Safety | HarmBench, StrongREJECT, WMDP, dangerous-capability evals | See [Safety & Alignment](../../society/safety-alignment/index.md) |

## Pitfalls

- **Contamination**: test items leak into training data — use held-out, dynamic or private sets
- **Saturation**: benchmarks stop discriminating once models near the ceiling
- **Goodhart's law**: optimising for a benchmark erodes its meaning
- **Prompt sensitivity**: small format changes swing scores; report settings
- **Statistical noise**: report confidence intervals; small test sets mislead
- **Construct validity**: does the benchmark measure what it claims? (Raji et al., 2021, "AI and the Everything in the Whole Wide World Benchmark")
- **Benchmarks ≠ real-world usefulness**

## Evaluating your own application

1. **Write down what good looks like** for real user tasks
2. **Build an eval set** from real or realistic inputs, including edge cases and adversarial ones (start with 50–200 examples)
3. **Choose graders**:
    - Exact match / unit tests / programmatic checks where possible
    - **LLM-as-judge** with a rubric — validate against human ratings; watch for position, verbosity and self-preference biases
    - Human review for high-stakes or subjective qualities
4. **Track regressions** on every change (prompt, model, retrieval settings)
5. **Monitor in production** with sampled reviews and user feedback

## Methods from psychology and measurement science

- **Item response theory** to estimate model ability and item difficulty
- **Reliability and validity** concepts from psychometrics
- **Controlled experiments** and counterbalancing (e.g. swapping answer order to detect position bias)
- **Cognitive-science-style probing** to test specific capacities (see [Psychology & AI](../../brain-mind/psychology/index.md))

## Tools

[lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness), [HELM](https://crfm.stanford.edu/helm/), [Inspect](https://inspect.aisi.org.uk/), [OpenAI Evals](https://github.com/openai/evals), promptfoo, Braintrust, LangSmith.

## Resources

- Liang et al. (2022), HELM
- Stanford AI Index (annual), benchmark trend chapters
- Epoch AI benchmarking hub
- Chang et al. (2024), "A Survey on Evaluation of Large Language Models"
