#!/usr/bin/env python3
"""Render two bilingual, static-first diffusion diagrams and exercise actual player behavior."""
from pathlib import Path
from xml.etree import ElementTree as ET
import asyncio
import re
import tempfile
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "docs/assets/concept-animations"
JS = ROOT / "docs/javascripts/concept-motion.js"
CSS = ROOT / "docs/stylesheets/concept-motion.css"
STEMS = ("score-sde-flow", "consistency-trajectory-map")
DOCS = ROOT / "docs/theory/paradigms/unsupervised/density-and-generative-models/diffusion"
NS = "{http://www.w3.org/2000/svg}"
OUT = ROOT / "artifacts/diffusion-motion"

def check_source():
    for stem in STEMS:
        motion = ASSETS / (stem + "-motion.svg")
        still = ASSETS / (stem + "-still.svg")
        a, b = ET.parse(motion).getroot(), ET.parse(still).getroot()
        assert a.tag == b.tag == NS + "svg"
        assert a.get("viewBox") == b.get("viewBox") == "0 0 800 420"
        assert any(x.tag in (NS + "animate", NS + "animateMotion") for x in a.iter())
        assert not any(x.tag in (NS + "animate", NS + "animateMotion") for x in b.iter())
        for root in (a, b):
            for node in root.iter():
                assert node.tag.split("}")[-1] not in {"script", "foreignObject", "iframe"}
                for key, value in node.attrib.items():
                    assert not key.split("}")[-1].startswith("on")
                    assert "javascript:" not in value and "data:" not in value
        for suffix in (".md", ".zh-TW.md"):
            p = DOCS / (("score-sde" if stem == "score-sde-flow" else "consistency-models") + suffix)
            content = p.read_text()
            assert f"{stem}-still.svg" in content
            assert "CC BY-SA 4.0" in content
    assert "staticFirst" in JS.read_text()

async def main():
    check_source()
    OUT.mkdir(parents=True, exist_ok=True)
    count = 0
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        for stem in STEMS:
            for chinese in (False, True):
                alt = "可水平捲動的教學動畫圖" if chinese else "A scrollable diffusion teaching diagram"
                # file:// is used so relative resources and repository JS load in a real browser.
                html = f'''<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="{CSS.as_uri()}"></head><body><article><img src="{(ASSETS / (stem+"-still.svg")).as_uri()}" alt="{alt}"></article><script src="{JS.as_uri()}"></script></body></html>'''
                with tempfile.TemporaryDirectory() as temp:
                    sample = Path(temp) / "sample.html"
                    sample.write_text(html)
                    for width in (320, 360, 720, 1024):
                        page = await browser.new_page(viewport={"width":width,"height":650})
                        await page.goto(sample.as_uri())
                        btn = page.locator(".concept-motion-toggle").first
                        assert await btn.count() == 1, (stem, chinese, width)
                        image = page.locator("img")
                        await image.evaluate("(img) => img.decode()")
                        assert await image.get_attribute("src") == (ASSETS / (stem + "-motion.svg")).as_uri()
                        host = page.locator(".concept-motion-wide")
                        assert await host.count() == 1
                        assert await host.get_attribute("tabindex") == "0"
                        await btn.click()
                        assert "-still.svg" in (await image.get_attribute("src"))
                        assert "Play" in (await btn.inner_text()) or "播放" in (await btn.inner_text())
                        await btn.focus()
                        await page.keyboard.press("Enter")
                        assert "-motion.svg" in (await image.get_attribute("src"))
                        await page.keyboard.press("Space")
                        assert "-still.svg" in (await image.get_attribute("src"))
                        if width <= 360:
                            dims=await host.evaluate("(el) => ({scroll:el.scrollWidth,client:el.clientWidth})")
                            assert dims["scroll"] > dims["client"], dims
                        await page.screenshot(path=str(OUT / f"{stem}-{'zh' if chinese else 'en'}-{width}.png"))
                        count += 1
                        await page.close()
            for width in (320, 360, 720, 1024):
                page = await browser.new_page(viewport={"width":width,"height":650}, reduced_motion="reduce")
                html = f'''<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="{CSS.as_uri()}"></head><body><img src="{(ASSETS / (stem+"-still.svg")).as_uri()}" alt="Still diagram"><script src="{JS.as_uri()}"></script></body></html>'''
                with tempfile.TemporaryDirectory() as temp:
                    sample=Path(temp)/"reduced.html"
                    sample.write_text(html)
                    await page.goto(sample.as_uri())
                    assert "-still.svg" in (await page.locator("img").get_attribute("src"))
                    assert "Play" in (await page.locator(".concept-motion-toggle").inner_text())
                count += 1
                await page.close()
        await browser.close()
    print(f"Diffusion static-first browser tests: {count} scenarios passed")

if __name__ == "__main__":
    asyncio.run(main())
