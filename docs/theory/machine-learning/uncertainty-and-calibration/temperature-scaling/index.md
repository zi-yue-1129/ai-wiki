---
status: draft
last_reviewed: 2026-10-28
related:
  - engineering/evaluation
tags:
  - calibration
  - uncertainty
  - evaluation
aliases:
  - 溫度縮放
  - 溫度校準
  - Temperature Scaling
---

# Temperature Scaling

Temperature scaling is a post-hoc method that makes the confidence of a trained classifier match its accuracy. It divides the network's logits by a single learned number, the temperature. Guo et al. (2017) proposed it as part of the [uncertainty and calibration](../index.md) topic.

## Overview

Guo et al. (2017) reported that modern networks are poorly calibrated, and they tested several post-processing fixes on image and document classification. Their abstract describes temperature scaling as a single-parameter variant of Platt scaling, and reports that it is surprisingly effective at calibrating predictions on most datasets. It is also a simple recipe. Because the method changes only the scale of the scores, it does not change which class has the highest score, so the predicted label and the accuracy stay the same. Only the confidence changes.

## Key concepts

- **Logits.** The raw scores \(z\) a network produces before the softmax turns them into probabilities.
- **Temperature.** A positive scalar \(T\). A value above 1 flattens the distribution and lowers confidence. A value below 1 sharpens it.
- **Negative log-likelihood (NLL).** The loss used to choose \(T\). It is a proper scoring rule, so it rewards honest probabilities.
- **Held-out set.** Validation data that the network did not see during training, drawn from the same distribution as the data it will face.

## How it works

Let \(\sigma_{\text{SM}}\) be the softmax. The calibrated prediction for input \(x_i\) with logits \(z_i\) is \(\sigma_{\text{SM}}(z_i / T)\). The single parameter is chosen by minimising the NLL on a validation set of \(n\) examples with labels \(y_i\):

\[
T^{*} = \arg\min_{T > 0} \; -\sum_{i=1}^{n} \log \sigma_{\text{SM}}\big(z_i / T\big)_{y_i}.
\]

The procedure is as follows.

1. Train the network as usual, then freeze it.
2. Compute the logits \(z_i\) for every example in a held-out validation set, which must not overlap with the training data.
3. Find \(T^{*}\) that minimises the NLL. Because this is a one-dimensional problem, a line search or a standard gradient method is enough.
4. At test time, divide each logit vector by \(T^{*}\) before the softmax. Dividing by one positive number preserves the order of the scores, so the predicted class is unchanged.

Calibration is then checked with a reliability diagram or ECE on a separate test set, before and after scaling.

## Results

The abstract of Guo et al. (2017) states that, on most of the image and document classification datasets used, temperature scaling is surprisingly effective at calibrating predictions, and that it offers a simple and straightforward recipe for practical settings. The same paper reports that depth, width, weight decay and batch normalisation are important factors influencing calibration. The exact figures are in the paper and were not re-run for this page.

## Limitations

- **One global number.** A single \(T\) cannot correct miscalibration that differs between classes or between inputs. Richer maps exist, but they need more validation data.
- **Same-distribution assumption.** The temperature is fitted on data that resembles the test data. Under dataset shift it may not transfer, and Ovadia et al. (2019) found that traditional post-hoc calibration falls short in exactly this setting.
- **Dependence on ECE.** The usual check, ECE, depends on how the bins are chosen, so a small change in the metric can reflect the binning rather than the model.
- **No new information.** Scaling does not make a model more accurate, and it does not help it recognise inputs it has never seen. Methods for those problems are on the [deep ensembles](../deep-ensembles/index.md) and [MC dropout](../mc-dropout/index.md) pages.

## Open questions

- When is a single temperature sufficient, and when are per-class or per-input corrections needed?
- How should calibration be maintained over time as the data drift, without a stream of new labels?
- How much of the calibration problem can be solved in training, through regularisation and normalisation choices, before any post-hoc step is applied?

## Connections

Temperature scaling is the post-hoc counterpart of the Bayesian approach. The [probabilistic methods](../../../paradigms/probabilistic/index.md) page describes the principled alternative, in which uncertainty comes from a distribution over the parameters. The idea that confidence should match reliability is also the one studied in human metacognition, as reviewed by Fleming and Lau (2014); see [cognitive science](../../../../brain-mind/cognitive-science/index.md). For the practical side of validation, see [evaluation](../../../../engineering/evaluation/index.md).

## References

### Seminal papers

- Guo, C., Pleiss, G., Sun, Y. & Weinberger, K. Q. (2017). *On Calibration of Modern Neural Networks*. ICML. https://arxiv.org/abs/1706.04599 — Introduces temperature scaling and shows that modern networks are poorly calibrated compared with older ones.
- Niculescu-Mizil, A. & Caruana, R. (2005). Predicting good probabilities with supervised learning. ICML. https://doi.org/10.1145/1102351.1102430 — Compares how different learners produce calibrated probabilities, and how post-hoc calibration changes them.
- Gneiting, T. & Raftery, A. E. (2007). Strictly proper scoring rules, prediction, and estimation. *Journal of the American Statistical Association*. https://doi.org/10.1198/016214506000001437 — Gives the theory of scoring rules, which justifies using NLL to fit the temperature.

### Surveys and textbooks

- Gawlikowski, J. et al. (2021). A survey of uncertainty in deep neural networks. arXiv. https://arxiv.org/abs/2107.03342 — Surveys the sources of uncertainty in deep networks and the post-hoc and training-time methods for estimating it.
- Hüllermeier, E. & Waegeman, W. (2021). Aleatoric and epistemic uncertainty in machine learning: an introduction to concepts and methods. *Machine Learning*. https://arxiv.org/abs/1910.09457 — Introduces the concepts that calibration and uncertainty estimation rely on.
- Fleming, S. M. & Lau, H. C. (2014). How to measure metacognition. *Frontiers in Human Neuroscience*. https://doi.org/10.3389/fnhum.2014.00443 — Reviews methods for measuring metacognition, meaning how well a person's confidence tracks their own accuracy.

### Articles and documentation

- Ovadia, Y. et al. (2019). Can you trust your model's uncertainty? Evaluating predictive uncertainty under dataset shift. NeurIPS. https://arxiv.org/abs/1906.02530 — Benchmarks post-hoc calibration under dataset shift, where it is shown to fall short.
