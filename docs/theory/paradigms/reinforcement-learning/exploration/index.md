---
related:
- theory/paradigms/online
- brain-mind/neuroscience
aliases:
  - Exploration
  - Exploration–Exploitation
  - Intrinsic Motivation
  - 探索
  - 探索與利用
  - 內在動機
tags:
  - reinforcement learning
  - exploration
  - intrinsic motivation
last_reviewed: 2026-10-28
---

# Exploration

An agent learns only about the actions it tries, so it must choose between exploiting what it already knows and exploring to find something better. In reinforcement learning this trade-off decides whether an agent ever finds rare rewards. Simple random exploration works when rewards are dense, but fails on hard problems where a long, specific sequence of actions is needed before any reward appears. Most exploration methods are therefore bonuses or mechanisms that make less-visited or less-understood states attractive. Exploration is a component of every [value-based](../value-based-methods/index.md) and [policy-gradient](../policy-gradient-and-actor-critic/index.md) method, and it is closely related to the [multi-armed bandit](../../online/stochastic-bandits/index.md) problem.

## Overview

Exploration methods differ in what signal they add to the reward:

- **Undirected noise** perturbs actions or parameters, without regard to what has been seen.
- **Count-based bonuses** reward visiting states that have been seen rarely.
- **Prediction-error bonuses** reward states the agent cannot yet predict, using a learned model.
- **Posterior or ensemble methods** keep several hypotheses and act according to one of them.
- **Archive-based methods** keep a memory of promising states and return to them.

## Approaches

