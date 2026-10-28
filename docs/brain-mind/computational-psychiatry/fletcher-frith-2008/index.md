---
status: draft
last_reviewed: 2026-10-28
related:
- applications/mental-health
- theory/paradigms/probabilistic
tags:
- neuroscience
- psychology
- bayesian
aliases:
  - Fletcher and Frith 2008
  - 貝氏解釋精神病
  - 陽性症狀
  - Positive symptoms
  - Bayesian account of psychosis
---

# Fletcher and Frith 2008 (Bayesian Account of Positive Symptoms)

Fletcher and Frith (2008) argued that the positive symptoms of schizophrenia, such as delusions and hallucinations, can be explained by a Bayesian account of perception in which prediction errors are weighted abnormally. This page is part of [Computational Psychiatry](../index.md). The parent page gives the overview; this page covers the account, its equation and the limits of the evidence.

## Overview

Positive symptoms are experiences or beliefs added to normal function. A delusion is a fixed belief that is held despite contrary evidence. A hallucination is a percept without an external source. Fletcher and Frith asked what kind of change in a normal perceptual system could produce these experiences. Their answer drew on the idea that perception combines expectations with sensory input, and that the brain signals when the two disagree.

The account builds on the [predictive-coding](../../predictive-coding/index.md) view of the cortex. If the prediction-error signal is abnormal, the balance between expectation and evidence changes. Beliefs that should be revised can then persist, and experiences can seem to come from outside when they do not. The same framework is also linked to the dopamine signal that reports reward prediction error, described in [Dopamine Reward Prediction Error](../../neuroscience/dopamine-reward-prediction-error/index.md).

## Key concepts

- **Prior**: the expectation a system holds before new evidence arrives. In this account, a prior can be a belief about the world or about oneself.
- **Likelihood**: how well the sensory evidence fits each hypothesis.
- **Prediction error**: the mismatch between what was predicted and what arrived. It is what drives belief revision.
- **Precision**: the weight given to a prediction error. High precision means the error has a large effect on belief; low precision means it is largely ignored.
- **Aberrant salience**: a related idea, from Kapur (2003), that psychotic experiences reflect a misplaced sense that events are significant.

## How it works

Bayes' rule describes how a belief about a hypothesis $h$ should change after evidence $e$:

$$p(h \mid e) \propto p(e \mid h)\, p(h).$$

In predictive-coding models, the belief is updated by the prediction error $\varepsilon = e - \hat{e}$, where $\hat{e}$ is the prediction, weighted by precision $\pi$. The update is roughly proportional to $\pi\,\varepsilon$.

The account can be stated in four steps.

1. The system generates a prediction from its current beliefs.
2. The prediction is compared with the incoming sensory input, and an error is computed.
3. The error is weighted by its precision and used to update the belief.
4. If the error is weighted abnormally, the belief is either revised too little, so that a prior persists against evidence, or the system's own predictions are treated as external input.

Fletcher and Frith apply step 4 to delusions and hallucinations. They argue that an overly strong prior, or an abnormal weighting of errors, can produce both kinds of experience.

## Results

The paper is a theoretical review, so it reports no single benchmark. It argues that behavioural and neuroimaging findings from people with psychosis, and from healthy people under manipulations, fit the account. This page describes that argument qualitatively and does not quote figures.

## Limitations

- The account is a framework rather than a fitted model, and it can accommodate many findings. This flexibility makes it harder to test.
- The mapping from prior and precision to specific symptoms is contested.
- The account is mainly about positive symptoms, and it does not cover negative symptoms and cognitive changes in the same detail.
- The link to dopamine is a hypothesis, and its evidence is mixed.

## Open questions

- Is the imbalance in priors, in precision, or in both? Different answers predict different experimental results.
- Do the same mechanisms explain delusions in people without psychosis?
- Which neuromodulators implement precision, and how do they relate to the dopamine signal?
- Is the abnormal prediction error a cause of symptoms or a consequence of them? Sterzer et al. (2018) update the account and review the evidence.

## References

### Seminal papers

- Fletcher, P. C. & Frith, C. D. (2008). Perceiving is believing: a Bayesian approach to explaining the positive symptoms of schizophrenia. *Nature Reviews Neuroscience*. https://doi.org/10.1038/nrn2536 — Argues that positive symptoms can be explained by abnormal weighting of prior beliefs and sensory prediction errors.
- Kapur, S. (2003). Psychosis as a state of aberrant salience: a framework linking biology, phenomenology, and pharmacology in schizophrenia. *American Journal of Psychiatry*. https://doi.org/10.1176/appi.ajp.160.1.13 — An influential framework that explains psychotic symptoms through aberrant salience, linking biology, experience and drug action.
- Schultz, W., Dayan, P. & Montague, P. R. (1997). A neural substrate of prediction and reward. *Science*. https://doi.org/10.1126/science.275.5306.1593 — Shows that dopamine neuron activity signals reward prediction errors of the kind used in temporal-difference learning.

### Surveys and textbooks

- Sterzer, P. et al. (2018). The Predictive Coding Account of Psychosis. *Biological Psychiatry*. https://doi.org/10.1016/j.biopsych.2018.05.015 — Review of the predictive-coding account of psychotic symptoms and the evidence for it.
- Adams, R. A., Huys, Q. J. M. & Roiser, J. P. (2015). Computational Psychiatry: towards a mathematically informed understanding of mental illness. *Journal of Neurology, Neurosurgery & Psychiatry*. https://doi.org/10.1136/jnnp-2015-310737 — Review of how formal models can inform the understanding of mental illness, including Bayesian accounts.
- Montague, P. R., Dolan, R. J., Friston, K. J. & Dayan, P. (2012). Computational psychiatry. *Trends in Cognitive Sciences*. https://doi.org/10.1016/j.tics.2011.11.018 — Review that sets out computational psychiatry as an approach using models of learning and decision making to understand mental illness.
