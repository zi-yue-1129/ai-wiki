#!/usr/bin/env python3
"""Browser rendering and bilingual player regression for AlphaZero SVG processes."""
from __future__ import annotations
import os
from pathlib import Path
from xml.etree import ElementTree as ET
from playwright.sync_api import sync_playwright

ROOT = Path.cwd()
ASSETS = ROOT / "docs/assets/concept-animations"
OUTPUT = ROOT / "artifacts/alphazero-motion"
STEMS = ("alphazero-policy-target", "alphazero-selfplay-labels", "alphazero-puct-select", "alphazero-value-backup")
WIDTHS = (320, 360, 720, 1024)
TIMES = (0.5, 3.4, 6.8, 10.2)

def exercise_animation(browser, stem, width):
    context = browser.new_context(viewport={"width": width, "height": max(400, int(width*.7))})
    for suffix in ("motion", "still"):
        svg = (ASSETS / f"{stem}-{suffix}.svg").read_text(encoding="utf-8")
        root = ET.fromstring(svg)
        assert root.attrib["viewBox"] == "0 0 640 360"
        ns = "{http://www.w3.org/2000/svg}"
        assert root.find(ns+"title") is not None and root.find(ns+"desc") is not None
        svg = svg.replace("<svg ", '<svg style="width:100%;height:auto;display:block" ', 1)
        page = context.new_page()
        page.set_content('<html><body style="margin:0">'+svg+"</body></html>")
        for t in (TIMES if suffix == "motion" else (None,)):
            if t is not None:
                page.evaluate('(t) => document.querySelector("svg").setCurrentTime(t)', t)
            box = page.locator("svg").bounding_box()
            assert box and abs(box["width"] - width) < 2
            overflow = page.evaluate("""() => {
              const r = document.querySelector('svg').getBoundingClientRect();
              return [...document.querySelectorAll('svg text')].filter(e => {
                const b = e.getBoundingClientRect();
                return b.width > 0 && (b.left < r.left-1 || b.top < r.top-1 || b.right > r.right+1 || b.bottom > r.bottom+1);
              }).map(e => e.textContent); }""")
            assert not overflow, f"{stem}/{width}/{t}: {overflow}"
            label = "still" if t is None else str(t).replace(".","p")
            page.locator("svg").screenshot(path=str(OUTPUT / f"{stem}-{width}-{label}.png"))
        page.close()
    context.close()

def exercise_player(browser, stem, lang, reduced):
    context = browser.new_context(viewport={"width": 360, "height": 600},
                                  reduced_motion="reduce" if reduced else "no-preference")
    page = context.new_page()
    def serve(route):
        filename = route.request.url.rsplit("/",1)[-1]
        route.fulfill(status=200, body=(ASSETS/filename).read_text(encoding="utf-8"),
                      content_type="image/svg+xml")
    page.route("**/concept-animations/*.svg", serve)
    alt = "自我對弈概念動畫" if lang == "zh" else "AlphaZero teaching animation"
    src = f"https://alphazero.invalid/concept-animations/{stem}-motion.svg"
    page.set_content(f'<html><body><img src="{src}" alt="{alt}" width="320"></body></html>')
    page.add_script_tag(content=(ROOT/"docs/javascripts/concept-motion.js").read_text(encoding="utf-8"))
    toggle = page.locator(".concept-motion-toggle")
    assert toggle.count() == 1
    img = page.locator("img")
    assert (img.get_attribute("src") or "").endswith("-still.svg" if reduced else "-motion.svg")
    toggle.focus()
    toggle.press("Enter")
    assert (img.get_attribute("src") or "").endswith("-motion.svg" if reduced else "-still.svg")
    toggle.press("Space")
    assert (img.get_attribute("src") or "").endswith("-still.svg" if reduced else "-motion.svg")
    toggle.click()
    assert (img.get_attribute("src") or "").endswith("-motion.svg" if reduced else "-still.svg")
    assert toggle.get_attribute("aria-label")
    page.close(); context.close()

def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        chromium = os.environ.get("CHROMIUM_BIN")
        browser = pw.chromium.launch(headless=True, executable_path=chromium or None,
                                     args=["--no-sandbox"])
        for stem in STEMS:
            for width in WIDTHS:
                exercise_animation(browser, stem, width)
            for lang in ("en", "zh"):
                for reduced in (False, True):
                    exercise_player(browser, stem, lang, reduced)
        browser.close()
    print("PASS: 80 responsive SVG screenshots; 16 bilingual keyboard/reduced-motion player checks")

if __name__ == "__main__":
    main()
