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

# Keep the four worked examples anchored to one explicitly identified, bilingual
# synthetic confusion matrix. Earlier prose referred to "100 cases above" even
# though no such 100-case example appeared on its own page.
worked_root = Path("docs/theory/evaluation/metrics/classification")
_tp, _fn, _fp, _tn = 40, 20, 10, 30
assert _tp + _fn + _fp + _tn == 100
assert _tp + _fn == 60 and _fp + _tn == 40
assert _tp + _fp == 50 and _fn + _tn == 50
assert math.isclose((_tp + _tn) / 100, .70)
assert math.isclose(_tp / (_tp + _fp), .80)
assert math.isclose(_tp / (_tp + _fn), 2 / 3)
assert math.isclose(2 * _tp / (2 * _tp + _fp + _fn), 8 / 11)
for suffix in (".md", ".zh-TW.md"):
    overview = (worked_root / ("index" + suffix)).read_text(encoding="utf-8")
    assert "40 (TP)" in overview and "20 (FN)" in overview
    assert "10 (FP)" in overview and "30 (TN)" in overview
    for metric in ("accuracy", "precision", "recall", "f1"):
        body = (worked_root / (metric + suffix)).read_text(encoding="utf-8")
        assert "](index.md)" in body and "100" in body
        assert "100 cases above" not in body
        assert "沿用上述 100 筆案例" not in body
print("Bilingual shared 100-case confusion matrix: four metric pages agree")

# Confusion-matrix metrics are label-based; the cost-sensitive decision rule is
# a separate modeling choice. Protect the bilingual explanations against
# regressions that incorrectly call accuracy threshold-free or metrics costs.
_accuracy_en = (worked_root / "accuracy.md").read_text(encoding="utf-8")
_accuracy_zh = (worked_root / "accuracy.zh-TW.md").read_text(encoding="utf-8")
assert "decision threshold" in _accuracy_en and "label-selection rule" in _accuracy_en
assert "決策門檻" in _accuracy_zh and "類別選取規則" in _accuracy_zh
for metric, en_error, zh_error in (
    ("precision", "Precision measures the cost of false alarms.", "精確率衡量誤報的代價。"),
    ("recall", "Recall measures the cost of misses.", "召回率衡量漏報的代價。"),
):
    assert en_error not in (worked_root / (metric + ".md")).read_text(encoding="utf-8")
    assert zh_error not in (worked_root / (metric + ".zh-TW.md")).read_text(encoding="utf-8")
print("Bilingual threshold and error-cost semantics OK")

# Keep ranking-probability and metric semantics consistent in both translations.
for suffix in (".md", ".zh-TW.md"):
    _roc = (worked_root / ("roc-auc" + suffix)).read_text(encoding="utf-8")
    _pr = (worked_root / ("pr-auc" + suffix)).read_text(encoding="utf-8")
    _f1 = (worked_root / ("f1" + suffix)).read_text(encoding="utf-8")
    if suffix == ".md":
        assert "half the probability of a tie" in _roc
        assert "expected" in _roc and "Equal class sizes are not required" in _roc
        assert "raw AP comparisons across datasets" in _pr
        assert "disagreement between precision and recall" in _f1
    else:
        assert "平手機率的一半" in _roc and "期望值" in _roc
        assert "不要求正負例數量相當" in _roc
        assert "不同盛行率資料集的原始 AP" in _pr
        assert "精確率與召回率之間的差距" in _f1
print("Bilingual ranking-baseline semantics and F1 interpretation OK")

# Exact population PPV and a cost-sensitive ROC threshold counterexample.
_prevalences = (.05, .10, .20, .40, .60)
_ppv_values = tuple(.8 * p / (.8 * p + .1 * (1 - p)) for p in _prevalences)
assert all(math.isclose(v, expected, abs_tol=0.0005) for v, expected in
           zip(_ppv_values, (.296296, .470588, .666667, .842105, .923077)))
assert all(left < right for left, right in zip(_ppv_values, _ppv_values[1:]))
_synthetic_labels = (1, 1, 0, 0, 0, 1)
_youden, _loss = [], []
for k in range(7):
    tp = sum(_synthetic_labels[:k])
    fp = k - tp
    tpr, fpr = tp / 3, fp / 3
    _youden.append(tpr - fpr)
    _loss.append(5 * .4 * (1 - tpr) + .6 * fpr)
assert _youden.index(max(_youden)) == 2
assert _loss.index(min(_loss)) == 6
assert math.isclose(_youden[2], 2 / 3)
assert math.isclose(_loss[2], 2 / 3) and math.isclose(_loss[6], .6)
for stem in ("roc-pr-prevalence", "roc-youden-cost"):
    svg_dir = Path("docs/assets/concept-animations")
    motion = (svg_dir / (stem + "-motion.svg")).read_text(encoding="utf-8")
    still = (svg_dir / (stem + "-still.svg")).read_text(encoding="utf-8")
    assert "prefers-reduced-motion" in motion and 'class="moving"' in motion
    assert "<animate " in motion and "<animate " not in still
    for suffix in (".md", ".zh-TW.md"):
        page = (worked_root / ("roc-auc" + suffix)).read_text(encoding="utf-8")
        assert stem + "-motion.svg" in page and stem + "-still.svg" in page
print("Bilingual prevalence-shift and Youden tradeoff motion semantics OK")


# Regression: the very same ranked ROC example selects different operating
# points when only the relative cost of missing a positive changes.
for _fn_cost, _expected_k in ((1, 2), (5, 6)):
    _hypothetical = []
    for _k in range(7):
        _tp = sum(_synthetic_labels[:_k])
        _fp = _k - _tp
        _tpr, _fpr = _tp / 3, _fp / 3
        _hypothetical.append(_fn_cost * .4 * (1 - _tpr) + .6 * _fpr)
    assert _hypothetical.index(min(_hypothetical)) == _expected_k
    if _fn_cost == 1:
        assert math.isclose(_hypothetical[2], 2 / 15)
        assert math.isclose(_hypothetical[6], .6)
for _suffix, _guide, _counterfactual in (
    (".md", "Guided animations", "cost-ratio counterfactual"),
    (".zh-TW.md", "教學動畫導覽", "成本比率的反事實比較"),
):
    _overview = (worked_root / ("index" + _suffix)).read_text(encoding="utf-8")
    _roc_text = (worked_root / ("roc-auc" + _suffix)).read_text(encoding="utf-8")
    assert _guide in _overview
    assert "roc-pr-prevalence-still.svg" in _overview
    assert "roc-youden-cost-still.svg" in _overview
    assert _counterfactual in _roc_text
print("Bilingual navigation and cost-ratio counterfactual OK")
