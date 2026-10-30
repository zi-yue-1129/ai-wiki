#!/usr/bin/env python3
"""Chromium regression checks for ZeRO sharding and Megatron tensor-parallel motion."""
from __future__ import annotations

import os
from pathlib import Path
from xml.etree import ElementTree as ET

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
ASSETS = DOCS / "assets" / "concept-animations"
OUT = ROOT / "distributed-motion-screenshots"
STEMS = {
    "zero-state-sharding": "zero",
    "megatron-column-row": "megatron-tensor-parallelism",
}
NS = "{http://www.w3.org/2000/svg}"


def structure():
    for stem, chapter in STEMS.items():
        for kind in ("motion", "still"):
            path = ASSETS / f"{stem}-{kind}.svg"
            assert path.stat().st_size < 50 * 1024, path
            root = ET.parse(path).getroot()
            assert root.tag == NS + "svg" and root.get("viewBox") == "0 0 640 360"
            assert root.find(NS + "title") is not None and root.find(NS + "desc") is not None
            animations = []
            for element in root.iter():
                tag = element.tag.split("}")[-1]
                assert tag not in {"script", "foreignObject", "iframe", "image"}
                assert not any(k.split("}")[-1].startswith("on") for k in element.attrib)
                assert not any(k.split("}")[-1] == "href" and
                               ("://" in v or v.startswith(("data:", "javascript:")))
                               for k, v in element.attrib.items())
                if tag in {"animate", "animateMotion", "animateTransform"}:
                    animations.append(element)
                    assert element.get("repeatCount") == "indefinite"
            assert bool(animations) == (kind == "motion"), path
        for suffix in (".md", ".zh-TW.md"):
            page = DOCS / "engineering" / "distributed-training" / (chapter + suffix)
            content = page.read_text(encoding="utf-8")
            assert f"{stem}-motion.svg" in content and f"{stem}-still.svg" in content
            assert "CC BY-SA 4.0" in content


def main():
    structure()
    OUT.mkdir(exist_ok=True)
    with sync_playwright() as pw:
        options = {"headless": True, "args": ["--no-sandbox"]}
        if os.environ.get("CHROMIUM_EXECUTABLE"):
            options["executable_path"] = os.environ["CHROMIUM_EXECUTABLE"]
        browser = pw.chromium.launch(**options)
        css = ((DOCS / "stylesheets" / "concept-motion.css").read_text() +
               "\n" + (DOCS / "stylesheets" / "extra.css").read_text())
        js = (DOCS / "javascripts" / "concept-motion.js").read_text()
        for stem in STEMS:
            for width in (360, 900):
                for reduce in (False, True):
                    context = browser.new_context(
                        viewport={"width": width, "height": 520},
                        reduced_motion="reduce" if reduce else "no-preference",
                    )
                    page = context.new_page()
                    def handle(route):
                        name = route.request.url.rsplit("/", 1)[-1]
                        route.fulfill(status=200, content_type="image/svg+xml",
                                      body=(ASSETS / name).read_bytes())
                    page.route("**/concept-animations/*.svg", handle)
                    page.set_content(
                        f'<html><head><style>body{{margin:12px;max-width:800px}}{css}</style></head>'
                        f'<body><img alt="{stem} illustration" '
                        f'src="https://example.invalid/concept-animations/{stem}-motion.svg"></body></html>'
                    )
                    page.add_script_tag(content=js)
                    button = page.locator(".concept-motion-toggle")
                    assert button.count() == 1, stem
                    image = page.locator(".concept-motion-player img")
                    assert f'-{"still" if reduce else "motion"}.svg' in image.get_attribute("src")
                    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth + 1")
                    if width == 360:
                        assert page.evaluate(
                            "document.querySelector('.concept-motion-player').scrollWidth >= 640"
                        )
                    page.screenshot(path=str(OUT / f"{stem}-{width}-reduced-{reduce}.png"))
                    button.focus()
                    page.keyboard.press("Space")
                    assert f'-{"motion" if reduce else "still"}.svg' in image.get_attribute("src")
                    page.close()
                    context.close()

            page = browser.new_page(viewport={"width": 900, "height": 520})
            page.set_content(
                "<style>svg{width:640px;height:360px}</style>" +
                (ASSETS / f"{stem}-motion.svg").read_text()
            )
            bad = page.evaluate("""() => [...document.querySelectorAll('svg text')]
                .filter(el => { const b=el.getBBox(); return b.x<0 || b.y<0 ||
                    b.x+b.width>640 || b.y+b.height>360; }).map(el=>el.textContent)""")
            assert not bad, (stem, bad)
            if stem == "zero-state-sharding":
                for t, expected, width in (
                    (0.2, [1, 1, 1], 255),
                    (4.5, [0, 1, 1], 159.375),
                    (7.5, [0, 0, 1], 143.438),
                    (10.5, [0, 0, 0], 127.5),
                ):
                    states = page.evaluate("""t => {
                        document.querySelector('svg').setCurrentTime(t);
                        return ['zero-o-0-1','zero-g-0-1','zero-p-0-1']
                          .map(id=>+getComputedStyle(document.getElementById(id)).opacity);
                    }""", t)
                    actual_width = page.evaluate(
                        "document.getElementById('zero-memory').width.animVal.value"
                    )
                    assert all(abs(a-b)<.01 for a,b in zip(states, expected)), (t, states)
                    assert abs(actual_width-width)<.1, (t, actual_width)
                    page.screenshot(path=str(OUT / f"{stem}-inline-t{t}.png"))
            else:
                for t, expected in (
                    (0.2, [0, 0]), (2.5, [0, 0]),
                    (5.5, [1, 0]), (8.5, [1, 1]),
                ):
                    states = page.evaluate("""t => {
                        document.querySelector('svg').setCurrentTime(t);
                        return ['tp-partial-0','tp-output']
                          .map(id=>+getComputedStyle(document.getElementById(id)).opacity);
                    }""", t)
                    assert all(abs(a-b)<.01 for a,b in zip(states, expected)), (t, states)
                    page.screenshot(path=str(OUT / f"{stem}-inline-t{t}.png"))
            page.close()
            print(f"{stem}: structure, timeline, keyboard, reduced motion, mobile and desktop passed")
        browser.close()


if __name__ == "__main__":
    main()
