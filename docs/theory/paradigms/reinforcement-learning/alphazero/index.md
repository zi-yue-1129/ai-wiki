---
status: complete
last_reviewed: 2026-10-28
related:
  - applications/games
tags:
  - reinforcement learning
  - search
  - self-play
aliases:
  - AlphaZero
  - 阿爾法零
---

# AlphaZero (Silver et al., 2018)

AlphaZero is one algorithm that learns to play chess, shogi and Go from self-play, starting from random play and given only the rules of each game. It reached superhuman strength in each game and defeated state-of-the-art programs specialised for them. It simplified the [AlphaGo](../alphago/index.md) approach by removing human game data and game-specific knowledge.

## Problem

Strong game programs before AlphaZero were built for one game each. They used opening libraries, handcrafted evaluation functions and game-specific search tricks. The paper asks whether a single learning algorithm can reach top strength in several games with no such knowledge.

## Key concepts

- **Single network**: one network takes a position and outputs both a move distribution (policy) and a value.
- **Self-play with search**: the moves are chosen by MCTS guided by the network, and the search results become the training targets.
- **Tabula rasa**: training starts from random play and uses only the rules, with no human data.

## Core idea

The network proposes moves and judges positions. Monte Carlo tree search, guided by those outputs, produces a stronger move choice than the raw network. The network is then trained to predict the search's choices and the eventual game outcome. Repeating this loop improves both the network and the search together.

## Algorithm

1. Initialise a network with random weights.
2. **Self-play.** For each move, run MCTS guided by the network. Record the visit-count distribution \(\pi\) over moves and, at the end of the game, the outcome \(z\).
3. **Training.** Sample positions from recent self-play games and update the network to reduce the combined loss below.
4. Repeat steps 2 and 3, always playing with the latest network.

```latex
\mathcal{L} = (z - v)^2 - \pi^\top \log p + c\,\lVert \theta \rVert^2
```

Here \(p\) and \(v\) are the network's move probabilities and value for a position, and \(c\) controls weight regularisation.

## Results

- **Chess**: against Stockfish, the 2016 TCEC champion, the paper's text reports no losses for AlphaZero across its matches.
- **Shogi**: against Elmo, the 2017 CSA champion, the paper's text reports eight losses for AlphaZero across its matches.
- **Go**: the paper reports matches against AlphaGo Zero (3-day version) and AlphaGo Lee. The counts are in its table.
- **Training time**: the abstract says AlphaZero reached a superhuman level "within 24 hours". The paper's supplementary table lists about 9 hours for chess, 12 for shogi and 34 for Go, so the 24-hour figure does not hold for Go.

## Limitations

- The method needs an exact simulator of the game, so it applies to games with known rules and no hidden information.
- Training consumed a large amount of computation, and the timing claim refers to the paper's hardware.
- The paper evaluates only three board games. Results on other games are not shown in it.

## Connections

- [AlphaGo](../alphago/index.md): the earlier, Go-specific system with human game data.
- [MuZero](../model-based-rl/muzero/index.md): extends the same search-and-network design to games whose rules are not given to the planner.
- [Reinforcement learning](../index.md): the wider family of methods for learning from reward.
- Brain and mind: the paper does not model neural activity. Its self-play loop is a computational example of learning from experience without human teachers.

## Applications

- Game research: a general template for self-play with search in perfect-information games.

## Open questions

- How far the approach extends to games with imperfect information, or to problems with no simulator.
- How much the learned strategies depend on the amount of compute spent on self-play.

## References

### Seminal papers

- Silver, D. et al. (2018). A general reinforcement learning algorithm that masters chess, shogi, and Go through self-play. *Science*. https://doi.org/10.1126/science.aar6404 — AlphaZero, the paper that introduces the single-algorithm approach.
- Silver, D. et al. (2017). Mastering the game of Go without human knowledge. *Nature* 550, 354–359. https://doi.org/10.1038/nature24270 — AlphaGo Zero, the Go-only predecessor that learns from random play.
- Silver, D. et al. (2016). Mastering the game of Go with deep neural networks and tree search. *Nature* 529. https://doi.org/10.1038/nature16961 — AlphaGo, which uses human game data.
- Silver, D. et al. (2017). Mastering Chess and Shogi by Self-Play with a General Reinforcement Learning Algorithm. arXiv. https://arxiv.org/abs/1712.01815 — The preprint of the AlphaZero work, with the 24-hour training result and the comparison with world-champion programs.

### Surveys and textbooks

- Browne, C. et al. (2012). A Survey of Monte Carlo Tree Search Methods. *IEEE Transactions on Computational Intelligence and AI in Games*. https://doi.org/10.1109/TCIAIG.2012.2186810 — Survey of the tree-search method AlphaZero uses for planning.
- Sutton, R. S. & Barto, A. G. *Reinforcement Learning: An Introduction*, 2nd ed. MIT Press, 2018. http://incompleteideas.net/book/the-book-2nd.html — Textbook covering the value and policy methods behind self-play learning.
