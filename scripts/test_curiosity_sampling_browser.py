#!/usr/bin/env python3
"""Chromium integration: seeded ICM samples versus analytic expectation."""
from pathlib import Path
from math import sqrt
import xml.etree.ElementTree as ET
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
JS = (ROOT / 'docs/javascripts/curiosity-labs.js').read_text()
CSS = (ROOT / 'docs/stylesheets/curiosity-labs.css').read_text()
PREVIEW = ROOT / 'docs/assets/concept-animations/icm-sample-mean-still.svg'
OUT = ROOT / 'artifacts/rnd-icm-motion'
OUT.mkdir(parents=True, exist_ok=True)


def set_range(el, value):
    el.evaluate('(e,v)=>{e.value=String(v);e.dispatchEvent(new Event("input",{bubbles:true}));}', value)


def run():
    root = ET.parse(PREVIEW).getroot()
    assert root.tag == '{http://www.w3.org/2000/svg}svg'
    assert root.attrib['viewBox'] == '0 0 420 565'
    assert PREVIEW.stat().st_size < 50 * 1024
    assert not any(node.tag.rsplit('}', 1)[-1] in ('animate', 'script', 'foreignObject') for node in root.iter())
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for width in (320, 360, 720, 1024):
            for locale in ('en', 'zh-TW'):
                context = browser.new_context(
                    viewport={'width': width, 'height': 1200},
                    reduced_motion='reduce' if locale == 'zh-TW' else 'no-preference',
                )
                page = context.new_page()
                errors = []
                page.on('pageerror', lambda exc: errors.append(str(exc)))
                page.set_content(
                    f'<html><head><meta name="viewport" content="width=device-width,initial-scale=1">'
                    f'<style>body{{margin:0;padding:8px;font-family:Arial,sans-serif}}{CSS}</style>'
                    f'</head><body><div data-curiosity-lab="icm" data-locale="{locale}"></div></body></html>'
                )
                page.add_script_tag(content=JS)
                panel = page.locator('.curiosity-lab-samples')
                assert panel.count() == 1 and not panel.is_visible()
                set_range(page.locator('input[data-timeline]'), 3)
                assert panel.is_visible()
                buttons = panel.get_by_role('button')
                assert buttons.count() == 3
                stats = page.locator('.curiosity-lab-sample-stats')
                assert page.locator('.curiosity-lab-sample-observed').is_hidden()
                assert page.locator('.curiosity-lab-sample-trajectory').is_hidden()
                buttons.nth(0).click()
                assert page.locator('.curiosity-lab-sample-chip').count() == 1
                assert len(page.locator('[data-sample-means]').get_attribute('points').split()) == 1
                first_mean = float(stats.text_content().split(' · ')[1].split(': ')[1])
                assert abs(first_mean - 3.250) < .001
                buttons.nth(1).click()
                assert '21' in stats.text_content()
                trace = page.locator('[data-sample-means]')
                assert len(trace.get_attribute('points').split()) == 21
                running = float(stats.text_content().split(' · ')[1].split(': ')[1])
                bounds = page.locator('.curiosity-lab-sample-trajectory')
                y_min = float(bounds.get_attribute('data-y-min'))
                y_max = float(bounds.get_attribute('data-y-max'))
                assert y_max > y_min
                # Exact loss variability, not the feature-space variance:
                # SD(loss) / sqrt(n) is the theoretical SE of the sample mean.
                outcomes = ((365, 101), (310, 174), (255, 115))
                losses = [((x-310)**2+(y-130)**2)/1000 for x,y in outcomes]
                analytic = sum(losses)/3
                sd = sqrt(sum((v-analytic)**2 for v in losses)/3)
                se = float(bounds.get_attribute('data-standard-error'))
                assert abs(se-sd/sqrt(21)) < 1e-9
                assert page.locator('[data-sample-se-band]').evaluate('(el)=>el.tagName') == 'polygon'
                envelope = [tuple(map(float, point.split(','))) for point in page.locator('[data-sample-se-band]').get_attribute('points').split()]
                assert len(envelope) == 42
                assert abs(envelope[20][1] - (122-(analytic+se-y_min)*90/(y_max-y_min))) < .02
                assert abs(envelope[21][1] - (122-(analytic-se-y_min)*90/(y_max-y_min))) < .02
                last_y = float(trace.get_attribute('points').split()[-1].split(',')[1])
                assert abs(last_y - (122 - (running - y_min) * 90 / (y_max - y_min))) < .02
                expected_y = float(page.locator('.curiosity-lab-sample-trajectory line[stroke="#775fb0"]').first.get_attribute('y1'))
                assert abs(expected_y - (122 - (3.017 - y_min) * 90 / (y_max - y_min))) < .02
                assert page.locator('.curiosity-lab-sample-chip').count() == 12
                assert page.locator('.curiosity-lab-sample-observed').is_visible()
                assert '3.017' in stats.text_content()
                (OUT / f'icm_sampling_{locale}_{width}_21.png').write_bytes(panel.screenshot())
                buttons.nth(2).click()
                assert page.locator('.curiosity-lab-sample-chip').count() == 0
                assert page.locator('.curiosity-lab-sample-trajectory').is_hidden()
                assert page.locator('.curiosity-lab-sample-observed').is_hidden()
                buttons.nth(0).click()
                assert abs(float(stats.text_content().split(' · ')[1].split(': ')[1]) - first_mean) < .001
                set_range(page.locator('input[data-skew]'), 60)
                assert page.locator('.curiosity-lab-sample-chip').count() == 0
                assert '2.649' in stats.text_content()
                buttons.nth(1).click()
                assert '20' in stats.text_content()
                (OUT / f'icm_sampling_{locale}_{width}_skew.png').write_bytes(page.locator('.curiosity-lab').screenshot())
                set_range(page.locator('input[data-bias]'), 40)
                assert page.locator('.curiosity-lab-sample-observed').is_hidden()
                assert '4.249' in stats.text_content()
                buttons.nth(1).click()
                assert page.locator('.curiosity-lab-sample-chip').count() == 12
                assert page.locator('.curiosity-lab-plot svg').count() == 1
                assert page.locator('.curiosity-lab-sample-trajectory svg').count() == 1
                for _ in range(7):
                    buttons.nth(1).click()
                trace = page.locator('[data-sample-means]')
                assert len(trace.get_attribute('points').split()) == 120
                assert len(page.locator('[data-sample-se-band]').get_attribute('points').split()) == 240
                assert float(page.locator('.curiosity-lab-sample-trajectory').get_attribute('data-standard-error')) > 0
                assert int(page.locator('.curiosity-lab-sample-trajectory').get_attribute('data-window-start')) > 1
                assert int(page.locator('.curiosity-lab-sample-trajectory').get_attribute('data-total-draws')) == 160
                assert page.locator('.curiosity-lab-sample-trajectory svg').get_attribute('aria-label')
                (OUT / f'icm_sampling_{locale}_{width}_bias.png').write_bytes(panel.screenshot())
                assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), (width, locale)
                assert page.locator('.curiosity-lab-sample-track').get_attribute('aria-label')
                assert not errors, errors
                context.close()
        browser.close()
    print('PASS: 4 widths, both languages, seeded draw/reset, probability weights, prediction bias, reduced motion')


if __name__ == '__main__':
    run()
