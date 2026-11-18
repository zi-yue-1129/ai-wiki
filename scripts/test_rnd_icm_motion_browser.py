#!/usr/bin/env python3
"""Browser QA for the paired RND/ICM instructional SVGs and shared player.

Render actual intermediate states at mobile/desktop widths, assert error reduction,
verify reduced-motion screenshots remain pixel-stable, and exercise both button
and keyboard controls on the MkDocs enhancement (when JS is present).
"""
from __future__ import annotations

import hashlib
import os
from pathlib import Path
import tempfile
import xml.etree.ElementTree as ET
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
ASSETS = Path(os.environ.get('RND_ICM_ASSETS', ROOT / 'docs/assets/concept-animations'))
PLAYER = ROOT / 'docs/javascripts/concept-motion.js'
STEMS = ('rnd-prediction-error', 'icm-forward-inverse')
REVIEW = ROOT / 'artifacts/rnd-icm-motion'


def frame(page, time: float) -> bytes:
    page.evaluate('(t) => document.querySelector("svg").setCurrentTime(t)', time)
    page.wait_for_timeout(30)
    return page.locator('svg').screenshot(animations='allow')







def check_rnd_desktop_squared_bonus(browser) -> None:
    """Desktop novelty bar tracks feature squared distance and input arrival."""
    source = (ASSETS / 'rnd-state-novelty-motion.svg').read_text(encoding='utf-8')
    initial_sq = (589 - 470) ** 2 + (145 - 235) ** 2
    ctx = browser.new_context(viewport={'width': 1050, 'height': 700})
    try:
        page = ctx.new_page()
        page.set_content(source)
        readings = {}
        for t in (0.0, 1.6, 3.6, 6.4, 6.9, 7.11, 7.15, 8.2, 9.6, 9.995):
            metrics = page.evaluate("""(time) => {
                const svg = document.querySelector('svg');
                svg.setCurrentTime(time);
                svg.pauseAnimations();
                const target = svg.querySelector('circle[cx="589"][cy="145"]');
                const pred = svg.querySelector('circle[cx="470"][cy="235"]');
                const bar = svg.querySelector('rect.animated[x="180"]');
                return {
                    tx: target.cx.animVal.value, ty: target.cy.animVal.value,
                    px: pred.cx.animVal.value, py: pred.cy.animVal.value,
                    bonus: bar.width.animVal.value,
                    a: Number(getComputedStyle(svg.querySelector('text[fill="#376aa9"]')).opacity),
                    b: Number(getComputedStyle(svg.querySelector('text[fill="#c67b36"]')).opacity)
                };
            }""", t)
            squared = (metrics['tx'] - metrics['px']) ** 2 + (
                metrics['ty'] - metrics['py']) ** 2
            normalized = 390 * squared / initial_sq
            assert abs(metrics['bonus'] - normalized) < 2.5, (t, metrics, normalized)
            if t <= 7.11:
                assert metrics['a'] > .99 and metrics['b'] < .01, (t, metrics)
            else:
                assert metrics['b'] > .99 and metrics['a'] < .01, (t, metrics)
            readings[t] = metrics
        assert readings[6.9]['tx'] == readings[7.11]['tx'] == 589
        assert readings[7.15]['tx'] == 550
        assert readings[9.995]['tx'] == 550, 'loop end interpolates to an imaginary observation'
        assert readings[7.15]['bonus'] > readings[6.4]['bonus'] * 10
        assert readings[9.6]['bonus'] < readings[7.15]['bonus'] * .12
    finally:
        ctx.close()
    print('PASS desktop RND: input timing, squared-distance bonus and loop reset')

def check_rnd_mobile_novelty(browser) -> None:
    """Responsive RND keeps causality and scales its schematic bonus to squared error."""
    stem = 'rnd-state-novelty-mobile'
    motion = ASSETS / f'{stem}-motion.svg'
    still = ASSETS / f'{stem}-still.svg'
    source = motion.read_text(encoding='utf-8')
    fallback = still.read_text(encoding='utf-8')
    assert ET.fromstring(source).get('viewBox') == '0 0 380 660'
    assert ET.fromstring(fallback).get('viewBox') == '0 0 380 660'
    initial_squared = (291 - 72) ** 2 + (379 - 496) ** 2
    for width in (320, 360, 480, 640):
        context = browser.new_context(viewport={'width': width + 16, 'height': 1000})
        page = context.new_page()
        page.set_content(f'<style>body{{margin:0}}svg{{width:{width}px;height:auto}}</style>' + source)
        states = []
        for label, t in (('a_early', 0), ('a_learning', 3.5), ('a_fitted', 6.5),
                         ('b_input', 6.99), ('b_new', 7.2), ('b_learning', 8.9),
                         ('b_fitted', 9.6)):
            data = page.evaluate("""(t) => {
                const s = document.querySelector('svg');
                s.setCurrentTime(t);
                const gs = s.querySelectorAll('g.animated[aria-hidden="true"]');
                const targets = gs[1].querySelectorAll('circle');
                const target = targets[0], prediction = targets[1];
                const bonus = s.querySelector('#mobile-rnd-bonus');
                return [target.cx.animVal.value, target.cy.animVal.value,
                        prediction.cx.animVal.value, prediction.cy.animVal.value,
                        bonus.width.animVal.value];
            }""", t)
            tx, ty, px, py, displayed = data
            squared = (tx - px) ** 2 + (ty - py) ** 2
            expected = 240 * squared / initial_squared
            assert abs(displayed - expected) < 1.5, (width, t, displayed, expected)
            states.append(data)
            (REVIEW / f'{stem}_{width}_{label}.png').write_bytes(
                page.locator('svg').screenshot(animations='allow'))
        assert tuple(states[2][:2]) == tuple(states[3][:2]) == (291, 379)
        assert tuple(states[4][:2]) == tuple(states[6][:2]) == (230, 467)
        assert states[2][4] < states[0][4] * .03
        assert states[4][4] > states[3][4] * 8
        assert states[6][4] < states[4][4] * .03
        page.set_content(f'<style>svg{{width:{width}px;height:auto}}</style>' + fallback)
        (REVIEW / f'{stem}_{width}_still.png').write_bytes(page.locator('svg').screenshot())
        context.close()
        context = browser.new_context(viewport={'width': width + 16, 'height': 1000},
                                      reduced_motion='reduce')
        page = context.new_page()
        page.set_content(source)
        checksums = [hashlib.sha256(frame(page, t)).hexdigest() for t in (0, 3, 7, 9)]
        assert len(set(checksums)) == 1, 'mobile RND ignores reduced motion'
        context.close()

    if PLAYER.is_file():
        uri = 'http://127.0.0.1:9/docs/assets/concept-animations/rnd-state-novelty-motion.svg'
        ctx = browser.new_context(viewport={'width': 390, 'height': 900})
        page = ctx.new_page()
        page.set_content(f'<img alt="RND novelty" src="{uri}">')
        page.add_script_tag(content=PLAYER.read_text())
        img = page.locator('img')
        assert img.get_attribute('src').endswith('-mobile-motion.svg')
        page.get_by_role('button', name='Pause concept animation').click()
        assert img.get_attribute('src').endswith('-mobile-still.svg')
        page.set_viewport_size({'width': 1024, 'height': 900})
        page.wait_for_function(
            '() => document.querySelector("img").getAttribute("src").endsWith("-still.svg")'
            ' && !document.querySelector("img").getAttribute("src").endsWith("-mobile-still.svg")')
        page.get_by_role('button', name='Play concept animation').focus()
        page.keyboard.press('Enter')
        assert img.get_attribute('src').endswith('-motion.svg')
        page.set_viewport_size({'width': 390, 'height': 900})
        page.wait_for_function(
            '() => document.querySelector("img").getAttribute("src").endsWith("-mobile-motion.svg")')
        ctx.close()
    print('PASS RND mobile: squared-error geometry, responsive player, reduced motion')

