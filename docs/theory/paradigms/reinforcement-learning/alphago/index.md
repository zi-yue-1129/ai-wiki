---
status: draft
last_reviewed: 2026-10-28
related:
  - applications/games
tags:
  - reinforcement learning
  - search
  - games
aliases:
  - AlphaGo
  - 阿爾法圍棋
---

# AlphaGo (Silver et al., 2016)

AlphaGo is a Go-playing system that combines deep neural networks with Monte Carlo tree search. In October 2015 it beat Fan Hui, the European Go champion, and the 2016 *Nature* paper reports those results. It marked the first time a computer program defeated a professional Go player in an even game, which had been considered out of reach for search-based programs.

## Problem

Go has a far larger space of legal positions than chess, and a position's value is hard to judge by counting material or territory. Earlier programs relied on handcrafted evaluations and were weak against professionals. The paper asks whether learned evaluation and learned move choice, combined with search, can close that gap.

## Key concepts

- **Policy network**: given a position, outputs a probability for each legal move. It proposes which moves are worth examining.
- **Value network**: given a position, estimates the probability that the player to move will win. It judges positions without playing them to the end.
- **Monte Carlo tree search (MCTS)**: builds a search tree by simulating games from the current position, guided by the policy and evaluated by the value network.
- **Self-play**: the networks improve by playing against earlier versions of themselves.

## Core idea

The policy network narrows the set of moves the search considers, and the value network replaces many random game playouts with a single learned judgement of each position. Search then chooses the move with the best combined evidence. Neither network alone is enough: the policy keeps the search focused, and the value keeps it from playing out every line to the end.

## Algorithm

1. **Supervised policy.** Train a policy network to predict moves from a database of expert human games.
2. **Reinforcement-learning policy.** Improve that policy by self-play, playing the current network against a pool of earlier versions and updating it from the results.
3. **Value network.** Train a value network on positions sampled from self-play games, with the eventual game outcome as the target.
4. **Search.** At each move, run MCTS. Each simulation selects an edge by a rule that balances the value estimate and the policy prior, expands a new position, evaluates it with the value network, and backs the result up the tree.

The selection rule in the paper has the form

```latex
a_t = \arg\max_a \left( Q(s_t, a) + u(s_t, a) \right), \qquad u(s, a) \propto \frac{P(s, a)}{1 + N(s, a)}
```

where \(Q\) is the average value of simulations through an edge, \(P\) is the policy prior and \(N\) is the visit count.

## Results

- **Against the European champion**: AlphaGo defeated the human European Go champion Fan Hui 5 games to 0, a result the 2016 paper reports.
- **Against other Go programs**: the abstract reports a 99.8% winning rate against other Go programs.
- **Without search**: the paper reports that its networks, with no lookahead search, play at the level of leading Monte Carlo tree search programs.

## Limitations

- Training used expert human games, so the system depended on human data for its starting point. The later [AlphaZero](../alphazero/index.md) work removed this dependency for its games.
- The method needs an exact simulator of the game, which Go provides but many real problems do not.
- Strength came from a large amount of computation, both in training and in search at play time.

## Connections

- [AlphaZero](../alphazero/index.md): the successor that learns from self-play with no human games.
- [MuZero](../model-based-rl/muzero/index.md): the successor that plans with a learned model instead of the game's rules.
- [Reinforcement learning](../index.md): the wider family, including the reward-prediction account of dopamine in its brain section.
- Brain and mind: a study of Go players reports that decisions changed after AlphaGo, with more novel moves (Shin et al., 2023). See the [Games](../../../../applications/games/index.md) page.

## Applications

- Game research: the approach is a reference point for combining learned evaluation with search in board games.
- Human expertise: the Shin et al. (2023) study uses Go as a setting in which to measure how a strong computer opponent changes human decisions.

## Open questions

- How much of the result came from the search and how much from the learned networks, and how the two trade off at different compute budgets.
- Whether the same combination works in games with hidden information, where the simulator cannot be used directly.

## References

### Seminal papers

- Silver, D. et al. (2016). Mastering the game of Go with deep neural networks and tree search. *Nature* 529. https://doi.org/10.1038/nature16961 — AlphaGo, combining policy and value networks with Monte Carlo tree search.
- Silver, D. et al. (2017). Mastering the game of Go without human knowledge. *Nature* 550, 354–359. https://doi.org/10.1038/nature24270 — AlphaGo Zero, which learns Go from random play without human game data.
- Silver, D. et al. (2018). A general reinforcement learning algorithm that masters chess, shogi, and Go through self-play. *Science*. https://doi.org/10.1126/science.aar6404 — AlphaZero, applying the same self-play method to three games.

- Shin, M. et al. (2023). Superhuman artificial intelligence can improve human decision-making by increasing novelty. *PNAS*. https://doi.org/10.1073/pnas.2214840120 — Compares Go players' moves before and after AlphaGo, finding more novel moves and improved decision quality.

### Surveys and textbooks

- Browne, C. et al. (2012). A Survey of Monte Carlo Tree Search Methods. *IEEE Transactions on Computational Intelligence and AI in Games*. https://doi.org/10.1109/TCIAIG.2012.2186810 — Survey of MCTS methods and their applications, including Go.
- Sutton, R. S. & Barto, A. G. *Reinforcement Learning: An Introduction*, 2nd ed. MIT Press, 2018. http://incompleteideas.net/book/the-book-2nd.html — Textbook covering the value and policy methods that AlphaGo combines with search.
