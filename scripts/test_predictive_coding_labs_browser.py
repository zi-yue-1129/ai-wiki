#!/usr/bin/env python3
"""Real Chromium, bilingual, responsive and numerical QA for predictive-coding toy labs."""
from __future__ import annotations
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
JS = ROOT / 'docs/javascripts/predictive-coding-labs.js'
CSS = ROOT / 'docs/stylesheets/predictive-coding-labs.css'
DOCS = ROOT / 'docs/brain-mind/predictive-coding'
OUT = ROOT / 'artifacts/predictive-coding-labs'
TOPICS = {'residual': 'rao-ballard-1999', 'settling': 'whittington-bogacz-2017'}

def render(pw) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    browser = pw.chromium.launch(headless=True,
        executable_path=os.environ.get('CHROMIUM_EXECUTABLE') or None,
        args=['--no-sandbox'])
    script = JS.read_text(encoding='utf-8')
    style = CSS.read_text(encoding='utf-8')
    cases = 0
    for mode, chapter in TOPICS.items():
        for lang in ('en', 'zh'):
            path = DOCS / chapter / ('index.md' if lang == 'en' else 'index.zh-TW.md')
            markdown = path.read_text(encoding='utf-8')
            assert f'data-lab="{mode}" data-lang="{lang}"' in markdown, path
            for width in (320, 360, 720, 1024):
                for reduced in (False, True):
                    context = browser.new_context(viewport={'width': width, 'height': 750},
                        reduced_motion='reduce' if reduced else 'no-preference')
                    page = context.new_page()
                    page.set_content('<!doctype html><html><head><meta charset="utf-8"><style>'
                        + style + '</style></head><body style="margin:0;padding:8px">'
                        + f'<div class="pc-lab" data-lab="{mode}" data-lang="{lang}"></div>'
                        + '</body></html>')
                    page.add_script_tag(content=script)
                    lab = page.locator('.pc-lab')
                    assert lab.locator('.pc-plot circle').count() == 9
                    assert lab.locator('[data-seek]').input_value() == '0'
                    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), (mode, lang, width)
                    scroll = lab.locator('.pc-scroll').evaluate('x => [x.clientWidth, x.scrollWidth]')
                    if width <= 360:
                        assert scroll[1] > scroll[0], (width, scroll)
                    lab.locator('[data-action="next"]').click()
                    assert lab.locator('[data-seek]').input_value() == '1'
                    content = lab.locator('.pc-readout').inner_text()
                    assert ('0.580' in content) if mode == 'residual' else ('0.350' in content), content
                    lab.locator('[data-seek]').fill('8')
                    assert lab.locator('[data-seek]').input_value() == '8'
                    lab.locator('[data-action="prev"]').click()
                    assert lab.locator('[data-seek]').input_value() == '7'
                    lab.locator('[data-speed]').select_option('2')
                    lab.locator('[data-action="reset"]').click()
                    assert lab.locator('[data-seek]').input_value() == '0'
                    assert lab.locator('[data-speed]').input_value() == '1'
                    assert lab.locator('[data-action="toggle"]').inner_text() in ('Play', '播放')
                    lab.locator('[data-action="toggle"]').click()
                    assert lab.locator('[data-action="toggle"]').inner_text() in ('Pause', '暫停')
                    lab.locator('[data-action="toggle"]').click()
                    assert lab.locator('[data-action="toggle"]').inner_text() in ('Play', '播放')
                    if mode == 'residual':
                        lab.locator('[data-param="x"]').fill('0.95')
                        lab.locator('[data-param="eta"]').fill('1.25')
                        lab.locator('[data-seek]').fill('1')
                        assert '1.125' in lab.locator('.pc-readout').inner_text()
                    else:
                        lab.locator('[data-param="a"]').fill('0.1')
                        lab.locator('[data-param="b"]').fill('0.9')
                        lab.locator('[data-seek]').fill('1')
                        assert '0.300' in lab.locator('.pc-readout').inner_text()
                    if width in (320, 1024) and not reduced:
                        page.screenshot(path=str(OUT / f'{mode}-{lang}-{width}.png'), full_page=True)
                    bounds = lab.locator('.pc-plot text').evaluate_all(
                        """es => es.map(e=>{let b=e.getBBox();return [b.x,b.y,b.width,b.height]})""")
                    assert all(x >= -1 and y >= -1 and x + w <= 661 and y + h <= 253
                               for x,y,w,h in bounds), (mode, lang, width, bounds)
                    cases += 1
                    context.close()
    browser.close()
    print(f'Predictive-coding labs: {cases} Chromium locale/viewport/motion checks passed')

if __name__ == '__main__':
    with sync_playwright() as pw:
        render(pw)
