---
related:
  - engineering/evaluation
tags:
  - evaluation
  - metrics
  - classification
---

# PR-AUC

PR-AUC summarises the precision-recall curve, which plots precision against recall as the decision threshold changes. It is the metric to prefer when positives are rare, because it focuses on how the positives are ranked.

## Definition

Average precision (AP) is the usual PR-AUC estimate. It sums the precision at each threshold, weighted by the gain in recall from the previous threshold:

$$AP = \sum_n (R_n - R_{n-1})\, P_n$$

where $P_n$ and $R_n$ are precision and recall at the $n$-th threshold. scikit-learn's `average_precision_score` uses this step-wise form, which does not interpolate between points. It warns that the trapezoidal area under the same curve can be overly optimistic.

## Interpretation

At population level, scores independent of the labels give a horizontal precision reference at the positive prevalence. This is not the exact expected non-interpolated AP of a finite randomly ordered sample. Unlike ROC-AUC, the baseline changes with the data, so PR-AUC values are not comparable across datasets with different prevalence. Compare models on the same dataset.

## When to use it

Use PR-AUC when positives are rare, as in fraud or fault detection, and when the scores will be used to pick the top of a ranked list. Saito and Rehmsmeier (2015) show that on imbalanced data the precision-recall plot is more informative than the ROC plot.

## Worked example

Use the same four scores. Sorted by score, the list is 0.9 (positive), 0.8 (negative), 0.6 (positive), 0.3 (negative). Precision at the two positives is $1/1$ and $2/3$, so average precision is $(1 + 2/3) / 2 \approx 0.83$, which matches the value `average_precision_score` returns. The prevalence reference is 0.5, but enumerating the six equally likely placements of two positives gives expected finite-sample AP $49/72 \approx 0.681$ under uniform random ordering.

## Animated ranking and average precision

<div class="concept-motion-scroll" style="width:100%;overflow-x:auto" tabindex="0" role="region" aria-label="Precision-recall threshold sweep animation">
<div style="width:640px">
<img data-source-asset-urls style="width:640px;min-width:640px;max-width:none;height:auto;display:block" src="../../../../assets/concept-animations/pr-threshold-sweep-still.svg" data-still-src="../../../../assets/concept-animations/pr-threshold-sweep-still.svg" data-motion-src="../../../../assets/concept-animations/pr-threshold-sweep-motion.svg" alt="Ten illustrative ranked prediction scores, three positive and seven negative. Lowering the threshold adds cases; negative cases decrease precision without changing recall, while positive cases increase recall. The prevalence baseline is 0.30." width="640" height="360">
</div>
</div>

*Original animated teaching visual (CC BY-SA 4.0).* This invented example uses the **same ten ranked scores as the ROC animation**: positives at ranks **1, 3, 6** and seven negatives. Each accepted positive increases recall by $1/3$; each accepted negative decreases precision while recall stays fixed. Precision at the three positive ranks is $1$, $2/3$ and $3/6$, giving **non-interpolated average precision $AP=(1+2/3+1/2)/3=13/18 \approx 0.722$**. The dashed line marks the positive prevalence $3/10=0.30$, a common population-level random-score reference. **For this finite ten-item example, the expected sample AP of a uniformly random permutation is about 0.450, not 0.300** (enumerating all 120 placements of three positives). At zero accepted cases, precision is undefined; the plot uses $(R,P)=(0,1)$ as an endpoint convention. The displayed polyline connects threshold operating points; **AP is the recall-increment-weighted mean of precisions, not the trapezoidal area underneath those segments** (see the scikit-learn reference). All scores and labels are **synthetic, not empirical model predictions**. MkDocs provides a keyboard-operable Play/Pause button and a reduced-motion still fallback; [GitHub static preview](../../../../assets/concept-animations/pr-threshold-sweep-still.svg) and [complete SVG animation](../../../../assets/concept-animations/pr-threshold-sweep-motion.svg) are also available. On narrow screens, scroll horizontally.

## Animated AP: recall-weighted rectangles

<div class="concept-motion-scroll" style="width:100%;overflow-x:auto" tabindex="0" role="region" aria-label="Average precision contribution animation">
<div style="width:640px">
<img data-source-asset-urls style="width:640px;min-width:640px;max-width:none;height:auto;display:block" src="../../../../assets/concept-animations/pr-ap-rectangles-still.svg" data-still-src="../../../../assets/concept-animations/pr-ap-rectangles-still.svg" data-motion-src="../../../../assets/concept-animations/pr-ap-rectangles-motion.svg" alt="Four synthetic ranked cases with positive labels at ranks one and three. At each positive hit, a rectangle of width one half in recall and height equal to precision is added. The resulting average precision is five sixths, about 0.833." width="640" height="360">
</div>
</div>

