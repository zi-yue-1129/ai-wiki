#!/usr/bin/env python3
"""Visual/semantic QA for hypothetical stochastic-observation RND limitation."""
from pathlib import Path
from xml.etree import ElementTree as ET
from playwright.sync_api import sync_playwright

BASE = Path(__file__).resolve().parents[1] / 'docs/assets/concept-animations'

def run():
    motion = (BASE / 'rnd-stochastic-distractor-motion.svg').read_text(encoding='utf-8')
    still = (BASE / 'rnd-stochastic-distractor-still.svg').read_text(encoding='utf-8')
    for source in (motion, still):
        assert ET.fromstring(source).get('viewBox') == '0 0 360 764'
        assert '<script' not in source and 'href=' not in source and 'onload=' not in source
    assert motion.count('repeatCount="indefinite"') == 6
    assert '<animate ' not in still
    assert 'Noisy · strong transfer' in still
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True, executable_path=(
            '/usr/bin/chromium' if Path('/usr/bin/chromium').exists() else None), args=['--no-sandbox'])
        try:
            for width in (320, 360, 720, 1024):
                context = browser.new_context(viewport={'width': width, 'height': 1100})
                page = context.new_page()
                page.set_content('<body style="margin:0"><div style="width:100%;max-width:460px">'
                                 + motion + '</div></body>')
                page.locator('svg').evaluate('(svg) => {svg.setAttribute("style", "width:100%;height:auto");}')
                for time_value, expected in ((0.2, 0), (1.5, 1), (3.0, 2), (4.3, 3), (5.8, 4), (7.5, 6)):
                    result = page.evaluate("""(timeValue) => {
                        const svg=document.querySelector('svg');
                        svg.setCurrentTime(timeValue); svg.pauseAnimations();
                        return [...svg.querySelectorAll('g.motion-only')]
                            .filter(g => +getComputedStyle(g).opacity > .5).length;
                    }""", time_value)
                    assert result == expected, (width, time_value, expected, result)
                assert not page.evaluate('document.documentElement.scrollWidth > innerWidth + 1')
                context.close()
                context = browser.new_context(viewport={'width': width, 'height': 1100}, reduced_motion='reduce')
                page = context.new_page()
                page.set_content('<body style="margin:0"><div style="width:100%;max-width:460px">'
                                 + motion + '</div></body>')
                assert page.locator('g.still-only').is_visible()
                assert not page.locator('g.motion-only').first.is_visible()
                context.close()
                context = browser.new_context(viewport={'width': width, 'height': 1100})
                page = context.new_page()
                page.set_content('<body style="margin:0"><div style="width:100%;max-width:460px">'
                                 + still + '</div></body>')
                assert page.locator('g[data-row="fixed"]').count() == 6
                assert page.locator('g[data-row="noise"]').count() == 6
                assert page.locator('g[data-row="transfer"]').count() == 6
                assert not page.evaluate('document.documentElement.scrollWidth > innerWidth + 1')
                context.close()
        finally:
            browser.close()
    print('PASS RND stochastic distractor: 6 reveal stages, 4 widths, reduced motion, still fallback')

if __name__ == '__main__':
    run()
