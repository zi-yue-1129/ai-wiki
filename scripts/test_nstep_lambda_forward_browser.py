"""Chromium regression for forward n-step SARSA and truncated lambda returns."""
from pathlib import Path
from xml.etree import ElementTree as ET
from playwright.sync_api import sync_playwright
import os

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "docs/assets/concept-animations"
OUT = ROOT / "artifacts/nstep-lambda-forward"
NS = "{http://www.w3.org/2000/svg}"

def main():
    motion = ASSETS / "nstep-lambda-forward-motion.svg"
    still = ASSETS / "nstep-lambda-forward-still.svg"
    for asset in (motion, still):
        root = ET.parse(asset).getroot()
        assert root.get("viewBox") == "0 0 520 626"
        for el in root.iter():
            assert el.tag.split("}")[-1] not in {"script", "image", "foreignObject", "iframe"}
            assert all(not k.split("}")[-1].startswith("on") for k in el.attrib)
            assert all(not v.startswith(("javascript:", "http:", "https:", "data:")) for v in el.attrib.values())
    assert len(ET.parse(motion).findall(".//" + NS + "animate")) >= 8
    assert not ET.parse(still).findall(".//" + NS + "animate")
    assert abs(.2 * 3.7 + .16 * .91 + .64 * 4.798 - 3.95632) < 1e-9
    assert {"3.700", "0.910", "4.798", "Gλ = 3.95632"}.issubset({(e.text or "").strip() for e in ET.parse(still).iter()})
    for topic in ("sarsa", "q-learning"):
        for language in ("index.md", "index.zh-TW.md"):
            page = ROOT / "docs/theory/paradigms/reinforcement-learning/value-based-methods" / topic / language
            body = page.read_text(encoding="utf-8")
            assert "nstep-lambda-forward-motion.svg" in body
            assert "nstep-lambda-forward-still.svg" in body
            assert "Sutton" in body
    OUT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        opts = {"headless": True, "args": ["--no-sandbox"]}
        if os.environ.get("CHROMIUM_EXECUTABLE"):
            opts["executable_path"] = os.environ["CHROMIUM_EXECUTABLE"]
        browser = p.chromium.launch(**opts)
        for width in (320, 360, 720, 1024):
            for sec in (0.6, 3.0, 5.5, 8.8, 11.0):
                page = browser.new_page(viewport={"width": width, "height": max(900, width * 2)})
                page.set_content('<style>body{margin:0}svg{display:block;width:100%;height:auto}</style>' + motion.read_text(encoding="utf-8"))
                page.locator("svg").evaluate("(el,t)=>{el.pauseAnimations();el.setCurrentTime(t)}", sec)
                assert page.evaluate("document.documentElement.scrollWidth<=innerWidth")
                boxes = page.locator("svg text").evaluate_all("els=>els.map(e=>{let b=e.getBBox();return [b.x,b.y,b.width,b.height]})")
                assert all(x >= -1 and y >= -1 and x+w <= 521 and y+h <= 627 for x,y,w,h in boxes)
                def bar(y,color):
                    return page.locator(f'svg rect[y="{y}"][fill="{color}"]').evaluate("el=>el.getBBox().width")
                if sec == 3.0:
                    assert 60 < bar(266,"#3285c5") < 92
                if sec == 5.5:
                    assert abs(bar(266,"#3285c5") - 92) < 1
                    assert 100 < bar(346,"#7765c6") < 188
                if sec >= 8.8:
                    assert abs(bar(266,"#3285c5") - 92) < 1
                    assert abs(bar(346,"#7765c6") - 188) < 1
                    assert abs(bar(426,"#259985") - 286) < 1
                page.locator("svg").screenshot(path=str(OUT / f"motion-{width}-{str(sec).replace('.', '_')}.png"))
                page.close()
            pg=browser.new_page(viewport={"width":width,"height":max(900,width*2)})
            pg.set_content('<style>body{margin:0}svg{display:block;width:100%;height:auto}</style>'+still.read_text(encoding="utf-8"))
            assert pg.locator("svg animate").count()==0
            pg.locator("svg").screenshot(path=str(OUT/f"still-{width}.png"))
            pg.close()
        player=(ROOT/"docs/javascripts/concept-motion.js").read_text(encoding="utf-8")
        host="https://local.invalid/concept-animations/"
        for alt in ("Three-step SARSA returns","SARSA 三步報酬"):
            for mode in ("no-preference","reduce"):
                context=browser.new_context(reduced_motion=mode)
                pg=context.new_page()
                pg.route(host+"**",lambda route:route.fulfill(
                    body=motion.read_text(encoding="utf-8") if "-motion.svg" in route.request.url else still.read_text(encoding="utf-8"),
                    content_type="image/svg+xml"))
                pg.set_content(f'<img alt="{alt}" src="{host}nstep-lambda-forward-still.svg" data-motion-src="{host}nstep-lambda-forward-motion.svg" data-still-src="{host}nstep-lambda-forward-still.svg">')
                pg.add_script_tag(content=player)
                button=pg.locator(".concept-motion-toggle")
                button.wait_for(state="visible",timeout=8000)
                first="-motion.svg" if mode=="no-preference" else "-still.svg"
                other="-still.svg" if mode=="no-preference" else "-motion.svg"
                assert first in pg.locator("img").get_attribute("src")
                button.focus()
                pg.keyboard.press("Enter")
                assert other in pg.locator("img").get_attribute("src")
                button.focus()
                pg.keyboard.press("Space")
                assert first in pg.locator("img").get_attribute("src")
                context.close()
        browser.close()
    print("PASS: 24 responsive screenshots, exact returns, keyboard and reduced motion")

if __name__=="__main__":
    main()
