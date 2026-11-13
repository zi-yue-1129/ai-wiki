#!/usr/bin/env python3
"""Browser regression: real shared motion player, static GitHub previews, keyboard and reduced motion.
Use in CI after Playwright/Chromium installation; no web server or network needed.
"""
import base64
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'docs/assets/concept-animations'
JS = ROOT / 'docs/javascripts/concept-motion.js'
CSS = ROOT / 'docs/stylesheets/concept-motion.css'
CASES = ('latent-space-denoise', 'video-joint-denoising')

def uri(path):
    return 'data:image/svg+xml;base64,' + base64.b64encode(path.read_bytes()).decode('ascii') + '#concept-animations/' + path.name

def run():
    with sync_playwright() as p:
        kwargs = {'headless': True, 'args': ['--no-sandbox']}
        if os.environ.get('CHROMIUM_PATH'):
            kwargs['executable_path'] = os.environ['CHROMIUM_PATH']
        browser = p.chromium.launch(**kwargs)
        tests = 0
        for topic in CASES:
            still = uri(ASSETS / f'{topic}-still.svg')
            motion = uri(ASSETS / f'{topic}-motion.svg')
            for width in (320, 360, 800, 1024):
                for reduced in (False, True):
                    page = browser.new_page(viewport={'width': width, 'height': 700}, reduced_motion='reduce' if reduced else 'no-preference')
                    # Style mirrors raw-HTML GitHub fallback used in both bilingual chapters.
                    html = '''<!doctype html><html lang="en"><meta charset="UTF-8"><style>body{margin:0;padding:12px;font-family:Arial}</style><div class="concept-motion-scroll" tabindex="0" aria-label="Scrollable diagram">
                      <img src="''' + still + '" data-motion-src="' + motion + '" data-still-src="' + still + '" alt="Latent/video explanatory diagram"></div></html>'
                    page.set_content(html)
                    page.add_style_tag(content=CSS.read_text())
                    page.add_script_tag(content=JS.read_text())
                    toggle = page.locator('.concept-motion-toggle')
                    assert toggle.count() == 1, (topic,width,reduced,'player did not initialize')
                    image = page.locator('img')
                    original = image.get_attribute('src')
                    assert original == (still if reduced else motion), (topic,width,reduced,'initial reduced state')
                    assert image.evaluate('(e)=>e.complete && e.naturalWidth>0'), (topic,width,'SVG decode')
                    toggle.click()
                    assert image.get_attribute('src') == (motion if reduced else still), (topic,width,reduced,'pause/play')
                    toggle.focus()
                    page.keyboard.press('Space')
                    assert image.get_attribute('src') == original, (topic,width,reduced,'keyboard Space')
                    toggle.focus()
                    page.keyboard.press('Enter')
                    assert image.get_attribute('src') != original, (topic,width,reduced,'keyboard Enter')
                    viewport = page.locator('.concept-motion-scroll').evaluate('(el)=>[el.clientWidth,el.scrollWidth]')
                    if width < 800:
                        assert viewport[1]>viewport[0], (topic,width,'mobile horizontal scroll')
                        page.locator('.concept-motion-scroll').focus()
                        page.keyboard.press('ArrowRight')
                    tests += 1
                    page.close()
        browser.close()
        print(f'PASS: {tests}/{tests} topic × responsive-width × reduced-motion combinations')

if __name__ == '__main__': run()