---
status: complete
last_reviewed: 2026-10-28
---

# Heuristics and biases (Tversky & Kahneman, 1974)

Judgement under uncertainty relies on a few heuristics, namely representativeness, availability, and anchoring and adjustment. Each is useful, and each produces systematic and predictable errors.

## Overview

People constantly judge how likely or how common things are, often without the time, data or statistical training to compute an exact answer. Their judgements are shaped by fast mental shortcuts, which usually work well and sometimes fail in predictable ways. Tversky and Kahneman's 1974 article in *Science* named three such shortcuts and showed the characteristic errors each one produces. It summarised a research programme, and several of its experiments were reported in fuller form in companion papers in *Cognitive Psychology*.

The work founded what came to be called the heuristics-and-biases programme. It also set up a long-running debate: are these shortcuts flawed reasoning, or adaptive tools that trade a little accuracy for a lot of speed?

## Key concepts

- **Heuristic**: a rule of thumb that reaches an answer quickly by replacing a hard question with an easier one.
- **Representativeness**: judging whether an object A belongs to a class B by how closely A resembles the typical member of B.
- **Availability**: judging how frequent or how probable an event is by how easily instances of it come to mind.
- **Anchoring and adjustment**: starting from a number, often one that is given, and adjusting from it. The adjustment is usually too small.
- **Base rate**: the prior frequency of a category in the population. Probability theory says it must be combined with the evidence about an individual.
- **Normative answer**: the answer that probability theory gives. Experiments compare people's judgements with it.

## Problem

How do people judge probabilities and frequencies when they cannot compute the exact answer? In everyday judgement there is seldom time or data for a full statistical analysis, so people must rely on something quicker. The question is whether that quicker route is systematically off, and if so, in which direction.

## Core idea

Under uncertainty, the article argues, people rely on a small set of heuristics:

- **Representativeness**, which is used when people judge whether an object or event belongs to a class by how well it resembles that class.
- **Availability**, which is used when people judge how frequent a class or how plausible a development is by how easily instances come to mind.
- **Adjustment from an anchor**, which is used when people make a numerical prediction starting from a value that is available.

These heuristics are economical and usually effective. They lead, however, to systematic and predictable errors. Understanding the heuristics and the biases they produce could improve judgements in uncertain situations.

## Equation or algorithm

The normative benchmark for the experiments is Bayes' rule, which gives the probability of an event A given evidence B:

$$P(A \mid B) = \frac{P(B \mid A)\, P(A)}{P(B)}$$

The term $P(A)$ is the base rate. Representativeness tends to drop it, which is why the bias is called base-rate neglect. The equation is the standard the experiments compare against. It is not a formula the article uses to model judgement.

The article describes the representativeness judgement as a procedure:

1. Read a description of an individual or an event.
2. Compare the description with the stereotype of each candidate category.
3. Pick the category whose stereotype the description matches best.
4. Report that category as the answer, without weighting it by how common the category is in the population.

Step 4 is where the bias enters. When base rates should matter, the method ignores them.

## Results

Judgements deviate in predictable directions from the normative answers. Examples from the 1974 article and its companion studies:

- **Base rates.** In the engineer-lawyer study, judged probabilities for a personal description were nearly the same whether the group was 70 engineers and 30 lawyers or the reverse. Bayes' rule requires a large difference between these conditions. When the description carried no diagnostic information, subjects gave about .5 whether engineers made up 70 or 30 per cent of the group, instead of using the base rate.
- **Sample size.** In a 1972 study of judged sampling distributions, sample size of 10, 100 or 1000 had no effect on subjective sampling distributions, although a larger sample is more reliable.
- **Anchoring.** Participants first spun a wheel of fortune that stopped at 10 or at 65, then estimated the percentage of African countries in the United Nations. The median estimates were 25 for the group anchored at 10 and 45 for the group anchored at 65. Payment for accuracy did not remove the effect.
- **Availability.** Words starting with *r* were judged more common than words with *r* in the third position, even for consonants that actually appear more often in the third position. Lists with more famous men or more famous women were judged to contain more people of that sex.

## Limitations

The heuristics are described in words rather than as a formal model. The article does not say exactly when each heuristic applies, so which one a person uses must be inferred from the errors they make. Many experiments used short hypothetical problems, which may not capture judgement in real settings.

