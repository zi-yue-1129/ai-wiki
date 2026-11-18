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

print("Classification motion semantics: 4 analytic cases OK")
