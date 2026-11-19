#!/usr/bin/env python3
"""Recompute the analytic precision/recall and harmonic-mean illustrations."""
from pathlib import Path
import math

labels = (1, 0, 1, 1, 0, 1, 0, 0)
assert sum(labels) == 4
precisions, recalls = [], []
for k in range(1, 9):
    tp = sum(labels[:k])
    fp = k - tp
    fn = sum(labels) - tp
    assert tp + fp == k and tp + fn == 4
    precisions.append(tp / (tp + fp))
    recalls.append(tp / (tp + fn))
assert precisions[3] == recalls[3] == .75
assert math.isclose(precisions[5], 4 / 6)
assert recalls[5] == 1
assert all(x <= y for x, y in zip(recalls, recalls[1:]))
assert precisions[1] < precisions[2]  # precision is not monotone under threshold sweep
for i in range(10, 96):
    p = i / 100
    r = .8
    harmonic = 2 * p * r / (p + r)
    arithmetic = (p + r) / 2
    assert harmonic <= arithmetic + 1e-12
assert math.isclose(2 * .2 * .8 / (.2 + .8), .32)
assert math.isclose((.2 + .8)/2, .5)
for stem in ("precision-recall-threshold", "f1-harmonic-gap"):
    root = Path("docs/assets/concept-animations")
    motion = (root / (stem + "-motion.svg")).read_text(encoding="utf-8")
    still = (root / (stem + "-still.svg")).read_text(encoding="utf-8")
    assert "prefers-reduced-motion" in motion and 'class="moving"' in motion
    assert "<animate " in motion and "<animate " not in still

# Fixed-conditional-rate prevalence sweep (population rates, not samples).
for i in range(10, 91):
    prevalence = i / 100
    accuracy = .8 * prevalence + .9 * (1 - prevalence)
    balanced = (.8 + .9) / 2
    assert math.isclose(accuracy, .9 - .1 * prevalence, abs_tol=1e-12)
    assert math.isclose(balanced, .85, abs_tol=1e-12)
assert math.isclose(.8 * .1 + .9 * .9, .89)
assert math.isclose(.8 * .9 + .9 * .1, .81)

# F-beta with a fixed analytic precision/recall pair.
def fbeta(beta, precision=.45, recall=.9):
    return (1 + beta**2) * precision * recall / (beta**2 * precision + recall)

assert math.isclose(fbeta(.5), .5)
assert math.isclose(fbeta(1), .6)
assert math.isclose(fbeta(2), .75)
assert all(fbeta(i / 20) <= fbeta((i + 1) / 20) for i in range(10, 40))
for stem in ("accuracy-prevalence", "fbeta-recall-emphasis"):
    root = Path("docs/assets/concept-animations")
    motion = (root / (stem + "-motion.svg")).read_text(encoding="utf-8")
    still = (root / (stem + "-still.svg")).read_text(encoding="utf-8")
    assert "prefers-reduced-motion" in motion and 'class="moving"' in motion
    assert "<animate " in motion and "<animate " not in still


# Base-rate effect at fixed sensitivity and false-positive rate.
def ppv(p):
    return .9 * p / (.9 * p + .05 * (1 - p))

assert math.isclose(ppv(.01), 2 / 13)
assert math.isclose(ppv(.10), 2 / 3)
assert math.isclose(ppv(.50), 18 / 19)
assert all(ppv(i / 1000) < ppv((i + 1) / 1000) for i in range(10, 500))

# Macro/micro F1 for a fixed 90:10 single-label class distribution.
def f1_a(k):
    return 180 / (190 - k)

def f1_b(k):
    return 2 * k / (10 + k)

def macro_f1(k):
    return (f1_a(k) + f1_b(k)) / 2

def micro_f1(k):
    return (90 + k) / 100

assert math.isclose(macro_f1(0), 9 / 19)
assert math.isclose(micro_f1(0), .9)
assert math.isclose(macro_f1(10), 1)
assert math.isclose(micro_f1(10), 1)
for k in range(11):
    # One-vs-rest: TP_A=90, FP_A=10-k, FN_A=0.
    # TP_B=k, FP_B=0, FN_B=10-k.
    assert math.isclose(f1_a(k), 2 * 90 / (2 * 90 + 10 - k))
    assert math.isclose(f1_b(k), 2 * k / (2 * k + 10 - k))
    assert micro_f1(k) >= macro_f1(k)
for stem in ("precision-base-rate", "f1-macro-micro-imbalance"):
    root = Path("docs/assets/concept-animations")
    motion = (root / (stem + "-motion.svg")).read_text(encoding="utf-8")
    still = (root / (stem + "-still.svg")).read_text(encoding="utf-8")
    assert "prefers-reduced-motion" in motion and 'class="moving"' in motion
    assert "<animate " in motion and "<animate " not in still


# Independent ranking interpretations for four strictly ordered artificial scores.
from itertools import product

positive_scores = (0.90, 0.60)
negative_scores = (0.80, 0.30)
pair_wins = sum(float(p > n) + 0.5 * float(p == n)
                for p, n in product(positive_scores, negative_scores))
assert pair_wins == 3
assert math.isclose(pair_wins / (len(positive_scores) * len(negative_scores)), 0.75)
assert (float(0.5 > 0.5) + 0.5 * float(0.5 == 0.5)) == 0.5

ranked_labels = (1, 0, 1, 0)
positives = sum(ranked_labels)
hits = 0
ap = 0.0
for rank, label in enumerate(ranked_labels, start=1):
    if label:
        hits += 1
        ap += (hits / rank) / positives
assert math.isclose(ap, 5 / 6)
assert math.isclose((0.5 * 1.0) + (0.5 * (2 / 3)), ap)

for stem in ("roc-pairwise-auc", "pr-ap-rectangles"):
    root = Path("docs/assets/concept-animations")
    motion = (root / (stem + "-motion.svg")).read_text(encoding="utf-8")
    still = (root / (stem + "-still.svg")).read_text(encoding="utf-8")
    assert "prefers-reduced-motion" in motion
    assert 'class="motion-layer moving"' in motion
    assert "<animate " in motion and "<animate " not in still

print("Classification motion semantics: 8 analytic cases OK")

# Independent regression for restricted ROC integration and PR area conventions.
order=(1,0,1,0,0,0)
wins=sum(1 for i,a in enumerate(order) for j,b in enumerate(order) if a==1 and b==0 and i<j)
assert wins==7 and math.isclose(wins/(2*4),7/8)
def raw_partial(c):
    assert .25<=c<=1
    return .25*.5+(c-.25)
assert math.isclose(raw_partial(.25),.125)
assert math.isclose(raw_partial(1),.875)
assert all(raw_partial(i/100)<raw_partial((i+1)/100) for i in range(25,100))
ap_step=.5+(1/2)*(2/3)
ap_trap=.5+(1/2)*(.5+2/3)/2
assert math.isclose(ap_step,5/6)
assert math.isclose(ap_trap,19/24)
assert math.isclose(ap_step-ap_trap,1/24)
for name in ("roc-partial-area","pr-ap-trapezoid-gap"):
    root=Path("docs/assets/concept-animations")
    motion=(root/(name+"-motion.svg")).read_text(encoding="utf-8")
    still=(root/(name+"-still.svg")).read_text(encoding="utf-8")
    assert "prefers-reduced-motion" in motion and 'class="still"' in motion
    assert "<animate " in motion and "<animate " not in still
print("Restricted ROC area and PR trapezoid semantics OK")


# Monotone transformations preserve each strictly ordered positive/negative pair.
from itertools import product as pairs_product
for i in range(201):
    t = i / 200
    transform = lambda s: (1 - t) * math.sqrt(s) + t * s**3
    wins = sum(float(transform(p) > transform(n)) +
               0.5 * float(transform(p) == transform(n))
               for p, n in pairs_product((.9, .6), (.8, .3)))
    assert wins == 3
assert all(math.sqrt(a) < math.sqrt(b) for a, b in ((.3, .6), (.6, .8), (.8, .9)))

