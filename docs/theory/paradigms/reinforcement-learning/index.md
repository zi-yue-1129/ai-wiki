---
related:
- brain-mind/memory-learning
- brain-mind/neuroai
- applications/robotics
- applications/games
- theory/models/llm
- society/safety-alignment
- theory/paradigms/online
- theory/paradigms/imitation
aliases:
  - RL
  - 增強學習
---

# Reinforcement Learning

## Intuition

An **agent** acts in an **environment**, receives **rewards**, and tries to learn a policy that maximises **long-term cumulative reward**. Nobody tells it the right answer; it learns by trial and error. This maps deeply onto animal learning (operant conditioning) and the brain's dopamine system.

![Animated agent–environment loop: the agent observes, acts, gets feedback, and improves a policy.](../../../assets/concept-animations/agent-environment.gif)

*Agent–environment interaction (original schematic, CC BY-SA 4.0).* The agent receives an observation, selects an action, and gets a subsequent observation and reward. The grid shows one illustrative trajectory toward a goal. **Reward is feedback, not a label identifying the correct action.** The actual policy update depends on the learning algorithm.

## Formalism: Markov decision processes

An MDP is \((S, A, P, R, \gamma)\): states, actions, transition probabilities, reward function, discount factor.

- **Policy** \(\pi(a\mid s)\)
- **Return** \(G_t = \sum_{k=0}^\infty \gamma^k r_{t+k+1}\)
- **State value** \(V^\pi(s) = \mathbb{E}_\pi[G_t\mid s_t=s]\)
- **Action value** \(Q^\pi(s,a) = \mathbb{E}_\pi[G_t\mid s_t=s, a_t=a]\)

**Bellman optimality equation:**

