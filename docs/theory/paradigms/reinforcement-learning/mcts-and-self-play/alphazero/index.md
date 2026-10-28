---
status: draft
last_reviewed: 2026-10-28
aliases:
  - AlphaZero
  - 阿爾法零
---

# AlphaZero (Silver et al., 2017)

AlphaZero is a single self-play algorithm that learns chess, shogi and Go from the game rules alone, using one neural network and [Monte Carlo tree search](../monte-carlo-tree-search/index.md). It generalised [AlphaGo](../alphago/index.md) by removing human game records and Go-specific design, and it is the reference design for the search-and-self-play approach in the [parent topic](../index.md).

## Overview

AlphaGo needed human expert games to start its policy network and relied on features designed for Go. The question behind AlphaZero was whether the same procedure could learn several games from scratch, starting from random play and knowing only the rules. The authors answered yes for chess, shogi and Go. The arXiv abstract reports that starting from random play, given no domain knowledge except the game rules, AlphaZero reached a superhuman level of play in these games within 24 hours and convincingly defeated a world-champion program in each case.

The algorithm was later published in Science (Silver et al., 2018). Its key simplification was to merge the policy and value networks of AlphaGo into one network with two outputs, and to train that network only on data from its own games.

## Key concepts

- **Single network**: takes the board and returns a probability for each move, the policy $\mathbf{p}$, and a scalar estimate of the outcome, the value $v$.
- **Search-guided targets**: the move counts from the search form the policy target, which is usually sharper than the raw network output.
- **Outcome targets**: the final result of each self-play game, from each position's player's view, is the value target.
- **PUCT selection**: a variant of the UCT rule in which the network's prior $P(s,a)$ replaces the uniform bias.

## How it works

Each self-play game is generated as follows. At every position, MCTS runs a fixed number of simulations, using the network for priors and leaf values. The search returns visit counts for each move, and a move is sampled from them. At each simulation the selection rule is

$$
a^\ast = \arg\max_a \left( Q(s,a) + c_{\text{puct}}\, P(s,a)\, \frac{\sqrt{\sum_b N(s,b)}}{1 + N(s,a)} \right),
$$

and the network is trained so that its value output predicts the game outcome $z$ and its policy output predicts the search distribution $\boldsymbol{\pi}$. The loss has the form

$$
\ell = (z - v)^2 - \boldsymbol{\pi}^\top \log \mathbf{p} + c\,\lVert\theta\rVert^2.
$$

The training loop is:

1. Initialise the network with random weights.
2. Play a game against itself, running MCTS with the current network at every move.
3. Store each position with its search distribution $\boldsymbol{\pi}$ and the final outcome $z$.
4. Sample positions from recent games and take a gradient step on the loss.
5. Repeat. The updated network guides the next games, and the search improves with it.

Because the network that generates the games is the one being trained, the difficulty of the training data rises together with the learner, and the data and the network improve together.

## Results

According to the arXiv abstract (Silver et al., 2017), AlphaZero learned chess and shogi as well as Go from random play, and within 24 hours reached superhuman strength in each game, defeating a world-champion program in each case. The paper's comparisons are with strong programs built for each game, and the exact scores are in the paper.

## Limitations

- **Perfect information.** The method was designed for deterministic, two-player, zero-sum games with fully visible positions.
- **Known rules.** Search needs an exact simulator, so the method does not transfer directly to tasks where the rules are unknown.
- **Compute.** Self-play needs very large amounts of search and training compute, which limits who can reproduce the results.

## Open questions

Can the approach be extended to imperfect information, such as poker, or to tasks with continuous actions and unknown dynamics? [MuZero](../muzero/index.md) answers the second question by learning the model. The first remains open for this family. A further question is how to use self-play with language models, where there is no clear winner; [Feng et al. (2023)](https://arxiv.org/abs/2309.17179) adapt the AlphaZero search to language model decoding, but the reward signal is much less clean than in games.

## Connections

AlphaZero builds on expert iteration (Anthony et al., 2017), which also alternated between a tree search and a learned policy that imitates the search, and on [AlphaGo](../alphago/index.md) and its Zero variant. Its training uses the same value and policy learning as [value-based methods](../../value-based-methods/index.md) and [policy gradient methods](../../policy-gradient-and-actor-critic/index.md). Its later successor [MuZero](../muzero/index.md) drops the requirement for the rules.

## References

### Seminal papers

- Silver, D. et al. (2018). *A general reinforcement learning algorithm that masters chess, shogi, and Go through self-play*. Science. https://doi.org/10.1126/science.aar6404 — The peer-reviewed AlphaZero paper, learning three board games from the rules alone through self-play and search.
- Silver, D. et al. (2017). *Mastering Chess and Shogi by Self-Play with a General Reinforcement Learning Algorithm*. arXiv:1712.01815. https://arxiv.org/abs/1712.01815 — The preprint of AlphaZero, with the description of the single-network design and the training results.
- Silver, D. et al. (2017). *Mastering the game of Go without human knowledge*. Nature. https://doi.org/10.1038/nature24270 — AlphaGo Zero, the Go-only predecessor that removed human game records.
- Anthony, T., Tian, Z. & Barber, D. (2017). *Thinking Fast and Slow with Deep Learning and Tree Search*. arXiv:1705.08439. https://arxiv.org/abs/1705.08439 — Expert iteration, the tree-search and policy-learning loop that AlphaZero builds on.

### Articles and documentation

- Feng, X. et al. (2023). *Alphazero-like Tree-Search can Guide Large Language Model Decoding and Training*. arXiv:2309.17179. https://arxiv.org/abs/2309.17179 — Adapts an AlphaZero-style tree search with a learned value function to language model decoding and training.