def check_icm_mobile_stacked(browser) -> None:
    """Render mobile stacked ICM panels and exercise responsive player state."""
    stem = "icm-predictable-stochastic-mobile"
    motion = ASSETS / f"{stem}-motion.svg"
    still = ASSETS / f"{stem}-still.svg"
    animated, fallback = motion.read_text(), still.read_text()
    svg = ET.fromstring(animated)
    assert svg.attrib["viewBox"] == "0 0 380 770"
    assert ET.fromstring(fallback).attrib["viewBox"] == "0 0 380 770"
    assert "<animate " in animated and "<animate " not in fallback
    # All outcomes have equal illustrative weight; their centroid equals the
    # fixed forward prediction. Sampled bars and violet expectation share a
    # single squared-distance scale, rather than being arbitrary decorations.
    outcomes = [(294, 544), (213, 610), (132, 553)]
    mean = (213, 569)
    assert tuple(sum(x[i] for x in outcomes) / 3 for i in (0, 1)) == mean
    errors = [(x - mean[0]) ** 2 + (y - mean[1]) ** 2 for x, y in outcomes]
    scale = 177 / max(errors)
    expected_tick = 153 + sum(errors) / 3 * scale
    for width in (320, 360, 480, 640):
        context = browser.new_context(viewport={"width": width + 25, "height": 1000})
        page = context.new_page()
        page.set_content(
            '<html><body style="margin:0"><style>svg{display:block;width:'
            + str(width) + 'px;height:auto}</style>' + animated + '</body></html>'
        )
        observed = []
        for label, t in (("initial", 0.0), ("learning", 2.0),
                         ("second", 3.0), ("third", 5.3), ("fitted", 7.2)):
            data = page.evaluate("""(t) => {
                const svg = document.querySelector('svg');
                svg.setCurrentTime(t);
                const panels = svg.querySelectorAll('g.animated');
                const upper = panels[0], lower = panels[1];
                return {
                    x: upper.querySelector('circle').cx.animVal.value,
                    learned: upper.querySelector('rect').width.animVal.value,
                    sampledX: lower.querySelector('circle').cx.animVal.value,
                    sampled: lower.querySelector('rect').width.animVal.value,
                    tick: Number(svg.getElementById('mobile-expected-error').getAttribute('x1'))
                };
            }""", t)
            observed.append(data)
            assert abs(data["tick"] - expected_tick) < .001, data
            assert data["sampledX"] in (294, 213, 132), data
            assert abs(data["sampled"] - errors[(294, 213, 132).index(data["sampledX"])] * scale) < .01, data
            (REVIEW / f"{stem}_{width}_{label}.png").write_bytes(
                page.locator('svg').screenshot(animations='allow')
            )
        assert observed[0]["learned"] > 170
        assert observed[-1]["learned"] < 2
        assert [a["sampledX"] for a in observed] == [294, 294, 213, 132, 132]
        page.set_content(fallback)
        (REVIEW / f"{stem}_{width}_still.png").write_bytes(page.locator('svg').screenshot())
        context.close()
        context = browser.new_context(
            viewport={"width": width + 25, "height": 1000},
            reduced_motion="reduce"
        )
        page = context.new_page()
        page.set_content(animated)
        signatures = []
        for t in (0.0, 2.0, 4.0, 6.0):
            signatures.append(hashlib.sha256(frame(page, t)).hexdigest())
        assert len(set(signatures)) == 1, f"{stem}: reduced motion moved at {width}"
        context.close()

    # Real shared site JavaScript, not a mock player: viewport switches must
    # preserve Play/Pause selection, including keyboard toggling and reduced
    # motion. Image URLs are inspected without requiring an external server.
    if PLAYER.is_file():
        src = "http://127.0.0.1:9/docs/assets/concept-animations/icm-predictable-stochastic-motion.svg"
        context = browser.new_context(viewport={"width": 390, "height": 850})
        page = context.new_page()
        page.set_content(f'<img alt="ICM diagram" src="{src}">')
        page.add_script_tag(content=PLAYER.read_text())
        img = page.locator("img")
        assert img.get_attribute("src").endswith("-mobile-motion.svg")
        page.get_by_role("button", name="Pause concept animation").click()
        assert img.get_attribute("src").endswith("-mobile-still.svg")
        page.set_viewport_size({"width": 1024, "height": 850})
        page.wait_for_function(
            '() => document.querySelector("img").getAttribute("src").endsWith("-still.svg")'
            ' && !document.querySelector("img").getAttribute("src").endsWith("-mobile-still.svg")'
        )
        page.get_by_role("button", name="Play concept animation").focus()
        page.keyboard.press("Enter")
        assert img.get_attribute("src").endswith("-motion.svg")
        assert not img.get_attribute("src").endswith("-mobile-motion.svg")
        page.set_viewport_size({"width": 390, "height": 850})
        page.wait_for_function(
            '() => document.querySelector("img").getAttribute("src").endsWith("-mobile-motion.svg")'
        )
        context.close()
        context = browser.new_context(
            viewport={"width": 390, "height": 850}, reduced_motion="reduce"
        )
        page = context.new_page()
        page.set_content(f'<img alt="ICM diagram" src="{src}">')
        page.add_script_tag(content=PLAYER.read_text())
        assert page.locator("img").get_attribute("src").endswith("-mobile-still.svg")
        assert page.get_by_role("button", name="Play concept animation").count() == 1
        context.close()

