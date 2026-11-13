#!/usr/bin/env python3
"""Chromium visual/control regression for S4D and Mamba-2.

Use in repository root. Requires playwright + Chromium; local tests can pass
--assets-dir to point at a prepared standalone asset folder.
"""
from __future__ import annotations
import asyncio
import argparse
from pathlib import Path
import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
from functools import partial
from playwright.async_api import async_playwright

ROOT=Path(__file__).resolve().parents[1] if Path('docs/javascripts/concept-motion.js').exists() else Path.cwd()
STEMS=('s4d-diagonal-modes','mamba2-ssd-causal-map')
SIZES=(320,360,760,1024)

async def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--assets-dir',type=Path,default=Path('docs/assets/concept-animations'))
    ap.add_argument('--screenshots',type=Path,default=Path('artifacts/ssm-motion'))
    args=ap.parse_args()
    assets=args.assets_dir.resolve()
    docs=Path('docs').resolve()
    js=docs/'javascripts/concept-motion.js'
    css=docs/'stylesheets/concept-motion.css'
    extra=docs/'stylesheets/extra.css'
    # The harness serves real SVGs and runs the existing site JS without mocking media events.
    args.screenshots.mkdir(parents=True,exist_ok=True)
    for stem in STEMS:
        for kind in ('motion','still'):
            assert (assets/f'{stem}-{kind}.svg').is_file(),stem
    handler=partial(SimpleHTTPRequestHandler,directory=str(assets))
    server=ThreadingHTTPServer(('127.0.0.1',0),handler)
    thread=Thread(target=server.serve_forever,daemon=True);thread.start()
    port=server.server_address[1]
    checks=[]
    async with async_playwright() as playwright:
        browser=await playwright.chromium.launch(headless=True, executable_path='/usr/bin/chromium' if Path('/usr/bin/chromium').exists() else None, args=['--no-sandbox'])
        for stem in STEMS:
            for lang in ('en','zh'):
                for width in SIZES:
                    page=await browser.new_page(viewport={'width':width,'height':560}, device_scale_factor=1, reduced_motion='reduce' if lang=='zh' else 'no-preference')
                    still=f'http://127.0.0.1:{port}/{stem}-still.svg'
                    motion=f'http://127.0.0.1:{port}/{stem}-motion.svg'
                    alt='狀態空間模型動畫說明' if lang=='zh' else 'State space model illustration'
                    html=f'''<!doctype html><html><head><meta charset="utf-8"><style>
                    body{{margin:0;padding:12px;background:#fff;font-family:Arial}}
                    .ssm-motion-viewport{{max-width:100%;overflow-x:auto;overflow-y:hidden;}}
                    .ssm-motion-viewport .concept-motion-player{{width:860px;max-width:none}}
                    .ssm-motion-viewport img{{width:860px;max-width:none}}
                    </style></head><body><div class="ssm-motion-viewport" tabindex="0">
                    <img alt="{alt}" src="{still}" data-motion-src="{motion}" data-still-src="{still}">
                    </div></body></html>'''
                    await page.set_content(html)
                    if css.exists():await page.add_style_tag(path=str(css))
                    if extra.exists():await page.add_style_tag(path=str(extra))
                    if js.exists():await page.add_script_tag(path=str(js))
                    else:
                        # Visual-only local run when the checked-out player is unavailable.
                        print('SKIP PLAYER:',js)
                        await page.screenshot(path=str(args.screenshots/f'{stem}-{lang}-{width}-static.png'))
                        await page.close(); continue
                    button=page.locator('button.concept-motion-toggle').first
                    await button.wait_for()
                    img=page.locator('.ssm-motion-viewport img').first
                    await page.wait_for_function('document.querySelector(".ssm-motion-viewport img").complete')
                    assert (await img.get_attribute('src'))==(still if lang=='zh' else motion)
                    assert await button.count()==1
                    size=await page.evaluate('''() => {let p=document.querySelector('.ssm-motion-viewport'),im=p.querySelector('img');return {client:p.clientWidth,scroll:p.scrollWidth,img:im.getBoundingClientRect().width,complete:im.complete, natural:im.naturalWidth}}''')
                    assert size['complete'] and size['natural'] == 860, size
                    assert size['img'] >= 859,size
                    if width < 860: assert size['scroll']>size['client'], size
                    await page.screenshot(path=str(args.screenshots/f'{stem}-{lang}-{width}-initial.png'))
                    await button.click()
                    assert await img.get_attribute('src')==(motion if lang=='zh' else still)
                    await button.focus(); await page.keyboard.press('Enter')
                    assert await img.get_attribute('src')==(still if lang=='zh' else motion)
                    if width < 860:
                        await page.locator('.ssm-motion-viewport').focus()
                        await page.keyboard.press('End')
                        # Scrollable and focusable rather than shrinking the SVG.
                        assert await page.evaluate("document.querySelector('.ssm-motion-viewport').scrollWidth > document.querySelector('.ssm-motion-viewport').clientWidth")
                    checks.append(f'{stem}/{lang}/{width}: load, keyboard, toggle, fallback, mobile scroll OK')
                    await page.close()
        await browser.close()
    server.shutdown();server.server_close()
    print('\n'.join(checks))
    print(f'PASS {len(checks)} browser combinations')

if __name__=='__main__':asyncio.run(main())