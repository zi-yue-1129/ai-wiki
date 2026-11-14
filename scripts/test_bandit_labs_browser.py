"""Chromium integration and screenshot check for deterministic stochastic-bandit labs."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import os

ROOT = Path(__file__).resolve().parent
if (ROOT.parent / "docs/javascripts/bandit-labs.js").exists():
    JS = ROOT.parent / "docs/javascripts/bandit-labs.js"
    CSS = ROOT.parent / "docs/stylesheets/bandit-labs.css"
else:
    JS = ROOT / "bandit-labs.js"
    CSS = ROOT / "bandit-labs.css"
ARTIFACTS = Path(os.environ.get('BANDIT_LAB_ARTIFACTS','artifacts/bandit-labs'))
ARTIFACTS.mkdir(parents=True, exist_ok=True)
HTML = '''<!doctype html><html lang="LANG"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>body{margin:0;padding:20px;font:16px system-ui;color:#213547} main{max-width:860px;margin:auto}</style></head><body>
<main><h1>Stochastic Bandits</h1>
<h2>UCB1</h2><div class="bandit-lab" data-bandit-lab="ucb" data-lang="LANG"><p>Static illustration above remains visible without JavaScript.</p></div>
<h2>Thompson</h2><div class="bandit-lab" data-bandit-lab="thompson" data-lang="LANG"><p>Static fallback.</p></div>
</main></body></html>'''

def main():
    with sync_playwright() as p:
        executable = os.getenv('CHROMIUM_PATH') or ('/usr/bin/chromium' if Path('/usr/bin/chromium').exists() else None)
        browser = p.chromium.launch(headless=True, executable_path=executable, args=['--no-sandbox'])
        cases = 0
        for lang in ('en', 'zh-TW'):
            for width in (320, 360, 720, 1024):
                for reduced in (False, True):
                    context = browser.new_context(
                        viewport={'width': width, 'height': 950},
                        reduced_motion='reduce' if reduced else 'no-preference'
                    )
                    page = context.new_page()
                    errors = []
                    page.on('pageerror', lambda e: errors.append(str(e)))
                    page.set_content(HTML.replace('LANG', lang))
                    assert page.get_by_text('Static fallback.').count() == 1
                    page.add_style_tag(content=CSS.read_text(encoding='utf8'))
                    page.add_script_tag(content=JS.read_text(encoding='utf8'))
                    page.wait_for_selector('[data-bandit-lab="thompson"] [data-role="svg"] path')
                    assert not errors, errors
                    assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth')
                    ucb = page.locator('[data-bandit-lab="ucb"]')
                    ts = page.locator('[data-bandit-lab="thompson"]')
                    assert ucb.locator('[data-role="svg"] rect').count() > 5
                    assert 'B' in ucb.locator('[data-role="metrics"]').inner_text()
                    ucb.locator('[data-role="seek"]').fill('2')
                    assert 'A' in ucb.locator('[data-role="metrics"]').inner_text()
                    assert '1.63' in ucb.locator('[data-role="metrics"]').inner_text()
                    ucb.locator('[data-role="reward"]').fill('1')
                    assert 'B' in ucb.locator('[data-role="metrics"]').inner_text()
                    ucb.locator('[data-action="reset"]').click()
                    assert ucb.locator('[data-role="seek"]').input_value() == '0'
                    ts.locator('[data-action="next"]').click()
                    assert 'C' in ts.locator('[data-role="metrics"]').inner_text()
                    ts.locator('[data-action="next"]').click()
                    assert '(5,3)' in ts.locator('[data-role="metrics"]').inner_text()
                    ts.locator('[data-role="outcome"]').select_option('0')
                    assert '(4,4)' in ts.locator('[data-role="metrics"]').inner_text()
                    ts.locator('[data-action="next"]').click()
                    assert 'A' in ts.locator('[data-role="metrics"]').inner_text()
                    ts.locator('[data-action="reset"]').click()
                    assert '(4,3)' in ts.locator('[data-role="metrics"]').inner_text()
                    if width <= 360:
                        assert page.evaluate(
                            'document.querySelector(".bandit-lab-canvas").scrollWidth > document.querySelector(".bandit-lab-canvas").clientWidth'
                        )
                    if reduced:
                        ucb.locator('[data-action="toggle"]').click()
                        assert ucb.locator('[data-action="toggle"]').inner_text() in ('Play', '播放')
                    else:
                        ucb.locator('[data-action="toggle"]').click()
                        assert ucb.locator('[data-action="toggle"]').inner_text() in ('Pause', '暫停')
                        ucb.locator('[data-action="toggle"]').click()
                    if width in (360, 1024) and not reduced:
                        page.screenshot(path=str(ARTIFACTS / f'{lang}-{width}.png'), full_page=True)
                    cases += 1
                    context.close()
        browser.close()
        print(f'{cases} Chromium bilingual/viewport/reduced-motion cases passed')


if __name__ == '__main__':
    main()
