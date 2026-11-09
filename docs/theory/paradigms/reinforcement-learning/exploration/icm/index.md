---
status: complete
last_reviewed: 2026-10-28
aliases:
  - ICM
  - Intrinsic curiosity module
  - Curiosity-driven exploration
---

# Intrinsic curiosity module (Pathak et al., 2017)

An exploration method that gives the agent a curiosity reward equal to the error of its own forward model, measured in a learned feature space. The features are trained with a self-supervised inverse dynamics model, encouraging the bonus to focus on action-relevant changes, though this filtering is not guaranteed.

## Problem

Extrinsic rewards are often extremely sparse or absent, so the agent needs an intrinsic reward to explore and to learn skills that may be useful later. Predicting raw pixels as a curiosity signal is a poor choice, since visual detail that the agent cannot control, such as moving leaves, produces large errors that carry no useful information. Pathak et al. ask how to define curiosity so that it responds to the consequences of the agent's own actions.

## Core idea

ICM has three networks:

- An **encoder** maps the observation \(s_t\) to a feature vector \(\phi(s_t)\).
- An **inverse dynamics model** predicts the action \(a_t\) from \(\phi(s_t)\) and \(\phi(s_{t+1})\). Training this model encourages features to retain information useful for identifying the agent's action, while reducing sensitivity to irrelevant changes; it does not guarantee complete disentanglement of controllable and uncontrollable factors.
- A **forward model** predicts \(\phi(s_{t+1})\) from \(\phi(s_t)\) and \(a_t\).

The intrinsic reward is the squared error of the forward model in the feature space. Ideally, the learned representation deemphasises uncontrollable visual changes, but unpredictable factors may remain and can still contribute to the bonus. The agent is rewarded for visiting states where its own actions have consequences it cannot yet predict.

## Equation or algorithm

With the forward model \(\hat\phi\), the intrinsic reward is

\[
r^{\text{int}}_t = \tfrac{\eta}{2}\,\lVert \hat\phi(\phi(s_t), a_t) - \phi(s_{t+1}) \rVert_2^2 ,
\]

where \(\eta\) is a scaling factor. The encoder, forward model and inverse model are trained jointly, and the policy maximises the sum of the intrinsic and extrinsic rewards.

## Instructional animation

![ICM process: current and next features feed forward and inverse dynamics; after comparison, a loss-driven update cue precedes forward prediction improvement](../../../../../assets/concept-animations/icm-forward-inverse-motion.svg)

