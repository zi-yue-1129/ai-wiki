#!/usr/bin/env python3
"""Real Chromium regression for original bilingual RND/ICM timeline probes."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import re

ROOT = Path(__file__).resolve().parents[1]
PREVIEW = ROOT / "docs/assets/concept-animations/rnd-b-transfer-preview.svg"
JS = ROOT / "docs/javascripts/curiosity-labs.js"
CSS = ROOT / "docs/stylesheets/curiosity-labs.css"
OUT = ROOT / "artifacts/rnd-icm-motion"
OUT.mkdir(parents=True, exist_ok=True)

def choose(host, n):
    control = host.locator('input[data-timeline]')
    control.evaluate("(e,n) => {e.value=String(n);e.dispatchEvent(new Event('input',{bubbles:true}));}", n)

def run():
    # The no-script GitHub fallback is a real, self-contained SVG, not a mock.
    import xml.etree.ElementTree as ET
    root = ET.parse(PREVIEW).getroot()
    assert root.tag == "{http://www.w3.org/2000/svg}svg"
    assert root.get("viewBox") == "0 0 560 700"
    assert not any(node.tag.endswith("}animate") for node in root.iter())
    assert PREVIEW.stat().st_size < 50 * 1024
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for width in (320, 360, 720, 1024):
            context = browser.new_context(viewport={"width":width,"height":1100})
            page = context.new_page()
            html = ('<html><head><style>body{margin:0;padding:8px;font-family:Arial,sans-serif}'
                    + CSS.read_text() + '</style></head><body>'
                    + '<div data-curiosity-lab="rnd" data-locale="en">RND fallback</div>'
                    + '<div data-curiosity-lab="icm" data-locale="zh-TW">ICM fallback</div>'
                    + '</body></html>')
            page.set_content(html)
            page.add_script_tag(content=JS.read_text())
            assert page.locator("svg").count() == 2
            assert page.locator("button").count() == 12
            for kind, states in (("rnd", (0,2,3,4,6,7)), ("icm", (0,2,3,4,5))):
                host = page.locator('[data-curiosity-lab="' + kind + '"]')
                for state in states:
                    choose(host, state)
                    assert host.locator("svg").count() == 1
                    if kind == "icm":
                        assert "特徵空間示意" in host.locator("svg").get_attribute("aria-label")
                    else:
                        assert "schematic feature-space" in host.locator("svg").get_attribute("aria-label")
                    assert host.locator(".curiosity-lab-status").text_content().startswith(
                        "Step " if kind == "rnd" else "步驟 ")
                    (OUT / f"probe_{kind}_{width}_{state}.png").write_bytes(host.screenshot())
                if kind == "rnd":
                    choose(host, 0)
                    assert "19.10" in host.locator("svg").text_content()
                    choose(host, 3)
                    assert "0.03" in host.locator("svg").text_content()
                    choose(host, 4)
                    assert "Obs B" in host.locator("svg").text_content()
                    assert "19.13" in host.locator("svg").text_content()
                    transfer = host.locator("input[data-transfer]")
                    assert transfer.count() == 1 and host.locator(".curiosity-lab-transfer").is_visible()
                    for percent, expected in ((0,19125),(50,4781.25),(100,0)):
                        transfer.evaluate(
                            "(e,v) => {e.value=String(v);e.dispatchEvent(new Event('input',{bubbles:true}));}", percent
                        )
                        predictor = host.locator('svg circle[fill="#e19748"]')
                        target = host.locator('svg circle[fill="#27926e"]')
                        px,py = float(predictor.get_attribute("cx")),float(predictor.get_attribute("cy"))
                        tx,ty = float(target.get_attribute("cx")),float(target.get_attribute("cy"))
                        squared = (tx-px)**2 + (ty-py)**2
                        assert abs(squared-expected) < 0.01
                        bar = float(host.locator('svg rect[fill="#d28a3e"]').get_attribute("width"))
                        assert abs(bar - 244*squared/21000) < 0.02
                        assert host.locator('svg circle[fill="none"][stroke="#e19748"]').count() == (1 if percent==100 else 0)
                        metrics = host.locator(".curiosity-lab-transfer .curiosity-lab-metrics").text_content()
                        assert metrics.endswith({0:"19.13",50:"4.78",100:"0.00"}[percent])
                        (OUT / f"rnd_transfer_{width}_{percent}.png").write_bytes(host.screenshot())
                    choose(host,3)
                    assert not host.locator(".curiosity-lab-transfer").is_visible()
                    assert host.locator('svg circle[fill="#e19748"]').get_attribute("cx") == "165"
                    choose(host,4)
                    transfer.focus()
                    page.keyboard.press("ArrowLeft")
                    assert transfer.input_value() == "75"
                    host.get_by_role("button",name="Reset transfer").click()
                    assert transfer.input_value() == "0"
                else:
                    # Predictable target stays fixed while the learner updates its
                    # deterministic forecast; the bar must track squared distance.
                    for index,forecast,formatted in (
                        (0,(260,165),"3.73"),(1,(289,145),"0.67"),
                        (2,(310,130),"0.00")):
                        choose(host,index)
                        predictor=host.locator('svg circle[fill="#e19748"]')
                        actual=host.locator('svg circle[fill="#27926e"]')
                        px,py=int(predictor.get_attribute("cx")),int(predictor.get_attribute("cy"))
                        tx,ty=int(actual.get_attribute("cx")),int(actual.get_attribute("cy"))
                        assert (px,py)==forecast and (tx,ty)==(310,130)
                        squared=(px-tx)**2+(py-ty)**2
                        actual_width=float(host.locator('svg rect[fill="#d28a3e"]').get_attribute("width"))
                        assert abs(actual_width-244*squared/16000)<0.02
                        # Deterministic next features have conditional variance zero;
                        # the violet expected-error tick must meet the sampled-error
                        # bar, including *before* the predictor is fitted.
                        tick = host.locator('svg path[stroke="#775fb0"]').first.get_attribute("d")
                        tick_x = float(tick.split(" ")[0][1:])
                        assert abs(tick_x-(128+actual_width)) < 0.02
                        expected_value = host.locator('svg text[fill="#7357a2"]').last.text_content()
                        assert expected_value == formatted, (index, expected_value, formatted)
                        content=host.locator("svg").text_content()
                        assert formatted in content and "Expected" in content, content
                    for index,val in ((3,"3.87"),(4,"1.94"),(5,"3.25")):
                        choose(host,index)
                        content = host.locator("svg").text_content()
                        assert "3.02" in content and val in content, content
            # Conditional-mean probe: bias moves the hypothetical forecast, not
            # sampled outcomes. Expected squared error = variance + squared bias.
            icm = page.locator('[data-curiosity-lab="icm"]')
            choose(icm, 3)
            bias_slider = icm.locator('input[data-bias]')
            assert bias_slider.count() == 1
            assert "3.02" in icm.locator(".curiosity-lab-bias:not(.curiosity-lab-transfer):not(.curiosity-lab-skew) .curiosity-lab-metrics").text_content()
            assert icm.locator('input[data-timeline]').count() == 1
            bias_slider.evaluate(
                "(e) => {e.value='40';e.dispatchEvent(new Event('input',{bubbles:true}));}"
            )
            assert icm.locator('svg circle[fill="#e19748"]').get_attribute("cx") == "350"
            width_bar = float(icm.locator('svg rect[fill="#d28a3e"]').get_attribute("width"))
            assert abs(width_bar - 244*1066/16000) < .02
            tick = icm.locator('svg path[stroke="#775fb0"]').first.get_attribute("d")
            assert abs(float(tick.split(" ")[0][1:]) - (128+244*(3017.3333333333+1600)/16000)) < .05
            numbers = icm.locator(".curiosity-lab-bias:not(.curiosity-lab-transfer):not(.curiosity-lab-skew) .curiosity-lab-metrics").text_content()
            assert all(v in numbers for v in ("4.62", "1.60", "3.02"))
            (OUT / f"probe_icm_bias_{width}_p40.png").write_bytes(icm.screenshot())
            # Reweight three stochastic outcomes without moving the possible outcomes.
            # Weighted conditional mean changes, while the mean predictor remains
            # optimal at zero additional bias; a selected sample can get larger error.
            bias_slider.evaluate(
                "(e) => {e.value='0';e.dispatchEvent(new Event('input',{bubbles:true}));}"
            )
            skew_slider = icm.locator('input[data-skew]')
            assert skew_slider.count() == 1 and icm.locator(".curiosity-lab-skew").is_visible()
            for skew_value, mean_x, mean_y, expected_var, p_text in (
                (-60,288,132.8,2402.293333333333,"13.3% / 33.3% / 53.3%"),
                (0,310,130,3017.333333333333,"33.3% / 33.3% / 33.3%"),
                (60,332,127.2,2648.693333333333,"53.3% / 33.3% / 13.3%")
            ):
                skew_slider.evaluate(
                    "(e,v) => {e.value=String(v);e.dispatchEvent(new Event('input',{bubbles:true}));}", skew_value
                )
                mean_ring=icm.locator('svg circle[stroke="#775fb0"]')
                assert abs(float(mean_ring.get_attribute("cx"))-mean_x)<.02
                assert abs(float(mean_ring.get_attribute("cy"))-mean_y)<.02
                predictor=icm.locator('svg circle[fill="#e19748"]')
                assert abs(float(predictor.get_attribute("cx"))-mean_x)<.02
                assert abs(float(predictor.get_attribute("cy"))-mean_y)<.02
                expected_tick=icm.locator('svg path[stroke="#775fb0"]').first.get_attribute("d")
                tick_position=float(expected_tick.split(" ")[0][1:])
                assert abs(tick_position-(128+244*expected_var/16000))<.05
                # A common axis allows either decomposition to produce the same expectation.
                vbar=icm.locator("svg rect[data-mse-variance]")
                bbar=icm.locator("svg rect[data-mse-bias]")
                assert abs(float(vbar.get_attribute("width"))-344*expected_var/6000)<0.03
                assert abs(float(bbar.get_attribute("width")))<0.01
                vector=icm.locator("svg line[data-bias-vector]")
                assert abs(float(vector.get_attribute("x1"))-mean_x)<0.02
                assert abs(float(vector.get_attribute("y1"))-mean_y)<0.02
                assert abs(float(vector.get_attribute("x2"))-mean_x)<0.02
                assert icm.locator("svg").get_attribute("viewBox")=="0 0 410 505"
                assert p_text in icm.locator(".curiosity-lab-skew .curiosity-lab-metrics").text_content()
                # The live coloured strip is a probability-weighted sum of
                # *three separate sample gaps*, not three unweighted errors.
                segments = icm.locator('svg rect[data-contribution]')
                assert segments.count() == 3
                # The same outcome colour identifies the gap and its weighted term.
                palette = ("#267f9f", "#319d91", "#8672b4")
                for component in range(3):
                    ray = icm.locator(f'svg line[data-outcome-ray="{component+1}"]')
                    assert ray.count() == 1
                    assert ray.get_attribute("stroke") == palette[component]
                    assert segments.nth(component).get_attribute("fill") == palette[component]
                    assert abs(float(ray.get_attribute("x2"))-mean_x) < .02
                    assert abs(float(ray.get_attribute("y2"))-mean_y) < .02
                scaled_total = sum(float(segments.nth(i).get_attribute("width")) for i in range(3))
                assert abs(scaled_total - 344 * expected_var / 6000) < 0.05
                for i in range(3):
                    assert segments.nth(i).get_attribute("data-contribution") == str(i + 1)
                assert "Σ " + format(expected_var / 1000, ".3f") in icm.locator("svg").text_content()
                (OUT / f"icm_weighted_{width}_{skew_value}.png").write_bytes(icm.screenshot())
            # Combining hypothetical probability reweighting and prediction bias:
            # the expected squared error gains exactly bias**2.
            bias_slider.evaluate(
                "(e) => {e.value='40';e.dispatchEvent(new Event('input',{bubbles:true}));}"
            )
            assert abs(float(icm.locator('svg circle[fill="#e19748"]').get_attribute('cx'))-372)<.02
            assert "4.25" in icm.locator(".curiosity-lab-bias:not(.curiosity-lab-transfer):not(.curiosity-lab-skew) .curiosity-lab-metrics").text_content()
            # Reweighting and shifting the prediction must recompute *each*
            # contribution, not merely move the expected-error marker.
            combined = icm.locator('svg rect[data-contribution]')
            assert abs(sum(float(combined.nth(i).get_attribute("width")) for i in range(3))
                       - 344 * (2648.693333333333 + 1600) / 6000) < 0.05
            variance_bar=icm.locator("svg rect[data-mse-variance]")
            bias_bar=icm.locator("svg rect[data-mse-bias]")
            assert abs(float(variance_bar.get_attribute("width"))-344*2648.693333333333/6000)<0.03
            assert abs(float(bias_bar.get_attribute("width"))-344*1600/6000)<0.03
            vector=icm.locator("svg line[data-bias-vector]")
            assert abs(float(vector.get_attribute("x1"))-332)<0.02
            assert abs(float(vector.get_attribute("x2"))-372)<0.02
            skew_slider.evaluate("(e) => {e.value='-60';e.dispatchEvent(new Event('input',{bubbles:true}));}")
            bias_slider.evaluate("(e) => {e.value='-40';e.dispatchEvent(new Event('input',{bubbles:true}));}")
            sample_width=float(icm.locator('svg rect[fill="#d28a3e"]').get_attribute("width"))
            assert abs(sample_width-244*14700.24/16000)<0.03 and sample_width<244
            bias_slider.evaluate("(e) => {e.value='40';e.dispatchEvent(new Event('input',{bubbles:true}));}")
            icm.get_by_role("button",name="恢復等機率").click()
            assert skew_slider.input_value()=="0"
            assert "4.62" in icm.locator(".curiosity-lab-bias:not(.curiosity-lab-transfer):not(.curiosity-lab-skew) .curiosity-lab-metrics").text_content()
            # Arrow-key slider adjustment remains available without pointer input.
            skew_slider.focus()
            page.keyboard.press("ArrowLeft")
            assert skew_slider.input_value()=="-20"
            icm.get_by_role("button",name="恢復等機率").click()
            # A keyboard nudge and the accessible reset button must recompute
            # the prediction and expected error, without touching the sample.
            bias_slider.focus()
            page.keyboard.press("ArrowLeft")
            assert bias_slider.input_value() == "30"
            icm.get_by_role("button", name="回到條件平均值").click()
            assert bias_slider.input_value() == "0"
            assert "3.02" in icm.locator(".curiosity-lab-bias:not(.curiosity-lab-transfer):not(.curiosity-lab-skew) .curiosity-lab-metrics").text_content()
            # Real mouse and keyboard actions, not just DOM existence.
            host=page.locator('[data-curiosity-lab="rnd"]')
            choose(host,2)
            host.get_by_role("button", name="Next step").focus()
            page.keyboard.press("Enter")
            assert "Step 4/8" in host.locator(".curiosity-lab-status").text_content()
            host.get_by_role("button", name="Play").click()
            assert host.get_by_role("button", name="Pause").count() == 1
            host.get_by_role("button", name="Pause").click()
            assert host.get_by_role("button", name="Play").count() == 1
            context.close()
        context = browser.new_context(viewport={"width":360,"height":1000},
                                      reduced_motion="reduce")
        page=context.new_page()
        page.set_content('<div data-curiosity-lab="rnd" data-locale="en"></div>'
                         '<div data-curiosity-lab="icm" data-locale="en"></div>')
        page.add_script_tag(content=JS.read_text())
        assert page.get_by_role("button", name="Play").count() == 2
        for button in page.get_by_role("button", name="Play").all():
            assert button.is_disabled()
        rnd=page.locator('[data-curiosity-lab="rnd"]')
        choose(rnd,4)
        assert "Obs B" in rnd.locator("svg").text_content()
        rnd.locator("input[data-transfer]").evaluate(
            "(e) => {e.value='100';e.dispatchEvent(new Event('input',{bubbles:true}));}"
        )
        assert "0.00" in rnd.locator(".curiosity-lab-transfer .curiosity-lab-metrics").text_content()
        icm = page.locator('[data-curiosity-lab="icm"]')
        choose(icm,3)
        icm.locator('input[data-bias]').evaluate(
            "(e) => {e.value='-40';e.dispatchEvent(new Event('input',{bubbles:true}));}"
        )
        assert "4.62" in icm.locator(".curiosity-lab-bias:not(.curiosity-lab-transfer):not(.curiosity-lab-skew) .curiosity-lab-metrics").text_content()
        context.close()
        browser.close()
    print("PASS curiosity probes: responsive renders, arithmetic, keyboard, timeline, reduced motion")

if __name__ == "__main__":
    run()
