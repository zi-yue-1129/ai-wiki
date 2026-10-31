/* Original CC BY-SA 4.0. Discrete EMA trajectory comparison for MoCo and BYOL.
 * All scalar values are hand-calculable illustrations, not model measurements.
 * Driven by the existing seek/momentum controls: no duplicate sliders.
 */
(() => {
  'use strict';
  const online = [0.70, 0.85, 0.78, 0.91];
  const baseline = 0.90;
  const xs = [72, 223, 374, 525];
  const y = v => 174 - (v - 0.20) * 160;
  const fmt = v => (Math.round((v + Number.EPSILON) * 1000) / 1000).toFixed(3);
  const clamp = (v, min, max, fallback) => Number.isFinite(v) ? Math.max(min, Math.min(max, v)) : fallback;
  function ema(m) {
    const values = [0.30];
    for (let i = 1; i < online.length; i++) values.push(m * values[i-1] + (1-m) * online[i]);
    return values;
  }
  // Reveal only updates that have actually happened at the current seek position.
  // Future points are not yet available to the online/target branch.
  const poly = (values, through) => values.slice(0, through + 1).map((v, i) => `${xs[i]},${y(v).toFixed(2)}`).join(' ');
  const circle = (x, cy, fill, active, step, series) => `<circle data-series="${series}" data-step="${step}" cx="${x}" cy="${cy.toFixed(2)}" r="${active ? 7 : 4.5}" fill="${fill}" stroke="white" stroke-width="${active ? 2.5 : 1.5}"/>`;
  function render(host, kind, zh, chart, readout) {
    const seek = host.querySelector('[data-act="seek"]');
    const momentum = host.querySelector('[data-act="momentum"]');
    if (!seek || !momentum) return;
    const frame = Math.round(clamp(Number(seek.value), 0, 14, 0));
    const m = clamp(Number(momentum.value), 0.5, 0.99, baseline);
    const turn = Math.floor(frame / 5), phase = frame % 5;
    // Query/online SGD happens before the target/key EMA in each iteration.
    const queryStep = turn + (phase >= (kind === 'moco' ? 2 : 3) ? 1 : 0);
    const keyStep = turn + (phase >= (kind === 'moco' ? 3 : 4) ? 1 : 0);
    const target = ema(m), original = ema(baseline);
    const compare = Math.abs(m - baseline) > 0.0001;
    const line = (values, color, dash, width, through, series) => `<polyline data-series="${series}" data-through="${through}" points="${poly(values, through)}" fill="none" stroke="${color}" stroke-width="${width}" stroke-linecap="round" stroke-linejoin="round" ${dash ? 'stroke-dasharray="5 6"' : ''}/>`;
    const circles = (values, color, active, series) => values.slice(0, active + 1).map((v, i) => circle(xs[i], y(v), color, i === active, i, series)).join('');
    const grid = [0.2, 0.6, 1.0].map(v => `<path d="M60 ${y(v).toFixed(2)} H545" stroke="#d7e3e9" stroke-width="1"/><text x="50" y="${(y(v)+4).toFixed(2)}" text-anchor="end" class="ssl-ema-axis">${v.toFixed(1)}</text>`).join('');
    const steps = xs.map((x,i) => `<text x="${x}" y="198" text-anchor="middle" class="ssl-ema-axis">${i}</text>`).join('');
    chart.innerHTML = `<svg viewBox="0 0 600 224" role="img" aria-label="${zh ? '已完成的離散線上與目標參數更新，示意數值' : 'Completed discrete online and target updates, toy scalars'}">`+
      `<rect x="0.5" y="0.5" width="599" height="223" rx="8" fill="#f8fbfd" stroke="#c4d4df"/>`+
      grid + `<path d="M60 14 V174 H545" fill="none" stroke="#7e93a1" stroke-width="1.5"/>`+
      `<text x="60" y="19" class="ssl-ema-axis">Toy scalar</text>` + steps +
      `<text x="302" y="217" text-anchor="middle" class="ssl-ema-axis">Update index</text>`+
      (compare ? line(original, '#9babb7', true, 2, keyStep, 'reference') : '')+
      line(online, '#2c709b', false, 3, queryStep, 'online') + line(target, '#138675', false, 3, keyStep, 'target') +
      circles(online, '#2c709b', queryStep, 'online') + circles(target, '#138675', keyStep, 'target') +
      `<path d="M${xs[queryStep]} ${y(online[queryStep]).toFixed(2)} L${xs[keyStep]} ${y(target[keyStep]).toFixed(2)}" stroke="#c07443" stroke-width="1.5" stroke-dasharray="3 4"/>`+
      `<g class="ssl-ema-legend"><path d="M365 18 H383" stroke="#2c709b" stroke-width="3"/><text x="389" y="22">Online</text>`+
      `<path d="M365 35 H383" stroke="#138675" stroke-width="3"/><text x="389" y="39">Target</text>`+
      (compare ? `<path d="M465 35 H483" stroke="#9babb7" stroke-width="2" stroke-dasharray="4 4"/><text x="489" y="39">m=.90</text>` : '')+
      `</g></svg>`;
    const q = online[queryStep], k = target[keyStep];
    readout.textContent = zh
      ? `線上更新 ${queryStep}：${fmt(q)} · 目標 EMA ${keyStep}：${fmt(k)} · |差距| ${fmt(Math.abs(q-k))}`
      : `Online update ${queryStep}: ${fmt(q)} · Target EMA ${keyStep}: ${fmt(k)} · |gap| ${fmt(Math.abs(q-k))}`;
  }
  function enhance() {
    document.querySelectorAll('[data-self-supervised-lab]').forEach(host => {
      if (host.dataset.emaTrajectoryReady) return;
      const kind = host.dataset.selfSupervisedLab;
      if (kind !== 'moco' && kind !== 'byol') return;
      const compute = host.querySelector('.ssl-compute');
      const seek = host.querySelector('[data-act="seek"]');
      const momentum = host.querySelector('[data-act="momentum"]');
      if (!compute || !seek || !momentum) return;
      host.dataset.emaTrajectoryReady = 'yes';
      const zh = host.dataset.locale === 'zh-TW';
      const section = document.createElement('section');
      section.className = 'ssl-ema-trajectory';
      const title = document.createElement('div');
      title.className = 'ssl-ema-heading';
      title.textContent = zh ? '動量更新軌跡（示意）' : 'Momentum update trajectory (toy scalars)';
      const chart = document.createElement('div');
      chart.className = 'ssl-ema-chart';
      const readout = document.createElement('output');
      readout.className = 'ssl-ema-readout';
      readout.setAttribute('aria-live', 'off');
      const note = document.createElement('p');
      note.className = 'ssl-ema-note';
      note.textContent = zh
        ? '只顯示已完成的離散更新：藍色為線上／查詢 SGD，綠色為目標／鍵 EMA；尚未發生的更新不會提前出現在圖上。改變動量後，灰色虛線顯示相同已完成步數的 m=0.90 對照。橘色虛線連接目前兩個分支的狀態；線段不是連續梯度或實測訓練軌跡。'
        : 'Only completed discrete updates are visible: blue is online/query SGD, green is target/key EMA. Future updates are not drawn in advance. Changing momentum adds an m=0.90 reference through the same completed steps. The orange dashed connector joins current branch states; lines are not continuous gradients or measured training traces.';
      section.append(title, chart, readout, note);
      compute.after(section);
      const update = () => render(host, kind, zh, chart, readout);
      seek.addEventListener('input', update);
      momentum.addEventListener('input', update);
      // The existing autoplay changes the seek value programmatically, without
      // firing input. Its computation readout changes on every operation.
      new MutationObserver(update).observe(compute, {childList:true, characterData:true, subtree:true});
      update();
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', enhance);
  else enhance();
  if (window.document$ && typeof window.document$.subscribe === 'function') window.document$.subscribe(enhance);
})();
