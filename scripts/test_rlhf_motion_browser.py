#!/usr/bin/env python3
"""Browser regression for bilingual RLHF motion assets and existing MkDocs player."""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'docs/assets/concept-animations'
SHOTS = ROOT / 'artifacts/rlhf-motion'
STEMS = ('rlhf-dpo-margin', 'rlhf-reward-sums')
WIDTHS = (320, 360, 720, 1024)
TIMES = (0.2, 2.0, 5.5, 8.3)

def main():
    SHOTS.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            for stem in STEMS:
                for width in WIDTHS:
                    page = browser.new_page(viewport={'width': width, 'height': 550})
                    try:
                        for kind in ('motion', 'still'):
                            svg = (ASSETS / f'{stem}-{kind}.svg').read_text(encoding='utf8')
                            page.set_content('<style>body{margin:0}svg{display:block;width:100%;max-width:640px;height:auto}</style>' + svg)
                            figure = page.locator('svg')
                            assert figure.is_visible()
                            assert figure.bounding_box()['width'] <= min(width, 640) + 0.2
                            moments = TIMES if kind == 'motion' else ('still',)
                            for t in moments:
                                if isinstance(t, float):
                                    page.evaluate('(v) => document.querySelector("svg").setCurrentTime(v)', t)
                                page.wait_for_timeout(60)
                                assert not page.evaluate('document.documentElement.scrollWidth > innerWidth')
                                figure.screenshot(path=str(SHOTS / f'{stem}-{width}-{t}.png'), animations='allow')
                        print(f'visible/responsive: {stem} at {width}px')
                    finally:
                        page.close()

                for lang, alt in (('en', 'DPO visual'), ('zh', '偏好示意圖')):
                    context = browser.new_context(viewport={'width': 360, 'height': 600})
                    page = context.new_page()
                    try:
                        def serve(route):
                            name = route.request.url.rsplit('/', 1)[-1]
                            target = ASSETS / name
                            assert target.is_file(), name
                            route.fulfill(status=200, content_type='image/svg+xml', body=target.read_bytes())
                        page.route('https://wiki.example/assets/concept-animations/**', serve)
                        page.set_content(f'<img src="https://wiki.example/assets/concept-animations/{stem}-motion.svg" alt="{alt}">')
                        page.add_script_tag(path=str(ROOT / 'docs/javascripts/concept-motion.js'))
                        button = page.locator('.concept-motion-toggle')
                        button.wait_for()
                        assert ('Pause' in button.inner_text()) if lang == 'en' else ('暫停' in button.inner_text())
                        button.click()
                        assert page.locator('img').get_attribute('src').endswith('-still.svg')
                        button.focus()
                        page.keyboard.press('Enter')
                        assert page.locator('img').get_attribute('src').endswith('-motion.svg')
                        page.keyboard.press('Space')
                        assert page.locator('img').get_attribute('src').endswith('-still.svg')
                    finally:
                        context.close()

                context = browser.new_context(reduced_motion='reduce')
                page = context.new_page()
                try:
                    page.route('https://wiki.example/assets/concept-animations/**', lambda route: route.fulfill(status=200, content_type='image/svg+xml', body=(ASSETS / route.request.url.rsplit('/', 1)[-1]).read_bytes()))
                    page.set_content(f'<img src="https://wiki.example/assets/concept-animations/{stem}-motion.svg" alt="DPO visual">')
                    page.add_script_tag(path=str(ROOT / 'docs/javascripts/concept-motion.js'))
                    page.locator('.concept-motion-toggle').wait_for()
                    assert page.locator('img').get_attribute('src').endswith('-still.svg')
                finally:
                    context.close()
                print(f'controls/reduced motion: {stem} (en, zh, reduced)')
        finally:
            browser.close()
    print('RLHF motion browser QA: passed; 40 screenshots produced')

if __name__ == '__main__':
    main()
