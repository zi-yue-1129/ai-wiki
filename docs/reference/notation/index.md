---
references: not-required  # lists and meta pages cite through their entries
last_reviewed: 2026-10-28
tags:
  - deep learning
  - reinforcement learning
  - generative models
aliases:
  - 符號與記號
  - 數學符號
  - Notation
  - Symbols
---

# Notation and Symbols

The mathematical symbols used across this wiki, so that a reader can tell what a letter stands for on any page. The tables cover vectors and matrices, probability and expectation, losses and gradients, reinforcement learning and generative models, and they mark the letters that carry more than one meaning.

## Overview

The wiki covers mathematics, machine learning, neuroscience and applications, and its pages are written by different authors. Most pages introduce their own symbols at first use and follow common conventions, such as $\theta$ for model parameters, $\mathcal{L}$ for a loss and $\gamma$ for a discount factor. This page records those conventions and the places where a letter is used in more than one sense.

It is a reading aid, not a standard. A page that follows a specific paper closely defines that paper's symbols in its own text, and the tables below describe what a reader will usually find.

A survey of the mathematics in the English pages, made while writing this page, gives a sense of which symbols are common. The most frequent is $\theta$, which appears in the mathematics of 66 pages, followed by $\sigma$ (38 pages), $\lambda$ (23 pages), and $\pi$, $\gamma$ and $\eta$ (22 pages each). The counts are rough, because one page can use a symbol in several roles.

## Key concepts

- **Scalar, vector, matrix**: a scalar is a single number, a vector is an ordered list of numbers, and a matrix is a two-dimensional array. Scalars are italic, matrices are capitals, and vectors are lower case, written either bold or plain depending on the page.
- **Subscripts and superscripts**: a subscript usually indexes something that varies, such as time $t$ or unit $i$. A superscript usually names a variant, such as the policy in $Q^\pi$, or the transpose in $A^\top$.
- **Conditioning and sampling**: $p(x \mid \theta)$ is the probability of $x$ given $\theta$, and $x \sim p$ means that $x$ is drawn from the distribution $p$.
- **Symbol overloading**: one letter with two or more meanings. It is common in mathematics and the main source of confusion across pages, so the last table lists the cases in this wiki.
- **Logarithm**: unless a page says otherwise, $\log$ with no base is the natural logarithm. A page that reports bits states base 2, as the [PixelCNN](../../theory/paradigms/unsupervised/density-and-generative-models/autoregressive/pixelcnn/index.md) page does.

## Vectors, matrices and tensors

| Object | Convention | Example | Where it appears |
|---|---|---|---|
| Scalar | Lower-case italic letter; Greek letters for many coefficients | $\eta$, $\gamma$, $\lambda$ | Almost every page |
| Vector | Lower case. Bold $\mathbf{x}$ on the computer-vision and multi-agent pages; plain italic $x$ on the [linear algebra](../../theory/math/linear-algebra/index.md) overview | $x \in \mathbb{R}^d$ | [Deformable convolution](../../theory/models/cnn/convolution-variants/deformable-convolution/index.md) |
| Matrix | Capital letter. Weights are $W$; a data matrix is $X$ with one row per example | $X \in \mathbb{R}^{n\times d}$ | [PCA](../../theory/math/linear-algebra/pca/index.md) |
| Transpose and inner product | $A^\top$ for the transpose (the form $A^{T}$ is not used); $a^\top b$ for a dot product | $\cos\theta = \frac{a^\top b}{\lVert a\rVert\,\lVert b\rVert}$ | [Linear algebra](../../theory/math/linear-algebra/index.md) |
| Norms | $\lVert\cdot\rVert$ with a subscript for the type | $\lVert x\rVert_2$, $\lVert M\rVert_F$ | [Linear algebra](../../theory/math/linear-algebra/index.md) |
| Elementwise product | $\odot$ | $\sigma(W_g x)\odot \tanh(W_f x)$ | [GRU](../../theory/models/rnn/gated-cells/gru/index.md) |
| Eigenvalues and singular values | $Av=\lambda v$; $A = U\Sigma V^\top$ with singular values $\sigma_i$ | $A_k = U_k \Sigma_k V_k^\top$ | [Truncated SVD](../../theory/math/linear-algebra/truncated-svd/index.md) |
| Special matrices and vectors | $I$ for the identity, $\mathbf{0}$ for zeros, $\mathbf{1}$ for ones | $\mathcal{N}(0, I)$ | [Probability and statistics](../../theory/math/probability-statistics/index.md) |
| Indicator | $\mathbb{1}[\cdot]$ is 1 when the condition holds and 0 otherwise | $\mathbb{1}[y_i = k]$ | [Probability and statistics](../../theory/math/probability-statistics/index.md) |

