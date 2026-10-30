#!/usr/bin/env python3
"""Render exact SVG counterfactual previews in Chromium (CC BY-SA 4.0)."""
from pathlib import Path
import re
import os
from xml.etree import ElementTree as ET
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'docs/assets/concept-animations'
PAGES = {
    'moco': ROOT / 'docs/theory/paradigms/self-supervised/contrastive-learning',
    'byol': ROOT / 'docs/theory/paradigms/self-supervised/non-contrastive-methods',
}
NS = '{http://www.w3.org/2000/svg}'

for kind, folder in PAGES.items():
    for suffix in ('motion', 'still'):
        path = ASSETS / f'{kind}-causal-{suffix}.svg'
        raw = path.read_text(encoding='utf-8')
        root = ET.fromstring(raw)
        assert root.tag == NS + 'svg' and root.attrib['viewBox'] == '0 0 640 244'
        assert root.find(NS+'title') is not None and root.find(NS+'desc') is not None
        assert len(raw.encode('utf-8')) < 12000
        assert not re.search(r'<script|<foreignObject|@import|url\(https?:|\son\w+=',raw,re.I)
        if suffix == 'motion':
            assert '@keyframes' in raw and 'prefers-reduced-motion' in raw
            assert 'animation-play-state:paused' in raw
        else:
            assert '@keyframes' not in raw and 'animation:' not in raw
    for lang in ('.md','.zh-TW.md'):
        page=(folder / f'{kind}{lang}').read_text(encoding='utf-8')
        assert f'{kind}-causal-still.svg' in page and f'{kind}-causal-motion.svg' in page

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=os.environ.get('CHROMIUM_EXECUTABLE') or None,args=['--no-sandbox'])
    for kind in PAGES:
        svg = (ASSETS / f'{kind}-causal-motion.svg').read_text(encoding='utf-8')
        for width in (360,900):
            for reduced in (False, True):
                page = browser.new_page(viewport={'width':width,'height':440},reduced_motion='reduce' if reduced else 'no-preference')
                page.set_content('<!doctype html><html><head><meta charset="utf-8"><style>body{margin:0}svg{display:block;width:100%;height:auto}</style></head><body>'+svg+'</body></html>')
                page.wait_for_timeout(120)
                result=page.evaluate("""() => {
                  const svg=document.querySelector('svg');
                  const boxes=[...svg.querySelectorAll('text')].map(e=>({label:e.textContent,...(()=>{const r=e.getBBox();return {x:r.x,y:r.y,w:r.width,h:r.height}})()}));
                  const moving=svg.querySelector('.arrive,.pulse-left');
                  return {overflow:document.documentElement.scrollWidth>innerWidth,boxes,
                    name:getComputedStyle(moving).animationName};
                }""")
                assert not result['overflow'],(kind,width,reduced,'overflow')
                for b in result['boxes']:
                    assert b['x']>=-1 and b['x']+b['w']<=641 and b['y']>=-1 and b['y']+b['h']<=245,(kind,width,b)
                assert (result['name']=='none') == reduced,(kind,width,reduced,result['name'])
                if not reduced:
                    moving=page.locator('.arrive,.pulse-left').first
                    before=moving.evaluate('(el)=>getComputedStyle(el).transform')
                    page.wait_for_timeout(1600)
                    after=moving.evaluate('(el)=>getComputedStyle(el).transform')
                    assert before != after,(kind,width,'animation did not advance')
                if width==360:
                    shot=ROOT/'artifacts/ssl-causal-previews'/f'{kind}-{width}-reduced-{reduced}.png'
                    shot.parent.mkdir(parents=True,exist_ok=True)
                    page.screenshot(path=str(shot))
                if not reduced:
                    page.locator('svg').focus()
                    assert page.locator('.arrive,.pulse-left').first.evaluate('(el)=>getComputedStyle(el).animationPlayState')=='paused'
                page.close()
    browser.close()
print('Validated 4 SVGs, 4 bilingual page links and 8 Chromium responsive/reduced-motion cases')
