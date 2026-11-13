#!/usr/bin/env python3
"""Chromium integration QA for the navigation concept-motion SVGs.

Tests the repository's real shared JS/CSS and exact SVG image bytes without network access.
The screenshot artifacts are for reviewing text, geometry and narrow-screen legibility.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "docs" / "assets" / "concept-animations"
JS = (ROOT / "docs" / "javascripts" / "concept-motion.js").read_text(encoding="utf-8")
CSS = (ROOT / "docs" / "stylesheets" / "concept-motion.css").read_text(encoding="utf-8")
SHOTS = ROOT / "artifacts" / "navigation-motion"
SHOTS.mkdir(parents=True, exist_ok=True)


def exercise_player(browser, name, language, reduced, width):
    page = browser.new_page(
        viewport={"width": width, "height": 700},
        reduced_motion="reduce" if reduced else "no-preference",
    )
    def route_asset(route):
        path = ASSETS / route.request.url.rsplit("/", 1)[-1]
        assert path.is_file(), path
        route.fulfill(status=200, content_type="image/svg+xml", body=path.read_bytes())

    page.route("**/concept-animations/*", route_asset)
    alt = "位置標記與折扣造訪" if language == "zh" else "Moving marker and occupancy"
    src = f"https://docs.example.test/concept-animations/{name}-motion.svg"
    page.set_content(
        f'<html><head><style>body{{margin:0}} {CSS}</style></head>'
        f'<body><main style="max-width:720px;margin:auto">'
        f'<img src="{src}" alt="{alt}"></main></body></html>'
    )
    page.add_script_tag(content=JS)
    page.wait_for_timeout(50)
    host = page.locator(".concept-motion-player")
    button = page.locator(".concept-motion-toggle")
    img = page.locator("main img")
    assert host.count() == 1 and button.count() == 1
    assert img.evaluate("(el)=>el.naturalWidth") == 640, "SVG image did not decode"
    assert host.get_attribute("tabindex") == "0"
    play = "播放" if language == "zh" else "Play"
    pause = "暫停" if language == "zh" else "Pause"
    assert (play in button.inner_text()) is reduced
    assert (pause in button.inner_text()) is (not reduced)
    assert img.get_attribute("src").endswith("-still.svg" if reduced else "-motion.svg")
    button.click()
    assert img.get_attribute("src").endswith("-motion.svg" if reduced else "-still.svg")
    button.focus()
    page.keyboard.press("Space")
    assert img.get_attribute("src").endswith("-still.svg" if reduced else "-motion.svg")
    # Enter is the second supported keyboard activation route.
    page.keyboard.press("Enter")
    assert img.get_attribute("src").endswith("-motion.svg" if reduced else "-still.svg")
    if width <= 360:
        sizes = host.evaluate("(el)=>({scroll:el.scrollWidth,client:el.clientWidth})")
        assert sizes["scroll"] > sizes["client"], sizes
        host.focus()
        page.keyboard.press("ArrowRight")
        page.wait_for_timeout(100)
        assert host.evaluate("(el)=>el.scrollLeft") > 0
    if width in (320, 720):
        page.screenshot(path=str(SHOTS / f"{name}-{language}-{width}-reduced{int(reduced)}.png"))
    page.close()


def exercise_motion(browser, name):
    svg = (ASSETS / f"{name}-motion.svg").read_text(encoding="utf-8")
    page = browser.new_page(viewport={"width": 720, "height": 400})
    page.set_content(f'<html><body style="margin:0">{svg}</body></html>')
    for seconds in (0, 3, 6, 9, 11.5, 13):
        page.evaluate("(t)=>document.querySelector('svg').setCurrentTime(t)", seconds)
        boxes = page.evaluate("""() => [...document.querySelectorAll('svg text')].map(el=>{
            let b=el.getBBox(); return [b.x,b.y,b.width,b.height];
        })""")
        assert all(x >= -1 and y >= -1 and x+w <= 641 and y+h <= 361
                   for x,y,w,h in boxes), (name, seconds, boxes)
    if name == "place-cell-firing":
        a = page.locator('animate[attributeName="width"]')
        assert a.count() == 3, "each place-cell rate requires independent movement"
        rect = a.first.evaluate("(el)=>el.parentNode")
        page.evaluate("document.querySelector('svg').setCurrentTime(0)")
        first = rect.evaluate("(el)=>el.width.baseVal.value")
        page.evaluate("document.querySelector('svg').setCurrentTime(6)")
        later = rect.evaluate("(el)=>el.width.animVal.value")
        assert first > 80 and later < 10, (first, later)
    else:
        bars = page.locator('animate[attributeName="height"]')
        assert bars.count() == 5
        page.evaluate("document.querySelector('svg').setCurrentTime(8.8)")
        reward_before = page.locator('text').filter(has_text="V=0.24").first.evaluate("(el)=>getComputedStyle(el).opacity")
        page.evaluate("document.querySelector('svg').setCurrentTime(10.0)")
        reward_after = page.locator('text').filter(has_text="V=0.49").first.evaluate("(el)=>getComputedStyle(el).opacity")
        assert reward_before == "1" and reward_after == "1", (reward_before, reward_after)
    page.close()


if __name__ == "__main__":
    total = 0
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        for name in ("place-cell-firing", "successor-occupancy"):
            exercise_motion(browser, name)
            for language in ("en", "zh"):
                for reduced in (False, True):
                    for width in (320, 360, 720, 1024):
                        exercise_player(browser, name, language, reduced, width)
                        total += 1
        browser.close()
    print(f"Navigation motion: {total} player cases + 2 animated SVG geometry/semantics cases passed")
