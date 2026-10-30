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
  const fmt = v => v.toFixed(3);
  const clamp = (v, min, max, fallback) => Number.isFinite(v) ? Math.max(min, Math.min(max, v)) : fallback;
  function ema(m) {
    const values = [0.30];
    for (let i = 1; i < online.length; i++) values.push(m * values[i-1] + (1-m) * online[i]);
    return values;
  }
  const poly = values => values.map((v, i) => `${xs[i]},${y(v).toFixed(2)}`).join(' ');
  const circle = (x, cy, fill, active) => `<circle cx="${x}" cy="${cy.toFixed(2)}" r="${active ? 7 : 4.5}" fill="${fill}" stroke="white" stroke-width="${active ? 2.5 : 1.5}"/>`;
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
    const line = (values, color, dash, width) => `<polyline points="${poly(values)}" fill="none" stroke="${color}" stroke-width="${width}" stroke-linecap="round" stroke-linejoin="round" ${dash ? 'stroke-dasharray="5 6"' : ''}/>`;
    const circles = (values, color, active) => values.map((v, i) => circle(xs[i], y(v), color, i === active)).join('');
    const grid = [0.2, 0.6, 1.0].map(v => `<path d="M60 ${y(v).toFixed(2)} H545" stroke="#d7e3e9" stroke-width="1"/><text x="50" y="${(y(v)+4).toFixed(2)}" text-anchor="end" class="ssl-ema-axis">${v.toFixed(1)}</text>`).join('');
    const steps = xs.map((x,i) => `<text x="${x}" y="198" text-anchor="middle" class="ssl-ema-axis">${i}</text>`).join('');
    chart.innerHTML = `<svg viewBox="0 0 600 224" role="img" aria-label="${zh ? '離散線上與目標參數更新軌跡，示意數值' : 'Discrete online and target parameter trajectories, toy scalars'}">`+
      `<rect x="0.5" y="0.5" width="599" height="223" rx="8" fill="#f8fbfd" stroke="#c4d4df"/>`+
      grid + `<path d="M60 14 V174 H545" fill="none" stroke="#7e93a1" stroke-width="1.5"/>`+
      `<text x="60" y="19" class="ssl-ema-axis">Toy scalar</text>` + steps +
      `<text x="302" y="217" text-anchor="middle" class="ssl-ema-axis">Update index</text>`+
      (compare ? line(original, '#9babb7', true, 2) : '')+
      line(online, '#2c709b', false, 3) + line(target, '#138675', false, 3) +
      circles(online, '#2c709b', queryStep) + circles(target, '#138675', keyStep) +
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
        ? '圓點代表離散更新後的參數，不是連續訓練軌跡。藍色為線上／查詢權重，綠色為目標／鍵權重；改變動量後，灰色虛線顯示 m=0.90 的對照。橘色虛線連接目前兩個分支的狀態；差距數值顯示在圖下方。'
        : 'Dots mark discrete parameter updates, not continuous training. Blue is online/query; green is target/key. When momentum changes, the grey dashed line shows the m=0.90 reference. The orange dashed connector joins the current branch states; the numeric gap is shown below.';
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
