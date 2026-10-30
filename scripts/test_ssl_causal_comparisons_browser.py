#!/usr/bin/env python3
"""Chromium visual and mathematical regression for MoCo/BYOL counterfactuals."""
from pathlib import Path
from math import exp, log, acos, sin
from playwright.sync_api import sync_playwright
import re, shutil
ROOT = Path(__file__).resolve().parents[1]
JS = (ROOT/'docs/javascripts/ssl-causal-comparisons.js').read_text()
CSS = (ROOT/'docs/stylesheets/ssl-causal-comparisons.css').read_text()
LAB_JS_PATH = ROOT/'docs/javascripts/self-supervised-labs.js'
LAB_CSS_PATH = ROOT/'docs/stylesheets/self-supervised-labs.css'
OUT = ROOT/'artifacts/ssl-causal-comparisons'
OUT.mkdir(parents=True,exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--no-sandbox'], **({'executable_path':'/usr/bin/chromium'} if shutil.which('chromium') else {}))
    for kind in ('moco','byol'):
        for locale in ('en','zh-TW'):
            for width in (360,900):
                for reduced in (False,True):
                    page = browser.new_page(viewport={'width':width,'height':900}, reduced_motion='reduce' if reduced else 'no-preference')
                    errors=[]
                    page.on('pageerror',lambda e: errors.append(str(e)))
                    page.set_content('<!doctype html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"></head><body><main style="max-width:850px;margin:auto">'+f'<div data-self-supervised-lab="{kind}" data-locale="{locale}">'+
                        ('' if LAB_JS_PATH.exists() else '<div class="ssl-loss"><input data-act="loss" type="range" min="'+('0.1' if kind=='moco' else '-1')+'" max="1" step="0.05" value="'+('0.2' if kind=='moco' else '0.5')+'"></div>')+'</div></main></body></html>')
                    page.add_style_tag(content=CSS)
                    if LAB_CSS_PATH.exists(): page.add_style_tag(content=LAB_CSS_PATH.read_text())
                    if LAB_JS_PATH.exists(): page.add_script_tag(content=LAB_JS_PATH.read_text())
                    page.add_script_tag(content=JS)
                    assert page.locator('.ssl-causal').count()==1,(kind,locale)
                    slider=page.locator('[data-act="loss"]')
                    if kind=='moco':
                        for tau in (0.1,0.2,0.5,1):
                            slider.evaluate('(el,v)=>{el.value=v;el.dispatchEvent(new Event("input",{bubbles:true}));}',str(tau))
                            out=page.locator('.ssl-causal-readout').inner_text()
                            losses=[float(v) for v in re.findall(r'L=([0-9.]+)',out)]
                            probs=[]
                            for negatives in ([ -.2,-.1,0,.1,.2,.05],[-.1,0,.1,.2,.05,.7]):
                                prob=1/(1+sum(exp((s-.7)/tau) for s in negatives))
                                probs.append(prob)
                            assert len(losses)==2 and all(abs(g+log(e))<.001 for g,e in zip(losses,probs)),(tau,losses,probs)
                            assert losses[1]>losses[0]
                            assert page.locator('.ssl-causal svg rect[stroke="#b94d32"]').count()==1
                    else:
                        for cosine in (-1,-.5,0,.5,1):
                            slider.evaluate('(el,v)=>{el.value=v;el.dispatchEvent(new Event("input",{bubbles:true}));}',str(cosine))
                            out=page.locator('.ssl-causal-readout').inner_text()
                            actual=float(re.search(r'\|dL/dφ\|=([0-9.]+)',out).group(1))
                            assert abs(actual-2*sin(acos(cosine)))<.001,(cosine,actual)
                            assert page.locator('.ssl-causal svg path[stroke="#b25e66"]').count()==2
                    assert not errors,errors
                    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(kind,locale,width,'overflow')
                    assert page.evaluate('''() => [...document.querySelectorAll('.ssl-causal svg text')].every(t=>{
                      const b=t.getBBox(),svg=t.ownerSVGElement,v=svg.viewBox.baseVal;
                      return b.x>=-1&&b.y>=-1&&b.x+b.width<=v.width+1&&b.y+b.height<=v.height+1;
                    })'''),(kind,locale,width,'text clipped')
                    # Native range remains keyboard operable; no extra input was introduced.
                    assert page.locator('.ssl-causal input').count()==0
                    slider.focus()
                    before=slider.input_value()
                    page.keyboard.press('ArrowRight' if before!='1' else 'ArrowLeft')
                    assert slider.input_value()!=before
                    page.locator('.ssl-causal').screenshot(path=str(OUT/f'{kind}-{locale}-{width}-reduced-{reduced}.png'))
                    page.close()
    browser.close()
print('PASS: 16 Chromium scenarios, finite toy losses, angular sensitivity, SVG text bounds, keyboard and responsive layout')