def check_icm_stochastic_comparison(browser) -> None:
    """Check actual animation geometry, static preview and reduced-motion fallback.

    Identical encoded state-action input may have multiple stochastic outcomes.
    The comparison must not depict irreversible predictor regression at loop end.
    """
    stem = 'icm-predictable-stochastic'
    motion = ASSETS / f'{stem}-motion.svg'
    still = ASSETS / f'{stem}-still.svg'
    assert motion.is_file() and still.is_file()
    source = motion.read_text(encoding='utf-8')
    fallback = still.read_text(encoding='utf-8')
    ET.fromstring(source)
    ET.fromstring(fallback)
    assert 'repeatCount="indefinite"' in source
    assert '<animate ' in source and '<animate ' not in fallback
    for width in (360, 720, 1024):
        html = ('<html><head><meta charset="utf-8"><style>'
                f'body{{margin:0;padding:14px}}svg{{width:{width}px;height:auto;display:block}}'
                '</style></head><body>' + source + '</body></html>')
        context = browser.new_context(viewport={'width': width + 32, 'height': 750})
        page = context.new_page()
        page.set_content(html)
        signatures = []
        for label, t in (('initial', 0.0), ('learning', 2.0), ('outcome2', 3.0),
                         ('outcome3', 5.4), ('fitted', 7.2)):
            png = frame(page, t)
            signatures.append(hashlib.sha256(png).hexdigest())
            (REVIEW / f'{stem}_{width}_{label}.png').write_bytes(png)
        assert len(set(signatures)) >= 4, 'missing informative ICM variance frames'
        moving = page.locator('g.animated circle')
        assert moving.count() == 2, 'expected prediction and next-feature signals'
        def snapshot(t):
            page.evaluate('(t) => document.querySelector("svg").setCurrentTime(t)', t)
            return (
                moving.nth(0).evaluate('(n) => n.cx.animVal.value'),
                moving.nth(1).evaluate('(n) => n.cx.animVal.value'),
                [round(v) for v in page.locator('g.animated rect').evaluate_all(
                    '(nodes) => nodes.map(n => n.width.animVal.value)')]
            )
        initial, second, third, fitted = map(snapshot, (0, 3.0, 5.4, 7.2))
        assert initial[0] == 136 and fitted[0] == 264, (initial, fitted)
        assert initial[2][0] == 216 and fitted[2][0] == 1, (initial, fitted)
        # The predictable panel's bar must track squared feature error,
        # rather than a visually plausible but incorrect distance proxy.
        for t in (0.0, .96, 1.35, 2.0, 2.8, 3.2, 4.1, 5.4, 6.7, 7.6):
            # Sample all three animated values atomically at exactly t.
            # Separate browser round-trips allow the SMIL clock to advance
            # between the point and bar readings near a keyframe boundary.
            px, py, bar_width = page.evaluate("""(t) => {
                const svg = document.querySelector('svg');
                svg.setCurrentTime(t);
                const dot = svg.querySelector('g.animated circle');
                const strip = svg.querySelector('g.animated rect');
                return [dot.cx.animVal.value, dot.cy.animVal.value,
                        strip.width.animVal.value];
            }""", t)
            expected = 216 * ((px - 275)**2 + (py - 202)**2) / 21170
            assert abs(bar_width - expected) < 1.2, (
                'predictable error bar diverges from squared feature distance',
                t, bar_width, expected
            )
        fallback_rect = ET.fromstring(fallback).find(
            ".//{http://www.w3.org/2000/svg}g[@class='resting']/"
            "{http://www.w3.org/2000/svg}rect[@x='93']"
        )
        assert fallback_rect is not None
        assert abs(float(fallback_rect.attrib['width']) - 216 * 130 / 21170) < .01
        assert initial[1] == 636 and second[1] == 566 and third[1] == 487
        assert initial[2][1] == 212 and second[2][1] == 16 and third[2][1] == 211
        # Three equally weighted, schematic stochastic outcomes have the
        # fixed orange prediction as their exact conditional mean.
        outcomes = []
        for t in (0.0, 3.0, 5.4):
            page.evaluate('(t) => document.querySelector("svg").setCurrentTime(t)', t)
            outcomes.append(moving.nth(1).evaluate(
                '(n) => [n.cx.animVal.value, n.cy.animVal.value]'
            ))
        assert outcomes == [[636, 210], [566, 253], [487, 233]], outcomes
        prediction = [563, 232]
        assert [sum(p[i] for p in outcomes) / len(outcomes)
                for i in range(2)] == prediction, 'prediction not at conditional mean'
        squared_distances = [
            sum((p[i] - prediction[i]) ** 2 for i in range(2))
            for p in outcomes
        ]
        # The violet guide is an EXPECTATION across all possible outcomes,
        # not the squared error of whichever successor was sampled.
        expected_mean_bar = 462 + 212 * (sum(squared_distances) / 3) / squared_distances[0]
        for document in (source, fallback):
            root = ET.fromstring(document)
            guide = root.find(
                ".//{http://www.w3.org/2000/svg}line[@id='expected-error-tick']"
            )
            assert guide is not None, 'expected-error reference missing'
            assert abs(float(guide.get('x1')) - expected_mean_bar) < .01, (
                'expected-error tick does not reflect equally weighted variance',
                guide.get('x1'), expected_mean_bar
            )
        guide = page.locator('#expected-error-tick')
        assert guide.count() == 1
        assert abs(float(guide.get_attribute('x1')) - expected_mean_bar) < .01
        observed_bars = [initial[2][1], second[2][1], third[2][1]]
        expected_bars = [
            212 * value / squared_distances[0] for value in squared_distances
        ]
        assert all(abs(shown - expected) <= 2
                   for shown, expected in zip(observed_bars, expected_bars)), (
            'stochastic error bars inconsistent with squared distances',
            observed_bars, expected_bars
        )
        # A stochastic outcome is a sampled event, not a continuous
        # trajectory through features never returned by the environment.
        # The bar must switch atomically with the sampled target.
        for t, actual_x, squared_error_bar in (
            (2.42, 636, 212), (2.55, 566, 16),
            (4.80, 566, 16), (4.92, 487, 211)
        ):
            state = snapshot(t)
            assert state[1] == actual_x and state[2][1] == squared_error_bar, (
                'outcome interpolation or delayed error bar',
                t, state
            )
        # The *same* encoded input travels to Forward before each
        # additional outcome is sampled.
        input_pulse = page.locator('circle.animated[aria-hidden="true"]')
        assert input_pulse.count() == 1, 'missing repeated input pulse'
        for before, after in ((2.32, 2.43), (4.72, 4.83)):
            page.evaluate('(t) => document.querySelector("svg").setCurrentTime(t)', before)
            first_x = input_pulse.evaluate('(n) => n.cx.animVal.value')
            page.evaluate('(t) => document.querySelector("svg").setCurrentTime(t)', after)
            second_x = input_pulse.evaluate('(n) => n.cx.animVal.value')
            assert second_x - first_x > 10, (
                'input cue does not precede the next discrete outcome',
                first_x, second_x
            )
        assert fitted[0] == snapshot(7.8)[0], 'predictor must not visibly unlearn before replay'
        assert page.locator('svg').bounding_box()['width'] <= width + 1
        page.set_content(html.replace(source, fallback))
        (REVIEW / f'{stem}_{width}_fallback.png').write_bytes(
            page.locator('svg').screenshot())
        assert page.locator('svg').bounding_box()['width'] <= width + 1
        context.close()
        context = browser.new_context(
            viewport={'width': width + 32, 'height': 750}, reduced_motion='reduce')
        page = context.new_page()
        page.set_content(html)
        pixel_hashes = [hashlib.sha256(frame(page, t)).hexdigest()
                        for t in (0, 3.0, 5.4, 7.2)]
        assert len(set(pixel_hashes)) == 1, 'reduced-motion display varies over time'
        context.close()
    print('PASS ICM predictable/stochastic: outcome variation, persistent error, three widths, fallback')


