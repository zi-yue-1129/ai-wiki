#!/usr/bin/env python3
"""Exercise the production concept-motion player with two semi-supervised lessons."""
from __future__ import annotations

from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "docs/assets/concept-animations"
PLAYER = (ROOT / "docs/javascripts/concept-motion.js").read_text(encoding="utf-8")
PAIRS = ("fixmatch-confidence-gate", "mean-teacher-ema-tracking")


def run() -> None:
    cases = 0
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        for stem in PAIRS:
            for zh in (False, True):
                alt = "信心門檻教學動畫" if zh else "Confidence-gated teaching animation"
                for width in (320, 360, 720, 1024):
                    for reduce in (False, True):
                        ctx = browser.new_context(
                            viewport={"width": width, "height": 470},
                            reduced_motion="reduce" if reduce else "no-preference",
                        )
                        page = ctx.new_page()
                        html = f"""<!doctype html><html><head><meta charset="utf-8">
<style>body{{margin:0}}#scroll{{max-width:100%;overflow-x:auto}}
#scroll>div{{width:640px}}img{{width:640px;height:360px}}</style></head>
<body><div id="scroll" role="group" tabindex="0"><div>
<img src="/assets/concept-animations/{stem}-still.svg"
data-motion-src="/assets/concept-animations/{stem}-motion.svg"
alt="{alt}" width="640" height="360">
</div></div><script>{PLAYER}</script></body></html>"""
                        def route(request):
                            path = request.request.url.split("?", 1)[0]
                            if path.endswith("/lesson"):
                                request.fulfill(status=200, content_type="text/html", body=html)
                            elif path.endswith(".svg"):
                                name = path.rsplit("/", 1)[-1]
                                file = ASSETS / name
                                assert file.is_file(), name
                                request.fulfill(status=200, content_type="image/svg+xml", body=file.read_bytes())
                            else:
                                request.abort()
                        page.route("**/*", route)
                        page.goto("https://wiki.example/lesson", wait_until="networkidle")
                        img = page.locator("img")
                        button = page.locator("button.concept-motion-toggle")
                        assert button.count() == 1, (stem, zh, width, reduce, "missing control")
                        expected = "-still.svg" if reduce else "-motion.svg"
                        assert img.get_attribute("src").endswith(expected), (stem, reduce, "initial fallback")
                        assert img.evaluate("el => el.decode().then(() => el.naturalWidth > 0 && Math.round(el.getBoundingClientRect().width) === 640)")
                        button.click()
                        expected = "-motion.svg" if reduce else "-still.svg"
                        assert img.get_attribute("src").endswith(expected), (stem, reduce, "click")
                        button.focus()
                        page.keyboard.press("Space")
                        expected = "-still.svg" if reduce else "-motion.svg"
                        assert img.get_attribute("src").endswith(expected), (stem, reduce, "Space")
                        page.keyboard.press("Enter")
                        expected = "-motion.svg" if reduce else "-still.svg"
                        assert img.get_attribute("src").endswith(expected), (stem, reduce, "Enter")
                        assert img.evaluate("el => el.decode().then(() => el.naturalWidth > 0 && Math.round(el.getBoundingClientRect().width) === 640)")
                        if width < 640:
                            scroll = page.locator("#scroll")
                            assert scroll.evaluate("el => el.scrollWidth > el.clientWidth"), (stem, width)
                            scroll.focus()
                            assert scroll.evaluate("el => document.activeElement === el"), (stem, width)
                            scroll.evaluate("el => { el.scrollLeft = 96; }")
                            assert scroll.evaluate("el => el.scrollLeft") > 0, (stem, width)
                        assert ("播放" in button.inner_text()) == zh if img.get_attribute("src").endswith("-still.svg") else ("暫停" in button.inner_text()) == zh
                        ctx.close()
                        cases += 1
        browser.close()
    print(f"PASS: {cases} production-player language/motion/keyboard/decode/mobile cases")


if __name__ == "__main__":
    run()