## Probability, expectation and information

| Quantity | Convention | Example | Where it appears |
|---|---|---|---|
| Density or mass | $p(\cdot)$ for a data or model distribution; $p_\theta$ for a model with parameters $\theta$; $q$ for an approximation | $p_\theta(x)$ | [Probabilistic methods](../../theory/paradigms/probabilistic/index.md) |
| Conditional | A vertical bar written as `\mid`, with spacing | $p(x \mid \theta)$ | [Maximum likelihood](../../theory/math/probability-statistics/maximum-likelihood/index.md) |
| Sampling | $x \sim p$; a Gaussian is $\mathcal{N}(\mu, \sigma^2)$ | $\varepsilon \sim \mathcal{N}(0, I)$ | [VAE](../../theory/paradigms/unsupervised/density-and-generative-models/vae/index.md) |
| Expectation | $\mathbb{E}_{x\sim p}[f(x)]$. The subscript names the distribution and is dropped when it is clear | $\mathbb{E}_\pi[G_t \mid s_t = s]$ | [Probability and statistics](../../theory/math/probability-statistics/index.md) |
| Variance | $\mathrm{Var}(X)$; a covariance matrix is $C$ or $\Sigma$, see the overlaps table | $\mathrm{Var}(X)$ | [Probability and statistics](../../theory/math/probability-statistics/index.md) |
| Likelihood | $L(\theta)$ for the likelihood; $\ell(\theta)$ for the log-likelihood; $\arg\max$ for the maximiser | $\ell(\theta) = \sum_i \log p(x_i \mid \theta)$ | [Maximum likelihood](../../theory/math/probability-statistics/maximum-likelihood/index.md) |
| Prior and posterior | $p(\theta)$ for the prior; $p(\theta \mid \mathcal{D})$ for the posterior | $p(y \mid x, \mathcal{D})$ | [Uncertainty and calibration](../../theory/machine-learning/uncertainty-and-calibration/index.md) |
| Entropy | $H(p)$ for entropy, and $H(p,q)$ for cross-entropy | $H(p,q) = H(p) + D_{\mathrm{KL}}(p \Vert q)$ | [Information theory](../../theory/information-theory/index.md) |
| Divergence | $D_{\mathrm{KL}}(p \Vert q)$ on the information-theory page; $\mathrm{KL}(q \Vert p)$ on the VAE and variational-inference pages | $\mathrm{KL}(q_\phi(z \mid x) \,\Vert\, p(z))$ | [Information theory](../../theory/information-theory/index.md) |

The two forms of the KL divergence name the same quantity. The information-theory page writes the subscript as $D_{\mathrm{KL}}$, while the variational pages write $\mathrm{KL}$ followed by the two distributions in brackets.

## Losses, gradients and parameters

