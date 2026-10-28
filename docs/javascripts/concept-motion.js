/* Accessible enhancement for shared concept-motion SVGs.
 * GitHub renders the SVG image without JavaScript; MkDocs adds controls.
 */
(() => {
  'use strict';
  const suffix = /-motion\.svg(?=$|[?#])/;
  const moeSuffix = /moe-top2-routing-motion\.svg(?=$|[?#])/;
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');

  function enhance(root = document) {
    for (const img of root.querySelectorAll('img[src*="concept-animations/"]')) {
      if (img.dataset.conceptMotionEnhanced === 'yes') continue;
      const animated = img.dataset.motionSrc || img.getAttribute('src') || '';
      if (!suffix.test(animated)) continue;
      const still = img.dataset.stillSrc || animated.replace(suffix, '-still.svg');
      const isMoe = moeSuffix.test(animated);
      const tokenB = isMoe ? animated.replace(suffix, '-token-b.svg') : '';
      const chinese = /[\u3400-\u9fff]/.test(img.alt || '');
      const originalAlt = img.alt;
      const host = document.createElement('span');
      host.className = 'concept-motion-player';
      img.before(host);
      host.append(img);
      img.dataset.conceptMotionEnhanced = 'yes';

      const controls = document.createElement('span');
      controls.className = 'concept-motion-controls';
      const toggle = document.createElement('button');
      toggle.className = 'concept-motion-toggle';
      toggle.type = 'button';
      controls.append(toggle);
      let paused = reduced.matches;
      let overridden = false;
      let token = 0;
      let step = null;
      let status = null;
      if (isMoe) {
        step = document.createElement('button');
        step.className = 'concept-motion-toggle';
        step.type = 'button';
        controls.append(step);
        status = document.createElement('span');
        status.className = 'concept-motion-status';
        status.setAttribute('role', 'status');
        status.setAttribute('aria-live', 'polite');
      }

      const sync = () => {
        const next = paused ? (isMoe && token === 1 ? tokenB : still) : animated;
        if (img.getAttribute('src') !== next) img.setAttribute('src', next);
        img.alt = paused && isMoe
          ? (token === 0
            ? (chinese ? '詞元 A 啟動 E1 與 E3，輸出匯入加權合併節點。' : 'Token A activates E1 and E3, feeding a weighted merge.')
            : (chinese ? '詞元 B 啟動 E2 與 E4，輸出匯入加權合併節點。' : 'Token B activates E2 and E4, feeding a weighted merge.'))
          : originalAlt;
        toggle.textContent = paused ? (chinese ? '▶ 播放動畫' : '▶ Play animation') : (chinese ? 'Ⅱ 暫停動畫' : 'Ⅱ Pause animation');
        toggle.setAttribute('aria-label', paused ? (chinese ? '播放概念動畫' : 'Play concept animation') : (chinese ? '暫停概念動畫' : 'Pause concept animation'));
        if (step) {
          step.textContent = paused
            ? (token === 0 ? (chinese ? '下一步：詞元 B' : 'Next: token B') : (chinese ? '下一步：詞元 A' : 'Next: token A'))
            : (chinese ? '逐步檢視' : 'Step through tokens');
          step.setAttribute('aria-label', step.textContent);
          status.textContent = paused
            ? (token === 0 ? (chinese ? '目前顯示詞元 A：E1 與 E3' : 'Showing token A: E1 and E3') : (chinese ? '目前顯示詞元 B：E2 與 E4' : 'Showing token B: E2 and E4'))
            : (chinese ? '正在播放兩個詞元的路由動畫' : 'Playing routing for both tokens');
        }
      };
      toggle.addEventListener('click', () => {
        overridden = true;
        paused = !paused;
        sync();
      });
      if (step) step.addEventListener('click', () => {
        overridden = true;
        if (paused) token = 1 - token;
        else { paused = true; token = 0; }
        sync();
      });
      reduced.addEventListener?.('change', event => {
        if (!overridden) { paused = event.matches; token = 0; sync(); }
      });
      host.append(controls);
      if (status) host.append(status);
      sync();
    }
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', () => enhance());
  else enhance();
  // Material for MkDocs instant navigation replaces the article without a page reload.
  if (typeof window.document$ !== 'undefined' && typeof window.document$.subscribe === 'function') {
    window.document$.subscribe(() => enhance());
  }
})();
