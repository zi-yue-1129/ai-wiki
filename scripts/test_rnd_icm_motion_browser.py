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
        assert initial[2][0] == 216 and fitted[2][0] == 12, (initial, fitted)
        assert initial[1] == 666 and second[1] == 594 and third[1] == 669
        assert initial[2][1] == 161 and second[2][1] == 78 and third[2][1] == 173
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

            check_icm_stochastic_comparison(browser)

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


if __name__ == '__main__':
    run()