| Quantity | Convention | Example | Where it appears |
|---|---|---|---|
| Parameters | $\theta$ for the parameters of a model; $\phi$ for a second set, usually an encoder; $\theta^{-}$ for a frozen target network | $Q(s, a; \theta)$ | [Deep Q-networks](../../theory/paradigms/reinforcement-learning/deep-q-networks/index.md) |
| Model and prediction | $f_\theta$ maps an input to an output; $\hat{y}$ is a prediction and $y$ the label | $\hat{y} = f_\theta(x)$ | [Machine learning](../../theory/machine-learning/index.md) |
| Loss | $\mathcal{L}$, usually minimised | $\mathcal{L}(\theta)$ | [Machine learning](../../theory/machine-learning/index.md) |
| Gradient | $\nabla_\theta$ is the gradient with respect to the variable under it | $\nabla_\theta \mathcal{L}(\theta)$ | [Gradient descent](../../theory/math/calculus/gradient-descent/index.md) |
| Learning rate and step | $\eta$ for the learning rate; $t$ for the step, with $\theta_{t-1}$ the value before the step | $\theta_t = \theta_{t-1} - \eta\,\nabla_\theta\mathcal{L}$ | [Adam](../../theory/optimization/adaptive/adam.md) |
| Regularisation | $\lambda$ for the strength of a penalty or of weight decay | $\theta_t = \theta_{t-1} - \eta\,(\dots + \lambda\,\theta_{t-1})$ | [AdamW](../../theory/optimization/adaptive/adamw.md) |
| Data | $D$ or $\mathcal{D}$ for a dataset; $(x_i, y_i)$ for example $i$; $N$ or $n$ for its size | $D = \{(x_i, y_i)\}_{i=1}^{N}$ | [Maximum likelihood](../../theory/math/probability-statistics/maximum-likelihood/index.md) |
| Layers | $W$ and $b$ for weights and bias; $\sigma$ for the nonlinearity | $h = \sigma(Wx + b)$ | [Linear algebra](../../theory/math/linear-algebra/index.md) |
| Temperature | $\tau$ or $T$ inside a softmax or exponential | $\exp(s/\tau)$ | [Contrastive learning](../../theory/paradigms/self-supervised/contrastive-learning/index.md) |

## Reinforcement learning

