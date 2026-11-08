#!/usr/bin/env python3
"""Real Chromium regression for original bilingual RND/ICM timeline probes."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import re

ROOT = Path(__file__).resolve().parents[1]
JS = ROOT / "docs/javascripts/curiosity-labs.js"
CSS = ROOT / "docs/stylesheets/curiosity-labs.css"
OUT = ROOT / "artifacts/rnd-icm-motion"
OUT.mkdir(parents=True, exist_ok=True)

def choose(host, n):
    control = host.locator('input[type="range"]')
    control.evaluate("(e,n) => {e.value=String(n);e.dispatchEvent(new Event('input',{bubbles:true}));}", n)

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for width in (320, 360, 720, 1024):
            context = browser.new_context(viewport={"width":width,"height":1100})
            page = context.new_page()
            html = ('<html><head><style>body{margin:0;padding:8px;font-family:Arial,sans-serif}'
                    + CSS.read_text() + '</style></head><body>'
                    + '<div data-curiosity-lab="rnd" data-locale="en">RND fallback</div>'
                    + '<div data-curiosity-lab="icm" data-locale="zh-TW">ICM fallback</div>'
                    + '</body></html>')
            page.set_content(html)
            page.add_script_tag(content=JS.read_text())
            assert page.locator("svg").count() == 2
            assert page.locator("button").count() == 6
            for kind, states in (("rnd", (0,2,3,4,6,7)), ("icm", (0,2,3,4,5))):
                host = page.locator('[data-curiosity-lab="' + kind + '"]')
                for state in states:
                    choose(host, state)
                    assert host.locator("svg").count() == 1
                    if kind == "icm":
                        assert "特徵空間示意" in host.locator("svg").get_attribute("aria-label")
                    else:
                        assert "schematic feature-space" in host.locator("svg").get_attribute("aria-label")
                    assert host.locator("output").text_content().startswith(
                        "Step " if kind == "rnd" else "步驟 ")
                    (OUT / f"probe_{kind}_{width}_{state}.png").write_bytes(host.screenshot())
                if kind == "rnd":
                    choose(host, 0)
                    assert "19.10" in host.locator("svg").text_content()
                    choose(host, 3)
                    assert "0.03" in host.locator("svg").text_content()
                    choose(host, 4)
                    assert "Obs B" in host.locator("svg").text_content()
                    assert "19.13" in host.locator("svg").text_content()
                else:
                    for index,val in ((3,"3.87"),(4,"1.94"),(5,"3.25")):
                        choose(host,index)
                        content = host.locator("svg").text_content()
                        assert "3.02" in content and val in content, content
            # Real mouse and keyboard actions, not just DOM existence.
            host=page.locator('[data-curiosity-lab="rnd"]')
            choose(host,2)
            host.get_by_role("button", name="Next step").focus()
            page.keyboard.press("Enter")
            assert "Step 4/8" in host.locator("output").text_content()
            host.get_by_role("button", name="Play").click()
            assert host.get_by_role("button", name="Pause").count() == 1
            host.get_by_role("button", name="Pause").click()
            assert host.get_by_role("button", name="Play").count() == 1
            context.close()
        context = browser.new_context(viewport={"width":360,"height":1000},
                                      reduced_motion="reduce")
        page=context.new_page()
        page.set_content('<div data-curiosity-lab="rnd" data-locale="en"></div>'
                         '<div data-curiosity-lab="icm" data-locale="en"></div>')
        page.add_script_tag(content=JS.read_text())
        assert page.get_by_role("button", name="Play").count() == 2
        for button in page.get_by_role("button", name="Play").all():
            assert button.is_disabled()
        rnd=page.locator('[data-curiosity-lab="rnd"]')
        choose(rnd,4)
        assert "Obs B" in rnd.locator("svg").text_content()
        context.close()
        browser.close()
    print("PASS curiosity probes: responsive renders, arithmetic, keyboard, timeline, reduced motion")

if __name__ == "__main__":
    run()
