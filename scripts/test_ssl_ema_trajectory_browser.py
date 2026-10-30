#!/usr/bin/env python3
"""Real Chromium integration of MoCo/BYOL labs and discrete EMA trajectory."""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
LAB_JS = (ROOT / 'docs/javascripts/self-supervised-labs.js').read_text()
EMA_JS = (ROOT / 'docs/javascripts/ssl-ema-trajectory.js').read_text()
LAB_CSS = (ROOT / 'docs/stylesheets/self-supervised-labs.css').read_text()
EMA_CSS = (ROOT / 'docs/stylesheets/ssl-ema-trajectory.css').read_text()
OUT = ROOT / 'artifacts/ssl-ema-trajectory'
OUT.mkdir(parents=True, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
    for kind in ('moco', 'byol'):
        for locale in ('en', 'zh-TW'):
            for width in (360, 900):
                for reduced in (False, True):
                    page = browser.new_page(viewport={'width':width,'height':850},
                        reduced_motion='reduce' if reduced else 'no-preference')
                    errors = []
                    page.on('pageerror', lambda e: errors.append(str(e)))
                    page.set_content('<!doctype html><meta name="viewport" content="width=device-width,initial-scale=1">'
                        f'<div data-self-supervised-lab="{kind}" data-locale="{locale}"></div>')
                    page.add_style_tag(content=LAB_CSS + '\n' + EMA_CSS)
                    page.add_script_tag(content=LAB_JS)
                    page.add_script_tag(content=EMA_JS)
                    assert page.locator('.ssl-ema-trajectory').count() == 1
                    seek = page.locator('[data-act="seek"]')
                    momentum = page.locator('[data-act="momentum"]')
                    for m, expected in ((0.50,'0.575'),(0.90,'0.355'),(0.99,'0.306')):
                        momentum.fill(str(m))
                        for step in (0,2,3,4,9,14):
                            seek.fill(str(step))
                            assert page.evaluate('''() => {
                              const svg=document.querySelector('.ssl-ema-chart svg');
                              return [...svg.querySelectorAll('text')].every(t=>{
                                const b=t.getBBox();
                                return b.x>=-1&&b.y>=-1&&b.x+b.width<=601&&b.y+b.height<=225;
                              });
                            }'''), (kind,locale,width,m,step,'SVG text clipped')
                            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
                            assert page.locator('.ssl-ema-chart circle').count() == 8
                            if step == 4:
                                assert expected in page.locator('.ssl-ema-readout').inner_text()
                    # Autoplay changes the existing computation trace but does
                    # not fire a native input event on the seek slider.
                    momentum.fill('0.9')
                    seek.fill('0')
                    page.locator('[data-act="speed"]').select_option('2')
                    page.locator('[data-act="play"]').click()
                    page.wait_for_timeout(850)
                    assert int(seek.input_value()) >= 1, 'autoplay did not advance'
                    page.locator('[data-act="play"]').click()
                    # Mimic the player changing seek without dispatching input.
                    seek.evaluate("(e)=>e.value='4'")
                    page.locator('.ssl-compute').evaluate("(e)=>e.textContent='autoplay render changed'")
                    page.wait_for_timeout(25)
                    assert '0.355' in page.locator('.ssl-ema-readout').inner_text()
                    seek.fill('4')
                    momentum.fill('0.50')
                    assert not errors, errors
                    page.locator('.ssl-ema-trajectory').screenshot(path=str(OUT/f'{kind}-{locale}-{width}-reduced-{reduced}.png'))
                    page.close()
    browser.close()
print('PASS: 16 Chromium cases, three momentum values, discrete states, autoplay synchronization, bounds, reduced motion')
