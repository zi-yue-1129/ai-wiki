"""RND return scaling and ICM auxiliary-gradient weighting browser regression."""
from pathlib import Path
from xml.etree import ElementTree as ET
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'docs/assets/concept-animations'
CASES = {
    'rnd-return-scale': ('rect[x="38"][y="339"][fill="#168a7d"]', 'width', [240, 120, 60]),
    'icm-loss-blend': ('line[stroke="#168a7d"][stroke-width="4.2"]', 'x2', [283, 205.5, 128]),
}

def check_xml():
    for topic in CASES:
        for kind in ('motion', 'still'):
            svg = ET.parse(ASSETS / f'{topic}-{kind}.svg').getroot()
            nodes = list(svg.iter())
            assert not any(n.tag.endswith(('script', 'foreignObject')) for n in nodes)
            if kind == 'still':
                assert not any(n.tag.endswith(('animate', 'animateMotion')) for n in nodes)
            else:
                animations = [n for n in nodes if n.tag.endswith('animate')]
                assert animations and all(n.get('repeatCount') == 'indefinite' for n in animations)
                for n in animations:
                    assert len(n.get('values').split(';')) == len(n.get('keyTimes').split(';'))
                    assert n.get('dur') == '9s'
            for n in nodes:
                assert not any(k.endswith('href') and (v.startswith('http:') or v.startswith('https:')) for k, v in n.attrib.items())


def check_browser():
    screenshots = ROOT / 'artifacts/rnd-icm-motion'
    screenshots.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        chrome = Path('/usr/bin/chromium')
        browser = pw.chromium.launch(headless=True, executable_path=str(chrome) if chrome.exists() else None, args=['--no-sandbox'])
        for topic, (selector, attr, expected) in CASES.items():
            for viewport in (320, 360, 720, 1024):
                for kind, moments in (('motion', [0.5, 3.7, 6.9]), ('still', [None])):
                    page = browser.new_page(viewport={'width': viewport, 'height': 900})
                    errors = []
                    page.on('pageerror', lambda err: errors.append(str(err)))
                    svg = (ASSETS / f'{topic}-{kind}.svg').read_text(encoding='utf-8')
                    page.set_content('<style>body{margin:0}svg{width:100%;height:auto;display:block}</style>' + svg)
                    for idx, moment in enumerate(moments):
                        if moment is not None:
                            page.evaluate('(time)=>{const svg=document.querySelector("svg");svg.pauseAnimations();svg.setCurrentTime(time)}', moment)
                            actual = page.eval_on_selector(selector, f'el=>el.{attr}.animVal.value')
                            assert abs(actual - expected[idx]) < 0.01, (topic, viewport, moment, actual, expected[idx])
                        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), (topic, viewport)
                        page.screenshot(path=str(screenshots / f'{topic}-{viewport}-{kind}-{idx}.png'))
                    assert not errors, errors
                    page.close()
        browser.close()

if __name__ == '__main__':
    check_xml()
    check_browser()
    print('RND/ICM balance animation regression passed')
