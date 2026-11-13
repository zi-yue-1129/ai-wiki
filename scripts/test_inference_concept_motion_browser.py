#!/usr/bin/env python3
"""Browser regression for shared PagedAttention and expert-offloading animations.

Uses the actual MkDocs player and stylesheet with local SVGs, not a mock UI.
"""
from pathlib import Path

from playwright.sync_api import sync_playwright

DOCS = Path(__file__).resolve().parents[1] / "docs"
ASSETS = DOCS / "assets" / "concept-animations"
JAVASCRIPT = (DOCS / "javascripts" / "concept-motion.js").read_text(encoding="utf-8")
STYLES = (DOCS / "stylesheets" / "concept-motion.css").read_text(encoding="utf-8")
STEMS = ("paged-block-mapping", "expert-cache-miss")
WIDTHS = (320, 360, 720, 1024)


def main() -> None:
    cases = 0
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        for stem in STEMS:
            for chinese in (False, True):
                for width in WIDTHS:
                    for reduced in (False, True):
                        page = browser.new_page(
                            viewport={"width": width, "height": 600},
                            reduced_motion="reduce" if reduced else "no-preference",
                        )
                        def serve_svg(route):
                            filename = route.request.url.rsplit("/", 1)[-1]
                            assert filename in (
                                f"{stem}-motion.svg", f"{stem}-still.svg"
                            )
                            route.fulfill(
                                status=200, content_type="image/svg+xml",
                                body=(ASSETS / filename).read_bytes()
                            )

                        page.route("https://example.test/concept-animations/**", serve_svg)
                        path = "https://example.test/concept-animations/"
                        motion = f"{path}{stem}-motion.svg"
                        still = f"{path}{stem}-still.svg"
                        alt = "示意快取轉換動畫" if chinese else "Schematic cache transition"
                        page.set_content(
                            f'<style>{STYLES}</style>'
                            f'<img src="{still}" data-motion-src="{motion}" alt="{alt}">'
                        )
                        page.add_script_tag(content=JAVASCRIPT)
                        image = page.locator("img")
                        toggle = page.locator(".concept-motion-toggle")
                        region = page.locator(".concept-motion-player")
                        assert toggle.count() == 1, (stem, width, chinese, reduced)
                        assert region.get_attribute("role") == "region"
                        assert region.get_attribute("tabindex") == "0"
                        assert image.get_attribute("src") == (still if reduced else motion)
                        image.evaluate("(img) => img.decode()")
                        assert image.evaluate("(img) => img.naturalWidth") == 640

                        toggle.focus()
                        page.keyboard.press("Enter")
                        assert image.get_attribute("src") == (motion if reduced else still)
                        image.evaluate("(img) => img.decode()")
                        toggle.focus()
                        page.keyboard.press("Space")
                        assert image.get_attribute("src") == (still if reduced else motion)

                        if width <= 360:
                            assert region.evaluate("(r) => r.scrollWidth > r.clientWidth")
                            region.focus()
                            page.keyboard.press("ArrowRight")
                            page.wait_for_timeout(200)
                            assert region.evaluate("(r) => r.scrollLeft > 0")

                        page.close()
                        cases += 1
        browser.close()
    print(f"PASS: {cases} bilingual inference-motion browser cases")


if __name__ == "__main__":
    main()
