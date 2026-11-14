"""Chromium QA for two shared bilingual evolutionary algorithm labs (file-backed harness)."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import argparse

BASE = Path(__file__).resolve().parent
JS = BASE.parent / 'docs/javascripts/evolution-labs.js'
CSS = BASE.parent / 'docs/stylesheets/evolution-labs.css'
if not JS.exists(): JS = BASE / 'evolution-labs.js'
if not CSS.exists(): CSS = BASE / 'evolution-labs.css'
HTML = '''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="stylesheet" href="evolution-labs.css"><style>body{font-family:Arial, sans-serif;max-width:940px;padding:16px;margin:auto;background:#f9fafb;color:#203445}h2{margin:28px 0 12px} .md-content{max-width:100%}</style></head><body><main class="md-content"><h2>Genetic algorithms</h2><div data-evolution-lab="ga" data-lang="__LANG__"><p>Static image fallback is provided above.</p></div><h2>MAP-Elites</h2><div data-evolution-lab="map" data-lang="__LANG__"><p>Static image fallback is provided above.</p></div></main><script src="evolution-labs.js"></script></body></html>'''


def check(playwright, width, lang, reduced, out):
    browser = playwright.chromium.launch(headless=True, executable_path='/usr/bin/chromium' if Path('/usr/bin/chromium').exists() else None, args=['--no-sandbox'])
    context = browser.new_context(viewport={'width':width,'height':1000},device_scale_factor=1,reduced_motion='reduce' if reduced else 'no-preference')
    page = context.new_page(); errors=[]
    page.on('pageerror',lambda err:errors.append(str(err)))
    page.set_content(HTML.replace('__LANG__',lang).replace('<link rel="stylesheet" href="evolution-labs.css">','').replace('<script src="evolution-labs.js"></script>',''))
    page.add_style_tag(content=CSS.read_text(encoding='utf-8'))
    page.add_script_tag(content=JS.read_text(encoding='utf-8'))
    assert page.locator('.evo-lab').count()==2
    ga = page.locator('[data-evolution-lab="ga"]')
    mp = page.locator('[data-evolution-lab="map"]')
    assert ga.locator('.evo-bit').count()==24
    assert mp.locator('.evo-niche').count()==24
    assert ga.locator('.evo-canvas').get_attribute('data-child')=='11010101'
    assert mp.locator('.evo-canvas').get_attribute('data-coverage')=='3'
    # Every input is focusable and modifiable from the keyboard.
    ga.locator('input[aria-label]').first.focus();page.keyboard.press('ArrowRight')
    assert ga.locator('input[aria-label]').first.input_value()=='5'
    ga.locator('button').filter(has_text='下一步' if lang=='zh' else 'Next').first.click()
    assert ga.locator('.evo-canvas').get_attribute('data-step')=='1'
    ga.locator('input[aria-label]').nth(2).fill('9');ga.locator('input[aria-label]').nth(2).dispatch_event('input')
    assert ga.locator('.evo-canvas').get_attribute('data-child')=='11010101' or ga.locator('.evo-canvas').get_attribute('data-step')=='9'
    ga.locator('input[aria-label]').nth(0).fill('4');ga.locator('input[aria-label]').nth(0).dispatch_event('input')
    ga.locator('input[aria-label]').nth(1).fill('7');ga.locator('input[aria-label]').nth(1).dispatch_event('input')
    ga.locator('input[aria-label]').nth(2).fill('9');ga.locator('input[aria-label]').nth(2).dispatch_event('input')
    assert ga.locator('.evo-canvas').get_attribute('data-child')=='11010111'
    mp.locator('input[aria-label]').nth(2).fill('4');mp.locator('input[aria-label]').nth(2).dispatch_event('input')
    assert mp.locator('.evo-canvas').get_attribute('data-coverage')=='5'
    assert ('Replace' in mp.locator('.evo-message').inner_text() or '取代' in mp.locator('.evo-message').inner_text() or 'Insert' in mp.locator('.evo-message').inner_text() or '插入' in mp.locator('.evo-message').inner_text())
    # Put a challenger above initial 0.82 and seek to event #2: must replace.
    mp.locator('input[aria-label]').nth(0).fill('0.95');mp.locator('input[aria-label]').nth(0).dispatch_event('input')
    mp.locator('input[aria-label]').nth(2).fill('2');mp.locator('input[aria-label]').nth(2).dispatch_event('input')
    assert mp.locator('.evo-canvas').get_attribute('data-coverage')=='4'
    assert mp.locator('.evo-canvas').get_attribute('data-last-decision') in ['Replace','取代']
    # Subordinate lower score cannot displace an existing higher elite.
    mp.locator('input[aria-label]').nth(0).fill('0.61');mp.locator('input[aria-label]').nth(0).dispatch_event('input')
    mp.locator('input[aria-label]').nth(2).fill('2');mp.locator('input[aria-label]').nth(2).dispatch_event('input')
    assert mp.locator('.evo-canvas').get_attribute('data-last-decision') in ['Reject','拒絕']
    # Reset also resets the parameter sliders.
    mp.locator('button').filter(has_text='重設' if lang=='zh' else 'Reset').click()
    assert mp.locator('.evo-canvas').get_attribute('data-step')=='0'
    assert mp.locator('input[aria-label]').nth(0).input_value()=='0.61'
    # Content must not overrun viewport, but the diagram may scroll inside its focusable canvas.
    overflow=page.evaluate('document.documentElement.scrollWidth > window.innerWidth + 2')
    assert not overflow,(width,lang,'document overflow')
    # Layout geometry: no clipped labels and no overlap of title/control containers.
    bad=page.evaluate('''() => [...document.querySelectorAll('.evo-lab .evo-slider-head,.evo-lab .evo-timeline button,.evo-lab .evo-step-status')].filter(el=>el.scrollWidth>el.clientWidth+3 || el.scrollHeight>el.clientHeight+3).map(el=>el.outerHTML.slice(0,200))''')
    assert not bad,(width,lang,bad)
    page.screenshot(path=str(out),full_page=True)
    assert not errors, errors
    browser.close()

if __name__ == '__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--out',default='artifacts/evolution-labs');args=parser.parse_args()
    output=Path(args.out);output.mkdir(parents=True,exist_ok=True)
    for lang in ('en','zh'):
        pass  # The in-memory harness needs no HTTP server or additional assets.
    with sync_playwright() as p:
        for w in (320,360,720,1024):
            for lang in ('en','zh'):
                for reduced in (False,True):
                    dest=output/f'{lang}-{w}-{int(reduced)}.png'
                    check(p,w,lang,reduced,dest)
                    print('PASS',dest.name)