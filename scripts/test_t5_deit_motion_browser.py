#!/usr/bin/env python3
"""Chromium integration QA for bilingual T5 / DeiT SVG motion and GitHub fallbacks.

Uses Playwright's local route.fulfill: no web server or external network.
"""
from __future__ import annotations

import os
from pathlib import Path
import re
from xml.etree import ElementTree as ET
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
ASSETS = DOCS / "assets" / "concept-animations"
CASES = {
    "t5-span-corruption": "theory/models/transformer/architecture-families/t5/index",
    "deit-dual-head-distillation": "theory/models/transformer/vision-transformer/deit/index",
}


def page_img(page: Path, stem: str):
    content = page.read_text(encoding="utf-8")
    image = next((m.group(0) for m in re.finditer(r"<img\b[^>]+>", content) if stem in m.group(0)), "")
    assert image, f"missing embedded fallback: {page}"
    attrs = {}
    for name in ("src", "data-motion-src", "data-still-src", "alt"):
        match = re.search(rf'\b{name}="([^"]+)"', image)
        assert match, f"{page}: missing {name}"
        attrs[name] = match.group(1)
    for key, suffix in (("src", "still"), ("data-motion-src", "motion"), ("data-still-src", "still")):
        target = (page.parent / attrs[key]).resolve()
        expect = (ASSETS / f"{stem}-{suffix}.svg").resolve()
        assert target == expect, f"invalid {key} link: {page}: {target} != {expect}"
    return attrs


def main():
    for stem in CASES:
        for suffix in ("motion", "still"):
            svg = ASSETS / f"{stem}-{suffix}.svg"
            tree = ET.parse(svg)
            root = tree.getroot()
            assert root.get("viewBox") == "0 0 640 360"
            animations = [
                x for x in root.iter()
                if x.tag.split("}")[-1] in ("animate", "animateMotion")
            ]
            assert bool(animations) == (suffix == "motion")
            assert all(x.get("repeatCount") == "indefinite" for x in animations)
            assert not any(
                x.tag.split("}")[-1] in ("script", "image", "foreignObject")
                for x in root.iter()
            )
    js = (DOCS / "javascripts" / "concept-motion.js").read_text(encoding="utf-8")
    css = (DOCS / "stylesheets" / "concept-motion.css").read_text(encoding="utf-8")
    screenshot_dir = ROOT / "artifacts" / "t5-deit-motion"
    screenshot_dir.mkdir(parents=True, exist_ok=True)
    count = 0
    with sync_playwright() as p:
        options = {"headless": True, "args": ["--no-sandbox"]}
        if os.environ.get("PLAYWRIGHT_CHROMIUM_EXECUTABLE"):
            options["executable_path"] = os.environ["PLAYWRIGHT_CHROMIUM_EXECUTABLE"]
        browser = p.chromium.launch(**options)
        for stem, page_stem in CASES.items():
            for language in ("en", "zh"):
                suffix = ".md" if language == "en" else ".zh-TW.md"
                attrs = page_img(DOCS / (page_stem + suffix), stem)
                for width in (320, 1024):
                    for motion in ("no-preference", "reduce"):
                        page = browser.new_page(
                            viewport={"width": width, "height": 520}, reduced_motion=motion
                        )
                        still = f"concept-animations/{stem}-still.svg"
                        animated = f"concept-animations/{stem}-motion.svg"

                        def serve(route):
                            name = route.request.url.split("/")[-1].split("?")[0]
                            assert name in (f"{stem}-motion.svg", f"{stem}-still.svg")
                            route.fulfill(
                                status=200,
                                content_type="image/svg+xml",
                                body=(ASSETS / name).read_bytes(),
                            )

                        page.route("**/concept-animations/*.svg", serve)
                        html = (
                            '<!doctype html><html><head><base href="https://example.test/">'
                            f'<style>body{{margin:0;padding:12px;font:16px Arial}}{css}</style>'
                            '</head><body><main>'
                            f'<img src="{still}" data-motion-src="{animated}" '
                            f'data-still-src="{still}" alt="{attrs["alt"]}">'
                            f'</main><script>{js}</script></body></html>'
                        )
                        page.set_content(html)
                        page.wait_for_timeout(250)
                        host = page.locator(".concept-motion-player")
                        image = host.locator("img")
                        toggle = host.locator("button")
                        assert host.count() == 1 and toggle.count() == 1
                        expect = still if motion == "reduce" else animated
                        assert image.get_attribute("src") == expect
                        assert image.evaluate("img => img.complete && img.naturalWidth > 0")
                        assert host.get_attribute("tabindex") == "0"
                        assert host.get_attribute("role") == "region"
                        toggle.click()
                        assert image.get_attribute("src") != expect
                        toggle.focus()
                        page.keyboard.press("Enter")
                        assert image.get_attribute("src") == expect
                        page.keyboard.press("Space")
                        assert image.get_attribute("src") != expect
                        if width == 320:
                            assert host.evaluate("x => x.scrollWidth > x.clientWidth")
                            host.focus()
                            page.keyboard.press("ArrowRight")
                            page.wait_for_timeout(250)
                            assert host.evaluate("x => x.scrollLeft > 0")
                        if language == "en" and motion == "no-preference":
                            page.screenshot(
                                path=str(screenshot_dir / f"{stem}-{width}.png")
                            )
                        count += 1
                        page.close()
        browser.close()
    print(
        f"T5/DeiT browser tests passed: {count}/16 "
        "(SVG decode, bilingual markup, reduced motion, Play/Pause, Enter, Space, mobile scroll)"
    )


if __name__ == "__main__":
    main()
