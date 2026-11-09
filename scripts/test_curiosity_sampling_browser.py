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
RUNS_PREVIEW = ROOT / 'docs/assets/concept-animations/icm-independent-runs-still.svg'
MOTION_PREVIEW = ROOT / 'docs/assets/concept-animations/icm-sampling-frequency-motion.svg'
MOTION_STILL = ROOT / 'docs/assets/concept-animations/icm-sampling-frequency-still.svg'
OUT = ROOT / 'artifacts/rnd-icm-motion'
OUT.mkdir(parents=True, exist_ok=True)


def set_range(el, value):
    el.evaluate('(e,v)=>{e.value=String(v);e.dispatchEvent(new Event("input",{bubbles:true}));}', value)


def verify_frequency_motion(browser):
    """Validate synthetic 20-draw motion and its GitHub-safe no-script fallback."""
    svg_ns = '{http://www.w3.org/2000/svg}'
    root = ET.parse(MOTION_PREVIEW).getroot()
    still = ET.parse(MOTION_STILL).getroot()
    assert root.attrib['viewBox'] == still.attrib['viewBox'] == '0 0 420 438'
    assert 0 < MOTION_PREVIEW.stat().st_size < 50 * 1024
    assert 0 < MOTION_STILL.stat().st_size < 50 * 1024
    for diagram in (root, still):
        assert diagram.find(svg_ns + 'title') is not None
        assert diagram.find(svg_ns + 'desc') is not None
        assert not any(node.tag in {svg_ns+'script', svg_ns+'foreignObject', svg_ns+'image'} for node in diagram.iter())
    animations = list(root.iter(svg_ns + 'animate'))
    assert len(animations) > 40
    assert all(node.attrib.get('repeatCount') == 'indefinite' for node in animations)
    assert all(len(node.attrib['keyTimes'].split(';')) == len(node.attrib['values'].split(';')) for node in animations)
    assert not list(still.iter(svg_ns + 'animate'))
    # The analytic standard-error funnel is an exact geometry at every n,
    # independently of the path taken by this synthetic draw sequence.
    losses = [3.866, 1.936, 3.250]
    expected = sum(losses) / len(losses)
    sd = sqrt(sum((value - expected)**2 for value in losses) / len(losses))
    for svg, expected_count in ((root, 2), (still, 1)):
        bands = [element for element in svg.iter(svg_ns + 'polygon')
                 if 'data-analytic-se-band' in element.attrib]
        assert len(bands) == expected_count
        for band in bands:
            points = [tuple(map(float, xy.split(','))) for xy in band.attrib['points'].split()]
            assert len(points) == 40
            for n in range(1, 21):
                x = 62 + (n - 1) * 316 / 19
                upper = 381 - (expected + sd / sqrt(n) - 2) * 52
                lower = 381 - (expected - sd / sqrt(n) - 2) * 52
                assert abs(points[n-1][0] - x) < 0.02
                assert abs(points[n-1][1] - upper) < 0.02
                assert abs(points[40-n][0] - x) < 0.02
                assert abs(points[40-n][1] - lower) < 0.02
    assert any(el.attrib.get('id') == 'icm-se-reveal'
               for el in root.iter(svg_ns + 'clipPath'))
    assert len(list(still.iter(svg_ns + 'polyline'))) == 1
    assert len(list(root.iter(svg_ns + 'polyline'))) == 1
    source = MOTION_PREVIEW.read_text(encoding='utf-8')
    for width in (320, 360, 720, 1024):
        context = browser.new_context(
            viewport={'width': width, 'height': 850},
            reduced_motion='reduce' if width == 360 else 'no-preference',
        )
        page = context.new_page()
        page.set_content(
            '<html><head><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<style>body{margin:0}svg{display:block;max-width:420px;width:100%;height:auto}</style>'
            '</head><body>' + source + '</body></html>'
        )
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
        page.evaluate('(t)=>{const svg=document.querySelector("svg");svg.pauseAnimations();svg.setCurrentTime(t)}', 12.6)
        if width != 360:
            active = page.locator('g.motion rect[fill="#267f9f"]')
            assert active.count() == 1
            assert abs(active.evaluate('e=>e.getBBox().width') - 30) < 0.1  # 2/20
            assert abs(page.locator('g.motion rect[fill="#319d91"]').evaluate('e=>e.getBBox().width') - 120) < 0.1  # 8/20
            assert abs(page.locator('g.motion rect[fill="#8672b4"]').evaluate('e=>e.getBBox().width') - 150) < 0.1  # 10/20
            assert page.locator('g.motion').first.evaluate('e=>getComputedStyle(e).display') != 'none'
            # Browser must animate the clipped SE envelope with the draw
            # count, not display a completed funnel at time zero.
            for n in (0, 1, 5, 10, 20):
                timestamp = n * 13.2 / 21 + 0.04
                page.evaluate('(t)=>{const svg=document.querySelector("svg");'
                              'svg.pauseAnimations();svg.setCurrentTime(t)}', timestamp)
                actual = page.locator('#icm-se-reveal rect').evaluate(
                    'e=>e.width.animVal.value')
                expected_width = 0 if n == 0 else (n - 1) * 316 / 19 + 1
                assert abs(actual - expected_width) < 0.1
            page.evaluate('(t)=>{const svg=document.querySelector("svg");'
                          'svg.setCurrentTime(t)}', 12.6)
        else:
            assert page.locator('g.still').first.evaluate('e=>getComputedStyle(e).display') != 'none'
            assert page.locator('g.motion').first.evaluate('e=>getComputedStyle(e).display') == 'none'
            assert page.locator('g.still [data-analytic-se-band]').count() == 1
        assert page.locator('svg').get_attribute('aria-labelledby') == 'title desc'
        (OUT / f'icm_frequency_motion_{width}.png').write_bytes(page.locator('svg').screenshot())
        context.close()


