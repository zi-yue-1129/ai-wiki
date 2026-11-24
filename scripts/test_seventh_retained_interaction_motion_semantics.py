#!/usr/bin/env python3
"""AST source contracts only; native browser execution remains separately required."""
import ast
from collections import Counter
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {'scripts/test_ssm_motion_browser.py': ["await page.keyboard.press('ArrowRight')", "assert await page.locator('.ssm-motion-viewport').evaluate('(v)=>v.scrollLeft>0')", "await page.keyboard.press('End')", "assert await end_region.evaluate('(e)=>document.activeElement===e')", 'assert await end_region.evaluate(\'(e)=>[e.clientWidth,e.scrollWidth,e.querySelector("img").getBoundingClientRect().width]\') == end_before', "assert await img.get_attribute('src') == end_src", 'await button.scroll_into_view_if_needed()', "assert await button.evaluate('(e)=>document.activeElement===e')", 'assert await button.is_visible() and await button.is_enabled()', "assert end_bounds and 0 <= end_bounds['x'] and (end_bounds['x'] + end_bounds['width'] <= width + 1)", "assert await img.get_attribute('src') != end_src", "assert await img.get_attribute('src') == end_src", "assert 0 <= end_bounds['y'] and end_bounds['y'] + end_bounds['height'] <= page.viewport_size['height'] + 1"], 'scripts/test_working_memory_labs_browser.py': ["assert gate.get_attribute('data-current-memory') == 'X', 'open distractor must overwrite A'", "assert gate.locator('.wm-lab-status').inner_text().endswith(memory_label + ': X')", 'assert gate.locator(\'svg text[x="580"][y="154"]\').text_content() == \'X\'', 'assert gate.locator(\'svg text[x="580"][y="154"]\').is_visible()', "assert gate.get_attribute('data-current-memory') == 'B'", "assert gate.locator('.wm-lab-status').inner_text().endswith(memory_label + ': B')", 'assert gate.locator(\'svg text[x="580"][y="154"]\').text_content() == \'B\'', 'assert gate.locator(\'svg text[x="580"][y="154"]\').is_visible()']}

def check(source, required):
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == 'inner_text':
            receiver = ast.unparse(node.func.value)
            assert 'svg text[' not in receiver, 'SVG text must use text_content(), not HTMLElement-only inner_text()'
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

# Actual source mutation: retain exact labels/visibility but regress SVG API only.
working_memory = (ROOT / 'scripts/test_working_memory_labs_browser.py').read_text()
for label in ('X', 'B'):
    good = "gate.locator('svg text[x=\"580\"][y=\"154\"]').text_content() == '" + label + "'"
    assert good in working_memory
    mutated = working_memory.replace(good, good.replace('.text_content()', '.inner_text()'), 1)
    try:
        check(mutated, REQUIRED['scripts/test_working_memory_labs_browser.py'])
    except AssertionError as error:
        assert 'SVG text must use text_content' in str(error), error
    else:
        raise AssertionError('SVG inner_text regression accepted')
print('PASS 2 SVG namespace/API substitution negatives; HTML status still uses inner_text')
