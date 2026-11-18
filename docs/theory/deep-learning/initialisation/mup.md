---
status: draft
last_reviewed: 2026-11-04
related:
  - theory/deep-learning/initialisation
tags:
  - muP
  - hyperparameter transfer
  - scaling
aliases:
  - 最大更新參數化
  - muP
  - Maximal update parametrisation
---

# Maximal update parametrisation (muP)

Maximal update parametrisation, usually written muP, is a scaling rule for the initialisation and learning rates of a network as its width grows. Yang et al. show that under this rule, the best hyperparameters found on a narrow model remain close to the best for a wider one. They call this zero-shot hyperparameter transfer.

## Overview

The [chapter](index.md) treats initialisation as a question of signal scale. muP asks how the scale of weights, updates and learning rates should depend on width, so that training dynamics stay comparable across model sizes.

## Problem

In the standard parametrisation, the best learning rate tends to change with width. Tuning a large model by search is then expensive, and a learning rate found on a small model may not transfer. The question is whether a parametrisation exists under which the best hyperparameters stay put as width grows.

## Core idea

Yang et al. identify such a parametrisation and verify the transfer on Transformer and ResNet models. In the paper's multiplier form, the learning rate and output multiplier of each layer are set according to its width, as listed below.

## Equation

The multiplier form for Adam, with $\text{fan\_in}$ the input width of a layer, is:

- hidden weights: Adam learning rate proportional to $1/\text{fan\_in}$;
- output layer: output multiplier $1/\text{fan\_in}$, with Adam learning rate 1;
- input layer: Adam learning rate 1.

## Width-dependent Adam multipliers

<div tabindex="0" role="region" aria-label="MuP width scaling animation; scroll horizontally on narrow screens." style="overflow-x:auto;overflow-y:hidden;max-width:100%;">
  <div style="width:640px;min-width:640px;">  <img data-source-asset-urls src="../../../assets/concept-animations/mup-width-multipliers-still.svg" data-motion-src="../../../assets/concept-animations/mup-width-multipliers-motion.svg" data-still-src="../../../assets/concept-animations/mup-width-multipliers-still.svg" alt="MuP schematic Adam multiplier scaling across fan-in width 128 to 1024: hidden-weight learning-rate and output scaling fall inversely with width; input and output Adam learning-rate factors remain constant." width="640" height="360" style="display:block;width:640px;max-width:none;height:auto;"></div>
</div>

*Original continuous teaching animation, CC BY-SA 4.0.* This diagram normalises the selected multipliers to one at a reference hidden-layer fan-in $n_0=128$. For a representative width $n$ increasing to 1024, the **hidden-weight Adam learning-rate factor** and the **output multiplier** both scale as $n_0/n$, hence fall to **1/8**; the **input/output-layer Adam learning-rate factors** remain at one under the specific multiplier-form recipe described above.[^mup-motion] Each quantity denotes a different part of the parametrisation: the output multiplier is **not** the output-layer Adam learning rate. These are **schematic scaling factors**, not learning curves, measured gradients or proof of hyperparameter transfer.

The wiki site provides **Play/Pause** (Enter/Space when focused), an initial static image for reduced motion, and horizontal keyboard scrolling on narrow screens. [Open the continuous SVG](../../../assets/concept-animations/mup-width-multipliers-motion.svg) · [View the static fallback](../../../assets/concept-animations/mup-width-multipliers-still.svg).

[^mup-motion]: Yang et al. (2022), *Tensor Programs V*, the Adam multiplier form and zero-shot hyperparameter transfer; see the original paper in References.

### A toy readout: why the output multiplier matters

<div tabindex="0" role="region" aria-label="MuP readout-aggregation schematic animation; scroll horizontally on narrow screens" style="overflow-x:auto;overflow-y:hidden;max-width:100%;">
  <div style="width:640px;min-width:640px;">  <img data-source-asset-urls src="../../../assets/concept-animations/mup-readout-aggregation-still.svg" data-motion-src="../../../assets/concept-animations/mup-readout-aggregation-motion.svg" data-still-src="../../../assets/concept-animations/mup-readout-aggregation-still.svg" alt="Schematic identical channel contributions: raw sum grows with channel count while multiplying by one over width keeps the readout at one." width="640" height="360" style="display:block;width:640px;max-width:none;height:auto;"></div>
</div>

