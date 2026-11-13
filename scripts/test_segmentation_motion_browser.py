#!/usr/bin/env python3
"""Chromium regression for segmentation teaching SVGs and shared MkDocs controls.

Run from repository root after `python -m playwright install chromium`.
"""
import asyncio
import hashlib
import tempfile
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'docs/assets/concept-animations'
PLAYER = ROOT / 'docs/javascripts/concept-motion.js'
PAIRS = ('roi-align-sampling', 'sam-prompt-ambiguity')

async def main():
    assert PLAYER.is_file(), f'Missing {PLAYER}'
    for stem in PAIRS:
        for suffix in ('motion', 'still'):
            assert (ASSETS / f'{stem}-{suffix}.svg').is_file()
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        checks = 0
        for stem in PAIRS:
            for width in (320, 360, 800, 1024):
                for language in ('en', 'zh-TW'):
                    page = await browser.new_page(viewport={'width': width, 'height': 610})
                    alt = ('示意圖：可水平捲動的分割動畫' if language == 'zh-TW' else 'Scrollable segmentation teaching animation')
                    still = (ASSETS / f'{stem}-still.svg').as_uri()
                    motion = (ASSETS / f'{stem}-motion.svg').as_uri()
                    # Same markup contract used by both bilingual wiki chapters.
                    markup = f'''<!doctype html><meta charset="utf-8">
                    <style>body{{margin:0;padding:10px}}.wide{{max-width:100%;overflow-x:auto}}.inner{{width:800px}}
                    .concept-motion-player{{display:block;max-width:640px}}
                    .concept-motion-player img{{display:block;width:100%;height:auto}}
                    </style>
                    <div class="wide" role="region" tabindex="0"><div class="inner">
                    <img src="{still}" data-motion-src="{motion}" data-still-src="{still}" alt="{alt}" width="800" height="460"></div></div>
                    <script>{PLAYER.read_text(encoding='utf-8')}</script>'''
                    with tempfile.TemporaryDirectory() as d:
                        fp = Path(d) / 'review.html'
                        fp.write_text(markup, encoding='utf-8')
                        await page.goto(fp.as_uri(), wait_until='load')
                        btn = page.locator('.concept-motion-toggle')
                        assert await btn.count() == 1, f'{stem}: player missing'
                        assert 'Pause' in await btn.inner_text() or '暫停' in await btn.inner_text()
                        await page.locator('img').evaluate('(im)=>im.decode()')
                        assert stem+'-motion.svg' in await page.locator('img').get_attribute('src')
                        await btn.click()
                        assert stem+'-still.svg' in await page.locator('img').get_attribute('src')
                        await btn.focus()
                        await page.keyboard.press('Enter')
                        assert stem+'-motion.svg' in await page.locator('img').get_attribute('src')
                        await page.keyboard.press('Space')
                        assert stem+'-still.svg' in await page.locator('img').get_attribute('src')
                        if width <= 360:
                            s = await page.locator('.wide').evaluate('(e)=>({scroll:e.scrollWidth,client:e.clientWidth})')
                            assert s['scroll'] > s['client'] + 200, (stem, s)
                        checks += 1
                    await page.close()
            # Reduced motion must show still before any manual interaction.
            page = await browser.new_page(viewport={'width':360,'height':600}, reduced_motion='reduce')
            alt='示意圖：靜態回退'
            still=(ASSETS/f'{stem}-still.svg').as_uri(); motion=(ASSETS/f'{stem}-motion.svg').as_uri()
            with tempfile.TemporaryDirectory() as d:
                fp=Path(d)/'reduced.html'
                fp.write_text(f'<meta charset="utf-8"><img src="{still}" data-motion-src="{motion}" alt="{alt}"><script>{PLAYER.read_text(encoding="utf-8")}</script>',encoding='utf-8')
                await page.goto(fp.as_uri(),wait_until='load')
                assert stem+'-still.svg' in await page.locator('img').get_attribute('src')
                assert '播放' in await page.locator('button').inner_text()
                checks+=1
            await page.close()
            # Verify SVG SMIL actually changes the rendered frame when scrubbed.
            page=await browser.new_page(viewport={'width':850,'height':520})
            await page.set_content((ASSETS/f'{stem}-motion.svg').read_text(encoding='utf-8'))
            await page.locator('svg').evaluate('(e)=>e.setCurrentTime(0)')
            first=hashlib.sha256(await page.locator('svg').screenshot()).hexdigest()
            await page.locator('svg').evaluate('(e)=>e.setCurrentTime(5.6)')
            second=hashlib.sha256(await page.locator('svg').screenshot()).hexdigest()
            assert first!=second, f'{stem} is not visibly animated'
            checks+=1
            await page.close()
        await browser.close()
        print(f'Segmentation browser regressions passed: {checks} checks')

if __name__=='__main__':
    asyncio.run(main())