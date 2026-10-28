---
status: draft
last_reviewed: 2026-10-28
related:
- brain-mind/predictive-coding
- theory/paradigms/reinforcement-learning
tags:
- computational psychiatry
- psychosis
- prediction error
aliases:
  - 異常預測誤差
  - 精神病的預測誤差
  - 妄想與預測誤差
  - Aberrant prediction error
  - Delusions and prediction error
---

# Aberrant prediction error in psychosis (Corlett et al., 2007)

A line of computational work proposes that delusional beliefs form when the brain's prediction-error signal, the learning signal from reinforcement learning, is disrupted. Corlett et al. (2007) tested this with functional MRI in 12 people with delusional beliefs and 12 healthy participants, measuring prediction-error-related brain responses.

This page is part of [Computational Psychiatry](../index.md). It describes a research hypothesis and its evidence. It does not describe a diagnostic test, and the findings concern groups rather than individual patients.

## Overview

Learning depends on comparing what happens with what was expected, and the difference is the prediction error that updates the expectation. Corlett and colleagues proposed that delusions, fixed beliefs that persist despite contrary evidence, can arise when this error signal is disrupted, so that events and beliefs become linked in ways the evidence does not support.

## Problem

Delusions are maladaptive beliefs about the world. Earlier experimental work had shown that prediction error drives belief formation. The open question was whether delusions form because the prediction-error process itself is disrupted in the brain, and whether the disruption explains why some people form delusions more readily than others.

## Core idea

Corlett et al. (2007) framed the account in associative terms. Prediction errors normally update the strength of a belief when an outcome differs from the expectation. In people with delusional beliefs, the brain response to these errors should differ from that of healthy participants. The authors also argued that disrupted attention and associative learning are part of the same picture. The hypothesis therefore makes a specific prediction: the neural prediction-error signal, not just the behaviour, should look abnormal, and its abnormality should track how prone a person is to delusions.

Using the notation of [Computational phenotyping with hierarchical Bayesian RL models](../computational-phenotyping/index.md), the learning update is \(V_{t+1} = V_t + \alpha\,\delta_t\), with \(\delta_t\) the prediction error. The hypothesis concerns the brain's representation of \(\delta_t\), which the update relies on.

Related accounts treat the same problem from other angles. Fletcher and Frith (2009) describe positive symptoms as a disturbance in the updating of beliefs, and Kapur (2003) describes psychosis as a state of aberrant salience.

## Equation or algorithm

The method is an experimental design rather than a single equation. The procedure is:

1. Recruit a group with delusional beliefs and a healthy comparison group, and measure delusional tendency.
2. Run a learning task in the scanner in which outcomes can violate expectations.
3. Model the trial-by-trial prediction errors, and use them as regressors in the fMRI analysis.
4. Compare the prediction-error responses between groups, and test whether the response relates to the degree of delusional belief across participants.

## Results

Corlett et al. (2007) studied 12 healthy participants and 12 individuals with delusional beliefs. Their abstract reports that frontal cortex responses in the patient group were suggestive of disrupted prediction-error processing, narrowed in the main text to the right prefrontal cortex. Across all participants, the extent of the disruption was significantly related to an individual's propensity to form delusions, and in the patient group the disruption was linked to delusion severity. The authors read this as support for a theory in which aberrant prediction-error signalling, disrupted attention and associative learning contribute to delusional belief.

Powers et al. (2017) extended the idea to hallucinations. Their title states that Pavlovian conditioning induces hallucinations because perceptual priors are overweighted, which links the hallucination account to the same updating mechanism.

## Limitations

- **Sample size.** The 2007 study compared 12 people with delusions with 12 controls. Small groups give limited power, so the findings need replication in larger samples.
- **Contested evidence.** Griffiths et al. (2014) re-examine the behavioural evidence for disrupted error signalling in delusion formation, so the support for the hypothesis is still debated.
- **Specificity.** Prediction-error abnormalities may reflect attention, salience or general belief processes rather than prediction error alone. Sterzer et al. (2018) review the predictive coding account of psychosis as a whole.
- **Correlation.** An abnormal signal in people with delusions does not by itself show that the abnormality causes the delusions.

