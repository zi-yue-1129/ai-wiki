---
status: draft
last_reviewed: 2026-10-28
related:
- applications/mental-health
- applications/healthcare
tags:
- psychology
- machine learning
aliases:
  - Chekroud et al. 2016
  - 跨試驗預測
  - 憂鬱症治療預測
  - Cross-trial prediction
  - Treatment outcome prediction
---

# Chekroud et al. 2016 (Cross-Trial Prediction of Treatment Outcome)

Chekroud et al. (2016) trained a machine learning model on baseline information from people with depression, and tested whether it could predict treatment outcome in a separate trial. It is a method for prediction rather than an account of mechanism. This page is part of [Computational Psychiatry](../index.md). The parent page gives the overview; this page covers the method, its steps and the limits of the evidence.

## Overview

Choosing an antidepressant is often a process of trial and error, and many patients do not respond to the first treatment they try. A model that predicts which treatment is likely to work would be useful, but such a model has to be tested carefully. A model that predicts well on the data it was built from may have learned the quirks of that sample.

Chekroud and colleagues used a stricter test. The model was trained on one trial and evaluated on another, so it had to transfer to a different set of patients and a different study setting. The wider clinical landscape in which such models are used is described in [Mental Health](../../../applications/mental-health/index.md).

## Key concepts

- **Baseline features**: information recorded before treatment starts, such as demographic details, clinical history and symptom ratings.
- **Outcome**: the result to be predicted, here a binary measure of whether a patient reaches remission.
- **Classifier**: a model that maps baseline features to a predicted outcome.
- **Cross-validation**: testing a model on held-out parts of one dataset. It is useful, but it does not test transfer to new settings.
- **Cross-trial validation**: training on one trial and testing on another. It tests whether predictions carry over between studies.
- **Accuracy**: the proportion of patients whose outcome is predicted correctly, $\text{accuracy} = \frac{TP + TN}{N}$, to be compared with a chance baseline.

## How it works

The method follows four steps.

1. Baseline data are assembled for each patient before treatment, including demographic, clinical and symptom measures.
2. A classifier is trained on one trial to predict the outcome from these baseline features.
3. The trained model is applied, without refitting, to data from a separate trial. This step is the cross-trial test, and it can involve different patients, sites or treatments.
4. Predictions are compared with the recorded outcomes and with a chance baseline, and the accuracy and related measures are reported.

The key step is the third. A model that works only inside the trial it was built on has not shown that it can be used elsewhere.

## Results

The paper tests prediction across trials, and its central claim is that predictive value carried over to the separate trial. The page does not quote accuracy figures or sample sizes. These are in the paper and should be read there. Readers should check the paper for its own view on clinical use.

## Limitations

- Predictive accuracy from baseline features is modest in many studies of this kind, so individual predictions carry substantial uncertainty.
- Baseline clinical features are often proxies for underlying causes. A classifier can predict outcome without explaining why patients respond.
- Trials differ in populations, measures and sites, and these differences limit how far a model transfers.
- A prediction model is not a treatment recommendation. Its use in decisions needs clinical judgement and evaluation.

## Open questions

- Does adding computational measures, such as those in [Gillan et al. 2016](../gillan-2016/index.md), improve prediction beyond clinical features?
- Do models trained in one health system transfer to others, and to other conditions?
- How should probabilistic predictions be communicated to patients and clinicians, so that they inform rather than determine decisions?

## References

### Seminal papers

- Chekroud, A. M. et al. (2016). Cross-trial prediction of treatment outcome in depression: a machine learning approach. *The Lancet Psychiatry*. https://doi.org/10.1016/S2215-0366(15)00471-X — Trains a machine learning model on baseline data and tests whether it predicts depression treatment outcome in a separate trial.

### Surveys and textbooks

- Dwyer, D. B., Falkai, P. & Koutsouleris, N. (2018). Machine Learning Approaches for Clinical Psychology and Psychiatry. *Annual Review of Clinical Psychology*. https://doi.org/10.1146/annurev-clinpsy-032816-045037 — Review of machine learning methods for diagnosis, prognosis and treatment, with the limits that apply to clinical translation.
- Huys, Q. J. M., Maia, T. V. & Frank, M. J. (2016). Computational psychiatry as a bridge from neuroscience to clinical applications. *Nature Neuroscience*. https://doi.org/10.1038/nn.4238 — Review of how computational models can connect neuroscience with clinical practice in psychiatry.
- Adams, R. A., Huys, Q. J. M. & Roiser, J. P. (2015). Computational Psychiatry: towards a mathematically informed understanding of mental illness. *Journal of Neurology, Neurosurgery & Psychiatry*. https://doi.org/10.1136/jnnp-2015-310737 — Review of how formal models can inform the understanding of mental illness.

### Articles and documentation

- Bzdok, D. & Meyer-Lindenberg, A. (2018). Machine Learning for Precision Psychiatry: Opportunities and Challenges. *Biological Psychiatry: Cognitive Neuroscience and Neuroimaging*. https://doi.org/10.1016/j.bpsc.2017.11.007 — Discusses how machine learning could support precision psychiatry, and the validation problems it faces.
