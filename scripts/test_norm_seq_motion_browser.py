#!/usr/bin/env python3
"""Chromium regression: Github-static-first SVGs enhanced by the actual MkDocs player."""
from __future__ import annotations
from pathlib import Path
from playwright.sync_api import sync_playwright

ASSETS=Path('docs/assets/concept-animations')
JS=Path('docs/javascripts/concept-motion.js').read_text(encoding='utf-8')
CSS=Path('docs/stylesheets/concept-motion.css').read_text(encoding='utf-8')
OUT=Path('artifacts/norm-seq-motion')
OUT.mkdir(parents=True,exist_ok=True)
STEMS=('layernorm-feature-shift','seq2seq-context-handoff')

def exercise(browser,stem,locale,width,reduced):
  ctx=browser.new_context(viewport={'width':width,'height':720},reduced_motion='reduce' if reduced else 'no-preference')
  page=ctx.new_page()
  def serve(route):
    filename=route.request.url.split('?',1)[0].split('/')[-1]
    p=ASSETS/filename
    if not p.is_file():
      route.fulfill(status=404,body='missing')
    else:
      route.fulfill(status=200,content_type='image/svg+xml',body=p.read_bytes())
  page.route('**/concept-animations/*.svg',serve)
  alt=('單一樣本的特徵軸正規化比較' if locale=='zh' else 'Single sample feature-wise normalisation')
  src=f'https://wiki.invalid/docs/assets/concept-animations/{stem}-still.svg'
  html=f'''<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head>
    <body><main style="max-width:1100px;margin:0 auto"><img alt="{alt}" src="{src}"></main></body></html>'''
  page.set_content(html,wait_until='domcontentloaded')
  page.add_script_tag(content=JS)
  page.wait_for_selector('.concept-motion-player button')
  host=page.locator('.concept-motion-player')
  img=page.locator('.concept-motion-player img')
  button=page.locator('.concept-motion-toggle').first
  assert host.count()==1 and host.get_attribute('tabindex')=='0'
  assert img.get_attribute('alt')==alt
  assert (img.get_attribute('src') or '').endswith('-still.svg')==reduced
  page.wait_for_function("document.querySelector('img').complete && document.querySelector('img').naturalWidth > 0")
  assert page.locator('.concept-motion-player img').evaluate('(i)=>i.naturalWidth')==860
  if width in (320,360):
    assert host.evaluate('(h)=>h.scrollWidth>h.clientWidth'), 'mobile image unexpectedly shrank'
    assert img.evaluate('(i)=>Math.round(i.getBoundingClientRect().width)')==860
    host.focus()
    page.keyboard.press('ArrowRight')
    page.wait_for_timeout(120)
    assert host.evaluate('(h)=>h.scrollLeft')>0
    host.evaluate('(h)=>h.scrollLeft=0')
  # Keyboard on native button toggles the source between motion and still.
  button.focus()
  page.keyboard.press('Enter')
  assert (img.get_attribute('src') or '').endswith('-motion.svg')==reduced
  button.focus()
  page.keyboard.press('Space')
  assert (img.get_attribute('src') or '').endswith('-still.svg')==reduced
  page.screenshot(path=str(OUT/f'{stem}-{locale}-{width}-{int(reduced)}.png'))
  page.close();ctx.close()

with sync_playwright() as p:
  browser=p.chromium.launch(headless=True)
  total=0
  for stem in STEMS:
    for locale in ('en','zh'):
      for width in (320,360,860,1024):
        exercise(browser,stem,locale,width,False);total+=1
      exercise(browser,stem,locale,320,True);total+=1
  browser.close()
print(f'PASS: {total} Chromium bilingual/responsive/reduced-motion player scenarios')