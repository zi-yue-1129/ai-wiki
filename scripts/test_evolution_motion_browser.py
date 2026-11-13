#!/usr/bin/env python3
"""Chromium QA: evolutionary concept SVGs, GitHub stills, and MkDocs controls."""
from __future__ import annotations
import os
from pathlib import Path
from xml.etree import ElementTree as ET
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'docs/assets/concept-animations'
STEMS = ('genetic-crossover-mutation', 'map-elites-archive')
CSS = (ROOT / 'docs/stylesheets/concept-motion.css').read_text(encoding='utf-8')
JS = (ROOT / 'docs/javascripts/concept-motion.js').read_text(encoding='utf-8')
OUT = ROOT / 'artifacts/evolution-motion'
OUT.mkdir(parents=True, exist_ok=True)
for stem in STEMS:
    for suffix in ('motion', 'still'):
        p = ASSETS / f'{stem}-{suffix}.svg'
        tree = ET.parse(p)
        root = tree.getroot()
        assert root.tag == '{http://www.w3.org/2000/svg}svg'
        assert root.attrib['viewBox'] == '0 0 640 360'
        assert root.find('{http://www.w3.org/2000/svg}title') is not None
        assert root.find('{http://www.w3.org/2000/svg}desc') is not None
        moving = sum(e.tag.rsplit('}', 1)[-1] == 'animate' for e in root.iter())
        assert (moving > 0) == (suffix == 'motion'), (stem, suffix, moving)

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(
        executable_path=os.environ.get('CHROMIUM_EXECUTABLE') or None,
        args=['--no-sandbox'],
    )
    cases = 0
    for stem in STEMS:
        svg = (ASSETS / f'{stem}-motion.svg').read_text(encoding='utf-8')
        for width in (320, 360, 720, 1024):
            page = browser.new_page(viewport={'width': width, 'height': 700})
            page.set_content('<!doctype html><html><body style="margin:0">' + svg + '</body></html>')
            for seconds in (0, 2, 4, 6, 8, 10):
                page.locator('svg').evaluate('(el,t)=>el.setCurrentTime(t)', seconds)
                boxes = page.locator('svg text').evaluate_all('''nodes => nodes.map(el => {
                  const b=el.getBBox(); return {text:el.textContent,x:b.x,y:b.y,w:b.width,h:b.height,
                    opacity:getComputedStyle(el).opacity}; })''')
                for b in boxes:
                    if float(b['opacity']) < 0.05:
                        continue
                    assert b['x'] >= -1 and b['y'] >= -1, (stem, width, seconds, b)
                    assert b['x'] + b['w'] <= 641 and b['y'] + b['h'] <= 361, (stem,width,seconds,b)
                if width in (320, 720) and seconds in (0, 4, 8):
                    page.locator('svg').screenshot(path=str(OUT / f'{stem}-{width}-{seconds}.png'))
                cases += 1
            page.close()
        for lang in ('en', 'zh'):
            for width in (320, 360, 720, 1024):
                for reduced in (False, True):
                    page = browser.new_page(
                        viewport={'width': width, 'height': 600},
                        reduced_motion='reduce' if reduced else 'no-preference',
                    )
                    def serve_svg(route):
                        name=route.request.url.split('/')[-1]
                        target = ASSETS / name
                        assert target.exists(), target
                        route.fulfill(status=200, body=target.read_bytes(), content_type='image/svg+xml')
                    page.route('https://motion.test/assets/concept-animations/*', serve_svg)
                    prefix='https://motion.test/assets/concept-animations/'
                    alt = '演化示意動畫' if lang == 'zh' else 'Evolutionary algorithm animation'
                    html=(f'<div class="concept-motion-wide" role="region" tabindex="0" aria-label="Scroll animation">'
                          f'<img src="{prefix}{stem}-still.svg" data-motion-src="{prefix}{stem}-motion.svg" '
                          f'data-still-src="{prefix}{stem}-still.svg" alt="{alt}"></div>')
                    page.set_content('<!doctype html><html><body>'+html+'</body></html>')
                    page.add_style_tag(content=CSS)
                    page.add_script_tag(content=JS)
                    button = page.locator('.concept-motion-toggle')
                    assert button.count() == 1, (stem,lang,width,reduced,'missing button')
                    img = page.locator('.concept-motion-player img')
                    assert img.count() == 1
                    assert img.get_attribute('src').endswith('-still.svg' if reduced else '-motion.svg')
                    page.wait_for_function('''() => { const i=document.querySelector('.concept-motion-player img');
                        return i && i.complete && i.naturalWidth > 0; }''')
                    if width < 640:
                        assert page.locator('.concept-motion-wide').evaluate('(e)=>e.scrollWidth>e.clientWidth'),(stem,width,'no scroll')
                    button.click()
                    assert img.get_attribute('src').endswith('-motion.svg' if reduced else '-still.svg')
                    button.focus()
                    page.keyboard.press('Space')
                    assert img.get_attribute('src').endswith('-still.svg' if reduced else '-motion.svg')
                    page.keyboard.press('Enter')
                    assert img.get_attribute('src').endswith('-motion.svg' if reduced else '-still.svg')
                    if width == 320 and not reduced:
                        page.screenshot(path=str(OUT / f'{stem}-{lang}-mobile.png'))
                    cases += 1
                    page.close()
    browser.close()
print(f'PASS {cases} Chromium semantic/viewport/player cases for {len(STEMS)} evolutionary concept animations')
