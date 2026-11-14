#!/usr/bin/env python3
"""Chromium functional checks against committed interactive SimCLR/Bahdanau assets."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import os
ROOT=Path(__file__).resolve().parents[1]
JS=(ROOT/'docs/javascripts/contrastive-alignment-labs.js').read_text()
CSS=(ROOT/'docs/stylesheets/contrastive-alignment-labs.css').read_text()
OUT=ROOT/'artifacts/contrastive-alignment-labs'
OUT.mkdir(parents=True,exist_ok=True)
HTML='''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head><body style="margin:0;padding:12px;font:16px system-ui"><main style="max-width:720px;margin:auto"><div class="concept-arithmetic-lab" data-concept-lab="simclr" data-lang="LANG">Static image above</div><div class="concept-arithmetic-lab" data-concept-lab="bahdanau" data-lang="LANG">Static image above</div></main></body></html>'''
def main():
  total=0
  with sync_playwright() as p:
    args={'headless':True,'args':['--no-sandbox']}
    if os.getenv('CHROMIUM_PATH'):args['executable_path']=os.environ['CHROMIUM_PATH']
    elif Path('/usr/bin/chromium').exists():args['executable_path']='/usr/bin/chromium'
    browser=p.chromium.launch(**args)
    for lang in ('en','zh-TW'):
      for width in (320,360,720,1024):
        for reduced in (False,True):
          ctx=browser.new_context(viewport={'width':width,'height':900},reduced_motion='reduce' if reduced else 'no-preference')
          page=ctx.new_page()
          page.set_content(HTML.replace('LANG',lang))
          page.add_style_tag(content=CSS);page.add_script_tag(content=JS)
          assert page.locator('.cal-scroll svg').count()==2
          assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(lang,width)
          sim=page.locator('[data-concept-lab="simclr"]')
          sim.locator('input[type=range]').first.fill('1')
          assert '0.353' in sim.locator('.cal-readout').inner_text()
          sim.locator('input[type=range]').first.fill('5')
          assert '0.851' in sim.locator('.cal-readout').inner_text()
          sim.locator('input[type=range]').nth(1).fill('0.1')
          assert 'NT-Xent' in sim.locator('.cal-readout').inner_text()
          sim.locator('button').last.click()
          sim.locator('button').nth(2).click()
          assert sim.locator('button').nth(2).inner_text() in ('Pause','暫停')
          sim.locator('button').nth(2).click()
          b=page.locator('[data-concept-lab="bahdanau"]')
          before=b.locator('.cal-readout').inner_text()
          b.locator('input[type=range]').nth(1).fill('2')
          assert b.locator('.cal-readout').inner_text()!=before
          b.locator('input[type=range]').first.fill('2')
          assert '1.000' in b.locator('.cal-readout').inner_text()
          b.locator('button').last.click()
          b.locator('select').last.select_option('2')
          b.locator('button').nth(2).click()
          assert b.locator('button').nth(2).inner_text() in ('Pause','暫停')
          b.locator('button').nth(2).click()
          for kind in ('simclr','bahdanau'):
            el=page.locator('[data-concept-lab="'+kind+'"] .cal-scroll')
            assert el.evaluate('(e)=>e.scrollWidth>e.clientWidth') if width<640 else True
            if width<640:
              el.focus();page.keyboard.press('ArrowRight')
              page.wait_for_timeout(50)
              assert el.evaluate('(e)=>e.scrollLeft>0')
          if width in (320,1024) and not reduced:
            page.screenshot(path=str(OUT/f'{lang}-{width}.png'),full_page=True)
          total+=1;ctx.close()
    browser.close()
  print(f'PASS {total}/16 bilingual size/reduced-motion cases, real SVG, numerical and keyboard controls')
if __name__=='__main__':main()
