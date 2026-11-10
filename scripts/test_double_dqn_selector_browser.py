"""Chromium regression for DQN versus Double DQN selection/evaluation."""
from __future__ import annotations

import os
from pathlib import Path
from xml.etree import ElementTree as ET

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "docs/assets/concept-animations"
OUT = ROOT / "artifacts/double-dqn-selector"
NS = "{http://www.w3.org/2000/svg}"


def run() -> None:
    motion = ASSETS / "double-dqn-selector-motion.svg"
    still = ASSETS / "double-dqn-selector-still.svg"
    for svg in (motion, still):
        root = ET.parse(svg).getroot()
        assert root.get("viewBox") == "0 0 440 634"
        for node in root.iter():
            assert node.tag.split("}")[-1] not in ("script", "foreignObject", "iframe", "image")
            for key, value in node.attrib.items():
                key = key.split("}")[-1]
                assert not key.startswith("on")
                if key == "href":
                    assert not value.startswith(("http:", "https:", "data:", "javascript:"))
    assert len(ET.parse(motion).getroot().findall(".//" + NS + "animate")) >= 7
    assert not ET.parse(still).getroot().findall(".//" + NS + "animate")
    online = {"L": 6, "R": 5}
    target = {"L": 3, "R": 7}
    selected = max(online, key=online.get)
    assert selected == "L" and max(target, key=target.get) == "R"
    assert round(1 + .9 * max(target.values()), 2) == 7.3
    assert round(1 + .9 * target[selected], 2) == 3.7

    OUT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        options = {"headless": True, "args": ["--no-sandbox"]}
        if os.environ.get("CHROMIUM_EXECUTABLE"):
            options["executable_path"] = os.environ["CHROMIUM_EXECUTABLE"]
        browser = p.chromium.launch(**options)
        for width in (320, 360, 720, 1024):
            for seconds in (0.5, 2.4, 4.0, 6.3, 8.3):
                page = browser.new_page(viewport={"width": width, "height": max(750, width * 2)})
                page.set_content('<style>body{margin:0}svg{display:block;width:100%;height:auto}</style>' + motion.read_text())
                page.locator("svg").evaluate(f"e => {{ e.pauseAnimations(); e.setCurrentTime({seconds}) }}")
                def opacity(ident: str) -> float:
                    return float(page.locator("#" + ident).evaluate("e => getComputedStyle(e).opacity"))
                if seconds == 0.5:
                    assert opacity("online-choice") > opacity("target-greedy")
                    assert opacity("double-target") < .2
                if seconds == 4.0:
                    assert opacity("target-greedy") > .9 and opacity("dqn-target") > .9
                    assert opacity("double-target") < .2
                if seconds == 8.3:
                    assert opacity("target-evaluation") > .85 and opacity("double-target") > .9
                    assert opacity("target-greedy") < .2
                boxes = page.locator("svg text").evaluate_all(
                    "els => els.map(e => { const b=e.getBBox(); return [b.x,b.y,b.width,b.height] })")
                assert all(x >= 0 and y >= 0 and x+w <= 440.5 and y+h <= 634.5 for x,y,w,h in boxes)
                assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
                page.locator("svg").screenshot(path=str(OUT / f"motion-{width}-{str(seconds).replace('.', '_')}.png"))
                page.close()
            page = browser.new_page(viewport={"width": width, "height": max(750, width * 2)})
            page.set_content('<style>body{margin:0}svg{display:block;width:100%;height:auto}</style>' + still.read_text())
            assert page.locator("#dqn-target").is_visible()
            assert page.locator("#double-target").is_visible()
            page.locator("svg").screenshot(path=str(OUT / f"still-{width}.png"))
            page.close()

        player = ROOT / "docs/javascripts/concept-motion.js"
        assert player.exists()
        host = "https://local.invalid/concept-animations/"
        for alt in ("Online selects Left while target values Right higher", "線上網路選擇左動作，目標網路對右動作給予較高估計"):
            for mode in ("no-preference", "reduce"):
                context = browser.new_context(reduced_motion=mode)
                page = context.new_page()
                page.route(host + "**", lambda route: route.fulfill(
                    body=motion.read_text() if "-motion.svg" in route.request.url else still.read_text(),
                    content_type="image/svg+xml"))
                page.set_content(f'<img alt="{alt}" src="{host}double-dqn-selector-still.svg" data-motion-src="{host}double-dqn-selector-motion.svg" data-still-src="{host}double-dqn-selector-still.svg">')
                assert page.locator("img").get_attribute("src").endswith("-still.svg")
                page.add_script_tag(content=player.read_text())
                button = page.locator(".concept-motion-toggle")
                button.wait_for(state="visible", timeout=5000)
                assert ("-still.svg" if mode == "reduce" else "-motion.svg") in page.locator("img").get_attribute("src")
                button.focus()
                page.keyboard.press("Enter")
                assert ("-motion.svg" if mode == "reduce" else "-still.svg") in page.locator("img").get_attribute("src")
                button.focus()
                page.keyboard.press("Space")
                assert ("-still.svg" if mode == "reduce" else "-motion.svg") in page.locator("img").get_attribute("src")
                context.close()
        browser.close()
    print("PASS: Double DQN semantics, 24 screenshots, keyboard, reduced motion, static fallback")


if __name__ == "__main__":
    run()