def check_rnd_transfer_motion(browser) -> None:
    """Counterfactual B transfer: spatial interpolation and *squared* bonus agree."""
    motion = ASSETS / 'rnd-b-transfer-motion.svg'
    still = ASSETS / 'rnd-b-transfer-still.svg'
    source = motion.read_text(encoding='utf-8')
    assert ET.fromstring(source).attrib['viewBox'] == '0 0 380 500'
    assert ET.fromstring(still.read_text(encoding='utf-8')).attrib['viewBox']
    assert '<animate ' in source and '<animate ' not in still.read_text(encoding='utf-8')
    for width in (320, 380, 640):
        context = browser.new_context(viewport={'width': width + 20, 'height': 1000})
        try:
            page = context.new_page()
            page.set_content(f'<style>body{{margin:0}}svg{{width:{width}px;height:auto}}</style>' + source)
            for t in (0.0, 1.6, 2.25, 3.2, 4.45, 5.5, 6.6, 7.7):
                metrics = page.evaluate("""(time) => {
                    const s = document.querySelector('svg');
                    s.pauseAnimations();
                    s.setCurrentTime(time);
                    const line = s.querySelector('line');
                    const predictor = s.querySelector('circle[cx="105"]');
                    const bars = [...s.querySelectorAll('rect[x="134"]')];
                    return {
                        px: predictor.cx.animVal.value,
                        py: predictor.cy.animVal.value,
                        lx: line.x2.animVal.value, ly: line.y2.animVal.value,
                        transfer: bars[1].width.animVal.value,
                        gap: bars[3].width.animVal.value
                    };
                }""", t)
                g = (metrics['px'] - 105) / 126
                assert -.01 <= g <= 1.01, (width, t, metrics)
                assert abs(metrics['py'] - (255 - 108 * g)) < .16, (width, t, metrics)
                assert abs(metrics['lx'] - metrics['px']) < .1
                assert abs(metrics['ly'] - metrics['py']) < .1
                assert abs(metrics['transfer'] - 220 * g) < .25
                assert abs(metrics['gap'] - 220 * (1-g)**2) < .35, (
                    'Squared bonus mismatches feature distance', width, t, metrics)
                (REVIEW / f'rnd-transfer_{width}_{t:.2f}.png').write_bytes(
                    page.locator('svg').screenshot(animations='allow'))
            assert page.locator('svg').bounding_box()['width'] <= width + 1
        finally:
            context.close()

    # Normal MkDocs image enhancement pairs this motion with a static still.
    if PLAYER.is_file():
        for reduced in (False, True):
            context = browser.new_context(reduced_motion='reduce' if reduced else 'no-preference')
            try:
                page = context.new_page()
                page.set_content('<img alt="RND unseen B transfer" src="/docs/assets/concept-animations/rnd-b-transfer-motion.svg">')
                page.add_script_tag(content=PLAYER.read_text(encoding='utf-8'))
                button = page.get_by_role('button', name='Play concept animation' if reduced else 'Pause concept animation')
                assert button.count() == 1
                if not reduced:
                    button.focus()
                    page.keyboard.press('Enter')
                assert page.locator('img').get_attribute('src').endswith(
                    '-still.svg'), 'Pause or reduced-motion must show static transfer cases'
            finally:
                context.close()
    print('PASS RND transfer: mobile/desktop animation, quadratic bonus, player fallback')


def check_primary_squared_bonus_geometry(browser) -> None:
    """Compare real Chromium SVG geometry with the squared error at intermediate times."""
    cases = (
        ('rnd-prediction-error', (581, 138), 406, 19429),
        ('icm-forward-inverse', (604, 143), 132, 10312),
    )
    for stem, target, full_width, initial_sq in cases:
        source = (ASSETS / f'{stem}-motion.svg').read_text(encoding='utf-8')
        ET.fromstring(source)
        for width in (360, 720, 1024):
            ctx = browser.new_context(viewport={'width': width + 32, 'height': 620})
            try:
                page = ctx.new_page()
                page.set_content(
                    '<style>body{margin:0}svg{display:block;width:'
                    + str(width) + 'px;height:auto}</style>' + source)
                for t in (0, 0.91, 1.44, 2.33, 3.35, 4.21, 5.39, 6.37, 7.13, 7.97):
                    px, py, shown = page.evaluate("""(time) => {
                        const svg = document.querySelector('svg');
                        svg.pauseAnimations();
                        svg.setCurrentTime(time);
                        const point = svg.querySelector('g.animated circle');
                        const bar = svg.querySelector('rect.animated');
                        return [point.cx.animVal.value, point.cy.animVal.value,
                                bar.width.animVal.value];
                    }""", t)
                    true_sq = (px - target[0])**2 + (py - target[1])**2
                    expected = full_width * true_sq / initial_sq
                    assert abs(shown - expected) < 0.65, (
                        stem, width, t, shown, expected)
                    if t == 7.97:
                        assert shown < .011 * full_width, (
                            stem, 'end of replay wrongly reverses predictor learning')
                    if t in (0, 2.33, 4.21, 6.37, 7.97):
                        (REVIEW / f'{stem}_{width}_squared_{t:.2f}.png').write_bytes(
                            page.locator('svg').screenshot(animations='allow'))
                assert page.locator('svg').bounding_box()['width'] <= width + 1
            finally:
                ctx.close()
    print('PASS original RND/ICM: squared error geometry and nonreversing replay')