# AUC 0.5 need not imply identical average precision.
for labels, target_ap in (((1, 0, 0, 1), .75), ((0, 1, 1, 0), 7/12)):
    n_pos = sum(labels)
    n_neg = len(labels) - n_pos
    hits = 0
    ap_value = 0
    for rank, positive in enumerate(labels, start=1):
        if positive:
            hits += 1
            ap_value += (hits / rank) / n_pos
    pair_wins = sum(int(i < j) for i, p in enumerate(labels)
                    for j, neg in enumerate(labels) if p and not neg)
    assert math.isclose(ap_value, target_ap)
    assert math.isclose(pair_wins / (n_pos * n_neg), .5)

for stem in ("roc-rank-transform", "auc-ap-ranking-contrast"):
    root = Path("docs/assets/concept-animations")
    moving = (root / (stem + "-motion.svg")).read_text(encoding="utf-8")
    still = (root / (stem + "-still.svg")).read_text(encoding="utf-8")
    assert "prefers-reduced-motion" in moving
    assert 'class="moving"' in moving and 'class="still"' in moving
    assert "<animate " in moving and "<animate " not in still
print("Rank-transform and AUC/AP contrast semantics OK")

# Positive/negative tied scores contribute half-credit to pairwise ROC-AUC.
tied_pos = (.90, .80)
tied_neg = (.80, .20)
tied_credits = [1.0 if p > n else .5 if p == n else 0.0
                for p in tied_pos for n in tied_neg]
assert tied_credits == [1.0, 1.0, .5, 1.0]
assert math.isclose(sum(tied_credits) / 4, .875)

# An AP score-threshold sweep enters all equal-score observations as a group.
tied_samples = ((.90, 1), (.70, 1), (.70, 0), (.20, 0))
prev_recall = 0.
group_ap = 0.
states = []
for threshold in sorted({s for s, _ in tied_samples}, reverse=True):
    subset = [(s, y) for s, y in tied_samples if s >= threshold]
    tp = sum(y for _, y in subset)
    recall = tp / 2
    precision = tp / len(subset)
    group_ap += (recall - prev_recall) * precision
    prev_recall = recall
    states.append((len(subset), recall, precision, group_ap))
assert [x[0] for x in states] == [1, 3, 4]
assert math.isclose(states[1][3], 5/6)
assert math.isclose(states[2][3], 5/6)
assert math.isclose(group_ap, 5/6)
for stem in ("roc-tie-half-credit", "pr-ap-tied-threshold"):
    root = Path("docs/assets/concept-animations")
    motion = (root / f"{stem}-motion.svg").read_text(encoding="utf-8")
    still = (root / f"{stem}-still.svg").read_text(encoding="utf-8")
    assert "prefers-reduced-motion" in motion and 'class="moving"' in motion
    assert "<animate " in motion and "<animate " not in still
print("Tied ROC-AUC credit and grouped-threshold AP semantics OK")

# F1 selected-prefix sweep under eight distinct-ranked artificial scores.
prefix_labels=(1,0,1,1,0,1,0,0)
f1_at_k=[]
for k in range(9):
    tp=sum(prefix_labels[:k]); fp=k-tp; fn=4-tp
    f1=2*tp/(2*tp+fp+fn)
    assert math.isclose(f1,2*tp/(k+4))
    f1_at_k.append(f1)
assert f1_at_k.index(max(f1_at_k))==6
assert math.isclose(f1_at_k[4],.75) and math.isclose(f1_at_k[5],2/3)
assert math.isclose(f1_at_k[6],.8)

# Two conditional operating rates combine linearly under independent rule randomization.
for i in range(101):
    weight=i/100
    fpr=(1-weight)*.10+weight*.40
    tpr=(1-weight)*.60+weight*.90
    assert 0<=fpr<=1 and 0<=tpr<=1
    assert math.isclose(tpr-fpr,.5)
assert math.isclose((.10+.40)/2,.25) and math.isclose((.60+.90)/2,.75)
for stem in ("f1-threshold-topk", "roc-randomized-operating-mix"):
    root=Path("docs/assets/concept-animations")
    motion=(root/(stem+"-motion.svg")).read_text(encoding="utf-8")
    still=(root/(stem+"-still.svg")).read_text(encoding="utf-8")
    assert "prefers-reduced-motion" in motion and 'class="moving"' in motion
    assert '<animate ' in motion and '<animate ' not in still
print("F1 prefix sweep and randomized ROC mixture semantics OK")


# Enumerate all six strictly ranked placements of two positive cases among four.
from itertools import combinations
baseline_ap = []
baseline_auc = []
for hits in combinations(range(4), 2):
    labels = [int(i in hits) for i in range(4)]
    seen = 0
    ap_score = 0.0
    for rank, label in enumerate(labels, start=1):
        if label:
            seen += 1
            ap_score += (seen / rank) / 2
    auc_score = sum(int(i < j) for i in range(4) for j in range(4)
                    if labels[i] == 1 and labels[j] == 0) / 4
    baseline_ap.append(ap_score)
    baseline_auc.append(auc_score)
assert all(math.isclose(a, b) for a, b in zip(baseline_ap, (1, 5/6, 3/4, 7/12, 1/2, 5/12)))
assert math.isclose(sum(baseline_ap) / 6, 49/72)
assert math.isclose(sum(baseline_auc) / 6, 1/2)
assert 49/72 > 1/2  # finite-sample expected AP exceeds prevalence

# Rank-order thresholds are mapped to conditional ROC rates; deployment prevalence is independent.
costs = []
label_prefix = (1, 0, 1, 0)
for k in range(5):
    tp = sum(label_prefix[:k])
    fp = k - tp
    tpr, fpr = tp/2, fp/2
    costs.append(2 * .25 * (1 - tpr) + 1 * .75 * fpr)
assert all(math.isclose(x, y) for x, y in zip(costs, (.5,.25,.625,.375,.75)))
assert costs.index(min(costs)) == 1
for stem in ("pr-random-ap-expectation", "roc-cost-operating-point"):
    root=Path("docs/assets/concept-animations")
    motion=(root/(stem+"-motion.svg")).read_text(encoding="utf-8")
    still=(root/(stem+"-still.svg")).read_text(encoding="utf-8")
    assert "prefers-reduced-motion" in motion and 'class="moving"' in motion
    assert "<animate " in motion and "<animate " not in still
print("Finite-sample AP baseline and cost-aware ROC semantics OK")

# Shared, explicitly synthetic 100-case count example.
# Check that all four bilingual metric pages reference the same defined sample.
tp, fp, fn, tn = 40, 10, 20, 30
assert tp + fp + fn + tn == 100
assert math.isclose((tp + tn) / 100, 0.7)
assert math.isclose(tp / (tp + fp), 0.8)
assert math.isclose(tp / (tp + fn), 2 / 3)
assert math.isclose(2 * tp / (2 * tp + fp + fn), 8 / 11)
shared_dir = Path("docs/theory/evaluation/metrics/classification")
for name in ("index.md", "index.zh-TW.md"):
    contents = (shared_dir / name).read_text(encoding="utf-8")
    for count in ("40 (TP)", "20 (FN)", "10 (FP)", "30 (TN)", "80/110"):
        assert count in contents, (name, count)
for metric in ("accuracy", "precision", "recall", "f1"):
    contents_en = (shared_dir / f"{metric}.md").read_text(encoding="utf-8")
    contents_zh = (shared_dir / f"{metric}.zh-TW.md").read_text(encoding="utf-8")
    assert "[shared synthetic 100-case confusion matrix](index.md)" in contents_en
    assert "[共用的人工 100 筆混淆矩陣範例](index.md)" in contents_zh
    assert "Using the 100 cases above" not in contents_en
    assert "沿用上述 100 筆案例" not in contents_zh
