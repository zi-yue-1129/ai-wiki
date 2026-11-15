#!/usr/bin/env python3
"""Rendered Chromium QA for new sliding-window and recurrent linear-attention teaching assets."""
from pathlib import Path
from xml.etree import ElementTree as ET
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'docs/assets/concept-animations'
PLAYER = ROOT / 'docs/javascripts/concept-motion.js'
PAIRS = ('sliding-window-mask', 'linear-attention-recurrence', 'sliding-window-depth-reach', 'linear-attention-work-growth', 'gqa-cache-growth', 'global-local-pair-count')
SVGNS = '{http://www.w3.org/2000/svg}'

def main():
    assert PLAYER.exists()
    for stem in PAIRS:
        for typ in ('motion','still'):
            path=ASSETS/f'{stem}-{typ}.svg'
            assert path.exists(), path
            tree=ET.parse(path); root=tree.getroot()
            assert root.tag==SVGNS+'svg'
            assert not any(k in path.read_text() for k in ('<script','<foreignObject','<image',' xlink:href=', ' href="http'))
            assert root.find(SVGNS+'title') is not None
            if typ=='motion':assert root.findall('.//'+SVGNS+'animate'),stem
            else:assert not root.findall('.//'+SVGNS+'animate') and not root.findall('.//'+SVGNS+'animateMotion')
    # Explicit numerical semantics of the scalar illustration, independent of XML structure.
    ks=[1,2,1,2];vs=[1,0,3,2]
    s=z=0;rows=[]
    for k,v in zip(ks,vs):
        s+=k*v;z+=k;rows.append((s,z,round(s/z,2)))
    assert rows==[(1,1,1),(1,3,0.33),(4,4,1),(8,6,1.33)]
    # Derive sparse edge counts via sets, not only their analytic formulas.
    for n in range(4,13):
        local={(i,j) for i in range(1,n+1) for j in range(1,n+1) if abs(i-j)<=1}
        global_edges={(i,3) for i in range(1,n+1)} | {(3,j) for j in range(1,n+1)}
        assert len(local)==3*n-2
        assert len(local|global_edges)==5*n-8
        assert len(local|global_edges)<=n*n
    checked=0
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True,args=['--no-sandbox'])
        for stem in PAIRS:
            motion=(ASSETS/f'{stem}-motion.svg').read_text()
            # Actually render at meaningful intermediate times, not only XML validation.
            page=browser.new_page(viewport={'width':1024,'height':650},reduced_motion='no-preference')
            page.set_content(motion)
            svg=page.locator('svg'); assert svg.is_visible()
            pngs=[]
            for t in (0.2,2.6,5.0,7.3):
                page.evaluate('(t)=>document.querySelector("svg").setCurrentTime(t)',t)
                pngs.append(svg.screenshot())
            assert len(set(pngs))>=3, f'{stem}: no actual changing frames'
            if stem=='linear-attention-recurrence':
                for i,t in enumerate((0.4,2.7,4.9,7.2)):
                    page.evaluate('(t)=>document.querySelector("svg").setCurrentTime(t)',t)
                    vis=page.locator('.state-step').evaluate_all('(els)=>els.map(x=>+getComputedStyle(x).opacity)')
                    assert vis.index(max(vis))==i,(t,vis)
            page.close();checked+=4
            for lang in ('en','zh'):
                for width in (320,360,800,1024):
                    page=browser.new_page(viewport={'width':width,'height':650},reduced_motion='reduce')
                    still=ASSETS/f'{stem}-still.svg'; animated=ASSETS/f'{stem}-motion.svg'
                    # Test the actual player script, with resources served through an isolated route.
                    def route_handler(route):
                        route.fulfill(content_type='image/svg+xml',body=(animated if '-motion.svg' in route.request.url else still).read_text())
                    page.route('**/assets/concept-animations/*.svg',route_handler)
                    page.set_content(f'''<style>.concept-motion-player{{display:inline-block;max-width:100%;overflow-x:auto}}.concept-motion-player img{{width:800px;max-width:none;display:block}}</style><p><img src="https://wiki.example/assets/concept-animations/{stem}-still.svg" alt="{'分組查詢注意力示意' if lang=='zh' else 'Attention visualisation'}"></p>''')
                    page.add_script_tag(content=PLAYER.read_text())
                    button=page.locator('.concept-motion-toggle')
                    assert button.count()==1,(stem,lang,width)
                    assert '-still.svg' in page.locator('img').get_attribute('src')
                    assert page.locator('.concept-motion-player').evaluate('(el)=>el.scrollWidth>el.clientWidth') == (width<=800)
                    button.focus();page.keyboard.press('Enter')
                    assert '-motion.svg' in page.locator('img').get_attribute('src')
                    page.keyboard.press('Space')
                    assert '-still.svg' in page.locator('img').get_attribute('src')
                    assert ('播放' in button.inner_text()) if lang=='zh' else ('Play' in button.inner_text())
                    page.close();checked+=1
        # Test the production CSS geometry, including the non-JS still fallback.
        css = (ROOT / 'docs/stylesheets/concept-motion.css').read_text()
        for stem in PAIRS:
            for width in (320, 1024):
                page = browser.new_page(viewport={'width': width, 'height': 550}, reduced_motion='reduce')
                still = ASSETS / f'{stem}-still.svg'
                motion = ASSETS / f'{stem}-motion.svg'
                def local_assets(route):
                    payload = motion if '-motion.svg' in route.request.url else still
                    route.fulfill(content_type='image/svg+xml', body=payload.read_text())
                page.route('**/assets/concept-animations/*.svg', local_assets)
                page.set_content(
                    '<meta name="viewport" content="width=device-width,initial-scale=1">'
                    + '<style>body{margin:0}.md-typeset p{margin:0}' + css + '</style>'
                    + '<article class="md-typeset"><p><img src="https://wiki.example/assets/concept-animations/'
                    + stem + '-still.svg" alt="Teaching motion"></p></article>')
                assert page.locator('p').evaluate('(e)=>e.scrollWidth>e.clientWidth') == (width < 860)
                assert page.locator('body').evaluate('(e)=>e.scrollWidth<=innerWidth')
                page.add_script_tag(content=PLAYER.read_text())
                host=page.locator('.concept-motion-player.concept-motion-wide')
                assert host.count() == 1, (stem,width)
                assert host.evaluate('(e)=>e.scrollWidth>e.clientWidth') == (width < 860)
                assert page.locator('img').evaluate('(e)=>parseFloat(getComputedStyle(e).width)') == 860
                if width == 320:
                    host.focus()
                    page.keyboard.press('ArrowRight')
                    # Keyboard scrolling is asynchronous in Chromium (often smooth).
                    page.wait_for_function(
                        "() => document.querySelector('.concept-motion-player.concept-motion-wide')?.scrollLeft > 0",
                        timeout=4000,
                    )
                page.close()
                checked += 1
        browser.close()
    print(f'PASS: {checked} Chromium render/control scenarios, bilingual fallback, reduced motion and exact causal recurrence')

if __name__=='__main__': main()