*Original continuous/staged teaching animation, CC BY-SA 4.0.* This **explicitly artificial** scalar calculation fixes every hidden-channel contribution at $h_i=1$. Then $s_n=\sum_{i=1}^{n}h_i=n$, while the toy scaled readout $f_n=(1/n)s_n=1$ for $n=4,8,12,16$. The display isolates the algebraic effect of a $1/n$ output multiplier; it is **not** a derivation of all muP layer rules, a guarantee about correlated learned features, or a measured activation or loss.[^mup-motion]

On the wiki site, use **Play/Pause** (Enter/Space while focused); reduced-motion users initially see the still preview. Narrow screens can scroll horizontally. [Open the moving diagram](../../../assets/concept-animations/mup-readout-aggregation-motion.svg) · [View the GitHub fallback](../../../assets/concept-animations/mup-readout-aggregation-still.svg).

### Zero-shot transfer: search small, reuse large

<div tabindex="0" role="region" aria-label="MuTransfer tune-and-reuse schematic animation; scroll horizontally on narrow screens" style="overflow-x:auto;overflow-y:hidden;max-width:100%;">
  <div style="width:640px;min-width:640px;">  <img data-source-asset-urls src="../../../assets/concept-animations/mup-transfer-protocol-still.svg" data-motion-src="../../../assets/concept-animations/mup-transfer-protocol-motion.svg" data-still-src="../../../assets/concept-animations/mup-transfer-protocol-still.svg" alt="Illustrative muTransfer procedure: search four candidate learning rates at narrow width and reuse the selected candidate at wide width pending empirical validation." width="640" height="360" style="display:block;width:640px;max-width:none;height:auto;"></div>
</div>

*Original staged process animation, CC BY-SA 4.0.* A narrow model tests four **illustrative, arbitrary** candidate learning rates $\eta\in\{0.05,0.10,0.20,0.40\}$ and selects $0.20$ solely to illustrate the workflow. The same candidate is then reused at wider width **without repeating the hyperparameter search**. The figure does **not** assert these rates are optimal, represent actual training runs, or prove that transfer will succeed; evaluation at the wider width remains essential.[^mup-motion]

On the wiki site, **Play/Pause** (Enter/Space while focused) reveals the staged search and transfer; reduced-motion users see the final static overview. [Open the motion](../../../assets/concept-animations/mup-transfer-protocol-motion.svg) · [View the GitHub fallback](../../../assets/concept-animations/mup-transfer-protocol-still.svg).


### Toy hidden-weight steps: the aggregate is not one coordinate

<div tabindex="0" role="region" aria-label="Artificial muP hidden-weight update budget animation; scroll horizontally on narrow screens" style="overflow-x:auto;overflow-y:hidden;max-width:100%;">
  <div style="width:640px;min-width:640px;">  <img data-source-asset-urls src="../../../assets/concept-animations/mup-update-budget-still.svg" data-motion-src="../../../assets/concept-animations/mup-update-budget-motion.svg" data-still-src="../../../assets/concept-animations/mup-update-budget-still.svg" alt="Sixteen synthetic equal-magnitude coordinate steps: widening from four to sixteen shrinks each width-scaled step while keeping the sum of absolute steps equal to one; a fixed per-coordinate step makes that sum grow." width="640" height="360" style="display:block;width:640px;max-width:none;height:auto;"></div>
</div>

*Original continuous/staged mathematical animation, CC BY-SA 4.0.* **Artificial arithmetic, not actual Adam updates:** for each of $n=4,8,16$ coordinates, set $|\Delta w_i|=1/n$, so $\sum_i|\Delta w_i|=1$. The contrasting, deliberately **unscaled** setting $|\Delta w_i|=1/4$ instead yields totals $1,2,4$. The diagram isolates the inverse-fan-in hidden-weight learning-rate factor under a toy equal-step assumption; it does **not** imply that muP preserves the $L_1$ norm of real learned weight updates, functional feature updates, or any measured gradient.[^mup-motion]

The wiki player offers **Play/Pause** (Enter/Space while focused); reduced-motion mode starts with the static fallback, and narrow screens scroll inside the diagram. [Open the motion](../../../assets/concept-animations/mup-update-budget-motion.svg) · [View the GitHub-safe still](../../../assets/concept-animations/mup-update-budget-still.svg).

### Transfer is conditional: a wide-model check still matters

