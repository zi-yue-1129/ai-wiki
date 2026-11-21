#!/usr/bin/env python3
"""Chromium regression for overlapping commands in two bilingual SVG timeline players.

The browser runs the real player and SVGs. Fetch is deliberately held until both
user actions have fired, so the test detects stale async continuations.
This is a same-origin fetch simulation, not a built-MkDocs end-to-end test.
"""
import base64
import os
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "docs/assets/concept-animations"
PLAYER = ROOT / "docs/javascripts/selective-accuracy-player.js"
CASES = [("accuracy-selective-coverage", "4/6"),
         ("accuracy-selective-class-coverage", "5/5")]
CSS = """body{margin:0;padding:8px;font-family:Arial,sans-serif}
.concept-motion-player{display:block;max-width:640px}
.concept-motion-player img,.concept-motion-inline{display:block;width:100%;height:auto}
.concept-motion-inline[hidden]{display:none!important}
.concept-motion-controls{display:flex;gap:6px;flex-wrap:wrap}
.concept-motion-chapter-note,.concept-motion-calculation{display:block}
"""


def markup(stem, zh):
    alt = "人工分類示意" if zh else "Synthetic classification"
    still = "data:image/svg+xml;base64," + base64.b64encode(
        (ASSETS / (stem + "-still.svg")).read_bytes()).decode()
    return f"""<!doctype html><meta charset="utf-8">
    <meta name="viewport" content="width=device-width">
    <base href="https://example.invalid/">
    <style>{CSS}</style><section style="max-width:100%;overflow-x:auto">
    <img style="display:block;width:640px;max-width:none" src="{still}" data-still-src="{still}"
    data-motion-src="/assets/concept-animations/{stem}-motion.svg"
    alt="{alt}" width="640" height="360"></section>"""