| Quantity | Convention | Example | Where it appears |
|---|---|---|---|
| State, action, observation | $s_t$ for the state, $a_t$ for the action; $o_t$ when the agent sees only part of the state | $a_t \sim \pi(\cdot \mid s_t)$ | [Reinforcement learning](../../theory/paradigms/reinforcement-learning/index.md) |
| Reward | The textbook convention is that $r_{t+1}$ is the reward received after acting in $s_t$. Some pages write $r_t$ instead | $\delta_t = r_t + \gamma V(s_{t+1}) - V(s_t)$ | [Reinforcement learning](../../theory/paradigms/reinforcement-learning/index.md), [Dopamine](../../brain-mind/neuroscience/dopamine-reward-prediction-error/index.md) |
| Discount and return | $\gamma$ for the discount factor; $G_t$ for the discounted return | $G_t = \sum_{k\ge 0}\gamma^k r_{t+k+1}$ | [Reinforcement learning](../../theory/paradigms/reinforcement-learning/index.md) |
| Policy | $\pi(a \mid s)$ for a stochastic policy; $\pi_\theta$ when it is parametrised; $\mu$ for a deterministic policy | $\mu_i(o_i)$ | [Policy gradient](../../theory/paradigms/reinforcement-learning/policy-gradient-and-actor-critic/index.md), [MADDPG](../../theory/paradigms/reinforcement-learning/multi-agent-rl/maddpg/index.md) |
| Value functions | $V^\pi(s)$ for the state value; $Q^\pi(s,a)$ for the action value; $Q^*$ for the optimal action value | $Q^*(s,a) = \mathbb{E}[r + \gamma \max_{a'} Q^*(s', a')]$ | [Value-based methods](../../theory/paradigms/reinforcement-learning/value-based-methods/index.md) |
| Advantage | $A_t$ for the advantage estimate at time $t$ | $\nabla_\theta J(\theta) = \mathbb{E}[\sum_t \nabla_\theta \log \pi_\theta(a_t \mid s_t)\, A_t]$ | [Policy gradient](../../theory/paradigms/reinforcement-learning/policy-gradient-and-actor-critic/index.md) |
| Transition | $P(s' \mid s, a)$ for the probability of moving to $s'$ | $P(s' \mid s, \mathbf{a})$ | [Multi-agent RL](../../theory/paradigms/reinforcement-learning/multi-agent-rl/index.md) |
| Joint quantities | Bold $\mathbf{a}$ for the joint action of all agents; $\boldsymbol{\tau}$ for their joint history | $Q_{\text{tot}}(\boldsymbol{\tau}, \mathbf{a})$ | [QMIX](../../theory/paradigms/reinforcement-learning/multi-agent-rl/qmix/index.md) |

## Generative models

| Quantity | Convention | Example | Where it appears |
|---|---|---|---|
| Data and latent variables | $x$ for data; $z$ for a latent variable, with $p(z)$ as its prior | $p_\theta(x \mid z)$ | [VAE](../../theory/paradigms/unsupervised/density-and-generative-models/vae/index.md) |
| Encoder and decoder | $q_\phi(z \mid x)$ for the encoder; $p_\theta(x \mid z)$ for the decoder | $\mathcal{L}(\theta, \phi; x)$ for the evidence lower bound | [VAE](../../theory/paradigms/unsupervised/density-and-generative-models/vae/index.md) |
| Noise schedule | $\beta_t$ for the variance added at step $t$; $\alpha_t = 1 - \beta_t$; $\bar\alpha_t = \prod_{s \le t} \alpha_s$ | $x_t = \sqrt{\bar\alpha_t}\, x_0 + \sqrt{1 - \bar\alpha_t}\, \epsilon$ | [DDPM](../../theory/paradigms/unsupervised/density-and-generative-models/diffusion/ddpm.md) |
| Denoiser | $\epsilon_\theta(x_t, t)$ predicts the noise added to $x_t$ | $\hat{x}_0 = \dfrac{x_t - \sqrt{1-\bar\alpha_t}\,\epsilon_\theta(x_t, t)}{\sqrt{\bar\alpha_t}}$ | [DDIM](../../theory/paradigms/unsupervised/density-and-generative-models/diffusion/ddim.md) |
| Flow matching | $x_0$ for a noise sample; $x_1$ for a data sample; $t$ for time, drawn from $[0,1]$; $v_\theta$ for the learned velocity | $x_t = (1-t)\,x_0 + t\,x_1$ | [Flow matching](../../theory/paradigms/unsupervised/density-and-generative-models/flow-matching/index.md) |

## Where one symbol has two meanings

The table lists the letters that carry more than one meaning in the English pages. A reader should check the definition at the top of each page before relying on it.

| Symbol | Meanings in the wiki | Where |
|---|---|---|
| $\sigma$ | An activation function; a standard deviation or variance ($\sigma^2$); a noise level; the softmax in knowledge distillation; a density in NeRF; a singular value in the SVD | [Deep learning](../../theory/deep-learning/index.md), [Knowledge distillation](../../theory/model-compression/knowledge-distillation/index.md), [NeRF](../../theory/models/computer-vision/3d-and-neural-rendering/nerf/index.md), [Truncated SVD](../../theory/math/linear-algebra/truncated-svd/index.md) |
| $\pi$ | A policy in RL; a mixture weight $\pi_k$ in EM; a transport plan in optimal-transport flow matching; a target distribution in MCMC; the number 3.14 in a cosine schedule | [RL](../../theory/paradigms/reinforcement-learning/index.md), [EM](../../theory/math/probability-statistics/expectation-maximisation/index.md), [OT-CFM](../../theory/paradigms/unsupervised/density-and-generative-models/flow-matching/ot-cfm/index.md), [MCMC](../../theory/paradigms/probabilistic/mcmc/index.md) |
| $\lambda$ | An eigenvalue; a regularisation or weight-decay strength; a hyperparameter in general | [Linear algebra](../../theory/math/linear-algebra/index.md), [AdamW](../../theory/optimization/adaptive/adamw.md), [Hyperparameter optimisation](../../theory/optimization/hyperparameter-optimisation.md) |
| $\tau$ | A softmax temperature in contrastive learning; a joint history in QMIX; a prior scale in ridge regression; a time constant in a continuous-time firing-rate model | [Contrastive learning](../../theory/paradigms/self-supervised/contrastive-learning/index.md), [QMIX](../../theory/paradigms/reinforcement-learning/multi-agent-rl/qmix/index.md), [Maximum likelihood](../../theory/math/probability-statistics/maximum-likelihood/index.md), [Working memory](../../brain-mind/working-memory-executive-function/funahashi-1989/index.md) |
| $\epsilon$ and $\varepsilon$ | A small constant $\epsilon$ in Adam; noise $\epsilon$ in diffusion; noise $\varepsilon$ in the VAE and in FFJORD; the dual-number unit $\varepsilon$ in forward-mode differentiation | [Adam](../../theory/optimization/adaptive/adam.md), [DDPM](../../theory/paradigms/unsupervised/density-and-generative-models/diffusion/ddpm.md), [VAE](../../theory/paradigms/unsupervised/density-and-generative-models/vae/index.md), [Forward mode](../../theory/math/automatic-differentiation/forward-mode/index.md) |
| $\Sigma$ and $C$ | The diagonal matrix of singular values $\Sigma$ in the SVD; the covariance $\Sigma_k$ of a Gaussian component in EM; the data covariance $C$ in PCA | [Truncated SVD](../../theory/math/linear-algebra/truncated-svd/index.md), [EM](../../theory/math/probability-statistics/expectation-maximisation/index.md), [PCA](../../theory/math/linear-algebra/pca/index.md) |
| $G_t$ | The discounted return in RL; a gradient at step $t$ in Shampoo | [RL](../../theory/paradigms/reinforcement-learning/index.md), [Shampoo](../../theory/optimization/shampoo.md) |
| $\mathcal{L}$ | A loss, to be minimised; in the VAE and variational inference, the evidence lower bound, which is maximised | [Machine learning](../../theory/machine-learning/index.md), [VAE](../../theory/paradigms/unsupervised/density-and-generative-models/vae/index.md), [Variational inference](../../theory/paradigms/probabilistic/variational-inference/index.md) |
| $D$ and $\mathcal{D}$ | A dataset; in the DSSM retrieval model, a document $D$ and the candidate set $\mathcal{D}$ | [Maximum likelihood](../../theory/math/probability-statistics/maximum-likelihood/index.md), [DSSM](../../applications/search-and-information-retrieval/dssm/index.md) |
| $\theta$ | Model parameters; an angle in the cosine formula | [Linear algebra](../../theory/math/linear-algebra/index.md) |
| $a$ and $\mathbf{a}$ | One agent's action; the joint action of all agents | [Multi-agent RL](../../theory/paradigms/reinforcement-learning/multi-agent-rl/index.md) |
| $T$ | A number of steps (1000 in DDPM); a temperature in knowledge distillation and in [Glow](../../theory/paradigms/unsupervised/density-and-generative-models/normalising-flows/glow/index.md) | [DDPM](../../theory/paradigms/unsupervised/density-and-generative-models/diffusion/ddpm.md), [Knowledge distillation](../../theory/model-compression/knowledge-distillation/index.md) |
| $\mu$ | A mean in normalisation layers; a deterministic policy in MADDPG | [Normalisation](../../theory/deep-learning/normalisation/index.md), [MADDPG](../../theory/paradigms/reinforcement-learning/multi-agent-rl/maddpg/index.md) |

Some conventions in the tables above also disagree with each other. The reward index is $r_{t+1}$ on the reinforcement-learning overview but $r_t$ in the TD error on the dopamine page, and the noise symbol is $\epsilon$ in some generative pages and $\varepsilon$ in others. When a page departs from the usual convention, it is worth checking which one the page defines.

## Connections

The [Glossary](../glossary/index.md) gives the English terms for each concept above, with their Traditional Chinese names. The overview pages for [linear algebra](../../theory/math/linear-algebra/index.md), [probability and statistics](../../theory/math/probability-statistics/index.md) and [information theory](../../theory/information-theory/index.md) define the objects that these symbols stand for.

Neuroscience papers often use their own letters. The [working-memory page on Funahashi (1989)](../../brain-mind/working-memory-executive-function/funahashi-1989/index.md) writes $\tau$ as a time constant in a continuous-time firing-rate model, not as a temperature or a prior scale. When a model from neuroscience is compared with a model from machine learning, the two sets of symbols should be mapped to each other first.

## References

### Seminal papers

- Shannon, C. E. (1948). *A Mathematical Theory of Communication*. Bell System Technical Journal. https://doi.org/10.1002/j.1538-7305.1948.tb01338.x — Introduces entropy as a measure of information, the source of the $H$ notation used on the information-theory pages.
- Golub, G. & Kahan, W. (1965). *Calculating the Singular Values and Pseudo-Inverse of a Matrix*. Journal of the Society for Industrial and Applied Mathematics, Series B. https://doi.org/10.1137/0702016 — Gives a numerically stable algorithm for computing the singular values of a matrix, the quantities in the decomposition $A = U\Sigma V^\top$ that the truncated SVD page builds on.
- Dempster, A. P., Laird, N. M. & Rubin, D. B. (1977). *Maximum Likelihood from Incomplete Data Via the EM Algorithm*. Journal of the Royal Statistical Society, Series B. https://doi.org/10.1111/j.2517-6161.1977.tb01600.x — Introduces the EM algorithm and its expected complete-data log-likelihood $Q(\theta \mid \theta^t)$, as used on the EM page.
- Kingma, D. P. & Welling, M. (2013). *Auto-Encoding Variational Bayes*. arXiv. https://arxiv.org/abs/1312.6114 — Introduces the variational autoencoder and its objective in the $q_\phi(z \mid x)$ and $p_\theta(x \mid z)$ notation used on the VAE pages.
- Ho, J., Jain, A. & Abbeel, P. (2020). *Denoising Diffusion Probabilistic Models*. arXiv. https://arxiv.org/abs/2006.11239 — Defines the variance schedule $\beta_t$, $\alpha_t$ and $\bar\alpha_t$ and the noise-prediction objective used on the diffusion pages.
- Kingma, D. P. & Ba, J. (2014). *Adam: A Method for Stochastic Optimization*. arXiv. https://arxiv.org/abs/1412.6980 — Introduces the Adam optimiser, whose learning rate $\eta$, moment decay rates $\beta_1$ and $\beta_2$ and small constant $\epsilon$ are the symbols of the Adam page.
- Mnih, V. et al. (2015). *Human-level control through deep reinforcement learning*. Nature. https://doi.org/10.1038/nature14236 — The deep Q-network paper, which writes the action-value function as $Q(s, a; \theta)$ with network parameters $\theta$.
- Rashid, T. et al. (2018). *QMIX: Monotonic Value Function Factorisation for Deep Multi-Agent Reinforcement Learning*. arXiv. https://arxiv.org/abs/1803.11485 — Introduces the mixing network that combines per-agent values into $Q_{\text{tot}}$, the joint value used on the QMIX page.
- Lowe, R. et al. (2017). *Multi-Agent Actor-Critic for Mixed Cooperative-Competitive Environments*. arXiv. https://arxiv.org/abs/1706.02275 — Introduces MADDPG, with deterministic per-agent policies $\mu_i(o_i)$ and a centralised critic that sees all agents' actions.
- Hinton, G., Vinyals, O. & Dean, J. (2015). *Distilling the Knowledge in a Neural Network*. arXiv. https://arxiv.org/abs/1503.02531 — Introduces knowledge distillation with a softmax temperature $T$, the origin of the temperature symbol on the distillation pages.
