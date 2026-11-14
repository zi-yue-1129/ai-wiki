"""Chromium exercise for LayerNorm and fixed-context Seq2Seq teaching labs.

This fixture uses the actual source files under docs, tests both languages at
mobile and desktop sizes, and records screenshots for human visual QA.
"""
from __future__ import annotations
import re
import shutil
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
JS = ROOT / 'docs/javascripts/norm-seq-labs.js'
CSS = ROOT / 'docs/stylesheets/norm-seq-labs.css'
ARTIFACTS = ROOT / 'artifacts/norm-seq-labs'


def run() -> None:
    assert JS.exists() and CSS.exists()
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    js, css = JS.read_text(encoding='utf-8'), CSS.read_text(encoding='utf-8')
    assert 'script src=' not in js and 'http://' not in css
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, executable_path=shutil.which('chromium') or None)
        count = 0
        for lang in ('en', 'zh'):
            for width in (320, 360, 720, 1024):
                for reduced in (False, True):
                    page = browser.new_page(viewport={'width': width, 'height': 920}, reduced_motion='reduce' if reduced else 'no-preference')
                    page.set_content('<!doctype html><html><head><meta charset="utf-8"></head><body style="margin:0;padding:12px;max-width:100%;overflow-x:hidden;box-sizing:border-box">'
                        f'<div data-norm-seq-lab="layernorm" data-lang="{lang}">Static fallback retained.</div>'
                        f'<div data-norm-seq-lab="seq2seq" data-lang="{lang}">Static fallback retained.</div></body></html>')
                    page.add_style_tag(content=css)
                    page.add_script_tag(content=js)
                    page.locator('.ns-lab').first.wait_for()
                    assert page.locator('.ns-lab').count() == 2
                    assert page.locator('.ns-svg').count() == 2
                    # Set shared offset and perturbation; invariance and sensitivity are computed in actual JS.
                    n = page.locator('[data-norm-seq-lab="layernorm"]')
                    offset = n.locator('input[type=range]').nth(0)
                    spike = n.locator('input[type=range]').nth(1)
                    offset.fill('4')
                    assert '0.00' in n.locator('.ns-metric').nth(2).inner_text()
                    spike.fill('3')
                    assert '0.00' not in n.locator('.ns-metric').nth(2).inner_text()
                    spike.fill('0')
                    seq = page.locator('[data-norm-seq-lab="seq2seq"]')
                    seq.locator('input[type=range]').first.fill('4')
                    context_before = seq.locator('.ns-metric').nth(1).inner_text()
                    seq.locator('select').first.select_option('forward')
                    seq.locator('input[type=range]').first.fill('4')
                    assert seq.locator('.ns-metric').nth(1).inner_text() != context_before
                    seq.locator('select').first.select_option('reverse')
                    seq.locator('.ns-button-row button').nth(2).click()
                    assert '1 / 7' in seq.locator('.ns-metric').first.inner_text()
                    seq.locator('input[type=range]').first.fill('7')
                    assert '7 / 7' in seq.locator('.ns-metric').first.inner_text()
                    seq.locator('.ns-button-row button').nth(3).click()
                    assert '0 / 7' in seq.locator('.ns-metric').first.inner_text()
                    assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth + 1')
                    assert page.locator('.ns-svg').count() == 2
                    if width <= 360:
                        scroller=page.locator('.ns-graph-scroll').first
                        assert scroller.evaluate('(el) => el.scrollWidth > el.clientWidth')
                        scroller.focus()
                        page.keyboard.press('End')
                    if reduced:
                        seq.locator('.ns-button-row button').nth(1).click()
                        assert seq.locator('.ns-button-row button').nth(1).inner_text() in ('Play','播放')
                    if not reduced:
                        seq.locator('.ns-button-row button').nth(1).click()
                        assert seq.locator('.ns-button-row button').nth(1).inner_text() in ('Pause','暫停')
                        seq.locator('.ns-button-row button').nth(1).click()
                    if not reduced:
                        page.screenshot(path=str(ARTIFACTS / f'{lang}-{width}.png'), full_page=True)
                    count += 1
                    page.close()
        browser.close()
        print(f'LayerNorm / Seq2Seq Chromium scenarios passed: {count}/{count}; screenshots: {ARTIFACTS}')


if __name__ == '__main__':
    run()