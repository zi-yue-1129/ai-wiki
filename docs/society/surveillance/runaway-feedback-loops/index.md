---
status: draft
last_reviewed: 2026-10-28
aliases:
  - 失控回饋迴圈
  - 預測性警務回饋迴圈
  - Runaway feedback loops
  - PredPol
---

# Runaway Feedback Loops in Predictive Policing (Ensign et al., 2017)

Ensign et al. (2017) model predictive policing as an urn process. They show why recorded crime can keep sending police to the same neighbourhoods whatever the true crime rate, and that correcting the incident data can let the system learn the true rates. It is a method page of [Surveillance, Facial Recognition and Human Rights](../index.md).

## Overview

A predictive policing system forecasts where crime will occur, sends patrols there, and adds the crimes they record to its data for the next forecast. Officers can record crime only where they are, so heavily patrolled areas produce more records, which justify more patrols. The paper names this runaway feedback and explains it mathematically.

## Key concepts

- **Discovered incident**: a crime recorded because an officer was present to see it.
- **Reported incident**: a crime recorded because a resident reported it.
- **Pólya urn**: a model in which drawing a ball and returning it with an extra ball of the same colour reinforces the colours already drawn.

## How it works

The paper models two areas, A and B, as an urn with red and black balls. Each step draws a ball to choose where the officer goes. If the officer is in an area with true crime rate $\lambda$, a crime is discovered with that probability, and a ball of the area's colour is added. Otherwise the urn is unchanged. With $n_A(t)$ red balls at time $t$, the chance of a visit to A is

$$
\Pr(\text{visit } A \text{ at } t) = \frac{n_A(t)}{n_A(t)+n_B(t)}
$$

1. Set initial ball counts, which stand for the system's prior belief.
2. Draw a ball to choose the area to patrol.
3. Record discoveries at that area's true rate, adding a ball of the matching colour for each.
4. Repeat, and read off the long-run share of visits to each area.

With equal crime rates, the long-run share is a random draw fixed by the initial counts, so the system never learns that the areas are identical. With unequal rates the outcome can be extreme. In the paper's example, a 10% rate in A and 11% in B make the process settle on B with probability one.

The repair drops incident records with a probability tied to how often police visit each area. If police go to A 90% of the time, A's records are dropped 90% of the time and B's 10% of the time. The paper argues that this makes the urn proportions converge to the ratio of crime rates.

## Results

- **Urn analysis.** With equal rates, the limiting share is set by the prior, not by the truth. With unequal rates, feedback can drive the outcome toward one area.
- **Urn simulation (Figure 1).** Over 1,000 runs of 1,000 days, a force deployed in line with the true rates would send 56.7% of patrols to Top1 rather than Top2, and 61.0% rather than a random region. Uncorrected urns send all patrols to Top1, while corrected urns converge to the true rates.
- **PredPol simulation (Figure 2).** Using the PredPol implementation and Oakland data from Lum and Isaac (2016), each one-year run is repeated 300 times. Uncorrected allocations fluctuate widely and do not converge to the true rates. With the correction, predictions fluctuate around the true rates, though still noisily.
- **Reported incidents.** Including reported incidents does not remove the runaway feedback, even with many of them, according to the paper.

## Limitations

- **Simplified model.** Each crime is one count, with no offence type, time of day or demographics.
- **Known rates in simulation.** The simulations treat drug-use rates as the crime rate. Real true rates are unknown, which makes the correction hard to check in practice.
- **One system, one city.** The empirical part covers one algorithm and one city's data.
- **Operator cooperation.** The repair changes the inputs in a black-box way, so only the system's operators can apply it.

## Connections

- The Oakland data, and the argument that biased records reproduce bias, come from [Lum and Isaac (2016)](https://doi.org/10.1111/j.1740-9713.2016.00960.x). [Alikhademi et al. (2021)](https://doi.org/10.1007/s10506-021-09286-4) review the fairness literature.
- The urn is a reinforcement process, the subject of [Reinforcement learning](../../../theory/paradigms/reinforcement-learning/index.md).
- The AI Act's ban on risk assessment based solely on profiling is the legal counterpart of this problem. See the [topic page](../index.md).

## Open questions

- Does the correction hold when true crime rates are unknown and reporting is itself biased?
- Do similar feedback loops affect other allocation systems, such as inspection schedules?
- Should predictive systems that change their own training data be restricted?

## References

### Seminal papers

- Ensign, D. et al. (2017). Runaway Feedback Loops in Predictive Policing. arXiv. https://arxiv.org/abs/1706.09847 — Urn model and simulations of predictive policing, showing runaway feedback and a data correction.

### Surveys and textbooks

- Alikhademi, K. et al. (2021). A review of predictive policing from the perspective of fairness. *Artificial Intelligence and Law*. https://doi.org/10.1007/s10506-021-09286-4 — Reviews predictive policing systems and the fairness problems they raise.

### Articles and documentation

- Lum, K. & Isaac, W. (2016). To Predict and Serve? *Significance*. https://doi.org/10.1111/j.1740-9713.2016.00960.x — Argues that predictive policing trained on biased data produces biased predictions.
- Hung, T.-W. & Yen, C.-P. (2023). Predictive policing and algorithmic fairness. *Synthese*. https://doi.org/10.1007/s11229-023-04189-0 — Examines racial discrimination in a Chicago predictive policing system and proposes governance.
- Chapman, A. et al. (2022). A Data-driven analysis of the interplay between Criminological theory and predictive policing algorithms. *ACM FAccT*. https://doi.org/10.1145/3531146.3533071 — Examines how criminological theory and predictive policing algorithms interact, using data.
