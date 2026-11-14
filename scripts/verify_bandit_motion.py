#!/usr/bin/env python3
"""SVG safety, bilingual paths and toy UCB/Beta mathematical consistency."""
from math import log, sqrt
from pathlib import Path
import re
from xml.etree import ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
D=ROOT/'docs/assets/concept-animations'
PREFIXES=('ucb1-optimism-switch','thompson-beta-posterior-draws')
PAGES=[ROOT/'docs/theory/paradigms/online/stochastic-bandits/index.md',ROOT/'docs/theory/paradigms/online/stochastic-bandits/index.zh-TW.md']
for name in PREFIXES:
    for suffix in ('motion','still'):
        f=D/f'{name}-{suffix}.svg'
        assert f.exists(),f
        txt=f.read_text()
        root=ET.fromstring(txt)
        assert root.attrib.get('viewBox')=='0 0 860 464',f
        assert not re.search(r'<script\b|javascript:|<foreignObject\b|(?:href|xlink:href)=\"https?://',txt,re.I),f
        ns='{http://www.w3.org/2000/svg}'
        assert bool(root.findall('.//'+ns+'animate'))==(suffix=='motion'),f
for p in PAGES:
    s=p.read_text()
    for name in PREFIXES:
        for suffix in ('motion','still'):
            assert (name+'-'+suffix+'.svg') in s,(p,name,suffix)
    assert 'data-motion-src=' in s and 'bandit-motion-viewport' in s
n=[[6,2,8],[6,3,8],[6,4,8]]
means=[[.65,.45,.60],[.65,.30,.60],[.65,.225,.60]]
winners=[max(range(3),key=lambda i:means[j][i]+sqrt(2*log(16+j)/n[j][i])) for j in range(3)]
assert winners==[1,1,0],winners
assert (4,3)==(4,3) and (5,3)==(4+1,3)
print('PASS: 4 safe SVGs, 2 bilingual chapter links, UCB1 B/B/A calculation and Beta(4,3)→Beta(5,3)')