assert "Accuracy needs no threshold" not in (shared_dir / "accuracy.md").read_text(encoding="utf-8")
assert "Precision measures the cost" not in (shared_dir / "precision.md").read_text(encoding="utf-8")
assert "Recall measures the cost" not in (shared_dir / "recall.md").read_text(encoding="utf-8")
print("Bilingual count example and decision-rule regression OK")

# ROC operating rates are fixed under a prevalence shift, while PPV is not.
def shifted_ppv(p):
    return .8 * p / (.8 * p + .1 * (1 - p))

assert math.isclose(shifted_ppv(.05), 8 / 27)
assert math.isclose(shifted_ppv(.60), 12 / 13)
assert all(shifted_ppv(k / 1000) < shifted_ppv((k + 1) / 1000)
           for k in range(50, 600))

# Synthetic ordering: + - + + - -, with 3 positives and 3 negatives.
# J peaks at k=4; the deployment-optimal cutoff changes with FN cost.
decision_labels = (1, 0, 1, 1, 0, 0)
j_values, low_cost, high_cost = [], [], []
for k in range(7):
    tp = sum(decision_labels[:k])
    fp = k - tp
    tpr, fpr = tp / 3, fp / 3
    j_values.append(tpr - fpr)
    low_cost.append(.1 * (1 - tpr) + .9 * fpr)
    high_cost.append(5 * .1 * (1 - tpr) + .9 * fpr)
assert j_values.index(max(j_values)) == 4
assert low_cost.index(min(low_cost)) == 1
assert high_cost.index(min(high_cost)) == 4
assert math.isclose(low_cost[1], 1 / 15)
assert math.isclose(high_cost[4], .3)
for stem in ("roc-pr-shift", "roc-youden-cost"):
    asset = Path("docs/assets/concept-animations")
    motion = (asset / f"{stem}-motion.svg").read_text(encoding="utf-8")
    still = (asset / f"{stem}-still.svg").read_text(encoding="utf-8")
    assert "prefers-reduced-motion" in motion
    assert 'class="moving"' in motion and 'class="baseline"' in still
    assert "<animate" in motion and "<animate" not in still
# Verify the seven-cutoff lower envelope, not merely the two displayed endpoints.
for index in range(81):
    fn_cost = 1 + index / 20
    losses = []
    for k in range(7):
        tp = sum(decision_labels[:k])
        fp = k - tp
        losses.append(fn_cost * .1 * (1 - tp / 3) + .9 * (fp / 3))
    minimum = min(losses)
    assert math.isclose(minimum, min(losses[1], losses[4]), abs_tol=1e-12)
    optima = [k for k, loss in enumerate(losses)
              if math.isclose(loss, minimum, abs_tol=1e-12)]
    expected = [1] if fn_cost < 4.5 else [4] if fn_cost > 4.5 else [1, 4]
    assert optima == expected, (fn_cost, optima, expected)

# Multi-line equations must use display delimiters in both translations.
for filename in ("roc-auc.md", "roc-auc.zh-TW.md"):
    page = (shared_dir / filename).read_text(encoding="utf-8")
    assert "\n$$\n" in page and r"\begin{aligned}" in page and r"\end{aligned}" in page
    assert "4.5" in page and "roc-youden-cost-still.svg" in page

print("ROC prevalence-shift and Youden-versus-cost analytic cases OK")

# Pure prevalence (prior-probability) shift: the same conditional rates, different PPV.
# Under changes to P(score | class), these fixed-rate assumptions need not hold.
for p in (.05, .10, .25, .60):
    numerator = .8 * p
    denominator = numerator + .1 * (1 - p)
    assert math.isclose(shifted_ppv(p), numerator / denominator)

# Youden J equivalence requires matching *effective* costs, not merely equal raw costs.
# Here p=0.1, FP cost=1 so FN cost=9 equalizes the two terms.
balanced_fn_cost = 9
effective_weight = .9
j_op = []
l_op = []
for k in range(7):
    true_positives = sum(decision_labels[:k])
    false_positives = k - true_positives
    tpr = true_positives / 3
    fpr = false_positives / 3
    j_op.append(tpr - fpr)
    l_op.append(balanced_fn_cost * .1 * (1 - tpr) + .9 * fpr)
    assert math.isclose(l_op[-1], effective_weight * (1 - j_op[-1]))
assert j_op.index(max(j_op)) == l_op.index(min(l_op)) == 4

# Source regression: paired translations must state the prior-shift assumption,
# equal-effective-cost condition and responsive display-math PPV equation.
for filename, required_terms in (
    ("roc-auc.md", ("class-conditional score distributions",
                    "pure prevalence (prior-probability) shift")),
    ("roc-auc.zh-TW.md", ("分數條件分布", "先驗比例")),
):
    page = (shared_dir / filename).read_text(encoding="utf-8")
    for term in required_terms:
        assert term in page, (filename, term)
    assert "$$\nPPV(p)=" in page
    assert "L(k)=w[1-J(k)]" in page
    assert "C_{FN}=9" in page

print("Prior-shift conditions and Youden effective-cost equivalence OK")


# Prevalence-driven policy crossover while class-conditional ROC rates stay fixed.
# This differs from the earlier PPV thought experiment: we REOPTIMISE the rule.
# The six strictly ordered artificial labels have seven possible prefix cutoffs.
# For the two undominated cutoffs, L1(p) = 4p/3 and L4(p) = (1-p)/3
# under C_FN=2 and C_FP=1. All others are more costly for 0<p<1.
assert math.isclose(1 / (2 * 2 + 1), 0.2)
assert math.isclose(4 * .1 / 3, 2 / 15)
assert math.isclose((1 - .1) / 3, .3)
assert math.isclose(4 * .4 / 3, 8 / 15)
assert math.isclose((1 - .4) / 3, .2)
for i in range(1, 1000):
    deployment_p = i / 1000
    losses = []
    for k in range(len(decision_labels) + 1):
        tp = sum(decision_labels[:k])
        fp = k - tp
        losses.append(2 * deployment_p * (1 - tp / 3)
                      + (1 - deployment_p) * fp / 3)
    assert math.isclose(losses[1], 4 * deployment_p / 3)
    assert math.isclose(losses[4], (1 - deployment_p) / 3)
    optimum = min(losses)
    expected = [1] if i < 200 else [4] if i > 200 else [1, 4]
    actual = [k for k, loss in enumerate(losses)
              if math.isclose(loss, optimum, abs_tol=1e-12)]
    assert actual == expected, (i, actual, expected)

asset_root = Path("docs/assets/concept-animations")
policy_motion = (asset_root / "roc-prior-policy-motion.svg").read_text(encoding="utf-8")
policy_still = (asset_root / "roc-prior-policy-still.svg").read_text(encoding="utf-8")
assert "prefers-reduced-motion" in policy_motion
assert 'class="moving"' in policy_motion
assert "<animateMotion " in policy_motion and "<animate" not in policy_still
for filename, language_marker in (
    ("roc-auc.md", "Animated cutoff switching under a prior shift"),
    ("roc-auc.zh-TW.md", "先驗比例漂移如何切換最低成本門檻"),
):
    page = (shared_dir / filename).read_text(encoding="utf-8")
    assert language_marker in page
    assert 'src="../../../../assets/concept-animations/roc-prior-policy-still.svg"' in page
    assert 'data-motion-src="../../../../assets/concept-animations/roc-prior-policy-motion.svg"' in page
    assert "[GitHub static preview]" in page or "[GitHub 靜態預覽]" in page
    assert "p^*=\\frac{C_{FP}}{2C_{FN}+C_{FP}}" in page
    assert "\n$$\nL(k)=w[1-J(k)].\n$$\n" in page
print("Prevalence-driven policy crossover: all 999 positive base rates and seven cutoffs OK")


