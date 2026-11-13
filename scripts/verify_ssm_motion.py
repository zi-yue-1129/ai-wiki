#!/usr/bin/env python3
"""Validate S4D/Mamba-2 motion, GitHub-visible stills and bilingual embedding."""
from pathlib import Path
from xml.etree import ElementTree as ET
from math import isclose
from html.parser import HTMLParser
import re

DOCS=Path('docs'); ASSETS=DOCS/'assets/concept-animations'
TOPICS={
 's4d-diagonal-modes':'theory/models/ssm/structured-state-spaces/s4d/index',
 'mamba2-ssd-causal-map':'theory/models/ssm/selective-state-spaces/mamba-2/index',
}
SVG_NS='{http://www.w3.org/2000/svg}'
class FigParser(HTMLParser):
 def __init__(self): super().__init__(); self.imgs=[]
 def handle_starttag(self,tag,attrs):
  if tag=='img':self.imgs.append(dict(attrs))

def run():
 errors=[]
 for stem,page in TOPICS.items():
  for name,animated in (('motion',True),('still',False)):
   file=ASSETS/f'{stem}-{name}.svg'
   if not file.is_file(): errors.append(f'{file}: missing');continue
   if file.stat().st_size>50*1024:errors.append(f'{file}: oversize')
   try: r=ET.parse(file).getroot()
   except ET.ParseError as e: errors.append(f'{file}: {e}');continue
   if r.tag!=SVG_NS+'svg' or r.get('viewBox')!='0 0 860 440':errors.append(f'{file}: invalid viewbox')
   for tag in ('title','desc'):
    if r.find(SVG_NS+tag) is None: errors.append(f'{file}: missing {tag}')
   nodes=list(r.iter()); animations=[n for n in nodes if n.tag in (SVG_NS+'animate',SVG_NS+'animateMotion')]
   if animated and len(animations)<2: errors.append(f'{file}: missing true temporal motion')
   if not animated and animations: errors.append(f'{file}: still has animations')
   for n in nodes:
    if n.tag.rsplit('}',1)[-1] in ('script','foreignObject','image','iframe'):errors.append(f'{file}: forbidden node')
    for k,v in n.attrib.items():
     k=k.rsplit('}',1)[-1]
     if k.startswith('on') or (k=='href' and (':' in v or v.startswith('//'))):errors.append(f'{file}: active resource')
    if n in animations and (n.get('repeatCount')!='indefinite' or n.get('dur')!='12s'):
     errors.append(f'{file}: animation must loop in 12 seconds')
  for suffix in ('.md','.zh-TW.md'):
   path=DOCS/(page+suffix)
   if not path.is_file(): errors.append(f'{path}: missing');continue
   data=path.read_text(encoding='utf-8');fig=FigParser();fig.feed(data)
   found=[attrs for attrs in fig.imgs if f'{stem}-still.svg' in attrs.get('src','')]
   if len(found)!=1:errors.append(f'{path}: missing single GitHub-visible still img');continue
   img=found[0]
   if not img.get('data-motion-src','').endswith(f'{stem}-motion.svg'):errors.append(f'{path}: missing player motion reference')
   if not img.get('data-still-src','').endswith(f'{stem}-still.svg'):errors.append(f'{path}: missing reduced-motion ref')
   for attribute in ('src','data-motion-src','data-still-src'):
    if not (path.parent/img[attribute]).resolve().is_file():errors.append(f'{path}: missing link {attribute}')
   if len(img.get('alt','').strip())<35:errors.append(f'{path}: missing descriptive alt')
   if '2026-11-14' not in data:errors.append(f'{path}: missing reviewed date')
 # Numerically cross-check the recurrence against its 1-semiseparable causal matrix.
 x=[1,.7,-.6,1.1];a=[1,.8,.7,.9];h=[]
 for i,z in enumerate(x): h.append(z if not i else a[i]*h[-1]+z)
 for j in range(4):
  total=0
  for i in range(j+1):
   c=1
   for k in range(i+1,j+1):c*=a[k]
   total+=c*x[i]
  if not isclose(total,h[j],abs_tol=1e-12):errors.append('SSD example numerical mismatch')
 for e in errors:print('ERROR',e)
 print('Checked two motion/still pairs, bilingual paths and SSD numbers; errors:',len(errors))
 return bool(errors)
if __name__=='__main__':raise SystemExit(run())