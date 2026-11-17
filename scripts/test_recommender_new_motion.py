#!/usr/bin/env python3
"""Independent calculations for the original item-CF and NeuMF teaching SVGs."""
from math import exp, isclose

def check():
    a, b, wa, wb = 5.0, 2.0, 0.8, 0.4
    assert isclose((wa * a) / wa, 5.0)
    assert isclose((wa * a + wb * b) / (wa + wb), 4.0)
    pg, qg = (0.8, 0.2), (0.5, 0.9)
    gmf = [x * y for x, y in zip(pg, qg)]
    pm, qm = (0.6, 0.1), (0.2, 0.7)
    hidden = [max(pm[0] - pm[1], 0), max(qm[0] - qm[1], 0)]
    assert all(isclose(x, y) for x, y in zip(gmf + hidden, [0.4, 0.18, 0.5, 0]))
    assert isclose(1 / (1 + exp(-sum(gmf + hidden))), 0.7464939833376621)
if __name__ == "__main__":
    check()
    print("OK: item-CF weighting and NeuMF synthetic branch fusion")
