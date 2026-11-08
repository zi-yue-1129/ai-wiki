#!/usr/bin/env python3
"""Browser QA for the paired RND/ICM instructional SVGs and shared player.

Render actual intermediate states at mobile/desktop widths, assert error reduction,
verify reduced-motion screenshots remain pixel-stable, and exercise both button
and keyboard controls on the MkDocs enhancement (when JS is present).
"""
from __future__ import annotations

import hashlib
import os
from pathlib import Path
import tempfile
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
ASSETS = Path(os.environ.get('RND_ICM_ASSETS', ROOT / 'docs/assets/concept-animations'))
PLAYER = ROOT / 'docs/javascripts/concept-motion.js'
STEMS = ('rnd-prediction-error', 'icm-forward-inverse')


def frame(page, time: float) -> bytes:
    page.evaluate('(t) => document.querySelector("svg").setCurrentTime(t)', time)
    page.wait_for_timeout(30)
    return page.locator('svg').screenshot(animations='allow')


def run() -> None:
    with sync_playwright() as runtime:
        browser = runtime.chromium.launch(headless=True, executable_path=("/usr/bin/chromium" if Path("/usr/bin/chromium").exists() else None), args=["--no-sandbox"])
        try:
            for stem in STEMS:
                motion = ASSETS / f'{stem}-motion.svg'
                still = ASSETS / f'{stem}-still.svg'
                assert motion.is_file() and still.is_file(), f'missing SVG pair: {stem}'
                source = motion.read_text(encoding='utf-8')
                assert '<animate ' in source and '<animate ' not in still.read_text(), stem

                for width in (360, 720, 1024):
                    html = ('<html><head><meta charset="utf-8"><style>'
                            f'body{{margin:0;padding:14px}}svg{{width:{width}px;height:auto;display:block}}'
                            '</style></head><body>' + source + '</body></html>')
                    ctx = browser.new_context(viewport={'width': width + 32, 'height': 640})
                    page = ctx.new_page()
                    page.set_content(html)
                    x0 = page.evaluate('document.querySelector(".animated circle").cx.animVal.value')
                    first = frame(page, 0.0)
                    middle = frame(page, 3.5)
                    end = frame(page, 6.0)
                    x1 = page.evaluate('document.querySelector(".animated circle").cx.animVal.value')
                    assert x1 > x0 + 15, f'{stem} at {width}: predictor did not approach target'
                    assert len({hashlib.sha256(b).hexdigest() for b in (first, middle, end)}) == 3, (
                        f'{stem} at {width}: intermediate motion missing'
                    )
                    assert page.locator('svg').bounding_box()['width'] <= width + 1
                    ctx.close()

                    ctx = browser.new_context(viewport={'width': width + 32, 'height': 640}, reduced_motion='reduce')
                    page = ctx.new_page()
                    page.set_content(html)
                    stills = [hashlib.sha256(frame(page, t)).hexdigest() for t in (0.0, 3.5, 6.0)]
                    assert len(set(stills)) == 1, f'{stem} at {width}: reduced-motion pixels changed'
                    ctx.close()
                print(f'PASS {stem}: three widths, three animation times, reduced-motion stable')

            # This is the repository's real shared MkDocs enhancement, not a mock.
            if PLAYER.is_file():
                with tempfile.TemporaryDirectory() as tmp:
                    fixture = Path(tmp) / 'test.html'
                    for stem in STEMS:
                        motion_uri = (ASSETS / f'{stem}-motion.svg').resolve().as_uri()
                        fixture.write_text('<html><body><img alt="RND concept animation" '
                                           f'src="{motion_uri}"></body></html>', encoding='utf-8')
                        ctx = browser.new_context()
                        page = ctx.new_page()
                        page.goto(fixture.as_uri())
                        page.add_script_tag(content=PLAYER.read_text(encoding='utf-8'))
                        toggle = page.get_by_role('button', name='Pause concept animation')
                        assert toggle.count() == 1, f'{stem}: player controls did not load'
                        toggle.click()
                        assert page.locator('img').get_attribute('src').endswith('-still.svg'), stem
                        page.get_by_role('button', name='Play concept animation').focus()
                        page.keyboard.press('Enter')
                        assert page.locator('img').get_attribute('src').endswith('-motion.svg'), stem
                        ctx.close()
                        ctx = browser.new_context(reduced_motion='reduce')
                        page = ctx.new_page()
                        page.goto(fixture.as_uri())
                        page.add_script_tag(content=PLAYER.read_text(encoding='utf-8'))
                        assert page.locator('img').get_attribute('src').endswith('-still.svg'), stem
                        assert page.get_by_role('button', name='Play concept animation').count() == 1
                        ctx.close()
                        print(f'PASS {stem}: MkDocs playback, keyboard, reduced-motion fallback')
            else:
                print('SKIP MkDocs enhancement controls: concept-motion.js not present in local asset-only QA')
        finally:
            browser.close()


if __name__ == '__main__':
    run()
