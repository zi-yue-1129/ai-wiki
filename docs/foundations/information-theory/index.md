---
status: draft
last_reviewed: 2026-10-27
related:
  - brain-mind/neuroai
  - models/generative
tags:
  - information theory
  - entropy
  - loss functions
  - neural coding
---

# Information Theory

Information theory, founded by Claude Shannon in 1948, gives a precise measure of how much uncertainty a random variable carries and how much one variable tells us about another. Its quantities (entropy, cross-entropy, KL divergence and mutual information) sit underneath most machine-learning loss functions and many hypotheses about how brains encode the world.

## Overview

Shannon asked a practical question: how many bits are needed to send a message reliably over a noisy channel? His answer separated two limits. Lossless compression cannot go below the entropy of the source, and reliable transmission cannot exceed the capacity of the channel, which is itself defined as a maximum of mutual information.

The same definitions matter far beyond telephone lines. A model that predicts data well is, in effect, a compressor, and a learner must decide which information to keep and which to discard. Information theory gives both of these ideas a common language. For the probability background these definitions rely on, see [Mathematics](../math/index.md) and [Probabilistic & Bayesian Methods](../probabilistic/index.md).

## Key concepts

- **Entropy** \(H(X) = -\sum_x p(x)\log p(x)\): the average surprise of the outcomes of \(X\). With base-2 logarithms it is measured in bits.
- **Cross-entropy** \(H(p,q) = -\sum_x p(x)\log q(x)\): the average code length when outcomes that actually follow \(p\) are encoded with a code designed for \(q\).
- **KL divergence** \(D_{\mathrm{KL}}(p\,\|\,q) = \sum_x p(x)\log\frac{p(x)}{q(x)}\): the extra cost of using \(q\) in place of \(p\). It is never negative, is zero only when the two distributions are equal, and is not symmetric.
- **Mutual information** \(I(X;Y) = H(X) - H(X\mid Y)\): how much learning \(Y\) reduces the uncertainty about \(X\). It is zero exactly when \(X\) and \(Y\) are independent.
- **Channel capacity**: the largest mutual information that a channel can carry, found by choosing the best input distribution.

Two identities tie these together. Cross-entropy splits into entropy plus KL divergence:

\[
H(p,q) = H(p) + D_{\mathrm{KL}}(p\,\|\,q)
\]

Because \(H(p)\) does not depend on the model \(q\), minimising cross-entropy against the data is the same as minimising the KL divergence between the data and the model.

## How it works

**Compression.** A fair coin needs one bit per toss. A coin that lands heads 90% of the time has entropy of about 0.47 bits, so an ideal code can average under half a bit per toss by giving frequent outcomes short codewords. Compression works by exploiting predictability: the better a model knows the data, the lower the entropy it can reach. This is why *perplexity*, the exponential of the average cross-entropy, is the standard measure for [language models](../../models/llm/index.md). It can be read as the effective number of equally likely choices the model still weighs at each step.

**Noisy channels.** For a binary symmetric channel that flips each bit with probability \(p\), the capacity is \(C = 1 - H(p)\). Shannon's channel coding theorem shows that any rate below \(C\) can be achieved with arbitrarily small error. This result is the theoretical basis for error-correcting codes.

**Learning as coding.** A classifier trained with cross-entropy loss is a maximum-likelihood estimator for categorical outputs. Minimising the average \(-\log q_\theta(y\mid x)\) over the training set is the same as minimising the KL divergence between the empirical data distribution and the model. The loss is explained in more detail on the [loss functions page](../paradigms/supervised/loss-functions-and-optimization/index.md).

Variational autoencoders use the same ideas. Their training objective has a reconstruction term and a KL term that keeps the learned latent distribution close to a simple prior, which is why they appear in the [generative models](../../models/generative/index.md) section.

**The information bottleneck.** Tishby, Pereira and Bialek (2000) framed representation learning as a trade-off. Compress an input \(X\) into a representation \(T\) that keeps as much information as possible about a target \(Y\). Formally, one minimises \(I(X;T) - \beta\, I(T;Y)\), where \(\beta\) sets how much predictive power is worth compared with compression. Alemi and colleagues (2016) made this objective trainable with neural networks by replacing the intractable terms with variational bounds. They reported better generalisation and better resistance to adversarial attacks than some standard regularisers.

The theory is not settled. Saxe and colleagues (2019) argued that some of its central claims about deep networks do not hold in general. In their experiments, the compression they observed depended mainly on which neural nonlinearity was used.

## Connections

