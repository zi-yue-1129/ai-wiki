#!/usr/bin/env python3
"""Live Chromium checks for bilingual, GitHub-static-first LIME/SHAP concept players."""
from __future__ import annotations
import hashlib,shutil,xml.etree.ElementTree as ET
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'docs/assets/concept-animations'
JS=ROOT/'docs/javascripts/concept-motion.js'
CSS=ROOT/'docs/stylesheets/concept-motion.css'
PAIRS=('lime-local-surrogate','shap-coalition-marginals')
PAGES=ROOT/'docs/society/interpretability'


def run():
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True,**({"executable_path":shutil.which("chromium")} if shutil.which("chromium") else {}))
        checks=0
        for stem in PAIRS:
            originals={s:(ASSETS/f'{stem}-{s}.svg').read_text(encoding='utf-8') for s in ('still','motion')}
            assert '<animate ' in originals['motion']
            assert '<animate ' not in originals['still']
            for state in ('still','motion'):
                root=ET.fromstring(originals[state])
                assert root.attrib.get('viewBox')=='0 0 640 360'
                assert len(root.findall('{http://www.w3.org/2000/svg}title')) == 1
                for e in root.iter():
                    tag=e.tag.split('}')[-1]
                    assert tag not in {'script','foreignObject','iframe','image'}
                    assert not any(k.lower().startswith('on') for k in e.attrib)
                    if tag=='animate':assert e.attrib.get('repeatCount')=='indefinite'
            topic='lime' if stem.startswith('lime') else 'shap'
            for locale in ('.md','.zh-TW.md'):
                content=(PAGES/(topic+locale)).read_text(encoding='utf-8')
                assert f'{stem}-still.svg' in content and f'{stem}-motion.svg' in content
                assert 'data-motion-src' in content

            for width in (320,360,720,1024):
                for lang in ('en','zh'):
                    page=browser.new_page(viewport={'width':width,'height':750})
                    def respond(route):
                        url=route.request.url
                        suffix='motion' if url.endswith('-motion.svg') else 'still'
                        route.fulfill(status=200,content_type='image/svg+xml',body=originals[suffix])
                    page.route('https://animation.test/**',respond)
                    alt=('LIME 局部模型與特徵擾動' if stem.startswith('lime') else 'SHAP 聯盟的加權邊際貢獻') if lang=='zh' else ('LIME weighted local surrogate' if stem.startswith('lime') else 'SHAP coalition contributions')
                    html=f'''<!doctype html><html><head><meta charset="utf-8" /></head><body>
                    <div class="concept-motion-viewport" tabindex="0" aria-label="Concept visualisation">
                    <div class="concept-motion-fixed"><img alt="{alt}" src="https://animation.test/concept-animations/{stem}-still.svg"
                    data-motion-src="https://animation.test/concept-animations/{stem}-motion.svg" data-still-src="https://animation.test/concept-animations/{stem}-still.svg" /></div></div>
                    </body></html>'''
                    page.set_content(html)
                    page.add_style_tag(content=CSS.read_text(encoding='utf-8'))
                    page.add_script_tag(content=JS.read_text(encoding='utf-8'))
                    page.locator('.concept-motion-toggle').wait_for()
                    img=page.locator('.concept-motion-player img')
                    assert img.evaluate('(x)=>x.complete && x.naturalWidth===640')
                    assert img.get_attribute('src').endswith('-motion.svg')
                    assert page.locator('.concept-motion-toggle').count()==1
                    viewport=page.locator('.concept-motion-viewport')
                    assert viewport.evaluate('(x)=>x.clientWidth<=window.innerWidth')
                    if width<640:
                        assert viewport.evaluate('(x)=>x.scrollWidth>x.clientWidth')
                        viewport.focus();page.keyboard.press('ArrowRight'); page.keyboard.press('ArrowRight'); page.wait_for_timeout(180)
                        assert viewport.evaluate('(x)=>x.scrollLeft>0')
                    button=page.locator('.concept-motion-toggle')
                    assert ('播放' in button.inner_text() or 'Play' in button.inner_text()) is False
                    button.click()
                    assert img.get_attribute('src').endswith('-still.svg')
                    assert ('播放' in button.inner_text() or 'Play' in button.inner_text())
                    button.focus();page.keyboard.press('Enter')
                    assert img.get_attribute('src').endswith('-motion.svg')
                    button.focus();page.keyboard.press('Space')
                    assert img.get_attribute('src').endswith('-still.svg')
                    checks+=1
                    page.close()
            page=browser.new_page(viewport={'width':720,'height':650},reduced_motion='reduce')
            page.route('https://animation.test/**',lambda route:route.fulfill(status=200,content_type='image/svg+xml',body=originals['still'] if route.request.url.endswith('-still.svg') else originals['motion']))
            page.set_content(f'<div class="concept-motion-viewport"><div class="concept-motion-fixed"><img alt="SHAP 測試" src="https://animation.test/concept-animations/{stem}-still.svg" data-motion-src="https://animation.test/concept-animations/{stem}-motion.svg" /></div></div>')
            page.add_script_tag(content=JS.read_text())
            page.locator('.concept-motion-toggle').wait_for()
            assert page.locator('img').get_attribute('src').endswith('-still.svg')
            checks+=1;page.close()
        browser.close()
    print(f'Passed {checks} bilingual viewport/keyboard/reduced-motion Chromium cases')

if __name__=='__main__':run()
