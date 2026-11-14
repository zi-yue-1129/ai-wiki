#!/usr/bin/env python3
"""Verify the new LayerNorm / original Seq2Seq instructional assets (stdlib only)."""
from __future__ import annotations
from pathlib import Path
from xml.etree import ElementTree as ET
import math
import re

BASE=Path('docs/assets/concept-animations')
NS='{http://www.w3.org/2000/svg}'
PAGES={
 'layernorm-feature-shift':Path('docs/theory/models/mlp/layer-normalisation/index'),
 'seq2seq-context-handoff':Path('docs/theory/models/rnn/sequence-modes/sequence-to-sequence/index'),
}
for stem,page in PAGES.items():
 for kind in ('motion','still'):
  p=BASE/f'{stem}-{kind}.svg'
  assert p.stat().st_size < 50*1024, p
  root=ET.parse(p).getroot()
  assert root.tag == NS+'svg' and root.get('viewBox')=='0 0 860 440', p
  assert root.find(NS+'title') is not None and root.find(NS+'desc') is not None
  anim=[el for el in root.iter() if el.tag in {NS+'animate', NS+'animateMotion', NS+'animateTransform'}]
  assert bool(anim)==(kind=='motion'), p
  assert all(x.attrib.get('repeatCount')=='indefinite' and x.get('dur')=='12s' for x in anim)
  for el in root.iter():
   assert el.tag.split('}')[-1] not in {'script','foreignObject','iframe','image'},p
   for attr,value in el.attrib.items():
    assert not attr.split('}')[-1].startswith('on'),p
    assert not (attr.split('}')[-1]=='href' and ('://' in value or value.startswith('javascript:'))),p
 for suffix in ('.md','.zh-TW.md'):
  f=page.with_name(page.name+suffix)
  txt=f.read_text(encoding='utf-8')
  links=re.findall(r'!\[[^]]+\]\(([^)]+\.svg)\)',txt)
  assert (BASE/f'{stem}-still.svg').resolve() in {(f.parent/link).resolve() for link in links},f
  assert any(token in txt.lower() for token in ('illustrative', 'schematic', '示意')), f
# Illustrative LayerNorm semantics: shifting a sample does not change normalised scores.
x=[1,3,5,7,9]
def standardise(v):
 m=sum(v)/len(v)
 var=sum((a-m)**2 for a in v)/len(v)
 return [(a-m)/math.sqrt(var) for a in v]
assert all(abs(a-b)<1e-12 for a,b in zip(standardise(x),standardise([a+2 for a in x])))
print('OK: 4 SVGs, both bilingual static previews and LayerNorm shift invariance')