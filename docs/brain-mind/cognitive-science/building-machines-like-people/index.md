---
status: complete
last_reviewed: 2026-10-28
---

# Building machines that learn and think like people (Lake et al., 2017)

Lake and colleagues argue that human-like learning machines need causal models of the world, intuitive theories of physics and psychology, and compositional learning-to-learn, not pattern recognition alone.

## Overview

Deep neural networks trained end to end now match or beat people on some tasks, such as object recognition, video games and board games. Yet they learn in ways that differ from human learning. A person can often learn a new handwritten character from a single example, use it in new ways and explain what it is. A typical network needs far more labelled examples to reach a similar level. Lake, Ullman, Tenenbaum and Gershman (2017) review cognitive science evidence for these differences and propose three ingredients that a human-like learner would need.

The article is a target article in *Behavioral and Brain Sciences*, a journal format that prints a paper together with peer commentary. It is a position piece. It sets out an agenda and a worked example, but it does not introduce a new benchmark result.

## Key concepts

- **Causal model**: an internal account of how events are produced. It supports explanation and prediction beyond the patterns seen in the data.
- **Intuitive theory**: a compact set of expectations about objects (intuitive physics) and about agents (intuitive psychology). People use these to make sense of new situations.
- **Compositionality**: building new concepts from parts that have already been learned, and recombining them in new ways.
- **Learning to learn**: acquiring shared structure from many earlier tasks, so that a new task needs fewer examples. This is closely tied to the idea of an [inductive bias](../../../reference/glossary/index.md), an assumption built into a learner before it sees the data.
- **Bayesian program learning**: a model in which a concept is a short probabilistic program, and learning means inferring which program best explains the examples (Lake, Salakhutdinov and Tenenbaum, 2015).

## Problem

Why do deep networks need far more data than people do, and how do they differ from people in what they learn and how they learn it? The authors frame the gap as one of learning goals and learning methods. Networks learn to classify patterns, while people build explanations. Networks start with little structure, while people bring intuitive theories to each new problem.

## Core idea

The authors propose three ingredients, which they say are needed to reach truly human-like learning:

1. **Causal models of the world.** A learner should build models that support explanation and understanding, rather than only solving pattern recognition problems.
2. **Intuitive theories.** Learning should be grounded in intuitive theories of physics and psychology, which support and enrich what is learned.
3. **Compositionality and learning-to-learn.** Concepts should be built from reusable parts, and prior experience should be used to acquire and generalise new knowledge quickly.

The three ingredients are not separate proposals. The authors suggest concrete routes that combine the strengths of recent neural network advances, such as flexible perception and large-scale training, with more structured cognitive models.

## Equation or algorithm

The article has no single governing equation. Its main worked example is Bayesian Program Learning (BPL), developed by Lake, Salakhutdinov and Tenenbaum (2015) for handwritten characters. The preprint describes its generative process, the steps by which the model would produce a new character:

1. Choose primitive pen actions from a library of primitives.
2. Combine primitives into sub-parts.
3. Combine sub-parts into parts.
4. Combine parts with spatial relations, such as "attached at start", into an object template. The template is a short program.
5. Run the program to produce exemplars, which are different tokens of the same concept.
6. Render each token as a binary image.

Learning runs this process in reverse. Given one image, the model considers candidate programs and scores each one with Bayes' rule:

$$P(\theta \mid D) \propto P(D \mid \theta)\, P(\theta)$$

Here $D$ is the observed image, $\theta$ is a candidate program, $P(\theta)$ is the prior that encodes which programs are plausible, and $P(D \mid \theta)$ is how likely the program is to produce the image. The equation is the general form of Bayes' rule, the standard way to update beliefs. It is not a formula printed in the article.

## Results

The target article reports no new benchmark. Its support comes from its review of cognitive science experiments and from the BPL work. The 2015 *Science* paper summarised in the article reports that the BPL model classifies, parses and recreates handwritten characters. It also reports that the model learns better than current deep learning algorithms on this task, and that the characters it generates pass Turing-like tests against human output. The text read for this page gives no accuracy figures for the one-shot comparison, so none are quoted here.

## Limitations

As a position piece, the article names challenges and routes rather than testing them across many tasks. Its claims rest on a review of existing experiments and on one structured model applied to a narrow domain of simple drawn characters. The article proposes combining neural networks with structured models, but it does not show that combination at scale.

