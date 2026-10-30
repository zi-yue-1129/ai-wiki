#!/usr/bin/env python3
"""Chromium integration checks for same-origin SMIL controls on six real diagrams."""
from __future__ import annotations

import os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
OUT = ROOT / 'distributed-motion-screenshots'
STEMS = ('gpipe-fill-drain', 'gpipe-gradient-accumulation', 'fsdp-gather-scatter',
         'fsdp-parameter-residency', 'zero-state-sharding', 'megatron-column-row')


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DOCS), **kwargs)

    def log_message(self, *_):
        pass


def main():
    OUT.mkdir(exist_ok=True)
    server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
    Thread(target=server.serve_forever, daemon=True).start()
    try:
        with sync_playwright() as pw:
            launch = {'headless': True, 'args': ['--no-sandbox']}
            if os.environ.get('CHROMIUM_EXECUTABLE'):
                launch['executable_path'] = os.environ['CHROMIUM_EXECUTABLE']
            browser = pw.chromium.launch(**launch)
            for stem in STEMS:
                for width in (360, 900):
                    for reduce in (False, True):
                        zh = width == 360
                        alt = '分散式訓練計算流程示意動畫' if zh else 'Distributed training computation animation'
                        ctx = browser.new_context(viewport={'width': width, 'height': 720},
                                                  reduced_motion='reduce' if reduce else 'no-preference')
                        page = ctx.new_page()
                        # Keep the document on the same origin as the SVG object.
                        page.goto(f'http://127.0.0.1:{server.server_port}/stylesheets/concept-motion.css')
                        page.set_content(f'''<!doctype html><html><head><meta name="viewport" content="width=device-width,initial-scale=1">
                            <style>body{{margin:12px}} .concept-motion-player{{display:block;max-width:640px}}
                            .concept-motion-player img{{display:block;width:100%}}</style></head><body>
                            <img alt="{alt}" src="/assets/concept-animations/{stem}-motion.svg"></body></html>''')
                        for sheet in ('concept-motion.css', 'distributed-motion-controls.css', 'extra.css'):
                            page.add_style_tag(content=(DOCS / 'stylesheets' / sheet).read_text())
                        for script in ('concept-motion.js', 'distributed-motion-controls.js'):
                            page.add_script_tag(content=(DOCS / 'javascripts' / script).read_text())
                        host = page.locator('.concept-motion-player')
                        assert host.count() == 1, stem
                        if reduce:
                            assert '-still.svg' in host.locator('img').first.get_attribute('src')
                            assert host.locator('.distributed-motion-controls').count() == 0
                            assert host.locator('img').first.is_visible()
                        else:
                            page.wait_for_function('''() => {
                                const b=document.querySelector('.distributed-motion-controls');
                                return b && !b.hidden;
                            }''', timeout=12000)
                            obj = host.locator('object')
                            assert obj.is_visible() and not host.locator('img').first.is_visible()
                            next_button = host.get_by_role('button', name='下一步' if zh else 'Step →')
                            next_button.focus()
                            page.keyboard.press('Space')
                            readout = host.locator('output')
                            assert float(readout.inner_text().split(' / ')[0]) > 0
                            slider = host.locator('input[type=range]')
                            slider.evaluate("e => {e.value='500';e.dispatchEvent(new Event('input',{bubbles:true}))}")
                            seconds = float(readout.inner_text().split(' / ')[0])
                            assert 0 < seconds < 8, (stem, seconds)
                            host.locator('select').select_option('2')
                            host.get_by_role('button', name='播放動畫' if zh else 'Play animation').click()
                            page.wait_for_timeout(280)
                            assert float(readout.inner_text().split(' / ')[0]) > seconds + .15
                            host.get_by_role('button', name='暫停動畫' if zh else 'Pause animation').click()
                            assert page.evaluate('''() => {
                                const svg=document.querySelector('object').contentDocument.documentElement;
                                return svg.animationsPaused();
                            }''')
                            assert page.evaluate('''() => {
                                const h=document.querySelector('.distributed-motion-controls').getBoundingClientRect();
                                const s=document.querySelector('.distributed-motion-seek').getBoundingClientRect();
                                return h.left>=0 && s.left>=0 && s.right<=innerWidth+1;
                            }'''), stem
                        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'), (stem, width)
                        page.screenshot(path=str(OUT / f'{stem}-controls-{width}-reduced-{reduce}.png'))
                        ctx.close()
                print(f'{stem}: timeline, keyboard, speed, reduced-motion fallback and responsive controls passed')
            browser.close()
    finally:
        server.shutdown()


if __name__ == '__main__':
    main()
