#!/usr/bin/env python3
"""Numerical and timing checks for synthetic autoregressive teaching figures."""
from pathlib import Path
import math
import re
import xml.etree.ElementTree as E
ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'docs/assets/concept-animations'
N={'s':'http://www.w3.org/2000/svg'}
def root(stem,kind):return E.parse(A/f'{stem}-{kind}.svg').getroot()
def texts(r):return {''.join(e.itertext()) for e in r.findall('.//s:text',N)}
qs=[.1,.25,.5,.8];survival=[];stops=[];s=1
for q in qs:stops.append(s*q);s*=1-q;survival.append(s)
assert math.isclose(sum(stops)+s,1)
assert math.isclose(s,.0675)
for kind in ['motion','still']:
 r=root('ar-eos-survival',kind)
 bars=[b for b in r.findall('.//s:rect',N) if b.get('width')=='85']
 assert len(bars)==4
 for b,p in zip(bars,stops):
  assert abs(float(b.get('height'))-290*p)<.51
  assert float(b.get('y'))+float(b.get('height'))==351
 blue=[b for b in r.findall('.//s:rect',N) if b.get('fill')=='#257db4']
 expected=survival if kind=='motion' else [survival[-1]]
 assert len(blue)==len(expected)
 for b,p in zip(blue,expected):assert abs(float(b.get('width'))-523*p)<.011
 assert {'0.1','0.225','0.3375','0.27'}<=texts(r)
 # Conditional EOS probabilities must use a common 430px scale.
 r=root('ar-context-drift',kind)
 for color,p in [('#257db4',.85),('#cf8133',.4)]:
  b=next(b for b in r.findall('.//s:rect',N) if b.get('fill')==color and b.get('height')=='26')
  assert math.isclose(float(b.get('width')),430*p)
 r=root('ar-likelihood-accumulation',kind);ts=texts(r)
 assert {'p = 0.50','p = 0.20','p = 0.40','0.50','0.10','0.04'}<=ts
 for p in [.5,.2,.4]:assert f'−log = {-math.log(p):.2f}' in ts
 assert math.isclose(math.prod([.5,.2,.4]),.04)
 assert any('3.22' in t for t in ts)
r=root('ar-eos-survival','motion')
bs=[g for g in r.findall('.//s:g',N) if any((t.text or '') in ['0.1','0.225','0.3375','0.27'] for t in g.findall('s:text',N))]
assert len(bs)==4
for i,g in enumerate(bs):
 a=g.find('s:animate',N)
 assert a.get('keyTimes')==('0;1' if i==0 else f'0;{i/4:g};1')
 assert a.get('values')==('1;1' if i==0 else '0;1;1')
for p in (ROOT/'docs/theory/paradigms/unsupervised/density-and-generative-models/autoregressive').glob('index*.md'):
 assert not re.search(r'^\$\s*$',p.read_text(),re.M)
 assert 'width:800px' not in p.read_text()
print('AR likelihood/NLL, conditional scales, survival conservation and synchronized stopping steps passed')
