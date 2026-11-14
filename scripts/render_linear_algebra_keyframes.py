#!/usr/bin/env python3
"""Render deterministic desktop SVG keyframes, not built-page UI coverage.

CI: python scripts/render_linear_algebra_keyframes.py
No-browser plan check: python scripts/render_linear_algebra_keyframes.py --check-plan
PNG/JSON evidence is written to artifacts/linear-algebra-motion/. Review pixels
alongside the assertions; this does not test mobile, reduced motion or controls.
"""
from __future__ import annotations

import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import math
from pathlib import Path
from threading import Thread

from test_linear_algebra_motion_semantics import (
    ASSETS, by_id, expected_iterates, motion, multiply, rotation, sample, svg,
)

OUT = Path(__file__).resolve().parents[1] / "artifacts/linear-algebra-motion"


def cases():
    normalized, applied = expected_iterates()
    power = []
    for k, seconds in enumerate((.3, 2.2, 4.2, 6.2, 8.2, 10.6)):
        power.append({"name": f"power-x{k}", "stem": "power-iteration-convergence",
                      "seconds": seconds, "vector": normalized[k], "row": k,
                      "highlight": 1, "phase": "normalized"})
    for name, seconds, end in (("apply", .9, applied[0]),
                                ("normalize", 1.5, normalized[1])):
        start = normalized[0] if name == "apply" else applied[0]
        power.append({"name": "power-" + name, "stem": "power-iteration-convergence",
                      "seconds": seconds, "vector": tuple((a + b) / 2 for a, b in zip(start, end)),
                      "row": 0, "highlight": 0, "phase": name})
    power.sort(key=lambda case: case["seconds"])
    # SVG y points down: U=R(-30), V-transpose=R(+35) in screen coordinates.
    stages = (
        ("initial", 0, 0, (1, 1), 0),
        ("rotate-vt", 1.5, 0, (1, 1), 17.5),
        ("vt-complete", 3, 0, (1, 1), 35),
        ("stretch", 4.5, 0, (1 + 1.5 / 2.88, 1 - .35 * 1.5 / 2.88), 35),
        ("sigma-complete", 6.2, 0, (2, .65), 35),
        ("rotate-u", 8.8, -30 / 2.52, (2, .65), 35),
        ("complete", 11, -30, (2, .65), 35),
    )
    return power + [{"name": "svd-" + name, "stem": "svd-unit-circle",
                     "seconds": seconds, "transforms": (u, scale, vt)}
                    for name, seconds, u, scale, vt in stages]


def close(actual, expected, tolerance=2e-4):
    assert len(actual) == len(expected), (actual, expected)
    assert all(abs(a - b) <= tolerance for a, b in zip(actual, expected)), (actual, expected)


def matrix_values(matrix):
    return [matrix[0][0], matrix[1][0], matrix[0][1], matrix[1][1], 0, 0]


def check_plan():
    """Validate chosen times/expectations against source without opening a browser."""
    assert len({case["name"] for case in cases()}) == 15
    for case in cases():
        root = svg(case["stem"])
        if "vector" in case:
            arrow, row = by_id(root, "power-vector"), by_id(root, "active-error-row")
            x, y = [sample(motion(arrow, axis), case["seconds"])[0] for axis in ("x2", "y2")]
            close(((x - 180) / 54, (195 - y) / 54), case["vector"])
            close(sample(motion(row, "y"), case["seconds"]), [87 + 36 * case["row"]])
            close(sample(motion(row, "opacity"), case["seconds"]), [case["highlight"]])
            close(sample(motion(by_id(root, "phase-" + case["phase"]), "opacity"), case["seconds"]), [1])
        else:
            animations = [e for e in root.iter() if e.tag.endswith("}animateTransform")]
            u, scale, vt = case["transforms"]
            for animation, expected in zip(animations, ([u], scale, [vt])):
                close(sample(animation, case["seconds"]), expected)
    print("PASS: 15 keyframe times and expected geometry match the numerical source contract; no browser run")


