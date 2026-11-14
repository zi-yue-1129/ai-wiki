"""Bilingual responsive and numerical checks for RoIAlign / SAM toy labs.

Run after `python -m playwright install chromium`. No external URLs needed.
"""
from pathlib import Path
import os
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
JS = ROOT / "docs/javascripts/segmentation-labs.js"
CSS = ROOT / "docs/stylesheets/segmentation-labs.css"
TOPIC = ROOT / "docs/theory/models/computer-vision/segmentation"
OUTPUT = ROOT / "artifacts/segmentation-labs"


def main():
    for base in ("mask-r-cnn", "segment-anything"):
        for suffix in (".md", ".zh-TW.md"):
            text = (TOPIC / f"{base}{suffix}").read_text(encoding="utf-8")
            expected = 'data-seg-lab="roi"' if base == "mask-r-cnn" else 'data-seg-lab="sam"'
            assert expected in text, (base, suffix, "missing lab")
            assert "-still.svg" in text, (base, suffix, "missing static fallback")
            assert "data-motion-src" in text, (base, suffix, "missing motion")
    source = JS.read_text(encoding="utf-8")
    css = CSS.read_text(encoding="utf-8")
    OUTPUT.mkdir(parents=True, exist_ok=True)
    html = ('<!doctype html><html><head><meta charset="UTF-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<style>*{{box-sizing:border-box}}body{{max-width:900px;margin:auto;padding:12px;font-family:Arial,sans-serif}}</style>'
            '</head><body><div data-seg-lab="roi" data-lang="{lang}"></div>'
            '<div data-seg-lab="sam" data-lang="{lang}"></div></body></html>')
    with sync_playwright() as p:
        chromium = p.chromium.launch(headless=True, executable_path=os.environ.get("SEGMENTATION_CHROMIUM"))
        for lang in ("en", "zh"):
            for width in (320, 360, 720, 1024):
                for reduced in (False, True):
                    page = chromium.new_page(viewport={"width": width, "height": 800},
                        reduced_motion="reduce" if reduced else "no-preference")
                    errors = []
                    page.on("pageerror", lambda error: errors.append(str(error)))
                    page.set_content(html.format(lang=lang))
                    page.add_style_tag(content=css)
                    page.add_script_tag(content=source)
                    assert not errors, errors
                    roi = page.locator('[data-seg-lab="roi"]')
                    sam = page.locator('[data-seg-lab="sam"]')
                    assert roi.locator('svg rect').count() >= 18
                    assert sam.locator('svg rect').count() >= 68
                    # Values are calculated from 2-D grid, not literal bars.
                    initial = roi.locator('[data-readout]').inner_text()
                    roi.locator('[data-axis="x"]').fill("2.4")
                    assert initial != roi.locator('[data-readout]').inner_text()
                    assert roi.locator('[data-out="x"]').inner_text() == "2.4"
                    roi.locator('[data-action="seek"]').fill("3")
                    assert "0.796" in roi.locator('[data-readout]').inner_text()
                    roi.locator('[data-action="prev"]').click()
                    assert roi.locator('[data-action="seek"]').input_value() == "2"
                    roi.locator('[data-action="speed"]').select_option("2")
                    roi.locator('[data-action="reset"]').click()
                    assert roi.locator('[data-out="x"]').inner_text() == "1.3"
                    assert roi.locator('[data-action="seek"]').input_value() == "0"
                    # Different nested masks and constraint change visible state.
                    original = sam.locator('[data-readout]').inner_text()
                    sam.locator('[data-pick="mask"]').select_option("2")
                    sam.locator('[data-pick="box"]').check()
                    sam.locator('[data-action="seek"]').fill("3")
                    updated = sam.locator('[data-readout]').inner_text()
                    assert original != updated
                    assert sam.locator('svg line[stroke="#c55050"]').count() == 2
                    sam.locator('[data-action="reset"]').click()
                    assert not sam.locator('[data-pick="box"]').is_checked()
                    # Reduced motion must not autoplay even after an explicit press.
                    roi.locator('[data-action="toggle"]').click()
                    if reduced:
                        assert roi.locator('[data-action="toggle"]').inner_text() in ("Play", "播放")
                    else:
                        assert roi.locator('[data-action="toggle"]').inner_text() in ("Pause", "暫停")
                        roi.locator('[data-action="toggle"]').click()
                    doc = page.evaluate('({scroll:document.documentElement.scrollWidth,client:document.documentElement.clientWidth})')
                    assert doc['scroll'] <= doc['client'] + 2, (lang,width,doc)
                    if width in (320,1024) and not reduced:
                        page.screenshot(path=str(OUTPUT / f"{lang}-{width}.png"),full_page=True)
                    print(f"PASS {lang} {width}px reduce={reduced}")
                    page.close()
        chromium.close()


if __name__ == "__main__":
    main()