**Brain and mind.** Information theory entered neuroscience early. Barlow (1961) proposed that sensory systems should reduce redundancy in their input, so that a limited number of neurons carries as much information as possible. This is the *efficient coding hypothesis*. Linsker (1988) proposed the *infomax* principle: layers of a model of perceptual processing can organise themselves by maximising the information they preserve about their input. Both ideas form a bridge to [NeuroAI](../../brain-mind/neuroai/index.md). If the brain is an efficient coder, objectives such as the information bottleneck or prediction-based self-supervision may help explain why its representations look the way they do.

The hypothesis is contested. Efficiency may be shaped by metabolic or other constraints that Barlow's account does not include, and estimating information from limited neural recordings is difficult.

**Other foundations.** Mutual information underlies the feature-selection and representation ideas discussed in [Unsupervised Learning](../paradigms/unsupervised/index.md) and [Self-Supervised Learning](../paradigms/self-supervised/index.md). The [Deep Learning](../deep-learning/index.md) page covers how the losses built from these quantities are optimised.

## Applications

- **Data compression and communication.** The bit is the unit of information, and compression and error-correcting codes in everyday devices rest on Shannon's limits.
- **Machine learning losses.** Cross-entropy trains classifiers and language models. KL divergence appears in variational models and in penalties that keep a fine-tuned model close to a reference model.
- **Model evaluation.** Perplexity, the exponential of cross-entropy, is used to compare language models.
- **Representation learning.** Mutual information is a criterion for asking whether a learned representation keeps information about a target, or whether it wastes capacity on irrelevant detail.

## Open questions

- Estimating mutual information in high dimensions is hard. Sample-based estimators are often biased, which makes claims about deep networks difficult to test.
- Does the information bottleneck explain how deep networks train? The Saxe et al. (2019) result suggests the answer depends on details such as the nonlinearity.
- Is the brain an efficient coder in Barlow's sense, and if so, which quantity does it optimise?

## References

### Seminal papers

- Shannon, C. E. (1948). *A Mathematical Theory of Communication*. Bell System Technical Journal, 27, 379–423 and 623–656. https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf — The founding paper: entropy as a measure of information, and the limits of compression and reliable communication. This is a hosted reprint.
- Linsker, R. (1988). Self-organization in a perceptual network. *Computer*, 21(3), 105–117. https://doi.org/10.1109/2.36 — Introduces the infomax principle, a layered model that organises itself by preserving information about its input.
- Barlow, H. B. (1961). Possible principles underlying the transformations of sensory messages. In *Sensory Communication*, pp. 217–234. https://mlanthology.org/misc/1961/barlow1961misc-possible — Proposes that sensory processing reduces redundancy. It is the origin of the efficient coding hypothesis.
- Tishby, N., Pereira, F. C. & Bialek, W. (2000). The information bottleneck method. arXiv:physics/0004057. https://arxiv.org/abs/physics/0004057 — Defines relevant information and derives the trade-off between compressing an input and predicting a target.
- Alemi, A. A., Fischer, I., Dillon, J. V. & Murphy, K. (2016). Deep variational information bottleneck. arXiv:1612.00410. https://arxiv.org/abs/1612.00410 — Makes the information bottleneck trainable with neural networks and reports better generalisation and adversarial robustness than some standard regularisers.
- Saxe, A. M., Bansal, Y., Dapello, J., Advani, M., Kolchinsky, A., Tracey, B. D. & Cox, D. (2019). On the information bottleneck theory of deep learning. *Journal of Statistical Mechanics*. https://research.ibm.com/publications/on-the-information-bottleneck-theory-of-deep-learning — Argues that central compression claims about deep networks do not hold in general, and that the compression observed depends mainly on the nonlinearity.

### Surveys and textbooks

- MacKay, D. J. C. (2003). *Information Theory, Inference, and Learning Algorithms*. Cambridge University Press. https://www.cambridge.org/0521642981 — A textbook that treats information theory together with Bayesian inference and learning algorithms.
- Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep Learning*. MIT Press. https://www.deeplearningbook.org/ — Chapter 3, "Probability and Information Theory", introduces entropy, KL divergence and cross-entropy in a deep-learning setting. The full text is free online.

### Lectures and videos

- Polyanskiy, Y. (instructor). *6.441 Information Theory*. MIT OpenCourseWare, Spring 2016. https://ocw.mit.edu/courses/6-441-information-theory-spring-2016/ — A graduate course from first principles. The course page provides lecture notes and problem sets; it lists no video lectures.

### Articles and documentation

- *Visual Information Theory*. colah's blog (2015). https://colah.github.io/posts/2015-09-Visual-Information/ — A diagram-based introduction to entropy, cross-entropy, KL divergence and mutual information.
