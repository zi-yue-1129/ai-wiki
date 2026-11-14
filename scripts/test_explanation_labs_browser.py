#!/usr/bin/env python3
"""Chromium visual and numerical regression for the deterministic LIME/SHAP labs."""
from __future__ import annotations
from pathlib import Path
import shutil
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
JS = ROOT / 'docs/javascripts/explanation-labs.js'
CSS = ROOT / 'docs/stylesheets/explanation-labs.css'
PAGES = ROOT / 'docs/society/interpretability'
ART = ROOT / 'artifacts/explanation-labs'


def run() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    for topic in ('lime', 'shap'):
        for suffix in ('.md', '.zh-TW.md'):
            page = (PAGES / (topic + suffix)).read_text(encoding='utf-8')
            assert f'data-explanation-lab="{topic}"' in page
            assert ('data-locale="zh"' if suffix == '.zh-TW.md' else 'data-locale="en"') in page
            assert '-still.svg' in page and '-motion.svg' in page
    checks = 0
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True, **({'executable_path': shutil.which('chromium')} if shutil.which('chromium') else {}))
        for width in (320, 360, 720, 1024):
            for lang in ('en', 'zh'):
                for reduced in (False, True):
                    page = browser.new_page(viewport={'width': width, 'height': 780}, reduced_motion='reduce' if reduced else 'no-preference')
                    page.set_content(f'<meta charset="utf-8"><main style="max-width:960px;margin:auto"><div data-explanation-lab="lime" data-locale="{lang}"></div><div data-explanation-lab="shap" data-locale="{lang}"></div></main>')
                    page.add_style_tag(content=CSS.read_text())
                    page.add_script_tag(content=JS.read_text())
                    labs = page.locator('.explanation-lab')
                    assert labs.count() == 2
                    lime, shap = labs.nth(0), labs.nth(1)
                    assert lime.locator('svg circle').count() == 13
                    assert shap.locator('svg rect').count() >= 10
                    assert '0.240' in shap.locator('.explanation-lab-stats').inner_text()
                    assert '0.15' in lime.locator('output').inner_text()
                    initial = lime.locator('.explanation-lab-stats').inner_text()
                    lime.locator('input[type=range]').fill('0.32')
                    assert lime.locator('.explanation-lab-stats').inner_text() != initial
                    assert lime.locator('output').inner_text() == '0.32'
                    shap.locator('button').nth(1).click()
                    assert '1 / 4' in shap.locator('output').inner_text()
                    shap.locator('input[type=range]').fill('4')
                    assert '0.240 / 0.240' in shap.locator('svg').text_content()
                    shap.locator('select').select_option('B')
                    assert '0.225' in shap.locator('.explanation-lab-stats').inner_text()
                    shap.locator('input[type=range]').fill('4')
                    assert '0.225 / 0.225' in shap.locator('svg').text_content()
                    shap.locator('select').select_option('C')
                    assert '0.085' in shap.locator('.explanation-lab-stats').inner_text()
                    shap.locator('input[type=range]').fill('4')
                    assert '0.085 / 0.085' in shap.locator('svg').text_content()
                    if reduced:
                        shap.locator('button').nth(2).click()
                        assert shap.locator('button').nth(2).inner_text() in ('Play', '播放')
                    else:
                        shap.locator('button').nth(2).click()
                        assert shap.locator('button').nth(2).inner_text() in ('Pause', '暫停')
                        shap.locator('button').nth(2).click()
                        assert shap.locator('button').nth(2).inner_text() in ('Play', '播放')
                    if width < 640:
                        viewport = lime.locator('.explanation-lab-scroll')
                        assert viewport.evaluate('(x)=>x.scrollWidth>x.clientWidth')
                        viewport.focus()
                        page.keyboard.press('ArrowRight')
                        page.wait_for_timeout(100)
                        assert viewport.evaluate('(x)=>x.scrollLeft>0')
                    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth+1')
                    if width in (320, 1024) and lang == 'en' and not reduced:
                        shap.locator('select').select_option('A')
                        page.screenshot(path=str(ART / f'lab-{width}-{lang}.png'), full_page=True)
                    checks += 1
                    page.close()
        browser.close()
    print(f'Passed {checks} bilingual viewport/reduced-motion/keyboard/numerical lab cases')


if __name__ == '__main__':
    run()