#!/usr/bin/env python3
"""Real Chromium interaction and visual regressions for GPipe and ZeRO explorers."""
from __future__ import annotations
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'distributed-explorer-screenshots'


def main():
    OUT.mkdir(exist_ok=True)
    js = (ROOT / 'docs/javascripts/distributed-parameter-explorers.js').read_text()
    css = (ROOT / 'docs/stylesheets/distributed-parameter-explorers.css').read_text()
    with sync_playwright() as pw:
        launch = {'headless': True, 'args': ['--no-sandbox']}
        if os.environ.get('CHROMIUM_EXECUTABLE'):
            launch['executable_path'] = os.environ['CHROMIUM_EXECUTABLE']
        browser = pw.chromium.launch(**launch)
        for name in ('gpipe', 'zero'):
            for lang in ('en', 'zh'):
                for width in (360, 900):
                    for reduce in (False, True):
                        ctx = browser.new_context(viewport={'width': width, 'height': 800},
                                                  reduced_motion='reduce' if reduce else 'no-preference')
                        page = ctx.new_page()
                        page.set_content(f'''<!doctype html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"></head><body style="margin:12px;max-width:900px">
                          <p><img src="/assets/concept-animations/{name}-still.svg" alt="Static fallback"></p><div class="distributed-explorer" data-explorer="{name}" data-lang="{lang}"></div></body></html>''')
                        page.add_style_tag(content=css)
                        page.add_script_tag(content=js)
                        host = page.locator('.distributed-explorer')
                        assert host.get_attribute('data-ready') == 'yes'
                        assert page.locator('p:has(img[alt="Static fallback"])').is_hidden()
                        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth+1'), (name, lang, width, reduce)
                        if name == 'gpipe':
                            assert host.locator('.dex-cell').count() == 3 * 12
                            assert '33.3%' in host.locator('.dex-stats').inner_text()
                            next_button = host.get_by_role('button', name='下一步' if lang == 'zh' else 'Next step')
                            next_button.focus()
                            page.keyboard.press('Space')
                            assert '1 / 12' in host.locator('.dex-time').inner_text()
                            host.get_by_role('slider', name='微批次' if lang == 'zh' else 'Micro-batches').fill('8')
                            assert '20.0%' in host.locator('.dex-stats').inner_text()
                            assert host.locator('.dex-cell').count() == 3 * 20
                            assert '0 / 20' in host.locator('.dex-time').inner_text()
                        else:
                            assert '16.00 B' in host.locator('.dex-stats').inner_text()
                            host.get_by_role('slider', name='ZeRO 階段' if lang == 'zh' else 'ZeRO stage').fill('3')
                            assert '8.00 B' in host.locator('.dex-stats').inner_text()
                            host.get_by_role('slider', name='裝置數' if lang == 'zh' else 'Ranks').fill('8')
                            assert '2.00 B' in host.locator('.dex-stats').inner_text()
                            assert '87.5%' in host.locator('.dex-stats').inner_text()
                            host.get_by_role('button', name='上一步' if lang == 'zh' else 'Previous step').click()
                            assert '3.75 B' in host.locator('.dex-stats').inner_text()
                        play = host.get_by_role('button', name='播放' if lang == 'zh' else 'Play')
                        if reduce:
                            assert play.is_disabled(), (name, lang, width)
                        else:
                            assert play.is_enabled()
                            play.click()
                            page.wait_for_timeout(300 if name == "zero" else 1200)
                            assert host.get_by_role('button', name='暫停' if lang == 'zh' else 'Pause').count() == 1
                            host.get_by_role('button', name='暫停' if lang == 'zh' else 'Pause').click()
                        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth+1'), (name, lang, width, reduce)
                        page.screenshot(path=str(OUT / f'{name}-{lang}-{width}-reduced-{reduce}.png'), full_page=True)
                        ctx.close()
        browser.close()
    print('GPipe/ZeRO: 16 Chromium combinations, formula, keyboard, motion, reduced-motion, overflow passed')

if __name__ == '__main__':
    main()
