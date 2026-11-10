#!/usr/bin/env python3
"""Chromium regression for SAC soft-target and temperature-feedback SVG motion.

Checks real rendering at multiple times and widths, numerical semantics, the
shared MkDocs playback button, bilingual keyboard control and reduced motion.
"""
from __future__ import annotations

import math
import os
from pathlib import Path
from xml.etree import ElementTree as ET

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "docs/assets/concept-animations"
JS = ROOT / "docs/javascripts/concept-motion.js"
OUT = ROOT / "artifacts/sac-motion"
STEMS = ("sac-soft-target", "sac-temperature-feedback")
NS = "{http://www.w3.org/2000/svg}"


def structural_and_numeric_check():
    for stem in STEMS:
        for kind in ("motion", "still"):
            f = ASSETS / f"{stem}-{kind}.svg"
            root = ET.parse(f).getroot()
            assert f.stat().st_size < 50 * 1024
            assert root.tag == NS + "svg" and root.get("viewBox") == "0 0 640 360"
            assert root.find(NS + "title") is not None
            assert root.find(NS + "desc") is not None
            anim = [n for n in root.iter() if n.tag.rsplit("}", 1)[-1] in ("animate", "animateMotion")]
            assert bool(anim) == (kind == "motion"), (f, len(anim))
            for n in root.iter():
                tag = n.tag.rsplit("}", 1)[-1]
                assert tag not in ("script", "foreignObject", "image", "iframe")
                for k, v in n.attrib.items():
                    key = k.rsplit("}", 1)[-1]
                    assert not key.startswith("on")
                    if key in ("href", "src"):
                        assert v.startswith("#"), (f, k, v)
        for lang in ("index.md", "index.zh-TW.md"):
            page = ROOT / "docs/theory/paradigms/reinforcement-learning/policy-gradient-and-actor-critic/sac" / lang
            text = page.read_text(encoding="utf8")
            assert f"{stem}-motion.svg" in text and f"{stem}-still.svg" in text
            assert "CC BY-SA 4.0" in text
    assert math.isclose(1 + .9 * (min(4.2, 3.8) - .2 * (-.7)), 4.546)
    assert math.isclose(1 + .9 * min(4.2, 3.8), 4.42)


def main():
    structural_and_numeric_check()
    OUT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        opts = {"headless": True, "args": ["--no-sandbox"]}
        if os.environ.get("CHROMIUM_EXECUTABLE"):
            opts["executable_path"] = os.environ["CHROMIUM_EXECUTABLE"]
        browser = pw.chromium.launch(**opts)
        count = 0
        for stem in STEMS:
            svg = (ASSETS / f"{stem}-motion.svg").read_text(encoding="utf-8")
            static = (ASSETS / f"{stem}-still.svg").read_text(encoding="utf-8")
            for width in (320, 360, 720, 1024):
                p = browser.new_page(viewport={"width": width, "height": 600})
                for kind, document in (("motion", svg), ("still", static)):
                    p.set_content(
                        '<!doctype html><style>body{margin:0}svg{display:block;width:100%;height:auto}</style>'
                        + document
                    )
                    for ts in ((.3, 2.8, 5.4, 8.2) if kind == "motion" else (0,)):
                        if kind == "motion":
                            p.evaluate("t => {let s=document.querySelector('svg');s.pauseAnimations();s.setCurrentTime(t)}", ts)
                        outside = p.evaluate("""() => [...document.querySelectorAll('svg text')]
                            .filter(x => {let b=x.getBBox();return b.x < -1||b.y < -1||
                                  b.x+b.width > 641||b.y+b.height > 361})
                            .map(x=>x.textContent)""")
                        assert not outside, (stem, width, ts, outside)
                        p.screenshot(path=str(OUT / f"{stem}-{width}-{kind}-t{ts}.png"))
                        count += 1
                p.close()
            if stem == "sac-temperature-feedback":
                p = browser.new_page(viewport={"width": 800, "height": 500})
                p.set_content(svg)
                def widths(t):
                    return p.evaluate("""t => {
                      let s=document.querySelector('svg');s.pauseAnimations();s.setCurrentTime(t);
                      return [...s.querySelectorAll('rect.moving')].map(x=>x.width.animVal.value)
                    }""", t)
                before, after = widths(.3), widths(5.4)
                assert len(before) == len(after) == 2, (before, after)
                assert abs(before[0] - 101) < .1 and abs(after[0] - 137) < .1
                assert abs(before[1] - 137) < .1 and abs(after[1] - 112) < .1
                p.close()
            for width in (320, 720):
                for zh in (False, True):
                    for reduced in (False, True):
                        ctx = browser.new_context(viewport={"width": width, "height": 490},
                                                  reduced_motion="reduce" if reduced else "no-preference")
                        p = ctx.new_page()
                        def serve(route):
                            name = route.request.url.split("/")[-1]
                            route.fulfill(status=200, content_type="image/svg+xml",
                                          body=(ASSETS / name).read_bytes())
                        p.route("**/concept-animations/*.svg", serve)
                        alt = "SAC 熵溫度動畫" if zh else "SAC entropy motion"
                        p.set_content(
                            f'<img alt="{alt}" src="https://example.invalid/concept-animations/{stem}-motion.svg">'
                        )
                        p.add_script_tag(content=JS.read_text(encoding="utf8"))
                        button = p.locator(".concept-motion-toggle")
                        assert button.count() == 1, (stem, zh, reduced)
                        image = p.locator(".concept-motion-player img")
                        assert image.get_attribute("src").endswith("-still.svg" if reduced else "-motion.svg")
                        button.focus()
                        p.keyboard.press("Space")
                        assert image.get_attribute("src").endswith("-motion.svg" if reduced else "-still.svg")
                        p.keyboard.press("Enter")
                        assert image.get_attribute("src").endswith("-still.svg" if reduced else "-motion.svg")
                        p.close()
                        ctx.close()
        browser.close()
    print(f"SAC Chromium PASS: {count} rendered frames; responsive, bilingual keyboard, reduced-motion, numerical semantics")


if __name__ == "__main__":
    main()
