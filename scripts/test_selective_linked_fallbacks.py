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
                     ['0%', '25%', '33%', '2/6', '4/6', '6/6', 'RISK'])
    circles = [(float(n.get('cx')), float(n.get('cy')))
               for n in risk.findall('.//svg:circle', NS)]
    assert len(circles) == 3
    assert [round(x) for x, _ in circles] == [240, 400, 560]
    assert circles[0][1] > circles[1][1] > circles[2][1]
    assert [round((circles[0][1] - y) / 200 * 100) for _, y in circles] == [0, 25, 33]

    coverage = check_svg('accuracy-selective-class-coverage-linked-still',
                         ['CLASS COVERAGE', 'ALL', 'SELECTIVE', 'POS', 'NEG', '4/4', '1/4'])
    colored = coverage.findall('.//svg:rect', NS)
    lengths = [(e.get('x'), e.get('width'), e.get('fill')) for e in colored
               if e.get('fill') in ('#087e85', '#3c719d')]
    assert lengths == [('76', '188', '#087e85'), ('76', '188', '#3c719d'),
                       ('392', '47', '#087e85'), ('392', '188', '#3c719d')]
    assert 47 / 188 == 1 / 4

    for filename in ('accuracy.md', 'accuracy.zh-TW.md'):
        page = (CHAPTER / filename).read_text(encoding='utf-8')
        for stem in ('accuracy-selective-coverage-linked-still',
                     'accuracy-selective-class-coverage-linked-still'):
            assert f'../../../../assets/concept-animations/{stem}.svg' in page, (filename, stem)
    print('PASS: 2 synthetic linked-plot fallbacks, numerical geometry, bilingual links')


if __name__ == '__main__':
    run()
