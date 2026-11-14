/* Bilingual, deterministic, keyboard-operable teaching labs for adaptive optimisers.
 * No network access or third-party code. Static Markdown SVG images are the fallback.
 */
(() => {
  'use strict';
  const DATA = [
    [1, 2, 1, 0],
    [3, 1, 2, 2],
    [0, 2, 4, 2],
  ];
  const ROWS = DATA.map(row => row.reduce((a, b) => a + b, 0));
  const COLS = DATA[0].map((_, j) => DATA.reduce((sum, row) => sum + row[j], 0));
  const TOTAL = ROWS.reduce((a, b) => a + b, 0);
  const GRADIENTS = [[1, 1, 1, 1, 1, 1], [1, 0, 0, 0, 1, 0]];
  const translations = {
    en: {
      play: 'Play', pause: 'Pause', prev: 'Previous', next: 'Next', speed: 'Speed',
      step: 'Step', cell: 'Cell', frequent: 'Frequent', sparse: 'Sparse',
      headingAda: 'Explore AdaGrad updates', headingFactor: 'Explore factored moments',
      adaHint: 'Move between observations: a zero gradient retains its gain but produces no update.',
      factorHint: 'Select an element: row and column statistics reconstruct an approximation, not the original.',
      gain: 'Gain', update: 'Update magnitude', original: 'Original', estimate: 'Estimate',
      difference: 'Absolute difference', state: 'State', sum: 'Sum',
    },
    zh: {
      play: '播放', pause: '暫停', prev: '上一步', next: '下一步', speed: '速度',
      step: '步驟', cell: '元素', frequent: '頻繁座標', sparse: '稀疏座標',
      headingAda: '操作 AdaGrad 更新', headingFactor: '操作因式分解矩估計',
      adaHint: '切換梯度觀測：零梯度雖保留增益，參數更新仍為零。',
      factorHint: '選取矩陣元素：依列與行統計重建的是近似值，不是原矩陣。',
      gain: '增益', update: '更新量大小', original: '原始值', estimate: '估計值',
      difference: '絕對差異', state: '狀態', sum: '總和',
    },
  };

  function node(tag, className, value) {
    const el = document.createElement(tag);
    if (className) el.className = className;
    if (value !== undefined) el.textContent = String(value);
    return el;
  }
  function labelledButton(label, action) {
    const b = node('button', 'adaptive-lab-button', label);
    b.type = 'button';
    b.dataset.action = action;
    return b;
  }
  function number(value) { return Number(value).toFixed(3); }

  function enhance(container) {
    if (container.dataset.ready === 'yes') return;
    const mode = container.dataset.adaptiveLab;
    if (mode !== 'adagrad' && mode !== 'adafactor') return;
    const lang = container.dataset.lang === 'zh' ? 'zh' : 'en';
    const t = translations[lang];
    container.dataset.ready = 'yes';
    container.setAttribute('role', 'region');
    container.setAttribute('aria-label', mode === 'adagrad' ? t.headingAda : t.headingFactor);
    container.classList.add('adaptive-lab');
    container.append(node('h4', 'adaptive-lab-title', mode === 'adagrad' ? t.headingAda : t.headingFactor));
    container.append(node('p', 'adaptive-lab-hint', mode === 'adagrad' ? t.adaHint : t.factorHint));
    const figure = node('div', 'adaptive-lab-figure');
    container.append(figure);
    const controls = node('div', 'adaptive-lab-controls');
    const previous = labelledButton('◀ ' + t.prev, 'previous');
    const toggle = labelledButton('▶ ' + t.play, 'toggle');
    const next = labelledButton(t.next + ' ▶', 'next');
    const sliderLabel = node('label', 'adaptive-lab-slider-label', mode === 'adagrad' ? t.step : t.cell);
    const slider = node('input', 'adaptive-lab-range');
    slider.type = 'range'; slider.min = mode === 'adagrad' ? '1' : '0';
    slider.max = mode === 'adagrad' ? '6' : '11'; slider.step = '1';
    slider.value = mode === 'adagrad' ? '1' : '6';
    slider.setAttribute('aria-label', mode === 'adagrad' ? t.step : t.cell);
    sliderLabel.append(slider);
    const speedLabel = node('label', 'adaptive-lab-speed-label', t.speed + ' ');
    const speed = node('select', 'adaptive-lab-speed');
    speed.setAttribute('aria-label', t.speed);
    for (const [v, text] of [['0.5', '0.5×'], ['1', '1×'], ['2', '2×']]) {
      const option = node('option', '', text); option.value = v; speed.append(option);
    }
    speed.value = '1'; speedLabel.append(speed);
    controls.append(previous, toggle, next, sliderLabel, speedLabel);
    container.append(controls);
    const readout = node('div', 'adaptive-lab-readout');
    readout.setAttribute('role', 'status');
    readout.setAttribute('aria-live', 'polite');
    readout.setAttribute('aria-atomic', 'true');
    container.append(readout);
    let current = Number(slider.value);
    let timer = null;

    function adagrad() {
      figure.replaceChildren();
      const table = node('div', 'adaptive-lab-stats');
      for (let k = 0; k < 2; k++) {
        const g = GRADIENTS[k][current - 1];
        const G = GRADIENTS[k].slice(0, current).reduce((sum, v) => sum + v * v, 0);
        const gain = 1 / Math.sqrt(G);
        const update = Math.abs(g) * gain;
        const card = node('section', 'adaptive-lab-stat-card');
        const title = node('div', 'adaptive-lab-stat-title', k === 0 ? t.frequent : t.sparse);
        const bar = node('div', 'adaptive-lab-meter');
        const fill = node('div', 'adaptive-lab-meter-fill ' + (k === 0 ? 'adaptive-lab-blue' : 'adaptive-lab-teal'));
        fill.style.width = `${100 * G / 6}%`;
        bar.append(fill);
        const values = node('div', 'adaptive-lab-values', `g = ${g}    Σg² = ${G}    ${t.gain} = ${number(gain)}    |Δθ| = ${number(update)}`);
        card.append(title, bar, values); table.append(card);
      }
      figure.append(table);
      readout.textContent = `${t.step} ${current}/6 · ${t.frequent}: ${t.gain} ${number(1 / Math.sqrt(current))} · ${t.sparse}: |Δθ| = ${number(GRADIENTS[1][current - 1] / Math.sqrt(current >= 5 ? 2 : 1))}`;
    }
    function adafactor() {
      figure.replaceChildren();
      const row = Math.floor(current / 4), col = current % 4;
      const wrap = node('div', 'adaptive-lab-factor-wrap');
      const matrix = node('div', 'adaptive-lab-matrix');
      matrix.setAttribute('aria-label', `S = g squared, 3 by 4`);
      for (let i = 0; i < 3; i++) for (let j = 0; j < 4; j++) {
        const cell = node('div', 'adaptive-lab-cell' + (i === row && j === col ? ' adaptive-lab-selected' : '') + (i === row || j === col ? ' adaptive-lab-cross' : ''), DATA[i][j]);
        cell.style.setProperty('--intensity', String(DATA[i][j] / 4));
        matrix.append(cell);
      }
      const separator = node('div', 'adaptive-lab-equals', '≈');
      const result = node('div', 'adaptive-lab-factor-results');
      const top = node('div', 'adaptive-lab-rowcol', `R${row + 1} = ${ROWS[row]}   ·   C${col + 1} = ${COLS[col]}`);
      const formula = node('div', 'adaptive-lab-formula', `${ROWS[row]} × ${COLS[col]} / ${TOTAL}`);
      const value = ROWS[row] * COLS[col] / TOTAL;
      const resultValue = node('div', 'adaptive-lab-answer', `V̂${row + 1},${col + 1} = ${number(value)}`);
      const note = node('div', 'adaptive-lab-note', `${t.original} S = ${DATA[row][col]} · ${t.difference}: ${number(Math.abs(value - DATA[row][col]))}`);
      result.append(top, formula, resultValue, note);
      wrap.append(matrix, separator, result);
      figure.append(wrap);
      readout.textContent = `${t.cell} (${row + 1},${col + 1}) · ${t.original} ${DATA[row][col]} · ${t.estimate} ${number(value)} · ${t.sum} = ${TOTAL} · ${t.state} 3 + 4 vs 12`;
    }
    function draw() {
      slider.value = String(current);
      (mode === 'adagrad' ? adagrad : adafactor)();
      previous.disabled = current === Number(slider.min);
      next.disabled = current === Number(slider.max) && !timer;
      toggle.textContent = timer ? 'Ⅱ ' + t.pause : '▶ ' + t.play;
      toggle.setAttribute('aria-pressed', timer ? 'true' : 'false');
      slider.setAttribute('aria-valuetext', mode === 'adagrad' ? `${t.step} ${current}` : `${t.cell} ${Math.floor(current / 4) + 1},${current % 4 + 1}`);
    }
    function stop() { if (timer !== null) clearInterval(timer); timer = null; draw(); }
    function cycle() {
      const max = Number(slider.max), min = Number(slider.min);
      current = current >= max ? min : current + 1;
      draw();
    }
    function start() {
      if (timer !== null) return;
      timer = setInterval(cycle, 950 / Number(speed.value));
      draw();
    }
    previous.addEventListener('click', () => { stop(); current = Math.max(Number(slider.min), current - 1); draw(); });
    next.addEventListener('click', () => { stop(); current = Math.min(Number(slider.max), current + 1); draw(); });
    slider.addEventListener('input', () => { const target = Number(slider.value); stop(); current = target; draw(); });
    toggle.addEventListener('click', () => timer === null ? start() : stop());
    speed.addEventListener('change', () => { if (timer !== null) { stop(); start(); } });
    document.addEventListener('visibilitychange', () => { if (document.hidden) stop(); });
    window.matchMedia('(prefers-reduced-motion: reduce)').addEventListener?.('change', e => { if (e.matches) stop(); });
    // Avoid persistent animations across MkDocs instant-navigation page changes.
    if (typeof window.document$?.subscribe === 'function') window.document$.subscribe(() => {
      if (!container.isConnected) stop();
    });
    draw();
  }
  function boot() { document.querySelectorAll('[data-adaptive-lab]').forEach(enhance); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
  if (typeof window.document$?.subscribe === 'function') window.document$.subscribe(boot);
})();