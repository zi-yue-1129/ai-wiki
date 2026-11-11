#!/usr/bin/env python3
"""Chromium regression: Diffusion Policy animation, reduced motion and MkDocs player.

This tests inline SVG time control and the real shared player script on a local
HTML fixture, not the deployed MkDocs theme. Screenshots are kept for review.
"""
from __future__ import annotations

import asyncio
import os
import threading
import xml.etree.ElementTree as ET
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[1]
ASSET = ROOT / "docs/assets/concept-animations"
PLAYER = ROOT / "docs/javascripts/concept-motion.js"
OUTPUT = ROOT / "artifacts/diffusion-policy-motion"
STEMS = ("diffusion-policy-denoising", "diffusion-policy-receding-horizon",
         "diffusion-policy-noise-training", "diffusion-policy-multimodal-actions")
WIDTHS = (320, 360, 720, 1024)
TIMES = (0.1, 2.3, 4.7, 7.1, 9.6)
NS = "{http://www.w3.org/2000/svg}"


def validate_sources(stem):
    for kind in ("motion", "still"):
        path = ASSET / f"{stem}-{kind}.svg"
        root = ET.parse(path).getroot()
        assert root.tag == NS + "svg" and root.get("viewBox") == "0 0 640 360"
        assert not any(e.tag == NS + "script" for e in root.iter())
        assert not any(k.startswith("{http://www.w3.org/1999/xlink}") for e in root.iter() for k in e.attrib)
        if kind == "motion":
            assert any(e.tag in (NS + "animate", NS + "animateMotion") for e in root.iter())
            assert 'repeatCount="indefinite"' in path.read_text(encoding="utf-8")


async def check_svg(browser, stem, width):
    page = await browser.new_page(viewport={"width": width, "height": max(260, int(width * .62) + 30)})
    try:
        motion = (ASSET / f"{stem}-motion.svg").read_text(encoding="utf-8")
        await page.set_content(f'<html><body style="margin:0"><div style="width:{width}px">{motion}</div></body></html>')
        svg = page.locator("svg")
        await svg.evaluate("s => {s.style.width='100%';s.style.height='auto';s.pauseAnimations()}")
        for t in TIMES:
            await svg.evaluate("(s,t) => s.setCurrentTime(t)", t)
            bounds = await svg.evaluate("""s => {
                const v = s.viewBox.baseVal;
                const nodes = [...s.querySelectorAll('text')];
                return {count:nodes.length, overflow:nodes.filter(n => {
                    const b=n.getBBox();
                    return b.x < -1 || b.y < -1 ||
                           b.x+b.width > v.width+1 || b.y+b.height > v.height+1;
                }).map(n => n.textContent)};
            }""")
            assert bounds["count"] >= 4 and not bounds["overflow"], (stem, width, t, bounds)
            await svg.screenshot(path=str(OUTPUT / f"{stem}-{width}-{t:.1f}.png"))
        await svg.evaluate("s => s.unpauseAnimations()")
        assert not await svg.evaluate("s => s.animationsPaused()")
        await page.emulate_media(reduced_motion="reduce")
        displays = await svg.evaluate("""s => ({
            motion:getComputedStyle(s.querySelector('.motion')).display,
            reduced:getComputedStyle(s.querySelector('.reduced')).display
        })""")
        assert displays["motion"] == "none" and displays["reduced"] != "none", displays
        still = (ASSET / f"{stem}-still.svg").read_text(encoding="utf-8")
        await page.set_content(f'<html><body style="margin:0"><div style="width:{width}px">{still}</div></body></html>')
        await page.locator("svg").evaluate("s => {s.style.width='100%';s.style.height='auto'}")
        await page.locator("svg").screenshot(path=str(OUTPUT / f"{stem}-{width}-still.png"))
    finally:
        await page.close()


async def check_player(browser, stem, lang, width, preference, base):
    context = await browser.new_context(
        viewport={"width": width, "height": 650}, reduced_motion=preference
    )
    page = await context.new_page()
    try:
        alt = "示意：擴散策略處理動作序列" if lang == "zh" else "Diffusion Policy action sequence"
        src = f"{base}/docs/assets/concept-animations/{stem}-motion.svg"
        await page.set_content(
            f'<html><head><meta charset="utf-8"></head><body style="margin:0;padding:8px">'
            f'<img src="{src}" alt="{alt}" style="width:100%;max-width:640px"></body></html>'
        )
        await page.add_script_tag(path=str(PLAYER))
        button = page.locator(".concept-motion-toggle")
        image = page.locator(".concept-motion-player img")
        assert await button.count() == 1
        paused = preference == "reduce"
        expected = "-still.svg" if paused else "-motion.svg"
        assert (await image.get_attribute("src")).endswith(expected)
        assert await image.get_attribute("alt") == alt
        label = await button.get_attribute("aria-label")
        assert label and (
            (("播放" if paused else "暫停") in label)
            if lang == "zh" else (("Play" if paused else "Pause") in label)
        )
        box = await image.bounding_box()
        assert box and box["x"] >= 0 and box["x"] + box["width"] <= width + 1
        await page.screenshot(
            path=str(OUTPUT / f"player-{stem}-{lang}-{width}-{preference}.png"),
            full_page=True,
        )
        await button.focus()
        for key in ("Enter", "Space"):
            await page.keyboard.press(key)
            paused = not paused
            assert (await image.get_attribute("src")).endswith(
                "-still.svg" if paused else "-motion.svg"
            ), (stem, lang, key)
    finally:
        await context.close()


async def check_preference_change(browser, stem, base):
    context = await browser.new_context(
        viewport={"width": 360, "height": 580}, reduced_motion="no-preference"
    )
    page = await context.new_page()
    try:
        src = f"{base}/docs/assets/concept-animations/{stem}-motion.svg"
        await page.set_content(f'<img src="{src}" alt="test">')
        await page.add_script_tag(path=str(PLAYER))
        image = page.locator(".concept-motion-player img")
        assert (await image.get_attribute("src")).endswith("-motion.svg")
        for preference, suffix in (("reduce", "-still.svg"), ("no-preference", "-motion.svg")):
            await page.emulate_media(reduced_motion=preference)
            await page.wait_for_function(
                """suffix => document.querySelector('.concept-motion-player img')
                    ?.getAttribute('src')?.endsWith(suffix)""",
                arg=suffix,
                timeout=5000,
            )
    finally:
        await context.close()


async def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for stem in STEMS:
        validate_sources(stem)
    server = ThreadingHTTPServer(
        ("127.0.0.1", 0), partial(SimpleHTTPRequestHandler, directory=str(ROOT))
    )
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{server.server_port}"
    try:
        async with async_playwright() as playwright:
            executable = os.getenv("CHROMIUM_EXECUTABLE", "/usr/bin/chromium")
            browser = await playwright.chromium.launch(
                headless=True, executable_path=executable if Path(executable).exists() else None,
                args=["--no-sandbox"],
            )
            try:
                for stem in STEMS:
                    for width in WIDTHS:
                        await check_svg(browser, stem, width)
                    for lang in ("en", "zh"):
                        for width in (320, 720):
                            for pref in ("reduce", "no-preference"):
                                await check_player(browser, stem, lang, width, pref, base)
                    await check_preference_change(browser, stem, base)
            finally:
                await browser.close()
    finally:
        server.shutdown()
    print(f"PASS: {len(STEMS) * len(WIDTHS) * (len(TIMES) + 1)} SVG frames, "
          f"{len(STEMS) * 2 * 2 * 2} bilingual player cases, {len(STEMS)} media-change cases")


if __name__ == "__main__":
    asyncio.run(main())