def run() -> None:
    REVIEW.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as runtime:
        browser = runtime.chromium.launch(headless=True, executable_path=("/usr/bin/chromium" if Path("/usr/bin/chromium").exists() else None), args=["--no-sandbox"])
        try:
            for stem in STEMS:
                motion = ASSETS / f'{stem}-motion.svg'
                still = ASSETS / f'{stem}-still.svg'
                assert motion.is_file() and still.is_file(), f'missing SVG pair: {stem}'
                source = motion.read_text(encoding='utf-8')
                assert '<animate ' in source and '<animate ' not in still.read_text(), stem

                for width in (360, 720, 1024):
                    html = ('<html><head><meta charset="utf-8"><style>'
                            f'body{{margin:0;padding:14px}}svg{{width:{width}px;height:auto;display:block}}'
                            '</style></head><body>' + source + '</body></html>')
                    ctx = browser.new_context(viewport={'width': width + 32, 'height': 640})
                    page = ctx.new_page()
                    page.set_content(html)
                    x0 = page.evaluate('document.querySelector(".animated circle").cx.animVal.value')
                    first = frame(page, 0.0)
                    middle = frame(page, 3.5)
                    end = frame(page, 6.0)
                    # Capture real Chromium frames for manual mobile/desktop visual QA.
                    for label, timestamp in (('initial', 0.0), ('input', 0.7),
                                             ('transfer', 1.6), ('learning', 3.5),
                                             ('output', 5.6), ('settled', 7.1)):
                        (REVIEW / f'{stem}_{width}_{label}.png').write_bytes(frame(page, timestamp))
                    x1 = page.evaluate('document.querySelector(".animated circle").cx.animVal.value')
                    assert x1 > x0 + 15, f'{stem} at {width}: predictor did not approach target'
                    assert len({hashlib.sha256(b).hexdigest() for b in (first, middle, end)}) == 3, (
                        f'{stem} at {width}: intermediate motion missing'
                    )
                    # The predictor channels are part of the actual RND teaching motion,
                    # not static decoration alongside an independently moving dot.
                    if stem == 'rnd-prediction-error':
                        channels = 'g.animated[fill="#d27b3f"] rect'
                        page.evaluate('(t) => document.querySelector("svg").setCurrentTime(t)', 0)
                        initial_bars = page.locator(channels).evaluate_all(
                            '(nodes) => nodes.map(node => node.height.animVal.value)'
                        )
                        page.evaluate('(t) => document.querySelector("svg").setCurrentTime(t)', 7.0)
                        fitted_bars = page.locator(channels).evaluate_all(
                            '(nodes) => nodes.map(node => node.height.animVal.value)'
                        )
                        assert initial_bars == [6, 25, 5, 30], initial_bars
                        assert fitted_bars == [13, 17, 10, 22], fitted_bars
                        # GitHub static preview must faithfully show the same
                        # first-frame feature vector as the animated SVG.
                        root = ET.fromstring(still.read_text(encoding='utf-8'))
                        group = root.find(".//{http://www.w3.org/2000/svg}g[@fill='#d27b3f']")
                        assert group is not None
                        still_heights = [int(rect.attrib['height']) for rect in group]
                        assert still_heights == initial_bars, (still_heights, initial_bars)
                        pulses = page.locator('g.animated[aria-hidden="true"] circle')
                        assert pulses.count() == 2, 'RND input must feed both networks'
                        for idx, t_start, t_finish in ((0, .3, .8), (1, .4, .9)):
                            positions = []
                            for t in (t_start, t_finish):
                                page.evaluate('(t) => document.querySelector("svg").setCurrentTime(t)', t)
                                positions.append(pulses.nth(idx).evaluate(
                                    '(node) => {let b=node.getBoundingClientRect(); return [b.x,b.y]}'
                                ))
                            travel = sum((a-b)**2 for a,b in zip(*positions)) ** .5
                            assert travel > width / 30, f'RND input pulse {idx} stationary'
                    else:
                        # Each visible pulse must travel along its own existing input
                        # dependency. The inverse branch must not feed the forward target.
                        pulses = page.locator('g.animated[aria-hidden="true"] circle')
                        assert pulses.count() == 8, 'missing input, comparison, inverse output, or training-update trace'
                        for pulse_idx, start_t, end_t in (
                            (0, .8, 1.6), (1, 1.9, 2.7),
                            (2, 3.55, 4.55), (3, 3.55, 4.55),
                        ):
                            positions = []
                            for t in (start_t, end_t):
                                page.evaluate('(t) => document.querySelector("svg").setCurrentTime(t)', t)
                                positions.append(pulses.nth(pulse_idx).evaluate(
                                    '(node) => {let b = node.getBoundingClientRect(); return [b.x,b.y] }'
                                ))
                            travel = sum((a-b)**2 for a,b in zip(*positions)) ** .5
                            assert travel > width / 30, (
                                f'{stem} at {width}: stationary input pulse {pulse_idx}'
                            )
                        # Fifth pulse is the inverse model's action estimate,
                        # not an arrow into the forward feature comparison.
                        positions = []
                        for t in (5.1, 5.9):
                            page.evaluate('(t) => document.querySelector("svg").setCurrentTime(t)', t)
                            positions.append(pulses.nth(6).evaluate(
                                '(node) => {let b=node.getBoundingClientRect(); return [b.x,b.y]}'
                            ))
                        output_travel = sum((a-b)**2 for a,b in zip(*positions)) ** .5
                        assert output_travel > width / 85, 'inverse output pulse stationary'
                        # The eighth pulse is a schematic gradient update:
                        # error comparison -> forward model, not reward -> policy.
                        # Its traversal must finish before predictor adaptation.
                        positions = []
                        for t in (3.65, 4.05):
                            page.evaluate('(t) => document.querySelector("svg").setCurrentTime(t)', t)
                            positions.append(pulses.nth(7).evaluate(
                                '(node) => {let b=node.getBoundingClientRect(); return [b.x,b.y]}'
                            ))
                        update_travel = sum((a-b)**2 for a,b in zip(*positions)) ** .5
                        assert update_travel > width / 20, (
                            f'ICM at {width}: missing loss-to-forward training feedback'
                        )
                        # The forward prediction and observed next-state feature
                        # arrive as separate signals before the error shrinks.
                        for idx, a, b in ((4, 3.02, 3.48), (5, 1.72, 3.45)):
                            positions = []
                            for t in (a, b):
                                page.evaluate('(t) => document.querySelector("svg").setCurrentTime(t)', t)
                                positions.append(pulses.nth(idx).evaluate(
                                    '(node) => {let r = node.getBoundingClientRect(); return [r.x,r.y] }'
                                ))
                            travel = sum((x-y)**2 for x,y in zip(*positions)) ** .5
                            assert travel > width / 85, f'ICM comparison pulse {idx} stationary'
                        # No error reduction occurs before both forward inputs
                        # have arrived. Schematic, not an empirical training curve.
                        predicted = page.locator('g.animated line').first
                        page.evaluate('(t) => document.querySelector("svg").setCurrentTime(t)', 3.2)
                        assert predicted.evaluate('(n) => n.x2.animVal.value') == 550, (
                            'ICM error begins to shrink before forward inputs arrive'
                        )
                        page.evaluate('(t) => document.querySelector("svg").setCurrentTime(t)', 4.1)
                        assert predicted.evaluate('(n) => n.x2.animVal.value') == 550, (
                            'ICM predictor improves before training-update cue arrives'
                        )
                        page.evaluate('(t) => document.querySelector("svg").setCurrentTime(t)', 5.6)
                        assert predicted.evaluate('(n) => n.x2.animVal.value') > 570, (
                            'ICM learning phase fails to approach the target feature'
                        )
                        assert 'd="M477 293H499"' in still.read_text(encoding='utf-8')
                    assert page.locator('svg').bounding_box()['width'] <= width + 1
                    # The actual GitHub-friendly still SVG must also be
                    # renderable at each review size, not merely parseable.
                    fallback_html = html.replace(source, still.read_text(encoding='utf-8'))
                    page.set_content(fallback_html)
                    (REVIEW / f'{stem}_{width}_fallback.png').write_bytes(
                        page.locator('svg').screenshot()
                    )
                    assert page.locator('svg').bounding_box()['width'] <= width + 1
                    ctx.close()

                    ctx = browser.new_context(viewport={'width': width + 32, 'height': 640}, reduced_motion='reduce')
                    page = ctx.new_page()
                    page.set_content(html)
                    stills = [hashlib.sha256(frame(page, t)).hexdigest() for t in (0.0, 3.5, 6.0)]
                    assert len(set(stills)) == 1, f'{stem} at {width}: reduced-motion pixels changed'
                    ctx.close()
                print(f'PASS {stem}: three widths, three animation times, reduced-motion stable')

            # Additional RND novelty comparison: a frozen target network's output
            # changes with the input even though its parameters do not. The bonus
            # falls on seen A, then can rise when the observation switches to B.
            novelty = 'rnd-state-novelty'
            motion = ASSETS / f'{novelty}-motion.svg'
            still = ASSETS / f'{novelty}-still.svg'
            assert motion.is_file() and still.is_file()
            source = motion.read_text(encoding='utf-8')
            fallback_source = still.read_text(encoding='utf-8')
            assert 'repeatCount="indefinite"' in source
            assert '<animate ' not in fallback_source
            ET.fromstring(source)
            ET.fromstring(fallback_source)
            for width in (360, 720, 1024):
                html = ('<html><head><meta charset="utf-8"><style>'
                        f'body{{margin:0;padding:14px}}svg{{width:{width}px;height:auto;display:block}}'
                        '</style></head><body>' + source + '</body></html>')
                ctx = browser.new_context(viewport={'width': width + 32, 'height': 640})
                page = ctx.new_page()
                page.set_content(html)
                # Freeze SMIL's clock: screenshots otherwise advance it while sampling
                # coordinates, making the before/after input assertions nondeterministic.
                page.evaluate('document.querySelector("svg").pauseAnimations()')
                # Both A and B must feed the frozen target and predictor before
                # the corresponding observation's output/bonus is evaluated.
                observation_pulses = page.locator(
                    'g.animated[aria-hidden="true"] circle'
                )
                assert observation_pulses.count() == 4, (
                    'RND novelty scene must trace A and B into both networks'
                )
                for idx, a, z in (
                    (0, .2, .9), (1, .2, .9),
                    (2, 6.67, 7.02), (3, 6.67, 7.02),
                ):
                    positions = []
                    for t in (a, z):
                        page.evaluate(
                            '(t) => document.querySelector("svg").setCurrentTime(t)', t
                        )
                        positions.append(observation_pulses.nth(idx).evaluate(
                            '(n) => {let r=n.getBoundingClientRect(); return [r.x,r.y]}'
                        ))
                    travel = sum((x-y)**2 for x,y in zip(*positions)) ** .5
                    assert travel > width / 22, (
                        f'RND observation pulse {idx} stationary at {width}'
                    )
                page.evaluate('(t) => document.querySelector("svg").setCurrentTime(t)', 6.85)
                target_x = page.locator('g.animated line').first.evaluate(
                    '(n) => n.x1.animVal.value'
                )
                assert target_x == 589, (
                    'RND B target response begins before both observation pulses arrive'
                )
                # Distinct observations A and B must not be shown as continuously
                # varying, nonexistent inputs. Both features and the reward cue
                # remain on A until the B input pulses reach the networks (~7.12 s).
                # They then switch together within one visually imperceptible tick.
                def response_at(timestamp):
                    page.evaluate(
                        '(t) => document.querySelector("svg").setCurrentTime(t)',
                        timestamp
                    )
                    coords = page.locator('g.animated line').first.evaluate(
                        '(n) => [n.x1.animVal.value, n.y1.animVal.value, '
                        'n.x2.animVal.value, n.y2.animVal.value]'
                    )
                    bonus = page.locator('rect.animated').first.evaluate(
                        '(n) => n.width.animVal.value'
                    )
                    return coords, bonus

                for timestamp in (6.90, 7.06, 7.10):
                    coords, bonus = response_at(timestamp)
                    assert coords == [589, 145, 572, 158] and abs(bonus - 8) < 1, (
                        'RND B response anticipated input or changed reward early',
                        timestamp, coords, bonus
                    )
                coords, bonus = response_at(7.13)
                assert coords == [550, 202, 621, 139] and abs(bonus - 158) < 1, (
                    'RND target, predictor and bonus did not switch together',
                    coords, bonus
                )
                signatures = []
                for label, t in (('visited', 0.0), ('early', 2.0),
                                 ('learning', 4.0), ('fitted', 6.4),
                                 ('new_state', 7.5), ('adapting_B', 8.3),
                                 ('trained_B', 9.4)):
                    signatures.append(hashlib.sha256(frame(page, t)).hexdigest())
                    (REVIEW / f'{novelty}_{width}_{label}.png').write_bytes(frame(page, t))
                assert len(set(signatures)) >= 4, 'novelty sequence lacks intermediate motion'
                def state_at(t):
                    page.evaluate('(t) => document.querySelector("svg").setCurrentTime(t)', t)
                    return page.locator('g.animated line').first.evaluate(
                        '(node) => [node.x1.animVal.value, node.y1.animVal.value,'
                        ' node.x2.animVal.value, node.y2.animVal.value]'
                    ), page.locator('rect.animated').first.evaluate(
                        '(node) => node.width.animVal.value'
                    )
                initial, initial_bonus = state_at(0)
                fitted, fitted_bonus = state_at(6.4)
                novel, novel_bonus = state_at(7.5)
                assert initial[:2] == fitted[:2] == [589, 145], 'target must remain on A'
                assert fitted_bonus < initial_bonus / 3, 'A error bonus did not fall'
                assert novel[:2] == [550, 202], 'target output did not change on B'
                assert novel_bonus > fitted_bonus * 4, 'B error bonus did not rise'
                # Once B is encountered, additional training on B lowers its
                # prediction error without changing the frozen target output.
                adapted, adapted_bonus = state_at(9.4)
                assert adapted[:2] == novel[:2] == [550, 202], (
                    'target output must stay fixed while training on B'
                )
                assert 550 < adapted[2] < novel[2], 'predictor B x did not approach target'
                assert novel[3] < adapted[3] < 202, 'predictor B y did not approach target'
                assert adapted_bonus < novel_bonus * .35, (
                    'RND B error bonus did not fall after predictor adaptation'
                )
                # The plotted orange circle and dashed error segment must
                # terminate at the same animated predictor coordinate.
                point = page.locator('g.animated circle').last.evaluate(
                    '(node) => [node.cx.animVal.value, node.cy.animVal.value]'
                )
                assert abs(point[0] - adapted[2]) < 1 and abs(point[1] - adapted[3]) < 1, (
                    f'RND B predictor point and error line diverged: {point} vs {adapted}'
                )
                assert page.locator('svg').bounding_box()['width'] <= width + 1
                page.set_content(html.replace(source, fallback_source))
                (REVIEW / f'{novelty}_{width}_fallback.png').write_bytes(
                    page.locator('svg').screenshot()
                )
                ctx.close()

                ctx = browser.new_context(
                    viewport={'width': width + 32, 'height': 640}, reduced_motion='reduce'
                )
                page = ctx.new_page()
                page.set_content(html)
                reduced_frames = [hashlib.sha256(frame(page, t)).hexdigest()
                                  for t in (0.0, 5.0, 9.0)]
                assert len(set(reduced_frames)) == 1, (
                    f'{novelty} at {width}: reduced-motion pixels changed'
                )
                ctx.close()
            print('PASS RND novelty: state-dependent target, reward shift, reduced-motion')

            check_primary_squared_bonus_geometry(browser)
            check_rnd_transfer_motion(browser)
            check_icm_weighted_probability_sweep(browser)
            check_rnd_desktop_squared_bonus(browser)
            check_icm_stochastic_comparison(browser)
            check_icm_mobile_stacked(browser)
            check_rnd_mobile_novelty(browser)

            # This is the repository's real shared MkDocs enhancement, not a mock.
            if PLAYER.is_file():
                with tempfile.TemporaryDirectory() as tmp:
                    fixture = Path(tmp) / 'test.html'
                    for stem in (*STEMS, 'rnd-state-novelty', 'icm-predictable-stochastic'):
                        motion_uri = (ASSETS / f'{stem}-motion.svg').resolve().as_uri()
                        fixture.write_text('<html><body><img alt="RND concept animation" '
                                           f'src="{motion_uri}"></body></html>', encoding='utf-8')
                        ctx = browser.new_context()
                        page = ctx.new_page()
                        page.goto(fixture.as_uri())
                        page.add_script_tag(content=PLAYER.read_text(encoding='utf-8'))
                        toggle = page.get_by_role('button', name='Pause concept animation')
                        assert toggle.count() == 1, f'{stem}: player controls did not load'
                        toggle.click()
                        assert page.locator('img').get_attribute('src').endswith('-still.svg'), stem
                        page.get_by_role('button', name='Play concept animation').focus()
                        page.keyboard.press('Enter')
                        assert page.locator('img').get_attribute('src').endswith('-motion.svg'), stem
                        ctx.close()
                        ctx = browser.new_context(reduced_motion='reduce')
                        page = ctx.new_page()
                        page.goto(fixture.as_uri())
                        page.add_script_tag(content=PLAYER.read_text(encoding='utf-8'))
                        assert page.locator('img').get_attribute('src').endswith('-still.svg'), stem
                        assert page.get_by_role('button', name='Play concept animation').count() == 1
                        ctx.close()
                        print(f'PASS {stem}: MkDocs playback, keyboard, reduced-motion fallback')
            else:
                print('SKIP MkDocs enhancement controls: concept-motion.js not present in local asset-only QA')
        finally:
            browser.close()




