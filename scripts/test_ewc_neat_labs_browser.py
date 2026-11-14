"""Chromium smoke/numerical regression for standalone bilingual EWC/NEAT labs.

Invoke in repository root with: python scripts/test_ewc_neat_labs_browser.py
"""
from pathlib import Path
from tempfile import TemporaryDirectory
from playwright.sync_api import sync_playwright
import os
import re

ROOT = Path(__file__).resolve().parents[1]
JS = ROOT / 'docs' / 'javascripts' / 'ewc-neat-labs.js'
CSS = ROOT / 'docs' / 'stylesheets' / 'ewc-neat-labs.css'
# Local authoring layout before upload to repository.
if not JS.exists():
    ROOT = Path(__file__).resolve().parent
    JS = ROOT / 'ewc-neat-labs.js'
    CSS = ROOT / 'ewc-neat-labs.css'


def main():
    assert JS.is_file() and CSS.is_file()
    screenshots = Path('artifacts/ewc-neat-labs')
    screenshots.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory() as temp:
        for locale in ('en', 'zh-TW'):
            page = Path(temp) / f'{locale}.html'
            page.write_text('<!doctype html><html lang="' + locale + '"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
                '<style>body{font-family:system-ui,sans-serif;margin:12px;max-width:1020px}</style><style>' + CSS.read_text() + '</style></head><body>'
                '<div data-ewc-neat-lab="ewc" data-locale="' + locale + '"><p>Fallback numerical table: EWC high/low Fisher</p></div>'
                '<div data-ewc-neat-lab="neat" data-locale="' + locale + '"><p>Fallback mutation states: #3 / #8 / #9</p></div>'
                '<script>' + JS.read_text() + '</script></body></html>', encoding='utf-8')
            with sync_playwright() as p:
                browser_args = {'headless': True}
                if os.path.exists('/usr/bin/chromium'):
                    browser_args['executable_path'] = '/usr/bin/chromium'
                    browser_args['args'] = ['--no-sandbox']
                browser = p.chromium.launch(**browser_args)
                for width in (320, 360, 760, 1024):
                    for reduced in (False, True):
                        tab = browser.new_page(viewport={'width': width, 'height': 760}, reduced_motion='reduce' if reduced else 'no-preference')
                        tab.set_content(page.read_text(encoding="utf-8"))
                        assert tab.locator('[data-ewc-neat-lab] .en-lab').count() == 2
                        assert tab.locator('[data-ewc-neat-lab] svg title').count() == 2
                        assert tab.evaluate('document.documentElement.scrollWidth <= window.innerWidth'), (locale,width,'document overflow')
                        # Graph is intentionally wide; narrow viewport has a keyboard-focusable scroller.
                        assert tab.locator('[data-ewc-neat-lab="ewc"] .en-lab-frame').get_attribute('tabindex') == '0'
                        ewc = tab.locator('[data-ewc-neat-lab="ewc"]')
                        neat = tab.locator('[data-ewc-neat-lab="neat"]')
                        ewc.locator('[data-action=seek]').fill('1')
                        assert '0.080' in ewc.locator('.en-lab-results').inner_text()  # eta .08, θ1=.08
                        ewc.locator('[data-setting=eta]').fill('0.12')
                        assert '0.120' in ewc.locator('.en-lab-results').inner_text()
                        ewc.locator('[data-action=seek]').fill('18')
                        assert ewc.locator('[data-action=next]').is_disabled()
                        if width in (320, 1024) and not reduced:
                            tab.screenshot(path=str(screenshots / f'{locale}-{width}-ewc-final.png'), full_page=True)
                        ewc.locator('[data-action=reset]').click()
                        assert '0/18' in ewc.locator('.en-lab-results').inner_text()
                        neat.locator('[data-action=seek]').fill('5')
                        assert '1.120' in neat.locator('.en-lab-results').inner_text()
                        assert '0.000' in neat.locator('.en-lab-results').inner_text()
                        neat.locator('[data-setting=activation]').select_option('tanh')
                        assert '0.000' not in neat.locator('.en-lab-results').inner_text().split('Difference:')[-1].split('差值:')[-1] if locale == 'en' else '0.000' not in neat.locator('.en-lab-results').inner_text().split('差值:')[-1]
                        if width in (320, 1024) and not reduced:
                            tab.screenshot(path=str(screenshots / f'{locale}-{width}-neat-final.png'), full_page=True)
                        neat.locator('[data-action=reset]').click()
                        assert '0/5' in neat.locator('.en-lab-results').inner_text()
                        if width in (320, 1024) and not reduced:
                            tab.screenshot(path=str(screenshots / f'{locale}-{width}.png'), full_page=True)
                        tab.close()
                # Confirm no-JS static fallback survives.
                no_js = browser.new_page(java_script_enabled=False)
                no_js.set_content(page.read_text(encoding="utf-8"))
                assert no_js.get_by_text('Fallback numerical table', exact=False).count() == 1
                browser.close()
    print('PASS: 16 bilingual responsive/reduced-motion cases + numerical updates + static fallback')

if __name__ == '__main__':
    main()