<div tabindex="0" role="region" aria-label="Artificial learning-rate optimum shift animation; scroll horizontally on narrow screens" style="overflow-x:auto;overflow-y:hidden;max-width:100%;">
  <div style="width:640px;min-width:640px;">  <img data-source-asset-urls src="../../../assets/concept-animations/mup-transfer-validation-still.svg" data-motion-src="../../../assets/concept-animations/mup-transfer-validation-motion.svg" data-still-src="../../../assets/concept-animations/mup-transfer-validation-still.svg" alt="Two invented convex objective curves: the narrow learning-rate optimum stays at 0.20, while the hypothetical wide-model optimum moves toward 0.35 and the reused candidate remains fixed at 0.20." width="640" height="360" style="display:block;width:640px;max-width:none;height:auto;"></div>
</div>

*Original continuous teaching animation, CC BY-SA 4.0.* The left curve is a **fabricated** narrow-model objective with minimiser $\eta=0.20$. On the right, the **fabricated** wide-model objective morphs between an aligned minimiser $0.20$ and a shifted minimiser $0.35$. For illustration, the endpoint can be described by $L_{\mathrm{wide}}(\eta)=(\eta-0.35)^2+0.15$, so reusing $0.20$ produces a toy excess loss $(0.20-0.35)^2=0.0225$. None of these curves or optima are training measurements or claims about the empirical transfer rate. muTransfer is a useful empirical result under suitable parametrisation and settings, **not a mathematical promise that every task, optimiser, or hyperparameter transfers**. The transferred setting still requires wide-model validation.[^mup-motion]

The site provides **Play/Pause**, keyboard operation and a reduced-motion still. [Open the motion](../../../assets/concept-animations/mup-transfer-validation-motion.svg) · [View the GitHub-safe still](../../../assets/concept-animations/mup-transfer-validation-still.svg).


### Averaging a readout: a stable mean can hide shrinking fluctuations

<div tabindex="0" role="region" aria-label="muP toy readout mean and independent-noise fluctuation animation; scroll horizontally on narrow screens" style="overflow-x:auto;overflow-y:hidden;max-width:100%;">
  <div style="width:640px;min-width:640px;">  <img data-source-asset-urls src="../../../assets/concept-animations/mup-readout-noise-still.svg" data-motion-src="../../../assets/concept-animations/mup-readout-noise-motion.svg" data-still-src="../../../assets/concept-animations/mup-readout-noise-still.svg" alt="For four to thirty-two independent toy channels with mean one and variance one, the scaled mean stays at one while the readout standard deviation falls as inverse square-root width." width="640" height="360" style="display:block;width:640px;max-width:none;height:auto;"></div>
</div>

*Original 12-second, four-width analytical teaching animation, CC BY-SA 4.0.* The preceding deterministic example used identical channel values $h_i=1$. Here, **only for a different, artificial independent-noise assumption**, let $h_i=1+\varepsilon_i$, with independent $\mathbb E[\varepsilon_i]=0$ and $\operatorname{Var}(\varepsilon_i)=1$. Then for $f_n=\frac{1}{n}\sum_i h_i$, **$\mathbb E[f_n]=1$** but **$\operatorname{SD}(f_n)=1/\sqrt n$**: at widths $n=4,8,16,32$, the standard deviation is approximately $0.500,0.354,0.250,0.177$. The moving markers distinguish a stable expectation from a contracting noise scale. This is *not* a prediction that every learned muP readout has vanishing noise: real channels may be correlated and width-scaled training dynamics are more involved.[^mup-motion] No values are empirical measurements.

The wiki player supports **Play/Pause** (Enter/Space when focused). Reduced Motion starts with the static still; the diagram scrolls horizontally on phones. [Open the SVG motion](../../../assets/concept-animations/mup-readout-noise-motion.svg) · [GitHub-readable fallback](../../../assets/concept-animations/mup-readout-noise-still.svg).

### Optimiser dependence: an Adam multiplier is not an SGD recipe

<div tabindex="0" role="region" aria-label="Illustrative Adam versus SGD single-step scaling animation; scroll horizontally on narrow screens" style="overflow-x:auto;overflow-y:hidden;max-width:100%;">
  <div style="width:640px;min-width:640px;">  <img data-source-asset-urls src="../../../assets/concept-animations/mup-adam-sgd-still.svg" data-motion-src="../../../assets/concept-animations/mup-adam-sgd-motion.svg" data-still-src="../../../assets/concept-animations/mup-adam-sgd-still.svg" alt="Synthetic positive gradients decrease as inverse square-root width; with the same inverse-width rate, the first bias-corrected Adam step and a plain SGD step decay at different rates." width="640" height="360" style="display:block;width:640px;max-width:none;height:auto;"></div>
