"""Chromium integration and screenshot check for deterministic stochastic-bandit labs."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import os

ROOT = Path(__file__).resolve().parent
if (ROOT.parent / "docs/javascripts/bandit-labs.js").exists():
    JS = ROOT.parent / "docs/javascripts/bandit-labs.js"
    CSS = ROOT.parent / "docs/stylesheets/bandit-labs.css"
else:
    JS = ROOT / "bandit-labs.js"
    CSS = ROOT / "bandit-labs.css"
ARTIFACTS = Path(os.environ.get('BANDIT_LAB_ARTIFACTS','artifacts/bandit-labs'))
ARTIFACTS.mkdir(parents=True, exist_ok=True)
HTML = '''<!doctype html><html lang="LANG"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>body{margin:0;padding:20px;font:16px system-ui;color:#213547} main{max-width:860px;margin:auto}</style></head><body>
<main><h1>Stochastic Bandits</h1>
<h2>UCB1</h2><div class="bandit-lab" data-bandit-lab="ucb" data-lang="LANG"><p>Static illustration above remains visible without JavaScript.</p></div>
<h2>Thompson</h2><div class="bandit-lab" data-bandit-lab="thompson" data-lang="LANG"><p>Static fallback.</p></div>
</main></body></html>'''

def main():
    with sync_playwright() as p:
        executable = os.getenv('CHROMIUM_PATH') or ('/usr/bin/chromium' if Path('/usr/bin/chromium').exists() else None)
        browser = p.chromium.launch(headless=True, executable_path=executable, args=['--no-sandbox'])
        cases = 0
        for lang in ('en', 'zh-TW'):
            for width in (320, 360, 720, 1024):
                for reduced in (False, True):
                    context = browser.new_context(
                        viewport={'width': width, 'height': 950},
                        reduced_motion='reduce' if reduced else 'no-preference'
                    )
                    page = context.new_page()
                    errors = []
                    page.on('pageerror', lambda e: errors.append(str(e)))
                    page.set_content(HTML.replace('LANG', lang))
                    assert page.get_by_text('Static fallback.').count() == 1
                    page.add_style_tag(content=CSS.read_text(encoding='utf8'))
                    page.add_script_tag(content=JS.read_text(encoding='utf8'))
                    page.wait_for_selector('[data-bandit-lab="thompson"] [data-role="svg"] path')
                    assert not errors, errors
                    assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth')
                    ucb = page.locator('[data-bandit-lab="ucb"]')
                    ts = page.locator('[data-bandit-lab="thompson"]')
                    assert ucb.locator('[data-role="svg"] rect').count() > 5
                    # Analytic phase diagram is a real, focusable SVG and not a raster or sampled heatmap.
                    boundary = ucb.locator('[data-role="boundary"]')
                    assert boundary.locator('svg polygon').count() == 1
                    assert boundary.locator('svg [data-role="reward-marker"]').count() == 1
                    assert '0.818' in boundary.inner_text()
                    trace = ucb.locator('[data-role="process"]')
                    assert trace.locator('[data-margin-step]').count() == 3
                    assert abs(float(trace.locator('[data-margin-step="0"]').get_attribute('data-delta')) - 0.503758) < 0.00001
                    assert abs(float(trace.locator('[data-margin-step="2"]').get_attribute('data-delta')) + 0.204400) < 0.00001
                    # A separate compact chart must show the exact reason optimism wins at t=16.
                    decomposition = trace.locator('svg[data-mean-gap]')
                    assert decomposition.count() == 1
                    gap_mean = float(decomposition.get_attribute('data-mean-gap'))
                    gap_bonus = float(decomposition.get_attribute('data-bonus-gap'))
                    gap_net = float(decomposition.get_attribute('data-net-gap'))
                    assert abs(gap_mean + 0.2) < 1e-5
                    assert abs(gap_bonus - 0.703758) < 1e-5
                    assert abs(gap_net - (gap_mean + gap_bonus)) < 2e-6
                    # The phase plane itself selects the two counterfactual rewards.
                    # It must agree with the sliders and recomputed analytic winner.
                    boundary.locator('svg').click(position={'x': 199, 'y': 43})  # r1=r2=.9
                    assert abs(float(ucb.locator('[data-role="reward1"]').input_value())-.9)<1e-9
                    assert abs(float(ucb.locator('[data-role="reward2"]').input_value())-.9)<1e-9
                    assert 'B' in boundary.locator('.bandit-lab-boundary-note').inner_text()
                    assert 'B.' in ucb.locator('[data-role="status"]').inner_text()
                    boundary.locator('svg').click(position={'x': 79, 'y': 163}) # r1=r2=.15
                    assert abs(float(ucb.locator('[data-role="reward1"]').input_value())-.15)<1e-9
                    assert 'A' in boundary.locator('.bandit-lab-boundary-note').inner_text()
                    # Restore the original state before independent slider tests.
                    ucb.locator('[data-action="reset"]').click()
                    initial_x = float(boundary.locator('[data-role="reward-marker"]').get_attribute('cx'))
                    assert 'A' in boundary.locator('.bandit-lab-boundary-note').inner_text()
                    assert 'B' in ucb.locator('[data-role="metrics"]').inner_text()
                    ucb.locator('[data-role="seek"]').fill('2')
                    assert 'A' in ucb.locator('[data-role="metrics"]').inner_text()
                    assert '1.63' in ucb.locator('[data-role="metrics"]').inner_text()
                    # With both constructed rewards zero, exploration no longer
                    # offsets B's empirical disadvantage on the third decision.
                    assert abs(float(decomposition.get_attribute('data-mean-gap')) + 0.425) < 1e-6
                    assert 0.220 < float(decomposition.get_attribute('data-bonus-gap')) < 0.222
                    assert float(decomposition.get_attribute('data-net-gap')) < 0
                    # A single good reward can overturn the second-pull switch.
                    ucb.locator('[data-role="reward1"]').fill('1')
                    assert float(boundary.locator('[data-role="reward-marker"]').get_attribute('cx')) > initial_x
                    assert 'B' in boundary.locator('.bandit-lab-boundary-note').inner_text()
                    assert 'B' in ucb.locator('[data-role="metrics"]').inner_text()
                    assert '0.000' not in ucb.locator('[data-role="metrics"]').inner_text()
                    assert float(trace.locator('[data-margin-step="2"]').get_attribute('data-delta')) > 0
                    # The second reward must not affect the state after the first pull.
                    ucb.locator('[data-role="seek"]').fill('1')
                    score_before = ucb.locator('[data-role="metrics"]').inner_text()
                    ucb.locator('[data-role="reward2"]').fill('1')
                    assert ucb.locator('[data-role="metrics"]').inner_text() == score_before
                    ucb.locator('[data-role="reward1"]').fill('0')
                    assert ucb.locator('[data-role="metrics"]').inner_text() != score_before
                    # At step two, reward2 can independently change the winner.
                    ucb.locator('[data-role="seek"]').fill('2')
                    assert 'B' in ucb.locator('[data-role="metrics"]').inner_text()
                    ucb.locator('[data-role="reward2"]').fill('0')
                    assert 'A' in ucb.locator('[data-role="metrics"]').inner_text()
                    assert 'A' in boundary.locator('.bandit-lab-boundary-note').inner_text()
                    assert 'Highest observed mean' in ucb.locator('[data-role="metrics"]').inner_text() or lang == 'zh-TW'
                    ucb.locator('[data-action="reset"]').click()
                    assert ucb.locator('[data-role="seek"]').input_value() == '0'
                    # Independent posterior-optimality probabilities must sum to one.
                    probabilities = ts.locator('[data-role="probabilities"] [data-prob]')
                    assert probabilities.count() == 3
                    initial = [float(probabilities.nth(i).get_attribute('data-prob')) for i in range(3)]
                    assert abs(sum(initial)-1.0) < 0.0001, initial
                    assert 0.57 < initial[2] < 0.58, initial
                    assert ts.locator('[role="meter"]').count() == 3
                    credible = ts.locator('[data-role="process"] svg[data-cred-low]')
                    assert credible.count() == 1
                    assert abs(float(credible.get_attribute('data-cred-low')) - 0.271338) < 1e-5
                    assert abs(float(credible.get_attribute('data-cred-high')) - 0.846839) < 1e-5
                    ts.locator('[data-action="next"]').click()
                    assert 'C' in ts.locator('[data-role="metrics"]').inner_text()
                    assert '0.5714' in ts.locator('[data-role="metrics"]').inner_text()
                    assert '0.0306' in ts.locator('[data-role="metrics"]').inner_text()
                    evidence = ts.locator('[data-role="process"] svg')
                    assert evidence.get_attribute('data-alpha') == '4' and evidence.get_attribute('data-beta') == '3'
                    assert ts.locator('[data-new-pseudo]').count() == 0
                    assert ts.locator('[data-role="svg"] circle').count() == 3
                    # Drawing a sample never changes an underlying Bayesian posterior.
                    assert abs(float(credible.get_attribute('data-cred-low')) - 0.271338) < 1e-5
                    ts.locator('[data-action="next"]').click()
                    assert '(5,3)' in ts.locator('[data-role="metrics"]').inner_text()
                    # A sample dot from the old posterior must not be repositioned on the updated curve.
                    assert ts.locator('[data-role="svg"] circle').count() == 0
                    # An earlier draw cannot be reported as a sample from a revised posterior.
                    selected_or_samples = ts.locator('[data-role="metrics"] span').all_inner_texts()
                    assert any('—' in v and ('draw' in v.lower() or '抽樣' in v) for v in selected_or_samples), selected_or_samples
                    assert '0.6250' in ts.locator('[data-role="metrics"]').inner_text()
                    assert '0.0260' in ts.locator('[data-role="metrics"]').inner_text()
                    assert evidence.get_attribute('data-alpha') == '5' and evidence.get_attribute('data-beta') == '3'
                    assert ts.locator('[data-new-pseudo="alpha"]').count() == 1
                    assert abs(float(credible.get_attribute('data-cred-low')) - 0.341261) < 1e-5
                    assert abs(float(credible.get_attribute('data-cred-high')) - 0.871244) < 1e-5
                    success = float(probabilities.nth(2).get_attribute('data-prob'))
                    assert success > initial[2] and 0.66 < success < 0.67
                    ts.locator('[data-role="outcome"]').select_option('0')
                    assert '(4,4)' in ts.locator('[data-role="metrics"]').inner_text()
                    assert '0.5000' in ts.locator('[data-role="metrics"]').inner_text()
                    assert '0.0278' in ts.locator('[data-role="metrics"]').inner_text()
                    assert evidence.get_attribute('data-alpha') == '4' and evidence.get_attribute('data-beta') == '4'
                    assert ts.locator('[data-new-pseudo="beta"]').count() == 1
                    assert ts.locator('[data-new-pseudo="alpha"]').count() == 0
                    assert abs(float(credible.get_attribute('data-cred-low')) - 0.225322) < 1e-5
                    assert abs(float(credible.get_attribute('data-cred-high')) - 0.774678) < 1e-5
                    failure = float(probabilities.nth(2).get_attribute('data-prob'))
                    assert 0.45 < failure < 0.46 and failure < initial[2]
                    ts.locator('[data-action="next"]').click()
                    assert 'A' in ts.locator('[data-role="metrics"]').inner_text()
                    assert ts.locator('[data-role="svg"] circle').count() == 3
                    ts.locator('[data-action="reset"]').click()
                    assert '(4,3)' in ts.locator('[data-role="metrics"]').inner_text()
                    if width <= 360:
                        assert page.evaluate(
                            'document.querySelector(".bandit-lab-canvas").scrollWidth > document.querySelector(".bandit-lab-canvas").clientWidth'
                        )
                        assert ucb.locator('.bandit-lab-scroll-hint').is_visible()
                        assert ts.locator('.bandit-lab-scroll-hint').is_visible()
                        assert boundary.locator('.bandit-lab-boundary-scroll').is_visible()
                        assert ts.locator('[data-role="process"]').get_attribute('tabindex') == '0'
                        assert ts.locator('[data-role="process"]').evaluate(
                            '(node) => node.scrollWidth > node.clientWidth'
                        )
                    if reduced:
                        ucb.locator('[data-action="toggle"]').click()
                        assert ucb.locator('[data-action="toggle"]').inner_text() in ('Play', '播放')
                    else:
                        ucb.locator('[data-action="toggle"]').click()
                        assert ucb.locator('[data-action="toggle"]').inner_text() in ('Pause', '暫停')
                        ucb.locator('[data-action="toggle"]').click()
                    if width in (320, 360, 1024) and not reduced:
                        page.screenshot(path=str(ARTIFACTS / f'{lang}-{width}.png'), full_page=True)
                        # Review the independent reward switch and posterior failure visually,
                        # not only the initial diagrams or XML structure.
                        if width in (320, 1024):
                            ucb.locator('[data-role="reward2"]').fill('1')
                            ucb.locator('[data-role="seek"]').fill('2')
                            ts.locator('[data-role="seek"]').fill('2')
                            ts.locator('[data-role="outcome"]').select_option('0')
                            page.screenshot(
                                path=str(ARTIFACTS / f'{lang}-{width}-counterfactual.png'),
                                full_page=True,
                            )
                    cases += 1
                    context.close()
        browser.close()
        print(f'{cases} Chromium bilingual/viewport/reduced-motion cases passed')


if __name__ == '__main__':
    main()