The article also leaves open how much built-in structure a machine needs. Progress in large neural networks since 2017 has made this an active question, and the article does not settle it. Readers should treat its three ingredients as a research programme with supporting evidence, not as a proven recipe.

## Key methods

A brief comparison of the approaches the article contrasts:

- [Deep neural networks](../../../theory/deep-learning/index.md): learn features end to end from large labelled datasets. They are strong at perception, but the article argues that they need far more data than people and lack explicit causal structure.
- Bayesian Program Learning (Lake et al., 2015): represents concepts as short probabilistic programs and learns from one example. It works in a narrow domain, and it is the authors' own worked example, not a general method.
- [ACT-R](../../cognitive-architectures/act-r/index.md): a cognitive architecture, an integrated theory of the mind's structure. It models the mind as a whole rather than as a learning algorithm for machines.
- [Predictive coding](../../predictive-coding/index.md): a brain theory in which cortex transmits prediction errors. It offers a neural account of inference that the causal-model ingredient can be compared with.

## Connections

- Parent topic: [Cognitive Science](../index.md)
- Companion page: [Heuristics and Biases](../heuristics-and-biases/index.md) describes how people reason under uncertainty with fast shortcuts, the kind of behaviour that a human-like machine would also need to explain.
- [Cognitive Architectures](../../cognitive-architectures/index.md) covers the integrated models of the mind that the article's ideas are compared with.
- [Predictive Coding](../../predictive-coding/index.md) is a brain-side account of inference with generative models, close to the causal-model ingredient.
- [Psychology](../../psychology/index.md) gives the wider empirical background for intuitive theories and reasoning.
- Theory side: [Probabilistic Methods](../../../theory/paradigms/probabilistic/index.md) describes the Bayesian inference used in the worked example, and [Deep Learning](../../../theory/deep-learning/index.md) describes the networks the article critiques.

## Applications

- **Learning from few examples.** The BPL model classifies and generates handwritten characters from one example (Lake et al., 2015). The same generative recipe, composing parts into programs, is a template for other symbolic domains.
- **Hybrid systems.** The article's suggested routes pair neural perception with structured models, a design that can be used when a system needs to explain its answers or learn from little data.
- **Benchmarks for human-like learning.** The article argues for tests that check explanation and generalisation, not only accuracy on large datasets. Such tests are a practical application of its agenda.

## Open questions

- How much built-in structure does a learning machine need, and which parts of it can be learned rather than designed by hand?
- Which intuitive theories, such as those of physics or other people's goals, should a machine start with, and how can they be acquired?
- Can compositional, program-like representations be learned by neural networks at large scale?
- How should "human-like" learning be measured, so that tests reward explanation and transfer rather than matching a dataset?

## References

### Seminal papers

- Lake, B. M., Ullman, T. D., Tenenbaum, J. B. & Gershman, S. J. (2017). Building machines that learn and think like people. *Behavioral and Brain Sciences*. https://doi.org/10.1017/S0140525X16001837 — The target article, arguing for causal models, intuitive theories and compositionality with learning-to-learn as ingredients of human-like learning.
- Lake, B. M., Salakhutdinov, R. & Tenenbaum, J. B. (2015). Human-level concept learning through probabilistic program induction. *Science*. https://doi.org/10.1126/science.aab3050 — Bayesian Program Learning for handwritten characters, which classifies, parses and generates new characters and outperforms deep learning algorithms on the task.
- Lake, B. M., Ullman, T. D., Tenenbaum, J. B. & Gershman, S. J. (2016). Building machines that learn and think like people. arXiv preprint. https://arxiv.org/abs/1604.00289 — Preprint version of the 2017 article, which includes the figure describing the generative steps of the character model.

### Surveys and textbooks

- Tenenbaum, J. B., Kemp, C., Griffiths, T. L. & Goodman, N. D. (2011). How to Grow a Mind: Statistics, Structure, and Abstraction. *Science*. https://doi.org/10.1126/science.1192788 — Reviews probabilistic models over structured representations, the framework that the article's proposals build on.
- Hassabis, D., Kumaran, D., Summerfield, C. & Botvinick, M. (2017). Neuroscience-Inspired Artificial Intelligence. *Neuron*. https://doi.org/10.1016/j.neuron.2017.06.011 — Review of how neuroscience has inspired AI, covering attention, episodic memory, and imagination and planning.