def run():
    root = ET.parse(PREVIEW).getroot()
    assert root.tag == '{http://www.w3.org/2000/svg}svg'
    assert root.attrib['viewBox'] == '0 0 420 565'
    assert PREVIEW.stat().st_size < 50 * 1024
    assert not any(node.tag.rsplit('}', 1)[-1] in ('animate', 'script', 'foreignObject') for node in root.iter())
    independent_root = ET.parse(RUNS_PREVIEW).getroot()
    assert independent_root.attrib['viewBox'] == '0 0 420 294'
    assert RUNS_PREVIEW.stat().st_size < 50 * 1024
    assert not any(node.tag.rsplit('}', 1)[-1] in ('animate', 'script', 'foreignObject') for node in independent_root.iter())
    two_paths = [node.attrib['points'].split() for node in independent_root.iter()
                 if node.tag.rsplit('}', 1)[-1] == 'polyline']
    assert len(two_paths) == 2 and all(len(points) == 20 for points in two_paths)
    for points, mean in zip(two_paths, (2.786, 3.0016)):
        target_y = 210 - (mean - 1) * (210 - 88) / 4
        assert abs(float(points[-1].split(',')[1]) - target_y) < .02
    with sync_playwright() as p:
        browser = p.chromium.launch()
        verify_frequency_motion(browser)
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
                assert buttons.count() == 4
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
                frequency = page.locator('.curiosity-lab-frequency-row')
                assert frequency.count() == 3
                shares = [float(frequency.nth(i).locator('.curiosity-lab-frequency-fill').get_attribute('data-observed')) for i in range(3)]
                assert abs(sum(shares)-1.0) < 1e-12
                # The seeded 20-draw result after an initial independent draw:
                # the frequency bars must match all 21 draws, not the 12 chips.
                sample_counts = [round(21 * v) for v in shares]
                assert sum(sample_counts) == 21
                gap_rows = page.locator('[data-gap-outcome]')
                assert gap_rows.count() == 3
                contributions = [float(gap_rows.nth(i).get_attribute('data-gap-term')) for i in range(3)]
                toy_losses = [3.866, 1.936, 3.250]
                expected_loss = sum(toy_losses) / 3
                for i, contribution in enumerate(contributions):
                    frequency_gap = sample_counts[i] / 21 - 1 / 3
                    centered_loss = toy_losses[i] - expected_loss
                    expected_term = frequency_gap * centered_loss
                    assert abs(contribution - expected_term) < 1e-10
                    assert abs(float(gap_rows.nth(i).get_attribute('data-centered-loss')) - centered_loss) < 1e-10
                    assert gap_rows.nth(i).get_attribute('aria-label')
                    # Adding a constant baseline to every loss cannot change
                    # a centered outcome attribution, unlike raw-loss bars.
                    shifted_losses = [value + 7.5 for value in toy_losses]
                    shifted_center = sum(shifted_losses) / 3
                    assert abs(frequency_gap * (shifted_losses[i] - shifted_center) - contribution) < 1e-10
                gap_total = float(page.locator('[data-gap-total]').get_attribute('data-gap-total'))
                assert abs(sum(contributions) - gap_total) < 1e-10
                assert gap_rows.nth(0).locator('.curiosity-lab-gap-fill').count() == 1
                assert all(abs(float(frequency.nth(i).locator('.curiosity-lab-frequency-target').get_attribute('data-probability')) - 1/3) < 1e-10 for i in range(3))
                assert all(frequency.nth(i).get_attribute('aria-label') for i in range(3))
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
                # Two independent 20-draw replicates use different deterministic
                # streams under unchanged probabilities and analytic expectation.
                buttons.nth(3).focus()
                page.keyboard.press('Enter')
                independent = stats.text_content()
                assert ('Run: 2' in independent or '第幾輪: 2' in independent)
                assert ('Previous run (n=1): 3.250' in independent
                        or '上一輪 (n=1): 3.250' in independent)
                assert '3.017' in independent
                assert len(page.locator('[data-sample-means]').get_attribute('points').split()) == 20
                second_mean = float(independent.split(' · ')[1].split(': ')[1])
                assert abs(second_mean - first_mean) > 0.001
                (OUT / f'icm_independent_run_{locale}_{width}.png').write_bytes(panel.screenshot())
                # Reset preserves run-2's seed, so Draw 20 replays its path.
                buttons.nth(2).focus()
                page.keyboard.press('Enter')
                assert ('Run: 2' in stats.text_content() or '第幾輪: 2' in stats.text_content())
                assert 'Previous run' not in stats.text_content() and '上一輪' not in stats.text_content()
                buttons.nth(1).click()
                assert abs(float(stats.text_content().split(' · ')[1].split(': ')[1]) - second_mean) < .0001
                set_range(page.locator('input[data-skew]'), 60)
                assert ('Run: 1' in stats.text_content() or '第幾輪: 1' in stats.text_content())
                assert page.locator('.curiosity-lab-sample-chip').count() == 0
                assert '2.649' in stats.text_content()
                buttons.nth(1).click()
                assert '20' in stats.text_content()
                (OUT / f'icm_sampling_{locale}_{width}_skew.png').write_bytes(page.locator('.curiosity-lab').screenshot())
                set_range(page.locator('input[data-bias]'), 40)
                assert page.locator('.curiosity-lab-sample-observed').is_hidden()
                # Distribution changes reset counts and move all three targets.
                assert all(float(frequency.nth(i).locator('.curiosity-lab-frequency-fill').get_attribute('data-observed')) == 0 for i in range(3))
                assert abs(float(frequency.nth(0).locator('.curiosity-lab-frequency-target').get_attribute('data-probability')) - 160/300) < 1e-10
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
                assert abs(sum(float(frequency.nth(i).locator('.curiosity-lab-frequency-fill').get_attribute('data-observed')) for i in range(3))-1) < 1e-12
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