*Original instructional animation (CC BY-SA 4.0).* The two **Encoder** boxes represent the **same learned feature mapping** applied to consecutive observations. The **Forward** model combines the current feature and action to predict the next feature; the orange point moves toward the green encoded next feature, reducing the squared feature-space error that supplies intrinsic reward. The **Inverse** branch uses both encoded features to learn which action produced the transition, encouraging action-relevant representations. The arrow to the comparison pane comes from the **actual next-state feature, not the inverse-model output**. The **Error → reward** bar follows the **squared distance** between the plotted green target and orange prediction throughout the learning phase, under a fixed illustrative scale. At loop restart it snaps to the initial state without depicting reverse learning. This is a **schematic example**, not measured performance or a promise that training error decreases monotonically. MkDocs offers Play/Pause; [static GitHub-friendly preview](../../../../../assets/concept-animations/icm-forward-inverse-still.svg). Source: [Pathak et al. (2017)](https://arxiv.org/abs/1705.05363).

**Reading the signal traces.** The short blue and amber pulses enter the **forward** model from the current feature and action, respectively. A subsequent **orange pulse** traces the forward prediction into the comparison pane, while a **green pulse** traces the independently encoded actual next feature there. A dashed amber **update** cue then returns from the error comparison to the **Forward** model. It represents a schematic loss-driven parameter update **across training iterations**, rather than a prediction correcting itself during a single inference. **Only after this cue** does the orange prediction approach the encoded target and the bonus shrink. The two purple input pulses enter the **inverse** model from the two encoded observations. A final short purple pulse exits as the estimated action (\(\hat a_t\)): this is an **inverse-dynamics training output**, not the next-feature target and not a curiosity reward. The input and comparison pulses show computational dependencies; only the amber return cue represents a training update. This short path is not a complete gradient graph (the encoder can also receive gradients), and the inverse output does not supply the forward target. Only the forward prediction error determines the illustrated intrinsic bonus.

### Predictable versus stochastic transitions

![ICM comparison: a forward prediction converges toward a repeatable next-state feature, while varying next-state features under the same input retain prediction error](../../../../../assets/concept-animations/icm-predictable-stochastic-motion.svg)

*Original instructional animation (CC BY-SA 4.0).* Both panels repeat the **same encoded current feature and action**. On the **Predictable** side, the observed next feature remains the same, so learning can move the orange forward prediction toward that green target and reduce its error. On the **Stochastic** side, several possible encoded next features arise from the **same input**; one deterministic forward prediction cannot match all outcomes simultaneously. Thus a prediction-error bonus can remain positive even after the model has learned the conditional distribution's central tendency. This is an **illustration of residual unpredictability, not a claim that ICM must reward every random observation**: the inverse-dynamics representation may suppress some uncontrollable factors, but cannot be assumed to remove all of them. In this **three-outcome schematic**, the three possible green targets are assigned equal illustrative weight, and their arithmetic mean equals the fixed orange forward prediction. The faint teal triangle outlines the three possible next-feature outcomes, while the orange point marked **mean** is their equal-weight centroid. The **violet tick** on the right-hand error bar stays fixed at the *expected* squared error over those outcomes, even as the orange bar switches between individual sampled squared errors; a sample can lie below that expectation. This conditional-variance floor assumes the encoder is fixed and the deterministic predictor outputs the conditional mean, rather than measuring ICM training. In **both** panels, the orange error bars scale with the **squared feature-space distance** between the predicted and actual feature: it decreases continuously during the illustrated training on the left, and changes discretely with sampled outcomes on the right. The blue input pulse repeats the unchanged feature–action pair immediately before each discrete outcome switch; the plotted green marker jumps between sampled outcomes instead of interpolating unobserved states. Coordinates and weights are not estimated probabilities, measured bonuses, or actual training trajectories. The animation loop replays the comparison, not a reset of learned weights. On MkDocs use Play/Pause. On narrow screens, the same comparison automatically uses a larger-label, vertically stacked animation instead of shrinking two panels side by side; pausing or enabling reduced motion shows its matching static frame. Both layouts are independent **schematic coordinate examples**, not measurements. [Static GitHub-friendly desktop preview](../../../../../assets/concept-animations/icm-predictable-stochastic-still.svg). Source: [Pathak et al. (2017)](https://arxiv.org/abs/1705.05363).

For a fixed encoder and a deterministic forward-model prediction, write \(z=(\phi(s_t),a_t)\) and \(Y=\phi(s_{t+1})\). The squared-error decomposition is

\[
\mathbb E[\|Y-\hat\phi(z)\|_2^2\mid z]
=\|\mathbb E[Y\mid z]-\hat\phi(z)\|_2^2
+\operatorname{tr}\!\big(\operatorname{Cov}[Y\mid z]\big).
\]

Even a predictor matching the conditional mean leaves the conditional-variance term. Joint feature learning can change that variance; the right-hand panel illustrates a **possible limitation**, not a universal failure of ICM.

## Interactive feature-error probe

Use **Previous/Next**, the timeline slider, or Play/Pause with 0.5×–2× speed to inspect each illustrative transition. The diagram is recomputed per step: **distinct stochastic outcomes switch discretely**, without depicting unobserved intermediate next states. The first three steps demonstrate repeated training on a **fixed, repeatable next-state feature**: the orange forward prediction approaches the unchanged green feature, so the squared gap decreases from **3.73 → 0.67 → 0.00** in arbitrary display units. The later three steps compare a **different stochastic conditional transition** whose fixed forecast equals its conditional mean; they are not additional training updates to the preceding deterministic case. The three equally likely stochastic outcomes have their mean at the fixed predictor. The orange bar is the **sample squared error**; the violet tick denotes the **expected squared error**, not any single observed reward. The coordinate scale and displayed squared gaps are **arbitrary teaching units, never trained-model measurements**.

**Deterministic expectation versus sample error.** During the three repeatable-outcome updates, the conditional next-feature distribution is a point mass: its variance is zero, but the predictor's error is not zero before fitting. Therefore, the violet **Expected** tick must coincide with the orange sampled squared-error bar at **3.73 → 0.67 → 0.00** (illustrative units). This is distinct from the stochastic case below, where the expected tick averages over three possible results and need not coincide with any single sample.

**Conditional-mean experiment (MkDocs).** Select stochastic step 4–6 and move **Prediction shift** between −40 and +40 schematic feature-coordinate units. The orange forecast moves horizontally, while the three possible green outcome locations remain fixed; their weights are equal in the default configuration. A dashed violet circle marks their **conditional mean**. The orange bar shows the current **sample** squared gap; the violet tick shows **expected** squared error over all three outcomes. The live readout computes **expected MSE = squared bias + conditional variance** using the same coordinates, with displayed values divided by 1,000. At the conditional mean (shift 0), the illustrative expected error is **3.02**; a 40-unit shift raises it to **4.62** (= 1.60 squared bias + 3.02 variance), even if the error for one particular sample becomes smaller. Use **Reset to mean** to compare. This slider **manually changes a hypothetical deterministic forecast**; it is not a learning update, an empirical reward trace, or a claim about ICM's trained features. Keyboard arrow keys operate the slider and manual controls remain available with reduced motion.

**Outcome-probability experiment (MkDocs).** In stochastic steps 4–6, the new **Outcome balance** slider changes a *hypothetical conditional distribution*, not the encoder, forward-model weights, or the three possible feature locations. With slider value \(k\) from −60 to +60, the probabilities of samples labelled 1/2/3 are \(p_1=(100+k)/300\), \(p_2=1/3\), and \(p_3=(100-k)/300\). All stay positive. The dotted green rings change weight, while the violet conditional-mean marker and the orange prediction move to the **probability-weighted** mean; a nonzero Prediction shift remains a horizontal offset from that new mean. The orange bar is still the *selected sample's* squared error, and the violet tick and readout recompute the **weighted expected error = conditional variance + squared prediction bias**. The animated **Weighted p × gap²** strip beneath the feature-space plot breaks this expectation into three colour-coded terms, one for each possible next feature: each segment's length is proportional to \(p_i\lVert Y_i-\hat\phi(z)\rVert^2\), and the three segments add to the violet expected error. Moving either slider recomputes all three segments, so a selected sample with a small error does not have to be the largest contributor. Unlike the individual sample-error bar above, this strip includes the hypothetical probabilities. At equal weights (33.3% each), variance is **3.02** schematic units; at k = −60 (13.3% / 33.3% / 53.3%), it is **2.40**; at k = +60 (53.3% / 33.3% / 13.3%), it is **2.65**. These different expected errors describe different assumed transition distributions, **not a training improvement**. Use **Equal weights** to restore the baseline, then **Reset to mean** to set prediction bias to zero. The GitHub static previews retain the equal-weight baseline; probability controls require the MkDocs site. All probabilities, coordinates and errors are constructed teaching examples, **not observed model or environment statistics**.

**Bias–variance geometry and decomposition (MkDocs).** In stochastic steps, a **violet segment from the weighted conditional mean to the orange prediction** represents forecast bias. Beneath the three outcome-weighted sample-error contributions, the new **Variance + Bias²** strip expresses the *same expected squared gap* in two terms: violet is the irreducible conditional variance; amber is the squared distance from the prediction to the mean. The first portion changes when **Outcome balance** changes; the second increases quadratically when **Prediction shift** moves the predictor. Both decomposition strips use the same fixed scale (344 pixels per 6,000 raw squared-coordinate units), so their total lengths agree up to SVG rounding. The upper **Squared gap** bar instead uses a separate fixed 16,000-unit range to avoid clipping even the largest allowed sample error (14,700.24); **compare numeric values rather than bar lengths across these differently scaled axes**. This is an interactive counterfactual, not a training update or measured ICM reward.

### Animated distribution reweighting

![ICM probability sweep: three fixed possible next-feature outcomes retain their locations while probability mass shifts, moving the conditional mean, the best deterministic forecast, and the three probability-weighted contributions to the expected squared-error floor](../../../../../assets/concept-animations/icm-weighted-outcomes-motion.svg)

*Original ten-second continuous instructional animation (CC BY-SA 4.0).* The three coloured widths represent the hypothetical conditional probabilities (p_1,p_2,p_3), while the **three encoded next-state outcomes remain in fixed positions**. Their coloured outer rings change with probability weight. Three outcome-coloured dashed links connect each fixed feature outcome to the **violet weighted mean**; their changing lengths trace the geometric distance entering each identically coloured lower contribution bar. Ring thickness, by contrast, reflects probability. The inner amber point is the **optimal deterministic prediction** under squared-error loss. The violet **Variance floor** bar responds to the same changing weights, using the exact conditional variance of those three outcomes (sampled densely for smooth rendering). Its **three coloured segments** now resolve that floor into the terms $p_i\lVert Y_i-\mu\rVert_2^2$, with $\mu=\sum_i p_iY_i$. The segment colours match outcome markers 1, 2 and 3; their lengths sum to the total floor at every instant. Because the distances to the *moving* conditional mean change along with the probabilities, an outcome's contribution need not change in direct proportion to its probability. The sweep goes from (k=-60) to (0) to (+60) and back: **it changes an assumed distribution, not learned weights, and is not a training trajectory**. Its expected gap need not move monotonically when probability is transferred between possible outcomes. On MkDocs use Play/Pause; pausing, reduced motion, and GitHub Markdown use the [matching static three-case preview](../../../../../assets/concept-animations/icm-weighted-outcomes-still.svg) below. The 400-pixel-wide portrait composition preserves readable symbols on phones. All positions, probabilities and error bars are constructed teaching examples, **not empirical ICM measurements**. Source: [Pathak et al. (2017)](https://arxiv.org/abs/1705.05363).

![ICM weighted next-feature outcomes: three counterfactual probability settings preserve possible next-feature locations but move the conditional mean and expected squared prediction error](../../../../../assets/concept-animations/icm-weighted-outcomes-still.svg)

*Original three-case GitHub-safe fallback (CC BY-SA 4.0).* All three panels share the same three possible next-feature locations; circle size encodes their **hypothetical probability**, the violet ring marks the resulting weighted conditional mean, and the orange point is a forecast at that mean. The values 2.40, 3.02 and 2.65 are **illustrative conditional variances** in arbitrary display units, not observed rewards. This summary is static only to support GitHub/no-script readers; the **Outcome balance** and **Prediction shift** sliders on MkDocs provide continuous, keyboard-operable counterfactual experiments.


### Monte Carlo samples versus the conditional expectation

The **Sample outcomes** controls on stochastic steps 4–6 repeatedly draw one of the *three fixed possible next features* under the currently selected hypothetical probabilities. **Draw 1** and **Draw 20** update the orange running mean of sampled squared errors; the violet analytic expected error remains fixed for the chosen distribution and predictor. The most recent outcomes appear as small colour-coded tokens. A **running-mean trajectory** now plots the cumulative sample average after *every draw* against the horizontal, exact expected-error line; its point at draw \(n\) is the average of the first \(n\) losses, **not** the loss of draw \(n\). This makes short-term departures and crossings of the expectation visible. The trajectory's vertical scale is chosen from the *possible* errors for the selected probability/prediction setting and stays fixed as more samples are drawn. The plot retains the last 120 prefix-mean points to bound rendering work, but the running mean and total count still use **all** draws. The separate marker strip uses a fixed 0–16 scale. Units throughout are squared feature-coordinate distances divided by 1,000.

For draws \(I_j\sim\mathrm{Categorical}(p_1,p_2,p_3)\) under an unchanged distribution and predictor, the empirical mean is \(\bar L_n = n^{-1}\sum_{j=1}^{n}\|Y_{I_j}-\hat\phi(z)\|^2/1000\), whereas the exact conditional expectation is \(L=\sum_i p_i\|Y_i-\hat\phi(z)\|^2/1000\). A finite sample mean can move **away** from the expectation before approaching it; convergence is not monotonic or guaranteed at any finite sample count. Changing **Outcome balance** or **Prediction shift** clears the samples so unlike distributions are never pooled. The draws use a **reproducible pseudo-random sequence**, not real environment transitions or empirical ICM rewards.

**Independent sampling replicates (MkDocs).** Select **New 20-draw run** to generate a fresh, independently seeded, 20-draw *toy sequence* without changing the three outcome probabilities, predictor, or analytic expectation. The panel reports the new run number together with the **previous run's mean and its sample size**; compare the orange trajectory and observed frequencies across runs to see how finite-sample averages differ under the *same* underlying distribution. **Reset samples** clears the current run but preserves its deterministic seed: pressing **Draw 20** again reproduces that run exactly. Either distribution/prediction slider restores run 1 and removes the comparison to avoid mixing experimental conditions. Different pseudo-random streams model **sampling variability**, not ICM training progress, learned parameters, or experimental measurements.

![Two reproducible 20-draw running-mean paths from the same hypothetical outcome probabilities, with the analytic expectation shown as a fixed dashed line](../../../../../assets/concept-animations/icm-independent-runs-still.svg)

*Original static fallback for GitHub and no-JavaScript views (CC BY-SA 4.0).* Both sequences use the same **illustrative** equally weighted three-outcome loss distribution, with no model update between runs. Their final sample means are **2.786** and **3.002**, while the exact conditional expectation is **3.017**. The full MkDocs probe creates and replays trajectories interactively; the static image is a comparison of two deterministic synthetic sequences, **not model data**.

**Analytic sampling uncertainty (MkDocs).** The shaded violet **±1 SE** reference surrounds the exact expected loss \(L\) and narrows with draw count \(n\). Let \(\ell_i=\lVert Y_i-\hat\phi(z)\rVert^2/1000\) be the loss for outcome \(i\), and let \(\sigma_\ell^2=\sum_i p_i(\ell_i-L)^2\). Then \(\operatorname{SE}(\bar L_n)=\sigma_\ell/\sqrt n\) for independent draws from a fixed distribution. This is the **theoretical standard error of the running mean of losses**, not the variance of next-state feature vectors, a fitted uncertainty estimate, a confidence interval, or a guarantee that the orange trace lies inside the shaded area. The chart's axis includes the n=1 reference range and remains fixed as new draws arrive. Sliders reset the sequence and recompute the analytic band. All numbers are schematic.

**Outcome-frequency experiment (MkDocs).** The three live bars now show the *empirical* relative frequencies `N_i/n` of outcomes 1–3, each compared with a dark vertical marker for its fixed *assumed* conditional probability `p_i`. The readout beside each bar is **observed / assumed**. The same colours identify the outcomes in the feature-space and weighted-error plots. These bars use **all draws**, even when the recent-outcome chips show only 12 results and the running-mean trace retains only 120 points. Consequently, for fixed current prediction and loss values, the displayed sampled mean can also be reconstructed exactly as

$
\\bar L_n=\\sum_{i=1}^3\\frac{N_i}{n}\\ell_i,\\qquad
L=\\sum_{i=1}^3 p_i\\ell_i.
$

The difference between the two means comes from how the empirical frequencies differ from the assumed distribution, not from an ICM training update. In the seeded **20-draw** equal-weight example, the frequencies are **2/20, 8/20, 10/20** (10%, 40%, 50%), while the assumed probabilities remain **1/3 each**; the sample mean is **2.786** versus the analytic **3.017**. More draws do not guarantee that each empirical bar approaches its marker monotonically. Both slider changes and Reset samples clear the counts. The numbers are hypothetical, not environment observations or model measurements.

**Why is the sampled mean different? Centered frequency contributions (MkDocs).** The difference between empirical and assumed outcome frequencies satisfies $\sum_i(N_i/n-p_i)=0$. We can therefore subtract the same baseline from every outcome loss without changing the sampling gap. Choosing the **analytic expected loss** $L$ gives a zero-centred, three-colour decomposition:

\[
\bar L_n-L=\sum_{i=1}^{3}\left(\frac{N_i}{n}-p_i\right)(\ell_i-L).
\]

An over-sampled *below-average-loss* outcome contributes negatively, while an over-sampled *above-average-loss* outcome contributes positively. Under the illustrative seeded 20 draws the centered terms are **−0.198, −0.072 and +0.039**, summing to **−0.231** (display rounding). Unlike a decomposition using uncentred $\ell_i$, **each centered term is unchanged if an arbitrary constant is added to all outcome losses**. This makes the displayed signs independent of the loss zero point. The signed terms are a finite-sample **accounting decomposition**, not causal effects, forward-model updates, intrinsic-reward measurements or a new training loss. The chart scale stays fixed during draws under a fixed distribution and predictor; either slider change or Reset samples clears the history.

![ICM signed contributions of three sampled outcomes to the difference between the sample mean and analytic expected error](../../../../../assets/concept-animations/icm-sampling-gap-still.svg)

*Original GitHub/no-script fallback (CC BY-SA 4.0).* The bars show the **20-draw hypothetical example**; the central line is zero and the numbers are schematic loss units, **not model measurements**. The live MkDocs chart updates after every draw and includes keyboard-operable sampling controls, screen-reader labels and reduced-motion support.

![ICM illustration comparing twenty sampled outcome frequencies with three assumed equal probabilities; vertical marks denote the assumed shares](../../../../../assets/concept-animations/icm-outcome-frequency-still.svg)

*Original static GitHub/no-script fallback (CC BY-SA 4.0).* This snapshot illustrates the frequency comparison after 20 seeded hypothetical draws. The fully interactive version, including frequency updates and a bilingual accessible label for each outcome, is available on MkDocs; the static file does not simulate sampling.

![ICM three snapshots after one, five and twenty toy outcome draws; the running sampled mean can move further from the fixed expectation before returning nearer](../../../../../assets/concept-animations/icm-sample-mean-still.svg)

*Original GitHub/no-script fallback (CC BY-SA 4.0).* At equal weights and zero prediction shift, the exact expectation is **3.017**, while the seeded sample means are **3.250**, **3.373** and **2.786** after 1, 5 and 20 draws. The diagram's axis runs from 0 to 6; the MkDocs marker strip uses 0–16 and the new prefix-mean trajectory explicitly labels its own vertical range. **Compare labelled numbers, not marker distances across plots with different axes.** Orange is the empirical mean and violet the analytic expectation. These are deliberately constructed teaching values, **not trained-model measurements**.

<div data-curiosity-lab="icm" data-locale="en"><p>This interactive step-through is available on the MkDocs site; the SVG animations and GitHub-safe static previews above remain available without scripts.</p></div>

## Results

The paper evaluates ICM on the visual games VizDoom and Super Mario Bros, where the extrinsic reward is sparse or absent. The abstract reports that curiosity alone lets the agent learn to explore. The paper reports that a Mario agent trained without any extrinsic reward can learn to cross over 30% of Level 1 of Super Mario Bros, and that in VizDoom the agent learns to walk along corridors instead of bumping into walls or getting stuck in corners.

## Limitations

- **Stochastic dynamics.** The forward model can still be unpredictable in states that the agent cannot control, if they are relevant to the transition.
- **Novelty.** Like other curiosity bonuses, the reward favours states the agent finds hard to predict, which may not be the states that matter for the task.
- **Feature learning.** The inverse-model features depend on the agent's actions, so exploration can be weak in environments where the agent has little control.

## Connections

- Parent topic: [Exploration](../index.md).
- It is a prediction-error bonus, like [random network distillation](../rnd/index.md), but it predicts in a learned feature space rather than comparing against a random target.
- The paper's main agent, ICM with A3C, combines the curiosity reward with the asynchronous actor-critic method of [A3C](../../policy-gradient-and-actor-critic/a3c/index.md).

## Applications

- **Games with sparse rewards**, such as the platform and first-person games used in the paper.
- **Robotics** where the agent must learn which of its actions change the scene.

## Open questions

- How to make the feature space capture the agent's control without losing task-relevant detail.
- How to combine curiosity with goal-directed exploration.

## References

### Seminal papers

- Pathak, Agrawal, Efros & Darrell (2017), "Curiosity-driven exploration by self-supervised prediction", [arXiv:1705.05363](https://arxiv.org/abs/1705.05363) — The ICM paper, with the inverse-dynamics feature space, the forward-model bonus and the VizDoom and Super Mario Bros experiments.
- Burda, Edwards, Storkey & Klimov (2018), "Exploration by random network distillation", [arXiv:1810.12894](https://arxiv.org/abs/1810.12894) — RND, a prediction-error bonus that does not need a feature space.
- Bellemare et al. (2016), "Unifying count-based exploration and intrinsic motivation", [arXiv:1606.01868](https://arxiv.org/abs/1606.01868) — Pseudo-count bonuses, the count-based approach that curiosity methods are compared with.
- Stadie, Levine & Abbeel (2015), "Incentivizing exploration in reinforcement learning with deep predictive models", [arXiv:1507.00814](https://arxiv.org/abs/1507.00814) — An earlier prediction-based exploration bonus that uses a learned predictive model.
- Houthooft et al. (2016), "VIME: Variational information maximizing exploration", [arXiv:1605.09674](https://arxiv.org/abs/1605.09674) — Information-gain exploration, an alternative curiosity signal.
