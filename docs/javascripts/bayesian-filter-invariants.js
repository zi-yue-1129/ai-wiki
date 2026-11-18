/* Synthetic, deterministic conservation checks for the existing Bayesian labs.
 * One Kalman correction and one systematic particle-resampling draw, not iterations.
 */
(() => {
  'use strict';
  const NS = 'http://www.w3.org/2000/svg';
  const particles = [1, 2.1, 2.9, 3.7, 4.4, 5.3, 6.1, 6.6, 7.4, 8.8];
  const svgElement = (tag, attrs = {}, text) => {
    const e = document.createElementNS(NS, tag);
    for (const [key, value] of Object.entries(attrs)) e.setAttribute(key, String(value));
    if (text !== undefined) e.textContent = String(text);
    return e;
  };
  const put = (svg, tag, attrs, text) => svg.appendChild(svgElement(tag, attrs, text));
  const label = (svg, x, y, s, opts = {}) => put(svg, 'text', {x, y, fill: '#35526b', 'font-size': 12, 'font-family': 'system-ui,sans-serif', ...opts}, s);
  const line = (svg, x1, y1, x2, y2, color, extra = {}) => put(svg, 'line', {x1, y1, x2, y2, stroke: color, 'stroke-width': 1.5, ...extra});
  const rect = (svg, x, y, width, height, fill, opts = {}) => put(svg, 'rect', {x, y, width: Math.max(0, width), height, fill, ...opts});
  const fmt = x => x.toFixed(3);
  const frame = (svg, heading, description) => {
    svg.replaceChildren();
    svg.setAttribute('viewBox', '0 0 700 244');
    svg.setAttribute('role', 'img');
    svg.setAttribute('aria-label', description);
    put(svg, 'title', {}, description);
    rect(svg, 0, 0, 700, 244, '#f7fafc', {rx: 12});
    rect(svg, 12, 10, 676, 224, '#ffffff', {rx: 9, stroke: '#dce7ee'});
    label(svg, 24, 38, heading, {'font-size': 16, 'font-weight': 700, fill: '#233f53'});
  };
  const translations = {
    en: {
      kalman: 'Kalman correction covariance decomposed into prior and measurement noise',
      particle: 'Systematic resampling cumulative-count discrepancy across ancestor boundaries',
      waitK: 'Prediction only. The Joseph variance contributions will appear after correction.',
      waitP: 'Weight calculation is not resampling. Realised cumulative counts appear only at the draw.',
      k: (a, b, v) => `Joseph scalar covariance: prior contribution ${fmt(a)} plus measurement-noise contribution ${fmt(b)} equals corrected variance ${fmt(v)}. These are synthetic calculations.`,
      p: (max, n) => `Across ${n} ancestor boundaries the maximum absolute cumulative count discrepancy is ${fmt(max)} descendants (strictly below one for systematic resampling). Synthetic ten-particle example.`
    },
    zh: {
      kalman: '卡爾曼 Joseph 共變異數修正中，預測誤差與量測雜訊的貢獻',
      particle: '系統性重採樣在各祖先邊界的累積後代數偏差',
      waitK: '目前只有預測階段；待修正階段才顯示 Joseph 變異數分解。',
      waitP: '概似加權不是重採樣；取得抽樣結果後才顯示實際累積數量。',
      k: (a, b, v) => `Joseph 一維變異數分解：預測誤差貢獻 ${fmt(a)} 加量測雜訊貢獻 ${fmt(b)} 等於後驗變異數 ${fmt(v)}；均為人工示意。`,
      p: (max, n) => `跨 ${n} 個祖先邊界，累積後代數偏差最大絕對值為 ${fmt(max)}（系統性重採樣嚴格小於一個後代）；人工十粒子示例。`
    }
  };
  function kalman(svg, [P, R, y], stage, t) {
    const K = P / (P + R), a = (1 - K) ** 2 * P, b = K ** 2 * R, v = a + b;
    frame(svg, 'JOSEPH / VARIANCE', t.kalman);
    const start = 168, width = 430, baseline = 184;
    label(svg, 29, 84, 'Prior P−');
    rect(svg, start, 69, width, 20, '#c4d5e8', {rx: 3});
    label(svg, 651, 84, fmt(P), {'text-anchor': 'end'});
    if (stage === 2) {
      label(svg, 29, 128, 'Joseph P+');
      const aw = width * a / P, bw = width * b / P;
      rect(svg, start, 113, aw, 20, '#527ab8');
      rect(svg, start + aw, 113, bw, 20, '#dc934c');
      label(svg, 651, 128, fmt(v), {'text-anchor': 'end'});
      rect(svg, 181, 195, 12, 9, '#527ab8');
      label(svg, 199, 204, 'Prior ' + fmt(a), {'font-size': 11});
      rect(svg, 371, 195, 12, 9, '#dc934c');
      label(svg, 389, 204, 'Noise ' + fmt(b), {'font-size': 11});
    } else {
      label(svg, 29, 127, 'Await correction', {'font-size': 12});
    }
    line(svg, start, 164, start + width, 164, '#a2b4c2');
    for (const f of [0, .5, 1]) label(svg, start + width * f, baseline, f === 0 ? '0' : f === 1 ? 'P−' : '0.5 P−', {'text-anchor': 'middle', 'font-size': 11});
    Object.assign(svg.dataset, {priorContribution: a.toFixed(9), noiseContribution: b.toFixed(9), posteriorVariance: v.toFixed(9), gain: K.toFixed(9), stage});
    return stage === 2 ? t.k(a, b, v) : t.waitK;
  }
  function particle(svg, [y, sd, u0], stage, t) {
    const raw = particles.map(x => Math.exp(-.5 * ((x - y) / sd) ** 2));
    const sum = raw.reduce((a, b) => a + b, 0);
    let cumulative = 0;
    const F = raw.map(x => (cumulative += x / sum));
    const targets = Array.from({length: 10}, (_, j) => u0 + j / 10);
    const ancestors = targets.map(z => {const index = F.findIndex(f => f > z); return index < 0 ? 9 : index;});
    const counts = particles.map((_, i) => ancestors.filter(j => j === i).length);
    let cumulativeDraws = 0;
    const deltas = [0, ...counts.map((count, i) => (cumulativeDraws += count) - 10 * F[i])];
    const max = Math.max(...deltas.map(Math.abs));
    frame(svg, 'SYSTEMATIC / CUMULATIVE ERROR', t.particle);
    const x = i => 78 + i * 55, z = d => 127 - 65 * d;
    rect(svg, 78, z(1), 550, 130, '#edf4fa');
    for (const d of [-1, 0, 1]) {
      line(svg, 78, z(d), 628, z(d), d === 0 ? '#698397' : '#bbcad8', {'stroke-dasharray': d === 0 ? 'none' : '4 5'});
      label(svg, 58, z(d) + 4, d > 0 ? '+1' : String(d), {'text-anchor': 'end', 'font-size': 11});
    }
    if (stage === 3) {
      put(svg, 'path', {d: deltas.map((d, i) => `${i ? 'L' : 'M'} ${x(i)} ${z(d)}`).join(' '), stroke: '#238f8e', fill: 'none', 'stroke-width': 3, 'stroke-linejoin': 'round'});
      deltas.forEach((d, i) => put(svg, 'circle', {cx: x(i), cy: z(d), r: 4, fill: '#238f8e', stroke: '#fff', 'stroke-width': 1}));
      label(svg, 618, 41, 'Max |Δ| = ' + fmt(max), {'text-anchor': 'end', 'font-size': 12, 'font-weight': 600});
    } else {
      label(svg, 425, 112, stage < 2 ? 'Await weights / draw' : 'Await draw', {'text-anchor': 'middle'});
    }
    for (let i = 0; i <= 10; i += 2) label(svg, x(i), 218, String(i), {'text-anchor': 'middle', 'font-size': 11});
    label(svg, 621, 233, 'Ancestor boundary', {'text-anchor': 'end', 'font-size': 11});
    Object.assign(svg.dataset, {deltas: deltas.map(d => d.toFixed(7)).join(','), maxDiscrepancy: max.toFixed(9), cumulativeLast: cumulativeDraws, stage});
    return stage === 3 ? t.p(max, 10) : t.waitP;
  }
  function enhance(host) {
    if (host.dataset.bfInvariantsReady) return;
    const panel = host.querySelector('.bf-panel');
    if (!panel) return;
    const kind = host.dataset.lab, t = translations[host.dataset.lang.startsWith('zh') ? 'zh' : 'en'];
    if (kind !== 'kalman' && kind !== 'particle') return;
    host.dataset.bfInvariantsReady = 'true';
    const region = document.createElement('div');
    region.className = 'bf-graphic bf-insight bf-invariant';
    region.tabIndex = 0;
    region.setAttribute('role', 'region');
    region.setAttribute('aria-label', t[kind]);
    const svg = svgElement('svg');
    svg.dataset.bfInvariant = kind;
    region.append(svg);
    const summary = document.createElement('p');
    summary.className = 'bf-insight-summary';
    summary.setAttribute('aria-live', 'polite');
    panel.querySelector('.bf-output').before(region, summary);
    const inputs = [...panel.querySelectorAll('.bf-ranges input')];
    const output = panel.querySelector('.bf-output');
    const update = () => {
      const values = inputs.map(input => Number(input.value));
      const stage = Number(panel.querySelector('.bf-step').value);
      summary.textContent = kind === 'kalman' ? kalman(svg, values, stage, t) : particle(svg, values, stage, t);
    };
    new MutationObserver(update).observe(output, {childList: true});
    host.addEventListener('input', update);
    update();
  }
  const init = () => document.querySelectorAll('.bayesian-filter-lab[data-lab]').forEach(enhance);
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
  if (window.document$?.subscribe) window.document$.subscribe(init);
})();
