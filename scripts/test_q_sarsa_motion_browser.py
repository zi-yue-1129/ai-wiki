#!/usr/bin/env python3
"""Chromium regression for the Q-learning / SARSA TD target comparison."""
from __future__ import annotations
import os
from pathlib import Path
from xml.etree import ElementTree as ET
from playwright.sync_api import sync_playwright

ASSETS = Path("docs/assets/concept-animations")
PLAYER = Path("docs/javascripts/concept-motion.js")
OUT = Path("artifacts/q-sarsa-backup")
NS = "{http://www.w3.org/2000/svg}"

def run():
    motion = ASSETS / "q-sarsa-backup-motion.svg"
    still = ASSETS / "q-sarsa-backup-still.svg"
    for p in (motion, still):
        root = ET.parse(p).getroot()
        assert root.tag == NS + "svg" and root.get("viewBox") == "0 0 640 360"
        assert root.find(NS + "title") is not None and root.find(NS + "desc") is not None
        assert p.stat().st_size < 50000
        for e in root.iter():
            assert e.tag.split("}")[-1] not in ("script","foreignObject","iframe","image")
            assert not any(k.split("}")[-1].startswith("on") for k in e.attrib)
            assert not any(v.startswith(("https:","http:","data:","javascript:")) for k,v in e.attrib.items() if k.split("}")[-1]=="href")
    animated = ET.parse(motion).getroot().findall(".//"+NS+"animate")
    assert len(animated) >= 6
    assert all(n.get("repeatCount")=="indefinite" and n.get("dur")=="10s" for n in animated)
    assert not ET.parse(still).getroot().findall(".//"+NS+"animate")
    assert abs(2+0.5*(1+0.9*5-2)-3.75)<1e-12
    assert abs(2+0.5*(1+0.9*2-2)-2.4)<1e-12
    m,s = motion.read_text(),still.read_text()
    OUT.mkdir(parents=True,exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True, executable_path=os.environ.get("CHROMIUM_EXECUTABLE") or None, args=["--no-sandbox"])
        for width in (320,360,720,1024):
            for seconds in (0.25,2.5,4.5,7.8):
                pg=b.new_page(viewport={"width":width,"height":int(width*360/640)+8})
                pg.set_content("<style>body{margin:0}svg{display:block;width:100%;height:auto}</style>"+m)
                pg.evaluate('document.querySelector("svg").pauseAnimations()')
                pg.evaluate('(t)=>document.querySelector("svg").setCurrentTime(t)',seconds)
                opacity=float(pg.locator("#q-target").evaluate("(e)=>getComputedStyle(e).opacity"))
                assert (opacity<0.1 if seconds<3.8 else opacity>0.9), (seconds,opacity)
                value=pg.locator("#q-updated-bar").evaluate("(e)=>e.width.animVal.value")
                assert (58.5<value<60 if seconds<5.2 else 110<value<112 if seconds>7.7 else True)
                boxes=pg.locator("svg text").evaluate_all("els=>els.map(e=>{let b=e.getBBox();return [b.x,b.y,b.width,b.height]})")
                assert all(x>=0 and y>=0 and x+w<=640.1 and y+h<=360.1 for x,y,w,h in boxes)
                pg.locator("svg").screenshot(path=str(OUT/f"motion-{width}-{seconds}.png"))
                pg.close()
            pg=b.new_page(viewport={"width":width,"height":int(width*360/640)+8})
            pg.set_content("<style>body{margin:0}svg{display:block;width:100%;height:auto}</style>"+s)
            assert pg.locator("#q-updated").is_visible() and pg.locator("#s-updated").is_visible()
            pg.locator("svg").screenshot(path=str(OUT/f"still-{width}.png"))
            pg.close()
        assert PLAYER.exists()
        for alt in ("Q-learning and SARSA comparison","Q-learning 與 SARSA 的備份比較"):
            for mode in ("no-preference","reduce"):
                cx=b.new_context(reduced_motion=mode)
                pg=cx.new_page()
                host="https://local.invalid/assets/"
                pg.route("https://local.invalid/assets/**",lambda route:route.fulfill(body=m if "-motion.svg" in route.request.url else s,content_type="image/svg+xml"))
                pg.set_content(f'<img alt="{alt}" src="{host}q-sarsa-backup-still.svg" data-motion-src="{host}q-sarsa-backup-motion.svg" data-still-src="{host}q-sarsa-backup-still.svg">')
                pg.add_script_tag(content=PLAYER.read_text())
                button=pg.locator(".concept-motion-toggle")
                button.wait_for(state="visible", timeout=5000)
                assert button.count()==1
                assert ("-still.svg" if mode=="reduce" else "-motion.svg") in pg.locator("img").get_attribute("src")
                button.focus();pg.keyboard.press("Enter")
                assert ("-motion.svg" if mode=="reduce" else "-still.svg") in pg.locator("img").get_attribute("src")
                button.focus();pg.keyboard.press("Space")
                assert ("-still.svg" if mode=="reduce" else "-motion.svg") in pg.locator("img").get_attribute("src")
                cx.close()
        b.close()
    print("PASS: 20 responsive renders, SVG security, timeline, keyboard, and reduced motion")

if __name__ == "__main__":
    run()
