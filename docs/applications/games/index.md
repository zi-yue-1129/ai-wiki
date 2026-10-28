---
related:
- theory/paradigms/reinforcement-learning
- theory/paradigms/symbolic-ai
- theory/models/agents
- applications/creative
aliases:
  - 遊戲
  - 電子遊戲
---

# Games

Games are AI's favourite laboratory: clear rules, measurable outcomes, and unlimited simulated experience.

## Milestones in game-playing AI

| Year | Game | System | Technique |
|---|---|---|---|
| 1952–59 | Checkers | Samuel | Early machine learning |
| 1992 | Backgammon | TD-Gammon | TD learning + neural network |
| 1994–2007 | Checkers | Chinook | Search; checkers solved in 2007 |
| 1997 | Chess | Deep Blue | Massive search + handcrafted evaluation |
| 2015 | Atari | DQN | Deep RL from pixels |
| 2016 | Go | AlphaGo | Policy/value networks + MCTS |
| 2017 | Chess, shogi, Go | AlphaZero | Self-play from scratch |
| 2017–2019 | Heads-up / six-player poker | Libratus, Pluribus | Counterfactual regret minimisation, imperfect information |
| 2019 | Dota 2 | [OpenAI Five](openai-five/index.md) | Large-scale PPO self-play |
| 2019 | StarCraft II | AlphaStar | League training, imitation + RL |
| 2020 | Atari, Go, chess without rules | MuZero | Learned model + planning |
| 2022 | Diplomacy | Cicero | Language model + strategic planning, negotiating with humans |
| 2022 | Stratego | DeepNash | Model-free RL in imperfect information |
| 2022 | Gran Turismo | GT Sophy | RL racing with sportsmanship |
| 2023+ | Minecraft and open worlds | Voyager, VPT, DreamerV3 | LLM agents, video pre-training, world models |

## AI in game development

- Procedural content generation: levels, terrain, quests
- Generative assets: textures, 3D models, voice, music
- NPC behaviour: behaviour trees and utility AI (still dominant), LLM-driven dialogue characters
- Testing: automated playtesting agents, bug detection
- Player modelling: matchmaking, difficulty adjustment, churn prediction, anti-cheat
- Rendering: DLSS-style neural upscaling and frame generation

## AI-native and simulated games

- Neural game engines that generate frames interactively (GameNGen ran DOOM inside a diffusion model, 2024; Genie-style world models)
- LLM-driven interactive fiction and social simulation (Generative Agents)

## Why games matter for AI research

- Benchmarks for planning, imperfect information, multi-agent cooperation and competition, long horizons
- Game theory: Nash equilibria, self-play convergence
- Transfer of ideas: AlphaZero-style search → AlphaFold's iterative refinement mindset, AlphaTensor, AlphaDev (sorting algorithms)

## Human cognition through games

