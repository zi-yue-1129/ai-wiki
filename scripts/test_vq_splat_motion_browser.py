#!/usr/bin/env python3
"""Chromium smoke tests for VQ-VAE and Gaussian-splatting animations."""
from __future__ import annotations
import asyncio, os, shutil, base64, re
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
                        topic = 'theory/paradigms/unsupervised/density-and-generative-models/vae/vq-vae' if stem.startswith('vqvae') else 'theory/models/computer-vision/3d-and-neural-rendering/gaussian-splatting'
                        source = (DOCS / f'{topic}{".zh-TW" if lang == "zh" else ""}.md').read_text()
                        markup = re.search(r'<div style="width:100%;overflow-x:auto".*?</div></div>',source,re.S).group(0)
                        markup = re.sub(r'(src|data-motion-src|data-still-src)="[^"]+"',lambda m:f'{m[1]}="{img if m[1]=="data-motion-src" else still}"',markup)
                        html=f'<html lang="{"zh-TW" if lang=="zh" else "en"}"><meta charset="utf-8"><style>{css}</style><main>{markup}</main></html>'
                        await page.set_content(html)
                        # Without JavaScript (including GitHub's sanitised Markdown),
                        # this element must directly show the static fallback.
                        assert '-still.svg' in await page.locator('img').get_attribute('src')
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
                                const node=document.querySelector('div[role=region]');
                                const img=node.querySelector('img');
                                const button=node.querySelector('button');
                                return [node.clientWidth,node.scrollWidth,img.getBoundingClientRect().width,button.getBoundingClientRect().left];
                            }""")
                            assert dims[1] > dims[0] and abs(dims[2]-640)<1 and dims[3]<width, (stem,lang,width,dims)
                        if width < 640:
                            region=page.locator('div[role=region]');await region.focus();await page.keyboard.press('ArrowRight')
                            await page.wait_for_function('el => el.scrollLeft > 0',arg=await region.element_handle())
                        assert await page.evaluate('document.documentElement.scrollWidth <= innerWidth+2')
                        out=ROOT/'artifacts/vq-splat-motion';out.mkdir(parents=True,exist_ok=True)
                        await page.screenshot(path=str(out/f'{stem}-{lang}-{width}-{int(reduce)}.png'),full_page=True)
                        count+=1
                        await page.close()
        await browser.close()
        print(f'VQ-VAE and Gaussian splatting real-player Chromium cases: {count}/{count} PASS')
if __name__=='__main__': asyncio.run(run())
