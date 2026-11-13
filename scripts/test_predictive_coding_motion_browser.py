#!/usr/bin/env python3
"""Render bilingual predictive-coding SVGs and exercise the real MkDocs player.

Run after: python -m playwright install chromium
"""
from __future__ import annotations

import os
import re
from pathlib import Path
from xml.etree import ElementTree as ET
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
ASSETS = DOCS / "assets" / "concept-animations"
OUT = ROOT / "artifacts" / "predictive-coding-motion"
TOPICS = {
    "rao-ballard-residual": "brain-mind/predictive-coding/rao-ballard-1999/index",
    "predictive-local-settling": "brain-mind/predictive-coding/whittington-bogacz-2017/index",
}
NS = "{http://www.w3.org/2000/svg}"


def validate_svg(stem: str, mode: str) -> Path:
    path = ASSETS / f"{stem}-{mode}.svg"
    assert path.is_file() and path.stat().st_size < 50_000, path
    root = ET.parse(path).getroot()
    assert root.tag == NS + "svg" and root.get("viewBox") == "0 0 640 360"
    assert root.find(NS + "title") is not None and root.find(NS + "desc") is not None
    animations = []
    for elem in root.iter():
        tag = elem.tag.split("}")[-1]
        assert tag not in {"script", "iframe", "image", "foreignObject"}, (path, tag)
        assert all(not k.split("}")[-1].startswith("on") for k in elem.attrib)
        assert not any(v.startswith(("javascript:", "http:", "https:", "data:"))
                       for v in elem.attrib.values())
        if tag in {"animate", "animateMotion"}:
            animations.append(elem)
            assert elem.get("repeatCount") == "indefinite"
    assert bool(animations) == (mode == "motion"), path
    return path


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    count = 0
    with sync_playwright() as pw:
        browser = pw.chromium.launch(
            headless=True, executable_path=os.environ.get("CHROMIUM_EXECUTABLE") or None,
            args=["--no-sandbox"],
        )
        js = (DOCS / "javascripts" / "concept-motion.js").read_text(encoding="utf-8")
        css = (DOCS / "stylesheets" / "concept-motion.css").read_text(encoding="utf-8")
        for stem, page_path in TOPICS.items():
            for mode in ("motion", "still"):
                file = validate_svg(stem, mode)
                svg = file.read_text(encoding="utf-8")
                for width in (320, 360, 720, 1024):
                    times = (0, 2.5, 5, 8, 10.5) if mode == "motion" else (0,)
                    page = browser.new_page(viewport={"width": width, "height": 500})
                    page.set_content("<!doctype html><body style='margin:0'>" + svg)
                    for t in times:
                        page.locator("svg").evaluate("(s,t)=>s.setCurrentTime(t)", t)
                        bounds = page.locator("svg text").evaluate_all(
                            """els => els.map(el => {
                                const b = el.getBBox();
                                return [b.x,b.y,b.width,b.height]
                            })"""
                        )
                        assert all(x >= -1 and y >= -1 and x + w <= 641 and y + h <= 361
                                   for x, y, w, h in bounds), (stem, width, t, bounds)
                        if width in (320, 720):
                            page.screenshot(path=str(OUT / f"{stem}-{mode}-{width}-{t}.png"))
                        count += 1
                    page.close()

            for lang in (".md", ".zh-TW.md"):
                path = DOCS / (page_path + lang)
                markdown = path.read_text(encoding="utf-8")
                match = re.search(r'<img\s+[^>]*data-motion-src=[^>]*>', markdown)
                assert match and f"{stem}-still.svg" in match.group()
                assert f"{stem}-motion.svg" in match.group() and "CC BY-SA 4.0" in markdown
                image = match.group()
                for reduced in (False, True):
                    for width in (320, 360, 720, 1024):
                        ctx = browser.new_context(
                            viewport={"width": width, "height": 520},
                            reduced_motion="reduce" if reduced else "no-preference",
                        )
                        page = ctx.new_page()
                        source = f"https://qa.example/docs/{path.parent.relative_to(DOCS)}/test.html"
                        html = f"""<!doctype html><html><head><base href="{source}">
                        <style>{css} body{{margin:0;padding:8px}}</style></head><body>
                        <div style="max-width:100%;overflow-x:auto" tabindex="0">
                        <div style="width:640px">{image}</div></div></body></html>"""
                        def intercept(route):
                            from urllib.parse import urlparse
                            name = Path(urlparse(route.request.url).path).name
                            file = ASSETS / name
                            if file.exists() and name.endswith(".svg"):
                                route.fulfill(status=200, content_type="image/svg+xml",
                                              body=file.read_bytes())
                            else:
                                route.abort()
                        page.route("**/concept-animations/*.svg", intercept)
                        page.set_content(html)
                        page.add_script_tag(content=js)
                        img = page.locator("img")
                        img.evaluate("(node)=>node.decode()")
                        assert img.evaluate("(node)=>node.naturalWidth") == 640
                        button = page.locator(".concept-motion-toggle")
                        assert button.count() == 1
                        initial = img.get_attribute("src")
                        assert initial.endswith("-still.svg" if reduced else "-motion.svg")
                        if width < 640:
                            scroll = page.locator("div[tabindex='0']").first.evaluate(
                                "el=>[el.clientWidth,el.scrollWidth]"
                            )
                            assert scroll[0] < scroll[1], (stem, lang, width, scroll)
                        button.focus()
                        page.keyboard.press("Space")
                        assert img.get_attribute("src").endswith(
                            "-motion.svg" if reduced else "-still.svg"
                        )
                        button.focus()
                        page.keyboard.press("Enter")
                        assert img.get_attribute("src") == initial
                        img.evaluate("(node)=>node.decode()")
                        if width == 320:
                            page.screenshot(path=str(OUT / f"{stem}-{lang.strip('.')}-reduce{reduced}.png"))
                        count += 1
                        ctx.close()
        browser.close()
    print(f"Predictive-coding motion Chromium checks: {count} passed")


if __name__ == "__main__":
    main()
