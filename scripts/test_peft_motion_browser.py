#!/usr/bin/env python3
"""Test (IA)³ and prefix SVGs with the repository's real MkDocs player in Chromium."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from urllib.parse import parse_qs, urlsplit
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
STEMS = ("ia3-channel-gates", "prefix-kv-attention")


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
        stem = args.get("stem", [""])[0]
        if stem not in STEMS:
            self.send_error(400)
            return
        alt = "鍵值注意力教學動畫" if args.get("lang", ["en"])[0] == "zh" else "KV attention teaching animation"
        html = f"""<!doctype html><meta charset="utf-8">
<link rel="stylesheet" href="/docs/stylesheets/concept-motion.css">
<main style="max-width:760px;margin:auto">
<img src="/docs/assets/concept-animations/{stem}-motion.svg" alt="{alt}">
</main><script src="/docs/javascripts/concept-motion.js"></script>"""
        data = html.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


def main():
    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    origin = f"http://127.0.0.1:{server.server_port}"
    passed = 0
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            for stem in STEMS:
                for lang in ("en", "zh"):
                    for width in (320, 360, 720, 1024):
                        page = browser.new_page(viewport={"width": width, "height": 540})
                        page.goto(f"{origin}/motion-review?stem={stem}&lang={lang}")
                        img = page.locator(".concept-motion-player img")
                        page.wait_for_function("() => { const i=document.querySelector('.concept-motion-player img'); return i && i.complete && i.naturalWidth > 0; }")
                        button = page.locator(".concept-motion-toggle")
                        assert button.count() == 1
                        assert img.get_attribute("src").endswith("-motion.svg")
                        button.click()
                        assert img.get_attribute("src").endswith("-still.svg")
                        page.wait_for_function("() => { const i=document.querySelector('.concept-motion-player img'); return i && i.complete && i.naturalWidth > 0; }")
                        button.focus()
                        page.keyboard.press("Enter")
                        assert img.get_attribute("src").endswith("-motion.svg")
                        page.keyboard.press("Space")
                        assert img.get_attribute("src").endswith("-still.svg")
                        if width < 640:
                            host = page.locator(".concept-motion-player")
                            assert host.get_attribute("tabindex") == "0"
                            assert host.evaluate("(e)=>e.scrollWidth > e.clientWidth")
                            host.evaluate("(e)=>e.scrollLeft = 240")
                            assert host.evaluate("(e)=>e.scrollLeft > 0")
                            bb = button.bounding_box()
                            assert bb and 0 <= bb["x"] < width
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
    print(f"PEFT motion Chromium player: {passed} cases passed")


if __name__ == "__main__":
    main()
