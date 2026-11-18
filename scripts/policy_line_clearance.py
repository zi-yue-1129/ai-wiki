"""Additional text/credit-line clearance; never relax the original glyph contract."""
import math
import re
NS = '{http://www.w3.org/2000/svg}'
MIN_CLEARANCE = 3.0

def check_return_credit_clearance(text_box, line_box, stroke_width):
    """Use actual native getBBox boxes (or conservative source envelope).

    The entire horizontal stroke is checked, even while partially dashed out,
    so every intermediate dash-offset frame remains safe.
    """
    for box in (text_box, line_box):
        assert set(box) == {'x', 'y', 'w', 'h'}, box
        assert all(type(box[k]) in (int, float) and math.isfinite(box[k]) for k in box), box
        assert box['w'] > 0 and box['h'] >= 0, box
    assert type(stroke_width) in (int, float) and math.isfinite(stroke_width) and stroke_width > 0
    assert line_box['h'] == 0, 'Expected the reviewed horizontal reward-to-go line'
    assert text_box['h'] > 0
    assert min(text_box['x'] + text_box['w'], line_box['x'] + line_box['w']) > max(text_box['x'], line_box['x']), 'Label must remain associated with the credit line'
    top = line_box['y'] - stroke_width / 2
    bottom = line_box['y'] + stroke_width / 2
    gap = max(top - (text_box['y'] + text_box['h']), text_box['y'] - bottom)
    assert gap >= MIN_CLEARANCE, ('Reward-to-go glyph/line clearance', gap, MIN_CLEARANCE)
    return gap

def check_return_credit_source(svg):
    labels = [e for e in svg.iter(NS+'text') if ''.join(e.itertext()) == 'Reward-to-go']
    lines = [e for e in svg.iter(NS+'path') if e.get('stroke') == '#d46a3a']
    assert len(labels) == len(lines) == 1
    label, line = labels[0], lines[0]
    assert label in list(svg) and line in list(svg), 'Reviewed glyph/line must be direct SVG children'
    assert not label.get('transform') and not line.get('transform'), 'Transformed geometry needs explicit review'
    m = re.fullmatch(r'M([\d.]+) ([\d.]+) H([\d.]+)', line.get('d', ''))
    assert m, 'Credit path geometry must be explicitly reviewed'
    x1, y, x2 = map(float, m.groups())
    # Only dash offset is animated. Its visible subset cannot exceed this
    # full path envelope; source checks cover the whole continuous timeline.
    assert not list(label), 'Unexpected animated label geometry'
    assert all(a.get('attributeName') == 'stroke-dashoffset' for a in line)
    assert label.get('text-anchor') == 'middle'
    size = float(label.get('font-size'))
    # 1em ascent + .25em descent is conservative for the reviewed font.
    width = len('Reward-to-go') * size
    text_box = dict(x=float(label.get('x')) - width/2, y=float(label.get('y')) - size,
                    w=width, h=1.25*size)
    line_box = dict(x=min(x1,x2), y=y, w=abs(x1-x2), h=0.)
    return check_return_credit_clearance(text_box, line_box, float(line.get('stroke-width')))
