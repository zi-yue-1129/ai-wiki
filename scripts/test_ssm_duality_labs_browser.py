#!/usr/bin/env python3
"""Real Chromium lab interaction, arithmetic, accessibility and responsive QA.
Run from repository root; defaults also work from a standalone QA archive.
"""
import asyncio
import argparse
from pathlib import Path
from playwright.async_api import async_playwright

async def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--root',type=Path,default=Path('.'))
    ap.add_argument('--out',type=Path,default=Path('artifacts/ssm-duality-labs'))
    args=ap.parse_args()
    js=(args.root/'docs/javascripts/ssm-duality-labs.js').resolve()
    css=(args.root/'docs/stylesheets/ssm-duality-labs.css').resolve()
    assert js.is_file() and css.is_file()
    args.out.mkdir(parents=True,exist_ok=True)
    async def set_range(locator, value):
        await locator.evaluate('(node, v) => {node.value = String(v); node.dispatchEvent(new Event(\"input\", {bubbles:true}));}', value)
    successes=[]
    async with async_playwright() as p:
        browser=await p.chromium.launch(headless=True,executable_path='/usr/bin/chromium' if Path('/usr/bin/chromium').exists() else None,args=['--no-sandbox'])
        for width in (320,360,760,1024):
            for lang in ('en','zh'):
                for motion in ('no-preference','reduce'):
                    page=await browser.new_page(viewport={'width':width,'height':820},reduced_motion=motion)
                    html=f'''<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>
                    body {{box-sizing:border-box;margin:0;padding:12px;font:16px Arial,sans-serif;}}
                    main {{max-width:880px;margin:auto;}}
                    *,*:before,*:after {{box-sizing:border-box;}}
                    </style></head><body><main><h2>{'範例計算' if lang=='zh' else 'Numeric demonstrations'}</h2>
                    <div class="ssm-lab" data-ssm-lab="s4d" data-lang="{lang}"></div>
                    <div class="ssm-lab" data-ssm-lab="ssd" data-lang="{lang}"></div></main></body></html>'''
                    await page.set_content(html)
                    await page.add_style_tag(path=str(css))
                    await page.add_script_tag(path=str(js))
                    labs=page.locator('.ssm-lab')
                    assert await labs.count()==2
                    assert await page.locator('.ssm-lab-viewport svg').count()==2
                    dims=await page.evaluate('''() => ({doc:document.documentElement.scrollWidth, client:document.documentElement.clientWidth,
                       plots:[...document.querySelectorAll('.ssm-lab-viewport')].map(v=>({client:v.clientWidth, scroll:v.scrollWidth,
                       svg:v.querySelector('svg').getBoundingClientRect().width,
                       bounds:v.getBoundingClientRect().width}))})''')
                    assert dims['doc']<=dims['client']+2,dims
                    if width<=760:assert all(v['svg']>=759 and v['scroll']>=v['client'] for v in dims['plots']),dims
                    s4d=labs.nth(0);ssd=labs.nth(1)
                    assert '1.630' in (await s4d.locator('[data-role=equation]').inner_text())
                    await s4d.locator('[data-action=next]').click()
                    assert (await s4d.locator('[data-role=seek]').input_value())=='1'
                    await set_range(s4d.locator('[data-param=decay]'),0.90)
                    assert '0.90' in (await s4d.locator('[data-value=decay]').inner_text())
                    await s4d.locator('[data-action=reset]').click()
                    assert (await s4d.locator('[data-role=seek]').input_value())=='0'
                    assert (await s4d.locator('[data-param=decay]').input_value())=='0.79'
                    assert '1.505' not in (await ssd.locator('[data-role=equation]').inner_text())  # first row only
                    await set_range(ssd.locator('[data-role=seek]'),3)
                    assert '1.505' in (await ssd.locator('[data-role=equation]').inner_text())
                    assert '0.0e+0' in (await ssd.locator('[data-role=metrics]').inner_text())
                    await set_range(ssd.locator('[data-param=a2]'),.50)
                    assert '1.505' not in (await ssd.locator('[data-role=equation]').inner_text())
                    await ssd.locator('[data-action=reset]').click()
                    await ssd.locator('[data-action=next]').click()
                    await ssd.locator('[data-action=speed]').click()
                    assert (await ssd.locator('[data-action=speed]').inner_text())=='2×'
                    await ssd.locator('[data-action=play]').click()
                    assert (await ssd.locator('[data-action=play]').inner_text()) in ('Pause','暫停')
                    await ssd.locator('[data-action=play]').click()
                    assert (await ssd.locator('[data-action=play]').inner_text()) in ('Play','播放')
                    await ssd.locator('[data-action=next]').focus()
                    await page.keyboard.press('Enter')
                    assert (await ssd.locator('[data-role=seek]').input_value())=='2'
                    if motion=='reduce':
                        assert await page.evaluate("matchMedia('(prefers-reduced-motion: reduce)').matches")
                    if (width,lang,motion) in ((320,'zh','reduce'),(360,'en','no-preference'),(1024,'en','no-preference'),(1024,'zh','reduce')):
                        await page.screenshot(path=str(args.out/f'{lang}-{width}-{motion}.png'),full_page=True)
                    successes.append((lang,width,motion))
                    await page.close()
        await browser.close()
    print('SSM LAB CHROMIUM PASS',len(successes),'combinations')

if __name__=='__main__':asyncio.run(main())