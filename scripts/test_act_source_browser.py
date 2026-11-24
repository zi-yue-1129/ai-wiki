#!/usr/bin/env python3
"""Chromium regression for ACT concept motion and shared bilingual controls.

Run after: python -m pip install playwright; python -m playwright install chromium.
All assets are served in-memory; no external network or third-party assets.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'docs/assets/concept-animations'
PLAYER = ROOT / 'docs/javascripts/concept-motion.js'
TOPICS = ('act-temporal-ensemble', 'act-cvae-train-deploy')
WIDTHS = (320, 360, 720, 1024)
OUT = ROOT / 'artifacts/act-source-browser'


def check(browser, stem, width, chinese, reduced):
    context = browser.new_context(viewport={'width': width, 'height': 510}, reduced_motion='reduce' if reduced else 'no-preference')
    context.route('**/concept-animations/*.svg', lambda route: route.fulfill(
        status=200, content_type='image/svg+xml', body=(ASSETS / route.request.url.rsplit('/', 1)[-1]).read_bytes()
    ))
    page = context.new_page()
    lang = 'zh-TW' if chinese else 'en'
    src = f'https://wiki.test/assets/concept-animations/{stem}-motion.svg'
    alt = '教學概念動畫' if chinese else 'Instructional concept animation'
    page.set_content(f'''<!doctype html><html lang="{lang}"><style>body{{margin:0;padding:8px}}img{{width:640px;min-width:640px;max-width:none;height:auto}}#scroll{{max-width:100%;overflow-x:auto}}button:focus-visible{{outline:3px solid #168b82}}</style><body><main><div id="scroll" tabindex="0" role="region" aria-label="Scrollable figure"><img alt="{alt}" src="{src.replace('-motion.svg','-still.svg')}" data-motion-src="{src}" data-still-src="{src.replace('-motion.svg','-still.svg')}"></div></main></body></html>''')
    page.add_script_tag(content=PLAYER.read_text(encoding='utf-8'))
    button = page.locator('button.concept-motion-toggle')
    assert button.count() == 1, f'{stem}: missing shared Play/Pause control'
    image = page.locator('img')
    page.wait_for_function('(selector)=>{let img=document.querySelector(selector);return img&&img.complete&&img.naturalWidth===640}', arg='img')
    assert image.get_attribute('src').endswith(('-still.svg' if reduced else '-motion.svg'))
    assert (('播放' if reduced else '暫停') in button.inner_text()) if chinese else (('Play' if reduced else 'Pause') in button.inner_text())
    assert button.get_attribute('aria-label')
    button.focus()
    assert button.evaluate('(b)=>document.activeElement===b'), 'button not focusable'
    page.keyboard.press('Enter')
    assert image.get_attribute('src').endswith(('-motion.svg' if reduced else '-still.svg')), f'{stem}: keyboard Enter failed'
    page.wait_for_function('(selector)=>{let img=document.querySelector(selector);return img&&img.complete&&img.naturalWidth===640}', arg='img')
    page.keyboard.press('Space')
    assert image.get_attribute('src').endswith(('-still.svg' if reduced else '-motion.svg')), f'{stem}: keyboard Space failed'
    page.wait_for_function('(selector)=>{let img=document.querySelector(selector);return img&&img.complete&&img.naturalWidth===640}', arg='img')
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), f'{stem}: document overflow at {width}px'
    scroller = page.locator('#scroll')
    scroller.focus()
    assert scroller.evaluate('(e)=>document.activeElement===e')
    if width < 656:
        page.keyboard.press('ArrowRight')
        page.wait_for_function("document.querySelector('#scroll').scrollLeft>0")
        scroller.evaluate('(e)=>e.scrollLeft=e.scrollWidth')
        page.wait_for_timeout(150)
        assert scroller.evaluate('(e)=>Math.abs(e.scrollLeft-(e.scrollWidth-e.clientWidth))<2')
        OUT.mkdir(parents=True,exist_ok=True)
        page.screenshot(path=str(OUT / f'{stem}-{width}-{lang}-{reduced}-right.png'))
        scroller.evaluate('(e)=>e.scrollLeft=0')
    OUT.mkdir(parents=True, exist_ok=True)
    image.screenshot(path=str(OUT / f'{stem}-{width}-{lang}-{("reduced" if reduced else "play")}.png'))
    context.close()


def main():
    assert PLAYER.is_file(), 'shared concept-motion.js missing'
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, **({'executable_path': '/usr/bin/chromium'} if Path('/usr/bin/chromium').is_file() else {}), args=['--no-sandbox'])
        for stem in TOPICS:
            for width in WIDTHS:
                for chinese in (False, True):
                    for reduced in (False, True):
                        check(browser, stem, width, chinese, reduced)
        browser.close()
    print('ACT: 32 Chromium SVG/player checks (English, zh-TW, reduced motion), keyboard Enter/Space, source-owned focusable local scroll and whole-document bounds: PASS')


if __name__ == '__main__':
    main()
