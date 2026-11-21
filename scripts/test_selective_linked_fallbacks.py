#!/usr/bin/env python3
"""Verify GitHub-safe fallback plots of interactive selective-classification metrics.

The fixtures contain synthetic example counts, not empirical model estimates.
"""
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'docs/assets/concept-animations'
CHAPTER = ROOT / 'docs/theory/evaluation/metrics/classification'
NS = {'svg': 'http://www.w3.org/2000/svg'}


def check_svg(stem, expected_labels):
    path = ASSETS / (stem + '.svg')
    assert path.stat().st_size < 10_000, path
    tree = ET.parse(path)
    root = tree.getroot()
    assert root.tag == '{http://www.w3.org/2000/svg}svg'
    assert root.attrib.get('role') == 'img'
    assert root.find('svg:title', NS) is not None
    assert root.find('svg:desc', NS) is not None
    assert not tree.findall('.//svg:script', NS)
    assert not tree.findall('.//svg:foreignObject', NS)
    assert not tree.findall('.//svg:animate', NS)
    texts = [node.text or '' for node in tree.findall('.//svg:text', NS)]
    for value in expected_labels:
        assert value in texts, (stem, value)
    for elem in root.iter():
        assert not any(key.lower().endswith('href') for key in elem.attrib)
    return root


def run():
    risk = check_svg('accuracy-selective-coverage-linked-still',
                     ['0%', '25%', '33%', '2/6', '4/6', '6/6', 'RISK', 'Δ 25 pp',
                      'AT k=3 · HYPOTHETICAL NEXT',
                      '+CORRECT', '1/4 25%', '+WRONG', '2/4 50%'])
    assert risk.attrib.get('viewBox') == '0 0 640 356'
    bars = {b.get('data-next-bar'): float(b.get('width'))
            for b in risk.findall('.//svg:rect', NS) if b.get('data-next-bar')}
    assert bars == {'correct': 90, 'wrong': 180}
    assert bars['wrong'] / bars['correct'] == 2
    bracket = [p for p in risk.findall('.//svg:path', NS)
               if p.get('data-next-spread') == 'true']
    assert len(bracket) == 1
    assert bracket[0].get('d') == 'M238 304V315 M238 310H328 M328 304V315'
    assert 328 - 238 == 360 / 4
    assert 'Neither is model-measured performance or a confidence interval' in risk.find('svg:desc', NS).text
    marker = [n for n in risk.findall('.//svg:circle', NS)
              if n.get('data-next-observed') == 'true']
    assert len(marker) == 1
    assert (marker[0].get('cx'), marker[0].get('cy'), marker[0].get('r')) == (
        '238', '253.5', '5')
    assert any(n.text == 'IN SAMPLE: +CORRECT'
               for n in risk.findall('.//svg:text', NS))
    circles = [(float(n.get('cx')), float(n.get('cy')))
               for n in risk.findall('.//svg:circle', NS) if n.get('data-risk-k')]
    assert len(circles) == 6
    assert [round(x) for x, _ in circles] == [160, 240, 320, 400, 480, 560]
    assert [round((144 - y) / 200 * 100) for _, y in circles] == [0, 0, 33, 25, 40, 33]
    risk_dots = [c for c in risk.findall('.//svg:circle', NS)
                 if c.get('data-risk-k')]
    assert [c.get('data-risk-k') for c in risk_dots] == [
        '1', '2', '3', '4', '5', '6']
    assert circles[2][1] < circles[3][1]  # 1/3 -> 1/4: risk drops
    assert circles[4][1] < circles[5][1]  # 2/5 -> 2/6: risk drops
    assert [c.get('fill') for c in risk_dots] == [
        '#f8fafc', '#087e85', '#f8fafc', '#087e85', '#f8fafc', '#087e85']

    coverage = check_svg('accuracy-selective-class-coverage-linked-still',
                         ['CLASS COVERAGE', 'ALL', 'SELECTIVE', 'POS', 'NEG', '4/4', '1/4',
                          '8/8 accepted · 6/8 correct',
                          '5/8 accepted · 5/5 correct',
                          '0/8 rejected · accuracy N/A',
                          '3/8 rejected · 1/3 correct · 2/3 wrong'])
    assert coverage.attrib.get('viewBox') == '0 0 380 464'
    assert 'not model measurements' in coverage.find('svg:desc', NS).text
    assert 'Rejection changes which outcomes are counted' in coverage.find('svg:desc', NS).text
    colored = coverage.findall('.//svg:rect', NS)
    lengths = [(e.get('x'), e.get('width'), e.get('fill')) for e in colored
               if e.get('fill') in ('#087e85', '#3c719d')]
    assert lengths == [('83', '215', '#087e85'), ('83', '215', '#3c719d'),
                       ('83', '53.75', '#087e85'), ('83', '215', '#3c719d')]
    assert 53.75 / 215 == 1 / 4

    for filename in ('accuracy.md', 'accuracy.zh-TW.md'):
        page = (CHAPTER / filename).read_text(encoding='utf-8')
        for stem in ('accuracy-selective-coverage-linked-still',
                     'accuracy-selective-class-coverage-linked-still'):
            assert f'../../../../assets/concept-animations/{stem}.svg' in page, (filename, stem)
    print('PASS: 2 synthetic linked-plot fallbacks, numerical geometry, bilingual links')


if __name__ == '__main__':
    run()
