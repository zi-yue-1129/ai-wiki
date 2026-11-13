#!/usr/bin/env python3
"""Exercise security teaching diagrams with the repository's actual MkDocs player.

Requires: playwright==1.55.0 and python -m playwright install chromium.
Runs a local HTTP server so image loads and JS execute as on the site.
"""
from __future__ import annotations

from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from urllib.parse import parse_qs, urlsplit
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
STEMS = ("prompt-injection-boundary", "watermark-greenlist-score")


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def log_message(self, *_args):
        pass

    def do_GET(self):
        url = urlsplit(self.path)
        if url.path != "/motion-review":
            return super().do_GET()
        args = parse_qs(url.query)
        stem = args["stem"][0]
        if stem not in STEMS:
            self.send_error(400)
            return
        lang = args.get("lang", ["en"])[0]
        alt = "信任邊界概念動畫" if lang == "zh" else "Security concept motion"
        html = f'''<!doctype html><meta charset="utf-8">
<link rel="stylesheet" href="/docs/stylesheets/concept-motion.css">
<main style="width:100%;max-width:760px;margin:auto">
<img src="/docs/assets/concept-animations/{stem}-motion.svg" alt="{alt}">
</main><script src="/docs/javascripts/concept-motion.js"></script>'''
        data = html.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


def main() -> None:
    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    worker = Thread(target=server.serve_forever, daemon=True)
    worker.start()
    origin = f"http://127.0.0.1:{server.server_port}"
    passed = 0
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            for stem in STEMS:
                for lang in ("en", "zh"):
                    for width in (320, 360, 760, 1024):
                        page = browser.new_page(viewport={"width": width, "height": 560})
                        page.goto(f"{origin}/motion-review?stem={stem}&lang={lang}")
                        button = page.locator(".concept-motion-toggle")
                        assert button.count() == 1, f"missing player button: {stem} {lang}"
                        img = page.locator(".concept-motion-player img")
                        assert img.evaluate("e => e.complete && e.naturalWidth > 0")
                        assert img.get_attribute("src").endswith("-motion.svg")
                        button.click()
                        assert img.get_attribute("src").endswith("-still.svg")
                        assert img.evaluate("e => e.complete && e.naturalWidth > 0")
                        button.focus()
                        page.keyboard.press("Enter")
                        assert img.get_attribute("src").endswith("-motion.svg")
                        page.keyboard.press("Space")
                        assert img.get_attribute("src").endswith("-still.svg")
                        if width < 680:
                            player = page.locator(".concept-motion-player")
                            assert player.evaluate("e => e.scrollWidth > e.clientWidth")
                            player.evaluate("e => e.scrollLeft = 250")
                            bounds = button.bounding_box()
                            assert bounds and 0 <= bounds["x"] < width, bounds
                        passed += 1
                        page.close()
                page = browser.new_page()
                page.emulate_media(reduced_motion="reduce")
                page.goto(f"{origin}/motion-review?stem={stem}&lang=en")
                assert page.locator(".concept-motion-player img").get_attribute("src").endswith("-still.svg")
                page.locator(".concept-motion-toggle").click()
                assert page.locator(".concept-motion-player img").get_attribute("src").endswith("-motion.svg")
                passed += 1
                page.close()
            browser.close()
    finally:
        server.shutdown()
        server.server_close()
    print(f"security motion Chromium player: {passed} cases passed")


if __name__ == "__main__":
    main()
