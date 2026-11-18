#!/usr/bin/env python3
"""Verify two instructional SVG pairs, responsive rendering and bilingual controls in Chromium."""
from pathlib import Path
from xml.etree import ElementTree as ET
from playwright.sync_api import sync_playwright

BASE = Path("docs/assets/concept-animations")
PAIRS = ("svi-minibatch-global", "soap-eigenbasis-adam")
JS = Path("docs/javascripts/concept-motion.js").read_text(encoding="utf-8")
for stem in PAIRS:
    for variant in ("motion", "still"):
        path = BASE / f"{stem}-{variant}.svg"
        root = ET.parse(path).getroot()
        assert root.get("viewBox") == "0 0 640 360", path
        content = path.read_text(encoding="utf-8")
        assert ("<animate " in content) == (variant == "motion"), path
        assert len(content.encode("utf-8")) < 50000
        assert "<script" not in content and "<foreignObject" not in content
    for directory, basename in (
        ("docs/theory/paradigms/probabilistic/variational-inference", "stochastic-variational-inference"),
        ("docs/theory/optimization/adaptive", "soap"),
    ):
        if (stem.startswith("svi") != (basename.startswith("stochastic"))):
            continue
        for lang in (".md", ".zh-TW.md"):
            body = (Path(directory) / (basename + lang)).read_text(encoding="utf-8")
            assert stem + "-still.svg" in body and stem + "-motion.svg" in body

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
    for stem in PAIRS:
        svg = (BASE / f"{stem}-motion.svg").read_text(encoding="utf-8")
        for width in (320, 360, 720, 1024):
            page = browser.new_page(viewport={"width": width, "height": 600})
            page.set_content(svg, wait_until="load")
            for t in (0, 2.5, 5, 7.5, 10):
                page.locator("svg").evaluate("(s,t)=>s.setCurrentTime(t)", t)
                assert page.locator("svg title").count() == 1
                rects = page.locator("svg text").evaluate_all(
                    "nodes=>nodes.map(n=>{let b=n.getBBox();return [b.x,b.y,b.width,b.height]})"
                )
                assert all(-1 <= x and -1 <= y and x + w <= 641 and y + h <= 361
                           for x, y, w, h in rects), (stem, width, t)
            page.close()
        for lang in ("en", "zh"):
            for reduced in (False, True):
                page = browser.new_page(
                    viewport={"width": 320, "height": 600},
                    reduced_motion="reduce" if reduced else "no-preference",
                )
                still = f"https://example.test/assets/concept-animations/{stem}-still.svg"
                motion = f"https://example.test/assets/concept-animations/{stem}-motion.svg"
                def serve(route):
                    filename = route.request.url.split("/")[-1]
                    route.fulfill(
                        status=200, content_type="image/svg+xml",
                        body=(BASE / filename).read_text(encoding="utf-8"),
                    )
                page.route("**/assets/concept-animations/*.svg", serve)
                alt = "示意動畫" if lang == "zh" else "Instructional diagram"
                page.set_content(
                    f'<div tabindex="0" style="width:300px;max-width:100%;overflow-x:auto">'
                    f'<div style="width:640px"><img src="{still}" data-motion-src="{motion}"'
                    f' alt="{alt}" width="640" height="360"></div></div>'
                )
                page.add_script_tag(content=JS)
                button = page.locator(".concept-motion-toggle")
                assert button.count() == 1, (stem, lang, reduced)
                assert ("-still.svg" if reduced else "-motion.svg") in page.locator("img").get_attribute("src")
                button.focus()
                page.keyboard.press("Enter")
                assert ("-motion.svg" if reduced else "-still.svg") in page.locator("img").get_attribute("src")
                page.keyboard.press("Space")
                assert ("-still.svg" if reduced else "-motion.svg") in page.locator("img").get_attribute("src")
                assert page.locator('div[tabindex="0"]').evaluate("(e)=>e.scrollWidth>e.clientWidth")
                page.close()
    browser.close()
print("PASS: 4 SVG files, 40 Chromium time/viewport states, 8 bilingual/reduced-motion player cases")
