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
