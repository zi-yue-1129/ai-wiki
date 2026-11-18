#!/usr/bin/env python3
"""Exercise mathematical values, keyboard, reduced-motion, and actual viewport rendering.
Run from repository root with playwright installed, including bundled Chromium.
"""
from pathlib import Path
import os,re
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
JS = ROOT / "docs/javascripts/sac-dpo-labs.js"
CSS = ROOT / "docs/stylesheets/sac-dpo-labs.css"
OUT = ROOT / "artifacts/sac-dpo-labs"


def html(lang):
    return f'''<!doctype html><html lang="{lang}"><meta charset="utf-8"><style>
    body{{margin:0;padding:12px;font:16px system-ui}}main{{max-width:800px;margin:auto}}
    </style><main><section data-sac-dpo-lab="sac" data-lang="{lang}">
    <p>Read the SVG preview above if the interactive lab is unavailable.</p></section>
    <section data-sac-dpo-lab="dpo" data-lang="{lang}"><p>Static SVG remains available.</p></section></main></html>'''


def close(actual, expected, tol=0.002):
    assert abs(float(actual) - expected) < tol, (actual, expected)


def assert_visible_loss_axis(svg):
    # SVGElement has textContent, not HTMLElement.innerText (Playwright 1.55).
    assert '8.0' in (svg.text_content() or '')
    label=svg.locator('text').filter(has_text=re.compile(r'^8\.0$'))
    assert label.count()==1 and label.is_visible(), 'Expected visible expanded loss-axis maximum'


