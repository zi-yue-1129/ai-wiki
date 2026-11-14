#!/usr/bin/env python3
"""Chromium smoke tests for video SVG motion and accessible static-first enhancement."""
from pathlib import Path
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial
from threading import Thread
from playwright.sync_api import sync_playwright
import os

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
ASSETS = DOCS / "assets" / "concept-animations"
OUTPUT = ROOT / "artifacts" / "video-motion"
OUTPUT.mkdir(parents=True, exist_ok=True)
HANDLER = partial(SimpleHTTPRequestHandler, directory=str(DOCS))
server = ThreadingHTTPServer(("127.0.0.1", 0), HANDLER)
Thread(target=server.serve_forever, daemon=True).start()
base = f"http://127.0.0.1:{server.server_port}/assets/concept-animations/"
cases = (("vivit-factorised-attention", "Space"), ("i3d-filter-inflation", "Enter"))
try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        for stem, key in cases:
            for width in (320, 360, 800, 1024):
                for lang, reduce in (("en", False), ("zh", True)):
                    ctx = browser.new_context(viewport={"width": width, "height": 600},
                                              reduced_motion="reduce" if reduce else "no-preference")
                    page = ctx.new_page()
                    alt = "示意動畫" if lang == "zh" else "Schematic animation"
                    page.set_content(f'<img alt="{alt}" src="{base}{stem}-still.svg">')
                    page.add_style_tag(path=str(DOCS / "stylesheets/concept-motion.css"))
                    page.add_script_tag(path=str(DOCS / "javascripts/concept-motion.js"))
                    toggle = page.locator(".concept-motion-toggle")
                    assert toggle.count() == 1, (stem, width, lang)
                    image = page.locator(".concept-motion-player img")
                    assert "-still.svg" in image.get_attribute("src") if reduce else "-motion.svg" in image.get_attribute("src")
                    assert page.locator(".concept-motion-wide").count() == 1
                    player = page.locator(".concept-motion-wide")
                    metrics = player.evaluate("(e) => [e.scrollWidth, e.clientWidth, e.tabIndex]")
                    assert metrics[2] == 0
                    if width <= 360:
                        assert metrics[0] > metrics[1], (stem, width, metrics)
                    toggle.focus()
                    toggle.press(key)
                    assert "-motion.svg" in image.get_attribute("src") if reduce else "-still.svg" in image.get_attribute("src")
                    toggle.click()
                    assert "-still.svg" in image.get_attribute("src") if reduce else "-motion.svg" in image.get_attribute("src")
                    if width in (320, 800):
                        page.screenshot(path=str(OUTPUT / f"{stem}-{lang}-{width}.png"),
                                        animations="allow")
                    ctx.close()
        browser.close()
finally:
    server.shutdown()
print("Chromium: 16 bilingual, keyboard, reduced-motion, responsive-control checks passed")