| Family | Idea | Key paper |
|---|---|---|
| Random action noise | ε-greedy or softmax action selection | Sutton & Barto (2018) |
| Pseudo-count bonus | Estimate state visitation with a density model and add a bonus that falls with visits | Bellemare et al. (2016), [arXiv:1606.01868](https://arxiv.org/abs/1606.01868) |
| [Intrinsic Curiosity Module](icm/index.md) | Bonus is the error of a forward model in a learned feature space | Pathak et al. (2017), [arXiv:1705.05363](https://arxiv.org/abs/1705.05363) |
| [Random network distillation](rnd/index.md) | Bonus is the error of a predictor that imitates a fixed random network | Burda et al. (2018), [arXiv:1810.12894](https://arxiv.org/abs/1810.12894) |
| Noisy networks | Learn the scale of noise on network weights, so exploration adapts during training | Fortunato et al. (2017), [arXiv:1706.10295](https://arxiv.org/abs/1706.10295) |
| Bootstrapped DQN | Several value heads on a shared network; a sampled head guides each episode | Osband et al. (2016), [arXiv:1602.04621](https://arxiv.org/abs/1602.04621) |
| Go-Explore | Keep an archive of visited states, return to promising ones, then explore from them | Ecoffet et al. (2019), [arXiv:1901.10995](https://arxiv.org/abs/1901.10995) |

### Count-based and prediction-based bonuses

Count bonuses decay with visits, which encourages covering the state space. In high-dimensional observations exact counts are impossible, so pseudo-counts come from a density model. Prediction-error bonuses use the error of a learned predictor as novelty. The Intrinsic Curiosity Module predicts the consequence of actions in a feature space learned to ignore things the agent cannot control. Random network distillation avoids a learned feature space by predicting outputs of a fixed random network.

### Parameter noise and ensembles

Noisy networks add learned noise to the weights, so the agent becomes less random as it learns. Bootstrapped DQN keeps several heads, each trained on a different bootstrap sample of the data. Acting with one sampled head for a whole episode produces consistent, deep exploratory behaviour rather than dithering, which is why it is often described as deep exploration.

### Archive-based exploration

Go-Explore separates two problems: reaching a state that has been found before and then exploring from it. It keeps an archive of distinct states, selects one, returns to it, and explores. Reaching a known state is possible because the simulator can be reset to a saved state. On Atari games with very sparse rewards, such as Montezuma's Revenge, it reached scores far beyond earlier methods.

## Trade-offs

- **Bonuses change the objective.** A bonus adds to the reward, so an agent can keep seeking novelty after the task is solved, and the final policy may be suboptimal unless the bonus decays.
- **Stochastic distractions.** A source of unpredictable noise produces permanent prediction error. An agent driven by prediction error can then stare at it indefinitely; this is called the noisy-TV problem.
- **Hyperparameter sensitivity.** The scale of the bonus relative to the task reward is often the most important setting, and the right value varies between tasks.
- **Reset requirements.** Archive methods assume the environment can be restored to a saved state, which is not true of many real systems.

## Connections

Exploration in bandit problems has a long theory based on regret bounds, covered in the [online learning](../../online/index.md) section. Those results guide value-based methods but rarely transfer directly to deep networks. Exploration is also tightly coupled to [experience replay](../experience-replay/index.md), since the data an agent keeps determines what it can learn from rare events.

Psychology and neuroscience separate two kinds of exploration in human choice. Wilson et al. (2014) found that people combine a directed component, which favours options with high uncertainty or information value, with a random component that adds choice noise. Dopamine and noradrenaline systems are often linked to exploration, although the mapping is debated. See [neuroscience](../../../../brain-mind/neuroscience/index.md) for the wider context.

## Open issues and further variants

- **Scaling counts and novelty.** Pseudo-counts and prediction errors become unreliable in very large observation spaces, and it is unclear which novelty measure scales best.
- **Distinguishing learnable from unlearnable novelty.** Methods that ignore stochastic noise are still approximate, and the boundary between useful and useless curiosity is not formalised.
- **Exploration in language and generative models.** Sampling diverse outputs during reinforcement learning from feedback can be seen as exploration. Its relation to classic bonuses is largely unstudied.
- **Exploration in sparse, long-horizon tasks.** Archive and subgoal methods help, but they need a notion of progress that is usually hand-designed.
- **Safety during exploration.** Exploratory actions can be unsafe in physical systems. Constrained exploration and safe fallback policies are active areas.
- **Evaluation.** Hard-exploration benchmarks such as Montezuma's Revenge are used to compare methods, but results are sensitive to seeds and implementation details.

## References

### Seminal papers

- Bellemare, M. G., et al. (2016). "Unifying Count-Based Exploration and Intrinsic Motivation". [arXiv:1606.01868](https://arxiv.org/abs/1606.01868) — Derives count-based bonuses from pseudo-counts of a density model.
- Pathak, D., et al. (2017). "Curiosity-driven Exploration by Self-supervised Prediction". [arXiv:1705.05363](https://arxiv.org/abs/1705.05363) — Uses forward-model prediction error in a learned feature space as the bonus.
- Burda, Y., et al. (2018). "Exploration by Random Network Distillation". [arXiv:1810.12894](https://arxiv.org/abs/1810.12894) — Uses the error of a predictor that copies a fixed random network as the novelty bonus.
- Osband, I., et al. (2016). "Deep Exploration via Bootstrapped DQN". [arXiv:1602.04621](https://arxiv.org/abs/1602.04621) — Uses an ensemble of value heads for consistent, deep exploration.
- Ecoffet, A., et al. (2019). "Go-Explore: a New Approach for Hard-Exploration Problems". [arXiv:1901.10995](https://arxiv.org/abs/1901.10995) — Archives promising states and returns to them before exploring.

### Surveys and textbooks

- Sutton, R. S. & Barto, A. G. *Reinforcement Learning: An Introduction*, 2nd ed. MIT Press, 2018. http://incompleteideas.net/book/the-book-2nd.html — Covers ε-greedy action selection and the exploration–exploitation trade-off.

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Wilson, R. C., et al. (2014). "Humans use directed and random exploration to solve the explore–exploit dilemma". *Journal of Experimental Psychology: General* 143(6). https://doi.org/10.1037/a0038199 — Behavioural evidence that people use both uncertainty-directed and random exploration.
- Fortunato, M., et al. (2017). "Noisy Networks for Exploration". [arXiv:1706.10295](https://arxiv.org/abs/1706.10295) — Learns the noise scale of network weights so exploration decays where the agent is certain.
