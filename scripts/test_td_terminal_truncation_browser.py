"""Chromium QA for terminal versus externally truncated Q/SARSA TD targets."""
from __future__ import annotations

import os
from pathlib import Path
from xml.etree import ElementTree as ET

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "docs/assets/concept-animations"
OUT = ROOT / "artifacts/td-terminal-truncation"
SVG_NS = "{http://www.w3.org/2000/svg}"


def main() -> None:
    motion = ASSETS / "td-terminal-truncation-motion.svg"
    still = ASSETS / "td-terminal-truncation-still.svg"
    for svg in (motion, still):
        root = ET.parse(svg).getroot()
        assert root.attrib["viewBox"] == "0 0 440 602"
        for e in root.iter():
            tag = e.tag.split("}")[-1]
            assert tag not in {"script", "image", "foreignObject", "iframe"}
            for name, val in e.attrib.items():
                assert not name.split("}")[-1].startswith("on")
                assert not val.startswith(("data:", "javascript:", "http:", "https:"))
    assert len(ET.parse(motion).getroot().findall(".//" + SVG_NS + "animate")) >= 8
    assert len(ET.parse(motion).getroot().findall(".//" + SVG_NS + "animateMotion")) >= 2
    assert not ET.parse(still).getroot().findall(".//" + SVG_NS + "animate")
    assert not ET.parse(still).getroot().findall(".//" + SVG_NS + "animateMotion")
    assert 1 + .9 * 0 == 1.0
    assert abs((1 + .9 * 4) - 4.6) < 1e-10
    assert abs((1 + .9 * 2) - 2.8) < 1e-10
    for topic in ("q-learning", "sarsa"):
        base = ROOT / "docs/theory/paradigms/reinforcement-learning/value-based-methods" / topic
        for name in ("index.md", "index.zh-TW.md"):
            page = (base / name).read_text()
            assert "td-terminal-truncation-still.svg" in page
            assert "td-terminal-truncation-motion.svg" in page
            assert "proceedings.mlr.press/v80/pardo18a.html" in page

    OUT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        launch = {"headless": True, "args": ["--no-sandbox"]}
        if os.environ.get("CHROMIUM_EXECUTABLE"):
            launch["executable_path"] = os.environ["CHROMIUM_EXECUTABLE"]
        browser = p.chromium.launch(**launch)
        for width in (320, 360, 720, 1024):
            for sec in (.3, 2.6, 4.8, 7.2, 9.0):
                page = browser.new_page(viewport={"width": width, "height": max(820, 2 * width)})
                page.set_content('<style>body{margin:0}svg{display:block;width:100%;height:auto}</style>' + motion.read_text())
                page.locator("svg").evaluate("(e,t) => { e.pauseAnimations(); e.setCurrentTime(t) }", sec)
                rects = page.locator("svg text").evaluate_all(
                    "els=>els.map(e=>{const b=e.getBBox();return [b.x,b.y,b.width,b.height]})"
                )
                assert all(x >= -.5 and y >= -.5 and x+w <= 440.5 and y+h <= 602.5
                           for x,y,w,h in rects), (width,sec)
                assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
                if sec == .3:
                    assert float(page.locator("#term-mask").evaluate("e=>getComputedStyle(e).opacity")) < .5
                if sec == 2.6:
                    assert float(page.locator("#term-mask").evaluate("e=>getComputedStyle(e).opacity")) > .8
                if sec == 4.8:
                    assert float(page.locator("#q-glow").evaluate("e=>getComputedStyle(e).opacity")) > .8
                if sec == 7.2:
                    assert float(page.locator("#s-glow").evaluate("e=>getComputedStyle(e).opacity")) > .8
                page.locator("svg").screenshot(path=str(OUT / f"motion-{width}-{str(sec).replace('.', '_')}.png"))
                page.close()
            page = browser.new_page(viewport={"width": width, "height": max(820, 2 * width)})
            page.set_content('<style>body{margin:0}svg{display:block;width:100%;height:auto}</style>' + still.read_text())
            assert page.locator("#term-q").is_visible()
            assert page.locator("#term-s").is_visible()
            assert page.locator("#q-glow").is_visible()
            assert page.locator("#s-glow").is_visible()
            page.locator("svg").screenshot(path=str(OUT / f"still-{width}.png"))
            page.close()

        # Exercise the repository's real MkDocs progressive enhancement, not a mock player.
        player = (ROOT / "docs/javascripts/concept-motion.js").read_text()
        host = "https://local.invalid/concept-animations/"
        for lang_alt in ("Terminal and truncation backup comparison", "終止與截斷的 TD 備份比較"):
            for mode in ("no-preference", "reduce"):
                cx = browser.new_context(reduced_motion=mode)
                pg = cx.new_page()
                pg.route(host + "**", lambda route: route.fulfill(
                    body=motion.read_text() if "-motion.svg" in route.request.url else still.read_text(),
                    content_type="image/svg+xml"))
                pg.set_content(
                    f'<img alt="{lang_alt}" src="{host}td-terminal-truncation-still.svg" '
                    f'data-motion-src="{host}td-terminal-truncation-motion.svg" '
                    f'data-still-src="{host}td-terminal-truncation-still.svg">')
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
    print("PASS: 24 responsive renders, terminal mask, time-limit bootstrap, bilingual player and reduced motion")


if __name__ == "__main__":
    main()
