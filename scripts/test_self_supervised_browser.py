#!/usr/bin/env python3
"""Chromium E2E: real SVG geometry, controls, reduced motion and mobile layout."""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
JS = (ROOT / "docs/javascripts/self-supervised-labs.js").read_text()
CSS = (ROOT / "docs/stylesheets/self-supervised-labs.css").read_text()
OUT = ROOT / "artifacts/self-supervised-labs"
OUT.mkdir(parents=True, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
    for kind in ("moco", "byol"):
        for width in (360, 900):
            for reduced in (False, True):
                page = browser.new_page(
                    viewport={"width": width, "height": 850},
                    reduced_motion="reduce" if reduced else "no-preference",
                )
                errors = []
                page.on("pageerror", lambda error: errors.append(str(error)))
                page.set_content(
                    '<!doctype html><meta name="viewport" content="width=device-width,initial-scale=1">'
                    f'<div data-self-supervised-lab="{kind}" data-locale="zh-TW"></div>'
                )
                page.add_style_tag(content=CSS)
                page.add_script_tag(content=JS)
                packet = page.locator(".ssl-packet")
                assert packet.count() == 1
                assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
                if reduced:
                    assert packet.evaluate("(e) => getComputedStyle(e).display") == "none"
                else:
                    assert packet.evaluate("(e) => getComputedStyle(e).display") != "none"
                # Inspect actual SVG label bounds, not just XML syntax.
                assert page.evaluate("""() => {
                    const svg = document.querySelector('.ssl-figure svg');
                    return [...svg.querySelectorAll('text')].every(t => {
                        const b = t.getBBox();
                        return b.x >= -1 && b.y >= -1 &&
                               b.x + b.width <= 641 && b.y + b.height <= 261;
                    });
                }"""), (kind, width, reduced, "SVG text clipped")
                page.locator('[data-act="seek"]').fill("4")
                calc = page.locator(".ssl-compute").inner_text()
                assert "0.355" in calc, (kind, calc)
                if kind == "moco":
                    assert "FIFO [B C D E F G]" in calc
                else:
                    assert "Target gradient = 0" in calc or "目標梯度 = 0" in calc
                page.locator('[data-act="prev"]').click()
                assert page.locator('[data-act="seek"]').input_value() == "3"
                page.locator('[data-act="next"]').focus()
                page.keyboard.press("Enter")
                assert page.locator('[data-act="seek"]').input_value() == "4"
                page.locator('[data-act="speed"]').select_option("2")
                if not reduced:
                    page.locator('[data-act="seek"]').fill("0")
                    start = packet.get_attribute("cx")
                    page.locator('[data-act="play"]').click()
                    page.wait_for_timeout(250)
                    assert packet.get_attribute("cx") != start, "packet did not move"
                    page.locator('[data-act="play"]').click()
                    paused = packet.get_attribute("cx")
                    page.wait_for_timeout(160)
                    assert packet.get_attribute("cx") == paused, "pause did not freeze particle"
                assert not errors, errors
                page.screenshot(
                    path=str(OUT / f"{kind}-{width}-reduced-{reduced}.png"),
                    full_page=True,
                )
                page.close()
    browser.close()
print("PASS: 8 Chromium cases, bilingual controls, geometry, seek, keyboard, tween, pause, reduced motion")