Later work has challenged the bias framing. Gigerenzer and Gaissmaier (2011) describe heuristics as efficient cognitive processes that ignore part of the information, and they argue that less information and computation can in some environments improve accuracy. On this view, many heuristics are adaptive rather than simply biased. The debate is not settled, and the article does not resolve it.

## Key methods

A brief comparison of the landmark accounts related to this topic:

- **Representativeness** (Kahneman & Tversky, 1972): judges by resemblance to a category. It explains base-rate and sample-size neglect, but not every case of misjudgement.
- **Availability** (Tversky & Kahneman, 1973): judges frequency by ease of recall. It explains errors driven by vivid, recent or imaginable events.
- **Anchoring and adjustment** (Tversky & Kahneman, 1974): starts from an available number and adjusts too little. It explains how an arbitrary starting value shapes estimates.
- **Fast-and-frugal heuristics** (Gigerenzer & Gaissmaier, 2011): a different reading of the same shortcuts, judged by how accurate they are in particular environments rather than by how far they depart from probability theory.
- The normative benchmark is [Bayesian inference](../../../theory/paradigms/probabilistic/index.md), which the experiments use as the standard for correct judgement.

## Connections

- Parent topic: [Cognitive Science](../index.md)
- Companion page: [Building Machines That Learn Like People](../building-machines-like-people/index.md) argues that human-like machines need causal and intuitive structure, which bears on why people's shortcuts go wrong.
- [Psychology](../../psychology/index.md) gives the wider empirical background on judgement, and [Decision and Reward](../../decision-reward/index.md) covers how judgements feed into choice.
- [Probabilistic Methods](../../../theory/paradigms/probabilistic/index.md) describes Bayesian reasoning, the normative standard used throughout the experiments.

## Applications

- **Medical and risk judgement.** Diagnosis requires combining the base rate of a condition with test evidence. The base-rate neglect described in 1974 explains why clinicians and patients can misread a positive result.
- **Forecasting and risk perception.** Availability explains why vivid events, such as a recent accident, can make a risk seem larger than its frequency (Tversky & Kahneman, 1973).
- **Numerical estimation.** The anchoring results show that an arbitrary starting value can shape estimates even when people are paid for accuracy (Tversky & Kahneman, 1974).
- **Machine learning.** The contrast between judging by resemblance and reasoning with explicit priors is one reason the [Lake et al. page](../building-machines-like-people/index.md) asks for structured, probabilistic models in learning systems.

## Open questions

- When do heuristics produce errors, and when are they adaptive? Gigerenzer and Gaissmaier (2011) give one answer, but the question is not settled.
- How well can training remove base-rate neglect and anchoring, and does the effect last outside the laboratory?
- Can the three heuristics be turned into formal models that predict which one a person will use in a given situation?
- Which brain processes implement representativeness and availability, and do they differ from the processes that compute probabilities?

## References

### Seminal papers

- Tversky, A. & Kahneman, D. (1974). Judgment under Uncertainty: Heuristics and Biases. *Science*. https://doi.org/10.1126/science.185.4157.1124 — Introduces representativeness, availability and anchoring and adjustment, and the systematic errors each produces.
- Kahneman, D. & Tversky, A. (1972). Subjective probability: A judgment of representativeness. *Cognitive Psychology*. https://doi.org/10.1016/0010-0285(72)90016-3 — Shows that judged sampling distributions ignore sample size, a consequence of judging by representativeness.
- Tversky, A. & Kahneman, D. (1973). Availability: A heuristic for judging frequency and probability. *Cognitive Psychology*. https://doi.org/10.1016/0010-0285(73)90033-9 — Introduces availability, with experiments on word frequency, famous names and illusory correlation.

### Surveys and textbooks

- Gigerenzer, G. & Gaissmaier, W. (2011). Heuristic decision making. *Annual Review of Psychology*. https://doi.org/10.1146/annurev-psych-120709-145346 — Reviews heuristics as efficient cognitive processes that can be accurate in uncertain environments.
- Gigerenzer, G. & Brighton, H. (2009). Homo heuristicus: Why biased minds make better inferences. *Topics in Cognitive Science*. https://doi.org/10.1111/j.1756-8765.2008.01006.x — Reviews evidence that less information and computation can improve accuracy, the main alternative to the bias account.
