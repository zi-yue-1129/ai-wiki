#!/usr/bin/env python3
"""Browser QA: two distinct RL curiosity learning-signal diagrams."""
from pathlib import Path
from xml.etree import ElementTree as ET
from playwright.sync_api import sync_playwright

DOCS = Path(__file__).resolve().parents[1] / "docs"
ASSETS = DOCS / "assets/concept-animations"
REVIEW = Path(__file__).resolve().parents[1] / "artifacts/rnd-icm-motion"

def run():
    names = ("rnd-learning-paths", "icm-auxiliary-gradients")
    for name in names:
        motion = (ASSETS / f"{name}-motion.svg").read_text(encoding="utf-8")
        still = (ASSETS / f"{name}-still.svg").read_text(encoding="utf-8")
        for body in (motion, still):
            root = ET.fromstring(body)
            assert root.attrib["viewBox"].startswith("0 0 360 ")
            assert root.attrib["role"] == "img"
            assert "<script" not in body and "href=" not in body and "onload=" not in body
            assert "https://" not in body and "http://" not in body.replace("http://www.w3.org/2000/svg", "")
        assert "animateMotion" in motion and 'repeatCount="indefinite"' in motion
        assert "animateMotion" not in still and "<animate " not in still
        assert "prefers-reduced-motion" in motion
    REVIEW.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True,
            executable_path="/usr/bin/chromium" if Path("/usr/bin/chromium").exists() else None,
            args=["--no-sandbox"])
        try:
            for name in names:
                motion = (ASSETS / f"{name}-motion.svg").read_text(encoding="utf-8")
                still = (ASSETS / f"{name}-still.svg").read_text(encoding="utf-8")
                for width in (320, 360, 720, 1024):
                    page = browser.new_page(viewport={"width": width, "height": 1280})
                    errors = []
                    page.on("pageerror", lambda error: errors.append(str(error)))
                    page.set_content('<body style="margin:0"><main style="max-width:360px">' +
                                     motion + '</main></body>')
                    page.locator("svg").evaluate("s => {s.style.width='100%';s.style.height='auto'}")
                    for t in (0.3, 2.5, 5.5, 7.8):
                        page.evaluate("t => {const s=document.querySelector('svg');s.setCurrentTime(t);s.pauseAnimations()}", t)
                        page.locator("svg").screenshot(path=str(REVIEW / f"{name}-{width}-{str(t).replace('.', '_')}.png"))
                    assert not errors, errors
                    assert not page.evaluate("document.documentElement.scrollWidth > innerWidth + 1"), (name, width)
                    if name == "rnd-learning-paths":
                        def bar_at(t):
                            return page.evaluate("""t => {const s=document.querySelector('svg');
                              s.setCurrentTime(t);s.pauseAnimations();
                              return s.querySelector('rect[fill="#dd9144"]').width.animVal.value;}""", t)
                        assert bar_at(8.5) < bar_at(3.0), (name, width)
                    page.close()
                    # Pause animations for reduced-motion users even if they open the SVG directly.
                    page = browser.new_page(viewport={"width":width,"height":1280}, reduced_motion="reduce")
                    page.set_content('<body style="margin:0"><main style="max-width:360px">'+motion+'</main></body>')
                    assert page.locator("g.pulse").first.evaluate("el => getComputedStyle(el).display") == "none"
                    page.close()
                    page = browser.new_page(viewport={"width":width,"height":1280})
                    page.set_content('<body style="margin:0"><main style="max-width:360px">'+still+'</main></body>')
                    page.locator("svg").screenshot(path=str(REVIEW / f"{name}-{width}-still.png"))
                    assert not page.evaluate("document.documentElement.scrollWidth > innerWidth + 1")
                    page.close()
                # Real wiki player, including keyboard toggle and no-motion default.
                player = (DOCS / "javascripts/concept-motion.js").read_text(encoding="utf-8")
                uri = "http://127.0.0.1:9/docs/assets/concept-animations/" + name
                for reduced in (False, True):
                    ctx = browser.new_context(viewport={"width":320,"height":900},
                        reduced_motion="reduce" if reduced else "no-preference")
                    page = ctx.new_page()
                    page.set_content(f'<img alt="Instructional motion" src="{uri}-still.svg" '
                        f'data-motion-src="{uri}-motion.svg" data-still-src="{uri}-still.svg">')
                    page.add_script_tag(content=player)
                    img = page.locator("img")
                    if reduced:
                        assert img.get_attribute("src").endswith("-still.svg")
                    else:
                        assert img.get_attribute("src").endswith("-motion.svg")
                        page.get_by_role("button", name="Pause concept animation").click()
                        assert img.get_attribute("src").endswith("-still.svg")
                    page.get_by_role("button", name="Play concept animation").focus()
                    page.keyboard.press("Enter")
                    assert img.get_attribute("src").endswith("-motion.svg")
                    ctx.close()
        finally:
            browser.close()
    print("PASS: 2 motion topics, 4 widths, 4 phases, reduced motion, static fallback and keyboard player")

