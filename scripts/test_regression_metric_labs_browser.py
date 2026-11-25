"""Render the actual shared regression metric labs in Chromium and check math/controls."""
from pathlib import Path
from datetime import datetime, timedelta, timezone
from math import isclose
import os
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
JS = (ROOT / "docs/javascripts/regression-metric-labs.js").read_text(encoding="utf-8")
CSS = (ROOT / "docs/stylesheets/regression-metric-labs.css").read_text(encoding="utf-8")
OUT = ROOT / "artifacts/regression-metric-labs"
OUT.mkdir(parents=True, exist_ok=True)


def run():
    tested = 0
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, executable_path=os.environ.get("AIWIKI_CHROMIUM_PATH") or None)
        for language in ("en", "zh"):
            for width in (320, 360, 720, 1024):
                for motion in ("no-preference", "reduce"):
                    page = browser.new_page(
                        viewport={"width": width, "height": 950},
                        reduced_motion=motion,
                    )
                    errors = []
                    page.on("pageerror", lambda err: errors.append(str(err)))
                    html = f"""<!doctype html><html><head><meta charset='utf-8'>
<meta name='viewport' content='width=device-width,initial-scale=1'>
<style>{CSS}</style><style>body{{margin:0;padding:8px;font-family:Arial,sans-serif}}
main{{max-width:1000px;margin:auto}}</style></head><body><main>
<div data-regression-lab='outlier' data-lang='{language}'></div>
<div data-regression-lab='r2' data-lang='{language}'></div>
</main><script>{JS}</script></body></html>"""
                    # Freeze wall time before the real page starts scheduling frames.
                    # Only run_for() advances playback; locator/keyboard latency must
                    # not change the direction or the slider's quantized value.
                    epoch = datetime(2026, 1, 1, tzinfo=timezone.utc)
                    page.clock.install(time=epoch)
                    page.clock.pause_at(epoch + timedelta(seconds=1))
                    page.set_content(html)
                    assert page.locator(".rml-panel").count() == 2
                    assert page.locator("svg[viewBox='0 0 680 390']").count() == 2
                    assert page.locator("svg[aria-label]").count() == 2
                    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth"), (language, width)
                    assert not errors, errors
                    outlier = page.locator('[data-regression-lab="outlier"]')
                    outlier.locator('input[type="range"]').fill("6")
                    assert "MAE=(4+d)/5=2.000" in outlier.locator(".rml-detail").inner_text()
                    assert "RMSE=√((4+d²)/5)=2.828" in outlier.locator(".rml-detail").inner_text()
                    squared_piece = outlier.locator('svg rect[y="317"][fill="#f4ad70"]')
                    assert isclose(float(squared_piece.get_attribute('width')), 270.0, abs_tol=0.01)
                    assert outlier.locator('svg text').filter(has_text='40.000').count() == 1
                    squared = page.locator('[data-regression-lab="r2"]')
                    squared.locator('input[type="range"]').fill("1.5")
                    assert "RSS=11.250" in squared.locator(".rml-detail").inner_text()
                    assert "R²=1−RSS/TSS=-1.250" in squared.locator(".rml-detail").inner_text()
                    rss_bar = squared.locator('svg rect[y="345"][fill="#f3ad75"]')
                    assert isclose(float(rss_bar.get_attribute('width')), 350.0, abs_tol=0.01)
                    squared.locator('input[type="range"]').fill("1")
                    assert isclose(float(rss_bar.get_attribute('width')), 350 * 5 / 11.25, abs_tol=0.01)
                    assert "R²=1−RSS/TSS=0.000" in squared.locator(".rml-detail").inner_text()
                    if motion == "reduce":
                        assert outlier.locator('.rml-button[aria-label="'+("播放" if language=="zh" else "Play")+'"]').is_disabled()
                    else:
                        outlier.locator('.rml-button[aria-label="'+("重設" if language=="zh" else "Reset")+'"]').click()
                        outlier.locator('.rml-button[aria-label="'+("下一步" if language=="zh" else "Next")+'"]').click()
                        assert "d=1.100" in outlier.locator(".rml-detail").inner_text()
                    if motion == "no-preference":
                        # Use the real Chromium controls and deterministic animation time.
                        for lab, minimum, step in ((outlier, 1.0, 0.1), (squared, 0.0, 0.05)):
                            reset_label = "重設" if language == "zh" else "Reset"
                            play_label = "播放" if language == "zh" else "Play"
                            pause_label = "暫停" if language == "zh" else "Pause"
                            lab.get_by_role("button", name=reset_label, exact=True).click()
                            slider = lab.locator('input[type="range"]')
                            play = lab.get_by_role("button", name=play_label, exact=True)
                            play.focus()
                            page.keyboard.press("Enter")
                            page.clock.run_for(1200)
                            lab.get_by_role("button", name=pause_label, exact=True).focus()
                            page.keyboard.press("Space")
                            paused = float(slider.input_value())
                            shown = float(lab.locator(".rml-number").inner_text())
                            assert paused > minimum, ("slider did not follow playback", language, width)
                            assert abs(paused - shown) <= step / 2 + 0.001
                            frozen = lab.locator(".rml-detail").inner_text()
                            page.clock.run_for(500)
                            assert lab.locator(".rml-detail").inner_text() == frozen
                            assert float(slider.input_value()) == paused
                            slider.focus()
                            page.keyboard.press("ArrowRight")
                            assert isclose(float(slider.input_value()), paused + step, abs_tol=0.001)
                            assert isclose(float(lab.locator(".rml-number").inner_text()), paused + step, abs_tol=0.001)
                            lab.get_by_role("button", name=play_label, exact=True).focus()
                            page.keyboard.press("Space")
                            assert lab.get_by_role("button", name=pause_label, exact=True).count() == 1, (
                                "resume did not enter playing state", language, width, minimum
                            )
                            before_resume = float(slider.input_value())
                            page.clock.run_for(500)
                            resumed = float(slider.input_value())
                            assert resumed > before_resume, (
                                "slider did not advance after resume", language, width,
                                minimum, before_resume, resumed, page.evaluate("document.visibilityState")
                            )
                            lab.get_by_role("button", name=pause_label, exact=True).focus()
                            page.keyboard.press("Enter")
                    assert len(page.locator("svg text").all_inner_texts()) >= 10
                    assert not errors, errors
                    if width in (320, 1024) and motion == "no-preference":
                        page.screenshot(path=str(OUT / f"{language}-{width}.png"),full_page=True)
                    tested += 1
                    page.close()
        browser.close()
    print(f"Regression metric numerical and responsive Chromium scenarios passed: {tested}/16")


if __name__ == "__main__":
    run()