OBSERVE = """() => {
  const root = document.documentElement;
  const matrix = m => [m.a, m.b, m.c, m.d, m.e, m.f];
  const result = {time:root.getCurrentTime(), paused:root.animationsPaused(),
                  bounds:{width:root.getBoundingClientRect().width,height:root.getBoundingClientRect().height}};
  const arrow = document.getElementById('power-vector');
  if (arrow) {
    const row = document.getElementById('active-error-row');
    result.arrow = [arrow.x2.animVal.value, arrow.y2.animVal.value];
    result.rowY = row.y.animVal.value;
    result.highlight = Number(getComputedStyle(row).opacity);
    result.phases = Object.fromEntries(['normalized','apply','normalize'].map(name =>
      [name, Number(getComputedStyle(document.getElementById('phase-'+name)).opacity)]));
    result.bars = Array.from({length:6}, (_,k) => ({
      width:document.getElementById('error-bar-'+k).width.animVal.value,
      label:document.getElementById('error-label-'+k).textContent.trim()}));
  } else {
    const origin = root.querySelector('g.animated');
    const u = [...origin.children].find(e => e.localName === 'g');
    const sigma = [...u.children].find(e => e.localName === 'g');
    const vt = [...sigma.children].find(e => e.localName === 'g');
    result.transforms = [u,sigma,vt].map(node =>
      matrix(node.parentNode.getCTM().inverse().multiply(node.getCTM())));
    result.composite = matrix(origin.getCTM().inverse().multiply(vt.getCTM()));
  }
  return result;
}"""


def verify_observed(case, observed):
    assert observed["paused"]
    close([observed["time"]], [case["seconds"]])
    close([observed["bounds"]["width"], observed["bounds"]["height"]], [640, 360])
    if "vector" in case:
        x, y = case["vector"]
        close(observed["arrow"], [180 + 54 * x, 195 - 54 * y])
        close([observed["rowY"], observed["highlight"]], [87 + 36 * case["row"], case["highlight"]])
        assert observed["phases"] == {name: int(name == case["phase"])
                                      for name in ("normalized", "apply", "normalize")}
        for k, bar in enumerate(observed["bars"]):
            error = math.degrees(math.atan(math.tan(math.radians(72)) / 3 ** k))
            close([bar["width"]], [136 * error / 72])
            assert bar["label"] == f"{error:.1f}°"
    else:
        u, scale, vt = case["transforms"]
        matrices = (rotation(u), ((scale[0], 0), (0, scale[1])), rotation(vt))
        for actual, expected in zip(observed["transforms"], matrices):
            close(actual, matrix_values(expected))
        close(observed["composite"], matrix_values(multiply(multiply(*matrices[:2]), matrices[2])))


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


def render():
    from playwright.sync_api import sync_playwright

    OUT.mkdir(parents=True, exist_ok=True)
    report = {"scope": "single-desktop direct-SVG deterministic keyframes; excludes built-page UI, mobile, reduced motion and controls",
              "status": "running", "cases": []}
    server = ThreadingHTTPServer(("127.0.0.1", 0), partial(QuietHandler, directory=str(ASSETS)))
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True, args=["--no-sandbox"])
            report["browser_version"] = browser.version
            page = browser.new_page(viewport={"width": 640, "height": 360},
                                    reduced_motion="no-preference", device_scale_factor=1)
            errors = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            current_stem = None
            for case in cases():
                if case["stem"] != current_stem:
                    response = page.goto(f"http://127.0.0.1:{server.server_port}/{case['stem']}-motion.svg")
                    assert response and response.ok, case["stem"]
                    page.wait_for_selector("svg")
                    page.evaluate("async () => { await document.fonts.ready; }")
                    current_stem = case["stem"]
                page.evaluate("""async seconds => {
                  const svg = document.documentElement;
                  svg.pauseAnimations(); svg.setCurrentTime(seconds);
                  await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
                }""", case["seconds"])
                observed = page.evaluate(OBSERVE)
                filename = case["name"] + ".png"
                page.locator("svg").screenshot(path=str(OUT / filename))
                report["cases"].append({"expected": case, "observed": observed, "screenshot": filename})
                verify_observed(case, observed)
                assert not errors, errors
            browser.close()
        report["status"] = "passed"
    except Exception as error:
        report["status"] = "failed"
        report["error"] = repr(error)
        raise
    finally:
        server.shutdown()
        server.server_close()
        thread.join()
        (OUT / "keyframes.json").write_text(json.dumps(report, indent=2) + "\n")
    print("PASS: 15 deterministic desktop SVG screenshots and DOM assertions; built-page UI/mobile/reduced-motion not covered")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-plan", action="store_true", help="Check samples without browser/server startup")
    args = parser.parse_args()
    check_plan()
    if not args.check_plan:
        render()
