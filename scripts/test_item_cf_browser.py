#!/usr/bin/env python3
"""Smoke-test actual bilingual item-CF build, including MathJax and navigation."""
import argparse
import json
from pathlib import Path
from urllib.parse import urljoin
from mkdocs.config import load_config
from playwright.sync_api import sync_playwright
from test_built_motion_browser import serve_site, check_math_rendering, assert_document_fits

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/item-cf-browser'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--executable-path')
    args = parser.parse_args()
    config = load_config(str(ROOT / 'mkdocs.yml'))
    OUT.mkdir(parents=True, exist_ok=True)
    results = []
    try:
        with serve_site(Path(config.site_dir), config.site_url) as base, sync_playwright() as pw:
            browser = pw.chromium.launch(**({'executable_path': args.executable_path} if args.executable_path else {}))
            for locale, prefix in [('en', ''), ('zh-TW', 'zh-TW/')]:
                path = prefix + 'theory/models/recommender/item-based-cf/'
                assert (Path(config.site_dir) / path / 'index.html').is_file()
                for width in [390, 1280]:
                    viewport = {'width': width, 'height': 900}
                    page = browser.new_page(viewport=viewport)
                    record = {'locale': locale, 'width': width}
                    results.append(record)
                    try:
                        response = page.goto(urljoin(base, path), wait_until='networkidle')
                        assert response.status == 200
                        page.wait_for_selector('mjx-container')
                        record['math'] = check_math_rendering(page)
                        assert record['math']['containers'] >= 20, record
                        record['geometry'] = assert_document_fits(page, viewport)
                        article = page.locator('.md-content__inner')
                        assert article.locator('table').count() == 2
                        assert article.locator('h1').count() == 1
                        page.screenshot(path=str(OUT / f'{locale}-{width}.png'), full_page=True)
                        record['tables'] = []
                        for index, table in enumerate(article.locator('table').all()):
                            state = table.evaluate("""table => {
                                let wrap = table.parentElement;
                                while (wrap && !(['auto', 'scroll'].includes(getComputedStyle(wrap).overflowX)
                                    && wrap.scrollWidth > wrap.clientWidth + 1)) wrap = wrap.parentElement;
                                if (!wrap) return {overflow: false};
                                wrap.scrollIntoView({block: 'center'});
                                wrap.scrollLeft = wrap.scrollWidth;
                                const edge = table.rows[0].cells[table.rows[0].cells.length - 1].getBoundingClientRect();
                                const box = wrap.getBoundingClientRect();
                                return {overflow: true, left: wrap.scrollLeft,
                                    max: wrap.scrollWidth - wrap.clientWidth,
                                    lastColumnVisible: edge.right <= box.right + 1 && edge.left < box.right};
                            }""")
                            record['tables'].append(state)
                            if state['overflow']:
                                assert abs(state['left'] - state['max']) <= 1, state
                                assert state['lastColumnVisible'], state
                                page.screenshot(path=str(OUT / f'{locale}-{width}-table-{index}-right.png'))
                        # Real internal navigation away and back must preserve math and geometry.
                        article.locator('a[href="../"]').first.click()
                        page.wait_for_url('**/recommender/')
                        page.locator('.md-content__inner a[href="item-based-cf/"]').first.click()
                        page.wait_for_url('**/item-based-cf/')
                        page.wait_for_selector('mjx-container')
                        check_math_rendering(page)
                        assert_document_fits(page, viewport)
                        record['passed'] = True
                    except Exception as error:
                        record['error'] = str(error)
                        page.screenshot(path=str(OUT / f'{locale}-{width}-failure.png'), full_page=True)
                        raise
                    finally:
                        page.close()
            browser.close()
    finally:
        (OUT / 'report.json').write_text(json.dumps(results, indent=2))
    assert len(results) == 4
    print('PASS: 4 bilingual desktop/mobile item-CF scenarios, real MathJax and navigation')


if __name__ == '__main__':
    main()
