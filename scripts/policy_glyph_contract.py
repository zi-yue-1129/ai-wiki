"""Pure producer/receipt glyph contract; original 760x400 bounds and 3px overlap tolerance."""
import math
# Reviewed SVG DOM text order, fixed literals. Never derive expected labels from a receipt.
EXPECTED_LABELS = {'reinforce-return-credit:motion': ['REINFORCE', 'Return-weighted policy gradient', 'Sampled episode', 'a0', 't=0', 'a1', 't=1', 'a2', 't=2', 'Reward', '+4', 'Credit assignment', 'γ = 0.8   ·   b = 2', 'G0 = 2.56', 'A0 = +0.56', 'G1 = 3.2', 'A1 = +1.20', 'G2 = 4.0', 'A2 = +2.00', 'A = G − baseline   ·   illustrative values', 'Reward-to-go'], 'reinforce-return-credit:still': ['REINFORCE', 'Return-weighted policy gradient', 'Sampled episode', 'a0', 't=0', 'a1', 't=1', 'a2', 't=2', 'Reward', '+4', 'Credit assignment', 'γ = 0.8   ·   b = 2', 'G0 = 2.56', 'A0 = +0.56', 'G1 = 3.2', 'A1 = +1.20', 'G2 = 4.0', 'A2 = +2.00', 'A = G − baseline   ·   illustrative values', 'Reward-to-go'], 'grpo-group-advantages:motion': ['GRPO', 'Within-group reward normalisation', 'One prompt  ·  four sampled outputs', 'r = 1', 'o1', 'r = 2', 'o2', 'r = 4', 'o3', 'r = 5', 'o4', 'mean = 3', 'Normalised advantages', 'σ = √2.5', '-1.26', '-0.63', '+0.63', '+1.26', 'A = (r − group mean) / group std   ·   illustrative values'], 'grpo-group-advantages:still': ['GRPO', 'Within-group reward normalisation', 'One prompt  ·  four sampled outputs', 'r = 1', 'o1', 'r = 2', 'o2', 'r = 4', 'o3', 'r = 5', 'o4', 'mean = 3', 'Normalised advantages', 'σ = √2.5', '-1.26', '-0.63', '+0.63', '+1.26', 'A = (r − group mean) / group std   ·   illustrative values']}
TIMES = (0, 2, 4, 6, 9, 11)

def number(value):
    try:
        return type(value) in (int, float) and math.isfinite(value)
    except OverflowError:
        return False

def check_boxes(boxes, stem, kind, t):
    assert type(boxes) is list and boxes, (stem, kind, t, "missing boxes")
    for b in boxes:
        assert type(b) is dict and set(b) == {"label", "x", "y", "w", "h"}, b
        assert type(b["label"]) is str and b["label"].strip(), b
        assert all(number(b[k]) for k in ("x", "y", "w", "h")), b
        assert b["w"] >= 0 and b["h"] >= 0, b
        assert b["x"] >= -2 and b["y"] >= -2, (stem, kind, t, b)
        assert b["x"] + b["w"] <= 762 and b["y"] + b["h"] <= 402, (stem, kind, t, b)
    for i, a in enumerate(boxes):
        for b in boxes[i+1:]:
            dx = max(0, min(a["x"]+a["w"],b["x"]+b["w"])-max(a["x"],b["x"]))
            dy = max(0, min(a["y"]+a["h"],b["y"]+b["h"])-max(a["y"],b["y"]))
            assert dx <= 3 or dy <= 3, (stem, kind, t, a["label"], b["label"])

def validate_glyph_sample(sample, stem, kind, expected_time):
    assert type(sample) is dict and set(sample) == {"time", "canvas", "boxes"}, sample
    assert stem+":"+kind in EXPECTED_LABELS, (stem, kind)
    assert number(sample["time"]) and number(expected_time), sample
    assert expected_time in (TIMES if kind == "motion" else (0,)), expected_time
    assert sample["time"] == expected_time, sample
    canvas = sample["canvas"]
    assert type(canvas) is list and len(canvas) == 4 and all(number(x) for x in canvas), canvas
    assert canvas == [0, 0, 760, 400], canvas
    check_boxes(sample["boxes"], stem, kind, expected_time)
    assert [b["label"] for b in sample["boxes"]] == EXPECTED_LABELS[stem+":"+kind], "Missing, extra or changed glyphs"
