#!/usr/bin/env python3
"""Browser regression: bilingual synthetic-data animations and accessible fallbacks."""
from __future__ import annotations

from pathlib import Path
import os
import re
from playwright.sync_api import sync_playwright

ROOT = Path(os.environ.get("AIWIKI_ROOT", Path(__file__).resolve().parents[1]))
DOCS = ROOT / "docs"
ASSETS = DOCS / "assets/concept-animations"
JS = (DOCS / "javascripts/concept-motion.js").read_text(encoding="utf-8")
CSS = (DOCS / "stylesheets/concept-motion.css").read_text(encoding="utf-8")
TOPICS = {
    "self-instruct-filter-loop": "engineering/synthetic-data/self-instruct",
    "recursive-tail-loss": "engineering/synthetic-data/model-collapse",
}


def test_all() -> int:
    checked = 0
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=True, args=["--no-sandbox"],
            **({"executable_path": os.environ["CHROMIUM_EXECUTABLE"]}
               if os.environ.get("CHROMIUM_EXECUTABLE") else {}),
        )
        try:
            for stem, page_stem in TOPICS.items():
                for suffix in (".md", ".zh-TW.md"):
                    source = (DOCS / (page_stem + suffix)).read_text(encoding="utf-8")
                    match = re.search(r'<div class="concept-motion-scroll".*?</div>\s*</div>', source, re.S)
                    assert match, f"Missing authored scroll markup: {page_stem}{suffix}"
                    markup = match.group(0)
                    attrs = dict(re.findall(r'([\w-]+)="([^"]*)"', re.search(r'<img[^>]+>', markup).group(0)))
                    static_name = Path(attrs['src']).name
                    motion_name = Path(attrs['data-motion-src']).name
                    assert static_name == f"{stem}-still.svg"
                    assert motion_name == f"{stem}-motion.svg"
                    alt = attrs['alt']
                    if suffix == ".zh-TW.md":
                        assert re.search(r"[\u3400-\u9fff]", alt)
                    for width in (320, 720):
                        for reduced in (False, True):
                            page = browser.new_page(viewport={"width": width, "height": 460})
                            page.emulate_media(reduced_motion="reduce" if reduced else "no-preference")

                            def route_svg(route):
                                asset = ASSETS / route.request.url.rsplit("/", 1)[-1]
                                assert asset.is_file(), asset
                                route.fulfill(body=asset.read_bytes(), content_type="image/svg+xml")

                            page.route("**/assets/concept-animations/*.svg", route_svg)
                            url_base = "https://wiki.test/assets/concept-animations/"
                            authored = markup.replace('../../assets/concept-animations/', url_base)
                            page.set_content(
                                '<!doctype html><html lang="' + ('zh-TW' if suffix == '.zh-TW.md' else 'en') + '"><head><style>body{margin:0;padding:8px}'
                                + CSS + '</style></head><body>' + authored + '</body></html>'
                            )
                            page.add_script_tag(content=JS)
                            button = page.locator(".concept-motion-toggle")
                            button.wait_for()
                            if suffix == ".zh-TW.md":
                                assert re.search(r"[\u3400-\u9fff]", button.inner_text())
                            assert page.evaluate("document.documentElement.scrollWidth") <= width
                            image = page.locator(".concept-motion-player img")
                            expected = static_name if reduced else motion_name
                            assert image.get_attribute("src").endswith(expected)
                            page.wait_for_function(
                                'document.querySelector("img").complete && document.querySelector("img").naturalWidth === 640'
                            )
                            button.click()
                            page.wait_for_function(
                                'document.querySelector("img").complete && document.querySelector("img").naturalWidth === 640'
                            )
                            assert image.get_attribute("src").endswith(motion_name if reduced else static_name)
                            button.focus()
                            page.keyboard.press("Space")
                            assert image.get_attribute("src").endswith(expected)
                            if width == 320:
                                host = page.locator(".concept-motion-scroll")
                                size = host.evaluate(
                                    "n => ({client:n.clientWidth,scroll:n.scrollWidth,tab:n.tabIndex})"
                                )
                                assert size["client"] < 640 <= size["scroll"] and size["tab"] == 0
                                host.focus()
                                page.keyboard.press("ArrowRight")
                                page.wait_for_function('document.querySelector(".concept-motion-scroll").scrollLeft > 0')
                            checked += 1
                            page.close()
        finally:
            browser.close()
    print(f"Synthetic-data motion browser: {checked}/16 cases passed")
    return checked


if __name__ == "__main__":
    test_all()