- Studies of chess expertise (de Groot; Chase & Simon's chunking) shaped theories of expert memory
- Go professionals' play changed after AlphaGo: decision quality improved and novelty increased (Shin et al., 2023, *PNAS*)
- Games such as bandits and two-step tasks are standard tools in cognitive science and computational psychiatry

## Key methods

Three methods cover most of the milestones above. Each links to the page that explains it.

- [Deep Q-networks](../../theory/paradigms/reinforcement-learning/deep-q-networks/index.md): deep value learning from raw pixels, the method behind the 2015 Atari results (Mnih et al., 2015).
- [Proximal policy optimisation](../../theory/paradigms/reinforcement-learning/proximal-policy-optimisation/index.md): a clipped policy-gradient update used in large self-play systems such as OpenAI Five (Schulman et al., 2017; OpenAI et al., 2019).
- [Model-based reinforcement learning](../../theory/paradigms/reinforcement-learning/model-based-rl/index.md): planning with a learned model of the game. MuZero does this without being given the rules (Schrittwieser et al., 2020).

## References

### Seminal papers

- Samuel, A. L. (1959). Some Studies in Machine Learning Using the Game of Checkers. *IBM Journal of Research and Development*. https://doi.org/10.1147/rd.33.0210 — An early checkers program that improved its evaluation function by learning from play.
- Tesauro, G. (1995). Temporal difference learning and TD-Gammon. *Communications of the ACM*. https://doi.org/10.1145/203330.203343 — A backgammon program trained by temporal-difference learning with a neural network.
- Chase, W. G. & Simon, H. A. (1973). Perception in chess. *Cognitive Psychology*. https://doi.org/10.1016/0010-0285(73)90004-2 — Classic study of how chess experts remember positions through chunking.
- Campbell, M., Hoane, A. J. & Hsu, F.-h. (2002). Deep Blue. *Artificial Intelligence*. https://doi.org/10.1016/s0004-3702(01)00129-1 — Describes the design of the chess system that beat the world champion in 1997.
- Mnih, V. et al. (2015). Human-level control through deep reinforcement learning. *Nature*. https://doi.org/10.1038/nature14236 — Deep Q-learning from pixels across dozens of Atari games.
- Silver, D. et al. (2016). Mastering the game of Go with deep neural networks and tree search. *Nature*. https://doi.org/10.1038/nature16961 — AlphaGo, combining policy and value networks with Monte Carlo tree search.
- Silver, D. et al. (2018). A general reinforcement learning algorithm that masters chess, shogi, and Go through self-play. *Science*. https://doi.org/10.1126/science.aar6404 — AlphaZero, learning chess, shogi and Go from self-play given only the rules.
- Schrittwieser, J. et al. (2020). Mastering Atari, Go, chess and shogi by planning with a learned model. *Nature*. https://doi.org/10.1038/s41586-020-03051-4 — MuZero, planning with a learned model without being given the rules.
- Schulman, J. et al. (2017). Proximal Policy Optimization Algorithms. arXiv. https://arxiv.org/abs/1707.06347 — The clipped-objective policy-gradient algorithm known as PPO.
- OpenAI et al. (2019). Dota 2 with Large Scale Deep Reinforcement Learning. arXiv. https://arxiv.org/abs/1912.06680 — OpenAI Five, large-scale self-play with PPO in Dota 2.
- Vinyals, O. et al. (2019). Grandmaster level in StarCraft II using multi-agent reinforcement learning. *Nature*. https://doi.org/10.1038/s41586-019-1724-z — AlphaStar, trained through league play against a population of agents.
- Brown, N. & Sandholm, T. (2019). Superhuman AI for multiplayer poker. *Science*. https://doi.org/10.1126/science.aay2400 — Pluribus, which plays six-player no-limit Texas hold'em.
- Perolat, J. et al. (2022). Mastering the game of Stratego with model-free multiagent reinforcement learning. *Science*. https://doi.org/10.1126/science.add4679 — DeepNash, model-free reinforcement learning in an imperfect-information game.
- Wurman, P. R. et al. (2022). Outracing champion Gran Turismo drivers with deep reinforcement learning. *Nature*. https://doi.org/10.1038/s41586-021-04357-7 — GT Sophy, reinforcement learning that raced against top human drivers.
- Meta Fundamental AI Research Diplomacy Team (FAIR) et al. (2022). Human-level play in the game of *Diplomacy* by combining language models with strategic reasoning. *Science*. https://doi.org/10.1126/science.ade9097 — Cicero, a language model combined with strategic planning for negotiation.
- Park, J. S. et al. (2023). Generative Agents: Interactive Simulacra of Human Behavior. arXiv. https://arxiv.org/abs/2304.03442 — LLM agents in a simulated town that plan and remember.
- Shin, M. et al. (2023). Superhuman artificial intelligence can improve human decision-making by increasing novelty. *PNAS*. https://doi.org/10.1073/pnas.2214840120 — Compares Go players' moves before and after AlphaGo, finding more novel and better decisions.

### Surveys and textbooks

- Yannakakis, G. N. & Togelius, J. (2018). *Artificial Intelligence and Games*. Springer. https://doi.org/10.1007/978-3-319-63519-4 — Textbook on AI for playing, generating and modelling games.

## Further learning

- [OpenSpiel](https://github.com/google-deepmind/open_spiel) — Open-source framework for research in games and multi-agent learning.
- [PettingZoo](https://pettingzoo.farama.org/) — Standard API and environments for multi-agent reinforcement learning.
