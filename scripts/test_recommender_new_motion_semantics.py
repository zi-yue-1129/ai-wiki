#!/usr/bin/env python3
"""Independent calculations for the original item-CF and NeuMF teaching SVGs."""
from math import exp, isclose

def check():
    a, b, wa, wb = 5.0, 2.0, 0.8, 0.4
    assert isclose((wa * a) / wa, 5.0)
    assert isclose((wa * a + wb * b) / (wa + wb), 4.0)
    # Read actual shipped endpoints, not only duplicated arithmetic.
    import xml.etree.ElementTree as ET
    from pathlib import Path
    root = Path(__file__).resolve().parents[1] / 'docs/assets/concept-animations'
    ns = '{http://www.w3.org/2000/svg}'
    for kind in ('motion', 'still'):
        r = ET.parse(root / f'itemcf-weighted-neighbors-{kind}.svg')
        text = '|'.join(e.text or '' for e in r.iter(ns+'text'))
        assert '4.8 / 1.2' in text and '= 4.0' in text
        r = ET.parse(root / f'neumf-dual-path-{kind}.svg')
        text = '|'.join(e.text or '' for e in r.iter(ns+'text'))
        for value in ('0.40', '0.18', '0.50', '0.00', '0.7465'):
            assert value in text
    r = ET.parse(root / 'itemcf-weighted-neighbors-motion.svg')
    widths = [e for e in r.iter(ns+'animate') if e.get('attributeName') == 'width']
    assert len(widths) == 1
    assert list(map(float,widths[0].get('values').split(';'))) == [0,0,32,32,0]
    cursor = next(e for e in r.iter(ns+'animate') if e.get('attributeName') == 'cx')
    assert list(map(float,cursor.get('values').split(';'))) == [728,728,665,665,728]
    assert widths[0].get('keyTimes') == cursor.get('keyTimes')
    pg, qg = (0.8, 0.2), (0.5, 0.9)
    gmf = [x * y for x, y in zip(pg, qg)]
    pm, qm = (0.6, 0.1), (0.2, 0.7)
    hidden = [max(pm[0] - pm[1], 0), max(qm[0] - qm[1], 0)]
    assert all(isclose(x, y) for x, y in zip(gmf + hidden, [0.4, 0.18, 0.5, 0]))
    assert isclose(1 / (1 + exp(-sum(gmf + hidden))), 0.7464939833376621)
if __name__ == "__main__":
    check()
    print("OK: item-CF weighting and NeuMF synthetic branch fusion")
