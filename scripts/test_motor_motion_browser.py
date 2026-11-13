#!/usr/bin/env python3
"""Actual Chromium QA for forward-model and minimal-intervention motion (EN / zh-TW)."""
from pathlib import Path
import base64
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'docs/assets/concept-animations'
JS = (ROOT / 'docs/javascripts/concept-motion.js').read_text(encoding='utf-8')
CSS = (ROOT / 'docs/stylesheets/concept-motion.css').read_text(encoding='utf-8')

def verify(page, stem, zh=False, reduced=False):
    lang = '手部狀態估計' if zh else 'Motor state estimation'
    preview = base64.b64encode((ASSETS / f'{stem}-still.svg').read_bytes()).decode('ascii')
    source = f'data:image/svg+xml;base64,{preview}#concept-animations/{stem}-still.svg'
    doc = f'''<!doctype html><html lang="{'zh-TW' if zh else 'en'}"><meta charset="utf-8">
<style>{CSS}</style><img alt="{lang}" src="{source}"><script>{JS}</script></html>'''
    page.set_content(doc)
    page.locator('.concept-motion-toggle').wait_for()
    image = page.locator('.concept-motion-player img')
    still = f'{stem}-still.svg'
    if reduced:
        assert still in image.get_attribute('src'), 'reduced-motion fallback absent'
    else:
        assert f'{stem}-motion.svg' in image.get_attribute('src')
    btn = page.locator('.concept-motion-toggle').first
    btn.click()
    assert (f'{stem}-motion.svg' if reduced else still) in image.get_attribute('src')
    btn.focus(); page.keyboard.press('Space')
    assert (still if reduced else f'{stem}-motion.svg') in image.get_attribute('src')
    player = page.locator('.concept-motion-player')
    if page.viewport_size['width'] < 681:
        assert player.evaluate('(e)=>e.scrollWidth>e.clientWidth')
        player.focus(); page.keyboard.press('ArrowRight')
        page.wait_for_timeout(80)
        assert player.evaluate('(e)=>e.scrollLeft') > 0
    assert image.evaluate('(e)=>e.complete && e.naturalWidth>0'), 'SVG failed to decode'

def main():
    passed = 0
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        for stem in ('forward-prediction-correction', 'ofc-selective-feedback'):
            for width in (320, 360, 720, 1024):
                for zh in (False, True):
                    for reduced in (False, True):
                        context = browser.new_context(viewport={'width':width,'height':480}, reduced_motion='reduce' if reduced else 'no-preference')
                        try:
                            verify(context.new_page(), stem, zh, reduced)
                            passed += 1
                        finally:
                            context.close()
        browser.close()
    print(f'Motor motion browser checks: {passed}/32 passed')

if __name__ == '__main__':
    main()
