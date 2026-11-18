#!/usr/bin/env python3
"""Chromium integration tests for the actual shared concept-motion.js player.

Exercises BOTH oscillation lessons in English and Traditional Chinese, with
real SVG assets, controlled network routing, narrow/desktop viewports,
native buttons, keyboard input, and prefers-reduced-motion.
"""
from pathlib import Path
import re
from urllib.parse import urlsplit
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "docs" / "assets" / "concept-animations"
OUT = ROOT / "artifacts" / "oscillation-motion"
HOST = "https://oscillation.qa"
STEMS = ("theta-gamma-phase-amplitude", "coherence-phase-gating")


def html(stem: str, zh: bool) -> str:
    topic = 'theta-gamma-coupling' if stem.startswith('theta') else 'communication-through-coherence'
    source = (ROOT / f"docs/brain-mind/oscillations/{topic}/index{'.zh-TW' if zh else ''}.md").read_text()
    markup = re.search(r'<div class="concept-motion-scroll".*?</div>\s*</div>', source, re.S).group(0)
    markup = markup.replace('../../../assets/concept-animations/', '/assets/concept-animations/')
    return f"""<!doctype html><html lang="{'zh-TW' if zh else 'en'}">
    <head><meta charset="utf-8"><link rel="stylesheet" href="/stylesheets/concept-motion.css"></head>
    <body><main>{markup}</main><script src="/javascripts/concept-motion.js" defer></script></body></html>"""


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    scenarios = 0
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        for stem in STEMS:
            for zh in (False, True):
                for width in (320, 720):
                    for reduced in (False, True):
                        context = browser.new_context(
                            viewport={"width": width, "height": 580},
                            reduced_motion="reduce" if reduced else "no-preference",
                        )
                        page = context.new_page()
                        markup = html(stem, zh)

                        def respond(route):
                            path = urlsplit(route.request.url).path
                            if path == "/test":
                                route.fulfill(body=markup, content_type="text/html")
                            elif path == "/stylesheets/concept-motion.css":
                                route.fulfill(
                                    path=str(ROOT / "docs/stylesheets/concept-motion.css"),
                                    content_type="text/css",
                                )
                            elif path == "/javascripts/concept-motion.js":
                                route.fulfill(
                                    path=str(ROOT / "docs/javascripts/concept-motion.js"),
                                    content_type="application/javascript",
                                )
                            elif path.startswith("/assets/concept-animations/"):
                                target = ASSETS / path.rsplit("/", 1)[-1]
                                assert target.is_file(), str(target)
                                route.fulfill(path=str(target), content_type="image/svg+xml")
                            else:
                                route.abort()

                        page.route(HOST + "/**", respond)
                        page.goto(HOST + "/test")
                        button = page.locator(".concept-motion-toggle")
                        button.wait_for()
                        assert page.evaluate("document.documentElement.scrollWidth") <= width
                        image = page.locator("img")
                        expected = "still" if reduced else "motion"
                        assert image.get_attribute("src").endswith(f"-{expected}.svg")
                        assert (("播放" if zh else "Play") in button.inner_text()) == reduced
                        page.wait_for_function(
                            "() => {let i=document.querySelector('img');return i.complete && i.naturalWidth===640;}"
                        )
                        button.click()
                        expected = "motion" if reduced else "still"
                        assert image.get_attribute("src").endswith(f"-{expected}.svg")
                        page.wait_for_function(
                            "() => {let i=document.querySelector('img');return i.complete && i.naturalWidth===640;}"
                        )
                        button.focus()
                        page.keyboard.press("Enter")
                        expected = "still" if reduced else "motion"
                        assert image.get_attribute("src").endswith(f"-{expected}.svg")
                        button.focus()
                        page.keyboard.press("Space")
                        expected = "motion" if reduced else "still"
                        assert image.get_attribute("src").endswith(f"-{expected}.svg")
                        if width < 640:
                            scroll = page.locator(".concept-motion-scroll")
                            dimensions = scroll.evaluate(
                                "(e)=>[e.clientWidth,e.scrollWidth]"
                            )
                            assert dimensions[1] > dimensions[0], dimensions
                            scroll.evaluate("(e)=>e.scrollLeft=0")
                            scroll.focus()
                            page.keyboard.press("ArrowRight")
                            page.wait_for_function('document.querySelector(".concept-motion-scroll").scrollLeft > 0')
                        name = f"{stem}-{'zh' if zh else 'en'}-{width}-{'reduced' if reduced else 'motion'}.png"
                        page.screenshot(path=str(OUT / name), full_page=True)
                        scenarios += 1
                        context.close()
        browser.close()
    print(f"PASS: {scenarios} real SVG/browser/player scenarios with keyboard, pause, fallback, reduced motion, and horizontal scrolling")


if __name__ == "__main__":
    main()
