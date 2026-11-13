#!/usr/bin/env python3
"""Test the actual shared player with original SVG files in Chromium."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from urllib.parse import urlsplit, parse_qs
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
STEMS = ("causal-lamp-intervention", "copycat-action-lag")

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self):
        parsed = urlsplit(self.path)
        if parsed.path == "/test-causal":
            zh = parse_qs(parsed.query).get("lang") == ["zh"]
            label = "教學動態示意圖" if zh else "Toy teaching motion"
            body = ['<!doctype html><html><head><meta charset="utf-8">',
                    '<meta name="viewport" content="width=device-width,initial-scale=1">',
                    '<link rel="stylesheet" href="/docs/stylesheets/concept-motion.css">',
                    '</head><body style="margin:0">']
            for stem in STEMS:
                body.append(f'<img alt="{label}: {stem}" src="/docs/assets/concept-animations/{stem}-still.svg">')
            body.append('<script src="/docs/javascripts/concept-motion.js"></script></body></html>')
            result = ''.join(body).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(result)))
            self.end_headers()
            self.wfile.write(result)
        else:
            super().do_GET()

    def log_message(self, *args):
        pass

def main():
    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    Thread(target=server.serve_forever, daemon=True).start()
    count = 0
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            for width in (320, 360, 720, 1024):
                for reduced in (False, True):
                    for language in ("en", "zh"):
                        page = browser.new_page(viewport={"width": width, "height": 500},
                                                reduced_motion="reduce" if reduced else "no-preference")
                        url = f"http://127.0.0.1:{server.server_port}/test-causal?lang={language}"
                        page.goto(url, wait_until="networkidle")
                        for stem in STEMS:
                            img = page.locator(f'.causal-imitation-motion img[src*="{stem}"]')
                            assert img.count() == 1, (stem, width, language, "player")
                            assert img.evaluate("(i) => i.complete && i.naturalWidth === 640"), (stem, "image decode")
                            initial = "-still.svg" if reduced else "-motion.svg"
                            assert img.get_attribute("src").endswith(initial), (stem, "initial state")
                            parent = img.locator("xpath=..")
                            toggle = parent.locator("button")
                            assert toggle.count() == 1, (stem, "control")
                            assert ("播放" if language == "zh" else "Play") in toggle.inner_text() if reduced else True
                            toggle.click()
                            assert img.get_attribute("src").endswith("-motion.svg" if reduced else "-still.svg"), (stem, "toggle")
                            toggle.focus()
                            toggle.press("Space")
                            assert img.get_attribute("src").endswith(initial), (stem, "keyboard")
                            if width < 640:
                                assert parent.evaluate("(e) => e.scrollWidth > e.clientWidth + 100"), (stem, "mobile scroll")
                                parent.focus()
                                parent.press("ArrowRight")
                                assert parent.evaluate("(e) => e.scrollLeft > 0"), (stem, "keyboard scroll")
                            count += 1
                        page.close()
            browser.close()
    finally:
        server.shutdown()
        server.server_close()
    print(f"PASS: {count} Chromium player and responsive states")

if __name__ == "__main__":
    main()
