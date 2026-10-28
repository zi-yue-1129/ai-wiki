# History of AI

## Timeline

| Year | Event | Significance |
|---|---|---|
| 1943 | McCulloch & Pitts formal neuron | First mathematical model of a neuron as a logic unit — where neuroscience met computation |
| 1949 | Hebb, *The Organization of Behavior* | "Cells that fire together wire together": the biological root of learning rules |
| 1950 | Turing, "Computing Machinery and Intelligence" | The imitation game (Turing test) |
| 1956 | Dartmouth workshop | McCarthy and colleagues coin "artificial intelligence" |
| 1957–58 | Rosenblatt's perceptron | First learning neural network in hardware |
| 1959 | Samuel's checkers program | Popularises "machine learning" |
| 1959 | Hubel & Wiesel find simple and complex cells in cat visual cortex | Later inspires the Neocognitron and CNNs |
| 1966 | ELIZA | Early chatbot; reveals how readily people anthropomorphise machines (the ELIZA effect) |
| 1969 | Minsky & Papert, *Perceptrons* | Limits of single-layer perceptrons; neural-net research cools |
| 1970s | First AI winter | Funding cuts after the Lighthill report |
| 1972 | Prolog | Logic programming |
| 1970s–80s | Expert systems (MYCIN, XCON) | Knowledge engineering goes commercial |
| 1980 | Fukushima's Neocognitron | Hierarchical vision model, CNN precursor |
| 1982 | Hopfield networks | Associative memory as energy minimisation (Nobel Prize in Physics 2024) |
| 1986 | Rumelhart, Hinton & Williams popularise backpropagation | Multi-layer networks become trainable |
| 1986 | *Parallel Distributed Processing* volumes | Connectionism's landmark in cognitive science |
| 1987–93 | Second AI winter | Expert-system market collapses |
| 1988 | Pearl, *Probabilistic Reasoning in Intelligent Systems* | Bayesian networks |
| 1989 | LeCun applies CNNs to handwritten digits | LeNet |
| 1992 | TD-Gammon | Temporal-difference learning plus a neural net plays backgammon |
| 1995 | Support vector machines (Cortes & Vapnik) | Kernel methods dominate |
| 1997 | Deep Blue beats Kasparov; LSTM published | Peak of search-based AI; key to sequence learning |
| 1997 | Schultz, Dayan & Montague | Dopamine neurons encode reward prediction error — matching TD learning |
| 2006 | Hinton's deep belief networks | "Deep learning" revival |
| 2009 | ImageNet | Large-scale labelled data |
| 2011 | IBM Watson wins *Jeopardy!*; Siri | |
| 2012 | AlexNet wins ImageNet | GPUs + big data + deep CNNs: the deep learning era begins |
| 2013 | word2vec; DQN plays Atari | Word embeddings; deep RL |
| 2014 | GANs; seq2seq; attention (Bahdanau) | Generative models and neural machine translation |
| 2014–15 | Yamins, DiCarlo et al. show CNNs predict primate visual cortex; ResNet | NeuroAI takes off; very deep networks |
| 2016 | AlphaGo beats Lee Sedol | Deep RL + Monte Carlo tree search |
| 2017 | Transformer, "Attention Is All You Need" | Architecture of modern LLMs |
| 2018 | BERT, GPT; Turing Award to Hinton, LeCun, Bengio | Pre-train then fine-tune |
| 2020 | GPT-3; AlphaFold 2 at CASP14; scaling laws | In-context learning; protein structure prediction |
| 2021 | CLIP, DALL·E; Codex | Multimodal models and code generation |
| 2022 | Stable Diffusion; ChatGPT (November) | Generative AI goes mainstream |
| 2023 | GPT-4, Claude, Llama, Gemini | Multiple frontier labs and open-weight models |
| 2024 | Nobel Prizes: Physics (Hopfield, Hinton), Chemistry (Baker, Hassabis, Jumper); reasoning models (o1); EU AI Act adopted | AI recognised by science's top prizes; test-time compute |
| 2025 | Reasoning models spread, including open-weight ones (e.g. DeepSeek-R1); coding and research agents; tool protocols such as MCP | From chat to agents |
| 2026 | Long-horizon autonomous agents, multi-agent systems, AI-assisted scientific discovery continue to advance | See individual pages |

## Three schools of thought

### Symbolism
Intelligence = manipulating symbols. Logic, expert systems, knowledge graphs, planning. Strengths: interpretable and verifiable. Weaknesses: knowledge-acquisition bottleneck, poor handling of uncertainty and perception. See [Symbolic AI](../../theory/paradigms/symbolic-ai/index.md).

### Connectionism
Intelligence emerges from many simple connected units. Neural networks and deep learning, directly inspired by neuroscience. See [NeuroAI](../../brain-mind/neuroai/index.md).

### Behaviourism / cybernetics / evolution
Intelligence arises from interaction with an environment. Reinforcement learning, control theory, embodied AI, evolutionary computation — closely tied to behaviourist psychology (Skinner) and animal-learning research.

The modern trend is **integration**: neural networks for perception and intuition; search, tools and code for precise reasoning (neuro-symbolic AI, LLMs with tools, AlphaGo's networks plus tree search).

## Lessons of the AI winters

1. **Over-promising**: in the 1960s researchers predicted machines would do any human work within 20 years.
2. **Combinatorial explosion**: symbolic methods failed at real-world scale.
3. **Not enough data or compute**: the core neural-net ideas existed in the 1980s; they took off only with GPUs and web-scale data in the 2010s.
4. **Takeaway**: keep benchmarks and real-world capability separate; a benchmark score is not deployment reliability (see [Evaluation](../../engineering/evaluation/index.md)).

## References

- McCulloch & Pitts (1943). A logical calculus of the ideas immanent in nervous activity. *Bulletin of Mathematical Biophysics* 5. https://doi.org/10.1007/bf02478259 — The first mathematical model of a neuron as a logic unit.
- Turing (1950). Computing Machinery and Intelligence. *Mind* 59. https://doi.org/10.1093/mind/lix.236.433 — Proposes the imitation game, later called the Turing test.
- Rumelhart, Hinton & Williams (1986). Learning representations by back-propagating errors. *Nature* 323. https://doi.org/10.1038/323533a0 — Popularises backpropagation for training multi-layer networks.
- LeCun, Bengio & Hinton (2015). Deep learning. *Nature* 521. https://doi.org/10.1038/nature14539 — A review of deep learning: representation learning with several processing layers.
- Nilsson, N. J. (2009). *The Quest for Artificial Intelligence*. Cambridge University Press. https://doi.org/10.1017/cbo9780511819346 — A history of AI's ideas and achievements, written by a Stanford AI researcher.
- Mitchell, M. (2019). *Artificial Intelligence: A Guide for Thinking Humans*. Farrar, Straus and Giroux. https://melaniemitchell.me/aibook/ — An accessible tour of what current AI can and cannot do, with its history.
- Sejnowski, T. J. (2018). *The Deep Learning Revolution*. MIT Press. https://doi.org/10.7551/mitpress/11474.001.0001 — A neuroscientist's history of deep learning and its links to the brain.

## Further learning

- [Wikipedia: History of artificial intelligence](https://en.wikipedia.org/wiki/History_of_artificial_intelligence) — An encyclopedia overview to read alongside the books above.
