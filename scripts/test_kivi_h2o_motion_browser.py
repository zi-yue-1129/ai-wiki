#!/usr/bin/env python3
"""Chromium regression for KIVI/H2O concept motion and shared bilingual controls.

Run after: python -m pip install playwright; python -m playwright install chromium.
All assets are served in-memory; no external network or third-party assets.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'docs/assets/concept-animations'
PLAYER = ROOT / 'docs/javascripts/concept-motion.js'
TOPICS = ('kivi-quantization-axis', 'h2o-heavy-hitter-selection')
WIDTHS = (320, 360, 720, 1024)
OUT = ROOT / 'artifacts/kivi-h2o-browser'


def check(browser, stem, width, chinese, reduced):
    context = browser.new_context(viewport={'width': width, 'height': 510}, reduced_motion='reduce' if reduced else 'no-preference')
    context.route('**/concept-animations/*.svg', lambda route: route.fulfill(
        status=200, content_type='image/svg+xml', body=(ASSETS / route.request.url.rsplit('/', 1)[-1]).read_bytes()
    ))
    page = context.new_page()
    lang = 'zh-TW' if chinese else 'en'
    src = f'https://wiki.test/assets/concept-animations/{stem}-motion.svg'
    alt = '教學概念動畫' if chinese else 'Instructional concept animation'
    page.set_content(f'''<!doctype html><html lang="{lang}"><style>body{{margin:0;padding:8px}}img{{max-width:100%;height:auto}}button:focus-visible{{outline:3px solid #168b82}}</style><body><main><img alt="{alt}" src="{src}"></main></body></html>''')
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
    assert image.evaluate('(img)=>img.getBoundingClientRect().right <= innerWidth + 1'), f'{stem}: horizontal clipping at {width}px'
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
                    check(browser, stem, width, chinese, False)
                check(browser, stem, width, False, True)
        browser.close()
    print('KIVI/H2O: 24 Chromium SVG/player checks (English, zh-TW, reduced motion), keyboard Enter/Space, responsive image bounds: PASS')


if __name__ == '__main__':
    main()
