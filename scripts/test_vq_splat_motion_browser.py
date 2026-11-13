#!/usr/bin/env python3
"""Chromium smoke tests for VQ-VAE and Gaussian-splatting animations."""
from __future__ import annotations
import asyncio, os, shutil, base64
from pathlib import Path
from playwright.async_api import async_playwright

ROOT=Path(__file__).resolve().parents[1]
DOCS=ROOT/'docs'
STEMS=('vqvae-codebook-snap','gaussian-splat-alpha-composite')

async def run():
    async with async_playwright() as pw:
        browser=await pw.chromium.launch(headless=True, executable_path=shutil.which("chromium") if os.getenv("USE_SYSTEM_CHROMIUM") else None)
        count=0
        for stem in STEMS:
            for lang in ('en','zh'):
                for width in (320,360,720,1024):
                    for reduce in (False,True):
                        page=await browser.new_page(viewport={'width':width,'height':580},reduced_motion='reduce' if reduce else 'no-preference')
                        def data_svg(mode):
                            raw=(DOCS/'assets/concept-animations'/f'{stem}-{mode}.svg').read_bytes()
                            encoded=base64.b64encode(raw).decode('ascii')
                            return f'data:image/svg+xml;base64,{encoded}#concept-animations/{stem}-{mode}.svg'
                        img=data_svg('motion')
                        still=data_svg('still')
                        alt='量化編碼動態演示' if lang=='zh' else 'Animated codebook walkthrough'
                        css=(DOCS/'stylesheets/concept-motion.css').read_text()
                        html=f'<meta charset="utf-8"><style>{css}</style><main><img alt="{alt}" src="{img}" data-still-src="{still}"></main>'
                        await page.set_content(html)
                        await page.add_script_tag(content=(DOCS/'javascripts/concept-motion.js').read_text())
                        await page.wait_for_selector('.concept-motion-toggle')
                        button=page.locator('.concept-motion-toggle')
                        picture=page.locator('.concept-motion-player img')
                        await page.wait_for_function("() => document.querySelector('img').complete && document.querySelector('img').naturalWidth === 640")
                        src=await picture.get_attribute('src')
                        assert ('-still.svg' in src) == reduce, (stem,lang,width,reduce,src)
                        await button.focus()
                        await page.keyboard.press('Enter')
                        src=await picture.get_attribute('src')
                        assert ('-still.svg' in src) != reduce, ('toggle failed',stem,width)
                        await page.keyboard.press('Space')
                        src=await picture.get_attribute('src')
                        assert ('-still.svg' in src) == reduce, ('second toggle failed',stem,width)
                        if width <= 680:
                            dims=await page.evaluate("""() => {
                                const node=document.querySelector('.concept-motion-player');
                                const img=node.querySelector('img');
                                const button=node.querySelector('button');
                                return [node.clientWidth,node.scrollWidth,img.getBoundingClientRect().width,button.getBoundingClientRect().left];
                            }""")
                            assert dims[1] > dims[0] and abs(dims[2]-640)<1 and dims[3]<width, (stem,lang,width,dims)
                        count+=1
                        await page.close()
        await browser.close()
        print(f'VQ-VAE and Gaussian splatting real-player Chromium cases: {count}/{count} PASS')
if __name__=='__main__': asyncio.run(run())
