/* Original bilingual numerical demonstrations for causal inference. No external dependencies. */
(function causalLabs() {
  'use strict';
  const copy = {
    en: {
      target: 'Target U=1 share', selected: 'Selection rate for (0,0)',
      reset: 'Reset example', observed: 'Observed, unadjusted', standard: 'Standardised target population',
      baseline: 'Original population: U=1 at 0.50',
      separate: 'Original treatment groups have different U mixtures: 0.20 / 0.80.',
      invariant: 'The risk difference remains 0.40 because treatment effect is constant in this constructed model.',
      retention: 'Other three cells are always retained. Changing (0,0) retention changes the selected sample, not the original joint population.',
      initial: 'Before selection X and Y are independent: both conditional risks are 0.50.',
      caveat: 'Constructed probabilities; neither visualization estimates an empirical causal effect.',
      eligible: 'Retained share', subgroup: 'Conditional outcome risk',
      selection: 'Selection-conditioned association', weight: 'Shared confounder weight',
    },
    zh: {
      target: '目標母體 U=1 比例', selected: '(0,0) 樣本保留率',
      reset: '重設示例', observed: '未調整的觀察組別', standard: '標準化目標母體',
      baseline: '原始母體：U=1 比例為 0.50',
      separate: '原始治療組別的 U 分布不同：0.20 / 0.80。',
      invariant: '此人工模型的處理效果固定，因此風險差始終為 0.40。',
      retention: '其餘三種組合全部保留。改變 (0,0) 的保留率，只會改變入選樣本，不會改變原始聯合分布。',
      initial: '選取前 X 與 Y 獨立，兩組的條件結果風險都是 0.50。',
      caveat: '所有機率皆為人工設定，並非真實研究中的因果效應估計。',
      eligible: '保留比例', subgroup: '條件結果風險',
      selection: '經選取後的統計關聯', weight: '共同混淆因子權重',
    },
  };
  const format = (n) => n.toFixed(2);
  const bar = (name, label, colour) => `<div class="causal-lab-series"><span class="causal-lab-key">${label}</span><div class="causal-lab-track"><span class="causal-lab-fill ${colour}" data-bar="${name}"></span></div><output data-value="${name}">0.00</output></div>`;
  function mount(root) {
    if (root.dataset.ready === '1') return;
    const kind = root.dataset.causalLab;
    if (!['backdoor', 'collider'].includes(kind)) return;
    const isZh = root.closest('[lang="zh-TW"]') || document.documentElement.lang.toLowerCase().startsWith('zh') || root.dataset.lang === 'zh';
    const t = copy[isZh ? 'zh' : 'en'];
    const backdoor = kind === 'backdoor';
    const title = backdoor ? t.target : t.selected;
    const message = backdoor ? t.invariant : t.retention;
    const description = backdoor ? t.separate : t.initial;
    root.innerHTML = `<div class="causal-lab-panel"><div class="causal-lab-toolbar"><label>${title} <output class="causal-lab-current" data-current>0.50</output><input type="range" min="0" max="100" value="${backdoor ? 50 : 0}" step="5" data-control aria-label="${title}" aria-valuetext="${backdoor ? '0.50' : '0.00'}"></label><button type="button" data-reset>${t.reset}</button></div><div class="causal-lab-graphic" role="group" aria-label="${backdoor ? t.standard : t.selection}"><div class="causal-lab-explainer">${backdoor ? t.weight : t.eligible}</div><div class="causal-lab-cells">${(backdoor ? ['U=0', 'U=1'] : ['00', '01', '10', '11']).map(k => `<div class="causal-lab-cell" data-cell="${k}"><span>${k}</span></div>`).join('')}</div><div class="causal-lab-caption">${t.subgroup}</div>${bar('a','X=0','coral')}${bar('b','X=1','teal')}<div class="causal-lab-delta"><span>${backdoor ? t.standard : t.selection}</span><output data-delta>0.40</output></div></div><p class="causal-lab-context">${description} ${message}</p><p class="causal-lab-context">${backdoor ? t.baseline + " " : ""}${t.caveat}</p><p class="causal-lab-live" role="status" aria-live="polite" aria-atomic="true" data-status></p></div>`;
    const control = root.querySelector('[data-control]');
    const output = root.querySelector('[data-current]');
    const draw = () => {
      const fraction = Number(control.value) / 100;
      const p0 = backdoor ? 0.1 + 0.4 * fraction : 1 / (1 + fraction);
      const p1 = backdoor ? 0.5 + 0.4 * fraction : 0.5;
      const riskDifference = p1 - p0;
      output.textContent = format(fraction);
      control.setAttribute('aria-valuetext', format(fraction));
      for (const [key, prob] of [['a', p0], ['b', p1]]) {
        root.querySelector(`[data-bar="${key}"]`).style.width = `${(100 * prob).toFixed(2)}%`;
        root.querySelector(`[data-value="${key}"]`).textContent = format(prob);
      }
      root.querySelector('[data-delta]').textContent = `${riskDifference > 0 ? '+' : ''}${format(riskDifference)}`;
      for (const cell of root.querySelectorAll('[data-cell]')) {
        const key = cell.dataset.cell;
        const share = backdoor ? (key === 'U=1' ? fraction : 1-fraction) : (key === '00' ? fraction : 1);
        cell.style.setProperty('--cell-share', share.toFixed(3));
        cell.title = `${key}: ${format(share)}`;
      }
      root.querySelector('[data-status]').textContent = backdoor
        ? `U=1 ${format(fraction)}; X=0 ${format(p0)}; X=1 ${format(p1)}; Δ +${format(riskDifference)}`
        : `(0,0) ${format(fraction)}; X=0 ${format(p0)}; X=1 ${format(p1)}; Δ ${format(riskDifference)}`;
    };
    control.addEventListener('input', draw);
    root.querySelector('[data-reset]').addEventListener('click', () => { control.value = backdoor ? 50 : 0; draw(); control.focus(); });
    root.dataset.ready = '1';
    draw();
  }
  function enhance(root = document) {root.querySelectorAll('[data-causal-lab]').forEach(mount);}
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', () => enhance());
  else enhance();
  if (window.document$?.subscribe) window.document$.subscribe(() => enhance());
})();
