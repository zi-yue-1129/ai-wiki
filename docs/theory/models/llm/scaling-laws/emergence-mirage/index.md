---
status: draft
last_reviewed: 2026-10-28
aliases:
  - 海市蜃樓
  - 湧現是測量假象
  - Emergence as a mirage
  - Mirage
---

# Emergence as a mirage (Schaeffer et al., 2023)

Schaeffer, Miranda and Koyejo argued that the sudden appearance of emergent abilities is often a product of the metric a researcher chooses, not of a sudden change in the model. With continuous metrics, the same outputs show smooth, predictable improvement. The general topic is covered in the parent page, [Scaling laws and emergent abilities](../index.md).

## Overview

Wei et al. (2022) reported that some abilities of language models appear abruptly at larger scales. Schaeffer et al. (2023) examined the same claims and asked a narrower question: given the outputs a model actually produces, does the apparent jump survive a change in how those outputs are scored? Their answer was that, for many tasks, it does not. Apparent emergence depends on whether the score is discontinuous, such as exact-match accuracy, or continuous, such as a graded measure of how close the answer is.


## Key concepts

- **Discontinuous metric**: a score that counts an answer as right or wrong, with nothing in between. Exact-match accuracy is an example.
- **Continuous metric**: a score that changes smoothly with how close an output is to the target, such as the log-probability assigned to the correct answer or an edit distance from it.
- **Apparent emergence**: a rise in a discontinuous score that looks sudden even though the underlying behaviour changes gradually.

## How it works

The paper proposes a simple mathematical argument and then tests it in three ways. The argument is that, for a given task and model family, the appearance of emergence depends on the scoring function applied to the same outputs.

To see the mechanism, consider a task whose answer has $L$ tokens, and suppose each token is correct with probability $p$. Exact-match accuracy is then roughly $p^L$. This is a convex function of $p$, so a steady rise in $p$ produces a score that stays low and then climbs quickly. A continuous score, such as the average per-token log-likelihood of the correct answer, rises smoothly with the same $p$. This calculation is an illustration of the mechanism in our own words, not a quotation of the paper.

The three tests reported in the paper are:

1. Predictions about the effect of metric choice, checked on the InstructGPT and GPT-3 model family for tasks where emergence had been claimed.
2. Predictions about metric choices in a meta-analysis of emergent abilities on BIG-bench.
3. A demonstration that metric choice can produce apparent emergence in several vision tasks across deep networks, where emergence was not previously claimed.

## Results

The abstract summarises the findings. Under discontinuous metrics, the claimed abilities appear sharp, and under linear or continuous metrics they appear as smooth, predictable improvements. The authors conclude that alleged emergent abilities evaporate under different metrics or better statistics, and that they may not be a fundamental property of scaling AI models.

## Limitations

- **Scope of the analysis.** The paper works on outputs that already exist, so it cannot show what a model at an untested scale would produce.
- **Not every case.** The argument shows that the jump can be produced by the metric. It does not show that every claimed emergent ability is a metric artefact, and the paper's wording is hedged for that reason.
- **Relevance to capability.** Even a smooth curve can be practically important when the crossing point of a useful threshold matters, for example when a user needs an answer that is fully correct.

## Open questions

- Which abilities are sharp under any reasonable metric? Such cases would be stronger evidence for genuine emergence than the cases the paper re-scored.
- How should forecasters report capability when users care about all-or-nothing success, such as solving a whole problem correctly, and a continuous score understates the risk?
- Do the vision results and the language results share a mechanism, or are they different phenomena that look alike under discontinuous scoring?

## Connections

- Parent topic: [Scaling laws and emergent abilities](../index.md). The claim it challenges is on [Emergent abilities](../emergent-abilities/index.md).
- The model family used in the analysis is described in [InstructGPT and RLHF](../../instructgpt-rlhf/index.md) and [GPT-3 Few-Shot Learning](../../gpt-3-few-shot/index.md).
- Choice of metric is a general issue in [Evaluation](../../../../../engineering/evaluation/index.md), not only for emergence.
- Brain and mind: psychophysics has long studied how the response measure can make a gradual change in perception look like a threshold. This is an analogy the paper does not draw. See [Psychology](../../../../../brain-mind/psychology/index.md).

## References

### Seminal papers

- Schaeffer, R., Miranda, B. & Koyejo, S. (2023). *Are Emergent Abilities of Large Language Models a Mirage?* arXiv. https://arxiv.org/abs/2304.15004 — The paper itself: argues that metric choice produces apparent emergence and tests this on language and vision tasks.
- Wei, J., et al. (2022). *Emergent Abilities of Large Language Models*. arXiv. https://arxiv.org/abs/2206.07682 — The claim this paper examines: abilities that appear abruptly at scale and cannot be extrapolated from smaller models.
- Ouyang, L., et al. (2022). *Training language models to follow instructions with human feedback*. arXiv. https://arxiv.org/abs/2203.02155 — The InstructGPT models, one of the families whose tasks the paper re-scores.
- Srivastava, A., et al. (2022). *Beyond the Imitation Game: Quantifying and extrapolating the capabilities of language models*. arXiv. https://arxiv.org/abs/2206.04615 — The BIG-bench tasks used for the meta-analysis of emergent abilities.
- Kaplan, J., et al. (2020). *Scaling Laws for Neural Language Models*. arXiv. https://arxiv.org/abs/2001.08361 — The smooth power-law trends in loss against which the emergence claims are contrasted.

### Surveys and textbooks

- Berti, L., Giorgi, F. & Kasneci, G. (2025). *Emergent Abilities in Large Language Models: A Survey*. arXiv. https://arxiv.org/abs/2503.05788 — Reviews the emergence literature, including the metric-based critique and the case for genuine emergence.

### Articles and documentation

- Ganguli, D., et al. (2022). *Predictability and Surprise in Large Generative Models*. arXiv. https://arxiv.org/abs/2202.07785 — Discusses predictable loss combined with unpredictable specific capabilities in large generative models.