## Connections

- **Dopamine and prediction error**: the animal evidence for the error signal is on [Dopamine Reward Prediction Error](../../neuroscience/dopamine-reward-prediction-error/index.md). The psychosis hypothesis asks whether a signal of this kind is abnormal in people. Decision-making links are on [Decision Making, Dopamine & Reward](../../decision-reward/index.md).
- **Predictive coding**: the view that psychosis reflects altered prediction is developed on [Predictive Coding & Free Energy](../../predictive-coding/index.md).
- **Attention and salience**: the aberrant-salience account links to [Attention in Brains & Machines](../../attention-brain-machine/index.md).
- **Individual differences and imaging**: tracking the signal across people relates to [Computational phenotyping](../computational-phenotyping/index.md), and the fMRI measurements are described on [Neuroimaging & Recording Methods](../../neuroimaging-methods/index.md).

## Applications

- **Experimental design**: associative learning tasks with patient and control groups are used to study how beliefs are formed and revised.
- **Understanding hallucinations**: Powers et al.'s conditioning paradigm separates the effect of perceptual priors from sensory evidence.
- **Clinical research**: the hypothesis guides mechanistic research. It is not yet a clinical test.

## Open questions

- **Specificity.** Is the prediction-error abnormality specific to psychosis, or does it also appear in other conditions?
- **Timing.** Does the abnormality come before symptoms, or does it develop with them?
- **Mechanism.** Is the disruption in the error signal itself, in attention, or in the priors that the error updates?
- **Replication.** Do the effects hold in larger and more diverse samples?

## References

### Seminal papers

- Corlett, P. R., Murray, G. K., Honey, G. D., Aitken, M. R. F., Shanks, D. R., Robbins, T. W., Bullmore, E. T., Dickinson, A. & Fletcher, P. C. (2007). Disrupted prediction-error signal in psychosis: evidence for an associative account of delusions. *Brain*, 130(9), 2387–2400. https://doi.org/10.1093/brain/awm173 — An fMRI study of 12 healthy participants and 12 with delusional beliefs, reporting frontal prediction-error responses that were disrupted in the patient group and related to delusion-forming tendency.
- Powers, A. R., Mathys, C. & Corlett, P. R. (2017). Pavlovian conditioning–induced hallucinations result from overweighting of perceptual priors. *Science*, 357(6351), 596–600. https://doi.org/10.1126/science.aan3458 — Reports that Pavlovian conditioning induces hallucinations, attributed to overweighted perceptual priors.
- Fletcher, P. C. & Frith, C. D. (2009). Perceiving is believing: a Bayesian approach to explaining the positive symptoms of schizophrenia. *Nature Reviews Neuroscience*, 10(1), 48–58. https://doi.org/10.1038/nrn2536 — Proposes a Bayesian account of the positive symptoms of schizophrenia, the account that the belief-updating view builds on.
- Kapur, S. (2003). Psychosis as a State of Aberrant Salience: A Framework Linking Biology, Phenomenology, and Pharmacology in Schizophrenia. *American Journal of Psychiatry*, 160(1), 13–23. https://doi.org/10.1176/appi.ajp.160.1.13 — Proposes aberrant salience as a framework linking the biology, phenomenology and pharmacology of schizophrenia.

### Surveys and textbooks

- Sterzer, P. et al. (2018). The Predictive Coding Account of Psychosis. *Biological Psychiatry*. https://doi.org/10.1016/j.biopsych.2018.05.015 — Reviews the evidence for aberrant predictive coding in psychosis and the challenges to the canonical account.
- Griffiths, O., Langdon, R., Le Pelley, M. E. & Coltheart, M. (2014). Delusions and prediction error: re-examining the behavioural evidence for disrupted error signalling in delusion formation. *Cognitive Neuropsychiatry*, 19(5), 439–467. https://doi.org/10.1080/13546805.2014.897601 — Re-examines the behavioural evidence for disrupted error signalling in delusion formation.
