/* CC BY-SA 4.0 — original causal counterfactuals for MoCo and BYOL.
 * The fixed similarities and gradient routes are teaching constructs, not measurements.
 * Reuses the existing native loss slider; never creates a timer or extra controls.
 */
(() => {
  'use strict';
  const similarities = [-.20, -.10, 0, .10, .20, .05];
  const esc = x => String(x).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const f = x => x.toFixed(3);
  function probability(tau, negatives) {
    // Shift by the positive similarity to avoid unnecessarily large exponentials.
    return 1 / (1 + negatives.reduce((s, n) => s + Math.exp((n - .70) / tau), 0));
  }
  function moco(tau, zh) {
    const good = probability(tau, similarities);
    const early = probability(tau, [...similarities.slice(1), .70]);
    const row = (name, letters, p, y, wrong) => {
      let result = `<text x="18" y="${y+23}" class="ssl-causal-label">${name}</text>`;
      letters.forEach((key, i) => {
        const x = 150 + i * 63, contaminated = wrong && i === 5;
        result += `<rect x="${x}" y="${y}" width="53" height="35" rx="6" fill="${contaminated?'#ffe3d9':'#e5f0f4'}" stroke="${contaminated?'#b94d32':'#95b0be'}" stroke-width="${contaminated?2:1}"/>`;
        result += `<text x="${x+26.5}" y="${y+24}" text-anchor="middle" class="ssl-causal-token">${key}</text>`;
      });
      result += `<rect x="150" y="${y+43}" width="368" height="10" rx="5" fill="#f1d5cd"/>`;
      result += `<rect x="150" y="${y+43}" width="${(368*p).toFixed(2)}" height="10" rx="5" fill="#168574"/>`;
      result += `<text x="533" y="${y+52}" class="ssl-causal-number">P+ ${f(p)}</text>`;
      return result;
    };
    const svg = `<svg viewBox="0 0 640 209" role="img" aria-label="${esc(zh?'MoCo：正確的損失前舊佇列，與錯誤提前入列造成假負樣本的比較':'MoCo: correct old queue versus an incorrect premature enqueue that makes the positive key a false negative')}">`+
      '<rect x="1" y="1" width="638" height="207" rx="11" fill="#f8fbfd" stroke="#b9cbd6"/>'+
      '<text x="18" y="27" class="ssl-causal-title">Queue timing</text>'+
      `<text x="620" y="27" text-anchor="end" class="ssl-causal-label">τ = ${tau.toFixed(2)}</text>`+
      row('Correct', ['A','B','C','D','E','F'], good, 39, false)+
      row('Too early', ['B','C','D','E','F','G'], early, 115, true)+
      '<text x="18" y="196" class="ssl-causal-foot">G = positive key · red G = false negative</text></svg>';
    return {svg, readout: (zh?'正確':'Correct')+` L=${f(-Math.log(good))} · `+(zh?'提前入列':'Early enqueue')+` L=${f(-Math.log(early))}`};
  }
  function byol(cosine, zh) {
    const angle = Math.acos(Math.max(-1, Math.min(1, cosine)));
    const sensitivity = 2 * Math.sin(angle);
    const row = (label, y, stopped) => {
      const mid = y + 20;
      return `<text x="17" y="${y-7}" class="ssl-causal-label">${label}</text>`+
        `<rect x="85" y="${y}" width="118" height="41" rx="8" fill="#dcecf5" stroke="#6d9ebc"/>`+
        `<rect x="435" y="${y}" width="118" height="41" rx="8" fill="#dff1e9" stroke="#75ab98"/>`+
        `<rect x="272" y="${y+2}" width="95" height="37" rx="8" fill="#f1f2f6" stroke="#adb4c4"/>`+
        `<text x="144" y="${y+26}" text-anchor="middle" class="ssl-causal-token">Online</text>`+
        `<text x="482" y="${y+26}" text-anchor="middle" class="ssl-causal-token">Target</text>`+
        `<text x="319" y="${y+26}" text-anchor="middle" class="ssl-causal-token">Loss</text>`+
        `<path d="M272 ${mid} H207" stroke="#c07440" stroke-width="4" marker-end="url(#ssl-causal-arrow)"/>`+
        (stopped
          ? `<path d="M368 ${mid} H419" stroke="#b25e66" stroke-width="3" stroke-dasharray="5 5"/><path d="M403 ${mid-9} l12 18 m0 -18 l-12 18" stroke="#b25e66" stroke-width="3"/>`
          : `<path d="M368 ${mid} H431" stroke="#c07440" stroke-width="4" marker-end="url(#ssl-causal-arrow)"/>`);
    };
    const svg = `<svg viewBox="0 0 640 236" role="img" aria-label="${esc(zh?'BYOL：停止梯度只讓線上分支接受損失梯度；未停止梯度的反事實比較':'BYOL: loss-gradient routing with target stop-gradient versus a counterfactual without it')}">`+
      '<defs><marker id="ssl-causal-arrow" markerWidth="5" markerHeight="5" refX="4" refY="2.5" orient="auto"><path d="M0 0 L5 2.5 L0 5 Z" fill="#c07440"/></marker></defs>'+
      '<rect x="1" y="1" width="638" height="234" rx="11" fill="#f8fbfd" stroke="#b9cbd6"/>'+
      '<text x="18" y="27" class="ssl-causal-title">Loss-gradient routes</text>'+
      row('Stop-grad', 54, true)+row('No stop-grad (what-if)', 138, false)+
      '<path d="M203 214 H435" stroke="#168574" stroke-width="2.5" stroke-dasharray="7 5"/>'+
      '<text x="320" y="207" text-anchor="middle" class="ssl-causal-foot">EMA ≠ backprop</text></svg>';
    return {svg, readout:`φ=${(angle*180/Math.PI).toFixed(1)}° · |dL/dφ|=${f(sensitivity)} rad⁻¹`};
  }
  function enhance() {
    document.querySelectorAll('[data-self-supervised-lab]').forEach(host => {
      if (host.dataset.causalReady) return;
      const kind = host.dataset.selfSupervisedLab;
      if (kind !== 'moco' && kind !== 'byol') return;
      const slider = host.querySelector('[data-act="loss"]');
      const panel = host.querySelector('.ssl-loss');
      if (!slider || !panel) return;
      host.dataset.causalReady = 'yes';
      const zh = host.dataset.locale === 'zh-TW';
      const section = document.createElement('section');
      section.className = 'ssl-causal';
      const heading = document.createElement('div');
      heading.className = 'ssl-causal-heading';
      heading.textContent = kind === 'moco'
        ? (zh ? '反事實比較：如果在計算損失前就入列？' : 'Counterfactual: what if enqueue happened before loss?')
        : (zh ? '反事實比較：停止梯度阻斷哪條路徑？' : 'Counterfactual: which route does stop-gradient block?');
      const graphic = document.createElement('div');
      graphic.className = 'ssl-causal-graphic';
      const output = document.createElement('output');
      output.className = 'ssl-causal-readout';
      output.setAttribute('aria-live', 'off');
      const note = document.createElement('p');
      note.className = 'ssl-causal-note';
      note.textContent = kind === 'moco'
        ? (zh ? '正確的 MoCo 先以舊佇列計算 InfoNCE，再入列新鍵 G。下方是刻意設計的錯誤操作：若 G 同時是正樣本與負樣本，損失會被人為拉高。使用固定示意相似度，不是實測。'
          : 'MoCo contrasts against the old queue, then enqueues G. The lower row deliberately violates this order: the positive G also becomes a false negative, inflating the toy loss. Similarities are fixed illustrations, not measurements.')
        : (zh ? '橘色箭頭僅表示可能的損失梯度路徑，不代表實際網路權重梯度大小。BYOL 只對線上分支反向傳播；目標分支透過獨立的 EMA 更新。下方未停止梯度的情況是反事實，不是 BYOL 訓練設定。'
          : 'Orange arrows indicate possible loss-gradient routes, not measured weight-gradient magnitudes. BYOL backpropagates only through online; target updates separately by EMA. The lower no-stop-gradient case is a counterfactual, not BYOL training.');
      section.append(heading, graphic, output, note);
      panel.after(section);
      const update = () => {
        const value = Number(slider.value);
        const result = kind === 'moco' ? moco(value, zh) : byol(value, zh);
        graphic.innerHTML = result.svg;
        output.textContent = result.readout;
      };
      slider.addEventListener('input', update);
      update();
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', enhance);
  else enhance();
  if (window.document$ && typeof window.document$.subscribe === 'function') window.document$.subscribe(enhance);
})();