</div>

*Original 12-second analytical teaching animation, CC BY-SA 4.0.* Take one **synthetic positive** scalar gradient $g_n=1/\sqrt n$ and apply the **same deliberately chosen** scalar rate $\eta_n=4/n$ to two *first-step* optimisers, starting with zero moments and zero weight decay. With bias-corrected Adam and the **illustrative special case $\epsilon=0$**, $|\Delta w_{\mathrm{Adam}}|=\eta_n g_n/|g_n|=4/n$; with SGD, $|\Delta w_{\mathrm{SGD}}|=\eta_n g_n=4/n^{3/2}$. The animated cursors track exact values at $n=4,8,16,32$. **Applying the Adam-oriented multiplier to SGD here is a counterexample, not a recommended SGD muP parametrisation.** Actual muP scaling depends on the optimiser, network architecture and parameter group.[^mup-motion] The artificial gradients are not model measurements or evidence that one optimiser trains better.

The diagram uses the existing **Play/Pause** control and an accessible still for reduced motion. [Open the SVG motion](../../../assets/concept-animations/mup-adam-sgd-motion.svg) · [GitHub-readable fallback](../../../assets/concept-animations/mup-adam-sgd-still.svg).

## Results

The abstract reports that hyperparameters tuned on a small model can be used on a much larger one, and that this holds for Transformer and ResNet models. Two examples are given. Transferring from a 13M-parameter model gives pretraining hyperparameters that outperform the published BERT-large numbers, at a tuning cost equal to pretraining BERT-large once. Transferring from a 40M-parameter model outperforms the published 6.7B GPT-3 model, with a tuning cost of only 7% of its total pretraining cost [(Yang et al., 2022)](https://arxiv.org/abs/2203.03466).

## Limitations

- The multiplier entries given above are for Adam. Other optimisers need their own derivation, and this page does not cover them.
- The verification in the paper covers Transformer and ResNet models, so other architectures need their own check.

## Connections

For the fan-based initialisation rules, see [Glorot initialisation](glorot-initialisation.md) and [He initialisation](he-initialisation.md).

## Applications

Tuning very large networks, where a full hyperparameter search is costly.

## Open questions

- How far does transfer extend across depth, batch size and architecture?
- How does muP interact with normalisation layers and with optimisers other than Adam?

Discrete depth/channel examples hold exact integer states and reset; connecting lines are guides, not fractional layers or channels. Parameter sweeps are illustrative interpolations, not training trajectories. Reversing a parameter sweep is not reversing training. The density plot shows only a finite window of the Gaussian tails, without renormalising the truncated view.

These are width-relative multipliers within the cited Adam parameterisation, not literal learning rates of 1 and not a complete implementation recipe. A common base learning rate remains tunable. The examples hold the architecture family and non-width dimensions fixed; initialisation, parameter grouping, biases and any attention/output multipliers must follow the same parameterisation. The transfer-validation morph explicitly uses L(eta) = (eta - mu)² + 0.15 with mu moving from 0.20 to 0.35; every moving marker is evaluated on that same curve.

## References

### Seminal papers

- Yang et al., *Tensor Programs V: Tuning Large Neural Networks via Zero-Shot Hyperparameter Transfer* (2022). https://arxiv.org/abs/2203.03466 — Introduces muP and zero-shot hyperparameter transfer.
- Glorot and Bengio, *Understanding the difficulty of training deep feedforward neural networks*, Proceedings of the 13th International Conference on Artificial Intelligence and Statistics (2010). https://proceedings.mlr.press/v9/glorot10a.html — Analyses training difficulty in deep feedforward networks and proposes a fan-based initialisation.
- He, Zhang, Ren and Sun, *Delving Deep into Rectifiers: Surpassing Human-Level Performance on ImageNet Classification* (2015). https://arxiv.org/abs/1502.01852 — Introduces an initialisation designed for rectifier networks.
- Schoenholz, Gilmer, Ganguli and Sohl-Dickstein, *Deep Information Propagation* (2016). https://arxiv.org/abs/1611.01232 — Mean-field analysis of signal propagation through deep networks.
- Vaswani et al., *Attention Is All You Need* (2017). https://arxiv.org/abs/1706.03762 — Introduces the Transformer architecture in which muP is most often applied.
