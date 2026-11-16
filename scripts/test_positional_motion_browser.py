#!/usr/bin/env python3
"""Rendered and interactive QA for two original positional-encoding motion pairs."""
from __future__ import annotations
import math
from pathlib import Path
from xml.etree import ElementTree as ET
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
ASSET = ROOT / "docs/assets/concept-animations"
PLAYER = ROOT / "docs/javascripts/concept-motion.js"
CSS = ROOT / "docs/stylesheets/concept-motion.css"
STEMS = ("alibi-distance-softmax", "rope-interpolation-angle", "alibi-content-recency", "rope-frequency-bands")
ARTIFACT = ROOT / 'artifacts/positional-motion'
SVG = "{http://www.w3.org/2000/svg}"


def validate_math():
    for m in (0, 0.25, 0.5, 1):
        probabilities = [math.exp(-m*d) for d in range(8)]
        z = sum(probabilities)
        probabilities = [p/z for p in probabilities]
        assert abs(sum(probabilities)-1) < 1e-12
        if m == 0:
            assert all(abs(p-0.125) < 1e-12 for p in probabilities)
        if m > 0:
            assert all(probabilities[i] > probabilities[i+1] for i in range(7))
    assert abs(1/sum(math.exp(-d) for d in range(8))-0.6323326828120425) < 1e-12
    scores = lambda m: [2-4*m, -3*m, -2*m, -m, 0]
    for m in (0.0,0.5,1.0):
        exps=[math.exp(z) for z in scores(m)]
        weights=[p/sum(exps) for p in exps]
        assert abs(sum(weights)-1)<1e-12
        if m==0: assert weights[0]>weights[4]
        if m==0.5: assert abs(weights[0]-weights[4])<1e-12
        if m==1: assert weights[0]<weights[4]
    assert abs(math.cos(math.pi*4/2)-1.0)<1e-12
    assert abs(math.cos(math.pi*4/10)-math.cos(2*math.pi/5))<1e-12
    assert abs(0.6*16-9.6) < 1e-12
    assert abs(0.6*(16/2)-4.8) < 1e-12


def main():
    validate_math()
    ARTIFACT.mkdir(parents=True, exist_ok=True)
    for stem in STEMS:
        for role in ('motion', 'still'):
            f = ASSET / f'{stem}-{role}.svg'
            assert f.is_file(), f
            root = ET.parse(f).getroot()
            assert root.tag == SVG + 'svg' and root.attrib.get('viewBox') == '0 0 640 360'
            assert root.find(SVG+'title') is not None and root.find(SVG+'desc') is not None
            assert not any(e.tag.rsplit('}',1)[-1] in {'script','foreignObject','iframe','image'} for e in root.iter())
            motions=[n for n in root.iter() if n.tag.rsplit('}',1)[-1] in ('animate','animateTransform')]
            assert bool(motions) == (role == 'motion'), (stem,role)
            assert all(m.get('repeatCount') == 'indefinite' for m in motions)
    assert PLAYER.is_file() and CSS.is_file()
    count = 0
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True, args=['--no-sandbox'])
        for stem in STEMS:
            motion=(ASSET / f'{stem}-motion.svg').read_text(encoding='utf-8')
            p=browser.new_page(viewport={'width':1024,'height':520})
            p.set_content(motion)
            svg=p.locator('svg')
            screenshots=[]
            for t in (0.2, 3.5, 7.3, 10.5):
                p.evaluate('(t)=>{const s=document.querySelector("svg");s.pauseAnimations();s.setCurrentTime(t);}', t)
                screenshots.append(svg.screenshot(path=str(ARTIFACT/f'{stem}-frame-{str(t).replace(chr(46),chr(95))}.png')))
            assert len(set(screenshots)) >= 3, f'{stem}: no visible animation'
            p.close();count+=4
            for lang in ('en', 'zh'):
                alt = '位置編碼示意圖' if lang == 'zh' else 'Illustrated positional encoding'
                for width in (320, 360, 640, 1024):
                    for reduced in ('no-preference', 'reduce'):
                        p=browser.new_page(viewport={'width':width,'height':540}, reduced_motion=reduced)
                        def provide(route):
                            role = 'motion' if '-motion.svg' in route.request.url else 'still'
                            payload=(ASSET/f'{stem}-{role}.svg').read_text(encoding='utf-8')
                            route.fulfill(status=200, content_type='image/svg+xml', body=payload)
                        p.route('**/assets/concept-animations/*.svg',provide)
                        p.set_content('<meta name="viewport" content="width=device-width,initial-scale=1">'
                          + '<style>body{margin:0}.md-typeset{width:100%}' + CSS.read_text(encoding='utf-8') + '</style>'
                          + '<article class="md-typeset"><p><img data-source-asset-urls class="concept-motion-wide" tabindex="0" '
                          + f'src="https://wiki.example/assets/concept-animations/{stem}-still.svg" '
                          + f'data-motion-src="https://wiki.example/assets/concept-animations/{stem}-motion.svg" '
                          + f'data-still-src="https://wiki.example/assets/concept-animations/{stem}-still.svg" alt="{alt}"></p></article>')
                        assert p.locator('img').evaluate('(img)=>img.complete && img.naturalWidth===640')
                        p.add_script_tag(content=PLAYER.read_text(encoding='utf-8'))
                        btn=p.locator('.concept-motion-toggle')
                        assert btn.count()==1, (stem,lang,width,reduced)
                        img=p.locator('img')
                        initial='-still.svg' if reduced=='reduce' else '-motion.svg'
                        assert initial in img.get_attribute('src')
                        assert p.locator('body').evaluate('(body)=>body.scrollWidth<=innerWidth'),(stem,width,'body overflow')
                        if width<640:
                            parent=p.locator('article p')
                            assert parent.evaluate('(el)=>el.scrollWidth>el.clientWidth'),(stem,width,'scroll missing')
                        btn.focus();p.keyboard.press('Enter')
                        toggled='-motion.svg' if reduced=='reduce' else '-still.svg'
                        assert toggled in img.get_attribute('src')
                        p.keyboard.press('Space')
                        assert initial in img.get_attribute('src')
                        if reduced=='reduce': assert ('播放' in btn.inner_text()) if lang=='zh' else ('Play' in btn.inner_text())
                        else: assert ('暫停' in btn.inner_text()) if lang=='zh' else ('Pause' in btn.inner_text())
                        if width in (320, 1024) and lang=='zh' and reduced=='reduce':
                            p.screenshot(path=str(ARTIFACT/f'{stem}-{width}-zh-reduced.png'), full_page=True)
                        p.close();count+=1
        browser.close()
    print(f'PASS: {count} actual Chromium rendered frames/locale/viewport/reduced-motion/keyboard scenarios')

if __name__=='__main__': main()
