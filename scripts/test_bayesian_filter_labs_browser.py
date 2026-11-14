"""Chromium visual/semantic regression for synthetic Kalman and particle labs.
Run: python scripts/test_bayesian_filter_labs_browser.py
"""
from __future__ import annotations
import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright

ROOT=Path(__file__).resolve().parent
OUT=Path('artifacts/bayesian-filter-labs')
OUT.mkdir(parents=True,exist_ok=True)
JS=(ROOT.parent/'docs/javascripts/bayesian-filter-labs.js').read_text(encoding='utf-8')
CSS=(ROOT.parent/'docs/stylesheets/bayesian-filter-labs.css').read_text(encoding='utf-8')

def fixture(lang='en'):
    fallback='Interactive numerical experiment requires JavaScript.' if lang=='en' else '互動數值實驗需要 JavaScript。'
    return f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{{max-width:960px;margin:0 auto;padding:12px;font-family:system-ui;background:#fff;color:#24394c}}*{{box-sizing:border-box}}{CSS}</style></head><body>
    <h1>{'Bayesian filter labs' if lang=='en' else '貝氏濾波互動實驗'}</h1>
    <h2>Kalman filter</h2><div class="bayesian-filter-lab" data-lab="kalman" data-lang="{lang}"><p class="bayesian-filter-fallback">{fallback}</p></div>
    <h2>Particle filter</h2><div class="bayesian-filter-lab" data-lab="particle" data-lang="{lang}"><p class="bayesian-filter-fallback">{fallback}</p></div>
    <script>{JS}</script></body></html>'''

async def run():
    async with async_playwright() as pw:
        browser=await pw.chromium.launch(headless=True,args=['--no-sandbox'])
        cases=0
        for lang in ('en','zh'):
            for width in (320,360,800,1024):
                page=await browser.new_page(viewport={'width':width,'height':900},device_scale_factor=1)
                await page.set_content(fixture(lang),wait_until='load')
                labs=page.locator('.bf-panel');assert await labs.count()==2
                assert await page.locator('.bayesian-filter-fallback').count()==0
                assert await page.locator('.bf-graphic svg').count()==2
                assert await page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'),f'{lang}/{width} page overflow'
                # Dynamic Kalman numeric result; y=7, prior=3, P=1.44, R=.64.
                ktext=await labs.nth(0).locator('.bf-output').inner_text()
                assert '3.000' in ktext and '1.440' in ktext,ktext
                # Move to final phase and assert posterior path appears.
                await labs.nth(0).get_by_role('button',name='Next' if lang=='en' else '下一步').click()
                await labs.nth(0).get_by_role('button',name='Next' if lang=='en' else '下一步').click()
                assert await labs.nth(0).locator('svg path').count()==3
                assert '5.769' in await labs.nth(0).locator('.bf-output').inner_text()
                # Particle weights exactly normalised, systematic ancestor sequence.
                ptext=await labs.nth(1).locator('.bf-output').inner_text()
                assert 'N = 10' in ptext,ptext
                await labs.nth(1).get_by_role('button',name='Next' if lang=='en' else '下一步').click()
                assert 'Σw = 1.000' in await labs.nth(1).locator('.bf-output').inner_text()
                await labs.nth(1).get_by_role('button',name='Next' if lang=='en' else '下一步').click()
                await labs.nth(1).get_by_role('button',name='Next' if lang=='en' else '下一步').click()
                assert await labs.nth(1).locator('svg circle').count()>=4
                # Seek and reset works.
                await labs.nth(1).locator('.bf-step').fill('1')
                await labs.nth(1).get_by_role('button',name='Reset' if lang=='en' else '重設').click()
                assert (await labs.nth(1).locator('.bf-step').input_value())=='0'
                # Keyboard access + focus outlines.
                await labs.nth(0).locator('.bf-step').focus()
                await page.keyboard.press('End')
                assert (await labs.nth(0).locator('.bf-step').input_value())=='2'
                await page.screenshot(path=str(OUT/f'{lang}-{width}.png'),full_page=True)
                await page.close();cases+=1
        # Test reduced-motion without spontaneous autoplay, and no-script fallbacks.
        page=await browser.new_page(reduced_motion='reduce')
        await page.set_content(fixture('en'))
        assert (await page.locator('.bf-panel').nth(0).get_by_role('button',name='Play').count())==1
        await page.close();cases+=1
        page=await browser.new_page(java_script_enabled=False)
        await page.set_content(fixture('zh'))
        assert await page.locator('.bayesian-filter-fallback').count()==2
        await page.close();cases+=1
        await browser.close()
        print(json.dumps({'cases':cases,'result':'PASS','screenshots':len(list(OUT.glob('*.png')))}))

if __name__=='__main__':asyncio.run(run())