# Bilingual decision-workshop navigation must connect all three original
# motion/still pairs without treating their unrelated synthetic inputs as one sample.
# The overview distinguishes a held-fixed rule from re-optimised deployment rules.
for filename, markers in (
    ("index.md", ("Three linked ROC decision experiments", "pure prior-probability shift",
                  "20% prevalence", "FN cost 4.5")),
    ("index.zh-TW.md", ("三組相互對照的 ROC 決策動畫", "純先驗比例漂移",
                        "盛行率 20%", "FN 成本 4.5")),
):
    overview = (shared_dir / filename).read_text(encoding="utf-8")
    for marker in markers:
        assert marker in overview, (filename, marker)
    for stem in ("roc-pr-shift", "roc-youden-cost", "roc-prior-policy"):
        for suffix in ("-motion.svg", "-still.svg"):
            asset_name = stem + suffix
            assert f"../../../../assets/concept-animations/{asset_name}" in overview
            assert (asset_root / asset_name).is_file(), (filename, asset_name)
    assert "100" in overview and "ROC-AUC" in overview

for filename, expected in (
    ("roc-auc.md", "pure prior-probability shift"),
    ("roc-auc.zh-TW.md", "純先驗比例漂移"),
):
    chapter = (shared_dir / filename).read_text(encoding="utf-8")
    assert expected in chapter
    assert ("finite samples" in chapter) if filename == "roc-auc.md" else ("抽樣波動" in chapter)

# Distinguish population invariance from precision changes at fixed conditional rates.
for prevalence in (.05, .1, .2, .4, .6):
    tpr, fpr = .8, .1  # fixed conditional rates; synthetic
    positive_mass = tpr * prevalence
    predicted_positive_mass = positive_mass + fpr * (1 - prevalence)
    assert math.isclose(positive_mass / predicted_positive_mass, shifted_ppv(prevalence))
assert math.isclose(shifted_ppv(.05), 8 / 27)
assert math.isclose(shifted_ppv(.6), 12 / 13)
print("Bilingual ROC decision-workshop navigation and prior-shift caveats OK")

# ROC secant-cost comparison regression: k=4 versus k=1 under prior shift.
# This is an exact identity for the synthetic six-case score ordering.
# The deployment prevalence is independent of the three-positive/three-negative sample.
for c_fn in (0.5, 1.0, 2.0, 5.0, 10.0):
    for c_fp in (0.5, 1.0, 3.0):
        for i in range(1, 100):
            p = i / 100
            loss_k1 = c_fn * p * (2 / 3)
            loss_k4 = c_fp * (1 - p) / 3
            delta_tpr, delta_fpr = 2 / 3, 1 / 3
            analytic_difference = (-c_fn * p * delta_tpr +
                                   c_fp * (1 - p) * delta_fpr)
            assert math.isclose(loss_k4 - loss_k1, analytic_difference,
                                rel_tol=1e-12, abs_tol=1e-12)
            better_k4 = (c_fn * p * delta_tpr >
                         c_fp * (1 - p) * delta_fpr)
            assert better_k4 == (loss_k4 < loss_k1)
            crossover = c_fp / (2 * c_fn + c_fp)
            assert better_k4 == (p > crossover)
for name in ("index.md", "index.zh-TW.md"):
    page = (shared_dir / name).read_text(encoding="utf-8")
    # Cross-language anchors are brittle; style guide links directly to the page.
    assert "](roc-auc.md#" not in page
    assert page.count("](roc-auc.md)") >= 3
for name in ("roc-auc.md", "roc-auc.zh-TW.md"):
    page = (shared_dir / name).read_text(encoding="utf-8")
    assert r"\Delta TPR" in page and r"\Delta FPR" in page
    assert r"2C_{FN}p>C_{FP}(1-p)" in page
for name in ("roc-auc.md", "roc-auc.zh-TW.md"):
    page = (shared_dir / name).read_text(encoding="utf-8")
    assert "\n$$\n\\begin{aligned}\nL(4;p)-L(1;p)" in page
print("ROC secant-cost comparison regression: 1485 scenarios OK")

# Independent randomized-policy regression, tied to two undominated ROC cutoffs.
# A distinct pre-existing motion illustrates interpolation with different rates.
for prevalence in (.10, .20, .40):
    loss1, loss4 = 4 * prevalence / 3, (1 - prevalence) / 3
    for step in range(101):
        lam = step / 100
        tpr, fpr = (1 + 2 * lam) / 3, lam / 3
        mixed = (1 - lam) * loss1 + lam * loss4
        direct = 2 * prevalence * (1 - tpr) + (1 - prevalence) * fpr
        assert math.isclose(mixed, direct, abs_tol=1e-12)
        assert mixed >= min(loss1, loss4) - 1e-12
        if prevalence == .20:
            assert math.isclose(mixed, 4 / 15, abs_tol=1e-12)
assert math.isclose((4 * .10 / 3 + .90 / 3) / 2, 13 / 60)
assert math.isclose((4 * .40 / 3 + .60 / 3) / 2, 11 / 30)
for filename, marker in (
    ("roc-auc.md", "Why randomizing between optimal cutoffs cannot beat both endpoints"),
    ("roc-auc.zh-TW.md", "為什麼隨機混合門檻不會同時勝過兩端策略"),
):
    content = (shared_dir / filename).read_text(encoding="utf-8")
    assert marker in content
    assert r"L_{\lambda}(p)=(1-\lambda)" in content
    for suffix in ("-motion.svg", "-still.svg"):
        assert "roc-randomized-operating-mix" + suffix in content
print("ROC randomized-policy interpolation: 303 cost/rate states OK")


# An FPR budget can make a randomized policy preferable to feasible deterministic
# cutoffs, even though it cannot beat the unconstrained minimum-loss endpoint.
cap, deployment_p = 1 / 6, .40
feasible_deterministic = []
for k in range(7):
    tp = sum(decision_labels[:k])
    fp = k - tp
    fpr, tpr = fp / 3, tp / 3
    if fpr <= cap + 1e-12:
        feasible_deterministic.append((k, 2 * deployment_p * (1-tpr) + (1-deployment_p)*fpr))
assert [k for k, _ in feasible_deterministic] == [0, 1]
assert min(feasible_deterministic, key=lambda item: item[1])[0] == 1
for step in range(501):
    lam = step / 1000
    tpr, fpr = (1+2*lam)/3, lam/3
    loss = 2*deployment_p*(1-tpr)+(1-deployment_p)*fpr
    assert fpr <= cap + 1e-12
    assert loss >= 11/30 - 1e-12
    assert math.isclose(loss, (1-lam)*8/15+lam/5, abs_tol=1e-12)
assert math.isclose((1+2*.5)/3, 2/3)
assert math.isclose(2*deployment_p*(1-2/3)+(1-deployment_p)/6, 11/30)
assert 11/30 < 8/15
for name, marker in (
    ("roc-auc.md", "When an FPR budget makes a mixture useful"),
    ("roc-auc.zh-TW.md", "有誤報率上限時，混合策略如何變得有用"),
):
    page = (shared_dir / name).read_text(encoding="utf-8")
    assert marker in page
    assert "11/30" in page and "8/15" in page
    assert r"\mathrm{FPR}_{\lambda}=\frac{\lambda}{3}" in page
    assert "\n$\n" not in page
    assert "\n$$\nL_{\\lambda}(p)=" in page
print("Constrained ROC mixture: 501 budget-feasible states, 7 deterministic cutoffs and bilingual display maths OK")

# An animated FPR budget must use the SAME synthetic conditional rates
# and cost assumptions as the constrained-policy derivation, not the
# different operating points shown by the previously linked generic animation.
fpr_cap = 1 / 6
for i in range(501):
    mixing_probability = i / 1000
    true_positive_rate = (1 + 2 * mixing_probability) / 3
    false_positive_rate = mixing_probability / 3
    expected_cost = .8 * (1 - true_positive_rate) + .6 * false_positive_rate
    assert false_positive_rate <= fpr_cap + 1e-12
    assert expected_cost >= 11 / 30 - 1e-12
    assert math.isclose(expected_cost, 8 / 15 - mixing_probability / 3,
                        abs_tol=1e-12)
