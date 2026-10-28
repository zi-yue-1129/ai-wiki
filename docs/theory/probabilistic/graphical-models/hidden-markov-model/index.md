---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/speech
  - theory/models/ssm
tags:
  - sequence modelling
  - state-space models
  - uncertainty
aliases:
  - 隱馬可夫模型
  - 隱藏馬可夫模型
  - HMM
  - Hidden Markov model
---

# Hidden Markov Model

A hidden Markov model (HMM) is a latent-variable model for sequences. A hidden state changes over time as a Markov chain, and each state emits an observation. It is the simplest directed graphical model for sequences, and one of the methods behind the [Probabilistic Graphical Models](../index.md) overview.

## Overview

Many signals are sequences produced by a process that is not directly visible, such as speech produced by a changing vocal tract. An HMM describes such a process with a transition rule for how the hidden state changes and an emission rule for what each state produces. The states are never observed, so the model is fitted and used through the observations alone.

Baum and colleagues (1970) gave the estimation procedure, later called Baum–Welch, and Rabiner's tutorial (1989) made the model widely known. HMMs became the dominant approach to speech recognition, and Gales and Young (2008) describe how the basic model was refined into large-vocabulary systems. Because an HMM is a Bayesian network on a chain, its algorithms are special cases of the general methods on the [topic page](../index.md).

## Key concepts

- **Hidden state** \(z_t\): the unobserved condition at time \(t\), taking one of \(K\) discrete values.
- **Observation** \(x_t\): what is seen at time \(t\). Emissions can be discrete symbols or continuous densities.
- **Transition matrix** \(A\), with \(a_{ij} = p(z_t = j \mid z_{t-1} = i)\), and **initial distribution** \(\pi\).
- **Emission distribution** \(b_j(x) = p(x \mid z = j)\).
- **Three problems** (Rabiner, 1989): evaluation, which computes the likelihood of a sequence; decoding, which finds the most likely hidden path; and learning, which estimates the parameters.

## How it works

For a sequence of length \(T\), the joint distribution of states and observations is a chain-structured product:

\[
p(z_{1:T}, x_{1:T}) = \pi(z_1)\,b_{z_1}(x_1)\prod_{t=2}^{T} a_{z_{t-1} z_t}\, b_{z_t}(x_t).
\]

**Evaluation** uses the forward algorithm, with \(\alpha_t(j) = p(x_{1:t}, z_t = j)\):

1. Set \(\alpha_1(j) = \pi_j\, b_j(x_1)\).
2. For each later step, compute \(\alpha_t(j) = b_j(x_t)\sum_i \alpha_{t-1}(i)\, a_{ij}\).
3. The likelihood is \(\sum_j \alpha_T(j)\). Both steps cost \(O(K^2 T)\).

**Decoding** uses the Viterbi algorithm. It replaces the sum over previous states with a maximum, tracks back-pointers, and traces back from the best final state.

**Learning** uses Baum–Welch, an instance of expectation–maximisation. The E step runs forward and backward passes to get the posterior over states and transitions. The M step re-estimates \(\pi\), \(A\) and the emission parameters from these expectations. The procedure converges to a local optimum that depends on its starting values.

## Results

Rabiner's tutorial has no benchmark of its own. Gales and Young (2008) report that HMM-based large-vocabulary continuous speech recognition systems were the basis of almost all such systems at the time of their review. Their case study applies these systems to broadcast news and conversational speech, and it shows how much engineering, such as discriminative parameter estimation and adaptation, was needed for state-of-the-art accuracy.

## Limitations

- **Short memory.** The next state depends only on the current one. Longer-range structure must be encoded in a larger state space, which grows quickly.
- **Conditional independence of observations.** Each observation depends only on its current state, so correlations between neighbouring observations need extra modelling.
- **Generative training.** Maximum likelihood fits the joint distribution, even when the task is only to predict labels. Discriminative alternatives were developed for this reason, for example the perceptron-style training of Collins (2002), which reports gains over a maximum-entropy tagger on part-of-speech tagging and chunking.
- **Local optima.** EM training depends on its starting values.

## Open questions

- Can the number of states and the transition structure be learned from data, instead of being fixed by hand?
- How much of the success of HMM systems came from the Markov structure, and how much from the engineering around it? Neural sequence models now replace much of this structure, and the comparison is not yet settled.
- Factorial HMMs (Ghahramani & Jordan, 1997) model several interacting hidden chains. How far can such structure be learned automatically?

## References

### Seminal papers

- Rabiner, L. R. (1989). A tutorial on hidden Markov models and selected applications in speech recognition. *Proceedings of the IEEE*. https://doi.org/10.1109/5.18626 — Tutorial that defines the evaluation, decoding and learning problems for HMMs and gives the forward, Viterbi and Baum–Welch algorithms.
- Baum, L. E., Petrie, T., Soules, G. & Weiss, N. (1970). A Maximization Technique Occurring in the Statistical Analysis of Probabilistic Functions of Markov Chains. *The Annals of Mathematical Statistics*. https://doi.org/10.1214/aoms/1177697196 — Introduces the estimation procedure for probabilistic functions of Markov chains that is now called Baum–Welch.
- Viterbi, A. (1967). Error bounds for convolutional codes and an asymptotically optimum decoding algorithm. *IEEE Transactions on Information Theory*. https://doi.org/10.1109/TIT.1967.1054010 — Introduces the decoding algorithm for convolutional codes that is now used to find the best hidden path in an HMM.

### Surveys and textbooks

- Gales, M. & Young, S. (2008). *The Application of Hidden Markov Models in Speech Recognition*. Foundations and Trends in Signal Processing. https://doi.org/10.1561/2000000004 — Review of HMM-based large-vocabulary speech recognition and the refinements needed for state-of-the-art accuracy.

### Articles and documentation

- Ghahramani, Z. & Jordan, M. I. (1997). Factorial Hidden Markov Models. *Machine Learning*. https://doi.org/10.1023/A:1007425814087 — Extends the HMM to several hidden chains that evolve in parallel and interact through the observations.
- Collins, M. (2002). Discriminative Training Methods for Hidden Markov Models: Theory and Experiments with Perceptron Algorithms. *EMNLP 2002*. https://aclanthology.org/W02-1001/ — Trains tagging models with Viterbi-decoded perceptron updates and compares them with a maximum-entropy tagger.
