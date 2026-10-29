#!/usr/bin/env python3
"""Chromium regression for the MoCo/BYOL gradient companion and existing slider."""
from pathlib import Path
from math import exp, acos, sin
import re
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
MAIN_JS = (ROOT / "docs/javascripts/self-supervised-labs.js").read_text()
MAIN_CSS = (ROOT / "docs/stylesheets/self-supervised-labs.css").read_text()
GRAD_JS = (ROOT / "docs/javascripts/ssl-gradient-sensitivity.js").read_text()
GRAD_CSS = (ROOT / "docs/stylesheets/ssl-gradient-sensitivity.css").read_text()
OUT = ROOT / "artifacts/ssl-gradient"
OUT.mkdir(parents=True, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
    for kind in ("moco", "byol"):
        for locale in ("en", "zh-TW"):
            for width in (360, 900):
                for reduced in (False, True):
                    page = browser.new_page(
                        viewport={"width": width, "height": 1000},
                        reduced_motion="reduce" if reduced else "no-preference",
                    )
                    errors = []
                    page.on("pageerror", lambda error: errors.append(str(error)))
                    page.set_content(
                        '<!doctype html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"></head><body>'
                        f'<main style="max-width:850px;margin:auto"><div data-self-supervised-lab="{kind}" data-locale="{locale}"></div></main></body></html>'
                    )
                    page.add_style_tag(content=MAIN_CSS)
                    page.add_style_tag(content=GRAD_CSS)
                    page.add_script_tag(content=MAIN_JS)
                    page.add_script_tag(content=GRAD_JS)
                    assert page.locator(".ssl-gradient").count() == 1
                    assert page.locator(".ssl-gradient-plot").count() == 1
                    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth"), (kind, locale, width)
                    slider = page.locator('[data-act="loss"]')
                    if kind == "moco":
                        for tau in (0.10, 0.20, 0.35, 0.50, 1.00):
                            slider.evaluate("(el,v) => {el.value=v; el.dispatchEvent(new Event('input',{bubbles:true}));}", f"{tau:.2f}")
                            readout = page.locator(".ssl-gradient-readout").inner_text()
                            got = float(re.search(r"/τ = (-?[0-9.]+)", readout).group(1))
                            ppos = 1 / (1 + sum(exp((v - .7) / tau) for v in (-.2, -.1, 0, .1, .2, .05)))
                            expected = (ppos - 1) / tau
                            assert abs(got - expected) < .001, (tau, got, expected)
                        slider.evaluate("(el) => {el.value='0.35'; el.dispatchEvent(new Event('input',{bubbles:true}));}")
                    else:
                        for cosine in (-1, -.5, 0, .5, 1):
                            slider.evaluate("(el,v) => {el.value=v; el.dispatchEvent(new Event('input',{bubbles:true}));}", f"{cosine:.2f}")
                            readout = page.locator(".ssl-gradient-readout").inner_text()
                            got = float(re.search(r"2sinφ = ([0-9.]+)", readout).group(1))
                            expected = 2 * sin(acos(cosine))
                            assert abs(got - expected) < .001, (cosine, got, expected)
                        slider.evaluate("(el) => {el.value='0'; el.dispatchEvent(new Event('input',{bubbles:true}));}")
                    assert page.evaluate("""() => {
                      const svg = document.querySelector('.ssl-gradient-plot');
                      return [...svg.querySelectorAll('text')].every(t => {
                        const b = t.getBBox();
                        return b.x >= -1 && b.y >= -1 &&
                               b.x + b.width <= 501 && b.y + b.height <= 167;
                      });
                    }"""), (kind, locale, width, "clipped labels")
                    slider.focus()
                    before = slider.input_value()
                    page.keyboard.press("ArrowRight")
                    assert slider.input_value() != before
                    assert page.locator(".ssl-gradient-readout").inner_text()
                    assert not errors, errors
                    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
                    page.locator(".ssl-gradient").screenshot(
                        path=str(OUT / f"{kind}-{locale}-{width}-reduced-{reduced}.png")
                    )
                    page.close()
    browser.close()
print("PASS: 16 Chromium cases, analytic derivatives, keyboard, reduced motion, SVG bounds, responsive layout")
