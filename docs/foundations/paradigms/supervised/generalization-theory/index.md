---
tags:
  - supervised learning
  - learning theory
  - generalization
---

# Generalisation and Statistical Learning Theory

Why does a model fit to a finite sample perform well on unseen data? Statistical learning theory gives conditions and bounds, and deep learning has revealed where the classical story falls short.

## Setup

Data $(x,y)$ are drawn i.i.d. from an unknown distribution $P$. The **true risk** is $R(f)=\mathbb{E}[L(f(x),y)]$; the learner only sees the **empirical risk** $\hat R(f)$. The **generalisation gap** is $R(f)-\hat R(f)$.

## Bias–variance trade-off

For squared error, expected test error decomposes into bias$^2$ + variance + irreducible noise. Simple models have high bias; flexible models have high variance. Classical wisdom says to pick the sweet spot in between.

## Capacity measures and bounds

| Concept | Idea |
|---|---|
| PAC learning (Valiant, 1984) | With probability $\ge 1-\delta$, error $\le\epsilon$ using polynomially many samples |
| VC dimension | Largest set the class can shatter; sample complexity grows with it |
| Rademacher complexity | How well the class fits random noise; data-dependent |
| Uniform stability | Changing one training point changes the output little |
| PAC-Bayes | Bounds average risk of a posterior over models via KL to a prior |
| Margin bounds | Larger margins give tighter bounds independent of dimension |

A typical bound has the form $R(f)\le\hat R(f)+O\big(\sqrt{(\text{complexity}+\log(1/\delta))/n}\big)$.

## What deep learning changed

- Networks can fit random labels (Zhang et al., 2017), so naive capacity bounds are vacuous.
- **Double descent** (Belkin et al., 2019): test error falls, rises near the interpolation threshold, then falls again as models grow.
- Overparameterised models generalise through implicit bias of the optimiser, flat minima and data structure. Scaling laws (Kaplan et al., 2020) describe the empirical regularity.

## No free lunch

No learner beats another across all possible problems; learning works because real data has structure (smoothness, compositionality, low dimension). This is the **inductive bias** that architectures such as convolution encode.

## Connections

Distribution shift breaks the i.i.d. assumption; see [transfer theory](../../transfer/index.md) and [online learning](../../online/index.md) for guarantees without it.

## References

### Seminal papers

- Valiant (1984), "A theory of the learnable", *Communications of the ACM* 27(11). https://mlanthology.org/misc/1984/valiant1984misc-theory
- Zhang et al. (2017), "Understanding deep learning requires rethinking generalization", ICLR, arXiv:1611.03530. https://mlanthology.org/iclr/2017/zhang2017iclr-understanding
- Jacot, Gabriel & Hongler (2018), "Neural tangent kernel", NeurIPS, arXiv:1806.07572.

### Surveys and textbooks

- Vapnik, *Statistical Learning Theory*, Wiley (1998). https://www.wiley-vch.de/en/areas-interest/mathematics-statistics/statistical-learning-theory-978-0-471-03003-4
- Shalev-Shwartz & Ben-David, *Understanding Machine Learning: From Theory to Algorithms*, Cambridge University Press (2014). https://doi.org/10.1017/CBO9781107298019

### Lectures and videos

- Yaser Abu-Mostafa, *Learning From Data*, Caltech online course (2012), lectures on VC dimension and generalisation. https://work.caltech.edu/telecourse

### Articles and documentation

- Belkin, Hsu, Ma & Mandal (2019), "Reconciling modern machine-learning practice and the bias–variance trade-off", *PNAS*, arXiv:1812.11118.
- Kaplan et al. (2020), "Scaling laws for neural language models", arXiv:2001.08361.
