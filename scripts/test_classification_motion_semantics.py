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

print("Classification motion semantics: 6 analytic cases OK")