def run():
    source = {
        f"/assets/concept-animations/{stem}-motion.svg":
        (ASSETS / (stem + "-motion.svg")).read_text(encoding="utf-8")
        for stem, _ in CASES
    }
    with sync_playwright() as p:
        opts = {"headless": True}
        if os.environ.get("PLAYWRIGHT_CHROMIUM_EXECUTABLE"):
            opts.update(
                executable_path=os.environ["PLAYWRIGHT_CHROMIUM_EXECUTABLE"],
                args=["--no-sandbox"],
            )
        browser = p.chromium.launch(**opts)
        try:
            for stem, expected in CASES:
                for zh in (False, True):
                    for width in (390, 1280):
                        ctx = browser.new_context(
                            viewport={"width": width, "height": 900},
                            reduced_motion="no-preference",
                        )
                        page = ctx.new_page()
                        errors = []
                        page.on("pageerror", lambda error: errors.append(str(error)))
                        page.set_content(markup(stem, zh))
                        page.evaluate("(v) => window.__sources = v", source)
                        # about:blank has an opaque origin. Map URL.origin to the
                        # simulated document origin only inside this isolated test.
                        page.evaluate("""() => {
                          const URLNative = window.URL;
                          window.URL = class extends URLNative {
                            constructor(input, base) {
                              super(input, base);
                              Object.defineProperty(this, 'origin',
                                {get:()=>location.origin});
                            }
                          };
                          window.pendingFetch = [];
                          window.fetch = url => new Promise(resolve => {
                            window.pendingFetch.push(() =>
                              resolve({ok:true, text:async() =>
                                window.__sources[new URL(url).pathname]}));
                          });
                        }""")
                        page.add_script_tag(content=PLAYER.read_text(encoding="utf-8"))
                        host = page.locator(".selective-motion-player")
                        assert host.count() == 1
                        page.wait_for_function("window.pendingFetch.length === 1")
                        play = "播放" if zh else "Play"
                        host.get_by_role("button", name=play).click()
                        host.get_by_role(
                            "button", name="下一步" if zh else "Next step"
                        ).click()
                        page.evaluate("window.pendingFetch[0]()")
                        host.locator("svg.concept-motion-inline").wait_for()
                        page.wait_for_timeout(140)
                        plot = host.locator("svg.selective-linked-plot")
                        assert plot.count() == 1, ("linked plot missing", stem, zh, width)
                        # Both linked charts must retain their 640px reading
                        # geometry under mobile widths, not shrink 12px labels.
                        layout = plot.evaluate("""svg => {
                          const scroller = svg.closest('section');
                          return {chart:svg.getBoundingClientRect().width,
                            scrollWidth:scroller.scrollWidth,
                            clientWidth:scroller.clientWidth};
                        }""")
                        assert abs(layout["chart"] - 640) < 1, (
                            "linked SVG text scaled down", stem, zh, width, layout)
                        if width < 640:
                            assert layout["scrollWidth"] > layout["clientWidth"], (
                                "linked chart cannot be scrolled on mobile",
                                stem, zh, width, layout)
                        slider = host.get_by_role("slider")
                        assert slider.input_value() == "40", (
                            stem, zh, width, slider.input_value())
                        assert expected in host.locator(
                            ".concept-motion-calculation").inner_text()
                        assert plot.get_attribute("data-active-stage") == "1"
                        # Stage changes have one localized semantic announcement.
                        # role=status is reserved for loading/errors, never a
                        # second (or stale) stage label announced by assistive tech.
                        status = host.locator(".concept-motion-status")
                        assert status.get_attribute("role") == "status"
                        assert status.inner_text() == "", (stem, zh, width)
                        # Announce the actual arithmetic once per stage rather
                        # than only a generic title; the title stays readable.
                        title = host.locator(".concept-motion-chapter-note")
                        calculation = host.locator(".concept-motion-calculation")
                        assert title.get_attribute("aria-live") == "off"
                        assert calculation.get_attribute("aria-live") == "polite"
                        assert calculation.get_attribute("aria-atomic") == "true"
                        assert expected in calculation.inner_text()
                        keyword = (("正確" if zh else "Correct")
                                   if stem == "accuracy-selective-class-coverage"
                                   else ("接受" if zh else "Accepted"))
                        assert keyword in calculation.inner_text()
                        if stem == "accuracy-selective-coverage":
                            assert "4/6" in plot.get_attribute("aria-label")
                            assert "25%" in plot.get_attribute("aria-label")
                            assert plot.locator(
                                "circle[stroke='#dc743b']").get_attribute("cx") == "400"
                            # All six exact integer cutoffs, including two
                            # local risk decreases; only 2/4/6 are clickable.
                            dots = plot.locator("circle[data-risk-k]")
                            assert dots.count() == 6
                            assert [dots.nth(i).get_attribute("data-risk-k")
                                    for i in range(6)] == [
                                        str(i) for i in range(1,7)]
                            assert float(dots.nth(2).get_attribute("cy")) < float(
                                dots.nth(3).get_attribute("cy"))
                            assert float(dots.nth(4).get_attribute("cy")) < float(
                                dots.nth(5).get_attribute("cy"))
                            assert [dots.nth(i).get_attribute("fill")
                                    for i in range(6)] == [
                                        "#f8fafc", "#087e85",
                                        "#f8fafc", "#087e85",
                                        "#f8fafc", "#087e85"]
                            # Focus traversal follows k=1..6 rather than grouping
                            # hollow inspection points before playable milestones.
                            focusables = plot.locator('[tabindex="0"]')
                            assert focusables.count() == 6
                            assert focusables.evaluate_all('''nodes => nodes.map(n =>
                              n.getAttribute('data-risk-k') ||
                              String(2 + 2*Number(n.getAttribute('data-acceptance-stage'))))''') == [
                                '1','2','3','4','5','6']
                            # Intermediate hollow markers are inspectable without
                            # changing the playable SVG's 2/4/6 acceptance masks.
                            inspection = plot.locator("text[data-risk-inspection]")
                            assert inspection.count() == 1
                            assert "k=4" in inspection.text_content()
                            assert "1/4 wrong" in inspection.text_content()
                            assert "↓8.3 pp" in inspection.text_content()
                            hollow3 = plot.locator("circle[data-risk-k='3']")
                            assert hollow3.get_attribute("role") == "button"
                            assert hollow3.get_attribute("tabindex") == "0"
                            assert "33.3%" in hollow3.get_attribute("aria-label")
                            assert (("增加 33.3 個百分點" if zh else
                                     "increase 33.3 percentage points")
                                    in hollow3.get_attribute("aria-label"))
                            assert ("選擇性風險" if zh else "risk") in (
                                hollow3.get_attribute("aria-label"))
                            # Synthetic click covers touch activation, independent
                            # of mouseenter and without moving the main timeline.
                            hollow3.dispatch_event('click')
                            assert 'k=3' in inspection.text_content()
                            assert slider.input_value() == '40'
                            # The larger pointer-only overlay should be operable
                            # by touch/click, focus the named visible marker and
                            # not add extra Tab stops or move the main SVG.
                            touch_targets = plot.locator('circle[data-risk-touch-k]')
                            assert touch_targets.count() == 3
                            assert [touch_targets.nth(i).get_attribute('r')
                                    for i in range(3)] == ['16','16','16']
                            touch3 = plot.locator('circle[data-risk-touch-k="3"]')
                            touch3.click()
                            assert hollow3.evaluate('(e) => document.activeElement === e')
                            assert 'k=3' in inspection.text_content()
                            assert slider.input_value() == '40'
                            hollow3.focus()
                            assert "k=3" in inspection.text_content()
                            assert "1/3 wrong" in inspection.text_content()
                            assert "+WRONG" in inspection.text_content()
                            assert any(term in hollow3.get_attribute("aria-label")
                                       for term in ("newly admitted incorrect", "新增錯誤"))
                            assert "33.3%" in inspection.text_content()
                            assert "↑33.3 pp" in inspection.text_content()
                            next_case = plot.locator("text[data-next-case]")
                            assert next_case.count() == 1
                            assert "+CORRECT 1/4 (25%)" in next_case.text_content()
                            assert "+WRONG 2/4 (50%)" in next_case.text_content()
                            correct_bar = plot.locator('rect[data-next-bar="correct"]')
                            wrong_bar = plot.locator('rect[data-next-bar="wrong"]')
                            assert float(correct_bar.get_attribute('width')) == 90
                            assert float(wrong_bar.get_attribute('width')) == 180
                            assert plot.locator('text[data-next-value="correct"]').text_content() == '1/4 25%'
                            assert plot.locator('text[data-next-value="wrong"]').text_content() == '2/4 50%'
                            observed = plot.locator('circle[data-next-observed]')
                            observed_note = plot.locator('text[data-next-observed-label]')
                            assert observed.count() == 1
                            assert observed.get_attribute('cx') == '238'
                            assert observed.get_attribute('cy') == '253.5'
                            assert observed.get_attribute('r') == '5'
                            assert observed_note.text_content() == 'IN SAMPLE: +CORRECT'
                            spread = plot.locator('path[data-next-spread]')
                            spread_value = plot.locator('text[data-next-spread-value]')
                            assert spread.count() == 1
                            assert spread_value.text_content() == 'Δ 25 pp'
                            assert spread.get_attribute('d') == 'M 238 304V315 M 238 310H328 M 328 304V315'
                            assert ("25 percentage points" if not zh else
                                    "25 個百分點") in hollow3.get_attribute("aria-label")
                            assert ("假設下一筆正確" if zh else "if correct") in (
                                hollow3.get_attribute("aria-label"))
                            assert hollow3.get_attribute("stroke") == "#193e69"
                            page.keyboard.press("Space")
                            assert slider.input_value() == "40", (
                                "Inspect must not seek the playable SVG")
                            assert plot.get_attribute("data-active-stage") == "1"
                            plot.locator("circle[data-acceptance-stage='1']").focus()
                            assert "↓8.3 pp" in inspection.text_content()
                            assert "+CORRECT 1/5 (20%)" in next_case.text_content()
                            assert "+WRONG 2/5 (40%)" in next_case.text_content()
                            assert float(correct_bar.get_attribute('width')) == 72
                            assert float(wrong_bar.get_attribute('width')) == 144
                            assert spread_value.text_content() == 'Δ 20 pp'
                            assert observed.get_attribute('cx') == '292'
                            assert observed.get_attribute('cy') == '284.5'
                            assert observed_note.text_content() == 'IN SAMPLE: +WRONG'
                            assert spread.get_attribute('d') == 'M 220 304V315 M 220 310H292 M 292 304V315'
                            assert "+CORRECT" in inspection.text_content()
                            hollow5 = plot.locator("circle[data-risk-k='5']")
                            hollow5.focus()
                            assert "k=5" in inspection.text_content()
                            assert "2/5 wrong" in inspection.text_content()
                            assert "↑15 pp" in inspection.text_content()
                            assert observed.get_attribute('cx') == '268'
                            assert observed.get_attribute('cy') == '253.5'
                            assert observed_note.text_content() == 'IN SAMPLE: +CORRECT'
                            plot.locator("circle[data-acceptance-stage='2']").focus()
                            assert "k=6" in inspection.text_content()
                            assert "↓6.7 pp" in inspection.text_content()
                            assert "END OF SIX OBSERVED CASES" in next_case.text_content()
                            assert float(correct_bar.get_attribute('width')) == 0
                            assert float(wrong_bar.get_attribute('width')) == 0
                            assert spread.get_attribute('d') == ''
                            assert spread_value.text_content() == '—'
                            assert observed.get_attribute('r') == '0'
                            assert observed_note.text_content() == ''
                            assert plot.locator('text[data-next-value="correct"]').text_content() == '—'
                            assert plot.locator('text[data-next-value="wrong"]').text_content() == '—'
                            # A mobile horizontal scroll may dispatch hover changes
                            # under a stationary pointer. Explicit keyboard focus
                            # must retain its exact k=6 mathematical explanation.
                            hollow3.dispatch_event("mouseenter")
                            assert "k=6" in inspection.text_content()
                            touch3.dispatch_event("mouseenter")
                            assert "k=6" in inspection.text_content()
                            touch3.dispatch_event("mouseleave")
                            assert "k=6" in inspection.text_content()
                            assert "↓6.7 pp" in inspection.text_content()
                            # Deliberately moving focus outside the plot restores
                            # pointer inspection, then returns to the selected k=4.
                            # An earlier Playwright touch/click leaves the physical
                            # pointer on the enlarged k=3 target. Move it away
                            # before simulating fresh enter/leave events; otherwise
                            # real overlay hover competes with synthetic events.
                            page.mouse.move(8, 8)
                            slider.focus()
                            assert slider.evaluate("(e) => document.activeElement === e")
                            hollow3.dispatch_event("mouseenter")
                            assert "k=3" in inspection.text_content()
                            hollow3.dispatch_event("mouseleave")
                            assert "k=4" in inspection.text_content()
                            assert slider.input_value() == "40"
                            assert plot.get_attribute("viewBox") == "0 0 640 356"
                            # The class chart keeps its independent native dimensions.
                            # Select cutoffs using both pointer and keyboard.
                            points = plot.locator("circle[data-acceptance-stage]")
                            assert points.count() == 3
                            assert all(points.nth(i).get_attribute("role") == "button"
                                       for i in range(3))
                            points.nth(0).click()
                            assert slider.input_value() == "0"
                            assert points.nth(0).get_attribute("aria-pressed") == "true"
                            points.nth(2).focus()
                            page.keyboard.press("Enter")
                            assert slider.input_value() == "80"
                            assert points.nth(2).get_attribute("aria-pressed") == "true"
                            points.nth(1).focus()
                            page.keyboard.press("Space")
                            assert slider.input_value() == "40"
                            assert points.nth(1).get_attribute("aria-pressed") == "true"
                            assert "4/6" in calculation.inner_text()
                            # Keyboard traversal also changes the discrete accepted set,
                            # not just the focus ring or a continuous timeline value.
                            page.keyboard.press("ArrowRight")
                            assert slider.input_value() == "80"
                            assert points.nth(2).evaluate("(e) => document.activeElement === e")
                            page.keyboard.press("Home")
                            assert slider.input_value() == "0"
                            assert points.nth(0).evaluate("(e) => document.activeElement === e")
                            page.keyboard.press("End")
                            assert slider.input_value() == "80"
                            page.keyboard.press("ArrowLeft")
                            assert slider.input_value() == "40"
                            assert "4/6" in calculation.inner_text()
                            assert status.inner_text() == ""
                            host.get_by_role(
                                "button", name="下一步" if zh else "Next step"
                            ).click()
                            assert slider.input_value() == "80"
                            assert plot.get_attribute("data-active-stage") == "2"
                            assert "33%" in plot.get_attribute("aria-label")
                            assert plot.locator(
                                "circle[stroke='#dc743b']").get_attribute("cx") == "560"
                            host.get_by_role(
                                "button", name="上一步" if zh else "Previous step"
                            ).click()
                            assert slider.input_value() == "40"
                            assert plot.get_attribute("data-active-stage") == "1"
                            # Risk inspection must also pause running playback,
                            # without seeking to the non-playable k=3 cutoff.
                            host.get_by_role("button", name=play).click()
                            page.wait_for_timeout(140)
                            assert int(slider.input_value()) > 40
                            hollow3.focus()
                            focused_position = slider.input_value()
                            assert "k=3" in inspection.text_content()
                            assert host.get_by_role("button", name=play).count() == 1
                            page.wait_for_timeout(180)
                            assert slider.input_value() == focused_position, (
                                "risk inspection kept animating", zh, width)
                            assert plot.get_attribute("data-active-stage") == "1"
                            points.nth(1).click()
                            assert slider.input_value() == "40"
                        else:
                            assert "1/4" in plot.get_attribute("aria-label")
                            assert "5/8" in plot.get_attribute("aria-label")
                            assert ("接受 5/8" if zh else "Accepted 5/8") in calculation.inner_text()
                            overall = plot.locator("text[data-overall-metrics]")
                            assert overall.count() == 1
                            # SVG <text> is an SVGElement, not HTMLElement: Playwright's
                            # inner_text() evaluates HTMLElement.innerText and fails in Chromium.
                            # text_content() reads the actual SVG text node, including
                            # after the player updates its accepted/correct ratios.
                            assert overall.text_content() == "5/8 accepted · 5/5 correct"
                            gap = plot.locator("text[data-class-gap]")
                            assert gap.count() == 1
                            assert gap.text_content() == "GAP 75 pp"
                            rejected = plot.locator("text[data-rejected-metrics]")
                            assert rejected.count() == 1
                            assert plot.get_attribute("viewBox") == "0 0 640 420"
                            cases = plot.locator("rect[data-case-id]")
                            assert cases.count() == 8
                            assert [cases.nth(i).get_attribute("data-case-correct")
                                    for i in range(8)] == [
                                "true", "false", "false", "true",
                                "true", "true", "true", "true"]
                            assert [cases.nth(i).get_attribute("data-case-accepted")
                                    for i in range(8)] == [
                                "true", "false", "false", "false",
                                "true", "true", "true", "true"]
                            # P4 stays right despite selective rejection.
                            assert cases.nth(3).get_attribute("data-case-correct") == "true"
                            assert cases.nth(3).get_attribute("stroke-dasharray") == "4 3"
                            # Case provenance: focus, navigation, exact outcomes,
                            # translated semantic labels, and no timeline seek.
                            case_controls = plot.locator("g[data-case-control]")
                            assert case_controls.count() == 8
                            assert all(case_controls.nth(i).get_attribute("role") == "button"
                                       for i in range(8))
                            detail = plot.locator("text[data-case-inspection]")
                            assert detail.text_content() == "✓ right · × wrong"
                            case_controls.nth(3).focus()
                            assert detail.text_content() == "P4: RIGHT · REJECTED → +1 OUT"
                            # Inspecting a correct but rejected example identifies
                            # exactly which conservation row/subset gets its +1.
                            chip = plot.locator("g[data-case-contribution]")
                            right_dot = plot.locator("circle[cx='40'][cy='216']")
                            wrong_dot = plot.locator("circle[cx='40'][cy='241']")
                            assert chip.get_attribute("visibility") == "visible"
                            assert chip.locator("text").text_content() == "+1 OUT"
                            flip = plot.locator("text[data-flip-preview]")
                            marker = plot.locator("line[data-flip-marker]")
                            assert flip.text_content() == (
                                "P4 → 6/6 RIGHT · POS 2/4 · NEG 4/4 · GAP 50 pp")
                            assert marker.get_attribute("visibility") == "visible"
                            assert marker.get_attribute("x1") == "323.5"
                            assert marker.get_attribute("y1") == "55"
                            assert (("若只反轉" if zh else "flipping only") in
                                    case_controls.nth(3).get_attribute("aria-label"))
                            assert cases.nth(3).get_attribute("data-case-accepted") == "false"
                            assert chip.locator("rect").get_attribute("y") == "205"
                            assert right_dot.get_attribute("r") == "8"
                            assert wrong_dot.get_attribute("r") == "5"
                            assert plot.locator("text[data-correct-balance]").get_attribute("fill") == "#087e85"
                            assert ("計數一筆" if zh else "contributes one") in (
                                case_controls.nth(3).get_attribute("aria-label"))
                            # The +1 footer remains legible without scrolling to
                            # the far-right chip at native-width phone viewports.
                            assert detail.evaluate(
                                "el => el.getBBox().x + el.getBBox().width"
                            ) < 390
                            assert cases.nth(3).get_attribute("stroke-width") == "3"
                            assert cases.nth(3).get_attribute("stroke") == "#193e69"
                            assert ("預測正確" if zh else "correct") in (
                                case_controls.nth(3).get_attribute("aria-label"))
                            assert ("拒答" if zh else "rejected") in (
                                case_controls.nth(3).get_attribute("aria-label"))
                            page.keyboard.press("ArrowLeft")
                            assert case_controls.nth(2).evaluate(
                                "(e) => document.activeElement === e")
                            assert detail.text_content() == "P3: WRONG · REJECTED → +1 OUT"
                            assert flip.text_content() == (
                                "P3 → 5/6 RIGHT · POS 2/4 · NEG 4/4 · GAP 50 pp")
                            assert chip.locator("text").text_content() == "+1 OUT"
                            assert chip.locator("rect").get_attribute("y") == "230"
                            assert right_dot.get_attribute("r") == "5"
                            assert wrong_dot.get_attribute("r") == "8"
                            assert plot.locator("text[data-wrong-balance]").get_attribute("fill") == "#b45336"
                            page.keyboard.press("Home")
                            assert detail.text_content() == "P1: RIGHT · ACCEPTED → +1 IN"
                            assert flip.text_content() == (
                                "P1 → 4/4 RIGHT · POS 0/4 · NEG 4/4 · GAP 100 pp")
                            page.keyboard.press("End")
                            assert detail.text_content() == "N4: RIGHT · ACCEPTED → +1 IN"
                            assert flip.text_content() == (
                                "N4 → 4/4 RIGHT · POS 1/4 · NEG 3/4 · GAP 50 pp")
                            assert marker.get_attribute("y1") == "103"
                            page.keyboard.press("Space")
                            assert slider.input_value() == "40"
                            bounds = detail.evaluate("""el => {
                              const b=el.getBBox();
                              return {left:b.x,right:b.x+b.width,bottom:b.y+b.height};
                            }""")
                            assert bounds["left"] >= 0 and bounds["right"] <= 630
                            assert bounds["bottom"] <= 420
                            assert rejected.text_content() == (
                                "3/8 rejected · 1/3 correct · 2/3 wrong")
                            right = plot.locator("text[data-correct-balance]")
                            wrong = plot.locator("text[data-wrong-balance]")
                            assert right.text_content() == (
                                "RIGHT 6 = 5 accepted + 1 rejected")
                            assert wrong.text_content() == (
                                "WRONG 2 = 0 accepted + 2 rejected")
                            assert ("拒答 3/8" if zh else "3/8 rejected") in (
                                plot.get_attribute("aria-label"))
                            assert ("2/3 錯誤" if zh else "2/3 wrong") in (
                                calculation.inner_text())
                            assert (("75 個百分點" if zh else "75 percentage points")
                                    in plot.get_attribute("aria-label"))
                            assert (("類別覆蓋差距 75" if zh else "class gap 75 pp")
                                    in calculation.inner_text())
                            assert plot.locator(
                                "rect[fill='#087e85']").get_attribute("width") == "103.75"
                            # Both class-coverage rules are directly selectable.
                            # Verify pointer, Enter, Space, focused button
                            # state, and the synchronized chart/trace/timeline.
                            choices = plot.locator("g[data-acceptance-stage]")
                            assert plot.get_attribute("role") == "group"
                            assert choices.count() == 2
                            assert all(choices.nth(i).get_attribute("role") == "button"
                                       for i in range(2))
                            assert choices.nth(1).get_attribute("aria-pressed") == "true"
                            choices.nth(0).click()
                            assert slider.input_value() == "0"
                            assert choices.nth(0).get_attribute("aria-pressed") == "true"
                            # Pointer focus must not mask the selected fill:
                            # the focused choice has BOTH a teal selected background
                            # and a dark keyboard-focus outline.
                            assert choices.nth(0).locator("rect").get_attribute("fill") == "#e3f0ef"
                            assert choices.nth(0).locator("rect").get_attribute("stroke") == "#193e69"
                            assert choices.nth(1).locator("rect").get_attribute("fill") == "#ffffff"
                            case_controls.nth(3).focus()
                            assert detail.text_content() == "P4: RIGHT · ACCEPTED → +1 IN"
                            assert flip.text_content() == (
                                "P4 → 5/7 RIGHT · POS 3/4 · NEG 4/4 · GAP 25 pp")
                            assert chip.locator("text").text_content() == "+1 IN"
                            assert chip.locator("rect").get_attribute("fill") == "#e3f0ef"
                            assert chip.locator("rect").get_attribute("y") == "205"
                            assert ("接受" if zh else "accepted") in (
                                case_controls.nth(3).get_attribute("aria-label"))
                            assert cases.nth(3).get_attribute("data-case-correct") == "true"
                            choices.nth(0).focus()
                            assert detail.text_content() == "✓ right · × wrong"
                            assert chip.get_attribute("visibility") == "hidden"
                            assert marker.get_attribute("visibility") == "hidden"
                            assert flip.text_content() == "FOCUS A CASE TO PREVIEW FLIP"
                            assert right_dot.get_attribute("r") == "5"
                            assert wrong_dot.get_attribute("r") == "5"
                            assert "8/8" in calculation.inner_text()
                            assert overall.text_content() == "8/8 accepted · 6/8 correct"
                            assert all(cases.nth(i).get_attribute(
                                "data-case-accepted") == "true" for i in range(8))
                            assert cases.nth(1).get_attribute("data-case-correct") == "false"
                            assert cases.nth(3).get_attribute("data-case-correct") == "true"
                            assert gap.text_content() == "GAP 0 pp"
                            assert rejected.text_content() == "0/8 rejected · accuracy N/A"
                            assert right.text_content() == (
                                "RIGHT 6 = 6 accepted + 0 rejected")
                            assert wrong.text_content() == (
                                "WRONG 2 = 2 accepted + 0 rejected")
                            assert ("拒答樣本正確率未定義" if zh else
                                    "rejected-only accuracy is undefined") in (
                                        plot.get_attribute("aria-label"))
                            assert ("未定義" if zh else "undefined") in (
                                calculation.inner_text())
                            assert (("0 個百分點" if zh else "0 percentage points")
                                    in plot.get_attribute("aria-label"))
                            assert plot.locator(
                                "rect[fill='#087e85']").get_attribute("width") == "415"
                            choices.nth(1).focus()
                            page.keyboard.press("Enter")
                            assert slider.input_value() == "40"
                            assert choices.nth(1).get_attribute("aria-pressed") == "true"
                            assert choices.nth(1).locator("rect").get_attribute("fill") == "#e3f0ef"
                            assert choices.nth(1).locator("rect").get_attribute("stroke") == "#193e69"
                            assert choices.nth(0).locator("rect").get_attribute("fill") == "#ffffff"
                            assert "5/8" in calculation.inner_text()
                            choices.nth(0).focus()
                            page.keyboard.press("Space")
                            assert slider.input_value() == "0"
                            assert choices.nth(0).locator("rect").get_attribute("fill") == "#e3f0ef"
                            assert choices.nth(0).locator("rect").get_attribute("stroke") == "#193e69"
                            choices.nth(1).click()
                            assert slider.input_value() == "40"
                            assert choices.nth(1).locator("rect").get_attribute("fill") == "#e3f0ef"
                            assert choices.nth(1).locator("rect").get_attribute("stroke") == "#193e69"
                            assert plot.get_attribute("data-active-stage") == "1"
                            assert gap.text_content() == "GAP 75 pp"
                            assert rejected.text_content() == "3/8 rejected · 1/3 correct · 2/3 wrong"
                            choices.nth(0).focus()
                            page.keyboard.press("ArrowRight")
                            assert slider.input_value() == "40"
                            assert choices.nth(1).evaluate("(e) => document.activeElement === e")
                            page.keyboard.press("Home")
                            assert slider.input_value() == "0"
                            page.keyboard.press("End")
                            assert slider.input_value() == "40"
                            page.keyboard.press("ArrowLeft")
                            assert slider.input_value() == "0"
                            page.keyboard.press("ArrowRight")
                            assert slider.input_value() == "40"
                            assert choices.nth(1).get_attribute("aria-pressed") == "true"
                            # Focusing an outcome while playback is running must
                            # freeze its acceptance decision and FLIP arithmetic.
                            host.get_by_role("button", name=play).click()
                            page.wait_for_timeout(140)
                            assert int(slider.input_value()) > 40
                            case_controls.nth(3).focus()
                            focused_position = slider.input_value()
                            assert host.get_by_role("button", name=play).count() == 1
                            assert detail.text_content() == "P4: RIGHT · REJECTED → +1 OUT"
                            page.wait_for_timeout(180)
                            assert slider.input_value() == focused_position, (
                                "focused inspection kept animating", zh, width)
                            assert plot.get_attribute("data-active-stage") == "1"
                            page.keyboard.press("Escape")
                            assert detail.text_content() == "✓ right · × wrong"
                            assert chip.get_attribute("visibility") == "hidden"
                            assert marker.get_attribute("visibility") == "hidden"
                            assert slider.input_value() == focused_position
                            # Restore the exact stage stop for shared checks.
                            choices.nth(1).click()
                            assert slider.input_value() == "40"
                        page.wait_for_timeout(180)
                        assert slider.input_value() == "40", (
                            "An obsolete Play command resumed playback", stem)
                        assert host.get_by_role("button", name=play).count() == 1
                        assert status.inner_text() == "", (
                            "Stale announcement after playback", stem, zh, width
                        )
                        # Live narration must change at stage boundaries, never
                        # on every requestAnimationFrame. A previous implementation
                        # issued dozens of redundant screen-reader announcements
                        # during 240 ms of visually smooth playback.
                        page.evaluate("""() => {
                          window.__liveStageMutations = 0;
                          const observer = new MutationObserver(records => {
                            window.__liveStageMutations += records.length;
                          });
                          document.querySelectorAll(
                            '.selective-motion-player .concept-motion-chapter-note, ' +
                            '.selective-motion-player .concept-motion-calculation'
                          ).forEach(node => observer.observe(node, {
                            childList: true, characterData: true, subtree: true
                          }));
                        }""")
                        # A fresh explicit Play remains operable.
                        host.get_by_role("button", name=play).click()
                        page.wait_for_timeout(240)
                        assert int(slider.input_value()) > 40
                        assert page.evaluate("window.__liveStageMutations") == 0, (
                            "aria-live rewritten within a constant stage", stem, zh, width
                        )
                        # A visibility change must stop playback at the current
                        # semantic stage, including on narrow layouts and both
                        # languages. Simulate a hidden tab deterministically.
                        page.evaluate("""() => {
                          Object.defineProperty(document, 'hidden',
                            {configurable:true, get:() => true});
                          document.dispatchEvent(new Event('visibilitychange'));
                        }""")
                        hidden_pause = slider.input_value()
                        assert host.get_by_role("button", name=play).count() == 1
                        page.wait_for_timeout(180)
                        assert slider.input_value() == hidden_pause, (
                            "hidden tab kept advancing", stem, zh, width)
                        page.evaluate("delete document.hidden")
                        page.wait_for_timeout(100)
                        assert slider.input_value() == hidden_pause, (
                            "playback resumed on return without user consent", stem)
                        # An explicit Play is the only way to resume, and the
                        # previous requestAnimationFrame timestamp is discarded.
                        host.get_by_role("button", name=play).click()
                        page.wait_for_timeout(180)
                        assert int(slider.input_value()) > int(hidden_pause)
                        host.get_by_role(
                            "button", name="暫停" if zh else "Pause").click()
                        paused = slider.input_value()
                        page.wait_for_timeout(180)
                        assert slider.input_value() == paused
                        # An actual step back must still announce the new stage
                        # and its independently updated arithmetic exactly once.
                        page.evaluate("window.__liveStageMutations = 0")
                        host.get_by_role(
                            "button", name="上一步" if zh else "Previous step"
                        ).click()
                        page.wait_for_timeout(90)
                        assert slider.input_value() == "0"
                        assert plot.get_attribute("data-active-stage") == "0"
                        if stem == "accuracy-selective-class-coverage":
                            assert ("接受 8/8" if zh else "Accepted 8/8") in calculation.inner_text()
                        if stem == "accuracy-selective-coverage":
                            assert plot.locator(
                                "circle[stroke='#dc743b']").get_attribute("cx") == "240"
                        else:
                            assert plot.locator(
                                "rect[fill='#087e85']").get_attribute("width") == "415"
                        assert page.evaluate("window.__liveStageMutations") == 2, (
                            "missing or duplicate chapter announcement", stem, zh, width
                        )
                        assert host.locator("img").is_hidden()
                        assert host.locator("img").evaluate(
                            "(img) => getComputedStyle(img).display === 'none'"), (
                            "Fallback still visible under inline display:block", stem, zh, width)

                        assert host.locator("svg.concept-motion-inline").is_visible()
                        assert not errors, errors
                        print("PASS", stem, "zh" if zh else "en", width)
                        ctx.close()
            # GitHub / disabled-JS rendering uses the independent static asset.
            ctx = browser.new_context(java_script_enabled=False)
            page = ctx.new_page()
            page.set_content(markup(CASES[0][0], False))
            assert page.locator("img").is_visible()
            assert page.locator("img").evaluate(
                "(e) => e.naturalWidth") > 0
            assert page.locator("svg.selective-linked-plot").count() == 0
            print("PASS no-JS GitHub fallback")
            ctx.close()
        finally:
            browser.close()


if __name__ == "__main__":
    run()
