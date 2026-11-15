#!/usr/bin/env python3
"""Real Chromium load/control/responsive regression for FlashAttention online-softmax SVGs.

Tests repository CSS, player JavaScript and SVGs over a local HTTP server.
Run separately from MkDocs strict build; this does not validate the deployed site.
"""
from __future__ import annotations

from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from contextlib import contextmanager
import hashlib

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
ASSET = "/docs/assets/concept-animations/"
TOPICS = ("flashattention-online-rescale", "flashattention-exact-merge")
OUT = ROOT / "artifacts" / "flashattention-online"


@contextmanager
def serve():
    class Quiet(SimpleHTTPRequestHandler):
        def log_message(self, *_args):
            pass

    httpd = ThreadingHTTPServer(
        ("127.0.0.1", 0), partial(Quiet, directory=str(ROOT))
    )
    worker = Thread(target=httpd.serve_forever, daemon=True)
    worker.start()
    try:
        yield f"http://127.0.0.1:{httpd.server_port}"
    finally:
        httpd.shutdown()
        httpd.server_close()
        worker.join(timeout=5)


def fixture(language: str) -> str:
    zh = language == "zh"
    labels = (
        ("在新最大值下重新縮放舊區塊的 Softmax 正規化質量",
         "精確合併區塊加權輸出，不直接平均各區塊")
        if zh else
        ("Rescale previous softmax mass after a new maximum",
         "Merge tile outputs under one shared softmax normaliser")
    )
    figures = "".join(
        f'<p><img alt="{alt}" src="{ASSET}{stem}-still.svg"></p>'
        for stem, alt in zip(TOPICS, labels)
    )
    return f"""<!doctype html><html lang="{language}"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="stylesheet" href="/docs/stylesheets/concept-motion.css">
<style>body{{margin:0;padding:12px;font-family:Arial,sans-serif}}
main{{max-width:960px;margin:auto}}p{{margin:0 0 16px}}</style>
</head><body><main class="md-typeset">{figures}</main>
<script src="/docs/javascripts/concept-motion.js"></script></body></html>"""


def image_loaded(page):
    assert page.locator("img").count() == 2
    for img in page.locator("img").all():
        page.wait_for_function(
            "(node) => node.complete && node.naturalWidth === 640",
            arg=img.element_handle(),
        )
        assert img.get_attribute("alt"), "missing localised alt text"


def check(page, width: int, locale: str, reduce: bool):
    page.route("**/flashattention-test", lambda route:
               route.fulfill(status=200, body=fixture(locale), content_type="text/html"))
    page.goto(page.context._base_url + "/flashattention-test", wait_until="load")
    image_loaded(page)
    assert page.evaluate("document.documentElement.scrollWidth") == width, (
        "Unexpected whole-page horizontal overflow", width, locale, reduce
    )
    controls = page.locator(".concept-motion-toggle")
    assert controls.count() == 2, "player did not enhance both stills"
    for n, stem in enumerate(TOPICS):
        host = page.locator(".concept-motion-player").nth(n)
        assert "concept-motion-wide" in (host.get_attribute("class") or "")
        img = host.locator("img")
        expected = "-still.svg" if reduce else "-motion.svg"
        assert img.get_attribute("src").endswith(stem + expected), img.get_attribute("src")
        if width < 640:
            assert host.evaluate("(node) => node.scrollWidth > node.clientWidth"), (
                "Mobile internal horizontal scroll missing", locale, stem
            )
        assert host.locator("button").get_attribute("aria-label")
    if not reduce and width == 1024 and locale == "en":
        first = page.locator(".concept-motion-player").first
        start = hashlib.sha256(first.screenshot()).hexdigest()
        page.wait_for_timeout(3950)
        later = hashlib.sha256(first.screenshot()).hexdigest()
        assert start != later, "Animation image did not change across stages"
    if (width, locale) in ((320, "zh"), (1024, "en")):
        OUT.mkdir(parents=True, exist_ok=True)
        page.screenshot(path=str(OUT / f"{locale}-{width}-{'reduced' if reduce else 'motion'}.png"), full_page=True)
    # Pause and resume with real keyboard controls; both assets must switch.
    for n, stem in enumerate(TOPICS):
        button = controls.nth(n)
        img = page.locator(".concept-motion-player").nth(n).locator("img")
        button.focus()
        button.press("Enter")
        assert img.get_attribute("src").endswith(stem + ("-motion.svg" if reduce else "-still.svg"))
        button.press("Space")
        assert img.get_attribute("src").endswith(stem + ("-still.svg" if reduce else "-motion.svg"))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    with serve() as base, sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        total = 0
        for viewport in (320, 360, 768, 1024):
            for locale in ("en", "zh"):
                for reduced in (False, True):
                    context = browser.new_context(
                        base_url=base,
                        viewport={"width": viewport, "height": 900},
                        reduced_motion="reduce" if reduced else "no-preference",
                    )
                    page = context.new_page()
                    check(page, viewport, locale, reduced)
                    context.close()
                    total += 1
        # GitHub/no-JavaScript fallback remains legible and decodes.
        for viewport in (320, 1024):
            context = browser.new_context(
                base_url=base, viewport={"width": viewport, "height": 900},
                java_script_enabled=False,
            )
            page = context.new_page()
            page.route("**/flashattention-test", lambda route:
                       route.fulfill(status=200, body=fixture("en"), content_type="text/html"))
            page.goto(base + "/flashattention-test")
            image_loaded(page)
            assert page.locator(".concept-motion-toggle").count() == 0
            assert all(img.get_attribute("src").endswith("-still.svg")
                       for img in page.locator("img").all())
            assert page.evaluate("document.documentElement.scrollWidth") == viewport
            context.close()
            total += 1
        browser.close()
        print(f"FlashAttention Chromium: {total}/{total} bilingual, viewport, "
              "reduced-motion, keyboard and no-script scenarios passed")


if __name__ == "__main__":
    main()
