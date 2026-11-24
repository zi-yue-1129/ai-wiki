"""Chromium QA for schematic cliff-walking exploration and control targets."""
from __future__ import annotations
import os
from pathlib import Path
from xml.etree import ElementTree as ET
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "docs/assets/concept-animations"
OUT = ROOT / "artifacts/cliff-walking"
SVG_NS = "{http://www.w3.org/2000/svg}"

def main() -> None:
    motion = ASSETS / "cliff-walking-motion.svg"
    still = ASSETS / "cliff-walking-still.svg"
    for svg in (motion, still):
        root = ET.parse(svg).getroot()
        assert root.attrib["viewBox"] == "0 0 440 548"
        for el in root.iter():
            tag = el.tag.split("}")[-1]
            assert tag not in {"script", "image", "foreignObject", "iframe"}
            for k, v in el.attrib.items():
                assert not k.split("}")[-1].startswith("on")
                assert not v.startswith(("data:", "javascript:", "http:", "https:"))
    animated_root = ET.parse(motion).getroot()
    assert len(animated_root.findall(".//" + SVG_NS + "animate")) >= 7
    assert len(animated_root.findall(".//" + SVG_NS + "animateMotion")) >= 2
    static_root = ET.parse(still).getroot()
    assert not static_root.findall(".//" + SVG_NS + "animate")
    assert not static_root.findall(".//" + SVG_NS + "animateMotion")
    assert all(static_root.find(".//*[@id='" + k + "']") is not None
               for k in ("q-route", "s-route", "slip-arrow"))
    assert animated_root.find(".//*[@id='q-route']").attrib["d"] != animated_root.find(".//*[@id='s-route']").attrib["d"]
    for topic in ("q-learning", "sarsa"):
        chapter = ROOT / "docs/theory/paradigms/reinforcement-learning/value-based-methods" / topic
        for locale in ("index.md", "index.zh-TW.md"):
            text = (chapter / locale).read_text()
            assert "cliff-walking-motion.svg" in text and "cliff-walking-still.svg" in text
            assert "Sutton" in text
    OUT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        launch = {"headless": True, "args": ["--no-sandbox"]}
        if os.environ.get("CHROMIUM_EXECUTABLE"):
            launch["executable_path"] = os.environ["CHROMIUM_EXECUTABLE"]
        browser = p.chromium.launch(**launch)
        for width in (320, 360, 720, 1024):
            for sec in (.4, 2.4, 4.7, 6.7, 9.4):
                page = browser.new_page(viewport={"width": width, "height": max(820, 2*width)})
                page.set_content('<style>body{margin:0}svg{display:block;width:100%;height:auto}</style>' + motion.read_text())
                page.locator("svg").evaluate("(el,t)=>{el.pauseAnimations();el.setCurrentTime(t)}", sec)
                bounds = page.locator("svg text").evaluate_all(
                    "els=>els.map(e=>{const b=e.getBBox();return [b.x,b.y,b.width,b.height]})")
                assert all(x >= -.5 and y >= -.5 and x+w <= 440.5 and y+h <= 548.5
                           for x,y,w,h in bounds), (width,sec)
                assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
                if sec == .4:
                    assert float(page.locator("#q-focus").evaluate("e=>getComputedStyle(e).opacity")) > .8
                if sec == 4.7:
                    assert float(page.locator("#slip-focus").evaluate("e=>getComputedStyle(e).opacity")) > .8
                if sec == 9.4:
                    assert float(page.locator("#s-focus").evaluate("e=>getComputedStyle(e).opacity")) > .8
                page.locator("svg").screenshot(path=str(OUT / f"motion-{width}-{str(sec).replace('.', '_')}.png"))
                page.close()
            page = browser.new_page(viewport={"width": width, "height": max(820, 2*width)})
            page.set_content('<style>body{margin:0}svg{display:block;width:100%;height:auto}</style>' + still.read_text())
            assert page.locator("#q-route").is_visible() and page.locator("#s-route").is_visible()
            assert page.locator("#slip-arrow").count() == 1
            assert page.locator("#slip-arrow").evaluate("e => e.getBBox().height > 25")
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.locator("svg").screenshot(path=str(OUT / f"still-{width}.png"))
            page.close()

        player = (ROOT / "docs/javascripts/concept-motion.js").read_text()
        host = "https://local.invalid/concept-animations/"
        for lang_alt in ("Schematic cliff walking paths", "懸崖行走探索風險示意"):
            for mode in ("no-preference", "reduce"):
                cx = browser.new_context(reduced_motion=mode)
                pg = cx.new_page()
                pg.route(host + "**", lambda route: route.fulfill(
                    body=motion.read_text() if "-motion.svg" in route.request.url else still.read_text(),
                    content_type="image/svg+xml"))
                pg.set_content(
                    f'<img alt="{lang_alt}" src="{host}cliff-walking-still.svg" '
                    f'data-motion-src="{host}cliff-walking-motion.svg" '
                    f'data-still-src="{host}cliff-walking-still.svg">')
                assert "-still.svg" in pg.locator("img").get_attribute("src")
                pg.add_script_tag(content=player)
                button = pg.locator(".concept-motion-toggle")
                button.wait_for(state="visible", timeout=7000)
                assert ("-still.svg" if mode == "reduce" else "-motion.svg") in pg.locator("img").get_attribute("src")
                button.focus()
                pg.keyboard.press("Enter")
                assert ("-motion.svg" if mode == "reduce" else "-still.svg") in pg.locator("img").get_attribute("src")
                button.focus()
                pg.keyboard.press("Space")
                assert ("-still.svg" if mode == "reduce" else "-motion.svg") in pg.locator("img").get_attribute("src")
                cx.close()
        browser.close()
    print("PASS: 24 visual renders, two distinct paths, risk phase, bilingual keyboard player, reduced-motion fallback")

if __name__ == "__main__":
    main()
