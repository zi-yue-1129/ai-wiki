#!/usr/bin/env python3
"""Regression for GitHub-safe still previews and MkDocs motion of four core curiosity diagrams."""
from __future__ import annotations

import re
from pathlib import Path
from xml.etree import ElementTree as ET
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
ASSETS = DOCS / "assets/concept-animations"
PLAYER = DOCS / "javascripts/concept-motion.js"
REVIEW = ROOT / "artifacts/rnd-icm-motion"
CASES = {
    "rnd": ("rnd-prediction-error", "rnd-state-novelty"),
    "icm": ("icm-forward-inverse", "icm-predictable-stochastic"),
}
BASE = "../../../../../assets/concept-animations/"


def main():
    REVIEW.mkdir(parents=True, exist_ok=True)
    # Markdown must be intelligible without executing scripts (GitHub render).
    for topic, stems in CASES.items():
        for locale in ("index.md", "index.zh-TW.md"):
            content = (DOCS / f"theory/paradigms/reinforcement-learning/exploration/{topic}/{locale}").read_text(encoding="utf-8")
            tags = re.findall(r"<img\\b[^>]*>", content)
            for stem in stems:
                base = BASE + stem
                matches = [tag for tag in tags if f'data-motion-src="{base}-motion.svg"' in tag]
                assert len(matches) == 1, (topic, locale, stem, len(matches))
                tag = matches[0]
                for fragment in (f'src="{base}-still.svg"', f'data-still-src="{base}-still.svg"',
                                 'loading="lazy"', 'alt="'):
                    assert fragment in tag, (topic, locale, stem, fragment)
                assert not re.search(r"!\\[[^\\]]*\\]\\([^\\n)]*" + stem + r"-motion\\.svg\\)", content)
                for suffix in ("motion", "still"):
                    assert (ASSETS / f"{stem}-{suffix}.svg").is_file()

    for stems in CASES.values():
        for stem in stems:
            for suffix in ("motion", "still"):
                svg = (ASSETS / f"{stem}-{suffix}.svg").read_text(encoding="utf-8")
                root = ET.fromstring(svg)
                assert root.tag == "{http://www.w3.org/2000/svg}svg"
                assert root.get("viewBox")
                assert "<script" not in svg and "onload=" not in svg
                if suffix == "still":
                    assert not root.findall(".//{*}animate") and not root.findall(".//{*}animateMotion")

    player = PLAYER.read_text(encoding="utf-8")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True,
            executable_path="/usr/bin/chromium" if Path("/usr/bin/chromium").exists() else None,
            args=["--no-sandbox"])
        try:
            for topic, stems in CASES.items():
                for stem in stems:
                    for width in (320, 360, 720, 1024):
                        for kind in ("still", "motion"):
                            svg = (ASSETS / f"{stem}-{kind}.svg").read_text(encoding="utf-8")
                            page = browser.new_page(viewport={"width": width, "height": 1150})
                            errors = []
                            page.on("pageerror", lambda e: errors.append(str(e)))
                            page.set_content('<body style="margin:0"><main style="max-width:760px">' + svg + '</main></body>')
                            page.locator("svg").evaluate("el=>{el.style.width='100%';el.style.height='auto'}")
                            if kind == "motion":
                                page.evaluate("() => {const s=document.querySelector('svg');s.setCurrentTime(4);s.pauseAnimations()}")
                            page.locator("svg").screenshot(path=str(REVIEW / f"paired-{stem}-{width}-{kind}.png"))
                            assert not errors, errors
                            assert not page.evaluate("document.documentElement.scrollWidth > innerWidth + 1"), (stem, width, kind)
                            page.close()
                    # Real MkDocs enhancement starts from GitHub-safe still src.
                    for zh in (False, True):
                        for reduced in (False, True):
                            ctx = browser.new_context(viewport={"width": 320, "height": 900},
                                reduced_motion="reduce" if reduced else "no-preference")
                            page = ctx.new_page()
                            alt = "教學動畫" if zh else "Instructional animation"
                            base = "http://127.0.0.1:9/docs/assets/concept-animations/" + stem
                            page.set_content(
                                f'<img alt="{alt}" src="{base}-still.svg" '
                                f'data-motion-src="{base}-motion.svg" data-still-src="{base}-still.svg">')
                            img = page.locator("img")
                            assert img.get_attribute("src").endswith("-still.svg")
                            page.add_script_tag(content=player)
                            mobile = stem in ("rnd-state-novelty", "icm-predictable-stochastic")
                            ending = "-mobile-still.svg" if mobile else "-still.svg"
                            playing = "-mobile-motion.svg" if mobile else "-motion.svg"
                            assert img.get_attribute("src").endswith(ending if reduced else playing)
                            pause = "暫停概念動畫" if zh else "Pause concept animation"
                            play = "播放概念動畫" if zh else "Play concept animation"
                            if not reduced:
                                page.get_by_role("button", name=pause).click()
                                assert img.get_attribute("src").endswith(ending)
                            page.get_by_role("button", name=play).focus()
                            page.keyboard.press("Enter")
                            assert img.get_attribute("src").endswith(playing)
                            page.get_by_role("button", name=pause).focus()
                            page.keyboard.press("Space")
                            assert img.get_attribute("src").endswith(ending)
                            if mobile:
                                page.set_viewport_size({"width": 1024, "height": 900})
                                assert img.get_attribute("src").endswith("-still.svg")
                                assert not img.get_attribute("src").endswith("-mobile-still.svg")
                            ctx.close()
        finally:
            browser.close()
    print("PASS: 4 diagrams x 2 languages; GitHub still fallback, 4 responsive widths, keyboard and reduced motion")


if __name__ == "__main__":
    main()
