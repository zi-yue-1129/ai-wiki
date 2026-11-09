#!/usr/bin/env python3
"""Render and check a schematic ICM inverse-dynamics feature-selection visual."""
from pathlib import Path
from xml.etree import ElementTree as ET
from playwright.sync_api import sync_playwright

BASE = Path(__file__).resolve().parents[1] / 'docs/assets/concept-animations'

def run():
    motion = (BASE / 'icm-inverse-feature-motion.svg').read_text(encoding='utf-8')
    still = (BASE / 'icm-inverse-feature-still.svg').read_text(encoding='utf-8')
    for xml in (motion, still):
        assert ET.fromstring(xml).get('viewBox') == '0 0 480 558'
        assert '<script' not in xml and 'href=' not in xml and 'onload=' not in xml
    assert motion.count('repeatCount="indefinite"') == 6
    assert '<animate ' not in still
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True, executable_path=(
            '/usr/bin/chromium' if Path('/usr/bin/chromium').exists() else None), args=['--no-sandbox'])
        try:
            for width in (320, 360, 720, 1024):
                context = browser.new_context(viewport={'width': width, 'height': 1000})
                page = context.new_page()
                page.set_content('<body style="margin:0"><div style="max-width:480px">' +
                                 motion + '</div></body>')
                page.locator('svg').evaluate("svg => svg.style.cssText='width:100%;height:auto'")
                for t,expected in ((0.1,(89,249,30)),(4.8,(203,105,89)),(7.4,(260,27,124))):
                    values = page.evaluate('''t => {
                        const svg=document.querySelector('svg');
                        svg.setCurrentTime(t);svg.pauseAnimations();
                        return ['motion-bar','noise-bar','inverse-bar'].map(
                          id => document.getElementById(id).getBBox().width);
                    }''', t)
                    assert all(abs(actual-want)<23 for actual,want in zip(values,expected)), (t,values)
                assert not page.evaluate('document.documentElement.scrollWidth > innerWidth + 1')
                context.close()
                context=browser.new_context(viewport={'width':width,'height':1000},reduced_motion='reduce')
                page=context.new_page()
                page.set_content('<body style="margin:0"><div style="max-width:480px">'+still+'</div></body>')
                assert page.locator('#motion-bar').get_attribute('width') == '260'
                assert page.locator('#noise-bar').get_attribute('width') == '27'
                assert not page.evaluate('document.documentElement.scrollWidth > innerWidth + 1')
                context.close()
        finally:
            browser.close()
    print('PASS ICM inverse-feature schematic: 4 widths, SMIL states, reduced-motion fallback')

if __name__ == '__main__':
    run()