assert math.isclose(.8 * (1 - 2/3) + .6 / 6, 11/30)
for kind in ("motion", "still"):
    path = asset_root / f"roc-fpr-budget-mix-{kind}.svg"
    source = path.read_text(encoding="utf-8")
    assert 'viewBox="0 0 640 360"' in source
    assert "false-positive-rate budget" in source
    assert 'x1="473.5"' in source  # budget at lambda=0.5
    assert "0.367" in source and "0.533" in source
    assert ("<animateMotion" in source) == (kind == "motion")
    assert ("prefers-reduced-motion" in source)
for filename, label in (
    ("roc-auc.md", "FPR-constrained randomized ROC policy"),
    ("roc-auc.zh-TW.md", "受 FPR 上限約束的隨機 ROC 決策規則"),
):
    page = (shared_dir / filename).read_text(encoding="utf-8")
    assert label in page
    assert 'src="../../../../assets/concept-animations/roc-fpr-budget-mix-still.svg"' in page
    assert 'data-motion-src="../../../../assets/concept-animations/roc-fpr-budget-mix-motion.svg"' in page
    assert "11/30" in page and "1/6" in page
print("ROC FPR-budget motion: 501 continuous feasible policies, bilingual exact-source links OK")

# Population FPR constraints do not bound the observed error fraction in
# every independent finite batch. Three negatives and one false alarm imply
# empirical FPR >= 1/3, exceeding the 1/6 assumed conditional rate.
from fractions import Fraction
finite_fpr = Fraction(1, 6)
prob_over_budget = 1 - (1 - finite_fpr) ** 3
assert prob_over_budget == Fraction(91, 216)
assert Fraction(1, 3) > finite_fpr
for filename in ("roc-auc.md", "roc-auc.zh-TW.md"):
    page = (shared_dir / filename).read_text(encoding="utf-8")
    assert "91/216" in page
    assert r"\widehat{\mathrm{FPR}}" in page
    assert "42.1%" in page
print("Finite-batch FPR risk: exact binomial probability 91/216 OK")

# Discrete outcome animation and exact binomial masses: equal-duration visuals
# illustrate possible counts, NOT samples drawn in proportion to probabilities.
from math import comb
binomial_counts = [Fraction(comb(3, k) * 5**(3-k), 6**3) for k in range(4)]
assert binomial_counts == [Fraction(125,216), Fraction(75,216),
                           Fraction(15,216), Fraction(1,216)]
assert sum(binomial_counts) == 1
assert sum(binomial_counts[1:]) == Fraction(91,216)
assert [Fraction(k,3) > finite_fpr for k in range(4)] == [False,True,True,True]
for kind in ("motion","still"):
    path = asset_root / f"roc-fpr-batch-{kind}.svg"
    source = path.read_text(encoding="utf-8")
    assert 'viewBox="0 0 640 360"' in source
    assert "125, 75, 15 and one out of 216" in source
    assert "P(K ≥ 1) = 91/216 = 42.1%" in source
    assert (source.count('calcMode="discrete"') == 4) == (kind == "motion")
    assert ("<animate " in source) == (kind == "motion")
    if kind == "motion":
        assert "prefers-reduced-motion" in source
        assert 'class="still"' in source and source.count('class="moving"') == 4
for filename, title in (
    ("roc-auc.md", "Animated finite-batch FPR: four possible false-alarm counts"),
    ("roc-auc.zh-TW.md", "有限批次 FPR 分布動畫：母體限制與四種可能的誤報數"),
):
    page = (shared_dir / filename).read_text(encoding="utf-8")
    assert title in page
    assert 'src="../../../../assets/concept-animations/roc-fpr-batch-still.svg"' in page
    assert 'data-motion-src="../../../../assets/concept-animations/roc-fpr-batch-motion.svg"' in page
    assert "125/216" in page and "91/216" in page
    assert "\n$$\nP(K=k)=" in page
print("Finite-batch binomial outcomes: 4 exact masses, 4 states and bilingual fallback links OK")


# Exact one-sided Clopper-Pearson upper FPR bound after zero false alarms.
# Invert the P(K=0) likelihood; repeated-sampling coverage, not a posterior.
def zero_alarm_upper(n):
    return 1 - 0.05 ** (1 / n)

assert zero_alarm_upper(16) > 1/6 > zero_alarm_upper(17)
assert math.ceil(math.log(0.05) / math.log(5/6)) == 17
for n, expected_percent in ((3,63.2),(12,22.1),(17,16.2),(30,9.5)):
    bound = zero_alarm_upper(n)
    assert math.isclose(round(bound * 100, 1),expected_percent,abs_tol=1e-12)
    assert math.isclose((1-bound)**n,0.05,rel_tol=1e-12)
assert all(zero_alarm_upper(n+1) < zero_alarm_upper(n) for n in range(3,60))
for kind in ("motion","still"):
    svg = (asset_root / f"roc-fpr-zero-alarms-{kind}.svg").read_text(encoding="utf-8")
    assert 'viewBox="0 0 640 360"' in svg
    assert "Zero alarms do not imply zero FPR" in svg
    assert 'class="still"' in svg if kind=="motion" else "<animate " not in svg
    assert ('<animate ' in svg) == (kind=="motion")
    if kind=="motion":
        assert svg.count('calcMode="discrete"') == 4
        assert "prefers-reduced-motion" in svg
for filename,heading in (
    ("roc-auc.md","Zero observed alarms and the exact upper FPR limit"),
    ("roc-auc.zh-TW.md","零筆誤報仍無法證明母體 FPR 為零"),
):
    page = (shared_dir / filename).read_text(encoding="utf-8")
    assert heading in page
    assert 'src="../../../../assets/concept-animations/roc-fpr-zero-alarms-still.svg"' in page
    assert 'data-motion-src="../../../../assets/concept-animations/roc-fpr-zero-alarms-motion.svg"' in page
    assert r"U_{0.95}(n)=1-0.05^{1/n}" in page
    assert "10.1093/biomet/26.4.404" in page
print("Exact zero-alarm FPR upper-bound and bilingual motion assets OK")

# Dependence changes the distribution of batch counts without changing any
# marginal false-alarm probability. The exact fractions are independent of SVG.
p = Fraction(1, 6)
independent = [Fraction(math.comb(3, k) * 5**(3-k), 216) for k in range(4)]
shared = [Fraction(5, 6), Fraction(0), Fraction(0), Fraction(1, 6)]
assert independent == [Fraction(125,216), Fraction(75,216), Fraction(15,216), Fraction(1,216)]
assert sum(independent) == sum(shared) == 1
for masses in (independent, shared):
    assert sum(Fraction(k, 3) * masses[k] for k in range(4)) == p
assert sum(independent[1:]) == Fraction(91, 216)
assert sum(shared[1:]) == Fraction(1, 6)
assert sum((Fraction(k,3)-p)**2*independent[k] for k in range(4)) == Fraction(5,108)
assert sum((Fraction(k,3)-p)**2*shared[k] for k in range(4)) == Fraction(5,36)
for kind in ("motion", "still"):
    svg = (asset_root / f"roc-fpr-dependence-{kind}.svg").read_text(encoding="utf-8")
    assert 'viewBox="0 0 640 360"' in svg
    assert "Different" in svg or "different batch risk" in svg
    assert (svg.count("<animate ") > 0) == (kind == "motion")
    assert "prefers-reduced-motion" in svg
for name, heading in (
    ("roc-auc.md", "When false alarms are dependent"),
    ("roc-auc.zh-TW.md", "誤報之間不獨立時會發生什麼事"),
):
    page = (shared_dir / name).read_text(encoding="utf-8")
    assert heading in page
    assert 'src="../../../../assets/concept-animations/roc-fpr-dependence-still.svg"' in page
    assert 'data-motion-src="../../../../assets/concept-animations/roc-fpr-dependence-motion.svg"' in page
    assert "91/216" in page and "5/108" in page and "5/36" in page
print("Dependent false alarms: exact marginal, tail and variance identities; bilingual fallback and motion assets OK")


