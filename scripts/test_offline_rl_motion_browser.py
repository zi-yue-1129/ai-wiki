#!/usr/bin/env python3
"""Visual, numeric and accessible-player regression for offline IQL/CQL motion."""
import math
import os
import re
from pathlib import Path
from xml.etree import ElementTree as ET
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'docs/assets/concept-animations'
OUT = ROOT / 'artifacts/offline-rl-motion'
STEMS = ('offline-iql-expectile', 'offline-cql-conservative')
NS = '{http://www.w3.org/2000/svg}'

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for stem, topic in zip(STEMS, ('iql', 'cql')):
        for kind in ('motion', 'still'):
            path = ASSETS / f'{stem}-{kind}.svg'
            raw = path.read_text(encoding='utf-8')
            root = ET.fromstring(raw)
            assert root.tag == NS+'svg' and root.attrib['viewBox'] == '0 0 440 548'
            assert root.find(NS+'title') is not None and root.find(NS+'desc') is not None
            assert len(raw.encode('utf-8')) < 14_000
            assert not re.search(r'<script|<image|<foreignObject|<iframe|@import|url\(https?:|\son\w+=', raw, re.I)
            assert not re.search(r'(?:href|src)\s*=\s*[\"\'](?:https?://|data:|javascript:)', raw, re.I)
            animations = root.findall('.//'+NS+'animate')
            assert len(animations) >= 3 if kind == 'motion' else len(animations) == 0
        for name in ('index.md', 'index.zh-TW.md'):
            md = (ROOT/'docs/theory/paradigms/reinforcement-learning/offline-rl'/topic/name).read_text()
            assert f'{stem}-motion.svg' in md and f'{stem}-still.svg' in md
            assert 'CC BY-SA 4.0' in md
    values = [1, 2, 4]
    expectile = 19 / 6
    loss_balance = .8*(4-expectile) - .2*(expectile-1) - .2*(expectile-2)
    assert abs(loss_balance) < 1e-12
    weights = [math.exp(.5*(q-expectile)) for q in values]
    probs = [w/sum(weights) for w in weights]
    assert all(abs(a-b)<.005 for a,b in zip(probs,[.14,.23,.63]))
    a,b=2.,5.
    for _ in range(4):
        ea,eb=math.exp(a-5),math.exp(b-5)
        pb=eb/(ea+eb)
        a-=.5*(-pb+(a-2))
        b-=.5*pb
    assert abs(a-2.7302)<.002 and abs(b-3.3204)<.002

    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path=os.getenv('CHROMIUM_EXECUTABLE') or None,args=['--no-sandbox'])
        shots=0
        for stem in STEMS:
            for width in (320,360,720,1024):
                page=browser.new_page(viewport={'width':width,'height':820})
                for stamp,sec in [('initial',.2),('expectile',3.0),('update',6.1),('result',8.6),('still',None)]:
                    raw=(ASSETS/f'{stem}-{"motion" if sec is not None else "still"}.svg').read_text()
                    page.set_content('<!doctype html><html><head><meta charset="utf-8"><style>body{margin:0}svg{display:block;width:100%;height:auto}</style></head><body>'+raw+'</body></html>')
                    if sec is not None:
                        page.evaluate('(t)=>document.querySelector("svg").setCurrentTime(t)',sec)
                    result=page.evaluate('''() => {const svg=document.querySelector('svg');return {overflow:document.documentElement.scrollWidth>innerWidth,bad:[...svg.querySelectorAll('text')].filter(el=>{const b=el.getBBox();return b.x< -1||b.y< -1||b.x+b.width>441||b.y+b.height>549}).map(el=>el.textContent)}}''')
                    assert not result['overflow'] and not result['bad'],(stem,width,stamp,result)
                    page.locator('svg').screenshot(path=str(OUT/f'{stem}-{width}-{stamp}.png'))
                    shots+=1
                page.close()
        js=(ROOT/'docs/javascripts/concept-motion.js').read_text()
        for stem in STEMS:
            for language in ('en','zh-TW'):
                for reduce in (False,True):
                    page=browser.new_page(viewport={'width':320,'height':700},reduced_motion='reduce' if reduce else 'no-preference')
                    alt='示意動畫' if language=='zh-TW' else 'Instructional animation'
                    page.set_content(f'''<!doctype html><html><body><img alt="{alt}" src="/assets/concept-animations/{stem}-still.svg" data-motion-src="/assets/concept-animations/{stem}-motion.svg" data-still-src="/assets/concept-animations/{stem}-still.svg"></body></html>''')
                    page.add_script_tag(content=js)
                    button=page.locator('.concept-motion-toggle')
                    assert button.count()==1
                    initial=page.locator('img').get_attribute('src')
                    assert initial.endswith('-still.svg') if reduce else initial.endswith('-motion.svg')
                    button.focus();button.press('Enter')
                    nextsrc=page.locator('img').get_attribute('src')
                    assert nextsrc!=initial
                    button.press('Space')
                    assert page.locator('img').get_attribute('src')==initial
                    page.close()
        browser.close()
    print(f'PASS: {shots} SVG Chromium screenshots, bilingual keyboard, reduced-motion, numeric checks')

if __name__ == '__main__':
    main()