*Original teaching animation (CC BY-SA 4.0).* Unlike the threshold-sweep visualization above, this panel **builds AP from the actual recall increments**. Four invented scores are ordered 0.90 **(positive)**, 0.80 (negative), 0.60 **(positive)**, 0.30 (negative). Positive hits at ranks 1 and 3 contribute rectangular areas `(1/2) × (1/1)` and `(1/2) × (2/3)`, respectively. Thus **AP = 1/2 + 1/3 = 5/6 ≈ 0.833**. Selecting a negative case does not increase recall, so it adds **zero area** even though it changes the precision of the active prefix. The rectangles encode **non-interpolated average precision**, not a linearly interpolated trapezoidal PR area. No probabilities or measurements were fitted to data. Use the MkDocs Play/Pause control or reduced-motion still; [GitHub static preview](../../../../assets/concept-animations/pr-ap-rectangles-still.svg) and [full SVG animation](../../../../assets/concept-animations/pr-ap-rectangles-motion.svg) are provided. The figure scrolls horizontally on narrow screens.

## Animated AP versus trapezoidal PR integration

<div class="concept-motion-scroll" style="width:100%;overflow-x:auto" tabindex="0" role="region" aria-label="AP rectangles and trapezoidal area comparison">
<div style="width:640px">
<img data-source-asset-urls style="width:640px;min-width:640px;max-width:none;height:auto;display:block" src="../../../../assets/concept-animations/pr-ap-trapezoid-gap-still.svg" data-still-src="../../../../assets/concept-animations/pr-ap-trapezoid-gap-still.svg" data-motion-src="../../../../assets/concept-animations/pr-ap-trapezoid-gap-motion.svg" alt="Four synthetic ranks positive negative positive negative. Non-interpolated average precision rectangles sum to 0.833, but straight-line interpolation between precision-recall points yields 0.792 trapezoidal area." width="640" height="360">
</div>
</div>

*Original animated teaching visual (CC BY-SA 4.0).* For the same four **synthetic** cases `+ − + −`, **non-interpolated average precision** sums two recall-weighted rectangles: $AP=(1/2)(1)+(1/2)(2/3)=5/6\approx0.833$. Connecting the *threshold-derived* PR points with straight lines, including vertical changes at fixed recall, instead produces **trapezoidal area** $(1/2)(1)+(1/2)(1/2+2/3)/2=19/24\approx0.792$. The difference is $1/24$ for this ranking. **Neither integration convention is always greater**; the ranking and interpolation rule matter. The animation reveals AP rectangles before the linearly interpolated region. These are analytic, not empirical classifier measurements; do not call the trapezoidal value `average_precision_score`. MkDocs supplies keyboard-operable Play/Pause and a reduced-motion still. [GitHub static comparison](../../../../assets/concept-animations/pr-ap-trapezoid-gap-still.svg) · [Full SVG animation](../../../../assets/concept-animations/pr-ap-trapezoid-gap-motion.svg). The scikit-learn AP reference below defines the step-wise formula.

## Animated comparison: equal ROC-AUC, different average precision

<div class="concept-motion-scroll" style="width:100%;overflow-x:auto" tabindex="0" role="region" aria-label="ROC-AUC versus average precision ranking comparison animation">
<div style="width:640px">
<img data-source-asset-urls style="width:640px;min-width:640px;max-width:none;height:auto;display:block" src="../../../../assets/concept-animations/auc-ap-ranking-contrast-still.svg" data-still-src="../../../../assets/concept-animations/auc-ap-ranking-contrast-still.svg" data-motion-src="../../../../assets/concept-animations/auc-ap-ranking-contrast-motion.svg" alt="Two synthetic four-item rankings have two correctly ordered positive–negative pairs out of four, so both ROC-AUC scores equal 0.5. Their positive ranks differ and average precision accumulates to 0.750 versus 0.583." width="640" height="360">
</div>
</div>

*Original teaching animation (CC BY-SA 4.0).* Compare two **synthetic, distinct-score** rankings, each with two positives and two negatives. Ranking A is `+ − − +`; positive ranks **1 and 4** give **$AP_A=(1+2/4)/2=0.750$**. Ranking B is `− + + −`; positive ranks **2 and 3** give **$AP_B=(1/2+2/3)/2=7/12\approx0.583$**. Both rankings nonetheless have **two correctly ordered positive–negative pairs out of four**, so **ROC-AUC is $0.500$ for each**. As the scan line advances, contribution bars appear only for positive ranks. The displayed final AP and AUC summaries are computed from all four items, even before the scan completes. This illustrates why pairwise discrimination alone does not specify *where* relevant items occur in a retrieval ranking. These are analytic examples, not measured predictions. MkDocs provides Play/Pause by keyboard and a reduced-motion still; [GitHub static preview](../../../../assets/concept-animations/auc-ap-ranking-contrast-still.svg) · [Full SVG animation](../../../../assets/concept-animations/auc-ap-ranking-contrast-motion.svg). Scroll horizontally on narrow screens. See Fawcett (2006) and the scikit-learn AP reference in References.