# Zero observed alarms are thirty *records*, not thirty independent draws,
# when every false-alarm indicator is a copy of one shared Bernoulli shock.
# Only under the iid construction is the usual n=30 CP upper bound valid.
from fractions import Fraction as ExactFraction
shared_p = ExactFraction(1, 6)
alpha = .05
n_records = 30
zero_iid = (1 - shared_p) ** n_records
zero_shared = 1 - shared_p
upper_iid_if_zero = 1 - alpha ** (1 / n_records)
upper_shared_if_zero = 1 - alpha
assert zero_iid < ExactFraction(1, 200)
assert zero_shared == ExactFraction(5, 6)
assert math.isclose(upper_iid_if_zero, .09503385285530419, abs_tol=1e-14)
assert upper_iid_if_zero < shared_p < upper_shared_if_zero
# Under the fully dependent model K is either 0 or 30. The mistaken iid
# interval fails exactly in the K=0 state; actual coverage is 1/6, not 95%.
naive_coverage = (1 - float(zero_shared)) * 1 + float(zero_shared) * 0
assert math.isclose(naive_coverage, 1 / 6, abs_tol=1e-14)
# Under the correctly specified single-shock model, both outcome-specific
# one-sided 95% CP upper bounds (.95 for 0, 1 for 1) include p=1/6.
assert all(shared_p <= bound for bound in (upper_shared_if_zero, 1.))
for kind in ("motion", "still"):
    source = (asset_root / f"roc-fpr-shared-bound-{kind}.svg").read_text(encoding="utf-8")
    assert 'viewBox="0 0 640 360"' in source
    assert "Zero alarms do not yield the same evidence under dependence" in source
    assert "One shared shock" in source
    assert "95%" in source and "9.5%" in source
    assert ("<animate " in source) == (kind == "motion")
    if kind == "motion":
        assert "prefers-reduced-motion" in source and 'class="still"' in source
for filename, title in (
    ("roc-auc.md", "why thirty fully dependent negatives are not thirty independent trials"),
    ("roc-auc.zh-TW.md", "三十筆完全相依資料，不等於三十次獨立試驗"),
):
    page = (shared_dir / filename).read_text(encoding="utf-8")
    assert title in page
    assert 'src="../../../../assets/concept-animations/roc-fpr-shared-bound-still.svg"' in page
    assert 'data-motion-src="../../../../assets/concept-animations/roc-fpr-shared-bound-motion.svg"' in page
    assert r"U_{\mathrm{iid}}&=1-0.05^{1/30}" in page
    assert r"U_{\mathrm{shared}}&=1-0.05=0.95" in page
    assert "\n$$\n\\begin{aligned}\nP_p(K=0" in page
print("Shared-shock versus iid zero-alarm bounds: analytic coverage and bilingual motion regression OK")


# Explicit batch-mixture interpretation of the intermediate dependence frames:
# choose one mechanism for the whole batch, then draw iid or one shared shock.
# The mixture weight is the intraclass correlation for THIS constructed model,
# not an arbitrary correlation-to-distribution conversion.
from math import comb as binom_comb
batch_n, marginal_p = 3, Fraction(1, 6)
iid_mass = [Fraction(binom_comb(batch_n, k) * 5 ** (batch_n-k), 216)
            for k in range(batch_n + 1)]
shared_mass = [Fraction(5,6), Fraction(0), Fraction(0), Fraction(1,6)]
for rho_step in range(101):
    rho = Fraction(rho_step, 100)
    mass = [(1-rho)*iid_mass[k] + rho*shared_mass[k]
            for k in range(batch_n+1)]
    assert sum(mass) == 1
    assert sum(Fraction(k,3)*mass[k] for k in range(4)) == marginal_p
    mean_variance = sum((Fraction(k,3)-marginal_p)**2*mass[k]
                        for k in range(4))
    assert mean_variance == Fraction(5,108)*(1+2*rho)
    assert sum(mass[1:]) == (1-rho)*Fraction(91,216)+rho*Fraction(1,6)
    assert Fraction(3,1+2*rho) == Fraction(3)/(1+2*rho)
assert (sum(((iid_mass[k]+shared_mass[k])/2) for k in range(1,4))
        == Fraction(127,432))
assert Fraction(5,108)*2 == Fraction(5,54)
assert Fraction(30)/(1+29*Fraction(1,2)) == Fraction(60,31)
for file,heading in (
    ("roc-auc.md", "Between independence and one shared shock: the intermediate frames"),
    ("roc-auc.zh-TW.md", "獨立與共同衝擊之間：明確的批次混合模型"),
):
    text_page = (shared_dir/file).read_text(encoding="utf-8")
    assert heading in text_page
    for exact in ("127/432", "5/54", "60/31", "Clopper"):
        assert exact in text_page, (file,exact)
    assert r"n_{\mathrm{eff,var}}&=\frac{3}{1+2\rho}" in text_page
    assert ("\n$$\n" + r"P_{\rho}(K=k)=") in text_page
    assert ("\n$$\n" + r"\begin{aligned}" + "\n" + r"P_{\rho}(K\geq1)") in text_page
print("Batch-mixture ROC dependence: 101 exact joint models, variance-equivalent counts and bilingual explanations OK")


# Whole-batch mechanism mixing at n=30: the iid one-sided CP 95% rule
# mis-covers the true p=1/6 when K=0 or K=1. At K>=2 its upper
# endpoint covers that value. This is about one-sided upper coverage,
# not a posterior probability or a nominal confidence promise under shift.
from math import comb as coverage_comb
p30 = Fraction(1, 6)
n30 = 30
iid_zero = (1-p30)**n30
iid_one = n30*p30*(1-p30)**(n30-1)
iid_bad = iid_zero + iid_one
# For k=1 and k=2, the binomial lower-tail probability at p determines
# whether the inverted 95% upper limit falls below or above the true p.
assert float(iid_bad) < .05 < float(iid_bad + Fraction(coverage_comb(n30, 2))*p30**2*(1-p30)**(n30-2))
for step in range(101):
    rho = Fraction(step, 100)
    # Draw ONE mechanism for the entire batch; not independent per record.
    p_zero = (1-rho)*iid_zero + rho*(1-p30)
    actual_coverage = (1-rho)*(1-iid_bad) + rho*p30
    assert p_zero == (1-rho)*(Fraction(5,6)**30) + rho*Fraction(5,6)
    assert actual_coverage == 1 - ((1-rho)*iid_bad + rho*(1-p30))
    assert 0 <= p_zero <= 1 and 0 <= actual_coverage <= 1
    if step==0:
        assert .9705 < float(actual_coverage) < .9706
    if step==50:
        assert .5685 < float(actual_coverage) < .5687
    if step==100:
        assert actual_coverage == Fraction(1, 6)
for filename, heading in (
    ("roc-auc.md", "Coverage erosion between independent and shared-shock batches"),
    ("roc-auc.zh-TW.md", "從獨立到共同衝擊：信賴上界的實際涵蓋率"),
):
    content = (shared_dir / filename).read_text(encoding="utf-8")
    assert heading in content
    assert r"P_{\rho}(K=0)" in content
    assert r"\mathrm{Coverage}_{\rho}" in content
    assert "\n$$\n" + r"\begin{aligned}" in content
print("Thirty-case shared-shock mixture: 101 exact models, zero-alarm likelihood and actual CP upper coverage OK")


# Coverage visual: explicit original geometry, GitHub fallback and bilingual reuse.
for kind in ("motion", "still"):
    source = (asset_root / f"roc-fpr-mix-coverage-{kind}.svg").read_text(encoding="utf-8")
    assert 'viewBox="0 0 640 360"' in source
    assert "Actual coverage" in source and "Zero-alarm probability" in source
    assert "95%" in source and "one batch-level mixture switch" in source
    assert ("<animate " in source) == (kind == "motion")
    assert "prefers-reduced-motion" in source
for name in ("roc-auc.md", "roc-auc.zh-TW.md"):
    content = (shared_dir / name).read_text(encoding="utf-8")
    assert 'src="../../../../assets/concept-animations/roc-fpr-mix-coverage-still.svg"' in content
    assert 'data-motion-src="../../../../assets/concept-animations/roc-fpr-mix-coverage-motion.svg"' in content
    assert 'data-source-asset-urls' in content
    assert "56.86" in content
