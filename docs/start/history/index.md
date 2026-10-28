# History of AI

## Period chapters

- [Dartmouth and the symbolic era (1956–1974)](symbolic-era/index.md): the 1956 workshop, the Logic Theorist and General Problem Solver, perceptrons and their critique, and the early language and vision programs.
- [Expert systems and the AI winters (1974–2006)](expert-systems-and-winters/index.md): the Lighthill report, MYCIN and expert systems, the Fifth Generation project, the second winter, backpropagation's revival and the statistical turn in language processing.
- [The deep learning revolution (2006–present)](deep-learning-revolution/index.md): deep belief networks, ImageNet, AlexNet, and the attention and Transformer era up to large language models, with the institutions that grew around them.

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
Intelligence = manipulating symbols. Logic, expert systems, knowledge graphs, planning. Strengths: interpretable and verifiable. Weaknesses: knowledge-acquisition bottleneck, poor handling of uncertainty and perception. See [Symbolic AI](../../theory/symbolic-ai/index.md).

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

## Further reading

- Nilsson, *The Quest for Artificial Intelligence* (free PDF on the author's site)
- Mitchell, *Artificial Intelligence: A Guide for Thinking Humans*
- Sejnowski, *The Deep Learning Revolution* (a neuroscientist's history of deep learning)
- [Wikipedia: History of artificial intelligence](https://en.wikipedia.org/wiki/History_of_artificial_intelligence)

## References

Seminal works for this overview, drawn from the sub-pages linked above, where each is discussed in detail.

- Newell, A. & Simon, H. A. (1956). The logic theory machine: A complex information processing system. *IEEE Transactions on Information Theory*. https://doi.org/10.1109/TIT.1956.1056797 — Describes the Logic Theorist, an early program that searches for proofs of logic theorems using heuristics rather than exhaustive enumeration.
- Newell, A., Shaw, J. C. & Simon, H. A. (1958). Elements of a theory of human problem solving. *Psychological Review*. https://doi.org/10.1037/h0048495 — Proposes a general theory of human problem solving as heuristic search, drawing on the Logic Theorist and the means–ends method behind the General Problem Solver.
- Shortliffe, E. H. & Buchanan, B. G. (1975). A model of inexact reasoning in medicine. *Mathematical Biosciences*. https://doi.org/10.1016/0025-5564(75)90047-4 — Presents the certainty-factor model for combining uncertain evidence, developed for the MYCIN consultation system.
- Rumelhart, D. E., Hinton, G. E. & Williams, R. J. (1986). Learning representations by back-propagating errors. *Nature*. https://doi.org/10.1038/323533a0 — Shows how error can be propagated backwards to adjust hidden units, so that a network learns its own internal features.
- Hinton, G. E., Osindero, S. & Teh, Y.-W. (2006). A fast learning algorithm for deep belief nets. *Neural Computation*. https://doi.org/10.1162/neco.2006.18.7.1527 — Introduces greedy layer-wise training of deep belief networks, the start of the revival.
- Deng, J. et al. (2009). ImageNet: A large-scale hierarchical image database. *CVPR 2009*. https://doi.org/10.1109/CVPR.2009.5206848 — Introduces the ImageNet database on which the yearly challenge is built.