## Properties and variants

- **Baseline.** Prevalence is the population-level random-score reference; finite-sample expected AP can be higher. State which baseline is being used.
- **Interpolation variants.** Older benchmarks, such as early PASCAL VOC evaluations, used 11-point interpolated average precision. At recall levels $0, 0.1, \ldots, 1$ it takes the maximum precision at or above each level and averages those. This differs from the step-wise average precision used here.
- **Single-point summaries.** Precision at a fixed recall, such as 90%, is a single-point summary that some applications prefer.
- **Limit.** Like ROC-AUC it judges the ranking but not calibration, and its value depends on prevalence.

## Pitfalls

- **Prevalence.** Two datasets with different positive rates give different PR-AUC baselines. Report the prevalence next to the score.
- **Interpolation.** Trapezoidal and step-wise estimates of the same curve differ. State which one is used.

## Related metrics

[ROC-AUC](roc-auc.md) is the threshold-free metric that uses the true and false positive rates instead. [Precision](precision.md) and [recall](recall.md) are the points on the curve. The family overview is [Classification Metrics](index.md).


## Animated explanation: Average precision with tied scores

<div class="concept-motion-scroll" style="width:100%;overflow-x:auto" tabindex="0" role="region" aria-label="Animated explanation: Average precision with tied scores">
<div style="width:640px">
<img data-source-asset-urls style="width:640px;min-width:640px;max-width:none;height:auto;display:block" src="../../../../assets/concept-animations/pr-ap-tied-threshold-still.svg" data-motion-src="../../../../assets/concept-animations/pr-ap-tied-threshold-motion.svg" data-still-src="../../../../assets/concept-animations/pr-ap-tied-threshold-still.svg" alt="Four schematic predictions include one positive and one negative tied at 0.70. The threshold admits both together, making noninterpolated AP rise to about 0.833." width="640" height="360">
</div>
</div>

*Original teaching animation, CC BY-SA 4.0; GitHub shows the static fallback.* [GitHub static preview](../../../../assets/concept-animations/pr-ap-tied-threshold-still.svg) · [Full SVG animation](../../../../assets/concept-animations/pr-ap-tied-threshold-motion.svg).

A score-threshold precision–recall curve admits **every item at a tied score together**, rather than breaking ties arbitrarily. With artificial scores $0.90(+),0.70(+),0.70(-),0.20(-)$, distinct thresholds yield $(R,P)=(1/2,1)$, $(1,2/3)$, $(1,1/2)$. Non-interpolated $AP=(1/2)(1)+(1/2)(2/3)=5/6\approx0.8333$. The last negative lowers precision but does not increase recall or AP. A forced ordering of individual tied records can give a different positive-rank average; the illustration follows scikit-learn `average_precision_score` with grouped thresholds. The values are **synthetic, not measured**. MkDocs Play/Pause and keyboard horizontal scrolling are available.

## References

### Seminal papers

- Saito, T. & Rehmsmeier, M. (2015). The precision-recall plot is more informative than the ROC plot when evaluating binary classifiers on imbalanced datasets. *PLoS ONE* 10(3). https://doi.org/10.1371/journal.pone.0118432 — Shows why precision-recall curves are more informative than ROC curves for rare positives.

### Articles and documentation

- scikit-learn contributors. *average_precision_score*. https://scikit-learn.org/stable/modules/generated/sklearn.metrics.average_precision_score.html — API reference giving the step-wise formula for average precision and the warning about the trapezoidal rule.
- scikit-learn contributors. *Metrics and scoring: quantifying the quality of predictions*. https://scikit-learn.org/stable/modules/model_evaluation.html — Overview of threshold-free classification scorers and how they are used.

### Additional sources

- Manning, C. D., Raghavan, P. & Schütze, H. *Evaluation of ranked retrieval results*, online edition of *Introduction to Information Retrieval*. https://nlp.stanford.edu/IR-book/html/htmledition/evaluation-of-ranked-retrieval-results-1.html — Defines precision, recall, the F measure and average precision for retrieval.
- Murphy, K. P. *Probabilistic Machine Learning: An Introduction*. MIT Press, 2022. https://probml.github.io/pml-book/book1.html — Textbook with a free online draft on probabilistic machine learning.