print("FPR dependent-coverage motion and bilingual source/fallback paths OK")


# A prespecified 17-negative zero-alarm test: exact finite-sample operating
# characteristics. These are probabilities under hypothetical populations.
from fractions import Fraction as PowerFraction
cap = PowerFraction(1, 6)
n_cert = 17
alpha_cert = PowerFraction(1, 20)
assert (1-cap)**16 > alpha_cert >= (1-cap)**17
assert (1-cap)**17 + n_cert*cap*(1-cap)**(n_cert-1) > alpha_cert
for p_cert, target in ((.01, .842943),(.05, .418120),(.10, .166772),(1/6, .045073)):
    assert math.isclose((1-p_cert)**n_cert, target, abs_tol=1e-6)
single_boundary = (1-cap)**n_cert
assert single_boundary < alpha_cert
for tries in (1, 5, 10, 20):
    any_pass = 1-(1-single_boundary)**tries
    assert any_pass >= single_boundary
assert .3694 < float(1-(1-single_boundary)**10) < .3696
assert all((1-PowerFraction(k,1000))**n_cert <= single_boundary
           for k in range(167,1000))
for kind in ("motion", "still"):
    svg = (asset_root / f"roc-fpr-certificate-power-{kind}.svg").read_text(encoding="utf-8")
    assert 'viewBox="0 0 640 360"' in svg
    assert 'P(pass) = (1 - p)^17' in svg
    assert ("<animate " in svg) == (kind == "motion")
    assert "prefers-reduced-motion" in svg
for fname, heading in (
    ("roc-auc.md", "Zero-alarm certification power and repeated attempts"),
    ("roc-auc.zh-TW.md", "零誤報檢驗的通過機率與重複測試問題"),
):
    s = (shared_dir / fname).read_text(encoding="utf-8")
    assert heading in s
    assert 'src="../../../../assets/concept-animations/roc-fpr-certificate-power-still.svg"' in s
    assert 'data-motion-src="../../../../assets/concept-animations/roc-fpr-certificate-power-motion.svg"' in s
    assert "36.95%" in s and "84.3%" in s
    assert "\n$$\n" + r"P_p(\mathrm{pass})" in s
print("Zero-alarm certification: fixed-n power, repeated independent attempts, bilingual fallback OK")


# Repeated zero-alarm FPR testing: exact boundary family-wise risk and
# Bonferroni allocation, with ten prespecified tests and 30 negatives per test.
from fractions import Fraction as RetryFraction
retry_p0 = RetryFraction(1, 6)
retry_alpha = RetryFraction(1, 20)
retry_alloc = retry_alpha / 10
assert (1-retry_p0)**17 < retry_alpha <= (1-retry_p0)**16
assert (1-retry_p0)**30 < retry_alloc < (1-retry_p0)**29
assert ((1-retry_p0)**30+30*retry_p0*(1-retry_p0)**29) > retry_alloc
for m_retry in range(1, 11):
    naive = 1-(1-(1-retry_p0)**17)**m_retry
    corrected = 1-(1-(1-retry_p0)**30)**m_retry
    assert 0 < corrected < naive < 1
    assert corrected <= m_retry*retry_alloc <= retry_alpha
    if m_retry == 10:
        assert .3694 < float(naive) < .3696
        assert .0413 < float(corrected) < .0414
for kind in ("motion", "still"):
    svg = (asset_root / f"roc-fpr-retries-{kind}.svg").read_text(encoding="utf-8")
    assert 'viewBox="0 0 640 360"' in svg
    for phrase in ("Bonferroni", "36.95%", "4.13%", "Family-wise"):
        assert phrase in svg
    assert ("<animate " in svg) == (kind == "motion")
    assert "prefers-reduced-motion" in svg
for name, heading in (
    ("roc-auc.md", "Animation: controlling false passes across ten prespecified tests"),
    ("roc-auc.zh-TW.md", "動畫：預先指定十次檢驗時的整體錯誤通過率控制"),
):
    page = (shared_dir / name).read_text(encoding="utf-8")
    assert heading in page
    assert 'src="../../../../assets/concept-animations/roc-fpr-retries-still.svg"' in page
    assert 'data-motion-src="../../../../assets/concept-animations/roc-fpr-retries-motion.svg"' in page
    assert "36.95%" in page and "4.13%" in page
    assert "\n$$\n" + r"R_n(m)=" in page
print("Repeated FPR certification: ten exact test counts, Bonferroni n=30, bilingual paths OK")


# Six invented scores: one positive and two negatives share 0.70.
# A score-only threshold cannot split this block; a diagonal in a ROC
# plot is interpolation between whole decision rules.
tie_cases = ((.90, 1), (.70, 1), (.70, 0), (.70, 0), (.40, 0), (.20, 0))
tie_pos = [score for score, label in tie_cases if label]
tie_neg = [score for score, label in tie_cases if not label]
tie_auc = sum((1 if pos > neg else .5 if pos == neg else 0)
              for pos in tie_pos for neg in tie_neg) / (len(tie_pos)*len(tie_neg))
assert math.isclose(tie_auc, 7/8)
tie_points = []
for threshold in (1, .90, .70, .40, .20):
    tp = sum(label and score >= threshold for score, label in tie_cases)
    fp = sum(not label and score >= threshold for score, label in tie_cases)
    tie_points.append((fp/4, tp/2))
assert tie_points == [(0,0),(0,.5),(.5,1),(.75,1),(1,1)]
# The two .70 endpoints differ in both rates: no score threshold yields (.25,.75).
assert (.25,.75) not in tie_points
tie_area = sum((r[0]-l[0])*(r[1]+l[1])/2
               for l, r in zip(tie_points, tie_points[1:]))
assert math.isclose(tie_area,tie_auc)
tie_dir = Path("docs/assets/concept-animations")
tie_motion=(tie_dir/"roc-tie-group-step-motion.svg").read_text(encoding="utf-8")
tie_still=(tie_dir/"roc-tie-group-step-still.svg").read_text(encoding="utf-8")
assert 'viewBox="0 0 640 360"' in tie_motion and 'viewBox="0 0 640 360"' in tie_still
assert 'calcMode="discrete"' in tie_motion and 'prefers-reduced-motion' in tie_motion
assert '<animate ' in tie_motion and '<animate ' not in tie_still
for lang in ("roc-auc.md","roc-auc.zh-TW.md"):
    page=(Path("docs/theory/evaluation/metrics/classification")/lang).read_text(encoding="utf-8")
    assert "roc-tie-group-step-motion.svg" in page and "roc-tie-group-step-still.svg" in page
print("Tied-threshold ROC endpoints, exact pairwise AUC, bilingual fallback OK")


# AUC is invariant to strictly increasing transforms, but not to a
# many-to-one score quantizer. Check every positive-negative comparison.
quant_cases=((0.90,1),(0.60,1),(0.80,0),(0.30,0))
def _pair_auc(positives,negatives):
    return sum(1 if p>n else 0.5 if p==n else 0
               for p in positives for n in negatives)/(len(positives)*len(negatives))
raw_pos=[s for s,y in quant_cases if y]
raw_neg=[s for s,y in quant_cases if not y]
assert _pair_auc(raw_pos,raw_neg)==0.75
# All four examples avoid rounding half-way ambiguity.
quant_pos=[round(2*s)/2 for s in raw_pos]
quant_neg=[round(2*s)/2 for s in raw_neg]
assert quant_pos==[1.0,0.5] and quant_neg==[1.0,0.5]
assert _pair_auc(quant_pos,quant_neg)==0.5
assert sorted(quant_pos+quant_neg)==[0.5,0.5,1.0,1.0]
assert _pair_auc([s**3 for s in raw_pos],[s**3 for s in raw_neg])==0.75
# Conversely, coarsening a misordered pair can raise its pairwise credit.
assert _pair_auc([0.49],[0.51])==0 and _pair_auc([0.5],[0.5])==0.5
for variant in ("motion","still"):
    quant_svg=(asset_root / f"roc-score-quantization-{variant}.svg").read_text(encoding="utf-8")
    assert 'viewBox="0 0 640 360"' in quant_svg
    assert "0.75" in quant_svg and "0.50" in quant_svg
    assert ("<animate " in quant_svg)==(variant=="motion")
    assert ("prefers-reduced-motion" in quant_svg)==(variant=="motion")