\[
Q^*(s,a) = \mathbb{E}\big[r + \gamma \max_{a'} Q^*(s',a')\big]
\]

## Algorithm families

| Family | Examples | Idea |
|---|---|---|
| Dynamic programming | Value iteration, policy iteration | Solve Bellman equations with a known model |
| Monte Carlo | MC control | Update from complete-episode returns |
| Temporal difference (TD) | TD(0), SARSA, Q-learning | Bootstrap from the next estimate |
| Deep value-based | DQN, Double DQN, Rainbow | Neural network approximates Q |
| Policy gradient | REINFORCE | Gradient ascent on policy parameters |
| Actor–critic | A2C/A3C, PPO, SAC, TD3 | Policy (actor) + value estimate (critic) |
| Model-based | Dyna, MuZero, Dreamer | Learn a model; plan or "imagine" with it |
| Offline RL | CQL, IQL, Decision Transformer | Learn from logged data only |
| Multi-agent RL | MADDPG, QMIX, self-play | Several interacting agents |

The **TD error** is the key quantity:

\[
\delta_t = r_{t+1} + \gamma V(s_{t+1}) - V(s_t)
\]

## Reinforcement learning and the brain

### Dopamine as reward-prediction error

Schultz, Dayan & Montague (1997) showed that midbrain dopamine neurons fire in a way that closely matches the TD error δ:

- Unexpected reward → dopamine burst (δ > 0)
- Once the reward is predicted, the response moves to the **predictive cue**; the reward itself no longer excites
- Predicted reward omitted → dip below baseline (δ < 0)

This is one of the most successful meetings of computational theory and neuroscience. Later, **distributional RL** found a counterpart too: different dopamine neurons appear to encode predictions with different degrees of optimism (Dabney et al., 2020, *Nature*).

### Other correspondences

| RL concept | Brain / psychology counterpart |
|---|---|
| Model-free control | Habits; dorsolateral striatum |
| Model-based control | Goal-directed behaviour; prefrontal cortex and dorsomedial striatum |
| Actor–critic | Dorsal striatum (actor) and ventral striatum (critic) hypothesis |
| Experience replay | Hippocampal sequence replay during sleep and rest |
| Exploration vs exploitation | Norepinephrine system, frontopolar cortex; human decision research |
| Curiosity / intrinsic motivation | Novelty-driven exploration, information seeking |
| Discount factor | Delay discounting, impulsivity |
| Successor representation | Predictive maps in hippocampal place cells (Stachenfeld et al., 2017) |

Psychological roots: Thorndike's law of effect, Skinner's operant conditioning, the Rescorla–Wagner model (1972) — itself a prediction-error learning rule.

## Key methods

### Deep Q-networks (Mnih et al., 2015)

- **Problem:** how can one algorithm learn control policies directly from raw pixels across many different games?
- **Core idea:** a convolutional network approximates the action-value function Q from raw frames. Two changes make training stable: experience replay, which samples random past transitions, and a target network, which is updated only now and then.
- **Equation:** the network is trained to reduce the squared temporal-difference error against the target network:

\[
L(\theta) = \mathbb{E}\left[\left(r + \gamma \max_{a'} Q(s', a'; \theta^-) - Q(s, a; \theta)\right)^2\right]
\]

- **Results:** one network and one training procedure learned to play a range of Atari 2600 games from raw pixels.
- **Limitations:** actions must be discrete, and training needs a great deal of experience. Later work such as Double DQN and Rainbow addresses some of the remaining instability, as the algorithm table above shows.

### Proximal policy optimisation (Schulman et al., 2017)

- **Problem:** plain policy gradients can take steps so large that performance collapses. Trust-region methods are stable but complicated to implement.
- **Core idea:** clip the ratio between the new and old action probabilities in the surrogate objective, so the update gains nothing from moving far from the old policy. This allows several epochs of minibatch updates on the same batch of data.
- **Equation:** with the probability ratio \(r_t(\theta) = \pi_\theta(a_t \mid s_t) / \pi_{\theta_{\text{old}}}(a_t \mid s_t)\) and advantage estimate \(\hat{A}_t\):

\[
L^{\text{CLIP}}(\theta) = \mathbb{E}_t\left[\min\left(r_t(\theta)\hat{A}_t,\ \text{clip}\left(r_t(\theta), 1-\epsilon, 1+\epsilon\right)\hat{A}_t\right)\right]
\]

- **Results:** the paper reports that PPO outperforms other online policy gradient methods on its benchmark tasks, which include simulated robotic locomotion and Atari, with a favourable balance of sample complexity, simplicity and wall-clock time.
- **Limitations:** the evidence is empirical, and clipping is a heuristic rather than a guarantee of improvement. PPO is also on-policy, so each batch of data supports only a few updates.

## Milestones

- **TD-Gammon** (1992)
- **DQN** (2013/2015): Atari from pixels
- **AlphaGo / AlphaZero / MuZero** (2016–2019): self-play + Monte Carlo tree search
- **OpenAI Five, AlphaStar** (2019): Dota 2, StarCraft II
- **RLHF** (2017 onward, mainstream with ChatGPT in 2022): train a reward model on human preferences, then optimise the LLM with PPO
- **RL for reasoning** (2024–2025): training long chains of thought with verifiable rewards (math answers, unit tests), e.g. GRPO as used for DeepSeek-R1
- **Robotics**: sim-to-real transfer for legged and humanoid locomotion

## Practical challenges

- Poor sample efficiency
- Reward design is hard; agents exploit loopholes (**reward hacking**) — see [Safety & Alignment](../../../society/safety-alignment/index.md)
- Exploration under sparse rewards
- Unstable training, hyperparameter sensitivity
- The sim-to-real gap

## Subtopics

- [Value-based methods](value-based-methods/index.md): Q-learning, DQN and planning with learned values.
- [Policy gradient and actor-critic](policy-gradient-and-actor-critic/index.md): REINFORCE, A3C and PPO.
- [Model-based RL](model-based-rl/index.md): world models, MuZero and Dreamer.
- [Offline RL](offline-rl/index.md): learning from fixed datasets with conservative value estimates.
- [Learning from human feedback](learning-from-human-feedback/index.md): reward models and RLHF.
- [Experience replay](experience-replay/index.md): reusing past transitions to learn more from each one.
- [Exploration](exploration/index.md): how agents try new actions when rewards are sparse.

## Resources

- Sutton & Barto, *Reinforcement Learning: An Introduction*, 2nd ed. (free PDF)
- David Silver's UCL RL course
- OpenAI [Spinning Up](https://spinningup.openai.com/) (MIT)
- Hugging Face Deep RL Course
- [Gymnasium](https://gymnasium.farama.org/), [Stable-Baselines3](https://stable-baselines3.readthedocs.io/)
- Niv (2009), "Reinforcement learning in the brain" (neuroscience review)

## References

### Seminal papers

- Mnih et al. (2015), "Human-level control through deep reinforcement learning", *Nature* 518. https://doi.org/10.1038/nature14236 — The DQN paper, the start of deep reinforcement learning at scale.
- Silver et al. (2016), "Mastering the game of Go with deep neural networks and tree search", *Nature* 529. https://research.google/pubs/mastering-the-game-of-go-with-deep-neural-networks-and-tree-search/ — AlphaGo, combining learned networks with search.
- Christiano et al. (2017), "Deep reinforcement learning from human preferences", NeurIPS, arXiv:1706.03741 — Learns reward functions from human comparisons, the basis of RLHF.
- Schulman et al. (2017), "Proximal policy optimization algorithms", arXiv:1707.06347 — PPO, the policy-gradient method most used in practice.

### Surveys and textbooks

- Sutton, R. S. & Barto, A. G. *Reinforcement Learning: An Introduction*, 2nd ed. MIT Press, 2018. http://incompleteideas.net/book/the-book-2nd.html — The standard RL textbook, with a free online draft covering the algorithm families above.
- Levine, S., Kumar, A., Tucker, G. & Fu, J. (2020), "Offline reinforcement learning: tutorial, review, and perspectives on open problems", arXiv:2005.01643 — Tutorial and review on learning from fixed datasets.
