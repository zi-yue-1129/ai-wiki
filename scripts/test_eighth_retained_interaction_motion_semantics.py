#!/usr/bin/env python3
"""AST source contracts only; native browser execution remains separately required."""
import ast
from collections import Counter
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {'scripts/test_norm_seq_labs_browser.py': ["page.keyboard.press('ArrowRight')", "assert scroller.evaluate('(el)=>el.scrollLeft') > 0", "page.keyboard.press('End')", "assert scroller.evaluate('(e)=>document.activeElement===e')", 'assert scroller.evaluate(\'(e)=>[e.clientWidth,e.scrollWidth,e.querySelector("svg").getBoundingClientRect().width]\') == end_before', "assert seq.locator('input[type=range]').first.input_value() == end_step", 'end_control.scroll_into_view_if_needed()', "assert end_control.evaluate('(e)=>document.activeElement===e')", 'assert end_control.is_visible() and end_control.is_enabled()', "assert end_bounds and 0 <= end_bounds['x'] and (end_bounds['x'] + end_bounds['width'] <= width + 1)", "assert 0 <= end_bounds['y'] and end_bounds['y'] + end_bounds['height'] <= page.viewport_size['height'] + 1"], 'scripts/test_causal_motion_browser.py': ["page.keyboard.press('ArrowRight')", "assert page.locator('.figure').evaluate('el=>el.scrollLeft>0')", "page.keyboard.press('End')", "assert end_region.evaluate('(e)=>document.activeElement===e')", 'assert end_region.evaluate(\'(e)=>[e.clientWidth,e.scrollWidth,e.querySelector("img").getBoundingClientRect().width]\') == end_before', "assert img.get_attribute('src') == end_src", 'toggle.scroll_into_view_if_needed()', "assert toggle.evaluate('(e)=>document.activeElement===e')", 'assert toggle.is_visible() and toggle.is_enabled()', "assert end_bounds and 0 <= end_bounds['x'] and (end_bounds['x'] + end_bounds['width'] <= width + 1)", "assert img.get_attribute('src') != end_src", "assert img.get_attribute('src') == end_src", "assert 0 <= end_bounds['y'] and end_bounds['y'] + end_bounds['height'] <= page.viewport_size['height'] + 1"]}

def check(source, required):
    tree = ast.parse(source)
    statements = {ast.unparse(n): n for n in ast.walk(tree) if isinstance(n, (ast.Assert, ast.Expr))}
    counts = Counter(ast.unparse(n) for n in ast.walk(tree) if isinstance(n, (ast.Assert, ast.Expr)))
    for expected, count in Counter(required).items():
        assert counts[expected] >= count, ('Missing retained interaction contract', expected, count)
    end = [n.lineno for k,n in statements.items() if ".press('End')" in k]
    if end:
        arrows = [n.lineno for k,n in statements.items() if ".press('ArrowRight')" in k]
        reveals = [n.lineno for k,n in statements.items() if 'scroll_into_view_if_needed' in k]
        assert arrows and min(arrows) < min(end) < min(reveals), 'Arrow proof, End event, then control reveal must remain ordered'
    return statements

negative_count = 0
for relative, required in REQUIRED.items():
    source = (ROOT / relative).read_text()
    statements = check(source, required)
    for expected in required:
        node = statements[expected]
        lines = source.splitlines()
        # Every protected statement is one source line, including semicolon pairs.
        assert node.lineno == node.end_lineno
        line = lines[node.lineno-1]
        lines[node.lineno-1] = line[:len(line)-len(line.lstrip())] + 'pass'
        try:
            check('\n'.join(lines), required)
        except AssertionError:
            negative_count += 1
        else:
            raise AssertionError(('Deleted original/new contract accepted', relative, expected))
print(f'PASS {len(REQUIRED)} browser-source contracts and {negative_count} actual source-deletion negatives; not a native browser run')
