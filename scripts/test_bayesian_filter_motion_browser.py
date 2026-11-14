#!/usr/bin/env python3
"""Browser regressions for the Kalman / particle-filter bilingual motion assets.

Requires Playwright Chromium, installed by concept-animation-validation.yml.
Renders actual repository SVGs and the shared MkDocs concept-motion.js/CSS.
"""
from __future__ import annotations

import os
from pathlib import Path
import tempfile
from xml.etree import ElementTree as ET

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "docs/assets/concept-animations"
JS = (ROOT / "docs/javascripts/concept-motion.js").as_uri()
CSS = (ROOT / "docs/stylesheets/concept-motion.css").as_uri()
OUT = ROOT / "artifacts/bayesian-filter-motion"
OUT.mkdir(parents=True, exist_ok=True)

TOPICS = ("kalman-gain-fusion", "particle-weight-resampling")
NS = "{http://www.w3.org/2000/svg}"


def validate_assets() -> None:
    for stem in TOPICS:
        for suffix, must_animate in (("motion", True), ("still", False)):
            path = ASSETS / f"{stem}-{suffix}.svg"
            assert path.is_file(), path
            root = ET.parse(path).getroot()
            assert root.get("viewBox") == "0 0 640 360"
            assert root.find(NS + "title") is not None
            assert root.find(NS + "desc") is not None
            anims = [el for el in root.iter() if el.tag.split("}")[-1] == "animate"]
            assert bool(anims) is must_animate, path
            for el in anims:
                assert el.get("repeatCount") == "indefinite", path
                assert el.get("dur") == "12s", path
            for el in root.iter():
                assert el.tag.split("}")[-1] not in ("script", "foreignObject", "image")
                for key, value in el.attrib.items():
                    assert not key.split("}")[-1].startswith("on")
                    if key.endswith("href"):
                        assert not value.startswith(("http", "data:", "javascript:"))


def make_html(stem: str, lang: str) -> str:
    alt = ("卡爾曼量測修正過程" if stem.startswith("kalman") else "粒子濾波依概似重採樣") if lang == "zh" else (
        "Kalman gain-weighted measurement update" if stem.startswith("kalman") else "Particle filter weighted resampling"
    )
    return (
        '<!doctype html><html lang="' + lang + '"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<link rel="stylesheet" href="{CSS}"></head><body>'
        f'<article><p><img src="{(ASSETS / (stem + "-motion.svg")).as_uri()}" alt="{alt}"></p></article>'
        f'<script src="{JS}"></script></body></html>'
    )


def main() -> None:
    validate_assets()
    completed = 0
    with tempfile.TemporaryDirectory(prefix="aiwiki-browser-") as temp:
        folder = Path(temp)
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(
                headless=True, args=["--no-sandbox"],
                executable_path=os.getenv("CHROMIUM_PATH") or None
            )
            for stem in TOPICS:
                for lang in ("en", "zh"):
                    for width in (320, 360, 760, 1024):
                        for reduced in (False, True):
                            pagefile = folder / "demo.html"
                            pagefile.write_text(make_html(stem, lang), encoding="utf-8")
                            context = browser.new_context(
                                viewport={"width": width, "height": 620},
                                reduced_motion="reduce" if reduced else "no-preference",
                            )
                            page = context.new_page()
                            page.goto(pagefile.as_uri())
                            toggle = page.locator(".concept-motion-toggle")
                            toggle.wait_for(state="visible")
                            img = page.locator(".concept-motion-player img")
                            img.evaluate("(el) => el.decode()")
                            initial = img.get_attribute("src") or ""
                            assert initial.endswith("-still.svg" if reduced else "-motion.svg"), (stem, lang, width, reduced, initial)
                            assert img.evaluate("(el) => el.naturalWidth") == 640
                            assert (toggle.get_attribute("aria-label") or "").startswith(
                                "播放" if reduced and lang == "zh" else
                                "Play" if reduced else
                                "暫停" if lang == "zh" else "Pause"
                            ), (stem, lang, reduced, toggle.get_attribute("aria-label"))
                            # The keyboard-reachable figure and native control must work at all sizes.
                            assert page.locator(".concept-motion-player").get_attribute("tabindex") == "0"
                            if width <= 360:
                                assert page.locator(".concept-motion-player").evaluate(
                                    "(el) => el.scrollWidth > el.clientWidth"
                                ), (stem, width, "missing horizontal scroll")
                            toggle.focus()
                            toggle.press("Enter")
                            assert (img.get_attribute("src") or "").endswith("-motion.svg" if reduced else "-still.svg")
                            toggle.press("Space")
                            assert (img.get_attribute("src") or "").endswith("-still.svg" if reduced else "-motion.svg")
                            if width in (320, 760) and not reduced:
                                img.screenshot(path=str(OUT / f"{stem}-{lang}-{width}.png"))
                            completed += 1
                            context.close()
            # Inline SVG timelines must actually move, rather than merely contain XML tags.
            for stem in TOPICS:
                svg = (ASSETS / (stem + "-motion.svg")).read_text(encoding="utf-8")
                page = browser.new_page(viewport={"width": 760, "height": 430})
                page.set_content('<html><body>' + svg + '</body></html>')
                page.locator("svg").evaluate("(el) => el.setCurrentTime(0)")
                start = page.locator("svg").screenshot()
                page.locator("svg").evaluate("(el) => el.setCurrentTime(9)")
                end = page.locator("svg").screenshot()
                assert start != end, (stem, "animation frame did not change")
                page.close()
            browser.close()
    print(f"PASS: {completed} bilingual/responsive/reduced-motion control scenarios and 2 animated timelines")


if __name__ == "__main__":
    main()
