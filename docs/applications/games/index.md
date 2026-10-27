---
related:
- foundations/paradigms/reinforcement-learning
- foundations/symbolic-ai
- models/agents
- applications/creative
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
| 2019 | Dota 2 | OpenAI Five | Large-scale PPO self-play |
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

## Resources

- Yannakakis & Togelius, *Artificial Intelligence and Games* (free PDF)
- [OpenSpiel](https://github.com/google-deepmind/open_spiel), [PettingZoo](https://pettingzoo.farama.org/)
- Silver et al. (2016, 2018), AlphaGo and AlphaZero papers
