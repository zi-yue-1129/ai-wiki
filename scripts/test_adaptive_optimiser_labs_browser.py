#!/usr/bin/env python3
"""Run deterministic interactive AdaGrad/Adafactor labs in real Chromium.

Checks bilingual mobile layout, keyboard + native range controls, arithmetic,
non-autoplay reduced-motion behaviour, and visibility of intermediate states.
"""
from __future__ import annotations
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
JS = (ROOT / 'docs/javascripts/adaptive-optimiser-labs.js')
CSS = (ROOT / 'docs/stylesheets/adaptive-optimiser-labs.css')
# In local QA, files are beside this script; CI uses repository paths.
if not JS.exists(): JS = Path(__file__).with_name('adaptive-optimiser-labs.js')
if not CSS.exists(): CSS = Path(__file__).with_name('adaptive-optimiser-labs.css')
OUT = ROOT / 'artifacts' / 'adaptive-optimiser-labs'
OUT.mkdir(parents=True, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True,
       executable_path=os.environ.get('CHROMIUM_EXECUTABLE') or None,
       args=['--no-sandbox'])
    cases = 0
    for mode in ('adagrad', 'adafactor'):
        for lang in ('en','zh'):
            for width in (320, 720):
                for reduced in (False,True):
                    print('CASE', mode, lang, width, reduced, flush=True)
                    page = browser.new_page(viewport={'width':width,'height':760},
                            reduced_motion='reduce' if reduced else 'no-preference')
                    errors = []
                    page.on('pageerror', lambda err: errors.append(str(err)))
                    page.set_content('<!doctype html><meta name="viewport" content="width=device-width,initial-scale=1">'
                                     f'<main style="padding:10px"><div data-adaptive-lab="{mode}" data-lang="{lang}"></div></main>')
                    page.add_style_tag(path=str(CSS))
                    page.evaluate('window.document$={subscribe(fn){window.navigateAdaptive=fn;fn();}}')
                    page.add_script_tag(path=str(JS))
                    assert page.locator('.adaptive-lab-title').count() == 1
                    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), (mode,lang,width,'overflow')
                    assert page.locator('[role=status]').count()==1
                    assert not errors, (mode,lang,width,errors)
                    assert page.locator('.adaptive-lab-button[aria-pressed=false]').count()==1
                    slider=page.locator('.adaptive-lab-range')
                    def set_range(val):
                        slider.evaluate('(el,v) => { el.value=String(v);el.dispatchEvent(new Event("input",{bubbles:true})); }',val)
                    assert slider.get_attribute('aria-valuetext')
                    if mode=='adagrad':
                        set_range(5)
                        body=page.locator('.adaptive-lab-readout').inner_text()
                        assert '0.447' in body and '0.707' in body, body
                        set_range(2)
                        assert '|Δθ| = 0.000' in page.locator('.adaptive-lab-stats').inner_text()
                        set_range(1)
                        assert '|Δθ| = 1.000' in page.locator('.adaptive-lab-stats').inner_text()
                    else:
                        assert '2.800' in page.locator('.adaptive-lab-answer').inner_text()
                        assert '0.800' in page.locator('.adaptive-lab-note').inner_text()
                        set_range(0)
                        assert '0.800' in page.locator('.adaptive-lab-answer').inner_text()
                        assert page.locator('.adaptive-lab-cell.adaptive-lab-selected').inner_text()=='1'
                        set_range(6)
                        assert page.locator('.adaptive-lab-selected').count()==1
                    # Verify every mathematical state, not just one selected value.
                    if mode=='adagrad':
                        for step in range(1,7):
                            set_range(step)
                            cards=page.locator('.adaptive-lab-values').all_inner_texts()
                            for k,history in enumerate(([1]*6,[1,0,0,0,1,0])):
                                G=sum(g*g for g in history[:step]);gain=G**-.5
                                assert f'{gain:.3f}' in cards[k]
                                assert f'|Δθ| = {abs(history[step-1])*gain:.3f}' in cards[k]
                        set_range(2)
                    else:
                        data=[[1,2,1,0],[3,1,2,2],[0,2,4,2]]
                        for cell in range(12):
                            set_range(cell);i,j=divmod(cell,4)
                            estimate=sum(data[i])*sum(row[j] for row in data)/20
                            assert f'{estimate:.3f}' in page.locator('.adaptive-lab-answer').inner_text()
                            assert page.locator('.adaptive-lab-selected').inner_text()==str(data[i][j])
                        set_range(6)
                    # The range and buttons must be reachable and respond to native keyboard keys.
                    slider.focus()
                    before=slider.input_value()
                    page.keyboard.press('ArrowRight')
                    assert slider.input_value()!=before, (mode,lang,'keyboard slider')
                    page.locator('[data-action="previous"]').focus()
                    before=slider.input_value()
                    page.keyboard.press('Enter')
                    assert int(slider.input_value()) == int(before)-1
                    page.locator('[data-action="next"]').click()
                    assert slider.input_value() == str(int(before))
                    page.locator('[data-action="toggle"]').click()
                    assert page.locator('[data-action="toggle"]').get_attribute('aria-pressed')=='true'
                    old=slider.input_value()
                    page.wait_for_timeout(520)
                    page.locator('.adaptive-lab-speed').select_option('2')
                    page.wait_for_timeout(530)
                    assert slider.input_value()!=old, (mode,lang,width,'playback not progressing')
                    page.locator('[data-action="toggle"]').click()
                    assert page.locator('[data-action="toggle"]').get_attribute('aria-pressed')=='false'
                    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
                    assert not errors
                    if width in (320,720) and not reduced:
                        page.screenshot(path=str(OUT / f'{mode}-{lang}-{width}.png'),full_page=True)
                    page.evaluate('navigateAdaptive();navigateAdaptive()')
                    assert page.locator('.adaptive-lab-title').count()==1
                    page.locator('[data-action="toggle"]').click()
                    assert page.locator('[role=status]').get_attribute('aria-live')=='off'
                    page.evaluate('window.oldAdaptive=document.querySelector("main");oldAdaptive.remove();navigateAdaptive()')
                    assert page.evaluate('oldAdaptive.querySelectorAll(".adaptive-lab-title").length')==0
                    page.evaluate('document.body.prepend(oldAdaptive);navigateAdaptive();navigateAdaptive()')
                    assert page.locator('.adaptive-lab-title').count()==1
                    assert page.locator('[data-action="toggle"]').get_attribute('aria-pressed')=='false'
                    page.close()
                    cases+=1
    if os.environ.get('ADAPTIVE_SITE_DIR'):
        from test_built_motion_browser import serve_site, check_math_rendering, assert_document_fits
        with serve_site(Path(os.environ['ADAPTIVE_SITE_DIR']).resolve(),'https://zi-yue-1129.github.io/ai-wiki/') as base:
            for mode in ('adagrad','adafactor'):
                for locale in ('','zh-TW/'):
                    for width in (390,1280):
                        page=browser.new_page(viewport={'width':width,'height':900},reduced_motion='reduce')
                        page.goto(base+locale+'theory/optimization/adaptive/'+mode+'/',wait_until='networkidle')
                        page.wait_for_selector('.adaptive-lab-title')
                        check_math_rendering(page);assert_document_fits(page,{'width':width})
                        page.locator('.adaptive-lab-range').fill('5' if mode=='adagrad' else '6')
                        assert ('0.707' if mode=='adagrad' else '2.800') in page.locator('.adaptive-lab-readout').inner_text()
                        page.locator('.adaptive-lab').scroll_into_view_if_needed()
                        page.screenshot(path=str(OUT/f'built-{mode}-{locale.replace("/","") or "en"}-{width}.png'))
                        page.close()
    browser.close()
print(f'Adaptive optimiser labs Chromium regression: {cases}/{cases} cases passed')