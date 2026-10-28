/* Accessible enhancement for shared concept-motion SVGs.
 * Markdown images remain independently viewable in GitHub without this script.
 * Each animated SVG has a matching '-still.svg' for motion-sensitive readers.
 */
(() => {
  'use strict';
  const suffix = /-motion\.svg(?=$|[?#])/;
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');

  function enhance(root = document) {
    for (const img of root.querySelectorAll('img[src*="concept-animations/"]')) {
      if (img.dataset.conceptMotionEnhanced === 'yes') continue;
      const animated = img.dataset.motionSrc || img.getAttribute('src') || '';
      if (!suffix.test(animated)) continue;
      const still = img.dataset.stillSrc || animated.replace(suffix, '-still.svg');
      const chinese = /[\u3400-\u9fff]/.test(img.alt || '');
      const host = document.createElement('span');
      host.className = 'concept-motion-player';
      img.before(host);
      host.append(img);
      img.dataset.conceptMotionEnhanced = 'yes';
      const button = document.createElement('button');
      button.className = 'concept-motion-toggle';
      button.type = 'button';
      let paused = reduced.matches;
      let overridden = false;
      const sync = () => {
        const next = paused ? still : animated;
        if (img.getAttribute('src') !== next) img.setAttribute('src', next);
        button.textContent = paused ? (chinese ? '▶ 播放動畫' : '▶ Play animation') : (chinese ? 'Ⅱ 暫停動畫' : 'Ⅱ Pause animation');
        button.setAttribute('aria-pressed', String(paused));
        button.setAttribute('aria-label', paused ? (chinese ? '播放概念動畫' : 'Play concept animation') : (chinese ? '暫停概念動畫' : 'Pause concept animation'));
      };
      button.addEventListener('click', () => {
        overridden = true;
        paused = !paused;
        sync();
      });
      reduced.addEventListener?.('change', event => {
        if (!overridden) {paused = event.matches; sync();}
      });
      host.append(button);
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