for locale in ("roc-auc.md","roc-auc.zh-TW.md"):
    chapter=(shared_dir/locale).read_text(encoding="utf-8")
    assert 'src="../../../../assets/concept-animations/roc-score-quantization-still.svg"' in chapter
    assert 'data-motion-src="../../../../assets/concept-animations/roc-score-quantization-motion.svg"' in chapter
    assert "0.75" in chapter and "0.50" in chapter
print("Score quantization: strict ranks versus ties, exact pairwise AUC, bilingual fallback OK")

# F1 macro / support-weighted / micro aggregation and the noncommuting
# harmonic-mean shortcut. Synthetic single-label 90:10 confusion counts.
for k in range(11):
    fa = 180 / (190-k)
    fb = 2*k / (10+k)
    macro = (fa+fb)/2
    weighted = .9*fa+.1*fb
    micro = (90+k)/100
    pa = 90/(100-k)
    pb = float(k>0)  # zero_division=0 when no B is predicted
    avgp=(pa+pb)/2
    avgr=(1+k/10)/2
    shortcut=2*avgp*avgr/(avgp+avgr)
    assert math.isclose(macro,(fa+fb)/2)
    assert math.isclose(weighted,(90*fa+10*fb)/100)
    assert math.isclose(micro,(90+k)/100)
    if k in (1,2,5,9):
        assert not math.isclose(shortcut,macro)
assert math.isclose(180/185, .972972972972973)
assert math.isclose(.5*(180/185 + 10/15), .8198198198198199)
assert math.isclose(.9*180/185 + .1*10/15, .9423423423423424)
assert math.isclose(2*((90/95+1)/2)*.75/(((90/95+1)/2)+.75),.847328244274809)
for variant in ('motion','still'):
    image=(asset_root/f'f1-averaging-rules-{variant}.svg').read_text(encoding='utf-8')
    assert 'viewBox="0 0 640 360"' in image
    assert ('<animate ' in image)==(variant=='motion')
    assert ('prefers-reduced-motion' in image)==(variant=='motion')
for locale in ('f1.md','f1.zh-TW.md'):
    page=(shared_dir/locale).read_text(encoding='utf-8')
    assert 'src="../../../../assets/concept-animations/f1-averaging-rules-still.svg"' in page
    assert 'data-motion-src="../../../../assets/concept-animations/f1-averaging-rules-motion.svg"' in page
print("F1 support-weighted versus macro/micro and noncommuting aggregation verified")


# Multilabel aggregation counterexample: pooled counts deliberately match,
# but row-wise F1 and exact-match accuracy rank the two scenarios differently.
from fractions import Fraction as MultiFraction
ml_truth=(3,1,2,3) # Bitmasks for labels A/B; no empty ground-truth sets.
ml_a=(3,0,1,3)
ml_b=(1,1,3,1)
def _ml_scores(predictions):
    tp=sum((t & p).bit_count() for t,p in zip(ml_truth,predictions))
    fp=sum((p & ~t & 3).bit_count() for t,p in zip(ml_truth,predictions))
    fn=sum((t & ~p & 3).bit_count() for t,p in zip(ml_truth,predictions))
    micro=MultiFraction(2*tp, 2*tp+fp+fn)
    per_record=[MultiFraction(2*(t & p).bit_count(),t.bit_count()+p.bit_count())
                for t,p in zip(ml_truth,predictions)]
    samples=sum(per_record,MultiFraction()) / len(ml_truth)
    exact=MultiFraction(sum(t==p for t,p in zip(ml_truth,predictions)),len(ml_truth))
    return (tp,fp,fn),micro,per_record,samples,exact
ma=_ml_scores(ml_a)
mb=_ml_scores(ml_b)
assert ma[0]==mb[0]==(4,1,2)
assert ma[1]==mb[1]==MultiFraction(8,11)
assert ma[2]==[MultiFraction(1),MultiFraction(0),MultiFraction(0),MultiFraction(1)]
assert mb[2]==[MultiFraction(2,3),MultiFraction(1),MultiFraction(2,3),MultiFraction(2,3)]
assert ma[3:]==(MultiFraction(1,2),MultiFraction(1,2))
assert mb[3:]==(MultiFraction(3,4),MultiFraction(1,4))
for kind in ('motion','still'):
    svg=(asset_root / f'f1-multilabel-aggregation-{kind}.svg').read_text(encoding='utf-8')
    assert 'viewBox="0 0 640 360"' in svg
    assert 'TP 4 · FP 1 · FN 2' in svg
    assert '0.727' in svg and '0.750' in svg and '0.250' in svg
    assert ('<animate ' in svg)==(kind=='motion')
    assert ('prefers-reduced-motion' in svg)==(kind=='motion') or kind=='still'
for filename in ('f1.md','f1.zh-TW.md'):
    lesson=(shared_dir / filename).read_text(encoding='utf-8')
    assert 'src="../../../../assets/concept-animations/f1-multilabel-aggregation-still.svg"' in lesson
    assert 'data-motion-src="../../../../assets/concept-animations/f1-multilabel-aggregation-motion.svg"' in lesson
    assert '\\frac{8}{11}' in lesson
    assert '0.500' in lesson and '0.750' in lesson and '0.250' in lesson
print("Multilabel micro-F1 vs samples-F1 and subset accuracy: exact aggregation and bilingual fallbacks OK")


# Conditional denominators for the SAME 100 hypothetical observations.
# Rows are actual classes; columns are predicted classes.
tp, fn, fp, tn = 40, 20, 10, 30
assert tp + fn + fp + tn == 100
for numerator, denom, expected in (
    (tp, tp + fn, 2/3),    # Recall / TPR
    (tn, tn + fp, 3/4),    # Specificity / TNR
    (tp, tp + fp, 4/5),    # Precision / PPV
    (tn, tn + fn, 3/5),    # Negative predictive value
):
    assert math.isclose(numerator / denom, expected, abs_tol=1e-12)
assert math.isclose(fp / (fp + tn), .25)
assert math.isclose(fn / (fn + tn), .40)

_condition = Path('docs/assets/concept-animations')
_motion = (_condition / 'confusion-condition-direction-motion.svg').read_text(encoding='utf-8')
_still = (_condition / 'confusion-condition-direction-still.svg').read_text(encoding='utf-8')
assert 'viewBox="0 0 640 360"' in _motion and 'viewBox="0 0 640 360"' in _still
assert '<animate ' in _motion and '<animate ' not in _still
assert 'prefers-reduced-motion' in _motion
assert 'opacity:0!important' in _motion and 'opacity:1!important' in _motion
assert 'dur="16s"' in _motion and 'calcMode="discrete"' in _motion
for key in ('0.667', '0.750', '0.800', '0.600'):
    assert key in _motion
assert 'ROW · TRUE +' in _still and 'COLUMN · PRED +' in _still
assert '0.667' in _still and '0.800' in _still
for _lang in ('index.md', 'index.zh-TW.md'):
    _page = (Path('docs/theory/evaluation/metrics/classification') / _lang).read_text(encoding='utf-8')
    assert 'data-source-asset-urls' in _page
    assert 'src="../../../../assets/concept-animations/confusion-condition-direction-still.svg"' in _page
    assert 'data-motion-src="../../../../assets/concept-animations/confusion-condition-direction-motion.svg"' in _page
    assert '30/50=0.600' in _page and '40/60' in _page
print('Confusion-matrix conditioning: four exact rates and shared bilingual fallback OK')
