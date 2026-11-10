"""Playwright visual and bilingual accessible-player regression for Rainbow."""
from __future__ import annotations
import os
from pathlib import Path
from xml.etree import ElementTree as ET
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'docs/assets/concept-animations'
OUT = ROOT / 'artifacts/rainbow-motion'
NS = '{http://www.w3.org/2000/svg}'
STEMS = ('rainbow-c51-projection', 'rainbow-dueling-head', 'rainbow-nstep-returns', 'rainbow-noisynet-samples')

def main() -> None:
    for stem in STEMS:
        for kind in ('motion', 'still'):
            path = ASSETS / f'{stem}-{kind}.svg'
            assert path.stat().st_size < 50_000
            root = ET.parse(path).getroot()
            assert root.tag == NS + 'svg' and root.attrib['viewBox'] == '0 0 440 548'
            assert root.find(NS + 'title') is not None and root.find(NS + 'desc') is not None
            animations = root.findall('.//' + NS + 'animate')
            assert (len(animations) >= 3) if kind == 'motion' else not animations
            for el in root.iter():
                assert el.tag.split('}')[-1] not in ('script', 'image', 'foreignObject', 'iframe')
                for key, val in el.attrib.items():
                    assert not key.split('}')[-1].startswith('on')
                    assert not val.startswith(('https:', 'http:', 'data:', 'javascript:'))
        for filename in ('index.md', 'index.zh-TW.md'):
            text = (ROOT / 'docs/theory/paradigms/reinforcement-learning/value-based-methods/rainbow' / filename).read_text()
            assert f'{stem}-still.svg' in text and f'{stem}-motion.svg' in text
            assert 'CC BY-SA 4.0' in text
    z, mass = [-10,-5,0,5,10], [.1,.2,.4,.2,.1]
    projected = [0.] * 5
    for v, p in zip(z, mass):
        v = max(-10, min(10, 2 + .5*v))
        u = (v+10)/5
        lower = int(u)
        upper = min(4, lower+1)
        projected[lower] += p*(upper-u) if lower != upper else p
        if lower != upper: projected[upper] += p*(u-lower)
    assert all(abs(a-b) < 1e-9 for a,b in zip(projected,[0,.08,.48,.40,.04]))
    q = [3 + a - (2+0-1)/3 for a in (2,0,-1)]
    assert all(abs(a-b)<.005 for a,b in zip(q,(4.67,2.67,1.67)))

    gamma=.9
    assert abs((1 + gamma*4)-4.60)<1e-9
    assert abs((1 + gamma*2 + gamma**2*(-1) + gamma**3*5)-5.635)<1e-9
    assert (.7+.2)>(.6-.2) and (.7-.25)<(.6+.2)

    OUT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        args={'headless':True, 'args':['--no-sandbox']}
        if os.environ.get('CHROMIUM_EXECUTABLE'):
            args['executable_path']=os.environ['CHROMIUM_EXECUTABLE']
        browser = p.chromium.launch(**args)
        for stem in STEMS:
            for width in (320,360,720,1024):
                signatures=[]
                for kind, sec in (('motion',.5),('motion',2.6),('motion',4.9),('motion',7.4),('still',0)):
                    path = ASSETS / f'{stem}-{kind}.svg'
                    page=browser.new_page(viewport={'width':width,'height':max(820,width*2)})
                    page.set_content('<style>body{margin:0}svg{width:100%;height:auto;display:block}</style>'+path.read_text())
                    if kind == 'motion':
                        page.locator('svg').evaluate('(e,t)=>{e.pauseAnimations();e.setCurrentTime(t)}', sec)
                    bounds=page.locator('svg text').evaluate_all('els=>els.map(e=>{let r=e.getBBox();return [r.x,r.y,r.width,r.height]})')
                    assert all(x>=-.5 and y>=-.5 and x+w<=440.5 and y+h<=548.5 for x,y,w,h in bounds), (stem,width,kind,sec)
                    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
                    png = page.locator('svg').screenshot(path=str(OUT / f'{stem}-{width}-{kind}-{str(sec).replace(".","_")}.png'))
                    if kind == 'motion': signatures.append(png)
                    page.close()
                assert len(set(signatures)) > 2, (stem,width,'animation must show meaningful change')
        player=(ROOT / 'docs/javascripts/concept-motion.js').read_text()
        host='https://local.invalid/concept-animations/'
        for stem in STEMS:
            motion=(ASSETS / f'{stem}-motion.svg').read_text()
            still=(ASSETS / f'{stem}-still.svg').read_text()
            for alt in ('Rainbow schematic distribution', 'Rainbow 分布與優勢分支示意'):
                for mode in ('no-preference','reduce'):
                    context=browser.new_context(reduced_motion=mode)
                    page=context.new_page()
                    page.route(host+'**',lambda route:route.fulfill(body=motion if '-motion.svg' in route.request.url else still, content_type='image/svg+xml'))
                    page.set_content(f'<img alt="{alt}" src="{host}{stem}-still.svg" data-motion-src="{host}{stem}-motion.svg" data-still-src="{host}{stem}-still.svg">')
                    page.add_script_tag(content=player)
                    button=page.locator('.concept-motion-toggle')
                    button.wait_for(state='visible')
                    expected='-still.svg' if mode=='reduce' else '-motion.svg'
                    assert expected in page.locator('img').get_attribute('src')
                    button.focus(); page.keyboard.press('Enter')
                    assert ('-motion.svg' if mode=='reduce' else '-still.svg') in page.locator('img').get_attribute('src')
                    button.focus(); page.keyboard.press('Space')
                    assert expected in page.locator('img').get_attribute('src')
                    context.close()
        browser.close()
    print('PASS: C51, dueling, n-step and NoisyNet numeric invariants; 80 Chromium screenshots; bilingual keyboard and reduced-motion player')

if __name__ == '__main__':
    main()
