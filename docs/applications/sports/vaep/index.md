---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/probabilistic
tags:
  - evaluation
  - sequence modelling
  - sports
aliases:
  - VAEP
  - 動作價值
  - 球員動作估值
  - Valuing player actions
  - Action values
---

# VAEP (Decroos et al. 2019)

VAEP is a framework for valuing any on-the-ball action in soccer by how much it changes a team's chance of scoring and of conceding. It extends the logic of expected goals from shots to every pass, dribble and tackle, and it is one of the methods described on the parent page [Sports Analytics and Performance](../index.md).

## Overview

Most traditional player statistics count a small set of events. Goals, assists and shots are easy to record, but they are rare, and they say little about the many other actions that move the ball toward or away from goal. Some metrics ignore the context in which an action happened. A pass in a team's own half, for example, means something different from the same pass near the opponent's penalty area. Decroos, Bransen, Van Haaren and Davis (2019) argue that a useful metric must value any type of action by its effect on the game outcome and must account for context.

VAEP answers this with two parts. The first is a language, SPADL, that describes each on-the-ball action in a common form, so that event logs from different providers can be analysed the same way. The second is a probabilistic model that scores each action by the change it makes to the probability of the next goal being scored by its team or conceded. Summing these values over a player's actions gives a total of offensive and defensive contribution.

## Key concepts

- **On-the-ball action**: an event in which a player touches the ball, such as a pass, a dribble, a shot or a tackle. VAEP values these actions.
- **Game state**: the short history of recent actions leading up to an action. The model uses this history as context.
- **Scoring and conceding probabilities**: estimates of the chance that a team scores, or concedes, within a fixed number of following actions, given the current game state.
- **Action value**: the change in those probabilities caused by an action. A positive value means the action raised the team's expected outcome.
- **Player contribution**: the sum of action values over a player's actions in a match or a season.

## How it works

Write $P^{\text{score}}(S)$ and $P^{\text{concede}}(S)$ for the estimated probabilities that the team in possession scores or concedes within a fixed look-ahead window of actions, given the game state $S$. Let $S_{t-1}$ be the state before action $a_t$ and $S_t$ the state after it. The value of the action is the change in the difference between the two probabilities:

$$
V(a_t) = \Big[P^{\text{score}}(S_t) - P^{\text{score}}(S_{t-1})\Big] - \Big[P^{\text{concede}}(S_t) - P^{\text{concede}}(S_{t-1})\Big].
$$

A pass that moves the ball into a dangerous area raises the scoring probability, so it receives a positive value. A pass that gives the ball away raises the conceding probability, so it receives a negative one. The notation here is simplified from the paper.

1. **Describe the actions.** Convert the provider's event log into SPADL. Each action has a type, a team, a player, a start and end location, a time and an outcome.
2. **Build states.** For each action, collect the recent actions as features, including their types, locations, times and results.
3. **Label the outcomes.** For each state, record whether the team scores, and whether it concedes, within the look-ahead window that follows.
4. **Train two classifiers.** Fit one model for each outcome on the labelled states from many matches. The authors' implementation uses gradient-boosted tree classifiers.
5. **Value and aggregate.** Apply the two models to every action, compute $V(a_t)$, and sum the values by player, team and season.

The approach is supervised, and it needs no hand-set weights for each action type. Its outputs are probabilities, so a player's total is an expected contribution rather than a count.

## Results

The arXiv abstract of the paper states that the authors introduce a language for describing player actions and a framework for valuing any type of action by its effect on the game outcome. It reports use cases in scouting and in characterising playing style, using matches from the 2016/2017 and 2017/2018 seasons in Europe's top competitions. The abstract stresses these use cases rather than a single benchmark score. Quantitative comparisons with other ratings are in the full paper, and they should be read there before any claim about accuracy is made.

## Limitations

- **Dependence on event data.** Action types, locations and outcomes come from a provider's log. A different definition of a tackle or a pass changes the values.
- **No off-ball value.** Event data record actions with the ball. Valuable movement without the ball, such as runs that open space, is invisible to the model unless tracking data are added.
- **Arbitrary choices.** The length of the look-ahead window and the features of the game state are design decisions, and the results may be sensitive to them.
- **Credit assignment.** An action may matter because of a chain of earlier actions, and the model credits each action only through the state it sees.
- **Aggregation bias.** Season totals favour players who play more minutes. Rates per minute or per action are needed for fair comparisons between players with different roles.

## Open questions

- Can event-based values be combined with tracking data to value off-ball movement?
- How well do the values agree with the judgements of professional analysts, and with the later results of the players being rated?
- Does the approach transfer to other invasion sports, such as basketball or hockey, with their own action types and scoring rules?
- Do the values reflect the quality of actions, or mainly the strength of the team that performs them? Separating the two is an open statistical question.

## References

### Seminal papers

- Decroos, T. et al. (2019). Actions speak louder than goals: valuing player actions in soccer. *KDD*. https://doi.org/10.1145/3292500.3330758 — Introduces SPADL and VAEP, which value each on-the-ball soccer action by its effect on scoring and conceding.
- Decroos, T. et al. (2018). Actions speak louder than goals: valuing player actions in soccer. arXiv. https://arxiv.org/abs/1802.07127 — Preprint version describing the action language and value framework, with scouting and playing-style use cases from two European seasons.
- Pappalardo, L. et al. (2019). PlayeRank: data-driven performance evaluation and player ranking in soccer via a machine learning approach. *ACM Transactions on Intelligent Systems and Technology*. https://doi.org/10.1145/3343172 — Rates players by role from millions of match events and compares the ratings with scouts' evaluations.

### Surveys and textbooks

- Gudmundsson, J. & Horton, M. (2017). Spatio-temporal analysis of team sports. *ACM Computing Surveys*. https://doi.org/10.1145/3054132 — Surveys the analysis of team movement from tracking data, the richer source against which event-based values can be compared.

### Articles and documentation

- Pappalardo, L. et al. (2019). A public data set of spatio-temporal match events in soccer competitions. *Scientific Data*. https://doi.org/10.1038/s41597-019-0247-7 — Releases a public dataset of match events, the kind of input that action-value models need.
- Rathke, A. (2017). An examination of expected goals and shot efficiency in soccer. *Journal of Human Sport and Exercise*. https://doi.org/10.14198/jhse.2017.12.Proc2.05 — Examines expected goals for shots, the shot-only measure that VAEP generalises to all actions.