def check_icm_weighted_probability_sweep(browser) -> None:
    """Real Chromium geometry and accessibility regression for a moving distribution.

    Fixed outcome coordinates, changing probabilities and the predictive mean
    must stay mathematically consistent with the variance bar at every instant.
    """
    name = "icm-weighted-outcomes"
    source = (ASSETS / (name + "-motion.svg")).read_text(encoding="utf-8")
    fallback = (ASSETS / (name + "-still.svg")).read_text(encoding="utf-8")
    assert ET.fromstring(source).attrib["viewBox"] == "0 0 400 640"
    assert "<animate " in source and "<animate " not in fallback
    # Each moving geometric link shares the matching weighted-risk bar colour.
    svg_root = ET.fromstring(source)
    for n, colour in enumerate(("#267f9f", "#319d91", "#8672b4"), 1):
        ray = svg_root.find(f".//*[@id='icm-outcome-ray-{n}']")
        term = svg_root.find(f".//*[@id='icm-variance-term-{n}']")
        assert ray is not None and term is not None
        assert ray.attrib["stroke"] == term.attrib["fill"] == colour
    points = [(365, 101), (310, 174), (255, 115)]
    for width in (320, 360, 720, 1024):
        context = browser.new_context(viewport={"width": width, "height": 850})
        page = context.new_page()
        page.set_content(
            '<html><body style="margin:0"><style>'
            'svg{width:min(100vw,400px);height:auto;display:block}'
            '</style>' + source + '</body></html>'
        )
        for idx, t in enumerate((0, 1.25, 2.5, 3.75, 5, 6.25, 7.5, 8.75, 9.99)):
            if t <= 2.5:
                skew = -60 + 24 * t
            elif t <= 5:
                skew = 24 * (t - 2.5)
            elif t <= 7.5:
                skew = 60 - 24 * (t - 5)
            else:
                skew = -24 * (t - 7.5)
            probabilities = [(100 + skew) / 300, 1 / 3, (100 - skew) / 300]
            mean_x = sum(p * x for p, (x, y) in zip(probabilities, points))
            mean_y = sum(p * y for p, (x, y) in zip(probabilities, points))
            variance = sum(
                p * ((x - mean_x) ** 2 + (y - mean_y) ** 2)
                for p, (x, y) in zip(probabilities, points)
            )
            data = page.evaluate("""time => {
              const s = document.querySelector('svg');
              s.setCurrentTime(time);
              s.pauseAnimations();
              const point = name => s.getElementById(name);
              return {
                widths: [1,2,3].map(i => point('icm-weight-'+i).width.animVal.value),
                mean: [point('icm-weighted-mean').cx.animVal.value,
                       point('icm-weighted-mean').cy.animVal.value],
                forecast: [point('icm-weighted-forecast').cx.animVal.value,
                           point('icm-weighted-forecast').cy.animVal.value],
                variance: point('icm-weighted-variance').width.animVal.value,
                contributions: [1,2,3].map(i => ({
                  x: point('icm-variance-term-'+i).x.animVal.value,
                  width: point('icm-variance-term-'+i).width.animVal.value
                })),
                rays: [1,2,3].map(i => ({
                  x: point('icm-outcome-ray-'+i).x2.animVal.value,
                  y: point('icm-outcome-ray-'+i).y2.animVal.value
                })),
                overflow: document.documentElement.scrollWidth > innerWidth + 1
              };
            }""", t)
            expected_mean = [70 + 1.9 * (mean_x - 245),
                             210 + 1.9 * (mean_y - 87)]
            assert max(abs(v - 352 * p) for v, p in zip(
                data["widths"], probabilities)) < .2, (width, t, data)
            for key in ("mean", "forecast"):
                assert max(abs(v - expected_mean[i]) for i, v in enumerate(
                    data[key])) < .2, (width, t, key, data)
            for ray in data["rays"]:
                assert abs(ray["x"] - expected_mean[0]) < .2
                assert abs(ray["y"] - expected_mean[1]) < .2
            assert abs(data["variance"] - 326 * variance / 4000) < .2, (
                width, t, variance, data)
            # The three color-coded terms must remain contiguous and add to the
            # moving irreducible risk. Each term is p_i * ||Y_i - mean||².
            component_widths = []
            for i, ((x, y), p) in enumerate(zip(points, probabilities)):
                expected_term = 326 * p * ((x - mean_x) ** 2 + (y - mean_y) ** 2) / 4000
                part = data["contributions"][i]
                assert abs(part["width"] - expected_term) < .2, (width, t, i, part)
                assert abs(part["x"] - (37 + sum(component_widths))) < .2, (
                    width, t, i, "noncontiguous weighted terms", part
                )
                component_widths.append(part["width"])
            assert abs(sum(component_widths) - data["variance"]) < .2, (
                width, t, "component total differs from variance floor", data
            )
            assert not data["overflow"], (width, t, "horizontal overflow")
            if idx in (0, 2, 4, 6, 8):
                (REVIEW / (name + "_" + str(width) + "_" + str(idx) + ".png")).write_bytes(
                    page.locator("svg").screenshot(animations="allow")
                )
        context.close()

    # Existing first-party MkDocs image player pairs -motion/-still by name,
    # and must retain a keyboard-operable pause and reduced-motion fallback.
    if PLAYER.is_file():
        url = "http://127.0.0.1:9/docs/assets/concept-animations/" + name + "-motion.svg"
        for locale, alt in (("en", "ICM weighted outcomes"),
                            ("zh", "ICM 加權結果動畫")):
            context = browser.new_context(viewport={"width": 320, "height": 700})
            page = context.new_page()
            page.set_content('<img alt="' + alt + '" src="' + url + '">')
            page.add_script_tag(content=PLAYER.read_text(encoding="utf-8"))
            img = page.locator("img")
            assert img.get_attribute("src").endswith("-motion.svg")
            page.get_by_role("button", name="Pause concept animation" if locale == "en"
                             else "暫停概念動畫").click()
            assert img.get_attribute("src").endswith("-still.svg")
            page.get_by_role("button", name="Play concept animation" if locale == "en"
                             else "播放概念動畫").focus()
            page.keyboard.press("Enter")
            assert img.get_attribute("src").endswith("-motion.svg")
            context.close()
            context = browser.new_context(
                viewport={"width": 320, "height": 700}, reduced_motion="reduce"
            )
            page = context.new_page()
            page.set_content('<img alt="' + alt + '" src="' + url + '">')
            page.add_script_tag(content=PLAYER.read_text(encoding="utf-8"))
            assert page.locator("img").get_attribute("src").endswith("-still.svg")
            context.close()
    print("PASS weighted ICM: 36 mathematical samples, responsive screenshots, "
          "shared player and reduced motion")

if __name__ == '__main__':
    run()
