#!/usr/bin/env python3
"""Chromium smoke tests of the actual shared SVG player and static-first bilingual bindings.

Run after installing playwright + Chromium, from the repository root. No network
access: each remote-looking image is served with a Playwright route from this repo.
"""
from __future__ import annotations

from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "docs" / "assets" / "concept-animations"
BASE = "https://wiki-motion.test/assets/concept-animations/"
TOPICS = ("pbwm-gate", "activity-silent-trace")
CSS = (ROOT / "docs" / "stylesheets" / "concept-motion.css").read_text(encoding="utf-8")
JS = (ROOT / "docs" / "javascripts" / "concept-motion.js").read_text(encoding="utf-8")


def build_document(chinese: bool) -> str:
    alts = (
        (
            "PBWM cue gate stores A, rejects a distractor, then stores B.",
            "Activity-silent working memory: a synaptic trace persists during a quiet delay.",
        )
        if not chinese
        else (
            "PBWM 閘門儲存 A、阻擋干擾，然後儲存 B。",
            "活動靜默工作記憶：突觸痕跡在安靜的延遲期持續存在。",
        )
    )
    html = []
    for stem, alt in zip(TOPICS, alts):
        html.append(
            f'<div class="wm-motion-pan" tabindex="0" role="region" aria-label="Teaching illustration">'
            f'<img alt="{alt}" width="640" src="{BASE}{stem}-still.svg" '
            f'data-motion-src="{BASE}{stem}-motion.svg"></div>'
        )
    return (
        '<!doctype html><html><head><meta charset="utf-8"><style>'
        + CSS + '</style></head><body>'
        + ''.join(html)
        + '<script>' + JS + '</script></body></html>'
    )


def main() -> None:
    checked = 0
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        for width in (320, 360, 720, 1024):
            for motion in ("reduce", "no-preference"):
                for chinese in (False, True):
                    context = browser.new_context(
                        viewport={"width": width, "height": 850},
                        reduced_motion=motion,
                    )
                    page = context.new_page()

                    def serve_asset(route):
                        name = route.request.url.rsplit("/", 1)[-1]
                        file = ASSETS / name
                        assert file.is_file(), name
                        route.fulfill(body=file.read_bytes(), content_type="image/svg+xml")

                    page.route(BASE + "*", serve_asset)
                    page.set_content(build_document(chinese), wait_until="load")
                    images = page.locator(".wm-motion-pan img")
                    toggles = page.locator(".concept-motion-toggle")
                    assert images.count() == 2 and toggles.count() == 2
                    for i in range(2):
                        image = images.nth(i)
                        button = toggles.nth(i)
                        assert image.evaluate("(el) => el.complete && el.naturalWidth === 640")
                        starts_static = motion == "reduce"
                        assert image.get_attribute("src").endswith(
                            "-still.svg" if starts_static else "-motion.svg"
                        )
                        button.focus()
                        page.keyboard.press("Enter")
                        page.wait_for_timeout(60)
                        assert image.get_attribute("src").endswith(
                            "-motion.svg" if starts_static else "-still.svg"
                        )
                        page.keyboard.press("Space")
                        page.wait_for_timeout(60)
                        assert image.get_attribute("src").endswith(
                            "-still.svg" if starts_static else "-motion.svg"
                        )
                        assert image.evaluate("(el) => el.complete && el.naturalWidth === 640")
                        viewport = page.locator(".wm-motion-pan").nth(i)
                        if width < 640:
                            assert viewport.evaluate("(el) => el.scrollWidth > el.clientWidth")
                            viewport.focus()
                            page.keyboard.press("ArrowRight")
                            page.wait_for_timeout(100)
                            assert viewport.evaluate("(el) => el.scrollLeft") > 0
                        checked += 1
                    context.close()
        browser.close()
    print(f"PASS: {checked} bilingual/reduced-motion/responsive SVG player cases")


if __name__ == "__main__":
    main()
