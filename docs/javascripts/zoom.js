/* Click or press Enter on a figure to enlarge it: content images, Mermaid diagrams and inline SVG.
 * One shared dialog shows a copy of the figure that can be zoomed (wheel, pinch, +/- keys) and panned.
 * Animated SVG images keep playing in the enlarged copy because they are still <img> elements.
 */
(() => {
  'use strict';
  const FIGURE = '.md-typeset img, .md-typeset .mermaid, .md-typeset > svg';
  // Zoom limits, relative to the scale at which the figure fits the screen.
  const MIN_ZOOM = 0.5;
  const MAX_ZOOM = 8;

  let dialog = null;
  let viewport = null;
  let content = null;
  let source = null; // figure that opened the dialog, so focus can return to it
  let size = { w: 0, h: 0 };
  let base = 1; // scale at which the figure fits the viewport
  let view = { k: 1, x: 0, y: 0 };
  const pointers = new Map();
  let pinch = null;
  let start = null;
  let moved = false;

  const clamp = (n, lo, hi) => Math.min(hi, Math.max(lo, n));
  const isZh = () => document.documentElement.lang.startsWith('zh');

  function naturalSize(svgOrImg) {
    const rect = svgOrImg.getBoundingClientRect();
    if (svgOrImg.tagName.toLowerCase() === 'svg') {
      const box = svgOrImg.viewBox?.baseVal;
      if (box?.width) return { w: box.width, h: box.height };
      return { w: rect.width, h: rect.height };
    }
    // Some SVG files report no intrinsic width, so keep the displayed aspect ratio.
    const w = svgOrImg.naturalWidth || rect.width;
    return { w, h: w * rect.height / rect.width };
  }

  function build() {
    const zh = isZh();
    const t = zh
      ? { in: '放大', out: '縮小', fit: '適合螢幕', close: '關閉', name: '放大檢視' }
      : { in: 'Zoom in', out: 'Zoom out', fit: 'Fit to screen', close: 'Close', name: 'Enlarged view' };
    dialog = document.createElement('dialog');
    dialog.className = 'zoom-dialog';
    dialog.setAttribute('aria-label', t.name);
    dialog.innerHTML = `
      <div class="zoom-toolbar">
        <button type="button" data-zoom="in" aria-label="${t.in}" title="${t.in}">+</button>
        <button type="button" data-zoom="out" aria-label="${t.out}" title="${t.out}">&minus;</button>
        <button type="button" data-zoom="fit" aria-label="${t.fit}" title="${t.fit}">${zh ? '適合' : 'Fit'}</button>
        <button type="button" data-zoom="close" aria-label="${t.close}" title="${t.close}">&times;</button>
      </div>
      <div class="zoom-viewport"><div class="zoom-content"></div></div>`;
    document.body.append(dialog);
    viewport = dialog.querySelector('.zoom-viewport');
    content = dialog.querySelector('.zoom-content');

    const centre = () => ({ x: viewport.clientWidth / 2, y: viewport.clientHeight / 2 });
    dialog.querySelector('.zoom-toolbar').addEventListener('click', event => {
      const action = event.target.closest('button')?.dataset.zoom;
      if (action === 'in') zoomAt(centre().x, centre().y, 1.25);
      else if (action === 'out') zoomAt(centre().x, centre().y, 0.8);
      else if (action === 'fit') fit();
      else if (action === 'close') dialog.close();
    });
    dialog.addEventListener('keydown', event => {
      if (event.key === '+' || event.key === '=') zoomAt(centre().x, centre().y, 1.25);
      else if (event.key === '-') zoomAt(centre().x, centre().y, 0.8);
      else if (event.key === '0') fit();
    });
    dialog.addEventListener('close', () => {
      content.replaceChildren();
      source?.focus({ preventScroll: true });
      source = null;
    });

    viewport.addEventListener('wheel', event => {
      event.preventDefault();
      const r = viewport.getBoundingClientRect();
      zoomAt(event.clientX - r.left, event.clientY - r.top, Math.exp(-event.deltaY * 0.002));
    }, { passive: false });
    viewport.addEventListener('pointerdown', event => {
      viewport.setPointerCapture(event.pointerId);
      pointers.set(event.pointerId, { x: event.clientX, y: event.clientY });
      if (pointers.size === 1) {
        start = { x: event.clientX, y: event.clientY };
        moved = false;
      }
      pinch = pinchState();
    });
    viewport.addEventListener('pointermove', event => {
      const prev = pointers.get(event.pointerId);
      if (!prev) return;
      const now = { x: event.clientX, y: event.clientY };
      pointers.set(event.pointerId, now);
      if (pointers.size === 1) {
        pan(now.x - prev.x, now.y - prev.y);
        if (Math.hypot(now.x - start.x, now.y - start.y) > 5) moved = true;
      } else if (pinch) {
        const g = pinchState();
        const r = viewport.getBoundingClientRect();
        zoomAt(g.x - r.left, g.y - r.top, g.d / pinch.d);
        pan(g.x - pinch.x, g.y - pinch.y);
        moved = true;
        pinch = g;
      }
    });
    const release = event => {
      pointers.delete(event.pointerId);
      pinch = pinchState();
    };
    viewport.addEventListener('pointerup', release);
    viewport.addEventListener('pointercancel', release);
    // A tap on the empty background closes the dialog; a drag or pinch does not.
    viewport.addEventListener('click', event => {
      if (!moved && event.target === viewport) dialog.close();
    });
  }

  function pinchState() {
    if (pointers.size !== 2) return null;
    const [a, b] = pointers.values();
    return {
      x: (a.x + b.x) / 2,
      y: (a.y + b.y) / 2,
      d: Math.hypot(a.x - b.x, a.y - b.y),
    };
  }

  function render() {
    content.style.transform = `translate(${view.x}px, ${view.y}px) scale(${view.k})`;
  }

  function fit() {
    const vw = viewport.clientWidth;
    const vh = viewport.clientHeight;
    base = Math.min(vw / size.w, vh / size.h) * 0.92;
    view = { k: base, x: (vw - size.w * base) / 2, y: (vh - size.h * base) / 2 };
    render();
  }

  function zoomAt(px, py, factor) {
    const k = clamp(view.k * factor, base * MIN_ZOOM, base * MAX_ZOOM);
    const ratio = k / view.k;
    view = { k, x: px - (px - view.x) * ratio, y: py - (py - view.y) * ratio };
    render();
  }

  function pan(dx, dy) {
    view.x += dx;
    view.y += dy;
    render();
  }

  function open(figure) {
    const target = figure.matches('.mermaid') ? figure.querySelector('svg') : figure;
    if (!target) return; // a Mermaid block that has not rendered yet
    size = naturalSize(target);
    if (!size.w || !size.h) return;
    if (!dialog || !dialog.isConnected) build();
    source = figure;
    const copy = target.cloneNode(true);
    copy.removeAttribute('style');
    copy.removeAttribute('loading');
    copy.removeAttribute('tabindex');
    copy.style.width = `${size.w}px`;
    copy.style.height = `${size.h}px`;
    copy.style.maxWidth = 'none';
    content.replaceChildren(copy);
    dialog.showModal();
    fit();
  }

  function enhance() {
    for (const figure of document.querySelectorAll(FIGURE)) {
      if (figure.closest('a') || figure.hasAttribute('tabindex')) continue;
      figure.tabIndex = 0;
    }
  }

  document.addEventListener('click', event => {
    if (event.target.closest?.('a')) return;
    const figure = event.target.closest?.(FIGURE);
    if (figure) open(figure);
  });
  document.addEventListener('keydown', event => {
    if (event.key !== 'Enter' && event.key !== ' ') return;
    if (!event.target.matches?.(FIGURE)) return;
    event.preventDefault();
    open(event.target);
  });
  window.addEventListener('resize', () => {
    if (dialog?.open) fit();
  });

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', () => enhance());
  else enhance();
  // Material for MkDocs instant navigation replaces the article without a page reload.
  if (typeof window.document$ !== 'undefined' && typeof window.document$.subscribe === 'function') {
    window.document$.subscribe(() => enhance());
  }
})();
