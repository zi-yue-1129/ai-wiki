#!/usr/bin/env python3
"""Chromium integration of OOD visuals with the actual shared MkDocs player.

Runs on a controlled local-origin page, not a publicly deployed website.
"""
from pathlib import Path
import re
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "docs/assets/concept-animations"
JS = (ROOT / "docs/javascripts/concept-motion.js").read_text(encoding="utf-8")
CSS = (ROOT / "docs/stylesheets/concept-motion.css").read_text(encoding="utf-8")
CASES = ("odin-gradient-perturbation", "mahalanobis-ellipse-threshold")
ORIGIN = "https://motion.local.test"


def run():
    out = ROOT / "artifacts/ood-motion"
    out.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        for stem in CASES:
            for language, reduced, width in (
                ("en", False, 720),
                ("zh-TW", False, 320),
                ("zh-TW", True, 360),
            ):
                context = browser.new_context(
                    viewport={"width": width, "height": 490},
                    reduced_motion="reduce" if reduced else "no-preference",
                )
                page = context.new_page()
                alt = (
                    "分布外偵測示意：輸入與分數逐步變化"
                    if language == "zh-TW"
                    else "Out-of-distribution detection: input and score evolve"
                )
                def file_url(mode):
                    return f"{ORIGIN}/docs/assets/concept-animations/{stem}-{mode}.svg"
                html = f'''<!doctype html><html><head><meta charset="utf-8">
                <style>{CSS}</style></head><body>
                <div tabindex="0" role="group" style="max-width:100%;overflow-x:auto" aria-label="Diagram">
                <div style="width:640px"><img src="{file_url('still')}"
                data-motion-src="{file_url('motion')}" alt="{alt}"
                width="640" height="360"></div></div></body></html>'''

                def route_handler(route):
                    url = route.request.url
                    if url.endswith("/test"):
                        route.fulfill(
                            status=200,
                            content_type="text/html; charset=utf-8",
                            body=html,
                        )
                        return
                    match = re.search(r"/([^/]+-(?:motion|still)\.svg)$", url)
                    if not match:
                        raise AssertionError(f"unexpected request: {url}")
                    source = ASSETS / match.group(1)
                    assert source.is_file(), str(source)
                    route.fulfill(
                        status=200,
                        content_type="image/svg+xml",
                        body=source.read_bytes(),
                    )

                page.route(f"{ORIGIN}/**", route_handler)
                page.goto(f"{ORIGIN}/test")
                page.add_script_tag(content=JS)
                img = page.locator('img[data-concept-motion-enhanced="yes"]')
                img.wait_for()
                initial = "still" if reduced else "motion"
                assert img.get_attribute("src") == file_url(initial)
                page.wait_for_function(
                    """() => { const img = document.querySelector('img');
                    return img.complete && img.naturalWidth === 640
                      && img.naturalHeight === 360; }"""
                )
                button = page.locator(".concept-motion-toggle")
                assert button.count() == 1
                if reduced and language == "zh-TW":
                    assert "播放" in button.inner_text()
                button.click()
                switched = "motion" if reduced else "still"
                assert img.get_attribute("src") == file_url(switched)
                button.focus()
                page.keyboard.press("Space")
                assert img.get_attribute("src") == file_url(initial)
                page.keyboard.press("Enter")
                assert img.get_attribute("src") == file_url(switched)
                if width <= 360:
                    group = page.locator("[role=group]")
                    assert group.evaluate("(e) => e.scrollWidth > e.clientWidth")
                    group.focus()
                    page.keyboard.press("ArrowRight")
                    page.wait_for_timeout(150)
                    assert group.evaluate("(e) => e.scrollLeft > 0"), (
                        stem, language, width
                    )
                page.screenshot(
                    path=str(out / f"{stem}-{language}-{width}-reduced-{int(reduced)}.png")
                )
                context.close()
        browser.close()
    print("PASS: 6 bilingual OOD player states, real SVG assets, keyboard, reduced motion")


if __name__ == "__main__":
    run()
