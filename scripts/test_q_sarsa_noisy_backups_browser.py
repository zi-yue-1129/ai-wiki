"""Browser and numerical regression for the Q-learning/SARSA noisy-backup illustration."""
from __future__ import annotations

import os
from pathlib import Path
from xml.etree import ElementTree as ET

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "docs/assets/concept-animations"
OUT = ROOT / "artifacts/q-sarsa-noisy-backups"
NS = "{http://www.w3.org/2000/svg}"


def run() -> None:
    motion = ASSETS / "q-sarsa-noisy-backups-motion.svg"
    still = ASSETS / "q-sarsa-noisy-backups-still.svg"
    for f in (motion, still):
        assert f.exists(), f
        root = ET.parse(f).getroot()
        assert root.get("viewBox") == "0 0 440 644"
        for e in root.iter():
            assert e.tag.split("}")[-1] not in ("script", "foreignObject", "iframe", "image")
            for k, v in e.attrib.items():
                key = k.split("}")[-1]
                assert not key.startswith("on")
                if key == "href":
                    assert not v.startswith(("http:", "https:", "data:", "javascript:"))
    assert len(ET.parse(motion).getroot().findall(".//" + NS + "animate")) >= 12
    assert not ET.parse(still).getroot().findall(".//" + NS + "animate")
    cases = [(5, 5), (5, 3), (3, 5), (3, 3)]
    assert sum(max(a, b) for a, b in cases) / 4 == 4.5
    assert sum(b for _, b in cases) / 4 == 4.0

    OUT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        opts = {"headless": True, "args": ["--no-sandbox"]}
        if os.environ.get("CHROMIUM_EXECUTABLE"):
            opts["executable_path"] = os.environ["CHROMIUM_EXECUTABLE"]
        browser = p.chromium.launch(**opts)
        for width in (320, 360, 720, 1024):
            for seconds, shown in ((0.2, 0), (1.9, 1), (4.05, 2), (6.2, 3), (9.0, 4)):
                page = browser.new_page(viewport={"width": width, "height": max(750, width * 2)})
                page.set_content('<style>body{margin:0}svg{display:block;width:100%;height:auto}</style>' + motion.read_text())
                page.locator("svg").evaluate("e => { e.pauseAnimations(); e.setCurrentTime(%s) }" % seconds)
                for i in range(1, 5):
                    q = float(page.locator(f"#case-{i}-max").evaluate("e => getComputedStyle(e).opacity"))
                    b = float(page.locator(f"#case-{i}-sample").evaluate("e => getComputedStyle(e).opacity"))
                    assert (q > .9) == (i <= shown), (width, seconds, i, q)
                    assert (b > .9) == (i <= shown), (width, seconds, i, b)
                visible_mean = float(page.locator("#mean-max").evaluate("e => getComputedStyle(e).opacity"))
                assert (visible_mean > .9) == (shown == 4)
                boxes = page.locator("svg text").evaluate_all("els => els.map(e => {const b = e.getBBox();return [b.x,b.y,b.width,b.height]})")
                assert all(x >= 0 and y >= 0 and x + w <= 440.5 and y + h <= 644.5 for x, y, w, h in boxes)
                assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
                page.locator("svg").screenshot(path=str(OUT / f"motion-{width}-{str(seconds).replace('.', '_')}.png"))
                page.close()
            page = browser.new_page(viewport={"width": width, "height": max(750, width * 2)})
            page.set_content('<style>body{margin:0}svg{display:block;width:100%;height:auto}</style>' + still.read_text())
            assert page.locator("#mean-max").is_visible()
            assert page.locator("#mean-sample").is_visible()
            page.locator("svg").screenshot(path=str(OUT / f"still-{width}.png"))
            page.close()
        browser.close()
    print("PASS: 24 responsive screenshots, four exhaustive noise cases, SMIL stages, safety and fallback")


if __name__ == "__main__":
    run()
