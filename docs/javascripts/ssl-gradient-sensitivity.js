/* Original CC BY-SA 4.0 gradient-sensitivity companion to the MoCo/BYOL labs.
 * The existing native loss slider drives this chart: no duplicate controls.
 * These are exact derivatives of toy objectives, not measured network gradients.
 */
(() => {
  'use strict';
  const negatives = [-0.20, -0.10, 0, 0.10, 0.20, 0.05];
  const W = 500, H = 166, left = 49, right = 476, top = 20, bottom = 127;
  const fmt = value => (Math.abs(value) < 0.0005 ? 0 : value).toFixed(3);
  function mocoGradient(tau) {
    // Shift by the positive logit: numerically stable at low temperatures.
    const negativeSum = negatives.reduce((sum, s) => sum + Math.exp((s - 0.70) / tau), 0);
    const p = 1 / (1 + negativeSum);
    return {p, derivative: (p - 1) / tau, magnitude: (1 - p) / tau};
  }
  function snapshot(kind, value) {
    if (kind === 'moco') {
      const tau = Math.min(1, Math.max(0.10, value));
      return {x: (tau - 0.10) / 0.90, value: tau, ...mocoGradient(tau), max: 1.5};
    }
    const cosine = Math.min(1, Math.max(-1, value));
    const angle = Math.acos(cosine);
    return {x: angle / Math.PI, value: angle, derivative: 2 * Math.sin(angle),
      magnitude: 2 * Math.sin(angle), max: 2};
  }
  function plot(kind, point, zh) {
    const x = u => left + (right - left) * u;
    const y = v => bottom - (bottom - top) * v / point.max;
    const points = [];
    for (let i = 0; i <= 120; i++) {
      const u = i / 120;
      const gradient = kind === 'moco' ? mocoGradient(0.10 + 0.90 * u).magnitude
        : 2 * Math.sin(Math.PI * u);
      points.push((i ? 'L' : 'M') + x(u).toFixed(2) + ' ' + y(gradient).toFixed(2));
    }
    const px = x(point.x).toFixed(2), py = y(point.magnitude).toFixed(2);
    const horizontal = kind === 'moco' ? 'τ' : 'φ (°)';
    const from = kind === 'moco' ? '0.10' : '0';
    const to = kind === 'moco' ? '1.00' : '180';
    const ordinate = kind === 'moco' ? '|∂L/∂s+|' : '|∂L/∂φ|';
    const accessible = kind === 'moco'
      ? (zh ? 'InfoNCE 正樣本相似度的梯度絕對值對溫度的曲線，現在的梯度為 ' : 'InfoNCE positive-similarity gradient magnitude against temperature, current value ') + fmt(point.magnitude)
      : (zh ? 'BYOL 損失對弧度角度的導數絕對值曲線，現在的梯度為 ' : 'BYOL loss derivative magnitude with respect to angle in radians, current value ') + fmt(point.magnitude);
    return '<svg class="ssl-gradient-plot" viewBox="0 0 ' + W + ' ' + H + '" role="img" aria-label="' + accessible + '">' +
      '<path d="M' + left + ' ' + top + ' V' + bottom + ' H' + right + '" fill="none" stroke="#718898" stroke-width="1.5"/>' +
      '<path d="M' + left + ' ' + y(point.max / 2).toFixed(2) + ' H' + right + '" stroke="#d8e3ea" stroke-dasharray="4 5"/>' +
      '<path d="' + points.join(' ') + '" fill="none" stroke="#087f83" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"/>' +
      '<path d="M' + px + ' ' + bottom + ' V' + py + '" stroke="#b66b40" stroke-width="2" stroke-dasharray="4 4"/>' +
      '<circle cx="' + px + '" cy="' + py + '" r="6" fill="#b66b40" stroke="#fff" stroke-width="2"/>' +
      '<text x="' + left + '" y="17" class="ssl-gradient-axis">' + ordinate + '</text>' +
      '<text x="' + (left - 8) + '" y="' + (bottom + 4) + '" text-anchor="end" class="ssl-gradient-axis">0</text>' +
      '<text x="' + (left - 8) + '" y="' + (top + 4) + '" text-anchor="end" class="ssl-gradient-axis">' + point.max.toFixed(1) + '</text>' +
      '<text x="' + left + '" y="146" class="ssl-gradient-axis">' + from + '</text>' +
      '<text x="' + right + '" y="146" text-anchor="end" class="ssl-gradient-axis">' + to + '</text>' +
      '<text x="' + ((left + right) / 2) + '" y="161" text-anchor="middle" class="ssl-gradient-axis">' + horizontal + '</text>' +
      '</svg>';
  }
  function enhance() {
    document.querySelectorAll('[data-self-supervised-lab]').forEach(host => {
      if (host.dataset.gradientReady) return;
      const kind = host.dataset.selfSupervisedLab;
      if (kind !== 'moco' && kind !== 'byol') return;
      const slider = host.querySelector('[data-act="loss"]');
      const panel = host.querySelector('.ssl-loss');
      if (!slider || !panel) return; // No JS or existing lab failed: keep fallback.
      host.dataset.gradientReady = 'yes';
      const zh = host.dataset.locale === 'zh-TW';
      const section = document.createElement('section');
      section.className = 'ssl-gradient';
      const title = document.createElement('div');
      title.className = 'ssl-gradient-heading';
      title.textContent = zh ? '損失梯度敏感度（示意數值）' : 'Loss gradient sensitivity (toy inputs)';
      const graphic = document.createElement('div');
      graphic.className = 'ssl-gradient-graphic';
      const readout = document.createElement('output');
      readout.className = 'ssl-gradient-readout';
      readout.setAttribute('aria-live', 'off');
      const note = document.createElement('p');
      note.className = 'ssl-gradient-note';
      note.textContent = kind === 'moco'
        ? (zh ? '這是損失對正樣本相似度的偏導數，不是編碼器權重梯度。固定示意相似度下，極小溫度可能使 Softmax 飽和，梯度不一定最大。'
          : 'Derivative with respect to positive similarity, not encoder weights. With these fixed toy similarities, very low temperature can saturate softmax, so its gradient need not be largest.')
        : (zh ? '導數是對夾角 φ（弧度）計算，不是對目標網路權重求梯度；停止梯度仍阻斷目標分支的反向傳播。'
          : 'Derivative is with respect to angle φ in radians, not target-network weights; stop-gradient still blocks target backpropagation.');
      section.append(title, graphic, readout, note);
      panel.after(section);
      const update = () => {
        const p = snapshot(kind, Number(slider.value));
        graphic.innerHTML = plot(kind, p, zh);
        readout.textContent = kind === 'moco'
          ? '∂L/∂s+ = (P(+) − 1)/τ = ' + fmt(p.derivative) + ' · Σ∂L/∂s− = +' + fmt(p.magnitude)
          : 'φ = ' + (p.value * 180 / Math.PI).toFixed(1) + '° · ∂L/∂φ = 2sinφ = ' + fmt(p.derivative) + ' rad⁻¹';
      };
      slider.addEventListener('input', update);
      update();
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', enhance);
  else enhance();
  if (window.document$ && typeof window.document$.subscribe === 'function') window.document$.subscribe(enhance);
})();
