"""Chromium and numerical regression for epsilon-greedy Q-learning/SARSA target differences."""
from __future__ import annotations
import os
from pathlib import Path
from xml.etree import ElementTree as ET
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'docs/assets/concept-animations'
OUT = ROOT / 'artifacts/q-sarsa-epsilon'
SVG = '{http://www.w3.org/2000/svg}'


def run():
    motion = ASSETS / 'q-sarsa-epsilon-motion.svg'
    still = ASSETS / 'q-sarsa-epsilon-still.svg'
    for file in (motion, still):
        root = ET.parse(file).getroot()
        assert root.get('viewBox') == '0 0 440 630'
        for element in root.iter():
            assert element.tag.split('}')[-1] not in ('script', 'foreignObject', 'iframe', 'image')
            assert all(not k.split('}')[-1].startswith('on') for k in element.attrib)
            assert all(not str(v).startswith(('http:', 'https:', 'javascript:', 'data:')) for k, v in element.attrib.items() if k.split('}')[-1] in ('href', 'src'))
    assert len(ET.parse(motion).getroot().findall(f'.//{SVG}animate')) >= 6
    assert not ET.parse(still).getroot().findall(f'.//{SVG}animate')
    eps = .2
    prob_l, prob_r = 1 - eps + eps / 2, eps / 2
    assert abs(prob_l - .9) < 1e-10 and abs(prob_r - .1) < 1e-10
    assert abs((prob_l * (1 + .9 * 5) + prob_r * (1 + .9 * 2)) - 5.23) < 1e-10

    OUT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        launch = {'headless': True, 'args': ['--no-sandbox']}
        if os.environ.get('CHROMIUM_EXECUTABLE'):
            launch['executable_path'] = os.environ['CHROMIUM_EXECUTABLE']
        browser = p.chromium.launch(**launch)
        for width in (320, 360, 720, 1024):
            for variant, seconds in [('motion', .5), ('motion', 2.5), ('motion', 4.5), ('motion', 6.9), ('motion', 9.4), ('still', 0)]:
                page = browser.new_page(viewport={'width': width, 'height': max(750, width * 2)})
                file = motion if variant == 'motion' else still
                page.set_content('<style>html,body{margin:0}svg{display:block;width:100%;height:auto}</style>' + file.read_text())
                if variant == 'motion':
                    page.locator('svg').evaluate('(e,t) => {e.pauseAnimations();e.setCurrentTime(t)}', seconds)
                    target = ('#q-highlight rect' if seconds == 2.5 else '#l-highlight rect' if seconds == 4.5 else '#r-highlight rect' if seconds == 6.9 else '#expected-highlight rect' if seconds == 9.4 else None)
                    if target:
                        opacity = float(page.locator(target).evaluate('e => getComputedStyle(e).opacity'))
                        assert opacity > .8, (target, seconds, opacity)
                boxes = page.locator('svg text').evaluate_all('els => els.map(e => {let b=e.getBBox();return [b.x,b.y,b.width,b.height]})')
                assert all(x >= -0.5 and y >= -0.5 and x + w <= 440.5 and y + h <= 630.5 for x, y, w, h in boxes)
                assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
                page.locator('svg').screenshot(path=str(OUT / f'{variant}-{width}-{str(seconds).replace(".", "_")}.png'))
                page.close()
        js = ROOT / 'docs/javascripts/concept-motion.js'
        host = 'https://local.invalid/concept-animations/'
        for alt in ('Epsilon greedy backups', '探索策略的備份目標'):
            for preference in ('no-preference', 'reduce'):
                ctx = browser.new_context(reduced_motion=preference)
                page = ctx.new_page()
                page.route(host + '**', lambda route: route.fulfill(body=(motion if '-motion.svg' in route.request.url else still).read_text(), content_type='image/svg+xml'))
                page.set_content(f'<img src="{host}q-sarsa-epsilon-still.svg" data-motion-src="{host}q-sarsa-epsilon-motion.svg" data-still-src="{host}q-sarsa-epsilon-still.svg" alt="{alt}">')
                assert page.locator('img').get_attribute('src').endswith('-still.svg')
                page.add_script_tag(content=js.read_text())
                toggle = page.locator('.concept-motion-toggle')
                toggle.wait_for(state='visible')
                assert page.locator('img').get_attribute('src').endswith('-still.svg' if preference == 'reduce' else '-motion.svg')
                toggle.focus()
                page.keyboard.press('Enter')
                assert page.locator('img').get_attribute('src').endswith('-motion.svg' if preference == 'reduce' else '-still.svg')
                page.keyboard.press('Space')
                assert page.locator('img').get_attribute('src').endswith('-still.svg' if preference == 'reduce' else '-motion.svg')
                ctx.close()
        browser.close()
    print('PASS epsilon-greedy: 24 Chromium captures, SVG semantics, localized keyboard controls, reduced motion')

if __name__ == '__main__':
    run()
