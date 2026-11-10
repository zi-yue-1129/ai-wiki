#!/usr/bin/env python3
"""Chromium regression for PETS / MBPO loop, GitHub stills and MkDocs controls."""
from __future__ import annotations

from pathlib import Path
from shutil import which
from urllib.parse import urlsplit
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "docs/assets/concept-animations"
OUT = ROOT / "artifacts/model-based-motion"
STEMS = ("pets-ensemble-particles", "mbpo-short-branches", "pets-cem-refit", "mbpo-horizon-error")
WIDTHS = (320, 360, 720, 1024)
TIMES = (0.4, 2.8, 5.4, 8.8)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    count = 0
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, executable_path=which("chromium"))
        for stem in STEMS:
            for width in WIDTHS:
                page = browser.new_page(viewport={"width": width, "height": 600})
                for kind in ("motion", "still"):
                    path = ASSETS / f"{stem}-{kind}.svg"
                    source = path.read_text(encoding="utf-8")
                    page.set_content(
                        '<style>body{margin:0}.figure{width:100%;max-width:640px;margin:auto}'
                        'svg{display:block;width:100%;height:auto}</style>'
                        '<div class="figure">' + source + '</div>'
                    )
                    assert page.locator("svg title").count() == 1
                    assert page.locator("svg desc").count() == 1
                    assert page.locator("svg animate").count() > 0 if kind == "motion" else page.locator("svg animate").count() == 0
                    for point in TIMES if kind == "motion" else (0,):
                        if kind == "motion":
                            page.locator("svg").evaluate("(svg,time) => svg.setCurrentTime(time)", point)
                        geometry = page.locator("svg").evaluate("""svg => {
                            const root = svg.getBoundingClientRect();
                            const texts = [...svg.querySelectorAll('text')].map(t => {
                                const b = t.getBoundingClientRect();
                                return {label: t.textContent, left:b.left, right:b.right,
                                        top:b.top, bottom:b.bottom};
                            });
                            return {root:{left:root.left,right:root.right,top:root.top,bottom:root.bottom}, texts};
                        }""")
                        box = geometry["root"]
                        for text in geometry["texts"]:
                            assert text["left"] >= box["left"] - 2 and text["right"] <= box["right"] + 2, (stem, width, point, text)
                            assert text["top"] >= box["top"] - 2 and text["bottom"] <= box["bottom"] + 2, (stem, width, point, text)
                        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth + 1")
                        name = f"{stem}-{width}-{kind}-{str(point).replace('.', '_')}.png"
                        page.locator(".figure").screenshot(path=str(OUT / name), animations="allow")
                        count += 1
                page.close()
        assert count == 80, count
        # Exercise the repository's actual shared player on all four real asset pairs,
        # in both languages and with motion preferences explicitly selected.
        script = (ROOT / "docs/javascripts/concept-motion.js").read_text(encoding="utf-8")

        def serve(route):
            name = urlsplit(route.request.url).path.rsplit("/", 1)[-1]
            route.fulfill(status=200, content_type="image/svg+xml",
                          body=(ASSETS / name).read_text(encoding="utf-8"))

        for stem in STEMS:
            for chinese in (False, True):
                alt = "模型動畫：探索轉換過程" if chinese else "Model-based planning animation"
                html = (
                    f'<html><body><img alt="{alt}" '
                    f'src="https://wiki.test/assets/concept-animations/{stem}-motion.svg">'
                    '<script>' + script + '</script></body></html>'
                )
                for reduced_motion in ("no-preference", "reduce"):
                    page = browser.new_page(
                        viewport={"width": 360, "height": 600}, reduced_motion=reduced_motion
                    )
                    page.route("https://wiki.test/**", serve)
                    page.set_content(html)
                    toggle = page.locator(".concept-motion-toggle")
                    assert toggle.count() == 1, (stem, chinese, reduced_motion)
                    paused_label = "播放" if chinese else "Play"
                    running_label = "暫停" if chinese else "Pause"
                    if reduced_motion == "reduce":
                        assert paused_label in toggle.inner_text()
                        assert page.locator("img").get_attribute("src").endswith(f"{stem}-still.svg")
                        toggle.click()
                        assert running_label in toggle.inner_text()
                        toggle.focus()
                        toggle.press("Space")
                        assert paused_label in toggle.inner_text()
                    else:
                        assert running_label in toggle.inner_text()
                        toggle.click()
                        assert paused_label in toggle.inner_text()
                        assert page.locator("img").get_attribute("src").endswith(f"{stem}-still.svg")
                        toggle.focus()
                        toggle.press("Enter")
                        assert running_label in toggle.inner_text()
                        toggle.press("Space")
                        assert paused_label in toggle.inner_text()
                    page.close()
        browser.close()
    print(f"PASS: {count} Chromium frames plus 16 bilingual/motion-preference MkDocs player checks")


if __name__ == "__main__":
    main()
