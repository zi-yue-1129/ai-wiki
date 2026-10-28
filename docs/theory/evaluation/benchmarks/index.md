---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - overview
---

# Benchmarks

A benchmark is a fixed set of tasks, data and a metric that a community agrees to use for comparison. This section gives each named benchmark its own page, grouped by task family, so that the question each one answers is clear and its score can be read together with its protocol.

## Families

| Family | Benchmarks | Task |
|---|---|---|
| [Vision](vision/index.md) | [ImageNet](vision/imagenet.md), [COCO](vision/coco.md) | Classification, detection and instance segmentation |
| [Language](language/index.md) | [GLUE](language/glue.md), [SuperGLUE](language/superglue.md), [MMLU](language/mmlu.md), [GPQA](language/gpqa.md), [Humanity's Last Exam](language/hle.md) | Understanding, knowledge and expert reasoning |
| [Math and code](math-and-code/index.md) | [GSM8K](math-and-code/gsm8k.md), [MATH](math-and-code/math.md), [SWE-bench](math-and-code/swe-bench.md) | Mathematical and software reasoning |
| [Multimodal](multimodal/index.md) | [VQA v2](multimodal/vqa-v2.md), [MMMU](multimodal/mmmu.md) | Combining images with knowledge and reasoning |
| [Reasoning and agents](reasoning-agents/index.md) | [ARC-AGI](reasoning-agents/arc-agi.md), [GAIA](reasoning-agents/gaia.md), [WebArena](reasoning-agents/webarena.md) | Rule acquisition, real-world questions and web tasks |
| [Speech](speech/index.md) | [LibriSpeech](speech/librispeech.md) | Transcribing spoken English |
| [Reinforcement](reinforcement/index.md) | [Arcade Learning Environment](reinforcement/ale.md), [MuJoCo](reinforcement/mujoco.md) | Return from playing games and controlling simulated bodies |
| [Science](science/index.md) | [MoleculeNet](science/moleculenet.md) | Predicting molecular properties |
| [Neuroscience](neuroscience/index.md) | [Brain-Score](neuroscience/brain-score.md) | Matching neural and behavioural responses |
| [Few-shot](few-shot/index.md) | [miniImageNet](few-shot/mini-imagenet.md) | Recognising new classes from few labelled examples |

## Reading a score

A benchmark score is only interpretable with three things attached: the metric, the protocol and the test-set history. The metric is described in [metrics](../metrics/index.md). The protocol, covering splits, contamination and reporting uncertainty, is in [protocols](../protocols/index.md). The date of the test set relative to the training data matters for any model trained on web text.

## What benchmarks can and cannot show

A benchmark gives a comparable number under fixed conditions. A high score shows that a system handles that test, not that it is useful in every setting (Raji et al., 2021). Holistic evaluations argue for reporting many scenarios and metrics, so that trade-offs are visible (Liang et al., 2022). Scores also saturate, and a test set can drift away from the population it was meant to sample (Recht et al., 2019).

## Open questions

Benchmarks saturate quickly, and the same test is often used both to select a model and to report its result. Open-ended and multi-step tasks need evaluation methods that the classic families do not provide.

## Related

- [Evaluation overview](../index.md) places benchmarks among metrics and protocols.
- [Evaluation & Benchmarks](../../../engineering/evaluation/index.md) gives practical guidance for language models.
- [Datasets](../../../reference/datasets/index.md) lists named datasets for lookup.

## References

### Seminal papers

- Raji, I. D. & Bender, E. M. et al. (2021). *AI and the Everything in the Whole Wide World Benchmark*. arXiv. https://arxiv.org/abs/2111.15366 — Examines construct validity and the limits of broad claims based on benchmark performance.
- Liang, P. & Bommasani, R. et al. (2022). *Holistic Evaluation of Language Models*. arXiv. https://arxiv.org/abs/2211.09110 — Evaluates language models across scenarios and metrics to expose trade-offs.
- Chollet, F. (2019). *On the Measure of Intelligence*. arXiv. https://arxiv.org/abs/1911.01547 — Argues that skill on a fixed task is a weak measure of intelligence.

### Articles and documentation

- Hendrycks, D. et al. (2021). *Measuring Massive Multitask Language Understanding*. ICLR. https://arxiv.org/abs/2009.03300 — A widely used benchmark whose saturation shows how quickly scores can change meaning.
- Srivastava, A. et al. (2022). *Beyond the Imitation Game: Quantifying and extrapolating the capabilities of language models*. arXiv. https://arxiv.org/abs/2206.04615 — Describes a large benchmark collection and how its tasks were chosen.