if __name__ == "__main__":
    run()



def check_target_drift():
    """Check isolated updates, responsive snapshots, and shared player controls."""
    from xml.etree import ElementTree as ET
    name = "rnd-icm-target-drift"
    motion = (ASSETS / (name + "-motion.svg")).read_text(encoding="utf-8")
    still = (ASSETS / (name + "-still.svg")).read_text(encoding="utf-8")
    for body in (motion, still):
        root = ET.fromstring(body)
        assert root.attrib["role"] == "img"
        assert root.attrib["viewBox"].startswith("0 0 360 ")
        assert "<script" not in body and "href=" not in body and "onload=" not in body
        assert "https://" not in body and "http://" not in body.replace("http://www.w3.org/2000/svg", "")
    assert len(ET.fromstring(motion).findall(".//{*}animate")) >= 8
    assert len(ET.fromstring(still).findall(".//{*}animate")) == 0
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True,
            executable_path="/usr/bin/chromium" if Path("/usr/bin/chromium").exists() else None,
            args=["--no-sandbox"])
        for width in (320, 360, 720, 1024):
            page = browser.new_page(viewport={"width": width, "height": 1050})
            page.set_content('<main style="max-width:360px">' + motion + "</main>")
            def coords(t):
                return page.evaluate("""t => {const s=document.querySelector('svg');
                    s.setCurrentTime(t);s.pauseAnimations();
                    const a=s.querySelectorAll('g.live circle.target');
                    const b=s.querySelectorAll('g.live rect.predict');
                    return [a[0].cx.animVal.value,a[1].cx.animVal.value,
                            b[0].x.animVal.value,b[1].x.animVal.value];}""", t)
            initial, drifted, fitted = coords(1), coords(5.8), coords(10.5)
            assert initial[0] == drifted[0] == fitted[0]  # frozen RND target
            assert drifted[1] > initial[1] + 40  # movable ICM target
            assert initial[2:] == drifted[2:]  # no predictor update yet
            assert fitted[2] > drifted[2] + 90 and fitted[3] > drifted[3] + 130
            for t in (1, 4, 6.2, 9.4, 11):
                coords(t)
                page.locator('svg').screenshot(path=str(REVIEW / f"{name}-{width}-{str(t).replace('.', '_')}.png"))
            assert not page.evaluate("document.documentElement.scrollWidth > innerWidth + 1")
            page.close()
            page = browser.new_page(viewport={"width": width, "height": 1050}, reduced_motion="reduce")
            page.set_content("<main>" + motion + "</main>")
            assert page.locator("g.live").evaluate("e=>getComputedStyle(e).display") == "none"
            assert page.locator("g.reduced-frame").evaluate("e=>getComputedStyle(e).display") != "none"
            page.locator("svg").screenshot(path=str(REVIEW / f"{name}-{width}-reduced.png"))
            page.close()
            page = browser.new_page(viewport={"width": width, "height": 1050})
            page.set_content("<main>" + still + "</main>")
            page.locator("svg").screenshot(path=str(REVIEW / f"{name}-{width}-still.png"))
            page.close()
        player = (DOCS / "javascripts/concept-motion.js").read_text(encoding="utf-8")
        uri = "http://127.0.0.1:9/docs/assets/concept-animations/" + name
        for reduced in (False, True):
            page = browser.new_page(viewport={"width": 320, "height": 900},
                reduced_motion="reduce" if reduced else "no-preference")
            page.set_content(f'<img alt="Target comparison" src="{uri}-still.svg" '
                f'data-motion-src="{uri}-motion.svg" data-still-src="{uri}-still.svg">')
            page.add_script_tag(content=player)
            im = page.locator("img")
            if reduced:
                assert im.get_attribute("src").endswith("-still.svg")
            else:
                assert im.get_attribute("src").endswith("-motion.svg")
                page.get_by_role("button", name="Pause concept animation").click()
                assert im.get_attribute("src").endswith("-still.svg")
            page.get_by_role("button", name="Play concept animation").focus()
            page.keyboard.press("Enter")
            assert im.get_attribute("src").endswith("-motion.svg")
            page.close()
        browser.close()
    print("PASS: target drift, 4 widths, 5 phases, reduced motion, static fallback, keyboard player")


if __name__ == "__main__":
    check_target_drift()
