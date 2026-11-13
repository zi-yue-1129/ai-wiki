#!/usr/bin/env python3
"""Chromium integration tests for the actual shared concept-motion.js player.

Exercises BOTH oscillation lessons in English and Traditional Chinese, with
real SVG assets, controlled network routing, narrow/desktop viewports,
native buttons, keyboard input, and prefers-reduced-motion.
"""
from pathlib import Path
from urllib.parse import urlsplit
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "docs" / "assets" / "concept-animations"
OUT = ROOT / "artifacts" / "oscillation-motion"
HOST = "https://oscillation.qa"
STEMS = ("theta-gamma-phase-amplitude", "coherence-phase-gating")


def html(stem: str, zh: bool) -> str:
    alt = (
        "發送端與接收端的相位變化示意圖。" if zh and stem.startswith("coherence")
        else "Theta 相位調變 gamma 振幅的示意圖。" if zh
        else "Phase-aligned sender and receiver waveforms." if stem.startswith("coherence")
        else "Theta phase modulates the gamma amplitude envelope."
    )
    return f"""<!doctype html><html lang="{'zh-TW' if zh else 'en'}">
    <head><meta charset="utf-8">
    <link rel="stylesheet" href="/stylesheets/concept-motion.css"></head>
    <body><main><div class="concept-motion-scroll" role="region" tabindex="0"
       style="overflow-x:auto;max-width:100%" aria-label="Scrollable diagram">
    <img src="/assets/concept-animations/{stem}-still.svg"
         data-motion-src="/assets/concept-animations/{stem}-motion.svg"
         data-still-src="/assets/concept-animations/{stem}-still.svg"
         width="640" height="360" style="min-width:640px;display:block"
         alt="{alt}"></div></main>
    <script src="/javascripts/concept-motion.js" defer></script></body></html>"""


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
                            page.wait_for_timeout(250)
                            assert scroll.evaluate("(e)=>e.scrollLeft") > 0
                        name = f"{stem}-{'zh' if zh else 'en'}-{width}-{'reduced' if reduced else 'motion'}.png"
                        page.screenshot(path=str(OUT / name), full_page=True)
                        scenarios += 1
                        context.close()
        browser.close()
    print(f"PASS: {scenarios} real SVG/browser/player scenarios with keyboard, pause, fallback, reduced motion, and horizontal scrolling")


if __name__ == "__main__":
    main()
