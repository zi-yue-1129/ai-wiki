---
related:
  - theory/models/computer-vision
  - theory/paradigms/reinforcement-learning
  - applications/healthcare
aliases:
  - 體育
  - 運動分析
  - 運動科學
---

# Sports Analytics and Performance

Sports analytics was an early and visible adopter of data science. Tracking systems now record player and ball positions many times per second, and models turn those traces into measures of player value, shot quality and injury risk. Officiating technology and broadcast tools are the other large application areas.

## Landscape

| Area | Methods | Notes |
|---|---|---|
| Tracking and pose estimation | Multi-person pose estimation from video; tracking-data pipelines | Foundation for most other analysis |
| Shot and chance quality | Expected-goals-style models from positional and event data | Anzer & Bauer (2021) use synchronised positional and event data |
| Player and action valuation | Models that value each action by its effect on scoring probability | VAEP (Decroos et al., 2019) |
| Team and possession models | Stochastic process models of possessions | Cervone et al. (2016) for basketball |
| Match prediction | Classifiers over team and player features | Bunker & Susnjak (2022) review the field |
| Injury prediction | Workload and biometric models | Weaker evidence than tracking analytics |
| Officiating technology | Camera-based line calls and goal-line decisions | Accuracy claims need independent checks |
| Broadcast and scouting | Automatic highlights, commentary, player search | Scouting is commercially sensitive |

## Why it is hard

- **Small samples**: a season has few goals, and many players have little playing time, so estimates are noisy.
- **Context**: the value of an action depends on the score, the opponent and the situation.
- **Data access**: tracking data is expensive, and teams guard it.
- **Causality**: a player who looks good may be on a strong team, so observational value estimates confound team and player effects.

## Key methods

- [Convolutional networks and computer vision](../../theory/models/computer-vision/index.md): the basis of camera-based tracking and pose estimation. OpenPose (Cao et al., 2017) is a widely used example.
- [Reinforcement learning](../../theory/paradigms/reinforcement-learning/index.md): values states and actions in a game, which is how some action-valuation models are framed.
- [Hierarchical and probabilistic models](../../theory/paradigms/probabilistic/index.md): model possession and shot outcomes with uncertainty, as Cervone et al. (2016) do.
- [Evaluation & validation](../../theory/paradigms/supervised/evaluation-and-validation/index.md): separating skill from luck and from team effects.

## Connections

- Injury prediction and biometric monitoring overlap with [Healthcare](../healthcare/index.md).
- Pose estimation is the same computer-vision problem used in robotics. See [Robotics](../robotics/index.md).

## Applications

- Scouting and recruitment
- In-game tactics and substitution decisions
- Automatic highlights and broadcast graphics
- Officiating assistance, such as line calls and goal-line decisions
- Training load management for injury prevention

## Risks and limits

- **Overfitting to small samples**: a model can confidently rank players on very little data.
- **Automation in officiating**: systems can be accurate and still contested, because rules decide what counts as an error.
- **Athlete surveillance**: biometric and location data raise privacy and labour questions.
- **Vendor claims**: many accuracy and injury-prediction results come from proprietary data and have not been independently replicated.

## Open questions

- How to separate a player's contribution from the contribution of teammates and opponents with observational tracking data.
- Whether injury prediction models generalise across clubs, leagues and training regimes.

## References

### Seminal papers

- Cao, Z. et al. (2017). Realtime Multi-Person 2D Pose Estimation using Part Affinity Fields. *CVPR*. https://arxiv.org/abs/1611.08050 — Real-time multi-person pose estimation that groups body parts into people, the standard approach behind many sports tracking systems.
- Decroos, T. et al. (2019). Actions Speak Louder than Goals: Valuing Player Actions in Soccer. *KDD 2019*. https://doi.org/10.1145/3292500.3330758 — Introduces VAEP, which values each on-ball action by its change in the probability of scoring or conceding.
- Cervone, D. et al. (2016). A Multiresolution Stochastic Process Model for Predicting Basketball Possession Outcomes. *Journal of the American Statistical Association*. https://doi.org/10.1080/01621459.2016.1141685 — Models basketball possessions as stochastic processes fitted to tracking data to predict outcomes.
- Anzer, G. & Bauer, P. (2021). A Goal Scoring Probability Model for Shots Based on Synchronized Positional and Event Data in Football (Soccer). *Frontiers in Sports and Active Living*. https://doi.org/10.3389/fspor.2021.624475 — Estimates shot quality from the positions of players and the ball at the moment of a shot.

### Surveys and textbooks

- Bunker, R. & Susnjak, T. (2022). The Application of Machine Learning Techniques for Predicting Match Results in Team Sport: A Review. *Journal of Artificial Intelligence Research*. https://doi.org/10.1613/jair.1.13509 — Review of machine learning methods for predicting match results, with a discussion of evaluation.
- Mathis, A. et al. (2018). DeepLabCut: markerless pose estimation of user-defined body parts with deep learning. *Nature Neuroscience*. https://doi.org/10.1038/s41593-018-0209-y — Tool for training pose estimators on custom body parts, used in animal and human movement studies.
