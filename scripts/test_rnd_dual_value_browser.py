#!/usr/bin/env python3
"""Check the illustrative RND dual-discount-value teaching motion in Chromium."""
from pathlib import Path
from xml.etree import ElementTree as ET
from playwright.sync_api import sync_playwright

BASE = Path(__file__).resolve().parents[1] / 'docs/assets/concept-animations'

def run():
    motion = (BASE / 'rnd-dual-value-motion.svg').read_text(encoding='utf-8')
    still = (BASE / 'rnd-dual-value-still.svg').read_text(encoding='utf-8')
    assert '10s' in motion and '<animate ' in motion and '<animate ' not in still
    for svg in (motion, still):
        assert ET.fromstring(svg).get('viewBox') == '0 0 520 470'
        assert 'href=' not in svg and '<script' not in svg
    assert abs(.9**3-.729) < 1e-12
    assert abs(1 + .6*.6 + .6**2*.3 - 1.468) < 1e-12
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True, executable_path=(
            '/usr/bin/chromium' if Path('/usr/bin/chromium').exists() else None), args=['--no-sandbox'])
        try:
            for width in (320, 360, 720, 1024):
                ctx = browser.new_context(viewport={'width':width,'height':1000})
                page = ctx.new_page()
                page.set_content('<body style="margin:0">'+motion+'</body>')
                for t,ext,intr in ((.5,0,0),(1.5,0,1),(3,0,1.36),(5,0,1.468),(7,.729,1.468)):
                    values = page.evaluate("""t => {
                        const svg=document.querySelector('svg'); svg.setCurrentTime(t); svg.pauseAnimations();
                        return [...svg.querySelectorAll('text.motion-only')]
                          .filter(n=>getComputedStyle(n).display!=='none' && +getComputedStyle(n).opacity>.5)
                          .map(n=>n.textContent.trim());
                    }""", t)
                    assert f'G = {ext:.3f}' in values and f'G = {intr:.3f}' in values, (width,t,values)
                    assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+1')
                ctx.close()
                ctx=browser.new_context(viewport={'width':width,'height':1000}, reduced_motion='reduce')
                page=ctx.new_page()
                page.set_content('<body style="margin:0">'+motion+'</body>')
                assert page.locator('rect.still-only:visible').count()==4
                assert page.locator('rect.motion-only:visible').count()==0
                ctx.close()
                ctx=browser.new_context(viewport={'width':width,'height':1000})
                page=ctx.new_page()
                page.set_content('<body style="margin:0">'+still+'</body>')
                assert 'G = 0.729' in still and 'G = 1.468' in still
                assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+1')
                ctx.close()
        finally:
            browser.close()
    print('PASS RND dual-value: five states, two discounts, four widths, reduced motion')

if __name__ == '__main__':
    run()