def run():
    assert JS.exists() and CSS.exists()
    OUT.mkdir(parents=True, exist_ok=True)
    count=0
    with sync_playwright() as playwright:
        binary = '/usr/bin/chromium' if Path('/usr/bin/chromium').exists() else None
        browser=playwright.chromium.launch(headless=True, executable_path=binary, args=['--no-sandbox'])
        for lang in ('en','zh-TW'):
            for width in (320,360,720,1024):
                for reduced in (False,True):
                    page=browser.new_page(viewport={'width':width,'height':850}, reduced_motion='reduce' if reduced else 'no-preference')
                    errors=[]
                    page.on('pageerror', lambda e: errors.append(str(e)))
                    page.set_content(html(lang), wait_until='load')
                    # The page must retain static fallback text when JS is disabled.
                    assert page.get_by_text('Static SVG remains available.').count()==1
                    page.add_style_tag(content=CSS.read_text())
                    page.evaluate("""() => {window.__active=new Set();const set=window.setInterval.bind(window),clear=window.clearInterval.bind(window);window.setInterval=(fn,ms)=>{const id=set(fn,ms);__active.add(id);return id;};window.clearInterval=id=>{__active.delete(id);clear(id);};window.document$={subscribe:fn=>window.__navigation=fn};const other=document.createElement('div');other.dataset.sacDpoLab='unrelated';other.textContent='untouched';document.body.append(other);}""")
                    page.add_script_tag(content=JS.read_text())
                    assert page.locator("[data-sac-dpo-ready='1']").count()==2
                    assert page.locator('.sd-scroll svg').count()==2
                    for kind in ('sac','dpo'):
                        lab=page.locator(f'[data-sac-dpo-lab="{kind}"]')
                        assert lab.locator('[data-act="previous"]').count()==1
                        assert lab.locator('[data-act="next"]').count()==1
                        assert lab.locator('[data-act="play"]').is_disabled() == reduced
                        assert lab.locator('.sd-scroll').evaluate('(e)=>e.scrollWidth>e.clientWidth') == (width < 760)
                        assert lab.locator('.sd-scroll').evaluate('(e)=>e.scrollWidth>=720')
                    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), width
                    sac=page.locator('[data-sac-dpo-lab="sac"]')
                    dpo=page.locator('[data-sac-dpo-lab="dpo"]')
                    # Q=[2,1,0], alpha=2: analytic entropy and expected Q.
                    close(sac.locator('[data-value="entropy"]').inner_text(),1.020,0.002)
                    sac.locator('[data-param="alpha"]').fill('0.5')
                    close(sac.locator('[data-value="entropy"]').inner_text(),0.441,0.003)
                    sac.locator('[data-act="reset"]').click()
                    close(sac.locator('[data-value="entropy"]').inner_text(),1.020,0.002)
                    # Default ref=p=.5 => margin 0, loss ln2.
                    close(dpo.locator('[data-value="margin"]').inner_text(),0)
                    close(dpo.locator('[data-value="loss"]').inner_text(),0.693,0.002)
                    dpo.locator('[data-param="reference"]').fill('0.8')
                    assert float(dpo.locator('[data-value="margin"]').inner_text()) < 0
                    assert float(dpo.locator('[data-value="loss"]').inner_text()) > 0.693
                    dpo.locator('[data-param="pref"]').fill('0.8')
                    close(dpo.locator('[data-value="margin"]').inner_text(),0)
                    dpo.locator('[data-act="reset"]').click()
                    # Keyboard-native step and seek.
                    pos_before=int(dpo.locator('[data-act="seek"]').input_value())
                    dpo.locator('[data-act="next"]').focus();dpo.locator('[data-act="next"]').press('Enter')
                    assert int(dpo.locator('[data-act="seek"]').input_value())==pos_before+1
                    dpo.locator('[data-act="seek"]').fill('0')
                    assert abs(float(dpo.locator('[data-value="margin"]').inner_text()) - (-2.197)) < .005
                    dpo.locator('[data-act="reset"]').click()
                    if not reduced:
                        # Replay from a near-end frame, assert timer updates and pause freezes.
                        dpo.locator('[data-act="seek"]').fill('16')
                        dpo.locator('[data-act="speed"]').select_option('2')
                        dpo.locator('[data-act="play"]').click()
                        page.wait_for_timeout(400)
                        assert int(dpo.locator('[data-act="seek"]').input_value())>=17
                        dpo.locator('[data-act="play"]').click()
                        paused=dpo.locator('[data-act="seek"]').input_value()
                        page.wait_for_timeout(430)
                        assert dpo.locator('[data-act="seek"]').input_value()==paused
                        dpo.locator('[data-act="reset"]').click()
                    for idx in (0,1,7,50,139,140):
                        sac.locator('[data-act="seek"]').fill(str(idx))
                        close(sac.locator('[data-param="alpha"]').input_value(),3-idx*.02,1e-8)
                    sac.locator('[data-param="alpha"]').fill('0.5')
                    close(sac.locator('[data-act="seek"]').input_value(),125,1e-8)
                    dpo.locator('[data-param="pref"]').fill('0.1');dpo.locator('[data-param="reference"]').fill('0.8');dpo.locator('[data-param="beta"]').fill('2')
                    assert float(dpo.locator('[data-value="loss"]').inner_text())>7
                    dot=dpo.locator('.sd-dot');assert float(dot.get_attribute('cy'))>58
                    assert_visible_loss_axis(dpo.locator('svg'))
                    for lab in (sac,dpo):
                        if width<760:
                            sc=lab.locator('.sd-scroll');sc.focus();page.keyboard.press('ArrowRight');page.wait_for_timeout(80);assert sc.evaluate('e=>e.scrollLeft>0')
                        lab.locator('[data-act="reset"]').click()
                        assert lab.locator('[data-act="speed"]').input_value()=='1'
                    if not reduced and width in (320,1024):page.screenshot(path=str(OUT/f'{lang}-{width}-final.png'),full_page=True)
                    page.evaluate('window.__navigation()');assert page.locator('.sd-scroll svg').count()==2
                    assert page.locator('[data-sac-dpo-lab=unrelated]').inner_text()=='untouched'
                    if not reduced:
                        sac.locator('[data-act="play"]').click();assert page.evaluate('__active.size')==1
                        page.evaluate("Object.defineProperty(document,'hidden',{value:true,configurable:true});document.dispatchEvent(new Event('visibilitychange'))")
                        assert page.evaluate('__active.size')==0
                        page.evaluate("Object.defineProperty(document,'hidden',{value:false,configurable:true})")
                        sac.locator('[data-act="play"]').click();sac.evaluate('e=>e.remove()');page.evaluate('window.__navigation()');assert page.evaluate('__active.size')==0
                    assert not errors, errors
                    if (lang,width) in (('en',1024),('zh-TW',320),('zh-TW',360),('en',720)) and not reduced:
                        page.screenshot(path=str(OUT/f'{lang}-{width}.png'),full_page=True)
                    count+=1
                    page.close()
        browser.close()
    print(f'SAC+DPO analytical browser lab scenarios: {count}/{count} PASS; screenshots in {OUT}')


if __name__=='__main__':run()
