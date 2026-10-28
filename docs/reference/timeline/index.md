---
references: not-required  # lists and meta pages cite through their entries
last_reviewed: 2026-10-28
aliases:
  - 模型與發表時間軸
  - Model timeline
  - AI timeline
---

# Timeline of Models and Releases

A dated list of milestones in AI, from the perceptron to large language models. It is a starting point for placing a model in its period, not a full history. Each entry links to the source that gives its date.

## How dates are counted

A paper can be public well before it is published in a journal, so each date is the first public version of the source named in its row:

- **Preprints** use the arXiv submission date of version 1.
- **Journal articles** use the online publication date. The print issue can be later.
- **Conference papers** use the year of the conference.
- **Company releases** use the date of the announcement.

## Milestones

| Date | Milestone | Why it matters | Source |
|---|---|---|---|
| 1958 | Perceptron | Rosenblatt presents the perceptron as a probabilistic model of information storage and organisation in the brain | [Rosenblatt, *Psychological Review* 65(6)](https://doi.org/10.1037/h0042519) |
| 1986 | Backpropagation | Rumelhart, Hinton and Williams describe learning representations by back-propagating errors through multi-layer networks | [Rumelhart et al., *Nature* 323](https://doi.org/10.1038/323533a0) |
| 1998 | Convolutional networks for documents | LeCun et al. present gradient-based learning for document recognition, a convolutional approach | [LeCun et al., *Proc. IEEE* 86(11)](https://doi.org/10.1109/5.726791) |
| 2012 | AlexNet | A deep convolutional network trained on ImageNet classification | [Krizhevsky, Sutskever & Hinton, NIPS 2012](https://papers.nips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html) |
| 2013 | Word vectors | Efficient word representations learned from large text corpora | [Mikolov et al., arXiv:1301.3781](https://arxiv.org/abs/1301.3781) |
| 2014 | Sequence-to-sequence | Encoder–decoder networks translate between sequences, see [Sequence to sequence](../../theory/models/rnn/sequence-modes/sequence-to-sequence/index.md) | [Sutskever et al., arXiv:1409.3215](https://arxiv.org/abs/1409.3215) |
| 2015 | Deep Q-network | Human-level control in Atari games from raw pixels through deep reinforcement learning | [Mnih et al., *Nature* 518](https://doi.org/10.1038/nature14236) |
| 2015 | Residual networks | Skip connections make very deep networks trainable | [He et al., arXiv:1512.03385](https://arxiv.org/abs/1512.03385) |
| 2016 | AlphaGo | Deep neural networks combined with tree search play the game of Go | [Silver et al., *Nature* 529](https://doi.org/10.1038/nature16961) |
| 2017 | Transformer | Self-attention replaces recurrence, see [Attention Is All You Need](../../theory/models/transformer/attention-is-all-you-need/index.md) | [Vaswani et al., arXiv:1706.03762](https://arxiv.org/abs/1706.03762) |
| 2018 | BERT | Bidirectional pre-training of Transformer encoders for language understanding | [Devlin et al., arXiv:1810.04805](https://arxiv.org/abs/1810.04805) |
| 2020 | GPT-3 | A large language model that performs tasks from a few examples in the prompt, see [GPT-3 few-shot](../../theory/models/llm/gpt-3-few-shot/index.md) | [Brown et al., arXiv:2005.14165](https://arxiv.org/abs/2005.14165) |
| 2020 | Denoising diffusion | A generative model trained to reverse a gradual noising process | [Ho et al., arXiv:2006.11239](https://arxiv.org/abs/2006.11239) |
| 2021 | AlphaFold 2 | Highly accurate protein structure prediction from sequence | [Jumper et al., *Nature* 596](https://doi.org/10.1038/s41586-021-03819-2) |
| 2021 | Latent diffusion | Diffusion run in a compressed latent space to synthesise high-resolution images | [Rombach et al., arXiv:2112.10752](https://arxiv.org/abs/2112.10752) |
| 2022 | Compute-optimal training | Chinchilla argues that model size and training tokens should be scaled together, see [Compute-optimal training](../../theory/models/llm/compute-optimal-training/index.md) | [Hoffmann et al., arXiv:2203.15556](https://arxiv.org/abs/2203.15556) |
| 2022 | ChatGPT | A conversational model related to InstructGPT released for free public testing | [OpenAI, "Introducing ChatGPT"](https://openai.com/index/chatgpt/) |
| 2023 | GPT-4 | A large model whose technical report describes its capabilities and evaluation | [OpenAI, arXiv:2303.08774](https://arxiv.org/abs/2303.08774) |
| 2023 | Llama 2 | Open foundation and fine-tuned chat models, described in a technical report | [Touvron et al., arXiv:2307.09288](https://arxiv.org/abs/2307.09288) |

## Connections

- The model families behind these milestones are covered in [Models](../../theory/models/index.md), including [Transformer](../../theory/models/transformer/index.md), [CNN](../../theory/models/cnn/index.md), [RNN](../../theory/models/rnn/index.md) and [LLM](../../theory/models/llm/index.md).
- The people and groups behind many of these releases are in [People and Research Labs](../people-and-labs/index.md).

## Open questions

- Which milestones should be added next, and how should the timeline stay current without becoming a list of every release?
