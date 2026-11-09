#!/usr/bin/env python3
"""Check action-aliasing teaching motion and its no-script fallback."""
from pathlib import Path
from xml.etree import ElementTree as ET
from playwright.sync_api import sync_playwright

ASSETS = Path(__file__).resolve().parents[1] / 'docs/assets/concept-animations'

def run():
    files = [ASSETS / f'icm-action-aliasing-{variant}.svg' for variant in ('motion', 'still')]
    motion, still = [f.read_text(encoding='utf-8') for f in files]
    for svg in (motion, still):
        root = ET.fromstring(svg)
        assert root.attrib['viewBox'] == '0 0 480 448'
        assert '<script' not in svg and 'href=' not in svg and 'onload=' not in svg
        assert 'http://' not in svg.replace('http://www.w3.org/2000/svg', '') and 'https://' not in svg
        assert svg.count('cx="380"') == 2
    assert motion.count('repeatCount="indefinite"') == 6
    assert '<animate ' not in still
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, executable_path=(
            '/usr/bin/chromium' if Path('/usr/bin/chromium').exists() else None), args=['--no-sandbox'])
        try:
            for width in (320, 360, 720, 1024):
                page = browser.new_page(viewport={'width': width, 'height': 1000})
                page.set_content('<body style="margin:0"><div style="max-width:480px">' + motion + '</div></body>')
                page.locator('svg').evaluate("svg => {svg.style.width='100%';svg.style.height='auto'}")
                def stroke_opacities(t):
                    return page.evaluate('''t => { let svg=document.querySelector('svg');
                       svg.setCurrentTime(t);svg.pauseAnimations();
                       return [...svg.querySelectorAll('rect[stroke="#2d88c5"],rect[stroke="#dd9136"]')]
                          .map(x => +getComputedStyle(x).opacity); }''', t)
                a = stroke_opacities(.8)
                b = stroke_opacities(4.2)
                assert a[0] > .7 and a[1] < .1, (width, a)
                assert b[1] > .7 and b[0] < .1, (width, b)
                assert not page.evaluate('document.documentElement.scrollWidth > innerWidth + 1')
                page.close()
                page = browser.new_page(viewport={'width':width,'height':1000}, reduced_motion='reduce')
                page.set_content('<body style="margin:0"><div style="max-width:480px">'+still+'</div></body>')
                page.locator('svg').evaluate("svg => {svg.style.width='100%';svg.style.height='auto'}")
                assert not page.evaluate('document.documentElement.scrollWidth > innerWidth + 1')
                page.close()
        finally:
            browser.close()
    print('PASS ICM action aliasing: 4 widths, two action phases, static reduced-motion fallback')

if __name__ == '__main__':
    run()
