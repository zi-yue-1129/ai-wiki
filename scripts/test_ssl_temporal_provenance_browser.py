#!/usr/bin/env python3
"""Chromium integration of the existing MoCo/BYOL player and new temporal probes."""
from pathlib import Path
import shutil
import os
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
JS=(ROOT/'docs/javascripts/ssl-temporal-provenance.js').read_text()
LAB_JS=(ROOT/'docs/javascripts/self-supervised-labs.js').read_text()
LAB_CSS=(ROOT/'docs/stylesheets/self-supervised-labs.css').read_text()
CSS=(ROOT/'docs/stylesheets/ssl-temporal-provenance.css').read_text()
OUT=ROOT/'artifacts/ssl-temporal-provenance'
OUT.mkdir(parents=True,exist_ok=True)

with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,args=['--no-sandbox'], **({'executable_path':'/usr/bin/chromium'} if shutil.which('chromium') else {}))
    count=0
    for kind in ('moco','byol'):
        for locale in ('en','zh-TW'):
            for width in (360,900):
                for reduced in (False,True):
                    page=browser.new_page(viewport={'width':width,'height':700},
                        reduced_motion='reduce' if reduced else 'no-preference')
                    errors=[]
                    page.on('pageerror',lambda e: errors.append(str(e)))
                    page.set_content('<!doctype html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"></head><body>'
                        f'<div data-self-supervised-lab="{kind}" data-locale="{locale}"></div></body></html>')
                    page.add_style_tag(content=LAB_CSS+'\n'+CSS)
                    page.add_script_tag(content=LAB_JS)
                    assert page.locator('[data-act=momentum]').count()==1, 'real lab momentum control missing'
                    page.add_script_tag(content=JS)
                    assert page.locator('.ssl-temporal-provenance').count()==1
                    seek=page.locator('[data-act="seek"]')
                    mom=page.locator('[data-act="momentum"]')
                    for m in (0.5,0.9,0.99):
                        mom.fill(str(m))
                        for frame in (0,3,4,5,8,9,10,13,14):
                            seek.fill(str(frame))
                            assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(kind,locale,width,m,frame,'overflow')
                            assert page.evaluate("""() => [...document.querySelectorAll('.ssl-temporal-chart svg text')].every(t=>{
                                const b=t.getBBox();return b.x>=-1&&b.y>=-1&&b.x+b.width<=641&&b.y+b.height<=271;
                            })"""),(kind,locale,width,m,frame,'SVG clipped text')
                            if kind=='moco':
                                step=frame//5+(frame%5==4)
                                expected=['A B C D E F','B C D E F G','C D E F G H','D E F G H I'][step]
                                assert expected in page.locator('.ssl-temporal-readout').inner_text()
                            else:
                                step=frame//5+(frame%5==4)
                                expected=100*(m**step)
                                actual=page.locator('.ssl-temporal-readout').inner_text()
                                assert f'{expected:.1f}%' in actual,(m,frame,actual)
                                assert page.locator('.ssl-temporal-chart rect').count()>=4
                    # Autoplay changes the seek value programmatically, without input.
                    seek.evaluate("e=>e.value='14'")
                    page.locator('.ssl-compute').evaluate("e=>e.textContent='autoplay changed frame'")
                    page.wait_for_timeout(35)
                    text=page.locator('.ssl-temporal-readout').inner_text()
                    assert '3/3' in text,text
                    mom.fill('0.9')
                    seek.fill('0')
                    page.locator('[data-act="speed"]').select_option('2')
                    page.locator('[data-act="play"]').click()
                    page.wait_for_timeout(1050)
                    assert int(seek.input_value()) >= 1,'player did not advance'
                    page.locator('[data-act="play"]').click()
                    assert not errors,errors
                    page.locator('.ssl-temporal-provenance').screenshot(
                        path=str(OUT/f'{kind}-{locale}-{width}-reduced-{reduced}.png'))
                    count+=1
                    page.close()
    browser.close()
print(f'PASS {count} Chromium cases: momentum, seek, autoplay, text bounds, responsive layout, reduced motion')
